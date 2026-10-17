#!/usr/bin/env python3
"""Synthetic-only R081 source guards and exact binary completion bounds."""
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "R080"))

from r081_original_all64_human_missingness_sharp_bounds import (
    TREATMENTS, round_bounds, delta_interval, bot_graph_structure,
    one_network, summarize_group, describe_all, ORIGINAL_SOURCE_SHA_SET
)

def author_like_doc(treatment="no_bots", bot_count=0, game="synthetic",
                    missing=None, full_coop=False):
    missing = missing or {}
    people = [{"player": "human" + str(i), "is_bot": False} for i in range(16)]
    people += [{"player": "bot" + str(i), "is_bot": True} for i in range(bot_count)]
    names = [p["player"] for p in people]
    # Keep bot graph edges confined to one distinct human per bot.
    edges = [{"source": "bot" + str(i), "target": "human" + str(i)}
             for i in range(bot_count)]
    return {
        "game_id": game,
        "treatment": treatment,
        "players": people,
        "result_behaviors": [
            {"round": rnd, "cooperation": [
                {"player": "human" + str(i),
                 "action": "C" if full_coop or i % 2 == 0 else "D"}
                for i in range(16) if i not in missing.get(rnd, ())
            ], "rewiring": []}
            for rnd in range(1, 31)
        ],
        "result_networks": [
            {"round": rnd, "network": {
                "directed": False, "multigraph": False,
                "nodes": [{"id": name} for name in names],
                "links": edges,
            }} for rnd in range(31)
        ],
    }

class PureBounds(unittest.TestCase):
    def test_all_observed(self):
        a = round_bounds(8, 16)
        self.assertEqual((a["complete_lower"], a["complete_upper"]), (.5, .5))

    def test_none_observed_forbidden(self):
        with self.assertRaises(ValueError):
            round_bounds(0, 0)

    def test_more_cooperation_than_observed_forbidden(self):
        with self.assertRaises(ValueError):
            round_bounds(9, 8)

    def test_boolean_counts_forbidden(self):
        with self.assertRaises(ValueError):
            round_bounds(True, 2)

    def test_all_missing_except_one(self):
        a = round_bounds(1, 1)
        self.assertEqual((a["complete_lower"], a["complete_upper"]), (1 / 16, 1.0))

    def test_defector_only_observed(self):
        a = round_bounds(0, 3)
        self.assertEqual(a["complete_upper"], 13 / 16)

    def test_exact_endpoint_extremes(self):
        before, after = round_bounds(0, 16), round_bounds(16, 16)
        self.assertEqual(delta_interval(before, after)["lower"], 1)

    def test_ambiguous_change(self):
        before, after = round_bounds(1, 1), round_bounds(0, 1)
        d = delta_interval(before, after)
        self.assertLess(d["lower"], 0)
        self.assertGreater(d["upper"], 0)

    def test_two_slot_full_enumeration_sharpness(self):
        before, after = round_bounds(0, 1, roster=2), round_bounds(1, 1, roster=2)
        d = delta_interval(before, after)
        outcomes = [(1 + late) / 2 - early / 2 for early in (0, 1) for late in (0, 1)]
        self.assertEqual(d["lower"], min(outcomes))
        self.assertEqual(d["upper"], max(outcomes))

