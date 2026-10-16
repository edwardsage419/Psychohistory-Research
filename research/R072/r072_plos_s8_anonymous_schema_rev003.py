#!/usr/bin/env python3
"""R072 REV003: anonymous PLOS S8 structural schema gate after fixed byte SHA.

Uses standard OOXML ZIP+XML read only; emits no workbook, sheet title,
participant row, raw field name, value, member profile, or human model fit.
"""
from __future__ import annotations
import argparse,hashlib,io,json,re
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from r072_plos_s8_signed_redirect_rev002 import retrieve,audit as source_audit

EXACT_SHA="5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b"
PREFIX="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SHEET_RE=re.compile(r"^xl/worksheets/sheet[0-9]+[.]xml$")
CELL_REF=re.compile(r"^[A-Z]{1,3}[1-9][0-9]*$")
TOKEN_WORDS=("treatment","condition","group","request","accept",
             "response","provider","profile","service","serving",
             "neutral","history","reference","reputation","match",
             "time","date","outcome","reciprocity","control")
MAX_SHEETS=20
MAX_ROWS=10000
MAX_COLS=200


def safe_xml(b):
    if b.find(b"<!DOCTYPE")>=0 or b.find(b"<!ENTITY")>=0:
        raise ValueError("UNTRUSTED_XML_DTD")
    try:
        return ET.fromstring(b)
    except ET.ParseError:
        raise ValueError("OOXML_MALFORMED") from None


def shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root=safe_xml(z.read("xl/sharedStrings.xml"))
    result=[]
    for si in root.findall(f"{PREFIX}si"):
        pieces=[x.text or "" for x in si.iter(f"{PREFIX}t")]
        result.append("".join(pieces))
        if len(result)>15000:raise ValueError("SHARED_STRING_BUDGET")
    return result


def row_header_semantics(row,shared):
    hits={k:0 for k in TOKEN_WORDS}
    for cell in row.findall(f"{PREFIX}c"):
        kind=cell.attrib.get("t")
        value=cell.find(f"{PREFIX}v")
        if kind=="s" and value is not None:
            try:
                header=shared[int(value.text)]
            except (ValueError,IndexError,TypeError):
                raise ValueError("SHARED_STRING_INDEX_UNRESOLVED") from None
        elif kind=="inlineStr":
            header="".join((t.text or "") for t in cell.iter(f"{PREFIX}t"))
        elif kind=="str" and value is not None:
            header=value.text or ""
        else:
            header=""
        normalized=header.casefold()
        for key in TOKEN_WORDS:
            if key in normalized:
                hits[key]+=1
    return hits


def anonymous_sheet(z,path,shared):
    root=safe_xml(z.read(path))
    row_container=root.find(f"{PREFIX}sheetData")
    if row_container is None:raise ValueError("WORKSHEET_SHEETDATA_MISSING")
    rows=row_container.findall(f"{PREFIX}row")
    if len(rows)>MAX_ROWS:raise ValueError("SHEET_ROW_LIMIT")
    max_col_seen=0
    occupied_cells=0
    numeric_cells=0
    text_style_cells=0
    formulas=0
    firstrow=rows[0] if rows and rows[0].attrib.get("r")=="1" else None
    for row in rows:
        cells=row.findall(f"{PREFIX}c")
        if len(cells)>MAX_COLS:raise ValueError("SHEET_COLUMN_LIMIT")
        for cell in cells:
            ref=cell.attrib.get("r","")
            if not CELL_REF.fullmatch(ref):
                raise ValueError("INVALID_EXCEL_CELL_REF")
            col=0
            for char in ref:
                if char.isdigit():break
                col=col*26+(ord(char)-64)
            if col>MAX_COLS:raise ValueError("SHEET_COLUMN_LIMIT")
            max_col_seen=max(max_col_seen,col)
            v=cell.find(f"{PREFIX}v")
            istring=cell.find(f"{PREFIX}is")
            if v is not None or istring is not None:
                occupied_cells+=1
                if cell.attrib.get("t","n") in ("n",""):
                    numeric_cells+=1
                else:
                    text_style_cells+=1
            if cell.find(f"{PREFIX}f") is not None:
                formulas+=1
    if formulas:
        # Do not infer missing/cached formula evaluations for human data.
        raise ValueError("UNEXECUTED_FORMULAS_IN_HUMAN_SPREADSHEET")
    header=row_header_semantics(firstrow,shared) if firstrow is not None else {k:0 for k in TOKEN_WORDS}
    return {
        "sheet_anonymous_index":None,
        "physical_row_tags":len(rows),
        "max_column_index_seen":max_col_seen,
        "nonempty_cell_total":occupied_cells,
        "cells_stored_as_numeric":numeric_cells,
        "cells_stored_as_text":text_style_cells,
        "first_row_may_contain_schema_headers":firstrow is not None,
        "whitelisted_semantic_header_matches":header,
        "header_mapping_status":"CANDIDATE_NAME_ONLY_NOT_AUTHOR_DATA_DICTIONARY"
            if any(header.values()) else "MAPPING_NOT_ESTABLISHED",
    }


