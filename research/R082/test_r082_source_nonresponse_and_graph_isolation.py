#!/usr/bin/env python3
"""Pure synthetic counterexamples; never read the original human dataset."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r082_source_nonresponse_and_graph_isolation import (
 classify,one_original_doc,summarize,audit_full64,CATS,ARMS,ALIGN,EXPOSURES)

def fake(arm="no_bots",name="synthetic0",missing=None,bot_edges=5):
 missing=set(missing or ())
 bots=5 if arm=="single_mgmt_bot" else (0 if arm=="no_bots" else 16)
 players=[{"player":f"H{i}","is_bot":False} for i in range(16)]
 players +=[{"player":f"B{i}","is_bot":True} for i in range(bots)]
 nodes=[{"id":x["player"]} for x in players]
 def edges(i):
  a=[{"source":f"H{j}","target":f"H{j+1}"} for j in range(15)]
  if bots:
   a +=[{"source":f"H{j%16}","target":f"B{j}"} for j in range(bots if arm!="single_mgmt_bot" else bot_edges if i==0 else bots)]
  return a
 behavior=[]
 for t in range(30):
  choices=[{"player":f"H{h}","action":"C" if h%2 else "D"}
           for h in range(16) if (t,h) not in missing]
  choices +=[{"player":f"B{j}","action":"C"} for j in range(bots)]
  behavior.append({"round":t+1,"cooperation":choices,"rewiring":[]})
 return {"game_id":name,"treatment":arm,"players":players,
  "result_behaviors":behavior,
  "result_networks":[{"round":t,"network":{"directed":False,"multigraph":False,
       "nodes":nodes,"links":edges(t)}} for t in range(31)]}

def seq_with_observed(indices):
 return [i in set(indices) for i in range(30)]

class PatternTaxonomy(unittest.TestCase):
 def test_all_observed(self):self.assertEqual(classify([True]*30),CATS[0])
 def test_never_observed(self):self.assertEqual(classify([False]*30),CATS[1])
 def test_leading_only(self):self.assertEqual(classify(seq_with_observed(range(2,30))),CATS[2])
 def test_trailing_only(self):self.assertEqual(classify(seq_with_observed(range(0,27))),CATS[3])
 def test_both_ends(self):self.assertEqual(classify(seq_with_observed(range(2,27))),CATS[4])
 def test_interior_missing(self):self.assertEqual(classify(seq_with_observed([0,2,29])),CATS[5])
 def test_interior_gaps_take_precedence_over_ends(self):self.assertEqual(classify(seq_with_observed([3,5,26])),CATS[5])
 def test_wrong_count_fails(self):
  with self.assertRaises(ValueError):classify([True]*29)
 def test_nonbool_fails(self):
  with self.assertRaises(ValueError):classify([1]*30)
 def test_no_phantom_person_in_categories(self):
  d=fake()
  self.assertEqual(one_original_doc(d)["cats"][CATS[0]],16)

class OriginalGraphAndHumanRole(unittest.TestCase):
 def test_16_real_humans_30_rounds(self):
  z=one_original_doc(fake())
  self.assertEqual(z["missing"],0)
  self.assertEqual(z["cats"][CATS[0]],16)
 def test_roundwise_missing_action_not_treated_defection(self):
  z=one_original_doc(fake(missing={(0,0),(10,0),(29,0)}))
  self.assertEqual(z["missing"],3)
  self.assertEqual(z["cats"][CATS[5]],1)
 def test_trailing_only_missing_slots(self):
  missing={(t,0) for t in range(25,30)}
  z=one_original_doc(fake(missing=missing))
  self.assertEqual(z["trailing_only_missing_slots"],5)
  self.assertEqual(z["any_final_suffix_missing_slots"],5)
 def test_leading_missing_has_no_trailing(self):
  z=one_original_doc(fake(missing={(0,0),(1,0)}))
  self.assertEqual(z["trailing_only_missing_slots"],0)
  self.assertEqual(z["cats"][CATS[2]],1)
 def test_bot_action_does_not_enter_human_decision_counts(self):
  z=one_original_doc(fake("single_mgmt_bot"))
  self.assertEqual(z["missing"],0)
  self.assertEqual(z["cats"][CATS[0]],16)
 def test_bots_have_five_distinct_record_nodes(self):
  z=one_original_doc(fake("single_mgmt_bot"))
  self.assertEqual(z["bot_HB_hist"][5],31)
  self.assertEqual(z["bot_deg_hist"][1],5*31)
 def test_anomalous_single_snapshot_retained(self):
  z=one_original_doc(fake("single_mgmt_bot",bot_edges=4))
  self.assertEqual(z["bot_anomalies"],1)
  self.assertEqual(z["bot_HB_hist"][4],1)
  self.assertEqual(z["bot_HB_hist"][5],30)
 def test_exposure_matrix_conserves_all_human_response_events(self):
  z=one_original_doc(fake("single_mgmt_bot",missing={(0,0),(29,0)}))
  s=summarize([z])
  for align in ALIGN:
   for ex in EXPOSURES:
    c=s["degree_missingness_associations_both_alignments"][align][ex]
    self.assertEqual(c["degree_zero_missing"]+c["degree_nonzero_missing"],2)
    self.assertEqual(c["degree_zero_observed"]+c["degree_nonzero_observed"],478)
 def test_snapshot_index_two_alignments_both_kept(self):
  d=fake()
  d["result_networks"][0]["network"]["links"]=[]
  z=one_original_doc(d)
  s=summarize([z])
  first=s["degree_missingness_associations_both_alignments"][ALIGN[0]]["no_any_neighbor"]
  second=s["degree_missingness_associations_both_alignments"][ALIGN[1]]["no_any_neighbor"]
  self.assertEqual(first["degree_zero_observed"],16)
  self.assertEqual(second["degree_zero_observed"],0)
 def test_zero_degree_empty_denominator_null(self):
  s=summarize([one_original_doc(fake())])
  c=s["degree_missingness_associations_both_alignments"][ALIGN[0]]["no_any_neighbor"]
  self.assertIsNone(c["missing_risk_degree_zero"])
  self.assertIsNone(c["risk_difference_zero_minus_nonzero"])
 def test_unknown_action_fails(self):
  d=fake()
  d["result_behaviors"][0]["cooperation"].append({"player":"not-on-roster","action":"C"})
  with self.assertRaises(ValueError):one_original_doc(d)
 def test_duplicate_realized_person_fails(self):
  d=fake()
  d["result_behaviors"][0]["cooperation"].append({"player":"H0","action":"C"})
  with self.assertRaises(ValueError):one_original_doc(d)
 def test_wrong_treatment_fails(self):
  d=fake();d["treatment"]="invented_bot"
  with self.assertRaises(ValueError):one_original_doc(d)
 def test_missing_human_roster_fails(self):
  d=fake();d["players"]=[x for x in d["players"] if x["player"]!="H0"]
  with self.assertRaises(ValueError):one_original_doc(d)
 def test_missing_original_snapshot_fails(self):
  d=fake();d["result_networks"]=d["result_networks"][:-1]
  with self.assertRaises(ValueError):one_original_doc(d)
 def test_all_arm_counts_zero_output_fails(self):
  with self.assertRaises(ValueError):audit_full64([fake()])
 def test_every_arm_8_and_private_actor_ids_excluded(self):
  docs=[]
  for arm in ARMS:
   for j in range(8):
    k=len(docs)
    needs=48 if k<56 else 47
    missing={(n//2,n%2) for n in range(needs)}
    docs.append(fake(arm,"synthetic"+str(k),missing=missing))
  r=audit_full64(docs)
  self.assertEqual(r["all64"]["observed_human_CD"],27656)
  self.assertEqual(r["all64"]["missing_human_slots"],3064)
  self.assertEqual(sum(r["all64"]["six_disjoint_human_response_patterns"].values()),1024)
  self.assertEqual(len(r["all_eight_author_treatments"]),8)
  self.assertNotIn('"H0"',str(r))
  self.assertNotIn("synthetic0",str(r))
  self.assertFalse(r["raw_actor_ids_or_edges_exported"])
 def test_arm_count_imbalance_fails(self):
  docs=[fake(arm,"synthetic"+str(k)) for k,arm in enumerate(x for x in ARMS for _ in range(8))]
  docs[0]["treatment"]="single_mgmt_bot"
  with self.assertRaises(ValueError):audit_full64(docs)

if __name__=="__main__":
 unittest.main()
