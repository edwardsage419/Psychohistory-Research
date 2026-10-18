"""R105 B full 4120 synthetic only person/group/round, never genuine extraction."""
import csv
import hashlib
import io
import unittest
from unittest.mock import patch
import r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only as a
import r105_phase_b_2024_original_cpr_actor_group_round_nonbehavior_roster as b

def fields():
    return ["","player_id","Treatment","group_id","round"]+[f"safe_{i}" for i in range(32)]

def fake_source(change=None):
    o=io.StringIO(newline="")
    writer=csv.DictWriter(o,fieldnames=fields(),lineterminator="\n")
    writer.writeheader()
    n=0
    for tr,total in (("Control",100),("Prosocial",156),("Selfish",156)):
        for roundnum in range(1,11):
            for person in range(1,total+1):
                n+=1
                row={"player_id":str(person),"Treatment":tr,
                     "group_id":str((person-1)//4+1),"round":str(roundnum),
                     "safe_0":"PRIVATE_BEHAVIOR_MUST_NEVER_READ"}
                if change is not None:
                    change(row,tr,roundnum,person,n)
                writer.writerow(row)
    return o.getvalue().encode("utf-8")

def audited(raw):
    with patch.object(a,"PUBLISHED_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"ORIGINAL_SHA",hashlib.sha256(raw).hexdigest()):
        return b.original_nonbehavior_roster(raw)

class SyntheticOnlySourceRoster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.source=fake_source()
    def test_complete_group_universe(self):
        x=audited(self.source)
        self.assertEqual(x["original_actor_round_rows"],4120)
        self.assertEqual(x["original_people_by_treatment_ID"],412)
        self.assertEqual(x["original_fixed_group_identity_count"],103)
        self.assertEqual(x["original_ten_round_group_combinations"],1030)
        self.assertEqual(x["source_original_group_size_histogram"],{4:103})
        self.assertEqual(x["source_original_person_round_count_histogram"],{10:412})
        self.assertEqual(x["original_treatment_count"],3)
        self.assertFalse(x["any_original_extraction_payoff_or_demographic_cell_dereferenced"])
        self.assertEqual(x["actual_human_model_scores"],0)
    def test_no_real_identity_or_behavior_exported(self):
        x=audited(self.source)
        self.assertNotIn("PRIVATE_BEHAVIOR",repr(x))
        self.assertFalse(x["raw_human_player_group_or_treatment_codes_exported"])
        self.assertNotIn("Prosocial",repr(x))
    def test_group_labels_reused_across_conditions_are_independent_keys(self):
        x=audited(self.source)
        self.assertEqual(x["original_fixed_group_identity_count"],103)
    def test_duplicate_actor_round_fails(self):
        def c(row,tr,t,p,n):
            if tr=="Control" and t==1 and p==2:row["player_id"]="1"
        self.assertRaises(b.SourceGateError,audited,fake_source(c))
    def test_moved_group_fails(self):
        def c(row,tr,t,p,n):
            if tr=="Control" and t==2 and p==1:row["group_id"]="2"
        self.assertRaises(b.SourceGateError,audited,fake_source(c))
    def test_round_outside_frozen_ten_fails(self):
        def c(row,tr,t,p,n):
            if tr=="Control" and t==1 and p==1:row["round"]="11"
        self.assertRaises(b.SourceGateError,audited,fake_source(c))
    def test_noninteger_round_fails(self):
        def c(row,tr,t,p,n):
            if tr=="Control" and t==1 and p==1:row["round"]="1.0"
        self.assertRaises(b.SourceGateError,audited,fake_source(c))
    def test_malicious_group_identity_fails(self):
        def c(row,tr,t,p,n):
            if tr=="Control" and t==1 and p==1:row["group_id"]="../private"
        self.assertRaises(b.SourceGateError,audited,fake_source(c))
    def test_source_original_MD5_without_synthetic_patching_fails(self):
        self.assertRaises(a.SourceGateError,b.original_nonbehavior_roster,self.source)
    def test_treatment_imbalance_real_rows_are_consistent(self):
        x=audited(self.source)
        self.assertEqual(sorted(d["original_individuals"] for d in x["anonymized_original_treatment_counts"]),[100,156,156])
        self.assertEqual(sorted(d["original_fixed_four_person_groups"] for d in x["anonymized_original_treatment_counts"]),[25,39,39])
    def test_no_source_experiment_sessions_claimed(self):
        x=audited(self.source)
        self.assertFalse(x["independent_original_lab_session_column_present"])
        self.assertIn("whole original fixed group",x["eligible_holdout_unit"])

if __name__=="__main__":unittest.main()