def scan_workbook(raw):
    if hashlib.sha256(raw).hexdigest()!=EXACT_SHA:
        raise ValueError("SOURCE_SHA_DIFFERENT_FROM_PRIOR_VALIDATED_BYTES")
    # REV002 source_audit performs ZIP CRC, max member, macro, compression checks.
    source_audit(raw,"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
    with ZipFile(io.BytesIO(raw)) as z:
        found=sorted(x for x in z.namelist() if SHEET_RE.fullmatch(x))
        if not 1<=len(found)<=MAX_SHEETS:
            raise ValueError("SHEET_COUNT_OUTSIDE_LIMIT")
        shared=shared_strings(z)
        summaries=[]
        for i,name in enumerate(found,1):
            record=anonymous_sheet(z,name,shared)
            record["sheet_anonymous_index"]=i
            summaries.append(record)
    return {
        "research_id":"R072",
        "stage":"E2_PLOS_S8_ANONYMOUS_WORKBOOK_STRUCTURE_REV003",
        "status":"E2_VERIFIED_REAL_SOURCE_ANONYMOUS_SCHEMA_ONLY",
        "protocol":"protocols/R072_E2_S8_ANONYMOUS_SCHEMA_DIAGNOSTIC_2026-10-16.md",
        "source_DOI":"10.1371/journal.pone.0152076.s008",
        "pinned_source_SHA256":EXACT_SHA,
        "total_anonymous_worksheets":len(summaries),
        "anonymous_sheet_metadata":summaries,
        "raw_header_values_exported":False,
        "raw_sheet_names_exported":False,
        "real_participant_values_exported":False,
        "person_level_analysis_performed":False,
        "verified_actual_group_or_sample_size":False,
        "human_R072_exact_model_E2":"BLOCKED_RULE_EXPOSURE_AND_DATA_DICTIONARY",
        "causal_reputation_model_fitted":False,
        "independent_E3":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        raw,mode=retrieve()
        if mode!="PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT":
            # Could be publisher-direct in future; still checksum original.
            if mode!="PLOS_DIRECT_PUBLISHER":
                raise ValueError("UNKNOWN_VERIFIED_PUBLISHER_MODE")
        result=scan_workbook(raw)
    except (ValueError,OSError) as ex:
        result={
            "research_id":"R072","stage":"E2_PLOS_S8_ANONYMOUS_WORKBOOK_STRUCTURE_REV003",
            "status":"SCHEMA_UNRESOLVED",
            "bounded_code":str(ex)[:100] if isinstance(ex,ValueError) else "SOURCE_TRANSPORT_FAILURE",
            "raw_human_data_exported":False,"pesen_v01":"FROZEN"}
    pth=p.parse_args()
    pth.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"sheet_count":result.get("total_anonymous_worksheets"),
                      "sheets":result.get("anonymous_sheet_metadata"),
                      "error":result.get("bounded_code")},sort_keys=True))
    if result["status"]!="E2_VERIFIED_REAL_SOURCE_ANONYMOUS_SCHEMA_ONLY":
        raise RuntimeError("R072 precise anonymous schema diagnostic failed")


if __name__=="__main__":main()
