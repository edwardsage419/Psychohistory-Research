#!/usr/bin/env python3
"""R100 Phase B0: pinned source XLSX A/B cell TAGS only, no cell value access.

The XML parser transiently materializes values internally, yet this program
never accesses any element's text and never exports identifying values.
"""
from __future__ import annotations
import argparse
import io
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

from r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only import (
    URL, MAX_SOURCE, OFFICIAL_MD5, ExactOfficialOriginRedirect,
    validate_url, verify_bytes, workbook_directory_only, SourceError,
)

PINNED_SHA256 = "825b1cd3226aeca7a19d76d9594f655114b12059648f9ca03b3291c3cf9ab200"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SHEET_PATH = re.compile(r"xl/worksheets/sheet([1-9][0-9]*)\.xml")
IDENTITY_REF = re.compile(r"([AB])([1-9][0-9]*)")


def structure_of_worksheet(handle):
    rows = cells_a = cells_b = rows_ab = 0
    previous_row = 0
    in_row = False
    cols = set()
    try:
        for event, elem in ET.iterparse(handle, events=("start", "end")):
            if event == "start":
                if elem.tag == NS + "row":
                    if in_row:
                        raise SourceError("R100_B0_NESTED_ROW")
                    number = elem.attrib.get("r", "")
                    if not number.isascii() or not number.isdecimal():
                        raise SourceError("R100_B0_ROW_NUMBER_ABSENT")
                    index = int(number)
                    if index <= previous_row or index > 100000:
                        raise SourceError("R100_B0_ROW_NUMBER_INVALID")
                    previous_row = index
                    rows += 1
                    if rows > 10000:
                        raise SourceError("R100_B0_TOO_MANY_ROWS")
                    in_row = True
                    cols = set()
                elif elem.tag == NS + "c" and in_row:
                    match = IDENTITY_REF.fullmatch(elem.attrib.get("r", ""))
                    if match:
                        if int(match.group(2)) != previous_row or match.group(1) in cols:
                            raise SourceError("R100_B0_DUPLICATE_OR_WRONG_AB_TAG")
                        cols.add(match.group(1))
                        if match.group(1) == "A":
                            cells_a += 1
                        else:
                            cells_b += 1
            else:
                if elem.tag == NS + "row":
                    if not in_row:
                        raise SourceError("R100_B0_ROW_STRUCTURE_INVALID")
                    if cols == {"A", "B"}:
                        rows_ab += 1
                    in_row = False
                # Never examine elem.text for any cell; discard every XML element.
                elem.clear()
    except (ET.ParseError, UnicodeError, OverflowError, MemoryError) as exc:
        raise SourceError("R100_B0_WORKSHEET_XML_REJECTED") from exc
    if in_row or rows == 0 or not cells_a or not cells_b:
        raise SourceError("R100_B0_A_B_TAGS_NOT_ESTABLISHED")
    return {
        "row_tag_count": rows,
        "column_A_cell_tag_count": cells_a,
        "column_B_cell_tag_count": cells_b,
        "rows_with_both_A_and_B_cell_tags": rows_ab,
    }


def source_structure_only(raw):
    identity = verify_bytes(raw)
    if identity["computed_original_SHA256"] != PINNED_SHA256:
        raise SourceError("R100_B0_PINNED_SHA256_MISMATCH")
    workbook_directory_only(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        found = []
        for name in z.namelist():
            match = SHEET_PATH.fullmatch(name)
            if match:
                found.append((int(match.group(1)), name))
        if len(found) != 10:
            raise SourceError("R100_B0_EXPECTED_EXACTLY_TEN_WORKSHEET_FILES")
        found.sort()
        summaries = []
        for slot, (_, name) in enumerate(found, 1):
            if z.getinfo(name).file_size > 8 * 1024 * 1024:
                raise SourceError("R100_B0_WORKSHEET_TOO_LARGE")
            with z.open(name) as stream:
                counts = structure_of_worksheet(stream)
            summaries.append({"anonymous_sheet_slot": slot, **counts})
    return {
        "research_id": "R100", "phase": "B0",
        "status": "B0_REAL_XLSX_WORKSHEET_A_B_TAG_STRUCTURE_VERIFIED_ONLY",
        "official_source_bytes": identity["original_bytes"],
        "official_source_MD5": OFFICIAL_MD5,
        "official_source_SHA256": PINNED_SHA256,
        "anonymous_sheets": summaries,
        "worksheet_cell_value_dereferences": 0,
        "actor_identifiers_or_pair_values_republished": False,
        "original_contributions_or_survey_values_republished": False,
        "original_human_model_scores": 0,
        "PESEN_v0_1": "FROZEN",
    }


def original_source():
    validate_url(URL)
    req = urllib.request.Request(
        URL, headers={"User-Agent": "Psychohistory-R100-B0-XLSX-AB-Tag-Only/1.0"}
    )
    opener = urllib.request.build_opener(ExactOfficialOriginRedirect())
    with opener.open(req, timeout=55) as response:
        validate_url(response.geturl())
        raw = response.read(MAX_SOURCE + 1)
    return source_structure_only(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    opts = parser.parse_args()
    try:
        result = original_source()
    except (OSError, ValueError, TypeError, zipfile.BadZipFile, KeyError) as exc:
        result = {
            "research_id": "R100", "phase": "B0",
            "status": "B0_BLOCKED_FAIL_CLOSED",
            "safe_failure": str(exc) if isinstance(exc, SourceError) else "R100_B0_SOURCE_UNVERIFIED",
            "original_human_model_scores": 0, "PESEN_v0_1": "FROZEN",
        }
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "B0_REAL_XLSX_WORKSHEET_A_B_TAG_STRUCTURE_VERIFIED_ONLY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
