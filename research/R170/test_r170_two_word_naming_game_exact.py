"""R170 complete finite naming-game probability and input tests."""
from __future__ import annotations
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r170_two_word_naming_game_exact import (
    N,CONTACTS,INVENTORIES,NOISE,FEEDBACK,HORIZON,
    checked_inventory,checked_contacts,checked_controls,words,
    transform_direct,direct_kernel,conditional_heard_probability_A,
    independently_enumerated_kernel,exact_path,oracle_path,metrics,document
)


class TestR170(unittest.TestCase):
    def check_world(self,gi,ii,ni,mi):
        _,edges=CONTACTS[gi]
        _,inv=INVENTORIES[ii]
        nu=NOISE[ni]
        feedback=FEEDBACK[mi]
        actual=exact_path(edges,inv,nu,feedback)
        independent=oracle_path(edges,inv,nu,feedback)
        self.assertEqual(actual,independent)
        self.assertEqual(len(actual),4)
        self.assertEqual(actual[0],((inv,F(1)),))
        for t,dist in enumerate(actual):
            self.assertEqual(sum((prob for _,prob in dist),F(0)),1)
            self.assertTrue(all(isinstance(prob,F) and prob>0 for _,prob in dist))
            self.assertEqual(len(dist),len({v for v,_ in dist}))
            self.assertTrue(all(checked_inventory(v)==v for v,_ in dist))
            mem=metrics(dist)
            self.assertEqual(mem["supported_inventory_vectors"],len(dist))
            self.assertEqual(F(mem["expected_inventory_items"]),sum(
                (p*sum(len(words(x)) for x in v) for v,p in dist),F(0)))
            self.assertEqual(F(mem["expected_bilingual_speakers"]),sum(
                (p*sum(x==3 for x in v) for v,p in dist),F(0)))
            if t:
                previous=dict(actual[t-1])
                next_values={}
                for old,mass in previous.items():
                    for new,weight in direct_kernel(edges,old,nu,feedback):
                        next_values[new]=next_values.get(new,F(0))+mass*weight
                self.assertEqual(dist,tuple(sorted(next_values.items())))
        if ii in (0,1) and nu==0:
            self.assertEqual(actual[1],exact_path(edges,inv,nu,FEEDBACK[1-mi])[1])

    def test_72_frozen_worlds(self):
        self.assertEqual(len(CONTACTS)*len(INVENTORIES)*len(NOISE)*len(FEEDBACK),72)

    def test_4_graphs_preserve_contacts(self):
        self.assertEqual([x[0] for x in CONTACTS],["path","star","cycle","complete"])
        self.assertEqual([len(x[1]) for x in CONTACTS],[3,3,4,6])

    def test_3_initial_word_inventories(self):
        self.assertEqual(INVENTORIES[0][1],(1,1,2,2))
        self.assertEqual(INVENTORIES[1][1],(1,2,1,2))
        self.assertEqual(INVENTORIES[2][1],(1,3,2,3))

    def test_word_masks_and_word_lists(self):
        self.assertEqual(words(1),(1,))
        self.assertEqual(words(2),(2,))
        self.assertEqual(words(3),(1,2))

    def test_independent_direct_kernel_identity_all_frozen_initial_worlds(self):
        for _,edges in CONTACTS:
            for _,initial in INVENTORIES:
                for nu in NOISE:
                    for fb in FEEDBACK:
                        self.assertEqual(direct_kernel(edges,initial,nu,fb),
                                         independently_enumerated_kernel(edges,initial,nu,fb))

    def test_direct_kernel_exact_normalization_all_initial_worlds(self):
        for _,edges in CONTACTS:
            for _,initial in INVENTORIES:
                for nu in NOISE:
                    for fb in FEEDBACK:
                        self.assertEqual(sum((p for _,p in direct_kernel(edges,initial,nu,fb)),F(0)),1)

    def test_initial_all_A_or_B_unanimity_absorbs_when_no_noise(self):
        for _,edges in CONTACTS:
            for fb in FEEDBACK:
                for v in (1,2):
                    state=(v,)*4
                    self.assertEqual(direct_kernel(edges,state,0,fb),((state,F(1)),))
                    self.assertEqual(exact_path(edges,state,0,fb),
                                     (((state,F(1)),),)*4)

    def test_noise_destroys_strict_unanimity_absorption(self):
        for _,edges in CONTACTS:
            for fb in FEEDBACK:
                for v in (1,2):
                    s=(v,)*4
                    for nu in NOISE[1:]:
                        self.assertNotEqual(direct_kernel(edges,s,nu,fb),((s,F(1)),))

    def test_bilingual_speaker_distinguishes_feedback_modes_immediately(self):
        for _,edges in CONTACTS:
            s=INVENTORIES[2][1]
            left=exact_path(edges,s,0,"both_confirm")[1]
            right=exact_path(edges,s,0,"listener_only")[1]
            self.assertNotEqual(left,right)

    def test_all_monolingual_speakers_feedback_modes_equal_on_first_noiseless_event(self):
        for _,edges in CONTACTS:
            for _,s in INVENTORIES[:2]:
                self.assertEqual(
                    exact_path(edges,s,0,"both_confirm")[1],
                    exact_path(edges,s,0,"listener_only")[1])

    def test_noise_can_change_monolingual_speaker_under_both_confirm(self):
        s=(1,2,2,2)
        after=transform_direct(s,0,1,2,"both_confirm")
        self.assertEqual(after[0],2)

    def test_noisy_message_channel_half_erases_utterance_choice(self):
        for mask in (1,2,3):
            self.assertEqual(conditional_heard_probability_A(mask,F(1,2)),F(1,2))

    def test_noiseless_utterance_A_prob_depends_on_speaker_inventory(self):
        self.assertEqual(conditional_heard_probability_A(1,0),1)
        self.assertEqual(conditional_heard_probability_A(2,0),0)
        self.assertEqual(conditional_heard_probability_A(3,0),F(1,2))

    def test_message_A_chance_for_singleton_A_under_quarter_noise(self):
        self.assertEqual(conditional_heard_probability_A(1,F(1,4)),F(3,4))
        self.assertEqual(conditional_heard_probability_A(2,F(1,4)),F(1,4))
        self.assertEqual(conditional_heard_probability_A(3,F(1,4)),F(1,2))

    def test_recognition_both_confirm_resets_bilingual_speaker(self):
        self.assertEqual(transform_direct((3,1,2,2),0,1,1,"both_confirm"),
                         (1,1,2,2))

    def test_recognition_listener_only_preserves_bilingual_speaker(self):
        self.assertEqual(transform_direct((3,1,2,2),0,1,1,"listener_only"),
                         (3,1,2,2))

    def test_failure_adds_word_only_to_listener(self):
        for fb in FEEDBACK:
            self.assertEqual(transform_direct((1,2,1,1),0,1,1,fb),(1,3,1,1))

    def test_bilingual_listener_success_shrinks_inventory(self):
        for fb in FEEDBACK:
            self.assertEqual(transform_direct((1,3,2,2),0,1,1,fb),(1,1,2,2))

    def test_listener_only_never_updates_speaker(self):
        for sender in (1,2,3):
            for listener in (1,2,3):
                for utterance in (1,2):
                    state=(sender,listener,1,2)
                    out=transform_direct(state,0,1,utterance,"listener_only")
                    self.assertEqual(out[0],sender)

    def test_no_invalid_or_empty_vocab_states_in_complete_path(self):
        for _,edges in CONTACTS:
            for _,s in INVENTORIES:
                for nu in NOISE:
                    for fb in FEEDBACK:
                        for dist in exact_path(edges,s,nu,fb):
                            self.assertTrue(all(all(x in (1,2,3) for x in state)
                                                for state,p in dist))

    def test_graph_topology_changes_communication_probabilities(self):
        path=CONTACTS[0][1]
        star=CONTACTS[1][1]
        s=INVENTORIES[0][1]
        self.assertNotEqual(exact_path(path,s,0,"both_confirm")[1],
                            exact_path(star,s,0,"both_confirm")[1])

    def test_complete_network_speaker_orientation_symmetric(self):
        edges=CONTACTS[3][1]
        state=(1,1,1,1)
        self.assertEqual(direct_kernel(edges,state,0,"both_confirm"),((state,F(1)),))

    def test_different_initial_inventory_types_change_possible_updates(self):
        edges=CONTACTS[0][1]
        a=direct_kernel(edges,INVENTORIES[0][1],0,"both_confirm")
        b=direct_kernel(edges,INVENTORIES[2][1],0,"both_confirm")
        self.assertNotEqual(a,b)

    def test_expected_memory_at_initial_bilingual_pattern(self):
        s=INVENTORIES[2][1]
        v=metrics(((s,F(1)),))
        self.assertEqual(v["expected_inventory_items"],"6")
        self.assertEqual(v["expected_bilingual_speakers"],"2")

    def test_expected_memory_at_initial_monolingual_pattern(self):
        for _,s in INVENTORIES[:2]:
            v=metrics(((s,F(1)),))
            self.assertEqual(v["expected_inventory_items"],"4")
            self.assertEqual(v["expected_bilingual_speakers"],"0")

    def test_noise_makes_vocabulary_size_more_than_four_possible(self):
        s=(1,1,1,1)
        edges=CONTACTS[0][1]
        result=direct_kernel(edges,s,F(1,4),"listener_only")
        self.assertTrue(any(sum(len(words(x)) for x in state)>4 for state,p in result))

    def test_communication_success_fidelity_not_same_as_word_frequency(self):
        s=(3,1,2,3)
        a=conditional_heard_probability_A(s[0],0)
        self.assertEqual(a,F(1,2))
        self.assertEqual(len(words(s[0])),2)

    def test_all_72_full_document_worlds_and_snapshots(self):
        d=document()
        self.assertEqual(d["frozen_world_count"],72)
        self.assertEqual(len(d["worlds"]),72)
        self.assertEqual(len({v["id"] for v in d["worlds"]}),72)
        self.assertTrue(all(v["independent_exact_oracles_equal"] for v in d["worlds"]))
        self.assertTrue(all(len(v["snapshots"])==4 for v in d["worlds"]))

    def test_all_prescored_controls(self):
        c=document()["prespecified_controls"]
        self.assertTrue(c["bilingual_split_feedback_first_step_different_without_noise"])
        self.assertTrue(c["nu_half_delivered_A_equals_half_all_inventory_masks"])
        self.assertTrue(c["nu_zero_consensus_A_absorbing"])
        self.assertTrue(c["nu_quarter_consensus_A_nonabsorbing"])

    def test_author_original_and_human_data_exclusions(self):
        d=document()
        self.assertFalse(d["original_Baronchelli_unbounded_vocabulary_model_reproduced"])
        self.assertFalse(d["original_human_utterance_data_used"])
        self.assertFalse(d["real_language_decline_estimated"])

    def test_canonical_full_JSON_byte_replay(self):
        file=Path(__file__).with_name("R170_EXACT_RESULTS.json")
        if not file.exists():self.skipTest("CI creates canonical data first")
        expected=(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(file.read_bytes(),expected)

    def test_reject_invalid_inventory(self):
        for bad in (None,(),(1,2,3),(0,1,2,3),(1,2,3,4),
                    (1,2,3,False),(1,2,3,1.0),(1,2,3,"1")):
            with self.assertRaises(ValueError):checked_inventory(bad)

    def test_reject_invalid_edges(self):
        for bad in (None,(),((0,0),),((0,4),),((0,1),(1,0)),
                    ((True,2),),((0,1,2),),((0.0,1),),"01"):
            with self.assertRaises(ValueError):checked_contacts(bad)

    def test_reject_bad_channel_probabilities(self):
        for bad in (-1,1,F(1,8),True,False,0.25,"1/4"):
            with self.assertRaises(ValueError):checked_controls(bad,"both_confirm")

    def test_reject_bad_feedback(self):
        for bad in ("speaker_only","both","",None,False,True,0):
            with self.assertRaises(ValueError):checked_controls(0,bad)

    def test_reject_bad_word_mask(self):
        for bad in (0,4,True,False,1.0,"1",None):
            with self.assertRaises(ValueError):words(bad)

    def test_reject_bad_conversation_roles(self):
        s=(1,2,1,2)
        for speaker,hearer in ((0,0),(-1,1),(0,4),(False,1),(1,True)):
            with self.assertRaises(ValueError):
                transform_direct(s,speaker,hearer,1,"both_confirm")

    def test_reject_bad_delivered_token(self):
        for bad in (0,3,False,True,1.0,"A",None):
            with self.assertRaises(ValueError):
                transform_direct((1,2,1,2),0,1,bad,"listener_only")

    def test_reject_invalid_metrics_probability_mass(self):
        with self.assertRaises(AssertionError):
            metrics((((1,2,1,2),F(1,2)),))


for gi in range(len(CONTACTS)):
    for ii in range(len(INVENTORIES)):
        for ni in range(len(NOISE)):
            for mi in range(len(FEEDBACK)):
                def create(gi=gi,ii=ii,ni=ni,mi=mi):
                    def test(self): self.check_world(gi,ii,ni,mi)
                    return test
                setattr(TestR170,f"test_frozen_g{gi}_i{ii}_n{ni}_m{mi}",create())


if __name__=="__main__":
    unittest.main()
