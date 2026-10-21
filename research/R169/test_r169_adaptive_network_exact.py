"""R169 exact labeled four-node adaptive network and no-op semantics tests."""
from __future__ import annotations
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r169_adaptive_network_exact import (
    N,GRAPHS,OPINIONS,ALPHAS,MODES,HORIZON,
    normalized_state,checked_controls,active_edges,eligible_targets,
    new_graph,direct_transition,enumerated_transition,direct_path,
    enumerated_path,component_count,summary,document
)


class TestR169(unittest.TestCase):
    def check_world(self,gi,oi,ai,mi):
        _,edges=GRAPHS[gi]
        _,op=OPINIONS[oi]
        a=ALPHAS[ai]
        m=MODES[mi]
        state=normalized_state(edges,op)
        left=direct_path(state,a,m)
        right=enumerated_path(state,a,m)
        self.assertEqual(left,right)
        self.assertEqual(len(left),HORIZON+1)
        self.assertEqual(left[0],((state,F(1)),))
        original_edge_count=len(state[0])
        for time,dist in enumerate(left):
            self.assertEqual(sum((v for _,v in dist),F(0)),1)
            self.assertTrue(all(isinstance(v,F) and v>0 for _,v in dist))
            self.assertEqual(len(dist),len({s for s,_ in dist}))
            self.assertEqual(sum(F(0) for _ in dist),0)
            for s,p in dist:
                self.assertEqual(normalized_state(*s),s)
                self.assertEqual(len(s[0]),original_edge_count)
                self.assertTrue(1<=component_count(s[0])<=4)
                if a==0:
                    self.assertEqual(s[0],state[0])
                if a==1:
                    self.assertEqual(s[1],state[1])
                if a==1 and m=="same" and time>0:
                    # Rewiring to a same-opinion vertex strictly reduces
                    # discordance or leaves state fixed.
                    self.assertLessEqual(len(active_edges(s)),len(active_edges(state)))
            metrics=summary(dist)
            self.assertEqual(metrics["distinct_labeled_states"],len(dist))
            self.assertIsInstance(F(metrics["expected_A_count"]),F)
        if a==0:
            other_mode=MODES[1-mi]
            self.assertEqual(left,direct_path(state,a,other_mode))

    def test_frozen_grid_72_worlds(self):
        self.assertEqual(len(GRAPHS)*len(OPINIONS)*len(ALPHAS)*len(MODES),72)

    def test_four_valid_graph_templates(self):
        self.assertEqual([x[0] for x in GRAPHS],["path","star","cycle","chord"])
        self.assertEqual([len(x[1]) for x in GRAPHS],[3,3,4,4])

    def test_all_three_opinion_templates(self):
        self.assertEqual([x[1] for x in OPINIONS],[
            (0,0,1,1),(0,1,0,1),(0,0,0,1)])

    def test_all_graph_templates_are_valid_and_simple(self):
        for _,edges in GRAPHS:
            self.assertEqual(normalized_state(edges,(0,0,0,0))[0],tuple(sorted(edges)))

    def test_edge_sorting_is_canonical(self):
        a=normalized_state(((3,0),(2,1)),(0,0,1,1))
        self.assertEqual(a[0],((0,3),(1,2)))

    def test_direct_oracle_each_world_one_step(self):
        for _,edge in GRAPHS:
            for _,op in OPINIONS:
                s=normalized_state(edge,op)
                for a in ALPHAS:
                    for m in MODES:
                        self.assertEqual(direct_transition(s,a,m),enumerated_transition(s,a,m))

    def test_all_direct_transition_rows_exact_normalization(self):
        for _,edge in GRAPHS:
            for _,op in OPINIONS:
                s=normalized_state(edge,op)
                for a in ALPHAS:
                    for m in MODES:
                        self.assertEqual(sum((p for _,p in direct_transition(s,a,m)),F(0)),1)

    def test_same_rule_zero_active_edges_absorbing(self):
        s=normalized_state(((0,1),(2,3)),(0,0,1,1))
        self.assertEqual(active_edges(s),())
        for a in ALPHAS:
            for m in MODES:
                self.assertEqual(direct_transition(s,a,m),((s,F(1)),))

    def test_consensus_opinions_absorb_every_graph(self):
        for _,edges in GRAPHS:
            for opinion in (0,1):
                s=normalized_state(edges,(opinion,)*4)
                for a in ALPHAS:
                    self.assertEqual(direct_path(s,a,"same"),(( (s,F(1)), ),)*4)

    def test_empty_graph_is_absorbing_even_when_opinions_disagree(self):
        s=normalized_state((),(0,1,0,1))
        self.assertEqual(active_edges(s),())
        self.assertEqual(direct_transition(s,F(1,2),"any"),((s,F(1)),))

    def test_alpha_zero_never_rewires(self):
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                for mode in MODES:
                    for outcome,_ in direct_transition(s,0,mode):
                        self.assertEqual(outcome[0],s[0])

    def test_alpha_zero_rewiring_mode_is_unidentifiable(self):
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                self.assertEqual(direct_path(s,0,"same"),direct_path(s,0,"any"))

    def test_alpha_one_never_changes_any_individual_opinion(self):
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                for mode in MODES:
                    for outcome,_ in direct_transition(s,1,mode):
                        self.assertEqual(outcome[1],s[1])

    def test_alpha_one_all_preserve_A_count(self):
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                for mode in MODES:
                    for path in direct_path(s,1,mode):
                        self.assertTrue(all(sum(t[1])==sum(s[1]) for t,_ in path))

    def test_alpha_zero_can_change_A_count(self):
        observed=False
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                if any(sum(t[1])!=sum(opinions) for t,_ in direct_transition(s,0,"same")):
                    observed=True
        self.assertTrue(observed)

    def test_no_eligible_rewire_has_explicit_no_op(self):
        full_edges=tuple((i,j) for i in range(4) for j in range(i+1,4))
        s=normalized_state(full_edges,(0,0,1,1))
        for mode in MODES:
            self.assertEqual(direct_transition(s,1,mode),((s,F(1)),))
            self.assertEqual(enumerated_transition(s,1,mode),((s,F(1)),))

    def test_no_target_anchor_returns_empty_tuple(self):
        s=normalized_state(((0,1),(0,2),(0,3)),(0,1,0,1))
        for mode in MODES:
            self.assertEqual(eligible_targets(s,0,1,mode),())

    def test_eligibility_does_not_consider_disconnected_original_neighbor(self):
        s=normalized_state(((0,1),), (0,1,0,1))
        self.assertEqual(eligible_targets(s,0,1,"same"),(2,))
        self.assertEqual(eligible_targets(s,0,1,"any"),(2,3))

    def test_eligible_targets_never_include_existing_neighbor(self):
        for _,edges in GRAPHS:
            for _,op in OPINIONS:
                s=normalized_state(edges,op)
                for edge in active_edges(s):
                    for anchor,other in (edge,(edge[1],edge[0])):
                        current={j if i==anchor else i for i,j in edges if anchor in (i,j)}
                        for mode in MODES:
                            actual=eligible_targets(s,anchor,other,mode)
                            self.assertTrue(all(x not in current for x in actual))
                            self.assertNotIn(anchor,actual)
                            self.assertNotIn(other,actual)

    def test_successful_rewire_preserves_exact_edge_count(self):
        s=normalized_state(((0,1),(1,2),(2,3)),(0,0,1,1))
        graph=new_graph(s[0],(1,2),(1,3))
        self.assertEqual(len(graph),len(s[0]))
        self.assertIn((1,3),graph)
        self.assertNotIn((1,2),graph)

    def test_same_rewire_discordance_reduces_or_noop(self):
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                for t,p in direct_transition(s,1,"same"):
                    self.assertTrue(t==s or len(active_edges(t))==len(active_edges(s))-1)

    def test_any_rewire_discordance_never_increases(self):
        for _,edges in GRAPHS:
            for _,opinions in OPINIONS:
                s=normalized_state(edges,opinions)
                for t,p in direct_transition(s,1,"any"):
                    self.assertLessEqual(len(active_edges(t)),len(active_edges(s)))

    def test_same_rewire_some_world_reduces_discordance(self):
        self.assertTrue(any(len(active_edges(t))<len(active_edges(s))
            for _,edges in GRAPHS for _,opinions in OPINIONS
            for s in [normalized_state(edges,opinions)]
            for t,p in direct_transition(s,1,"same")))

    def test_any_rewire_can_preserve_discordance_when_target_disagrees(self):
        self.assertTrue(any(t!=s and len(active_edges(t))==len(active_edges(s))
            for _,edges in GRAPHS for _,opinions in OPINIONS
            for s in [normalized_state(edges,opinions)]
            for t,p in direct_transition(s,1,"any")))

    def test_same_and_any_ever_have_different_labeled_distributions(self):
        self.assertTrue(any(
             direct_transition(normalized_state(edge,op),1,"same")!=
             direct_transition(normalized_state(edge,op),1,"any")
             for _,edge in GRAPHS for _,op in OPINIONS))

    def test_same_and_any_have_equal_opinion_counts_at_alpha_one(self):
        for _,edge in GRAPHS:
            for _,op in OPINIONS:
                s=normalized_state(edge,op)
                for mode in MODES:
                    self.assertEqual({sum(x[1]) for snapshot in direct_path(s,1,mode)
                                      for x,p in snapshot},{sum(op)})

    def test_component_count_four_isolated(self):
        self.assertEqual(component_count(()),4)

    def test_component_count_connected_templates(self):
        for _,edges in GRAPHS:
            self.assertEqual(component_count(edges),1)

    def test_component_count_two_separate_pairs(self):
        self.assertEqual(component_count(((0,1),(2,3))),2)

    def test_node_opinions_do_not_directly_change_components(self):
        s=normalized_state(((0,1),(2,3)),(0,1,1,0))
        self.assertEqual(component_count(s[0]),2)
        for next_state,_ in direct_transition(s,0,"any"):
            self.assertEqual(component_count(next_state[0]),2)

    def test_document_full_72_unique_worlds(self):
        doc=document()
        self.assertEqual(doc["world_count"],72)
        self.assertEqual(len(doc["worlds"]),72)
        self.assertEqual(len({w["id"] for w in doc["worlds"]}),72)
        self.assertTrue(all(w["exact_complete_oracles_equal"] for w in doc["worlds"]))
        self.assertTrue(all(len(w["snapshots"])==4 for w in doc["worlds"]))

    def test_document_frozen_controls(self):
        d=document()
        self.assertEqual(d["frozen_controls"]["edge_count_templates"],[3,3,4,4])
        self.assertTrue(d["frozen_controls"]["target_mode_different_at_alpha1_worlds"])
        self.assertTrue(d["frozen_controls"]["alpha0_graph_fixed"])
        self.assertTrue(d["frozen_controls"]["alpha1_A_count_fixed"])

    def test_original_phase_transition_or_human_data_not_claimed(self):
        d=document()
        self.assertFalse(d["author_phase_transition_recreated"])
        self.assertFalse(d["original_author_event_clock_claimed"])
        self.assertFalse(d["real_network_or_opinion_data_used"])

    def test_canonical_result_json_byte_replay(self):
        file=Path(__file__).with_name("R169_EXACT_RESULTS.json")
        if not file.exists():self.skipTest("CI creates full original JSON before unittest")
        canonical=(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(file.read_bytes(),canonical)

    def test_reject_invalid_alpha(self):
        for value in (True,False,-1,F(1,4),F(3,4),2,0.5,"1/2"):
            with self.assertRaises(ValueError): checked_controls(value,"same")

    def test_reject_invalid_target_mode(self):
        for value in ("homophilic","ALL","",None,False,True,1):
            with self.assertRaises(ValueError): checked_controls(F(1,2),value)

    def test_reject_invalid_opinions(self):
        for value in ((),(0,1,0),(0,1,0,2),(0,1,0,False),
                      (0,1,0,1.0),"0101",None):
            with self.assertRaises(ValueError):
                normalized_state(((0,1),),value)

    def test_reject_invalid_edges(self):
        for edges in (None,"01",((0,0),),((0,4),),((0,1),(1,0)),
                      ((True,1),),((0,1,2),),((0,1.0),)):
            with self.assertRaises(ValueError):
                normalized_state(edges,(0,0,1,1))

    def test_reject_bad_orientation_and_link_removal(self):
        s=normalized_state(((0,1),),(0,1,0,1))
        for i,j in ((-1,1),(0,4),(True,1),(0,0)):
            with self.assertRaises(ValueError):eligible_targets(s,i,j,"same")
        with self.assertRaises(ValueError):new_graph(s[0],(1,2),(0,2))


for gi in range(len(GRAPHS)):
    for oi in range(len(OPINIONS)):
        for ai in range(len(ALPHAS)):
            for mi in range(len(MODES)):
                def build(gi=gi,oi=oi,ai=ai,mi=mi):
                    def test(self):self.check_world(gi,oi,ai,mi)
                    return test
                setattr(TestR169,f"test_frozen_g{gi}_o{oi}_a{ai}_m{mi}",build())


if __name__=="__main__":
    unittest.main()
