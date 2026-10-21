"""R162 artificial copying probabilities versus externally assigned correctness."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r162_prestige_attention_exact import (
    PATTERNS,FAVORED,EXTRA_TICKETS,CORRECT_ACTIONS,
    checked_pattern,params,direct_score,ticket_score,result_document
)

class TestPrestigeCue(unittest.TestCase):
    def check_world(self,pi,ji,li,ci):
        bits=PATTERNS[pi];j=FAVORED[ji]
        extra=EXTRA_TICKETS[li];correct=CORRECT_ACTIONS[ci]
        direct=direct_score(bits,j,extra,correct)
        enumerated=ticket_score(bits,j,extra,correct)
        self.assertEqual(direct,enumerated)
        self.assertTrue(all(isinstance(v,F) for v in direct))
        self.assertTrue(all(0<=v<=1 for v in direct[:4]))
        self.assertTrue(F(-1)<=direct[4]<=1)
        self.assertEqual(direct[4],direct[2]-direct[3])
        self.assertEqual(direct[1],F(sum(bits),3))
        if extra==0:
            self.assertEqual(direct[0],direct[1])
            self.assertEqual(direct[4],0)
        if bits in ((0,0,0),(1,1,1)):
            self.assertEqual(direct[0],direct[1])
            self.assertEqual(direct[4],0)

    def test_fixed_72_scenarios(self):
        self.assertEqual(len(PATTERNS)*len(FAVORED)*len(EXTRA_TICKETS)*len(CORRECT_ACTIONS),72)

    def test_favored_A_one_of_three_becomes_two_thirds(self):
        self.assertEqual(direct_score((1,0,0),0,3,1)[0],F(2,3))

    def test_favored_B_one_of_three_copy_A_one_sixth(self):
        self.assertEqual(direct_score((1,0,0),1,3,1)[0],F(1,6))

    def test_no_attention_bonus_is_neutral(self):
        for bits in PATTERNS:
            for j in FAVORED:
                for correct in CORRECT_ACTIONS:
                    data=direct_score(bits,j,0,correct)
                    self.assertEqual(data[0],F(sum(bits),3))
                    self.assertEqual(data[-1],0)

    def test_high_attention_correctness_help_when_target_correct(self):
        d=direct_score((1,0,0),0,3,1)
        self.assertEqual(d[-1],F(1,3))

    def test_high_attention_correctness_harm_when_target_wrong(self):
        d=direct_score((1,0,0),0,3,0)
        self.assertEqual(d[-1],F(-1,3))

    def test_same_cue_can_help_or_harm_with_same_actions(self):
        good=direct_score((1,0,0),0,3,1)[-1]
        bad=direct_score((1,0,0),0,3,0)[-1]
        self.assertEqual(good,-bad)

    def test_cue_weight_does_not_implicate_real_competence(self):
        d=result_document()
        self.assertFalse(d["prestige_validity_or_competence_measured"])
        self.assertFalse(d["real_demonstrators_or_cue_observations_used"])

    def test_unanimous_A_copy_certain(self):
        for j in FAVORED:
            for extra in EXTRA_TICKETS:
                for correct in CORRECT_ACTIONS:
                    self.assertEqual(direct_score((1,1,1),j,extra,correct)[0],1)

    def test_unanimous_B_copy_certain(self):
        for j in FAVORED:
            for extra in EXTRA_TICKETS:
                for correct in CORRECT_ACTIONS:
                    self.assertEqual(direct_score((0,0,0),j,extra,correct)[0],0)

    def test_unanimity_all_cues_unidentified(self):
        for bits in ((0,0,0),(1,1,1)):
            reference=direct_score(bits,0,0,1)[0]
            for j in FAVORED:
                for extra in EXTRA_TICKETS:
                    self.assertEqual(direct_score(bits,j,extra,1)[0],reference)

    def test_target_indices_indistinguishable_if_zero_bonus(self):
        for bits in PATTERNS:
            self.assertEqual(direct_score(bits,0,0,1),direct_score(bits,1,0,1))
            self.assertEqual(direct_score(bits,1,0,1),direct_score(bits,2,0,1))

    def test_copying_probability_increases_when_A_favored(self):
        for extra in EXTRA_TICKETS[1:]:
            self.assertGreater(direct_score((1,0,0),0,extra,1)[0],F(1,3))

    def test_copying_probability_decreases_when_B_favored(self):
        for extra in EXTRA_TICKETS[1:]:
            self.assertLess(direct_score((1,0,0),1,extra,1)[0],F(1,3))

    def test_response_strength_monotone_given_target_A(self):
        vals=[direct_score((1,0,0),0,l,1)[0] for l in EXTRA_TICKETS]
        self.assertTrue(all(a<b for a,b in zip(vals,vals[1:])))

    def test_response_strength_reverse_given_target_B(self):
        vals=[direct_score((1,0,0),1,l,1)[0] for l in EXTRA_TICKETS]
        self.assertTrue(all(a>b for a,b in zip(vals,vals[1:])))

    def test_action_frequency_alone_does_not_fix_weighted_result(self):
        p0=direct_score((1,0,0),0,3,1)
        p1=direct_score((1,0,0),1,3,1)
        self.assertEqual(p0[1],p1[1])
        self.assertNotEqual(p0[0],p1[0])

    def test_relabel_actions_and_correct_answer_symmetry(self):
        for bits in PATTERNS:
            swapped=tuple(1-x for x in bits)
            for j in FAVORED:
                for l in EXTRA_TICKETS:
                    for correct in CORRECT_ACTIONS:
                        a=direct_score(bits,j,l,correct)
                        b=direct_score(swapped,j,l,1-correct)
                        self.assertEqual(a[0],1-b[0])
                        self.assertEqual(a[2],b[2])
                        self.assertEqual(a[3],b[3])
                        self.assertEqual(a[4],b[4])

    def test_j0_A_copying_tickets_under_strength_one(self):
        self.assertEqual(ticket_score((1,0,0),0,1,1)[0],F(1,2))

    def test_j1_B_copying_tickets_under_strength_one(self):
        self.assertEqual(ticket_score((1,0,0),1,1,1)[0],F(1,4))

    def test_three_demo_sampling_has_no_network_dynamics(self):
        d=result_document()
        self.assertTrue(d["not_original_prestige_model_or_experiment"])
        self.assertEqual(d["case_count"],72)

    def test_reject_invalid_action_sequences(self):
        for bits in ((),(1,0),[0,0,0,1],(2,0,1),("1",0,1),(True,0,1),None):
            with self.assertRaises(ValueError): checked_pattern(bits)

    def test_reject_invalid_favored_index(self):
        for j in (-1,3,False,F(1,2),0.0,"0"):
            with self.assertRaises(ValueError): params(j,0,1)

    def test_reject_invalid_attention_tickets(self):
        for l in (-1,2,4,True,0.0,"3"):
            with self.assertRaises(ValueError): params(0,l,1)

    def test_reject_invalid_ground_truth_choice(self):
        for c in (-1,2,True,0.0,"1"):
            with self.assertRaises(ValueError): params(0,3,c)

    def test_all_72_cases_have_id_and_two_exact_oracles(self):
        d=result_document()
        self.assertEqual(len(d["worlds"]),72)
        self.assertEqual(len({w["id"] for w in d["worlds"]}),72)
        self.assertTrue(all(w["two_independent_Fraction_routes_identical"] for w in d["worlds"]))
        self.assertTrue(d["counterexamples"]["no_bonus_cue_unidentifiable"])
        self.assertTrue(d["counterexamples"]["unanimity_cue_unidentifiable"])

    def test_full_result_json_replay(self):
        path=Path(__file__).with_name("R162_EXACT_RESULTS.json")
        if not path.exists(): self.skipTest("CI builds canonical JSON before tests")
        self.assertEqual(path.read_bytes(),
                         (json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode())

for pi in range(len(PATTERNS)):
    for ji in range(len(FAVORED)):
        for li in range(len(EXTRA_TICKETS)):
            for ci in range(len(CORRECT_ACTIONS)):
                def maker(pi=pi,ji=ji,li=li,ci=ci):
                    def case(self): self.check_world(pi,ji,li,ci)
                    return case
                setattr(TestPrestigeCue,f"test_frozen_p{pi}_j{ji}_l{li}_c{ci}",maker())


if __name__=="__main__":
    unittest.main()
