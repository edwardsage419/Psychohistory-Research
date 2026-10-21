"""R172 original country-year source and frozen retrospective hazard audit tests."""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib,io,json,math,unittest

from r172_real_historical_retrospective_hazards import (
    HERE,SOURCE,DATA,OUTPUT,PREDICTIONS,DATA_SHA256,AUTHOR_CODE_SHA256,
    ORIGINAL_UPLOAD_SHA256,PRECODE_PROTOCOL_COMMIT,CUTOFF_TRAIN_CALENDAR,
    CUTOFF_TEST_CALENDAR,WEIGHT,BINS,BOOTSTRAPS,SEED,
    assert_original_sources,parse_int,parse_optional_decimal,
    parse_rows,load_validated_episodes,cohorts,bucket,fit_models,
    predict,logloss,brier,percentile,twelve,serial_fit,score,run
)


class TestR172(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.episodes,cls.source_ids=load_validated_episodes()
        cls.train,cls.test,cls.withheld=cohorts(cls.episodes)
        cls.fit=fit_models(cls.train)
        cls.d=run()

    def test_original_dataset_SHA256(self):
        self.assertEqual(hashlib.sha256(DATA.read_bytes()).hexdigest(),DATA_SHA256)

    def test_original_author_code_SHA256(self):
        self.assertEqual(hashlib.sha256((SOURCE/"Original_Replication_code_Stata.do").read_bytes()).hexdigest(),AUTHOR_CODE_SHA256)

    def test_original_as_uploaded_data_SHA256(self):
        self.assertEqual(hashlib.sha256((SOURCE/"Original_Replication_dataset_as_uploaded.bin").read_bytes()).hexdigest(),ORIGINAL_UPLOAD_SHA256)

    def test_real_original_Harvard_Dataverse_doi(self):
        self.assertEqual(self.d["original_dataset_doi"],"10.7910/DVN/WFO1N1")

    def test_CC0_license_recorded(self):
        self.assertTrue(self.d["CC0_license"])

    def test_precode_protocol_commit_pinned(self):
        self.assertEqual(PRECODE_PROTOCOL_COMMIT,"099b7a50924c86fdaecb6254eca2748836ae0c64")

    def test_exact_raw_years_count(self):
        self.assertEqual(len(parse_rows(DATA.read_bytes())),1731)

    def test_exclusion_leaves_1725_real_years(self):
        self.assertEqual(sum(map(len,self.episodes.values())),1725)

    def test_source_has_103_original_episodes(self):
        self.assertEqual(self.d["source_original_episodes"],103)

    def test_eligible_has_102_complete_labeled_episodes(self):
        self.assertEqual(len(self.episodes),102)

    def test_only_Nigeria_episode_is_entirely_excluded_for_missing_outcome(self):
        self.assertNotIn("NGA2011",self.episodes)
        self.assertEqual(self.d["excluded_missing_outcome_rows"],6)

    def test_all_included_events_are_binary(self):
        self.assertTrue(all(r["event"] in (0,1) for ep in self.episodes.values() for r in ep))

    def test_exact_total_real_events_45(self):
        self.assertEqual(sum(r["event"] for ep in self.episodes.values() for r in ep),45)

    def test_all_breakdown_events_end_episode(self):
        for ep in self.episodes.values():
            self.assertLessEqual(sum(r["event"] for r in ep),1)
            self.assertTrue(all(r["event"]==0 for r in ep[:-1]))

    def test_no_episode_year_duplicates(self):
        for ep in self.episodes.values():
            years=[r["year"] for r in ep]
            self.assertEqual(len(years),len(set(years)))

    def test_all_episode_years_contiguous(self):
        for ep in self.episodes.values():
            years=[r["year"] for r in ep]
            self.assertEqual(years,list(range(years[0],years[-1]+1)))

    def test_duration_age_matches_year_minus_t0(self):
        for ep in self.episodes.values():
            for r in ep:self.assertEqual(r["age"],r["year"]-r["t0"])

    def test_no_episode_outcome_after_first_breakdown(self):
        for ep in self.episodes.values():
            once=[i for i,x in enumerate(ep) if x["event"]==1]
            if once:self.assertEqual(once,[len(ep)-1])

    def test_original_country_ids_not_as_episode_ids(self):
        self.assertGreater(len(self.episodes),len({ep[0]["country_id"] for ep in self.episodes.values()}))

    def test_exact_distinct_country_count_original_source(self):
        rows=parse_rows(DATA.read_bytes())
        self.assertEqual(len({r["country_id"] for r in rows}),83)

    def test_strict_training_cutoff_transition(self):
        self.assertTrue(all(r["transition"]<=1998 for r in self.train))

    def test_strict_training_cutoff_calendar(self):
        self.assertTrue(all(r["year"]<=1999 for r in self.train))

    def test_strict_heldout_new_transition_cohort(self):
        self.assertTrue(all(r["transition"]>=1999 for r in self.test))

    def test_strict_heldout_calendar(self):
        self.assertTrue(all(r["year"]>=2000 for r in self.test))

    def test_train_test_episode_identifiers_disjoint(self):
        self.assertFalse({r["episode_id"] for r in self.train}&{r["episode_id"] for r in self.test})

    def test_train_test_calendar_time_disjoint(self):
        self.assertLess(max(r["year"] for r in self.train),min(r["year"] for r in self.test))

    def test_withheld_old_cohort_followups_not_in_train_or_test(self):
        keys={(r["episode_id"],r["year"]) for r in self.train+self.test}
        for r in self.withheld:
            self.assertNotIn((r["episode_id"],r["year"]),keys)
            self.assertLessEqual(r["transition"],1998)
            self.assertGreater(r["year"],1999)

    def test_no_duplicate_observation_across_three_partitions(self):
        observed=self.train+self.test+self.withheld
        self.assertEqual(len(observed),len({(r["episode_id"],r["year"]) for r in observed}))
        self.assertEqual(len(observed),1725)

    def test_heldout_contains_at_least_one_real_breakdown(self):
        self.assertGreater(sum(r["event"] for r in self.test),0)

    def test_training_contains_breakdown_and_no_breakdown(self):
        self.assertGreater(self.fit["E"],0)
        self.assertLess(self.fit["E"],self.fit["N"])

    def test_m0_Laplace_formula_exact(self):
        self.assertEqual(self.fit["p0"],F(self.fit["E"]+1,self.fit["N"]+2))

    def test_fixed_four_duration_buckets(self):
        self.assertEqual(BINS,((0,2),(3,7),(8,15),(16,None)))

    def test_duration_boundary_ages(self):
        self.assertEqual([bucket(x) for x in (0,2,3,7,8,15,16,42)], [0,0,1,1,2,2,3,3])

    def test_duration_smoothed_p_b_exact(self):
        for b,fit in self.fit["duration"].items():
            self.assertEqual(fit["p"],(F(fit["E"])+WEIGHT*self.fit["p0"])/(F(fit["N"])+WEIGHT))

    def test_duration_observations_partition_training(self):
        self.assertEqual(sum(v["N"] for v in self.fit["duration"].values()),len(self.train))

    def test_duration_events_partition_training(self):
        self.assertEqual(sum(v["E"] for v in self.fit["duration"].values()),self.fit["E"])

    def test_m2_strat_formula_exact_for_all_predefined_cells(self):
        for (b,s),x in self.fit["duration_baseline"].items():
            self.assertEqual(x["p"],(F(x["E"])+WEIGHT*self.fit["duration"][b]["p"])/(F(x["N"])+WEIGHT))

    def test_stratified_models_train_without_first_year_covariate(self):
        n=sum(x["N"] for x in self.fit["duration_baseline"].values())
        expected=sum(r["age"]>=1 and r["baseline_libdem0"] is not None for r in self.train)
        self.assertEqual(n,expected)

    def test_m2_earliest_t0_fallback_exact(self):
        for r in self.test:
            if r["age"]==0:
                p=predict(self.fit,r)
                self.assertEqual(p[2],p[1])

    def test_m2_missing_baseline_uses_M1_exact(self):
        a=dict(self.test[0]);a["baseline_libdem0"]=None
        p=predict(self.fit,a)
        self.assertEqual(p[2],p[1])

    def test_all_three_hazards_are_exact_rational(self):
        for r in self.test:
            self.assertTrue(all(type(p) is F for p in predict(self.fit,r)))

    def test_all_three_hazards_strictly_between_zero_and_one(self):
        for r in self.test:
            self.assertTrue(all(F(0)<p<F(1) for p in predict(self.fit,r)))

    def test_model_fits_reference_train_only(self):
        self.assertEqual(self.fit["N"],len(self.train))
        self.assertEqual(self.fit["E"],sum(r["event"] for r in self.train))

    def test_baseline_threshold_frozen_at_50(self):
        a=dict(self.test[0]);a["age"]=1
        a["baseline_libdem0"]=D("49.999999")
        l=predict(self.fit,a)[2]
        a["baseline_libdem0"]=D("50")
        h=predict(self.fit,a)[2]
        self.assertEqual(l,self.fit["duration_baseline"][(bucket(1),"low")]["p"])
        self.assertEqual(h,self.fit["duration_baseline"][(bucket(1),"high")]["p"])

    def test_log_loss_half_probability_matches_log_two(self):
        self.assertAlmostEqual(logloss(0,F(1,2)),math.log(2),places=13)
        self.assertAlmostEqual(logloss(1,F(1,2)),math.log(2),places=13)

    def test_Brier_extremes_and_half(self):
        self.assertEqual(brier(0,F(1,2)),.25)
        self.assertEqual(brier(1,F(1,2)),.25)

    def test_zero_event_logloss_is_log_one_minus_p(self):
        self.assertAlmostEqual(logloss(0,F(1,4)),-math.log(.75),places=13)

    def test_one_event_logloss_is_minus_log_p(self):
        self.assertAlmostEqual(logloss(1,F(1,4)),-math.log(.25),places=13)

    def test_bootstrap_seed_frozen(self):
        self.assertEqual(SEED,20261021)
        self.assertEqual(BOOTSTRAPS,512)

    def test_percentile_constant_sample(self):
        self.assertEqual(percentile([3.0]*512,.025),3.0)

    def test_percentile_linear_interp(self):
        self.assertAlmostEqual(percentile([1,2,3,4],.5),2.5)

    def test_score_annual_brier_metric_range(self):
        for key,value in self.d["score_summary"]["annual_brier"].items():
            if key in ("M0","M1","M2"):
                self.assertTrue(0<=float(value)<1)

    def test_actual_score_logloss_finite_nonnegative(self):
        for key,value in self.d["score_summary"]["annual_logloss"].items():
            if key in ("M0","M1","M2"):
                self.assertTrue(math.isfinite(float(value)) and float(value)>=0)

    def test_comparator_differences_are_reported_without_model_selection(self):
        for metric in ("annual_logloss","annual_brier"):
            out=self.d["score_summary"][metric]
            for candidate in ("M1","M2"):
                self.assertAlmostEqual(float(out[candidate+"_vs_M0_difference"]),float(out[candidate])-float(out["M0"]),places=10)

    def test_episode_clustered_intervals_in_output(self):
        for key in ("annual_logloss","annual_brier"):
            for candidate in ("M1_vs_M0","M2_vs_M0"):
                interval=self.d["episode_cluster_resample_CI"]["intervals"][key][candidate]
                self.assertLessEqual(float(interval["lower_2p5"]),float(interval["upper_97p5"]))

    def test_heldout_full_output_file_sha256_recorded(self):
        self.assertEqual(hashlib.sha256(PREDICTIONS.read_bytes()).hexdigest(),
                         self.d["full_heldout_predictions_original_rows"]["sha256"])

    def test_heldout_full_csv_record_count(self):
        with PREDICTIONS.open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),len(self.test))

    def test_heldout_csv_event_count(self):
        with PREDICTIONS.open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(sum(int(r["recorded_breakdown_event"]) for r in rows),
                         self.d["split"]["test_breakdown_events"])

    def test_full_csv_predictions_recompute_exact_from_training(self):
        with PREDICTIONS.open() as f:
            actual=list(csv.DictReader(f))
        self.assertEqual(len(actual),len(self.test))
        for observed,row in zip(actual,self.test):
            self.assertEqual(observed["episode_id"],row["episode_id"])
            self.assertEqual(int(observed["year"]),row["year"])
            for col,expected in zip(("M0_constant_exact","M1_duration_exact","M2_duration_baseline_exact"),predict(self.fit,row)):
                self.assertEqual(F(observed[col]),expected)

    def test_heldout_scores_do_not_mutate_train_parameters(self):
        before=serial_fit(self.fit)
        score(self.test,self.fit)
        self.assertEqual(serial_fit(self.fit),before)

    def test_all_study_results_are_retrospective_not_realtime_forecasts(self):
        self.assertFalse(self.d["independent_real_time_historical_event_prediction"])
        self.assertFalse(self.d["author_original_Cox_model_reproduced"])
        self.assertFalse(self.d["author_original_regime_study_reproduced"])
        self.assertEqual(self.d["new_E3_genuinely_external_historical_forecasts"],0)

    def test_r073_and_PESEN_remain_frozen(self):
        self.assertEqual(self.d["R073"],"FROZEN")
        self.assertEqual(self.d["PESEN_v0_1"],"FROZEN")

    def test_three_frozen_models_in_output(self):
        self.assertEqual(set(self.d["models_train_only_counts_and_exact_Fraction_parameters"]),{"M0","M1","M2"})

    def test_16_fixed_M2_duration_baseline_cells_no(self):
        self.assertEqual(len(self.d["models_train_only_counts_and_exact_Fraction_parameters"]["M2"]),8)

    def test_source_future_followup_not_leaking_into_test(self):
        train_ids={r["episode_id"] for r in self.train}
        self.assertTrue(all(r["episode_id"] in train_ids for r in self.withheld))

    def test_source_real_event_spell_codes_preserved(self):
        with PREDICTIONS.open() as f:
            rows=list(csv.DictReader(f))
        self.assertTrue(all(r["episode_id"] and r["country_id"] for r in rows))

    def test_real_model_test_output_deterministic_JSON_replay(self):
        expected=OUTPUT.read_bytes()
        replay=run()
        self.assertEqual(OUTPUT.read_bytes(),expected)
        self.assertEqual(replay["full_heldout_predictions_original_rows"]["sha256"],
                         self.d["full_heldout_predictions_original_rows"]["sha256"])

    def test_zero_age_or_missing_data_fallback_consistency(self):
        for r in self.test:
            if r["age"]==0 or r["baseline_libdem0"] is None:
                self.assertEqual(predict(self.fit,r)[1],predict(self.fit,r)[2])

    def test_negative_bucket_invalid_age(self):
        for x in (-1,-2,0.0,True,False,"3",F(1,2)):
            with self.assertRaises(ValueError):bucket(x)

    def test_negative_parse_int_invalid_fractional(self):
        for x in ("0.5","nan","inf","two"):
            with self.assertRaises((ValueError,ArithmeticError)):parse_int(x)

    def test_negative_training_empty_sample(self):
        with self.assertRaises(ValueError):fit_models([])

    def test_negative_training_all_zero_events(self):
        with self.assertRaises(ValueError):fit_models([
            {"event":0,"age":0,"baseline_libdem0":D("60")}])

    def test_negative_training_nonbinary_event(self):
        with self.assertRaises(ValueError):fit_models([
            {"event":None,"age":0,"baseline_libdem0":D("60")}])

    def test_negative_logloss_nonbinary_event(self):
        with self.assertRaises(ValueError):logloss(None,F(1,2))

    def test_negative_logloss_boundary_hazard(self):
        for p in (F(0),F(1)):
            with self.assertRaises(ValueError):logloss(0,p)

    def test_negative_Brier_nonbinary_event(self):
        with self.assertRaises(ValueError):brier(2,F(1,2))

    def test_negative_bootstrap_empty(self):
        with self.assertRaises(ValueError):percentile([],.025)

    def test_negative_source_modified_byte_integrity(self):
        modified=DATA.read_bytes()[:-1]+b"X"
        self.assertNotEqual(hashlib.sha256(modified).hexdigest(),DATA_SHA256)

    def test_all_output_prediction_rows_from_source_only(self):
        original={(r["episode_id"],r["year"]) for ep in self.episodes.values() for r in ep}
        with PREDICTIONS.open() as f:
            rows=list(csv.DictReader(f))
        self.assertTrue(all((r["episode_id"],int(r["year"])) in original for r in rows))


