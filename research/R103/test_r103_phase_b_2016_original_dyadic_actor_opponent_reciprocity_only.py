"""R103 B pure synthetic actor/opponent source identity reciprocal testing."""
import csv
import hashlib
import io
import unittest
from unittest.mock import patch
import r103_phase_a_2016_drbrain_original_md5_header_only as a
import r103_phase_b_2016_original_dyadic_actor_opponent_reciprocity_only as b

def synthetic_data(mutate=None,experiments=30):
    o=io.StringIO(newline="")
    writer=csv.DictWriter(o,fieldnames=a.MANDATORY_FIELDS,lineterminator="\n")
    writer.writeheader()
    line=0
    for exp in range(1,experiments+1):
        for t in range(1,6):
            for actor,opponent in ((2*exp-1,2*exp),(2*exp,2*exp-1)):
                line+=1
                row={
                    "Experiment_number":str(exp),"User_ID":str(actor),
                    "Round_number":str(t),"Opponent_ID":str(opponent),
                    "S":"0.5","T":"1.5","Game":"PD",
                    "Action":"C","Opponent_Action":"D",
                }
                if mutate:mutate(row,line,exp,t,actor)
                writer.writerow(row)
    return o.getvalue().encode()

def audit(raw):
    with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()), \
         patch.object(b,"PINNED_SOURCE_SHA",hashlib.sha256(raw).hexdigest()), \
         patch.object(b,"PINNED_LINES",raw.count(b"\n")-1):
        return b.identity_only(raw)

class TrueDyadicRosterSynthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=synthetic_data()
    def test_true_reciprocal_30_experiments(self):
        r=audit(self.data)
        self.assertEqual(r["status"],"R103_B_ORIGINAL_DYADIC_SOURCE_RECIPROCITY_ELIGIBLE")
        self.assertEqual(r["actor_rounds_with_exact_reciprocal_opponent"],300)
        self.assertEqual(r["unique_source_reciprocal_pair_rounds"],150)
        self.assertEqual(r["original_experiment_number_count"],30)
        self.assertEqual(r["actual_human_model_scores"],0)
    def test_no_private_ids_or_choices_released(self):
        r=audit(self.data)
        self.assertFalse(r["actual_original_actions_or_opponent_actions_dereferenced"])
        self.assertFalse(r["original_raw_person_opponent_experiment_IDs_exported"])
        self.assertNotIn("PRIVATE_CHOICE",str(r))
    def test_missing_opponent_diagnostic(self):
        # One bad partner reference gives one missing and its reciprocal peer
        # is still missing a backlink, so two source actor-rounds ineligible.
        def edit(row,line,ex,t,actor):
            if line==1: row["Opponent_ID"]="99999"
        r=audit(synthetic_data(edit))
        self.assertEqual(r["source_actor_rounds_with_missing_opponent"],1)
        self.assertEqual(r["source_actor_rounds_with_nonreciprocal_opponent"],1)
        self.assertEqual(r["actor_rounds_with_exact_reciprocal_opponent"],298)
    def test_false_mutual_partner_diagnostic(self):
        def edit(row,line,ex,t,actor):
            if line==1:row["Opponent_ID"]="100"
        r=audit(synthetic_data(edit))
        self.assertEqual(r["actor_rounds_with_exact_reciprocal_opponent"],298)
    def test_duplicate_actor_round_fail_closed(self):
        def edit(row,line,ex,t,actor):
            if line==2:row["User_ID"]="1"
        self.assertRaises(b.SourceError,audit,synthetic_data(edit))
    def test_self_partner_fail_closed(self):
        def edit(row,line,ex,t,actor):
            if line==1:row["Opponent_ID"]=row["User_ID"]
        self.assertRaises(b.SourceError,audit,synthetic_data(edit))
    def test_invalid_original_game_payoff(self):
        def edit(row,line,ex,t,actor):
            if line==1:row["S"]="inf"
        self.assertRaises(b.SourceError,audit,synthetic_data(edit))
    def test_source_person_ID_noninteger(self):
        def edit(row,line,ex,t,actor):
            if line==1:row["User_ID"]="one"
        self.assertRaises(b.SourceError,audit,synthetic_data(edit))
    def test_too_few_experiments_bounded(self):
        r=audit(synthetic_data(experiments=2))
        self.assertEqual(r["status"],"R103_B_BOUNDED_ORIGINAL_DYADIC_RECIPROCITY_INELIGIBLE")
    def test_fake_original_MD5_rejected(self):
        self.assertRaises(a.SourceError,b.identity_only,self.data)
    def test_private_actions_never_affect_source_roster(self):
        def edit(row,line,ex,t,actor):
            row["Action"]="SENSITIVE_HUMAN_CHOICE"
            row["Opponent_Action"]="SENSITIVE_OTHER_CHOICE"
        r=audit(synthetic_data(edit))
        self.assertTrue(r["eligible_for_prescoring_after_B"])
        self.assertNotIn("SENSITIVE_HUMAN_CHOICE",str(r))
        self.assertNotIn("SENSITIVE_OTHER_CHOICE",str(r))

if __name__=="__main__":
    unittest.main()
