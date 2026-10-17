"""R080 42 completely synthetic human-bot graph and source E2 safety checks."""
from __future__ import annotations
import copy,json,unittest
from r080_original_64_networks_human_only_cooperation_topology import (
 parse_network_source,network_moments_validated,aggregate_all_64_source_files,
 NETWORK_COUNT,HUMANS_PER_NETWORK,BEHAVIOR_ROUNDS,NETWORK_SNAPSHOTS,
 TREATMENTS,MEASURES,
)
def fake_network(idx=0,treatment=None,n_bots=0):
 tr=treatment or TREATMENTS[idx//8]
 human=[f"human_{z}" for z in range(16)]
 bots=[f"agent_{z}" for z in range(n_bots)]
 players=[{"player":z,"is_bot":False} for z in human]+[{"player":z,"is_bot":True} for z in bots]
 node_set=[{"id":z} for z in human+bots]
 links=[{"source":human[i],"target":human[(i+1)%16]} for i in range(16)]
 if bots:links.append({"source":bots[0],"target":human[0]})
 snapshots=[{"round":t,"network":{"directed":False,"multigraph":False,
          "nodes":copy.deepcopy(node_set),"links":copy.deepcopy(links)}} for t in range(31)]
 behavior=[{"round":t+1,
            "cooperation":[{"player":z,"action":"C" if (t+i)%2 else "D"}
                for i,z in enumerate(human+bots)],
            "rewiring":[]} for t in range(30)]
 return {"game_id":f"game_{idx}","treatment":tr,
         "players":players,"result_behaviors":behavior,"result_networks":snapshots}
def fake64():
 return [fake_network(i,TREATMENTS[i//8],i%2) for i in range(64)]
def fake_metadata():
 files=[]
 for i in range(64):
  files.append({"filename":f"experiment_{i}.json","folder_id":"raw",
       "size":128,"content_details":{"sha256_hash":"a"*64}})
 for ext in ("r","csv"):
  for j in range(3):
   files.append({"filename":f"author_{ext}_{j}.{ext}","folder_id":"other",
    "size":123,"content_details":{"sha256_hash":"b"*64}})
 return {"version":1,"doi":{"id":"10.17632/t963ktp6ft.1"},"files":files}

class TestR080Original64(unittest.TestCase):
 def setUp(self):self.d=fake_network()
 def check_bad(self,fn,reason):
  d=copy.deepcopy(self.d);fn(d)
  with self.assertRaisesRegex(ValueError,reason):parse_network_source(d)
 def test_01_study_treatment_eight(self):self.assertEqual(len(TREATMENTS),8)
 def test_02_study_original64(self):self.assertEqual(NETWORK_COUNT,64)
 def test_03_16_true_humans(self):self.assertEqual(HUMANS_PER_NETWORK,16)
 def test_04_30_rounds(self):self.assertEqual(BEHAVIOR_ROUNDS,30)
 def test_05_31_snapshots(self):self.assertEqual(NETWORK_SNAPSHOTS,31)
 def test_06_legal_measure_dimensions(self):self.assertEqual(len(MEASURES),22)
 def test_07_genuine_synthetic_parsing(self):
  s=parse_network_source(self.d);self.assertEqual(s["human_nodes"],16)
 def test_08_synthetic_bot_split(self):
  d=fake_network(n_bots=5);s=parse_network_source(d)
  self.assertEqual(s["bot_nodes"],5)
  self.assertEqual(s["human_nodes"],16)
 def test_09_no_bot_in_human_rate(self):
  d=fake_network(n_bots=1)
  a=parse_network_source(d)["human_rates_private"][0]
  for round_ in d["result_behaviors"]:
   round_["cooperation"][-1]["action"]="C" if round_["cooperation"][-1]["action"]=="D" else "D"
  b=parse_network_source(d)["human_rates_private"][0]
  self.assertEqual(a,b)
 def test_10_duplicate_person_rejected(self):
  self.check_bad(lambda x:x["players"].append(copy.deepcopy(x["players"][0])),"DUPLICATE_PLAYER")
 def test_11_nonboolean_bot_rejected(self):
  self.check_bad(lambda x:x["players"][0].update({"is_bot":0}),"BOT_BOOL")
 def test_12_wrong_human_count_rejected(self):
  self.check_bad(lambda x:x["players"][0].update({"is_bot":True}),"EXPECTED_16")
 def test_13_invalid_treatment_rejected(self):
  self.check_bad(lambda x:x.update({"treatment":"HACK"}),"TREATMENT_INVALID")
 def test_14_no_cooperation_field_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0].pop("cooperation"),"ROUND_FIELDS")
 def test_15_no_human_choices_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0].update({"cooperation":[]}),"NO_REAL_HUMAN")
 def test_16_unknown_cooperation_actor_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0]["cooperation"][0].update({"player":"ghost"}),"UNKNOWN_OR_DUPLICATE")
 def test_17_duplicate_human_choice_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0]["cooperation"].append(copy.deepcopy(x["result_behaviors"][0]["cooperation"][0])),"UNKNOWN_OR_DUPLICATE")
 def test_18_non_C_D_action_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0]["cooperation"][0].update({"action":"NA"}),"NON_C_D")
 def test_19_missing_human_action_permitted(self):
  d=copy.deepcopy(self.d);d["result_behaviors"][0]["cooperation"].pop()
  s=parse_network_source(d)
  self.assertLess(s["human_observed_actions"],16*30)
 def test_20_missing_round_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"].pop(),"THIRTY_ACTION_ROUNDS")
 def test_21_out_of_order_behavior_round_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][1].update({"round":1}),"NOT_STRICT")
 def test_22_noninteger_round_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0].update({"round":"1"}),"ROUND_NUMBER_TYPE")
 def test_23_30_network_snapshots_rejected(self):
  self.check_bad(lambda x:x["result_networks"].pop(),"THIRTY_ACTION_ROUNDS")
 def test_24_duplicate_snapshot_round_rejected(self):
  self.check_bad(lambda x:x["result_networks"][1].update({"round":0}),"NETWORK_ROUNDS_NOT_STRICT")
 def test_25_missing_node_rejected(self):
  self.check_bad(lambda x:x["result_networks"][0]["network"]["nodes"].pop(),"EDGE_ENDPOINT_NOT_DECLARED")
 def test_26_directed_edge_graph_rejected(self):
  self.check_bad(lambda x:x["result_networks"][0]["network"].update({"directed":True}),"SIMPLE_UNDIRECTED")
 def test_27_multigraph_rejected(self):
  self.check_bad(lambda x:x["result_networks"][0]["network"].update({"multigraph":True}),"SIMPLE_UNDIRECTED")
 def test_28_unknown_edge_actor_rejected(self):
  self.check_bad(lambda x:x["result_networks"][0]["network"]["links"][0].update({"target":"ghost"}),"UNKNOWN_ACTOR")
 def test_29_self_loop_rejected(self):
  self.check_bad(lambda x:x["result_networks"][0]["network"]["links"][0].update({"target":"human_0"}),"SELF_LOOP")
 def test_30_duplicate_edge_rejected(self):
  self.check_bad(lambda x:x["result_networks"][0]["network"]["links"].append(copy.deepcopy(x["result_networks"][0]["network"]["links"][0])),"DUPLICATE_UNDIRECTED")
 def test_31_invalid_rewiring_actor_rejected(self):
  self.check_bad(lambda x:x["result_behaviors"][0]["rewiring"].append({"sender":"ghost","receiver":"human_0","action":"suggest"}),"REWIRING_ACTOR")
 def test_32_snapshot_edge_type_partition(self):
  s=network_moments_validated(parse_network_source(fake_network(n_bots=1)))
  self.assertEqual(s["edges_first_all"],s["edges_first_HH"]+s["edges_first_HB"]+s["edges_first_BB"])
 def test_33_human_density_only_16_fixed(self):
  s=network_moments_validated(parse_network_source(self.d))
  self.assertAlmostEqual(s["HH_density_first"],16/120)
 def test_34_moments_delta_identity(self):
  s=network_moments_validated(parse_network_source(self.d))
  self.assertAlmostEqual(s["human_coop_delta"],s["human_coop_last"]-s["human_coop_first"])
 def test_35_64_network_synth_valid(self):
  x=aggregate_all_64_source_files(fake_metadata(),fake64())
  self.assertEqual(x["original_source"]["original_human_participant_network_slots"],1024)
  self.assertEqual(x["all_64_networks_equal_weight_aggregate"]["networks"],64)
 def test_36_8_per_stratum(self):
  x=aggregate_all_64_source_files(fake_metadata(),fake64())
  self.assertTrue(all(v["networks"]==8 for v in x["treatment_equal_network_aggregate"].values()))
 def test_37_missing_network_stops_without_partial_score(self):
  with self.assertRaisesRegex(ValueError,"EXACT_64"):
   aggregate_all_64_source_files(fake_metadata(),fake64()[:-1])
 def test_38_duplicate_game_ids_rejected(self):
  x=fake64();x[1]["game_id"]=x[0]["game_id"]
  with self.assertRaisesRegex(ValueError,"DUPLICATE_NETWORK"):
   aggregate_all_64_source_files(fake_metadata(),x)
 def test_39_wrong_treatment_arm_count_rejected(self):
  x=fake64();x[0]["treatment"]=TREATMENTS[1]
  with self.assertRaisesRegex(ValueError,"8_GROUPS_TIMES_8"):
   aggregate_all_64_source_files(fake_metadata(),x)
 def test_40_strict_official_file_manifest(self):
  fake=fake_metadata();fake["files"].pop()
  with self.assertRaisesRegex(ValueError,"70_OFFICIAL_AUTHOR"):
   aggregate_all_64_source_files(fake,fake64())
 def test_41_source_output_no_person_or_single_graph(self):
  x=aggregate_all_64_source_files(fake_metadata(),fake64())
  z=json.dumps(x)
  self.assertNotIn("human_0",z)
  self.assertNotIn("game_0",z)
  self.assertNotIn("snapshots_private",z)
  self.assertNotIn("human_rates_private",z)
 def test_42_strict_science_boundary(self):
  x=aggregate_all_64_source_files(fake_metadata(),fake64())
  self.assertEqual(x["robot_intervention_causal_effect"],"NOT_IDENTIFIED")
  self.assertEqual(x["PESEN_v0.1"],"FROZEN")
 def test_43_legitimate_zero_degree_human_isolate_omitted(self):
  d=copy.deepcopy(self.d)
  for snap in d["result_networks"]:
   snap["network"]["nodes"]=[n for n in snap["network"]["nodes"] if n["id"]!="human_0"]
   snap["network"]["links"]=[e for e in snap["network"]["links"] if "human_0" not in (e["source"],e["target"])]
  val=parse_network_source(d)
  self.assertEqual(val["human_nodes"],16)
  self.assertEqual(len(val["snapshots_private"][0]),14)
  self.assertAlmostEqual(val["human_rates_private"][0],parse_network_source(self.d)["human_rates_private"][0])
 def test_44_omitted_bot_even_if_isolated_is_forbidden(self):
  d=fake_network(n_bots=1)
  d["result_networks"][0]["network"]["nodes"]=[n for n in d["result_networks"][0]["network"]["nodes"] if n["id"]!="agent_0"]
  d["result_networks"][0]["network"]["links"]=[e for e in d["result_networks"][0]["network"]["links"] if "agent_0" not in (e["source"],e["target"])]
  with self.assertRaisesRegex(ValueError,"CANNOT_OMIT_BOT"):
   parse_network_source(d)
 def test_45_unknown_node_even_without_edges_is_forbidden(self):
  d=copy.deepcopy(self.d)
  d["result_networks"][0]["network"]["nodes"].append({"id":"unknown_actor"})
  with self.assertRaisesRegex(ValueError,"DUPLICATE_OR_UNKNOWN_NODE"):
   parse_network_source(d)
if __name__=="__main__":unittest.main()
