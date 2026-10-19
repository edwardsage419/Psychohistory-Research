"""R110 C1 pure synthetic tests; NEVER downloads real source."""
import csv
import hashlib
import io
import json
import unittest
from unittest.mock import patch

import r110_phase_b0_2015_PLOS_original_12000_CSV_row_width_and_18_public_headers_only as p0
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as p1
import r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier as c0
import r110_phase_c1_2015_UCL_frozen_binary_eligibility_diagnostic as c1
from test_r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier import simulate

def audit(raw):
    sha=hashlib.sha256(raw).hexdigest()
    with patch.object(p0,"PINNED_SHA",sha), \
         patch.object(p0,"EXPECTED_BYTES",len(raw)), \
         patch.object(p1,"PINNED_SHA",sha):
        return c1.diagnose(raw)

def mutate(raw, column, sid="TEST001", game="sym", round_number="2", token="NA"):
    data=list(csv.reader(io.StringIO(raw.decode())))
    rows=0
    for row in data[1:]:
        if row[1]==sid and row[9]==game and row[0]==round_number:
            row[column]=token
            rows+=1
    assert rows==1
    output=io.StringIO(newline="")
    csv.writer(output,lineterminator="\n").writerows(data)
    return output.getvalue().encode()

class R110FrozenC1Diagnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=simulate()
        cls.baseline=audit(cls.raw)

    def test_complete_120x2x50_synthetic_universe(self):
        x=self.baseline
        self.assertEqual(x["original_source_rows"],12000)
        self.assertEqual(x["total_valid_C0_identical_targets"],11760)
        self.assertEqual(x["source_actors_with_valid_targets"],120)
        self.assertEqual(x["game_categories_with_valid_targets"],2)
        self.assertEqual(x["mutually_exclusive_reasons"]["first_round_each_actor_game"],240)

    def test_exact_C0_sample_target_and_no_frozen_C0_claim(self):
        x=self.baseline
        self.assertEqual(x["status"],c1.DISCREPANCY)
        self.assertTrue(x["frozen_C0_evidence_gate_pass_in_C1_diagnostic"])
        self.assertEqual(x["new_human_prediction_scores"],0)
        self.assertEqual(x["C0_original_failure_unchanged"],
                         "R110_C0_PRE_FROZEN_REAL_800_TARGET_40_ACTOR_2_GAME_GATE_FAIL")

    def test_whole_universe_and_two_game_denominators(self):
        x=self.baseline
        self.assertEqual(sum(x["mutually_exclusive_reasons"].values())+
                         x["total_valid_C0_identical_targets"],12000)
        self.assertEqual(sum(g["source_rows"] for g in x["game_level_anonymous_denominators"]),12000)
        self.assertEqual(sum(g["eligible_targets"] for g in x["game_level_anonymous_denominators"]),11760)
        self.assertTrue(x["denominator_closed"])

    def test_whitelist_behavior_token_classes(self):
        x=self.baseline
        for counts in x["behavior_field_anonymous_token_class_counts"].values():
            self.assertEqual(sum(counts.values()),12000)
            self.assertEqual(set(counts),set(c1.TOKEN_CLASSES))

    def test_token_classification_cannot_coerce_optout(self):
        for s,c in [("0","accepted_zero"),("1.0","accepted_one"),
                    (" 0.0 ","accepted_zero"),("","blank"),
                    ("  ","blank"),("NA","other_nonempty"),
                    ("2","other_numeric"),("true","other_nonempty")]:
            self.assertEqual(c1.token_class(s),c)
        self.assertIsNone(c0.binary("NA"))

    def test_invalid_current_own_and_following_previous_is_accounted(self):
        x=audit(mutate(self.raw,15,token="NA"))
        self.assertEqual(x["mutually_exclusive_reasons"]["invalid_or_missing_current_binary_action"],1)
        self.assertEqual(x["mutually_exclusive_reasons"]["invalid_or_missing_previous_own_binary_action"],1)
        self.assertEqual(x["total_valid_C0_identical_targets"],11758)

    def test_partner_lag_invalid_wins_over_optout(self):
        x=audit(mutate(self.raw,8,token="NA"))
        self.assertEqual(x["mutually_exclusive_reasons"]["invalid_or_missing_author_previous_peer_signal"],1)
        self.assertEqual(x["total_valid_C0_identical_targets"],11759)

    def test_previous_partner_optout_is_not_recoded_defection(self):
        x=audit(mutate(self.raw,16,token="1"))
        self.assertEqual(x["mutually_exclusive_reasons"]["prior_partner_optout_or_unknown"],1)
        self.assertEqual(x["total_valid_C0_identical_targets"],11759)

    def test_refuses_incorrect_source_sha(self):
        with self.assertRaises(Exception):
            c1.diagnose(self.raw)

    def test_anonymity_and_no_private_cells_in_output(self):
        rendered=json.dumps(self.baseline,sort_keys=True)
        for forbidden in ("TEST001","PRIVATE_PUNISHMENT_NOT_ACCESSED","sym","asym"):
            self.assertNotIn(forbidden,rendered)
        self.assertFalse(self.baseline["raw_tokens_actor_identifiers_and_person_actions_exported"])
        self.assertNotIn("brier",rendered.lower())
        self.assertNotIn("prediction_probability",rendered)

    def test_no_real_source_called_during_synthetic_tests(self):
        with patch.object(c1.a,"actual_official_source",side_effect=AssertionError("network forbidden")):
            self.assertEqual(audit(self.raw)["original_source_rows"],12000)

    def test_c1_never_calls_C0_scoring(self):
        with patch.object(c0,"evaluate_original_source",side_effect=AssertionError("scoring forbidden")):
            self.assertEqual(audit(self.raw)["new_human_prediction_scores"],0)

    def test_frozen_threshold_qualification_fail_is_preserved(self):
        with patch.object(c0,"MIN_TARGETS",20000):
            x=audit(self.raw)
        self.assertEqual(x["status"],c1.SUCCESS)
        self.assertFalse(x["frozen_C0_evidence_gate_pass_in_C1_diagnostic"])
        self.assertEqual(x["total_valid_C0_identical_targets"],11760)

if __name__=="__main__":
    unittest.main()
