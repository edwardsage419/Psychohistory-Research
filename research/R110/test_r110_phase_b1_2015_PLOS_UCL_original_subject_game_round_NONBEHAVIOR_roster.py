"""R110 B1 synthetic ONLY original 120×2×50 actor game-round roster, no behavior."""
import hashlib,unittest
from unittest.mock import patch
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
import r110_phase_b0_2015_PLOS_original_12000_CSV_row_width_and_18_public_headers_only as b
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as c

HEAD=("Round","Subject ID","Player type","Partner type","Gender","Age",
      "Country","Subject studied","Partner coop prev","Game type",
      "Player C after D","Player P in response to C","Partner P after D prev",
      "Player opt out after D","Player P in response to D","Player cooperated",
      "Partner opt out prev","Player C after D 2")

def source():
    lines=[",".join(HEAD)]
    for person in range(1,121):
        for gi,game in enumerate(("sym","asym")):
            for t in range(1,51):
                vals=["X"]*18
                vals[0]=str(t)
                vals[1]="synthetic%03d"%person
                vals[2]="S" if person%2 else "W"
                vals[3]=vals[2] if gi==0 else ("W" if person%2 else "S")
                vals[9]=game
                if person==1 and t==1 and gi==0:vals[15]="PRIVATE_HUMAN_ACTION"
                lines.append(",".join(vals))
    return ("\n".join(lines)+"\n").encode("utf-8")

def checked(blob):
    with patch.object(b,"PINNED_SHA",hashlib.sha256(blob).hexdigest()),\
         patch.object(b,"EXPECTED_BYTES",len(blob)),\
         patch.object(c,"PINNED_SHA",hashlib.sha256(blob).hexdigest()):
        return c.audited_source_actor_game_round_roster(blob)

class HumanRosterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=source()
        cls.genuine=checked(cls.raw)
    def test_exact_original_120x2x50_synthetic_universe(self):
        x=self.genuine
        self.assertEqual(x["original_human_candidate_rows_from_true_original"],12000)
        self.assertEqual(x["source_distinct_pseudonymous_Subject_ID_codes"],120)
        self.assertTrue(x["exact_paper_reported_120_people_two_games_50_each_source_structure"])
    def test_240_original_source_actor_game_units(self):
        self.assertEqual(self.genuine["source_distinct_Subject_ID_by_Game_type_groups"],240)
        self.assertEqual(self.genuine["source_actor_game_groups_exactly_50_ordinal_rounds_1_to_50"],240)
    def test_all_lags_ordinal_no_original_duplicates(self):
        self.assertEqual(self.genuine["source_duplicate_subject_game_round_keys"],0)
        self.assertEqual(self.genuine["source_round_distinct_count"],50)
        self.assertEqual(self.genuine["source_round_max"],50)
    def test_source_actor_game_row_distribution(self):
        self.assertEqual(self.genuine["source_anonymous_rows_per_subject_game_histogram"],{"50":240})
        self.assertEqual(self.genuine["source_anonymous_rows_per_subject_histogram"],{"100":120})
    def test_stable_type_conditions(self):
        self.assertEqual(self.genuine["source_actor_game_groups_player_and_partner_type_stable"],240)
        self.assertEqual(self.genuine["source_anonymous_distinct_player_type_code_count"],2)
    def test_two_original_games_per_subject(self):
        self.assertEqual(self.genuine["source_anonymous_game_type_count_per_subject_histogram"],{"2":120})
    def test_absent_true_lab_session_ID_no_LOSO(self):
        self.assertFalse(self.genuine["original_true_lab_session_key_present_in_published_CSV"])
    def test_absent_actual_partner_person_ID_no_true_dyad_claim(self):
        self.assertFalse(self.genuine["original_actual_counterpart_Subject_ID_key_present_in_published_CSV"])
    def test_no_behavior_source_application_dereference(self):
        self.assertFalse(self.genuine["original_cooperation_punishment_optout_demographic_or_partner_coop_prev_cells_read"])
        self.assertTrue(self.genuine["original_subject_ID_or_nonbehavior_condition_values_transiently_read"])
    def test_no_private_original_values_or_model_scores_exported(self):
        self.assertNotIn("PRIVATE_HUMAN_ACTION",repr(self.genuine))
        self.assertNotIn("synthetic001",repr(self.genuine))
        self.assertEqual(self.genuine["real_human_next_action_model_scores"],0)
    def test_pinned_real_SHA_rejects_fake_unpatched(self):
        self.assertRaises(a.SourceError,c.audited_source_actor_game_round_roster,self.raw)
    def test_source_actor_nonliteral_ID_rejected(self):
        bad=self.raw.replace(b"synthetic001",b"someone@email.example",1)
        self.assertRaisesRegex(a.SourceError,"SUBJECT_ID_INVALID",checked,bad)
    def test_one_invalid_ordinal_rejected(self):
        bad=self.raw.replace(b"1,synthetic001",b"0,synthetic001",1)
        self.assertRaisesRegex(a.SourceError,"ROUND_NOT_1_TO_1000",checked,bad)
    def test_missing_real_record_not_silently_accepted(self):
        bad=self.raw.replace(b"1,synthetic001",b"9,synthetic001",1)
        x=checked(bad)
        self.assertFalse(x["exact_paper_reported_120_people_two_games_50_each_source_structure"])
        self.assertEqual(x["source_duplicate_subject_game_round_keys"],1)
    def test_unstable_partner_type_reported_not_excluded(self):
        bad=self.raw.replace(b"1,synthetic001,S,S",b"1,synthetic001,S,W",1)
        x=checked(bad)
        self.assertEqual(x["source_actor_game_groups_player_and_partner_type_stable"],239)
    def test_source_row_less_than_12000_fails(self):
        bad=self.raw.rsplit(b"\n",2)[0]+b"\n"
        self.assertRaisesRegex(a.SourceError,"12000x18_NOT_PINNED",checked,bad)

if __name__=="__main__":unittest.main()