class OriginalSourceGates(unittest.TestCase):
    def test_human_bot_structural_five_nodes(self):
        doc = author_like_doc("single_mgmt_bot", 5)
        info = one_network(doc)
        self.assertEqual(info["bot_marked_nodes"], 5)
        self.assertEqual(info["bot_structure"]["snapshots"], 31)
        self.assertEqual(info["bot_structure"]["snapshots_exactly_five_HB_edges"], 31)
        self.assertEqual(info["bot_structure"]["snapshots_every_bot_marked_node_one_HH_neighbor"], 31)

    def test_bot_degree_nonconforming_preserved_as_zero_not_ignored(self):
        doc = author_like_doc("single_mgmt_bot", 5)
        doc["result_networks"][0]["network"]["links"] = doc["result_networks"][0]["network"]["links"][:-1]
        info = one_network(doc)
        self.assertEqual(info["bot_structure"]["snapshots_exactly_five_HB_edges"], 30)
        self.assertEqual(info["bot_structure"]["snapshots_every_bot_marked_node_one_HH_neighbor"], 30)

    def test_non_bot_arm_structure_none(self):
        self.assertIsNone(one_network(author_like_doc())["bot_structure"])

    def test_first_last_missing_counts(self):
        doc = author_like_doc(missing={1: [0, 1], 30: [0]})
        x = one_network(doc)
        self.assertEqual(x["first"]["missing"], 2)
        self.assertEqual(x["last"]["missing"], 1)
        self.assertEqual(x["all_human_slots_missing"], 3)
        self.assertEqual(x["full_human_response_rounds"], 28)

    def test_no_human_actions_in_round_fails(self):
        doc = author_like_doc(missing={3: list(range(16))})
        with self.assertRaises(ValueError):
            one_network(doc)

    def test_duplicate_person_round_fails(self):
        doc = author_like_doc()
        doc["result_behaviors"][0]["cooperation"].append(
            {"player": "human0", "action": "C"})
        with self.assertRaises(ValueError):
            one_network(doc)

    def test_non_binary_action_fails(self):
        doc = author_like_doc()
        doc["result_behaviors"][0]["cooperation"][0]["action"] = "MISSING"
        with self.assertRaises(ValueError):
            one_network(doc)

    def test_unknown_graph_endpoint_fails(self):
        doc = author_like_doc()
        doc["result_networks"][0]["network"]["links"].append(
            {"source": "human0", "target": "stranger"})
        with self.assertRaises(ValueError):
            one_network(doc)

    def test_network_snapshot_cannot_omit_bot(self):
        doc = author_like_doc("single_mgmt_bot", 5)
        doc["result_networks"][0]["network"]["nodes"] = (
            doc["result_networks"][0]["network"]["nodes"][:-1])
        with self.assertRaises(ValueError):
            one_network(doc)

    def test_unconnected_human_snapshot_isolate_allowed(self):
        doc = author_like_doc()
        doc["result_networks"][0]["network"]["nodes"] = (
            doc["result_networks"][0]["network"]["nodes"][:-1])
        self.assertEqual(one_network(doc)["bot_marked_nodes"], 0)

    def test_invalid_temporal_round_index_fails(self):
        doc = author_like_doc()
        doc["result_behaviors"][1]["round"] = 1
        with self.assertRaises(ValueError):
            one_network(doc)

    def test_summary_counts_and_bounds(self):
        doc = author_like_doc(missing={1: [0, 1], 30: [0]})
        m = summarize_group([one_network(doc)])
        self.assertEqual(m["original_networks"], 1)
        self.assertEqual(m["all30_missing_human_slots"], 3)
        self.assertLessEqual(m["all16_hypothetical_delta_lower"],
                             m["all16_hypothetical_delta_upper"])

    def test_invalid_64_universe_fails(self):
        with self.assertRaises(ValueError):
            describe_all([author_like_doc()])

    def test_source_fingerprint_is_frozen(self):
        self.assertEqual(
            ORIGINAL_SOURCE_SHA_SET,
            "555e2127ac21f4532c33a2e0a08f2e081b5f970891bd772c9bac3155d1d53571"
        )

    def test_all64_synthetic_gives_zero_effect_and_no_person_leak(self):
        bots = {
            "no_bots": 0,
            "single_mgmt_bot": 5,
        }
        docs = [author_like_doc(
            treatment=t, bot_count=bots.get(t, 16), game="synthetic" + str(k)
        ) for k, t in enumerate([x for x in TREATMENTS for _ in range(8)])]
        result = describe_all(docs)
        self.assertEqual(result["all_64_original_networks_equal_weight"]["original_networks"], 64)
        self.assertEqual(result["all_64_original_networks_equal_weight"]["all30_missing_human_slots"], 0)
        self.assertEqual(result["all_64_original_networks_equal_weight"]["observed_only_R080_first_last_delta"], 0)
        self.assertFalse(result["human_or_bot_original_actor_ids_exported"])
        self.assertNotIn("game_id", str(result))
        self.assertEqual(len(result["only_three_predeclared_noncausal_arm_contrasts"]), 3)

    def test_wrong_arm_counts_fail(self):
        docs = [author_like_doc(t, 5 if t == "single_mgmt_bot" else 0,
                    game="synthetic" + str(i))
                for i, t in enumerate([x for x in TREATMENTS for _ in range(8)])]
        docs[-1]["treatment"] = "no_bots"
        with self.assertRaises(ValueError):
            describe_all(docs)

if __name__ == "__main__":
    unittest.main()
