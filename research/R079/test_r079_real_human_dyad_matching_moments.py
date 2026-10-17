"""R079 30 wholly synthetic two-person matching/finite population tests."""
from __future__ import annotations
import unittest
from fractions import Fraction as F
from r079_real_human_dyad_matching_moments import (
    parse_author_csv,git_blob,validate_real_pair_graph,moments_exact,score_aggregate,
    TREATMENTS,MEASURES,SOURCE_GIT_BLOB,SOURCE_BYTES
)
def make_rows():
    rows=[]
    for tr,sid in (("NoCondInfo",1),("CondInfo",2)):
        for t in range(1,11):
            p0=0 if t%2==0 else 50
            p1=100
            p2=50 if t%2==0 else 100
            p3=0
            for group,a,b,x,y in ((1,1,2,p0,p1),(2,3,4,p2,p3)):
                rows.extend([
                    dict(tr=tr,sess=sid,period=t,subj=a,group=group,opp=b,action=x,opp_action=y,first_player=True),
                    dict(tr=tr,sess=sid,period=t,subj=b,group=group,opp=a,action=y,opp_action=x,first_player=False)
                ])
    return rows
def csv_fixture(rows):
    fields=["treatment","session","period","subject","group","opp","action","opp_action","first_player"]
    lines=[",".join(fields)]
    for r in rows:
        lines.append(",".join(str(r[f]).upper() if f=="first_player" else str(r[f] if f not in ("treatment",) else r[f]) for f in fields))
    return ("\n".join(lines)+"\n").encode()
def csv_author_fixture(rows):
    lines=["treatment,session,period,subject,group,opp,action,opp_action,first_player"]
    for r in rows:
        vals=[r["tr"],r["sess"],r["period"],r["subj"],r["group"],r["opp"],r["action"],r["opp_action"],int(r["first_player"])]
        lines.append(",".join(map(str,vals)))
    return ("\n".join(lines)+"\n").encode()