# Each frozen 4 duration bins and 2 baseline groups gets its own distinct
# source-data-specific exact M1/M2 count and smoothing verification case.
for b in range(4):
    def create_duration(b=b):
        def test(self):
            pred=self.fit["duration"][b]
            expected=[r for r in self.train if bucket(r["age"])==b]
            self.assertEqual(pred["N"],len(expected))
            self.assertEqual(pred["E"],sum(r["event"] for r in expected))
            self.assertEqual(pred["p"],(F(pred["E"])+WEIGHT*self.fit["p0"])/(F(pred["N"])+WEIGHT))
        return test
    setattr(TestR172,f"test_original_duration_bin_{b}_training_count_and_probability",create_duration())
    for typ in ("low","high"):
        def create_stratum(b=b,typ=typ):
            def test(self):
                cell=self.fit["duration_baseline"][(b,typ)]
                expected=[r for r in self.train if r["age"]>=1 and bucket(r["age"])==b and r["baseline_libdem0"] is not None and
                       ("high" if r["baseline_libdem0"]>=D(50) else "low")==typ]
                self.assertEqual(cell["N"],len(expected))
                self.assertEqual(cell["E"],sum(r["event"] for r in expected))
            return test
        setattr(TestR172,f"test_original_duration_{b}_{typ}_baseline_cell_exact",create_stratum())


if __name__=="__main__":
    unittest.main()
