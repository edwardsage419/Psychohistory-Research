"""R187 exact ordinal proportional-odds versus threshold-specific grid inference.

12 strictly prescored artificial three-level response worlds, 1950 complete
multinomial count tables and 325 unique training profiles. Every model
probability, likelihood and source mass uses exact Fraction. Independent
future responses are evaluated by float and high-precision Decimal log loss.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product,combinations_with_replacement
from math import factorial,log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R187_ORDINAL_PO_12_WORLDS_1950_TABLES_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R187_EXACT_RESULTS.json"
SAMPLES=HERE/"R187_ALL_1950_ORDINAL_TRAINING_TABLES.csv"
LIBRARY=HERE/"R187_ALL_325_ORDINAL_FIT_PROFILES.json"
ACCEPT=HERE/"R187_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R187_Exact_Ordinal_PO_12_Worlds_Archive.zip"

ODDS=(F(1,4),F(1,2),F(1),F(2),F(4))
FACTORS=(F(1,2),F(1),F(2),F(4))
M_VALUES=(3,4)
SOURCE_SCENARIOS=(
 ("NULL",F(1,2),F(2),F(1),F(1),True),
 ("PARALLEL_UP",F(1,2),F(2),F(2),F(2),True),
 ("PARALLEL_DOWN",F(1,2),F(2),F(1,2),F(1,2),True),
 ("DIVERGENT",F(1,2),F(2),F(1,2),F(2),False),
 ("COMPRESS",F(1,2),F(2),F(2),F(1),False),
 ("CROSSED_THRESHOLDS",F(1,4),F(4),F(2),F(1,2),False),
)


def ordinal_pmf_cdf(odds0,odds1):
    """Route A: cumulative odds transformed to successive differences."""
    if odds0<=0 or odds1<=odds0:
        raise ValueError("ordinal cutoff odds must be strictly ordered and positive")
    f0=odds0/(1+odds0)
    f1=odds1/(1+odds1)
    return f0,f1-f0,1-f1


def ordinal_pmf_algebra(odds0,odds1):
    """Route B: independent explicit rational normalized odds differences."""
    if odds0<=0 or odds1<=odds0:
        raise ValueError("invalid ordinal odds")
    return odds0/(1+odds0), (odds1-odds0)/((1+odds0)*(1+odds1)), F(1)/(1+odds1)


def model_probabilities(base0,base1,t0,t1):
    if base0 not in ODDS or base1 not in ODDS or t0 not in FACTORS or t1 not in FACTORS:
        raise ValueError("model parameters outside frozen grid")
    if not (base0<base1 and base0*t0<base1*t1):
        raise ValueError("invalid ordered cumulative probability in one condition")
    group0=ordinal_pmf_cdf(base0,base1)
    group1=ordinal_pmf_cdf(base0*t0,base1*t1)
    if group0!=ordinal_pmf_algebra(base0,base1) or group1!=ordinal_pmf_algebra(base0*t0,base1*t1):
        raise AssertionError("two independent ordinal probability constructions differ")
    if sum(group0,F(0))!=1 or sum(group1,F(0))!=1 or min(group0+group1)<=0:
        raise AssertionError("invalid ordinal source PMFs")
    return group0,group1


def worlds():
    for source,m in product(SOURCE_SCENARIOS,M_VALUES):
        name,o0,o1,t0,t1,is_po=source
        yield name,m,o0,o1,t0,t1,is_po


@lru_cache(maxsize=None)
def candidate_grid():
    # Candidate ordering establishes an immutable tie resolution protocol.
    po=[]
    flexible=[]
    for o0 in ODDS:
        for o1 in ODDS:
            if o0>=o1:
                continue
            for t0 in FACTORS:
                for t1 in FACTORS:
                    if o0*t0>=o1*t1:
                        continue
                    spec=(o0,o1,t0,t1,*model_probabilities(o0,o1,t0,t1))
                    flexible.append(spec)
                    if t0==t1:
                        po.append(spec)
    if len(po)!=40 or not all(x in flexible for x in po):
        raise AssertionError("proportional odds candidate grid not nested as frozen")
    return tuple(po),tuple(flexible)


def count_vectors(m):
    if m not in M_VALUES:
        raise ValueError("unknown source group sample size")
    vectors=[]
    for ordered in combinations_with_replacement(range(3),m):
        freq=Counter(ordered)
        vectors.append((freq[0],freq[1],freq[2]))
    if len(vectors)!=(10 if m==3 else 15):
        raise AssertionError("ordinal count support not as frozen")
    return tuple(vectors)


def multinomial_mass(counts,pmf):
    m=sum(counts)
    if len(counts)!=3 or any(not isinstance(x,int) or x<0 for x in counts) or m not in M_VALUES:
        raise ValueError("invalid three-level multinomial data")
    coefficient=F(factorial(m),factorial(counts[0])*factorial(counts[1])*factorial(counts[2]))
    return coefficient*pmf[0]**counts[0]*pmf[1]**counts[1]*pmf[2]**counts[2]


def likelihood_counts(group_counts,group_pmf):
    """A: exact likelihood with category count exponents, constants omitted."""
    v=F(1)
    for cnt,probs in zip(group_counts,group_pmf):
        for frequency,prob in zip(cnt,probs):
            v*=prob**frequency
    return v


def likelihood_individual_rows(group_counts,group_pmf):
    """B: expand each counted categorical observation and multiply individually."""
    v=F(1)
    for counts,probs in zip(group_counts,group_pmf):
        for category in range(3):
            for _ in range(counts[category]):
                v*=probs[category]
    return v


def fit_table(count0,count1):
    if sum(count0)!=sum(count1) or sum(count0) not in M_VALUES:
        raise ValueError("invalid prescored two-condition ordinal count table")
    m=sum(count0)
    po,flex=candidate_grid()
    best_po=None
    best_flex=None
    for spec in flex:
        o0,o1,t0,t1,prob0,prob1=spec
        trial=likelihood_counts((count0,count1),(prob0,prob1))
        alternate=likelihood_individual_rows((count0,count1),(prob0,prob1))
        if trial!=alternate:
            raise AssertionError("independent category likelihood formulas differ")
        if best_flex is None or trial>best_flex[0]:
            best_flex=(trial,spec)
        if t0==t1 and (best_po is None or trial>best_po[0]):
            best_po=(trial,spec)
    if best_po is None or best_flex is None or best_flex[0]<best_po[0]:
        raise AssertionError("nested exact ordinal models invalid")
    return {
        "m":m,"group0_counts":count0,"group1_counts":count1,
        "po_max_training_likelihood":best_po[0],
        "nonpo_max_training_likelihood":best_flex[0],
        "po_selected_odds":best_po[1][:4],
        "nonpo_selected_odds":best_flex[1][:4],
        "po_predictive_probabilities":best_po[1][4:],
        "nonpo_predictive_probabilities":best_flex[1][4:],
        "independent_CDF_algebra_and_full_likelihood_paths_equal":True,
    }


@lru_cache(maxsize=None)
def fit_library():
    lib={}
    for m in M_VALUES:
        for c0,c1 in product(count_vectors(m),repeat=2):
            lib[(m,c0,c1)]=fit_table(c0,c1)
    if len(lib)!=325:
        raise AssertionError("prescored 325 ordinal count tables are missing")
    return lib


def loss_float(true_pmfs,fitted_pmfs):
    return -sum(float(v)*log(float(q))
                for p,qgroup in zip(true_pmfs,fitted_pmfs)
                for v,q in zip(p,qgroup))/2


def loss_decimal(true_pmfs,fitted_pmfs):
    with localcontext() as ctx:
        ctx.prec=60
        s=Decimal(0)
        for p,qgroup in zip(true_pmfs,fitted_pmfs):
            for v,q in zip(p,qgroup):
                s-=(Decimal(v.numerator)/Decimal(v.denominator))*(Decimal(q.numerator)/Decimal(q.denominator)).ln()/2
        return s


def world_eval(name,m,o0,o1,t0,t1,is_po,fits,rows):
    source_pmfs=model_probabilities(o0,o1,t0,t1)
    allmass=F(0)
    strict_training_gain=F(0)
    po_risk=0.0
    flex_risk=0.0
    po_high=Decimal(0)
    flex_high=Decimal(0)
    n_tables=0
    for c0,c1 in product(count_vectors(m),repeat=2):
        mass=multinomial_mass(c0,source_pmfs[0])*multinomial_mass(c1,source_pmfs[1])
        fit=fits[(m,c0,c1)]
        llpo=loss_float(source_pmfs,fit["po_predictive_probabilities"])
        llflex=loss_float(source_pmfs,fit["nonpo_predictive_probabilities"])
        dpo=loss_decimal(source_pmfs,fit["po_predictive_probabilities"])
        dflex=loss_decimal(source_pmfs,fit["nonpo_predictive_probabilities"])
        if abs(llpo-float(dpo))>1e-12 or abs(llflex-float(dflex))>1e-12:
            raise AssertionError("ordinal out-of-sample math and Decimal routes diverged")
        allmass+=mass
        n_tables+=1
        po_risk+=float(mass)*llpo
        flex_risk+=float(mass)*llflex
        decmass=Decimal(mass.numerator)/Decimal(mass.denominator)
        po_high+=decmass*dpo
        flex_high+=decmass*dflex
        strict_training_gain+=mass*int(fit["nonpo_max_training_likelihood"]>fit["po_max_training_likelihood"])
        rows.append({
            "source_world":name,"m_per_group":m,
            "true_group0_categories":",".join(str(v) for v in source_pmfs[0]),
            "true_group1_categories":",".join(str(v) for v in source_pmfs[1]),
            "training_count_group0":",".join(map(str,c0)),
            "training_count_group1":",".join(map(str,c1)),
            "true_training_probability":str(mass),
            "po_selected_base_odds_and_two_threshold_factors":",".join(map(str,fit["po_selected_odds"])),
            "nonpo_selected_base_odds_and_two_threshold_factors":",".join(map(str,fit["nonpo_selected_odds"])),
            "po_max_likelihood":str(fit["po_max_training_likelihood"]),
            "nonpo_max_likelihood":str(fit["nonpo_max_training_likelihood"]),
            "new_independent_test_po_logloss":format(llpo,".16g"),
            "new_independent_test_nonpo_logloss":format(llflex,".16g"),
        })
    if allmass!=1 or n_tables!=(100 if m==3 else 225):
        raise AssertionError("complete original artificial count likelihood invalid")
    if abs(po_risk-float(po_high))>1e-12 or abs(flex_risk-float(flex_high))>1e-12:
        raise AssertionError("independent expected future log score paths diverged")
    cdf_shift_low=source_pmfs[1][0]-source_pmfs[0][0]
    cdf_shift_upper=(source_pmfs[1][0]+source_pmfs[1][1])-(source_pmfs[0][0]+source_pmfs[0][1])
    signs_cross=cdf_shift_low*cdf_shift_upper<0
    if (name in ("DIVERGENT","CROSSED_THRESHOLDS"))!=signs_cross:
        raise AssertionError("frozen true crossing or noncrossing classification inconsistent")
    return {
        "source_world":name,"group_sample_size_m":m,
        "truth_satisfies_proportional_odds":is_po,
        "source_threshold_base_odds":[str(o0),str(o1)],
        "source_threshold_odds_multipliers":[str(t0),str(t1)],
        "truth_categorical_PMF_group0":[str(v) for v in source_pmfs[0]],
        "truth_categorical_PMF_group1":[str(v) for v in source_pmfs[1]],
        "true_cdf_shift_threshold_low":str(cdf_shift_low),
        "true_cdf_shift_threshold_upper":str(cdf_shift_upper),
        "true_threshold_effects_cross":signs_cross,
        "full_training_tables":n_tables,
        "probability_nonPO_training_fit_strictly_better":str(strict_training_gain),
        "future_PO_model_independent_test_logloss":format(po_risk,".16g"),
        "future_NONPO_model_independent_test_logloss":format(flex_risk,".16g"),
        "NONPO_minus_PO_future_test_logloss":format(flex_risk-po_risk,".16g"),
        "all_source_probabilities_and_independent_logloss_scoring_verified":True,
    }


def serialize_fits(fits):
    content=[]
    for (m,c0,c1),v in sorted(fits.items()):
        content.append({
            "m":m,"group0_counts":list(c0),"group1_counts":list(c1),
            "po_selected_parameters":[str(x) for x in v["po_selected_odds"]],
            "nonpo_selected_parameters":[str(x) for x in v["nonpo_selected_odds"]],
            "po_exact_max_training_likelihood":str(v["po_max_training_likelihood"]),
            "nonpo_exact_max_training_likelihood":str(v["nonpo_max_training_likelihood"]),
            "po_fitted_group0_and_group1":[[str(x) for x in p] for p in v["po_predictive_probabilities"]],
            "nonpo_fitted_group0_and_group1":[[str(x) for x in p] for p in v["nonpo_predictive_probabilities"]],
            "both_independent_ordinal_probability_and_likelihood_routes_pass":True
        })
    return content


def run():
    po,flex=candidate_grid()
    fits=fit_library()
    rows=[]
    results=[]
    for params in worlds():
        results.append(world_eval(*params,fits,rows))
    if len(results)!=12 or len(rows)!=1950 or len(fits)!=325:
        raise AssertionError("prescored artificial source universe changed")
    crossing=[w for w in results if w["source_world"]=="CROSSED_THRESHOLDS"]
    if len(crossing)!=2 or any(w["truth_satisfies_proportional_odds"] or not w["true_threshold_effects_cross"] for w in crossing):
        raise AssertionError("locked ordinal cutoff direction inversion was not demonstrated")
    if any(w["true_cdf_shift_threshold_low"]!="2/15" or w["true_cdf_shift_threshold_upper"]!="-2/15" for w in crossing):
        raise AssertionError("exact crossing threshold cumulative probability counterexample failed")
    with SAMPLES.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    entries=serialize_fits(fits)
    LIBRARY.write_text(json.dumps({
        "research_id":"R187","profiles":entries,
        "unique_training_tables":len(entries),
        "po_candidates":len(po),"nonpo_candidates":len(flex),
        "exact_all_candidate_probability_and_likelihood_routes":True,
    },sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    output={
        "research_id":"R187",
        "status":"E1_ARTIFICIAL_ORDINAL_CUMULATIVE_ODDS_GRID",
        "world_count":12,"all_source_training_tables":1950,
        "unique_fitted_count_tables":325,
        "candidate_PO_count":len(po),"candidate_NONPO_count":len(flex),
        "all_positive_ordered_three_level_probability_sources":True,
        "all_exact_nested_PO_and_NONPO_training_likelihoods_verified":True,
        "all_heldout_logloss_numeric_double_checked":True,
        "locked_opposite_threshold_sign_counterexample":crossing,
        "source_world_results":results,
        "original_sample_CSV_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "full_profile_library_sha256":sha256(LIBRARY.read_bytes()).hexdigest(),
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0,
    }
    RESULT.write_text(json.dumps(output,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accepted={
        "research_id":"R187","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_ORDINAL_LOGIT",
        "world_count":12,"source_training_tables":1950,"full_fit_profiles":325,
        "independent_cumulative_and_analytic_probabilities_exact":True,
        "independent_full_individual_and_aggregate_likelihoods_exact":True,
        "nonproportional_model_contains_all_PO_candidates":True,
        "true_cross_cutoff_odds_direction_counterexample":True,
        "independent_heldout_logscore_double_path":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "source_csv_sha256":output["original_sample_CSV_sha256"],
        "full_fit_library_sha256":output["full_profile_library_sha256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False,
    }
    ACCEPT.write_text(json.dumps(accepted,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R187_MACHINE_ACCEPTANCE",json.dumps(accepted,sort_keys=True))
    print("R187_PRELOCKED_EFFECT_CROSSING",json.dumps(crossing,sort_keys=True))
    return output


def archive():
    names=[Path(__file__).name,RESULT.name,SAMPLES.name,LIBRARY.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R187_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestOrdinalOdds(unittest.TestCase):
    def test_source_scenarios_six(self):
        self.assertEqual(len(SOURCE_SCENARIOS),6)
    def test_exact_twelve_worlds(self):
        self.assertEqual(len(list(worlds())),12)
    def test_1950_training_tables(self):
        self.assertEqual(sum(len(count_vectors(m))**2 for s,m,*rest in worlds()),1950)
    def test_fit_library_325(self):
        self.assertEqual(len(fit_library()),325)
    def test_po_candidate_count_40(self):
        self.assertEqual(len(candidate_grid()[0]),40)
    def test_flexible_contains_all_po(self):
        po,flex=candidate_grid()
        self.assertTrue(all(x in flex for x in po))
    def test_nonpo_more_flexible(self):
        po,flex=candidate_grid()
        self.assertGreater(len(flex),len(po))
    def test_probability_full_two_routes_all_candidates(self):
        po,flex=candidate_grid()
        for o0,o1,t0,t1,p0,p1 in flex:
            self.assertEqual(p0,ordinal_pmf_algebra(o0,o1))
            self.assertEqual(p1,ordinal_pmf_algebra(o0*t0,o1*t1))
    def test_all_candidates_strict_positive_three_probabilities(self):
        po,flex=candidate_grid()
        for *args,p0,p1 in flex:
            self.assertTrue(all(v>0 for v in p0+p1))
            self.assertEqual(sum(p0,F(0)),1)
            self.assertEqual(sum(p1,F(0)),1)
    def test_multinomial_source_mass_exact_all(self):
        for name,m,o0,o1,t0,t1,is_po in worlds():
            p0,p1=model_probabilities(o0,o1,t0,t1)
            self.assertEqual(sum((multinomial_mass(c,p0) for c in count_vectors(m)),F(0)),1)
            self.assertEqual(sum((multinomial_mass(c,p1) for c in count_vectors(m)),F(0)),1)
    def test_probability_hand(self):
        self.assertEqual(ordinal_pmf_cdf(F(1,2),F(2)),(F(1,3),F(1,3),F(1,3)))
    def test_crossing_true_probs_exact(self):
        p0,p1=model_probabilities(F(1,4),F(4),F(2),F(1,2))
        self.assertEqual(p0,(F(1,5),F(3,5),F(1,5)))
        self.assertEqual(p1,(F(1,3),F(1,3),F(1,3)))
    def test_crossing_cumulative_both_directions(self):
        p0,p1=model_probabilities(F(1,4),F(4),F(2),F(1,2))
        self.assertTrue(p1[0]>p0[0])
        self.assertTrue(sum(p1[:2])<sum(p0[:2]))
    def test_crossing_not_representable_by_PO(self):
        p0,p1=model_probabilities(F(1,4),F(4),F(2),F(1,2))
        self.assertFalse(any(a==p0 and b==p1 for *args,a,b in candidate_grid()[0]))
    def test_same_true_PO_three_scenarios(self):
        self.assertEqual(sum(int(x[-1]) for x in SOURCE_SCENARIOS),3)
    def test_all_PO_work_shared_factor(self):
        self.assertTrue(all(p[2]==p[3] for p in candidate_grid()[0]))
    def test_fit_likelihood_full_two_routes(self):
        for fit in fit_library().values():
            self.assertGreaterEqual(fit["nonpo_max_training_likelihood"],fit["po_max_training_likelihood"])
    def test_training_likelihood_multinomial_constants_cancel(self):
        c0,c1=(1,1,1),(2,1,0)
        p0,p1=model_probabilities(F(1,2),F(2),F(1),F(1))
        l=likelihood_counts((c0,c1),(p0,p1))
        raw=multinomial_mass(c0,p0)*multinomial_mass(c1,p1)
        self.assertEqual(raw/l,F(6)*F(3))
    def test_training_observation_likelihood_two_algorithms(self):
        x=((1,1,1),(0,1,2))
        p=model_probabilities(F(1,2),F(2),F(2),F(2))
        self.assertEqual(likelihood_counts(x,p),likelihood_individual_rows(x,p))
    def test_predictive_float_decimal_scenario_and_profiles(self):
        for name,m,o0,o1,t0,t1,is_po in worlds():
            true=model_probabilities(o0,o1,t0,t1)
            for fit in fit_library().values():
                if fit["m"]!=m:
                    continue
                for key in ("po_predictive_probabilities","nonpo_predictive_probabilities"):
                    self.assertAlmostEqual(loss_float(true,fit[key]),
                                           float(loss_decimal(true,fit[key])),places=12)
    def test_minimum_one_probability(self):
        for fit in fit_library().values():
            self.assertTrue(all(z>0 for p in fit["po_predictive_probabilities"] for z in p))
    def test_disallowed_cutoff_order(self):
        with self.assertRaises(ValueError):
            ordinal_pmf_cdf(F(4),F(1))
    def test_disallowed_crossed_fitted_odds(self):
        with self.assertRaises(ValueError):
            model_probabilities(F(1),F(2),F(4),F(1,2))
    def test_disallowed_non_grid_factor(self):
        with self.assertRaises(ValueError):
            model_probabilities(F(1,4),F(2),F(3),F(1))
    def test_invalid_group_size(self):
        with self.assertRaises(ValueError):
            count_vectors(2)
    def test_invalid_fit_count_total(self):
        with self.assertRaises(ValueError):
            fit_table((3,0,0),(1,1,0))
    def test_invalid_source_negative_counts(self):
        with self.assertRaises(ValueError):
            multinomial_mass((-1,4,0),(F(1,3),)*3)
    def test_fixed_ordinal_three_classes(self):
        self.assertEqual(len(model_probabilities(F(1,2),F(2),F(1),F(1))[0]),3)
    def test_PO_false_constraint_detected(self):
        self.assertFalse(SOURCE_SCENARIOS[-1][-1])


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
