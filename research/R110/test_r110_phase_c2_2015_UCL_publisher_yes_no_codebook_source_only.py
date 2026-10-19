"""C2 source word coverage pure synthetic, no original files or network."""
import csv,hashlib,io,json,unittest
from unittest.mock import patch
import r110_phase_b0_2015_PLOS_original_12000_CSV_row_width_and_18_public_headers_only as p0
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as p1
import r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier as c0
import r110_phase_c2_2015_UCL_publisher_yes_no_codebook_source_only as c2
from test_r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier import simulate

def transform(base, change=None):
    data=list(csv.reader(io.StringIO(base.decode())))
    for row in data[1:]:
        for idx in (8,15):
            if row[idx] in ("0","1"):
                row[idx]="NO" if row[idx]=="0" else " Yes "
            elif row[idx]=="":
                row[idx]=" no "
        if change and row[1]=="TEST001" and row[9]=="sym" and row[0]=="2":
            row[change[0]]=change[1]
    out=io.StringIO(newline="")
    csv.writer(out,lineterminator="\n").writerows(data)
    return out.getvalue().encode()

def audit(raw):
    sha=hashlib.sha256(raw).hexdigest()
    with patch.object(p0,"PINNED_SHA",sha), \
         patch.object(p0,"EXPECTED_BYTES",len(raw)), \
         patch.object(p1,"PINNED_SHA",sha):
        return c2.summarize(raw)

class PublisherYesNoAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.synthetic=transform(simulate())
        cls.pass_result=audit(cls.synthetic)
    def test_yes_no_strict_ascii_whitespace_and_case(self):
        for t,expected in (("YES","yes"),(" no ","no"),(" Yes ","yes"),
                           ("1","other_nonempty"),("true","other_nonempty"),
                           ("Cooperate","other_nonempty"),("","blank"),
                           (" ","blank")):
            self.assertEqual(c2.class_word(t),expected)
    def test_complete_yes_no_synthetic_coverage(self):
        x=self.pass_result
        self.assertEqual(x["status"],c2.PASS)
        self.assertEqual(x["original_records"],12000)
        self.assertEqual(x["behavior_anonymous_dictionary_counts"]["own_cooperation"]["other_nonempty"],0)
        self.assertEqual(x["behavior_anonymous_dictionary_counts"]["author_prior_partner_cooperation"]["other_nonempty"],0)
        self.assertTrue(x["every_cooperation_cell_matches_pre_frozen_yes_no"])
    def test_unknown_author_token_fail_closed(self):
        x=audit(transform(simulate(),(15,"Cooperate")))
        self.assertEqual(x["status"],c2.UNKNOWN)
        self.assertEqual(x["behavior_anonymous_dictionary_counts"]["own_cooperation"]["other_nonempty"],1)
        self.assertFalse(x["every_cooperation_cell_matches_pre_frozen_yes_no"])
    def test_unknown_prior_peer_token_fail_closed(self):
        x=audit(transform(simulate(),(8,"TRUE")))
        self.assertEqual(x["status"],c2.UNKNOWN)
        self.assertEqual(x["behavior_anonymous_dictionary_counts"]["author_prior_partner_cooperation"]["other_nonempty"],1)
    def test_no_raw_person_actions_or_model_scores(self):
        x=self.pass_result
        self.assertEqual(x["real_human_model_score_count"],0)
        self.assertTrue(x["previous_C0_gate_still_failed"])
        self.assertFalse(x["raw_tokens_person_IDs_and_actions_exported"])
        rendered=json.dumps(x)
        self.assertNotIn("TEST001",rendered)
        self.assertNotIn("PRIVATE_PUNISHMENT",rendered)
        self.assertNotIn("brier",rendered.lower())
    def test_wrong_unpinned_source_denied(self):
        with self.assertRaises(Exception):
            c2.summarize(self.synthetic)
    def test_two_anonymous_game_denominators(self):
        x=self.pass_result
        self.assertEqual(len(x["original_two_game_anonymous_counts"]),2)
        self.assertEqual([g["source_rows"] for g in x["original_two_game_anonymous_counts"]],[6000,6000])
    def test_no_C0_score_call_allowed(self):
        with patch.object(c0,"evaluate_original_source",side_effect=AssertionError("NO_SCORE")):
            self.assertEqual(audit(self.synthetic)["real_human_model_score_count"],0)

if __name__=="__main__":
    unittest.main()
