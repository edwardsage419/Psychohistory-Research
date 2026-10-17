#!/usr/bin/env python3
"""R100 B1b source identity and partner graph audit, A/B ONLY. No human action cells.

Pure source-check with fail-closed anonymous violation counts. Never serialize
actual focal IDs, partner labels, worksheet names or person-level pairs.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import io
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

from r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only import (
    URL, MAX_SOURCE, OFFICIAL_MD5, ExactOfficialOriginRedirect,
    SourceError, validate_url, verify_bytes, workbook_directory_only,
)
from r100_phase_b0_zenodo_xlsx_ab_tag_structure_only import PINNED_SHA256
from r100_phase_b1a_only_AB_literal_source_code_diagnostic import (
    raw_ab_cells, referenced_shared_strings, resolved_value,
)

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
O = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
P = "{http://schemas.openxmlformats.org/package/2006/relationships}"
SHEETPATH = re.compile(r"xl/worksheets/sheet[1-9][0-9]*\.xml")
ROLENAME = re.compile(r"(.{1,60})_Type ([12])")
EXPECTED = sorted([104, 110, 110, 112, 118])


def approved_workbook_sheet_map(z):
    if "xl/_rels/workbook.xml.rels" not in z.namelist():
        raise SourceError("R100_B1B_WORKBOOK_RELATIONSHIPS_MISSING")
    try:
        wb_raw = z.read("xl/workbook.xml")
        rr_raw = z.read("xl/_rels/workbook.xml.rels")
        if max(len(wb_raw), len(rr_raw)) > 256 * 1024 or any(b"<!DOCTYPE" in x.upper() or b"<!ENTITY" in x.upper() for x in (wb_raw, rr_raw)):
            raise SourceError("R100_B1B_WORKBOOK_XML_UNSAFE")
        workbook = ET.fromstring(wb_raw)
        relations = ET.fromstring(rr_raw)
    except ET.ParseError as exc:
        raise SourceError("R100_B1B_WORKBOOK_RELATIONSHIPS_INVALID") from exc
    refmap = {}
    for rel in relations.findall(P + "Relationship"):
        if rel.attrib.get("TargetMode", "Internal") == "External":
            continue
        if not rel.attrib.get("Type", "").endswith("/worksheet"):
            continue
        target = rel.attrib.get("Target", "")
        if target.startswith("/xl/worksheets/"):
            full = target.lstrip("/")
        elif target.startswith("worksheets/"):
            full = "xl/" + target
        else:
            raise SourceError("R100_B1B_UNSUPPORTED_WORKSHEET_TARGET")
        if not SHEETPATH.fullmatch(full):
            raise SourceError("R100_B1B_UNPINNED_WORKSHEET_TARGET")
        rid = rel.attrib.get("Id", "")
        if not rid or rid in refmap or full not in z.namelist():
            raise SourceError("R100_B1B_RELATIONSHIP_AMBIGUOUS")
        refmap[rid] = full
    root = workbook.find(M + "sheets")
    if root is None:
        raise SourceError("R100_B1B_WORKBOOK_MISSING_SHEETS")
    sheets = root.findall(M + "sheet")
    if len(sheets) != 10 or len(refmap) != 10:
        raise SourceError("R100_B1B_NOT_TEN_SOURCE_SHEETS")
    matched, names = [], set()
    for entry in sheets:
        match = ROLENAME.fullmatch(entry.attrib.get("name", ""))
        rid = entry.attrib.get(O + "id", "")
        if not match or rid not in refmap:
            raise SourceError("R100_B1B_AUTHOR_ORIGINAL_TYPE_NAME_NOT_MATCHED")
        treatment, role = match.group(1), int(match.group(2))
        if (treatment, role) in names:
            raise SourceError("R100_B1B_DUPLICATE_TREATMENT_ROLE")
        names.add((treatment, role))
        matched.append((treatment, role, refmap[rid]))
    cohorts = Counter(name for name, _, _ in matched)
    if len(cohorts) != 5 or any(c != 2 for c in cohorts.values()) or any({role for name, role, _ in matched if name == t} != {1, 2} for t in cohorts):
        raise SourceError("R100_B1B_TREATMENT_SHEET_ROLE_PAIR_INVALID")
    return matched


def extracted_ab_source_blocks(raw):
    identity = verify_bytes(raw)
    if identity["computed_original_SHA256"] != PINNED_SHA256:
        raise SourceError("R100_B1B_FULL_SOURCE_SHA_MISMATCH")
    workbook_directory_only(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        mapping = approved_workbook_sheet_map(z)
        encoded, needed = [], set()
        for treatment, role, file in mapping:
            rows = raw_ab_cells(z.read(file))
            encoded.append((treatment, role, rows))
            for row in rows[1:]:
                for c in ("A", "B"):
                    kind, literal = row[c]
                    if kind == "s" and literal:
                        if not literal.isascii() or not literal.isdecimal() or int(literal) > 50000:
                            raise SourceError("R100_B1B_SHARED_STRING_INDEX_UNSAFE")
                        needed.add(int(literal))
        shared = referenced_shared_strings(z, needed)
    blocks = []
    for treatment, role, rows in encoded:
        for start in range(1, len(rows), 4):
            group = rows[start:start + 4]
            a = [resolved_value(record["A"], shared) for record in group]
            b = [resolved_value(record["B"], shared) for record in group]
            blocks.append((treatment, role, a, b))
    return blocks, identity


def count_components(adjacency):
    unseen = set(adjacency)
    sizes = []
    while unseen:
        start = unseen.pop()
        reached = {start}
        frontier = [start]
        while frontier:
            n = frontier.pop()
            for q in adjacency[n]:
                if q not in reached:
                    reached.add(q)
                    frontier.append(q)
                    unseen.discard(q)
        sizes.append(len(reached))
    return len(sizes), min(sizes) if sizes else 0, max(sizes) if sizes else 0


def assess_blocks(blocks, expected_sizes=None):
    """All strings remain internal. Return anonymous aggregate only."""
    treatment_order = list(dict.fromkeys(t for t, _, _, _ in blocks))
    if len(treatment_order) != 5:
        raise SourceError("R100_B1B_NOT_FIVE_SOURCE_TREATMENTS")
    expected_sizes = EXPECTED if expected_sizes is None else sorted(expected_sizes)
    per = []
    for slot, treatment in enumerate(treatment_order, 1):
        source = [(role, a, b) for name, role, a, b in blocks if name == treatment]
        problems = Counter()
        individuals = []
        for role, a, b in source:
            if len(a) != 4 or len(b) != 4 or a[0] is None or any(v is not None for v in a[1:]):
                problems["A_not_one_code_on_first_row"] += 1
                continue
            if any(x is None for x in b):
                problems["B_missing_code"] += 1
                continue
            own_position = (0, 3) if role == 1 else (1, 2)
            if b[own_position[0]] != b[own_position[1]]:
                problems["focal_repeated_position_mismatch"] += 1
                continue
            self_code = b[own_position[0]]
            opponents = (b[1], b[2]) if role == 1 else (b[0], b[3])
            if self_code in opponents:
                problems["self_as_partner_code"] += 1
            if opponents[0] == opponents[1]:
                problems["same_opponent_two_sessions"] += 1
            individuals.append({"role": role, "aid": a[0], "self": self_code, "peers": opponents})
        raw_a = [p["aid"] for p in individuals]
        raw_self = [p["self"] for p in individuals]
        if len(raw_a) != len(set(raw_a)):
            problems["duplicated_source_A_identifier"] += len(raw_a) - len(set(raw_a))
        if len(raw_self) != len(set(raw_self)):
            problems["duplicated_B_focal_identifier"] += len(raw_self) - len(set(raw_self))
        by_code = {p["self"]: p for p in individuals}
        pair_sets = [set(), set()]
        adjacency = {key: set() for key in by_code}
        directed_seen = set()
        for focal in individuals:
            self_code = focal["self"]
            for phase, other_code in enumerate(focal["peers"]):
                if other_code not in by_code:
                    problems["unmatched_B_partner_code"] += 1
                    continue
                target = by_code[other_code]
                if target["peers"][phase] != self_code:
                    problems["nonreciprocal_partner"] += 1
                if target["role"] == focal["role"]:
                    problems["same_role_within_pair"] += 1
                if target["self"] == self_code:
                    continue
                edge = frozenset((self_code, other_code))
                pair_sets[phase].add(edge)
                adjacency[self_code].add(other_code)
                directed_seen.add((phase, self_code, other_code))
        # Each genuine two-person pair has two focus reports.
        if len(directed_seen) != len(individuals) * 2:
            problems["missing_actor_phase_pairs"] += 1
        if sum(len(ps) for ps in pair_sets) != len(individuals):
            problems["unexpected_pair_session_count"] += 1
        component_count, component_min, component_max = count_components(adjacency)
        per.append({
            "anonymous_treatment_slot": slot,
            "source_four_row_focal_blocks": len(source),
            "parsed_candidate_focals": len(individuals),
            "anonymous_distinct_A_codes": len(set(raw_a)),
            "anonymous_distinct_B_focal_codes": len(set(raw_self)),
            "stage1_undirected_pair_candidates": len(pair_sets[0]),
            "stage2_undirected_pair_candidates": len(pair_sets[1]),
            "person_graph_connected_components": component_count,
            "person_graph_component_smallest": component_min,
            "person_graph_component_largest": component_max,
            "violations": dict(sorted(problems.items())),
        })
    actual_sizes = sorted(x["source_four_row_focal_blocks"] for x in per)
    size_ok = actual_sizes == expected_sizes
    all_ok = size_ok and all(not x["violations"] and x["parsed_candidate_focals"] == x["source_four_row_focal_blocks"] for x in per)
    return {
        "research_id": "R100", "phase": "B1b",
        "status": "B1B_STRICT_SOURCE_PAIR_RECIPROCITY_PASS" if all_ok else "B1B_BLOCKED_BOUNDED",
        "five_original_treatments_expected_sizes_match": size_ok,
        "anonymous_treatment_summaries": per,
        "verified_distinct_source_people": sum(x["anonymous_distinct_A_codes"] for x in per) if all_ok else None,
        "source_pair_full_reciprocity": all_ok,
        "source_two_sessions_same_humans": True,
        "original_person_pair_ids_exported": False,
        "C_to_Z_cell_values_dereferenced": 0,
        "original_human_model_scores": 0,
        "PESEN_v0_1": "FROZEN",
    }


def real_source_audit(raw):
    blocks, identity = extracted_ab_source_blocks(raw)
    result = assess_blocks(blocks)
    result["official_original_bytes"] = identity["original_bytes"]
    result["official_original_MD5"] = OFFICIAL_MD5
    result["official_original_SHA256"] = PINNED_SHA256
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        validate_url(URL)
        req = urllib.request.Request(URL, headers={"User-Agent": "Psychohistory-R100-B1b-AB-partner-graph-only/1.0"})
        with urllib.request.build_opener(ExactOfficialOriginRedirect()).open(req, timeout=55) as response:
            validate_url(response.geturl())
            raw = response.read(MAX_SOURCE + 1)
        result = real_source_audit(raw)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        result = {
            "research_id": "R100", "phase": "B1b",
            "status": "B1B_SOURCE_FAIL_CLOSED",
            "safe_failure": str(exc) if isinstance(exc, SourceError) else "R100_B1B_SOURCE_UNVERIFIED",
            "original_human_model_scores": 0, "PESEN_v0_1": "FROZEN",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "B1B_STRICT_SOURCE_PAIR_RECIPROCITY_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
