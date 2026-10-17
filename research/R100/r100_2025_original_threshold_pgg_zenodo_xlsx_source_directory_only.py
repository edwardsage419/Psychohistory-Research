#!/usr/bin/env python3
"""R100 Phase A: official Zenodo MD5 and XLSX workbook directory ONLY. No actions."""
import argparse
import hashlib
import io
import json
import pathlib
import urllib.parse
import urllib.request
import zipfile
from xml.etree import ElementTree

RECORD = "16918146"
NAME = "ThresholdPGG_ExperimentalData.xlsx"
URL = f"https://zenodo.org/records/{RECORD}/files/{NAME}?download=1"
OFFICIAL_MD5 = "c40171abb172da8e16b0839db98a2cf2"
MAX_SOURCE = 2 * 1024 * 1024
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


class SourceError(ValueError):
    pass


def validate_url(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or p.netloc != "zenodo.org" or p.path != f"/records/{RECORD}/files/{NAME}" or p.query not in ("", "download=1") or p.fragment:
        raise SourceError("R100_NON_OFFICIAL_URL_REJECTED")


def verify_bytes(raw, expected_md5=OFFICIAL_MD5):
    if type(raw) is not bytes or not (0 < len(raw) <= MAX_SOURCE):
        raise SourceError("R100_ORIGINAL_SOURCE_SIZE_INVALID")
    if hashlib.md5(raw).hexdigest() != expected_md5:
        raise SourceError("R100_ORIGINAL_PUBLISHER_MD5_MISMATCH")
    return {"original_bytes": len(raw), "publisher_MD5": OFFICIAL_MD5, "computed_original_SHA256": hashlib.sha256(raw).hexdigest(), "publisher_MD5_verified": True}


def workbook_directory_only(raw):
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            files = z.infolist()
            if not 2 <= len(files) <= 300:
                raise SourceError("R100_XLSX_ENTRY_COUNT_INVALID")
            seen, total = set(), 0
            for f in files:
                n = f.filename
                if n in seen or not n or n.startswith("/") or "\\" in n or ".." in n.split("/") or any(x in ("", ".") for x in n.split("/")[:-1]):
                    raise SourceError("R100_XLSX_UNSAFE_ARCHIVE_PATH")
                seen.add(n)
                if (f.external_attr >> 16) & 0o170000 == 0o120000:
                    raise SourceError("R100_XLSX_SYMLINK")
                if f.file_size > 8 * 1024 * 1024 or f.compress_size > MAX_SOURCE or (f.file_size and (not f.compress_size or f.file_size > f.compress_size * 1000)):
                    raise SourceError("R100_XLSX_UNSAFE_ENTRY_SIZE")
                total += f.file_size
            if total > 16 * 1024 * 1024:
                raise SourceError("R100_XLSX_UNSAFE_EXPANDED_TOTAL")
            # DO NOT read worksheets, sharedStrings, relationships, IDs, pairings or survey.
            metadata_paths = ("[Content_Types].xml", "xl/workbook.xml")
            xml = []
            for n in metadata_paths:
                if n not in seen or z.getinfo(n).file_size > 256 * 1024:
                    raise SourceError("R100_XLSX_WORKBOOK_METADATA_MISSING")
                xml.append(z.read(n))
            for b in xml:
                if b"<!DOCTYPE" in b.upper() or b"<!ENTITY" in b.upper():
                    raise SourceError("R100_XLSX_FORBIDDEN_XML")
            w = ElementTree.fromstring(xml[1])
            if w.tag != f"{{{MAIN_NS}}}workbook":
                raise SourceError("R100_XLSX_WORKBOOK_NAMESPACE_UNKNOWN")
            node = w.find(f"{{{MAIN_NS}}}sheets")
            if node is None:
                raise SourceError("R100_XLSX_SHEETS_ABSENT")
            sheets = node.findall(f"{{{MAIN_NS}}}sheet")
            if len(sheets) != 10:
                raise SourceError("R100_PUBLISHER_TEN_SHEETS_EXPECTATION_FAILED")
            names = [x.attrib.get("name", "") for x in sheets]
            if len(set(names)) != 10 or any(not x or len(x) > 64 for x in names):
                raise SourceError("R100_XLSX_SHEET_NAMES_UNSAFE")
            return {"original_workbook_sheet_count": 10, "worksheet_xml_read": False, "shared_string_xml_read": False, "actor_pair_contributions_or_survey_values_read": False, "original_sheet_names_republished": False}
    except (zipfile.BadZipFile, OSError, ElementTree.ParseError, RuntimeError) as e:
        raise SourceError("R100_ORIGINAL_XLSX_DIRECTORY_UNREADABLE") from e


def actual_original_publisher_source():
    validate_url(URL)
    req = urllib.request.Request(URL, headers={"User-Agent": "Psychohistory-R100-2025-First-Party-Workbook-Metadata-Only/1.0"})
    with urllib.request.urlopen(req, timeout=55) as res:
        validate_url(res.geturl())
        raw = res.read(MAX_SOURCE + 1)
    identity = verify_bytes(raw)
    try:
        directory = workbook_directory_only(raw)
    except SourceError as e:
        return {"research_id": "R100", "phase": "A", "status": "E1_SOURCE_AUTHENTICATED_SCHEMA_BLOCKED", "source_identity": identity, "safe_failure": str(e), "actual_human_model_scores": 0, "PESEN_v0_1": "FROZEN"}
    return {"research_id": "R100", "phase": "A", "status": "E1_SOURCE_AUTHENTICATED_WORKBOOK_DIRECTORY_ONLY", "publisher_DOI": "10.5281/zenodo.16918146", "source_filename": NAME, "source_identity": identity, "nonbehavior_workbook_directory": directory, "publisher_reported_treatment_participant_counts_not_verified": [110, 118, 112, 104, 110], "same_humans_in_sequential_sessions": True, "actual_human_model_scores": 0, "PESEN_v0_1": "FROZEN"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=pathlib.Path, required=True)
    args = p.parse_args()
    try:
        result = actual_original_publisher_source()
    except (OSError, ValueError, TypeError) as e:
        result = {"research_id": "R100", "phase": "A", "status": "E0_SOURCE_BLOCKED", "safe_failure": str(e) if isinstance(e, SourceError) else "R100_PUBLISHER_SOURCE_UNVERIFIED", "actual_human_model_scores": 0, "PESEN_v0_1": "FROZEN"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "E1_SOURCE_AUTHENTICATED_WORKBOOK_DIRECTORY_ONLY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
