"""R110 C0 pure synthetic 120-human x two-game x 50-round peer-vs-shrink Brier."""
import hashlib,unittest
from unittest.mock import patch
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
import r110_phase_b0_2015_PLOS_original_12000_CSV_row_width_and_18_public_headers_only as p0
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as p1
import r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier as d

def peer_of(sid):
    return sid+1 if sid%2 else sid-1

def simulate(mode="peer"):
    choose={}
    for g in ("sym","asym"):
        for t in range(1,51):
            for sid in range(1,121):
                if t==1:y=sid%2
                elif mode=="peer":y=choose[(peer_of(sid),g,t-1)]
                elif mode=="self":y=choose[(sid,g,t-1)]
                else:y=(sid+t)%2
                choose[(sid,g,t)]=y
    lines=[",".join(d.HEAD)]
    for sid in range(1,121):
        for g in ("sym","asym"):
            pt="S" if sid%2 else "W"
            partner_t=pt if g=="sym" else ("W" if pt=="S" else "S")
            for t in range(1,51):
                row=["X"]*18
                row[0]=str(t);row[1]="TEST%03d"%sid;row[2]=pt;row[3]=partner_t
                row[9]=g
                row[15]=str(choose[(sid,g,t)])
                row[8]="" if t==1 else str(choose[(peer_of(sid),g,t-1)])
                row[16]="0" if t>1 else ""
                row[11]="PRIVATE_PUNISHMENT_NOT_ACCESSED"
                lines.append(",".join(row))
    return ("\n".join(lines)+"\n").encode()

def run(data,enforce_real=True):
    sha=hashlib.sha256(data).hexdigest()
    with patch.object(p0,"PINNED_SHA",sha),\
         patch.object(p0,"EXPECTED_BYTES",len(data)),\
         patch.object(p1,"PINNED_SHA",sha):
        return d.evaluate_original_source(data,enforce_real_source=enforce_real)

class FixedUCLHumanLagModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.peer=simulate("peer")
        cls.scored=run(cls.peer)
    def test_original_synthetic_120human_two50_source(self):
        x=self.scored
        self.assertTrue(x["original_120_actor_two_50_game_roster_exact"])
        self.assertEqual(x["total_true_original_person_game_round_records"],12000)
        self.assertEqual(x["source_distinct_actors_with_eligible_targets"],120)
        self.assertEqual(x["source_game_categories_with_eligible_targets"],2)
    def test_exact_first_round_exclusion_and_11760_targets(self):
        self.assertEqual(self.scored["source_legal_target_exclusion_reason_counts"]["first_round_each_actor_game"],240)
        self.assertEqual(self.scored["source_eligible_next_binary_actions"],11760)
    def test_forecast_identical_source_target_denominators(self):
        self.assertEqual(set(self.scored["overall_identical_source_next_action_targets"]["brier"]),set(d.MODELS))
        self.assertEqual(self.scored["overall_identical_source_next_action_targets"]["scored_actions"],11760)
    def test_genuine_peer_lag_has_synthetic_predictive_gain(self):
        self.assertGreater(self.scored["overall_identical_source_next_action_targets"]["gains"]["M3_vs_M2_equal_shrink"],0)
    def test_all_five_model_probabilities_sane(self):
        self.assertTrue(all(0<=x<=1 for x in self.scored["overall_identical_source_next_action_targets"]["brier"].values()))
    def test_real_negative_example_preserved_by_competitor(self):
        x=run(simulate("self"))
        self.assertEqual(x["overall_identical_source_next_action_targets"]["brier"]["M1"],0)
        self.assertLess(x["overall_identical_source_next_action_targets"]["gains"]["M3_vs_M1_own_lag"],0)
    def test_early_late_fixed_cover_all_same_targets(self):
        self.assertEqual(self.scored["early_t2_to_t10"]["scored_actions"]+self.scored["late_t11_to_t50"]["scored_actions"],11760)
    def test_original_subject_level_directions_never_as_6_sessions(self):
        self.assertEqual(len(self.scored["anonymous_source_actor_level_results"]),120)
        self.assertTrue(self.scored["not_genuine_lab_session_LOSO"])
        self.assertFalse(self.scored["original_source_has_true_lab_session_ID"])
        self.assertFalse(self.scored["original_source_has_counterpart_person_ID"])
    def test_original_person_ID_or_punishment_never_exported(self):
        rendered=str(self.scored)
        self.assertNotIn("TEST001",rendered)
        self.assertNotIn("PRIVATE_PUNISHMENT_NOT_ACCESSED",rendered)
        self.assertFalse(self.scored["original_source_actor_ID_or_choice_values_exported"])
    def test_M4_sham_is_not_asserted_true_other_person(self):
        self.assertTrue(self.scored["same_marginal_sham_donor_might_be_actual_partner"])
        self.assertTrue(self.scored["original_author_prior_partner_signal_not_independently_partner_ID_verified"])
    def test_brier_noncausal_nonprospective(self):
        self.assertTrue(self.scored["not_causal_social_learning"])
        self.assertTrue(self.scored["not_prospective_calendar_E3"])
        self.assertTrue(self.scored["not_exact_R073_model_reproduction"])
    def test_fixed_Laplace(self):
        self.assertEqual(d.fixed_laplace(0,0),0.5)
        self.assertEqual(d.fixed_laplace(2,3),3/5)
    def test_strict_binary(self):
        for s,y in (("0",0),("1",1),("0.0",0),("1.0",1)):
            self.assertEqual(d.binary(s),y)
        for s in ("2","NA","", "C","D"):
            self.assertIsNone(d.binary(s))
    def test_reproducible_two_thousand_fixed_bootstrap(self):
        self.assertEqual(self.scored["fixed_source_actor_bootstrap_descriptive_only"]["M3_vs_M2_equal_shrink"]["subject_cluster_bootstrap_n"],2000)
        self.assertEqual(self.scored["fixed_source_actor_bootstrap_descriptive_only"]["M3_vs_M2_equal_shrink"]["fixed_seed"],110)
    def test_missing_partner_previous_observation_excluded(self):
        changed=self.peer.replace(b"2,TEST001",b"2,TEST001",1)
        self.assertEqual(changed,self.peer)
        self.assertTrue("prior_partner_optout_or_unknown" not in self.scored["source_legal_target_exclusion_reason_counts"])
    def test_source_real_sha_not_fake_claimed(self):
        self.assertRaises(a.SourceError,d.evaluate_original_source,self.peer)
    def test_mode_no_behavior_permitted_before_source_forbidden(self):
        self.assertIn("M3_vs_M4_same_marginal_shuffled_peer",self.scored["overall_identical_source_next_action_targets"]["gains"])

if __name__=="__main__":unittest.main()
