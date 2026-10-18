"""R105 C source E2 pure synthetic 4120-row full held-out group paired controls."""
import csv
import hashlib
import io
import unittest
from unittest.mock import patch
import r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only as a
import r105_phase_b_2024_original_cpr_actor_group_round_nonbehavior_roster as b
import r105_phase_c_2024_original_103groups_3708_realpeer_equalshrink_rotated_LOOG as c

def fixture(peer_mode=False,modify=None):
    columns=["","player_id","Treatment","group_id","round","extraction"]+[f"safe_{i}" for i in range(31)]
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=columns,lineterminator="\n")
    w.writeheader()
    index=0
    for tr,total in (("Control",100),("Prosocial",156),("Selfish",156)):
        previous={}
        for t in range(1,11):
            current={}
            for p in range(1,total+1):
                gid=(p-1)//4+1
                if not peer_mode:
                    amount=1+((7*p+gid)%30)
                elif t==1:
                    amount=1+((gid*7+(p-1)%4*5)%30)
                else:
                    four=[q for q in range(4*(gid-1)+1,4*gid+1)]
                    peers=[q for q in four if q!=p]
                    amount=max(1,min(30,round(.5*previous[p]+.5*sum(previous[q] for q in peers)/3)))
                current[p]=amount
                row={"player_id":str(p),"Treatment":tr,"group_id":str(gid),
                     "round":str(t),"extraction":str(amount),
                     "safe_0":"PRIVATE_AGE_99"}
                index+=1
                if modify is not None:modify(row,tr,t,p,index)
                w.writerow(row)
            previous=current
    return out.getvalue().encode()

def verified(fake_bytes):
    sha=hashlib.sha256(fake_bytes).hexdigest()
    with patch.object(a,"PUBLISHED_MD5",hashlib.md5(fake_bytes).hexdigest()), \
         patch.object(b,"ORIGINAL_SHA",sha), \
         patch.object(c,"ORIGINAL_SHA",sha):
        return c.source_score(fake_bytes)

class TruePeerVsShrinkageSynthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.self_source=fixture()
    def test_five_models_same_3708_complete_holdout(self):
        r=verified(self.self_source)
        self.assertEqual(r["original_next_actor_round_targets_same_for_all_five_models"],3708)
        self.assertEqual(set(r["all_recorded_t2_to_t10"]["MSE"]),set(c.MODELS))
        self.assertEqual(r["original_source_complete_groups"],103)
        self.assertEqual(r["source_full_SHA256"],hashlib.sha256(self.self_source).hexdigest())
        self.assertFalse(r["raw_original_person_group_treatment_or_action_rows_exported"])
        self.assertEqual(r["equal_shrinkage_weight_in_M2_and_M3"],.5)
    def test_all_stage_windows_consistent(self):
        r=verified(self.self_source)
        self.assertEqual(r["early_target_t2_to_t5"]["target_count"],1648)
        self.assertEqual(r["transition_target_t6"]["target_count"],412)
        self.assertEqual(r["late_target_t7_to_t10"]["target_count"],1648)
        self.assertEqual(sum(t["original_group_count"] for t in r["anonymous_source_treatment_summaries"]),103)
    def test_stable_personal_fixture_can_favor_own_history(self):
        r=verified(self.self_source)
        self.assertAlmostEqual(r["all_recorded_t2_to_t10"]["MSE"]["M1"],0,places=18)
        self.assertLess(r["all_recorded_t2_to_t10"]["gains"]["M3_vs_M1_own_only"],0)
        self.assertEqual(r["original_source_group_gain_directions"]["M3_vs_M1_own_only"]["negative_groups"],103)
    def test_peer_generated_fixture_favors_true_peer_over_shrink(self):
        r=verified(fixture(peer_mode=True))
        self.assertGreater(r["all_recorded_t2_to_t10"]["gains"]["M3_vs_M2_matched_shrinkage"],0)
        self.assertGreater(r["all_recorded_t2_to_t10"]["gains"]["M3_vs_M4_rotated_group"],0)
    def test_no_demographic_or_person_values_exported(self):
        r=verified(self.self_source)
        text=str(r)
        self.assertNotIn("PRIVATE_AGE",text)
        self.assertNotIn("Prosocial",text)
        self.assertNotIn("Selfish",text)
        self.assertFalse(r["raw_original_person_group_treatment_or_action_rows_exported"])
    def test_zero_action_rejected(self):
        def edit(row,tr,t,p,k):
            if k==1:row["extraction"]="0"
        self.assertRaises(c.SourceGateError,verified,fixture(modify=edit))
    def test_source_above_thirty_rejected(self):
        def edit(row,tr,t,p,k):
            if k==1:row["extraction"]="31"
        self.assertRaises(c.SourceGateError,verified,fixture(modify=edit))
    def test_noninteger_extraction_rejected(self):
        def edit(row,tr,t,p,k):
            if k==1:row["extraction"]="1.5"
        self.assertRaises(c.SourceGateError,verified,fixture(modify=edit))
    def test_missing_action_rejected(self):
        def edit(row,tr,t,p,k):
            if k==1:row["extraction"]=""
        self.assertRaises(c.SourceGateError,verified,fixture(modify=edit))
    def test_original_group_switch_rejected_before_scoring(self):
        def edit(row,tr,t,p,k):
            if tr=="Control" and t==2 and p==1:row["group_id"]="2"
        self.assertRaises(c.SourceGateError,verified,fixture(modify=edit))
    def test_unpinned_original_publisher_MD5_rejected(self):
        self.assertRaises(a.SourceGateError,c.source_score,self.self_source)

if __name__=="__main__":
    unittest.main()
