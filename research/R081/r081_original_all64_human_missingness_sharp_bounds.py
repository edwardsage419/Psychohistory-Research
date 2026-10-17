#!/usr/bin/env python3
"""R081: immutable author source, all-16 hypothetical binary slot sharp bounds.

All source documents live only in memory of the GitHub Actions runner.
Output contains no raw human IDs, no graph edges, and no per-network metrics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import Counter, defaultdict

from r080_official_dataset_per_file_content_and_role_schema import (
    BASE, MAX_ITEM, SHA256_RE, get, metadata_overview, safe_official_download_url
)
from r080_original_64_networks_human_only_cooperation_topology import (
    BEHAVIOR_ROUNDS, HUMANS_PER_NETWORK,
    NETWORK_COUNT, TREATMENTS, TREATMENT_NET_COUNT, average,
    aggregate_all_64_source_files, exact_source_bytes_retry, parse_network_source
)

PROTOCOL = "protocols/R081_AUTHOR_64_NETWORK_ASSIGNMENT_BOT_ENTITY_AND_MISSINGNESS_BOUNDS_FREEZE_2026-10-17.md"
ORIGINAL_SOURCE_SHA_SET = "555e2127ac21f4532c33a2e0a08f2e081b5f970891bd772c9bac3155d1d53571"
R080_OBSERVED_DELTA = -0.11073225819319567
PRESET_CONTRASTS = (
    ("disengaged_mgmt_bots", "no_bots"),
    ("engaged_mgmt_bots", "no_bots"),
    ("single_mgmt_bot", "no_bots"),
)

def round_bounds(cooperators: int, observed: int, roster: int = 16):
    """Sharp slot-level possible cooperation under all arbitrary completions."""
    if (type(cooperators) is not int or type(observed) is not int
            or type(roster) is not int or not 1 <= observed <= roster
            or not 0 <= cooperators <= observed):
        raise ValueError("R081_INVALID_HUMAN_ROUND_COUNTS")
    missing = roster - observed
    return {
        "observed": observed, "C": cooperators, "missing": missing,
        "observed_rate": cooperators / observed,
        "complete_lower": cooperators / roster,
        "complete_upper": (cooperators + missing) / roster,
    }

def delta_interval(first, last):
    """Endpoint bounds over independently missing binary human slots."""
    return {
        "lower": last["complete_lower"] - first["complete_upper"],
        "upper": last["complete_upper"] - first["complete_lower"],
        "observed_only": last["observed_rate"] - first["observed_rate"],
    }

def bot_graph_structure(doc, bot_ids):
    """Opaque bot-node incidence counts; never serialize actor identifiers."""
    all_one_tie = 0
    all_five_HB = 0
    total = 0
    for snap in doc["result_networks"]:
        degree = Counter()
        hb = 0
        for e in snap["network"]["links"]:
            a, b = e["source"], e["target"]
            if a in bot_ids and b not in bot_ids:
                hb += 1
                degree[a] += 1
            elif b in bot_ids and a not in bot_ids:
                hb += 1
                degree[b] += 1
        total += 1
        if hb == 5:
            all_five_HB += 1
        if len(bot_ids) == 5 and all(degree[b] == 1 for b in bot_ids):
            all_one_tie += 1
    return {
        "snapshots": total,
        "snapshots_exactly_five_HB_edges": all_five_HB,
        "snapshots_every_bot_marked_node_one_HH_neighbor": all_one_tie,
    }

def one_network(doc):
    """Validate original source first; expose a local-only private aggregate."""
    validated = parse_network_source(doc)
    bots = {p for p, is_bot in validated["actor_types_private"].items() if is_bot}
    human = {p for p, is_bot in validated["actor_types_private"].items() if not is_bot}
    rounds = []
    for b in doc["result_behaviors"]:
        human_actions = [
            action["action"] for action in b["cooperation"]
            if action["player"] in human
        ]
        rounds.append(round_bounds(human_actions.count("C"), len(human_actions)))
    if len(rounds) != BEHAVIOR_ROUNDS:
        raise ValueError("R081_ORIGINAL_30_BEHAVIOR_ROUNDS_MISSING")
    change = delta_interval(rounds[0], rounds[-1])
    bot_stats = (
        bot_graph_structure(doc, bots)
        if validated["treatment"] == "single_mgmt_bot" else None
    )
    return {
        "treatment": validated["treatment"],
        "first": rounds[0], "last": rounds[-1],
        "delta": change,
        "all_human_slots_missing": sum(r["missing"] for r in rounds),
        "full_human_response_rounds": sum(r["missing"] == 0 for r in rounds),
        "early_human_coverage": average(r["observed"] / 16 for r in rounds[:15]),
        "late_human_coverage": average(r["observed"] / 16 for r in rounds[15:]),
        "bot_marked_nodes": len(bots),
        "bot_structure": bot_stats,
    }

def summarize_group(xs):
    if not xs:
        raise ValueError("R081_EMPTY_GROUP")
    low = average(x["delta"]["lower"] for x in xs)
    high = average(x["delta"]["upper"] for x in xs)
    observed = average(x["delta"]["observed_only"] for x in xs)
    if low > high + 1e-12:
        raise ValueError("R081_INVALID_SHARP_BOUNDS")
    return {
        "original_networks": len(xs),
        "observed_only_R080_first_last_delta": observed,
        "all16_hypothetical_delta_lower": low,
        "all16_hypothetical_delta_upper": high,
        "forced_increase_networks": sum(x["delta"]["lower"] > 0 for x in xs),
        "forced_decrease_networks": sum(x["delta"]["upper"] < 0 for x in xs),
        "ambiguous_sign_networks": sum(x["delta"]["lower"] <= 0 <= x["delta"]["upper"] for x in xs),
        "first_human_response_coverage": average(x["first"]["observed"] / 16 for x in xs),
        "last_human_response_coverage": average(x["last"]["observed"] / 16 for x in xs),
        "first_missing_human_slots": sum(x["first"]["missing"] for x in xs),
        "last_missing_human_slots": sum(x["last"]["missing"] for x in xs),
        "all30_missing_human_slots": sum(x["all_human_slots_missing"] for x in xs),
        "early15_human_coverage": average(x["early_human_coverage"] for x in xs),
        "late15_human_coverage": average(x["late_human_coverage"] for x in xs),
        "full_16_human_response_network_rounds": sum(x["full_human_response_rounds"] for x in xs),
        "network_rounds": 30 * len(xs),
        "delta_sign_robustly_positive": low > 0,
        "delta_sign_robustly_negative": high < 0,
    }

def describe_all(original_documents):
    # R080 validation is a mandatory guard before output or aggregation.
    if len(original_documents) != NETWORK_COUNT:
        raise ValueError("R081_REQUIRED_ALL64_ORIGINAL_NETWORKS")
    v = [parse_network_source(doc) for doc in original_documents]
    ids = [x["game_id"] for x in v]
    if len(set(ids)) != NETWORK_COUNT:
        raise ValueError("R081_DUPLICATE_ORIGINAL_NETWORK")
    counts = Counter(x["treatment"] for x in v)
    if set(counts) != set(TREATMENTS) or any(counts[t] != TREATMENT_NET_COUNT for t in TREATMENTS):
        raise ValueError("R081_EXACTLY_8_AUTHOR_ARMS_WITH_8_NETWORKS_EACH")
    observations = [one_network(doc) for doc in original_documents]
    by_arm = defaultdict(list)
    for item in observations:
        by_arm[item["treatment"]].append(item)
    arms = {name: summarize_group(by_arm[name]) for name in sorted(TREATMENTS)}
    global_summary = summarize_group(observations)

    contrasts = {}
    for first, second in PRESET_CONTRASTS:
        a, b = arms[first], arms[second]
        low = a["all16_hypothetical_delta_lower"] - b["all16_hypothetical_delta_upper"]
        high = a["all16_hypothetical_delta_upper"] - b["all16_hypothetical_delta_lower"]
        contrasts[first + "_minus_" + second] = {
            "lower": low, "upper": high,
            "observed_only_difference": (
                a["observed_only_R080_first_last_delta"] -
                b["observed_only_R080_first_last_delta"]
            ),
            "strictly_positive_for_every_completion": low > 0,
            "crosses_zero_under_unrestricted_missing_actions": low <= 0 <= high,
            "causally_identified": False,
            "different_experimental_phase": first == "single_mgmt_bot",
        }
    one_arm = by_arm["single_mgmt_bot"]
    one_bot_structure = {
        "original_networks": len(one_arm),
        "source_is_bot_marked_nodes_per_network": sorted(set(x["bot_marked_nodes"] for x in one_arm)),
        "bot_marked_nodes_across_eight_networks": sum(x["bot_marked_nodes"] for x in one_arm),
        "observed_original_graph_snapshots": sum(x["bot_structure"]["snapshots"] for x in one_arm),
        "snapshots_exactly_five_HB_edges": sum(x["bot_structure"]["snapshots_exactly_five_HB_edges"] for x in one_arm),
        "snapshots_every_bot_marked_node_exactly_one_human_neighbor": sum(
            x["bot_structure"]["snapshots_every_bot_marked_node_one_HH_neighbor"]
            for x in one_arm
        ),
        "authors_paper_experiment2_design_claim": "one logical bot with five ties",
        "five_source_nodes_equal_one_logical_bot": "UNVERIFIED_IMPLEMENTATION_MAPPING",
    }
    return {
        "study": "R081",
        "status": "R081_ALL64_ORIGINAL_SOURCE_RECHECKED_HUMAN_MISSINGNESS_SHARP_BOUNDS_E2",
        "evidence_grade": "E2_RETROSPECTIVE_HYPOTHETICAL_BINARY_MISSING_SLOT_IDENTIFICATION_REGION",
        "frozen_before_any_R081_real_bounds": PROTOCOL,
        "R080_source_fingerprint": ORIGINAL_SOURCE_SHA_SET,
        "R080_observed_rate_parity_strict": True,
        "hypothetical_estimand": "all 16 original human slots have a binary response each round, including slots without an observed action",
        "missing_action_assumption": "arbitrary binary completion, no MAR/MCAR/MNAR assumed",
        "source_observed_only_R080": "observed C / observed human C or D; missing is never silently mapped to D",
        "experiment1_arm_random_assignment_evidence": "UNVERIFIED_FROM_MAIN_TEXT_AND_RECORD_LABELS",
        "experiment2_phase_interchangeability": "NOT_IDENTIFIED",
        "all_64_original_networks_equal_weight": global_summary,
        "all_eight_source_treatments_equal_network": arms,
        "only_three_predeclared_noncausal_arm_contrasts": contrasts,
        "experiment2_logical_bot_vs_five_original_bot_nodes": one_bot_structure,
        "human_or_bot_original_actor_ids_exported": False,
        "raw_graph_edges_exported": False,
        "per_network_private_behaviors_exported": False,
        "robot_intervention_causal_effect": "NOT_IDENTIFIED",
        "PESEN_v0.1": "FROZEN",
    }

def source_verified_result():
    metadata_raw, _ = get(BASE)
    md = json.loads(metadata_raw)
    overview = metadata_overview(md)
    if (overview["original_file_count"] != 70
            or overview["file_extensions"] != {"csv": 3, "json": 64, "r": 3}
            or overview["sha256_published_in_file_content_details_count"] != 70):
        raise ValueError("R081_MENDELEY_VERSION1_70_ORIGINAL_SOURCE_FILES_CHANGED")
    files = [f for f in md["files"] if f.get("filename", "").lower().endswith(".json")]
    if len(files) != 64:
        raise ValueError("R081_ORIGINAL_64_JSONS_NOT_PRESENT")
    declared = sorted((f.get("content_details") or {}).get("sha256_hash", "").lower() for f in files)
    if any(not SHA256_RE.fullmatch(h) for h in declared):
        raise ValueError("R081_PUBLISHER_SHA256_MISSING")
    fingerprint = hashlib.sha256("\n".join(declared).encode()).hexdigest()
    if fingerprint != ORIGINAL_SOURCE_SHA_SET:
        raise ValueError("R081_PREVIOUSLY_FROZEN_64_PUBLISHER_SHA_SET_CHANGED")

    all_docs = []
    for f in files:
        c = f.get("content_details") or {}
        expected = c["sha256_hash"]
        size = int(f.get("size") or 0)
        url = c.get("download_url")
        if not safe_official_download_url(url) or not 0 < size <= MAX_ITEM:
            raise ValueError("R081_OFFICIAL_ORIGINAL_NETWORK_URL_OR_SIZE_INVALID")
        raw = exact_source_bytes_retry(f, expected, size, url)
        all_docs.append(json.loads(raw))

    # Required independent parity of R080 original all-64 source grammar and universes.
    old = aggregate_all_64_source_files(md, all_docs)
    if abs(old["all_64_networks_equal_weight_aggregate"]["human_coop_delta"] - R080_OBSERVED_DELTA) > 1e-12:
        raise ValueError("R081_R080_ORIGINAL_ALL64_MACRO_PARITY_CHANGED")
    result = describe_all(all_docs)
    result["original_source"] = {
        "DOI": "10.17632/t963ktp6ft.1",
        "publisher": "Mendeley Data v1",
        "verified_original_network_SHA256_count": 64,
        "original_network_file_sha256_set_fingerprint": fingerprint,
        "publisher_file_count": 70,
        "observed_human_C_D_actions": 27656,
        "possible_human_binary_slots": 30720,
        "observed_source_human_action_count_verified": (
            30720 - result["all_64_original_networks_equal_weight"]["all30_missing_human_slots"]
        ),
    }
    if result["original_source"]["observed_source_human_action_count_verified"] != 27656:
        raise ValueError("R081_R080_SOURCE_HUMAN_ACTION_COVERAGE_CHANGED")
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=pathlib.Path, required=True)
    args = ap.parse_args()
    try:
        result = source_verified_result()
    except (ValueError, OSError, UnicodeError, KeyError, TypeError) as error:
        result = {
            "study": "R081",
            "status": "R081_AUTHOR_SOURCE_OR_RULE_FAILURE_CLOSED",
            "error_type": type(error).__name__,
            "reason": str(error)[:115] if type(error) is ValueError else "SOURCE_SCHEMA_OR_IO_ERROR",
            "real_human_bounds_exported": 0,
            "PESEN_v0.1": "FROZEN",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "source": result.get("original_source"),
        "group_summary": result.get("all_64_original_networks_equal_weight"),
        "contrasts": result.get("only_three_predeclared_noncausal_arm_contrasts"),
        "bot_structure": result.get("experiment2_logical_bot_vs_five_original_bot_nodes"),
        "reason": result.get("reason"),
    }, sort_keys=True))
    if result["status"] != "R081_ALL64_ORIGINAL_SOURCE_RECHECKED_HUMAN_MISSINGNESS_SHARP_BOUNDS_E2":
        raise RuntimeError("R081_RETAIN_FAIL_CLOSED_AND_NO_TRUE_HUMAN_SCORES")

if __name__ == "__main__":
    main()