class SyntheticDyadGuards(unittest.TestCase):
    def setUp(self):
        self.rows=make_rows()
    def test_01_git_source_sha_fixed(self):self.assertEqual(len(SOURCE_GIT_BLOB),40)
    def test_02_real_source_byte_size_fixed(self):self.assertEqual(SOURCE_BYTES,425701)
    def test_03_two_treatments(self):self.assertEqual(len(TREATMENTS),2)
    def test_04_exact_seven_measures(self):self.assertEqual(len(MEASURES),7)
    def test_05_synthetic_raw_rows(self):self.assertEqual(len(self.rows),80)
    def test_06_true_synth_two_person_pair_validation(self):
        pairs,meta=validate_real_pair_graph(self.rows)
        self.assertEqual(meta["actual_realized_two_person_dyads"],40)
        self.assertEqual(meta["original_source_sessions"],2)
    def test_07_realized_other_action_reciprocity(self):
        _,s=validate_real_pair_graph(self.rows)
        self.assertTrue(s["all_dyad_partner_and_action_reciprocals_verified"])
    def test_08_synth_action_rows_sum(self):
        self.assertEqual(len(parse_author_csv(csv_author_fixture(self.rows),verify_source=False)),80)
    def test_09_fixed_source_file_source_hash_blocks_fakes(self):
        with self.assertRaisesRegex(ValueError,"GIT_BLOB"):
            parse_author_csv(csv_author_fixture(self.rows))
    def test_10_duplicate_person_same_round_rejected(self):
        rows=make_rows();rows[1]["subj"]=1
        with self.assertRaisesRegex(ValueError,"DUPLICATE_SUBJECT"):
            validate_real_pair_graph(rows)
    def test_11_opp_wrong_identity_rejected(self):
        rows=make_rows();rows[0]["opp"]=4
        with self.assertRaisesRegex(ValueError,"NOT_RECIPROCAL"):
            validate_real_pair_graph(rows)
    def test_12_opp_action_wrong_rejected(self):
        rows=make_rows();rows[0]["opp_action"]=0
        with self.assertRaisesRegex(ValueError,"NOT_RECIPROCAL"):
            validate_real_pair_graph(rows)
    def test_13_not_two_person_group_rejected(self):
        rows=make_rows();rows[0]["group"]=2
        with self.assertRaisesRegex(ValueError,"DYAD_NOT_TWO"):
            validate_real_pair_graph(rows)
    def test_14_odd_people_rejected(self):
        rows=make_rows();rows.pop()
        with self.assertRaisesRegex(ValueError,"ODD_OR_SMALL"):
            validate_real_pair_graph(rows)
    def test_15_unknown_treatment_rejected(self):
        rows=make_rows();rows[0]["tr"]="Risky"
        with self.assertRaisesRegex(ValueError,"TREATMENT_NOT_UNIQUE|REQUIRED_TWO"):
            validate_real_pair_graph(rows)
    def test_16_missing_period_rejected(self):
        rows=[r for r in make_rows() if not(r["sess"]==1 and r["period"]==8)]
        with self.assertRaisesRegex(ValueError,"NOT_ALL_ORIGINAL_SESSIONS_COMPLETE"):
            validate_real_pair_graph(rows)
    def test_17_finite_group_2_zero_population_variance(self):
        v=moments_exact([(F(1,2),F(1,2))])
        self.assertEqual(v["pop_var"],F(0))
        self.assertEqual(v["excess_cross"],F(0))
    def test_18_pair_product_exact_group_n4(self):
        v=moments_exact([(F(0),F(1)),(F(0),F(1))])
        self.assertEqual(v["mu"],F(1,2))
        self.assertEqual(v["pop_var"],F(1,4))
        self.assertEqual(v["pair_cross"],-F(1,4))
    def test_19_perfect_positive_pairing_cross(self):
        v=moments_exact([(F(0),F(0)),(F(1),F(1))])
        self.assertEqual(v["pair_cross"],F(1,4))
        self.assertEqual(v["excess_cross"],F(1,3))
    def test_20_random_reference_negative_finite_population(self):
        v=moments_exact([(F(0),F(0)),(F(1),F(1))])
        self.assertEqual(v["random_match_cross"],-F(1,12))
    def test_21_two_person_pair_mean_var_identity(self):
        v=moments_exact([(F(0),F(0)),(F(1),F(1))])
        self.assertEqual(v["pair_mean_var"],(v["pop_var"]+v["pair_cross"])/2)
    def test_22_excess_twice_group_variance_difference(self):
        v=moments_exact([(F(0),F(0)),(F(1),F(1))])
        self.assertEqual(v["excess_cross"],2*(v["pair_mean_var"]-v["random_match_pair_mean_var"]))
    def test_23_normalized_three_level_middle(self):
        v=moments_exact([(F(0),F(1,2)),(F(1),F(1))])
        self.assertTrue(F(0)<=v["mu"]<=1)
    def test_24_very_many_simulated_pairs_exact_identity(self):
        v=moments_exact([(F(i%3,2),F((i+1)%3,2)) for i in range(120)])
        self.assertEqual(v["pair_mean_var"],(v["pop_var"]+v["pair_cross"])/2)
    def test_25_bad_group_empty(self):
        with self.assertRaisesRegex(ValueError,"AT_LEAST_TWO"):
            moments_exact([])
    def test_26_no_person_path_in_statistic_export(self):
        a=score_aggregate(make_rows())
        self.assertNotIn("subject",str(a))
        self.assertNotIn("per_session",str(a))
        self.assertNotIn("participant_ids",str(a))
    def test_27_session_weight_over_rows(self):
        a=score_aggregate(make_rows())
        self.assertEqual(a["all_original_sessions_equal_weight"]["original_sessions"],2)
    def test_28_treatment_distribution_equal_10_rounds(self):
        a=score_aggregate(make_rows())
        self.assertEqual(a["treatments_session_equal_weight"]["CondInfo"]["original_sessions"],1)
    def test_29_early_late_dynamic_bounded(self):
        a=score_aggregate(make_rows())
        for tr,v in a["treatments_session_equal_weight"].items():
            self.assertAlmostEqual(v["late_mu"]-v["early_mu"],v["late_minus_early"])
    def test_30_real_causal_effect_not_claimed(self):
        a=score_aggregate(make_rows())
        self.assertEqual(a["causal_peer_influence"],"NOT_IDENTIFIED")
        self.assertIn("NOT_APPLICABLE",a["comparison_to_R078_n10_model"])
    def test_31_csv_bad_binary_role_block(self):
        r=make_rows();r[0]["first_player"]="invalid"
        c=csv_author_fixture(r)
        with self.assertRaisesRegex(ValueError,"ACTION_OR_ID_INVALID"):
            parse_author_csv(c,verify_source=False)
    def test_32_csv_bad_contribution_block(self):
        r=make_rows();r[0]["action"]=55
        with self.assertRaisesRegex(ValueError,"ACTION_OR_ID_INVALID"):
            parse_author_csv(csv_author_fixture(r),verify_source=False)
    def test_33_csv_missing_required_column_block(self):
        with self.assertRaisesRegex(ValueError,"REQUIRED_AUTHOR_COLUMN"):
            parse_author_csv(b"subject,group\n1,1\n",verify_source=False)
    def test_34_dedicated_author_six_sessions_pending_no_synth_pretence(self):
        self.assertEqual(score_aggregate(make_rows())["source_universe"]["original_source_sessions"],2)
if __name__=="__main__":unittest.main()
