#!/usr/bin/env python3
"""R100 B1a: audit ONLY Excel A/B identity and pairing code representation.

No C:Z cell value dereference, no names, IDs, code examples, or microdata output.
All public counts refer to source-format eligibility, not independent subjects.
"""
from __future__ import annotations
import argparse
from collections import Counter
import io
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

from r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only import (
    URL, MAX_SOURCE, OFFICIAL_MD5, ExactOfficialOriginRedirect, SourceError,
    validate_url, verify_bytes, workbook_directory_only,
)
from r100_phase_b0_zenodo_xlsx_ab_tag_structure_only import PINNED_SHA256

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SHEET_RE = re.compile(r"xl/worksheets/sheet([1-9][0-9]*)\.xml")
CELL_RE = re.compile(r"([AB])([1-9][0-9]*)")
CODE_RE = re.compile(r"[A-Za-z0-9 _.:;,/#=()+-]{1,64}")


def sanitized_token(value):
    if not isinstance(value, str) or not CODE_RE.fullmatch(value) or value != value.strip():
        raise SourceError("R100_B1A_AB_LITERAL_UNSUPPORTED")
    return value


def raw_ab_cells(sheet_bytes):
    if len(sheet_bytes) > 8 * 1024 * 1024 or b"<!DOCTYPE" in sheet_bytes.upper() or b"<!ENTITY" in sheet_bytes.upper():
        raise SourceError("R100_B1A_UNSAFE_WORKSHEET_XML")
    row_index, cells, rows = 0, {}, []
    try:
        for event, node in ET.iterparse(io.BytesIO(sheet_bytes), events=("end",)):
            if node.tag == NS + "c":
                address = node.attrib.get("r", "")
                match = CELL_RE.fullmatch(address)
                if match:
                    col, pos = match.group(1), int(match.group(2))
                    if pos != len(rows) + 1:
                        raise SourceError("R100_B1A_WRONG_CELL_ROW")
                    if col in cells:
                        raise SourceError("R100_B1A_DUPLICATE_IDENTITY_CELL")
                    if node.find(NS + "f") is not None:
                        raise SourceError("R100_B1A_FORMULA_IN_AB")
                    kind = node.attrib.get("t", "n")
                    if kind not in ("n", "s", "inlineStr", "str"):
                        raise SourceError("R100_B1A_AB_TYPE_NOT_ALLOWED")
                    if kind == "inlineStr":
                        obj = node.find(NS + "is")
                        val = "".join(obj.itertext()) if obj is not None else ""
                    else:
                        obj = node.find(NS + "v")
                        val = obj.text if obj is not None and obj.text is not None else ""
                    cells[col] = (kind, val)
                node.clear()
            elif node.tag == NS + "row":
                n = node.attrib.get("r", "")
                if not n.isascii() or not n.isdecimal() or int(n) != len(rows) + 1:
                    raise SourceError("R100_B1A_NONCONSECUTIVE_ROW")
                row_index = int(n)
                if "A" not in cells or "B" not in cells:
                    raise SourceError("R100_B1A_AB_TAG_MISSING")
                rows.append(cells)
                if len(rows) > 10000:
                    raise SourceError("R100_B1A_EXCESS_ROWS")
                cells = {}
                node.clear()
    except ET.ParseError as exc:
        raise SourceError("R100_B1A_XML_INVALID") from exc
    if len(rows) < 5 or (len(rows) - 1) % 4:
        raise SourceError("R100_B1A_FOUR_ROW_BLOCK_SHAPE_WRONG")
    return rows


def referenced_shared_strings(z, needed):
    if not needed:
        return {}
    name = "xl/sharedStrings.xml"
    if name not in z.namelist() or z.getinfo(name).file_size > 2 * 1024 * 1024:
        raise SourceError("R100_B1A_SHARED_STRINGS_MISSING")
    raw = z.read(name)
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise SourceError("R100_B1A_SHARED_STRINGS_UNSAFE")
    found, index = {}, -1
    try:
        for event, node in ET.iterparse(io.BytesIO(raw), events=("end",)):
            if node.tag == NS + "si":
                index += 1
                if index in needed:
                    found[index] = sanitized_token("".join(node.itertext()))
                node.clear()
    except ET.ParseError as exc:
        raise SourceError("R100_B1A_SHARED_STRINGS_INVALID") from exc
    if set(found) != set(needed):
        raise SourceError("R100_B1A_SHARED_STRING_INDEX_OUT_OF_RANGE")
    return found


