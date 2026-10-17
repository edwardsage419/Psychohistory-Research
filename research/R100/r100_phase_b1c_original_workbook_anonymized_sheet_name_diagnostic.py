#!/usr/bin/env python3
"""R100 B1c actual workbook metadata ONLY: masked name pattern, never cell data."""
from __future__ import annotations
import argparse
import io
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter

from r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only import (
    URL, MAX_SOURCE, OFFICIAL_MD5, ExactOfficialOriginRedirect,
    SourceError, validate_url, verify_bytes, workbook_directory_only,
)
from r100_phase_b0_zenodo_xlsx_ab_tag_structure_only import PINNED_SHA256

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ROLE_RULES = [
    r"(.+)_Type ([12])",
    r"(.+)_Type([12])",
    r"(.+)[ _-]Type[ _-]?([12])",
    r"(.+)[ _-]T([12])",
    r"(.+)[ _-]([12])",
    r"(.+)\(([12])\)",
    r"(.+)[ _-]Player[ _-]?([12])",
    r"(.+)Type([12])",
]


def name_mask(name):
    if not isinstance(name, str) or not (1 <= len(name) <= 64):
        raise SourceError("R100_B1C_SOURCE_NAME_INVALID")
    mask = []
    for c in name:
        if "A" <= c <= "Z":
            mask.append("U")
        elif "a" <= c <= "z":
            mask.append("l")
        elif "0" <= c <= "9":
            mask.append("9")
        elif c == " ":
            mask.append("s")
        elif c == "_":
            mask.append("_")
        elif c == "-":
            mask.append("h")
        else:
            mask.append("p")
    return "".join(mask)


def masked_source_workbook_names(raw):
    identity = verify_bytes(raw)
    if identity["computed_original_SHA256"] != PINNED_SHA256:
        raise SourceError("R100_B1C_PINNED_ORIGINAL_SHA_MISMATCH")
    workbook_directory_only(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        workbook_raw = z.read("xl/workbook.xml")
        relationships_raw = z.read("xl/_rels/workbook.xml.rels")
        if any(len(x) > 256 * 1024 or b"<!DOCTYPE" in x.upper() or b"<!ENTITY" in x.upper() for x in (workbook_raw,relationships_raw)):
            raise SourceError("R100_B1C_XML_METADATA_UNSAFE")
        try:
            wb = ET.fromstring(workbook_raw)
            rel = ET.fromstring(relationships_raw)
        except ET.ParseError as exc:
            raise SourceError("R100_B1C_XML_METADATA_BAD") from exc
        root = wb.find(NS + "sheets")
        if root is None or len(root.findall(NS+"sheet")) != 10:
            raise SourceError("R100_B1C_TEN_WORKBOOK_SHEETS_NOT_FOUND")
        names=[x.attrib.get("name","") for x in root.findall(NS+"sheet")]
        relation_count = sum(x.attrib.get("Type","").endswith("/worksheet") for x in rel)
        if relation_count != 10:
            raise SourceError("R100_B1C_TEN_WORKSHEET_RELATIONS_NOT_FOUND")
    checks = []
    for idx, pattern in enumerate(ROLE_RULES, 1):
        matched = [re.fullmatch(pattern, name, flags=re.IGNORECASE if idx in (3,4,7,8) else 0) for name in names]
        pairs = Counter((x.group(1), x.group(2)) for x in matched if x)
        tr = Counter(x.group(1) for x in matched if x)
        all_matched = all(x is not None for x in matched)
        checks.append({
            "candidate_rule_number":idx,
            "matched_sheets":sum(x is not None for x in matched),
            "all_ten_distinct_treatment_role_pairs":all_matched and len(pairs)==10 and
                len(tr)==5 and all(v==2 for v in tr.values()) and
                all({r for n,r in pairs if n==t}=={"1","2"} for t in tr)
        })
    return {
        "research_id":"R100","phase":"B1c",
        "status":"B1C_ANONYMOUS_ORIGINAL_WORKBOOK_NAME_DIAGNOSTIC_ONLY",
        "original_bytes":identity["original_bytes"],
        "publisher_MD5":OFFICIAL_MD5,
        "original_SHA256":PINNED_SHA256,
        "sheet_count":10,
        "anonymous_name_structure":[{"sheet_slot":i+1,
            "name_length":len(name),"name_character_class_signature":name_mask(name),
            "has_word_type":bool(re.search("type",name,flags=re.I)),
            "ends_with_role_digit":name[-1] if name[-1] in "12" else "NONE"}
            for i,name in enumerate(names)],
        "prespecified_candidate_grammar_checks":checks,
        "raw_sheet_names_exported":False,
        "worksheets_read":False,
        "A_B_or_C_Z_cell_values_read":False,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R100-B1c-workbook-names-masked-only/1.0"})
        with urllib.request.build_opener(ExactOfficialOriginRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            raw=response.read(MAX_SOURCE+1)
        result=masked_source_workbook_names(raw)
    except (OSError,ValueError,TypeError,KeyError,zipfile.BadZipFile) as exc:
        result={"research_id":"R100","phase":"B1c","status":"B1C_BLOCKED_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R100_B1C_UNVERIFIED",
                "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="B1C_ANONYMOUS_ORIGINAL_WORKBOOK_NAME_DIAGNOSTIC_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
