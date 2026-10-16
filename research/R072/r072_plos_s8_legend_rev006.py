#!/usr/bin/env python3
"""R072 REV006 post-exploratory author workbook noncandidate footer legend check.

Only boolean public-keyword indicators across note rows. No strings, user IDs,
profile codes, individual row data, or original workbook leaves CI memory.
"""
from __future__ import annotations
from collections import Counter
import argparse,hashlib,io,json,re
from pathlib import Path
from zipfile import ZipFile
from r072_plos_s8_signed_redirect_rev002 import retrieve,audit as original_audit
from r072_plos_s8_anonymous_schema_rev003 import EXACT_SHA,PREFIX,SHEET_RE,safe_xml,shared_strings
from r072_plos_s8_column_domains_rev004 import decode_cell,cell_column

TOKENS=("serving","service","neutral","history","provider","response",
        "replied","reply","yes","maybe","no","male","female","dutch",
        "israel","profile","code","variable","reference","request")
PATTERNS={k:re.compile(r"(?<![a-z])"+re.escape(k)+r"(?![a-z])",re.I) for k in TOKENS}
LEGEND=re.compile(r"(?<![a-z0-9])[0-9]{1,2}\s*[:=]\s*[a-z]",re.I)


def read_note_profile(raw):
    if hashlib.sha256(raw).hexdigest()!=EXACT_SHA:
        raise ValueError("SOURCE_SHA_NOT_PINNED")
    original_audit(raw,"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
    with ZipFile(io.BytesIO(raw)) as z:
        names=[n for n in z.namelist() if SHEET_RE.fullmatch(n)]
        if len(names)!=1:raise ValueError("UNEXPECTED_NUMBER_OF_WORKSHEETS")
        strings=shared_strings(z)
        root=safe_xml(z.read(names[0]))
        sheet=root.find(f"{PREFIX}sheetData")
        if sheet is None:raise ValueError("MISSING_SHEET_DATA")
        rows={}
        for row in sheet.findall(f"{PREFIX}row"):
            try:rid=int(row.attrib["r"])
            except (KeyError,ValueError):raise ValueError("INVALID_ROW_INDEX") from None
            if rid in rows or rid<1:raise ValueError("REPEATED_OR_BAD_ROW_NUMBER")
            observed={}
            for cell in row.findall(f"{PREFIX}c"):
                k=cell_column(cell.attrib.get("r",""))
                if k in observed:raise ValueError("DUPLICATE_COL_IN_ROW")
                observed[k]=decode_cell(cell,strings)
            rows[rid]=observed
    if 1 not in rows:raise ValueError("NO_HEADER")
    notes=[]
    case_positions=[]
    for rid in sorted(k for k in rows if k!=1):
        cells=rows[rid]
        if (cells.get(1,(None,"empty"))[1]=="numeric" and
            cells.get(2,(None,"empty"))[1]=="numeric"):
            case_positions.append(rid)
        else:
            notes.append((rid,cells))
    if not case_positions:raise ValueError("NO_NUMERIC_CASE_BLOCK")
    summary={k:False for k in TOKENS}
    candidate_syntax=False
    before=after=inside=0
    for rid,cells in notes:
        if rid<min(case_positions):before+=1
        elif rid>max(case_positions):after+=1
        else:inside+=1
        text_parts=[value for value,kind in cells.values() if kind=="text"]
        # Read in memory for keyword presence, NEVER include values in report.
        content=" ".join(text_parts)
        for k,regex in PATTERNS.items():
            summary[k]=summary[k] or bool(regex.search(content))
        if (LEGEND.search(content)
            and any(PATTERNS[k].search(content) for k in ("serving","service","history"))
            and PATTERNS["neutral"].search(content)):
            candidate_syntax=True
    return {
        "study":"R072","stage":"E2_S8_EXPLORATORY_NONCASE_LEGEND_CHECK_REV006",
        "status":"R072_REV006_REAL_NONCASE_LEGEND_KEYWORDS_CHECKED",
        "protocol":"protocols/R072_E2_S8_REV006_INTERNAL_CODEBOOK_LEGEND_DETECTION_2026-10-16.md",
        "source_SHA256":EXACT_SHA,
        "candidate_rows_by_first_two_numeric":len(case_positions),
        "other_noncase_format_rows":len(notes),
        "noncase_rows_before_numeric_block":before,
        "noncase_rows_after_numeric_block":after,
        "noncase_rows_inside_numeric_block":inside,
        "public_keyword_presence_across_all_noncase_lines_only":summary,
        "strict_numeric_label_assignment_syntax_with_both_serving_and_neutral":candidate_syntax,
        "author_codebook_status":"LEGEND_SYNTAX_CANDIDATE_UNVERIFIED"
            if candidate_syntax else "AUTHOR_CODEBOOK_STILL_NOT_RECOVERED",
        "author_treatment_encoding_verified":False,
        "real_response_analysis_performed":False,
        "individual_text_or_codes_exported":False,
        "human_reputation_norm_mechanism":"NOT_ESTABLISHED",
        "independent_E3":"OPEN","PESEN_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        blob,mode=retrieve()
        if mode not in ("PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT","PLOS_DIRECT_PUBLISHER"):
            raise ValueError("INVALID_SOURCE_MODE")
        result=read_note_profile(blob)
    except (ValueError,OSError) as exc:
        result={"study":"R072","status":"FOOTER_CODEBOOK_UNRESOLVED",
                "error_code":str(exc)[:100] if isinstance(exc,ValueError) else "NETWORK_OR_IO",
                "no_personal_data_exported":True,"PESEN_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R072_REV006_REAL_NONCASE_LEGEND_KEYWORDS_CHECKED":
        raise RuntimeError("Source-locked R072 footer legend audit failed")


if __name__=="__main__":main()