def resolved_value(pair, shared):
    kind, raw = pair
    if not raw:
        return None
    if kind == "s":
        if not raw.isascii() or not raw.isdecimal():
            raise SourceError("R100_B1A_SHARED_STRING_INDEX_INVALID")
        return shared[int(raw)]
    if kind == "n":
        if not re.fullmatch(r"0|[1-9][0-9]{0,15}", raw):
            raise SourceError("R100_B1A_NUMERIC_IDENTIFIER_INVALID")
    return sanitized_token(raw)


def analyze_source(raw):
    identity = verify_bytes(raw)
    if identity["computed_original_SHA256"] != PINNED_SHA256:
        raise SourceError("R100_B1A_ORIGINAL_SHA_MISMATCH")
    workbook_directory_only(raw)
    sheet_data = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        paths = [(int(m.group(1)), n) for n in z.namelist() if (m := SHEET_RE.fullmatch(n))]
        if len(paths) != 10 or len(set(i for i, _ in paths)) != 10:
            raise SourceError("R100_B1A_EXPECT_TEN_SHEETS")
        paths.sort()
        needed = set()
        for _, filename in paths:
            rows = raw_ab_cells(z.read(filename))
            sheet_data.append(rows)
            for row in rows[1:]:
                for col in ("A", "B"):
                    kind, value = row[col]
                    if kind == "s" and value:
                        if not value.isascii() or not value.isdecimal() or int(value) > 50000:
                            raise SourceError("R100_B1A_SHARED_STRING_REFERENCE_INVALID")
                        needed.add(int(value))
        shared = referenced_shared_strings(z, needed)

    sheets = []
    for index, rows in enumerate(sheet_data, 1):
        data = rows[1:]
        formats = {"A": Counter(), "B": Counter()}
        blocks = {"A": Counter(), "B": Counter()}
        # This is the only moment participant/pairing identifiers are held.
        # Raw values remain in local variables, never returned or serialized.
        for col in ("A", "B"):
            resolved = []
            for record in data:
                formats[col][record[col][0]] += 1
                resolved.append(resolved_value(record[col], shared))
            for start in range(0, len(data), 4):
                four = resolved[start:start + 4]
                nonempty = [x for x in four if x is not None]
                blocks[col]["nonempty_"+str(len(nonempty))] += 1
                blocks[col]["distinct_"+str(len(set(nonempty)))] += 1
                if len(nonempty) == 4 and len(set(nonempty)) == 1:
                    blocks[col]["four_identical"] += 1
                if len(nonempty) in (1, 2, 3):
                    blocks[col]["partially_blank"] += 1
        sheets.append({
            "anonymous_sheet_slot": index, "source_xml_row_tags": len(rows),
            "candidate_four_row_blocks": len(data) // 4,
            "A_cell_storage_type_counts": dict(sorted(formats["A"].items())),
            "B_cell_storage_type_counts": dict(sorted(formats["B"].items())),
            "A_four_row_pattern_counts": dict(sorted(blocks["A"].items())),
            "B_four_row_pattern_counts": dict(sorted(blocks["B"].items())),
        })
    return {
        "research_id": "R100", "phase": "B1a",
        "status": "B1A_ORIGINAL_AB_CODE_FORMAT_DIAGNOSTIC_ONLY",
        "original_publisher_MD5": OFFICIAL_MD5,
        "original_full_SHA256": PINNED_SHA256,
        "original_source_bytes": identity["original_bytes"],
        "actual_source_sheet_count": len(sheets),
        "anonymous_sheet_summaries": sheets,
        "original_AB_literals_exported": False,
        "original_worksheet_names_exported": False,
        "C_to_Z_cell_values_dereferenced": 0,
        "source_pair_reciprocity_verified": False,
        "actual_independent_people_count_verified": False,
        "actual_human_model_scores": 0,
        "PESEN_v0_1": "FROZEN",
    }


def original_source():
    validate_url(URL)
    req = urllib.request.Request(URL, headers={"User-Agent": "Psychohistory-R100-B1a-AB-code-only/1.0"})
    with urllib.request.build_opener(ExactOfficialOriginRedirect()).open(req, timeout=55) as response:
        validate_url(response.geturl())
        raw = response.read(MAX_SOURCE + 1)
    return analyze_source(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        result = original_source()
    except (ValueError, OSError, TypeError, KeyError, zipfile.BadZipFile) as exc:
        result = {
            "research_id": "R100", "phase": "B1a",
            "status": "B1A_BLOCKED_FAIL_CLOSED",
            "safe_failure": str(exc) if isinstance(exc, SourceError) else "R100_B1A_SOURCE_UNVERIFIED",
            "actual_human_model_scores": 0, "PESEN_v0_1": "FROZEN",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "B1A_ORIGINAL_AB_CODE_FORMAT_DIAGNOSTIC_ONLY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
