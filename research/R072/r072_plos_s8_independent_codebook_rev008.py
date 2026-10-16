#!/usr/bin/env python3
"""R072 REV008: look ONLY for outcome-independent author profile codebook.

No real group codes, names, individual rows, or note text in report.
"""
from __future__ import annotations
import argparse,hashlib,io,json,re
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
from decimal import Decimal
from r072_plos_s8_signed_redirect_rev002 import retrieve,audit as source_audit
from r072_plos_s8_anonymous_schema_rev003 import EXACT_SHA,PREFIX,SHEET_RE,safe_xml,shared_strings
from r072_plos_s8_column_domains_rev004 import decode_cell,cell_column

SERVICE=re.compile(r"\b(?:serving|service[\s_-]+(?:history|profile))\b",re.I)
NEUTRAL=re.compile(r"\bneutral\b",re.I)
A_BIND=re.compile(r"(?<!\d)(\d{1,2})\s*(?:=|:|->|-)\s*([^\n;]{1,80})",re.I)
RANGE_HINT=re.compile(r"\d+\s*(?:-|to|through)\s*\d+",re.I)
MAX_NOTE_ROWS=20


def characterize_codebook(group_codes, notes):
    """Inputs solely synthetic group labels/notes. No outcome data."""
    if len(group_codes)!=8 or len(set(group_codes))!=8:
        raise ValueError("EIGHT_GROUP_CODES_REQUIRED")
    allowed=set(group_codes)
    proposals=defaultdict(set)
    conflict=False
    ranged=False
    # Only note lines. Either isolated numeric cell and clear label in
    # another cell, or a code-label pair with punctuation in one cell.
    for cells in notes:
        strings=[v for v,kind in cells.values() if kind=="text" and isinstance(v,str)]
        nums=[v for v,kind in cells.values() if kind=="numeric"]
        for s in strings:
            ranged=ranged or bool(RANGE_HINT.search(s))
            text=s.casefold()
            srv=bool(SERVICE.search(text))
            neu=bool(NEUTRAL.search(text))
            if srv and neu:
                conflict=True
                continue
            if not (srv or neu):
                continue
            cat="SERVICE" if srv else "NEUTRAL"
            for m in A_BIND.finditer(s):
                n=Decimal(int(m.group(1)))
                label=m.group(2)
                if n in allowed and ((cat=="SERVICE" and SERVICE.search(label)) or
                                     (cat=="NEUTRAL" and NEUTRAL.search(label))):
                    proposals[n].add(cat)
            # B format: a single source-level numeric code in its own cell
            # and exactly one nonambiguous concept across text-only cells.
        merged=" ".join(strings).casefold()
        srv=bool(SERVICE.search(merged));neu=bool(NEUTRAL.search(merged))
        if len(nums)==1 and nums[0] in allowed and srv != neu:
            proposals[nums[0]].add("SERVICE" if srv else "NEUTRAL")
        elif len(nums)>1 and (srv or neu):
            conflict=True
    if any(len(v)>1 for v in proposals.values()):
        conflict=True
    complete=(not conflict and len(proposals)==8 and
              sum(v=={"SERVICE"} for v in proposals.values())==4 and
              sum(v=={"NEUTRAL"} for v in proposals.values())==4)
    return {
        "candidate_full_eight_codebook_exists":bool(complete),
        "candidate_unique_serving_neutral_four_each":bool(complete),
        "candidate_conflict_found":bool(conflict),
        "range_syntax_hint_present_not_adopted":bool(ranged),
        "all_proposed_code_values_belong_to_anonymous_original_eight":True,
        "status":"FULL_AUTHOR_CODEBOOK_CANDIDATE_REQUIRES_NEXT_STAGE_CONFIRMATION"
           if complete else "BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK",
        "raw_group_codes_notes_and_individual_responses_disclosed":False,
        "human_serving_effect_calculated":False,
    }


def original_data_gate(raw):
    if hashlib.sha256(raw).hexdigest()!=EXACT_SHA:
        raise ValueError("PINNED_SOURCE_SHA_MISMATCH")
    source_audit(raw,"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
    with ZipFile(io.BytesIO(raw)) as z:
        sheets=[name for name in z.namelist() if SHEET_RE.fullmatch(name)]
        if len(sheets)!=1:raise ValueError("EXPECTED_ONE_ORIGINAL_SHEET")
        strings=shared_strings(z)
        root=safe_xml(z.read(sheets[0]))
        tab=root.find(f"{PREFIX}sheetData")
        if tab is None:raise ValueError("NO_SHEETDATA")
        groupcodes=set()
        notes=[]
        eligible_rows=0
        for row in tab.findall(f"{PREFIX}row"):
            try:rid=int(row.attrib["r"])
            except (KeyError,ValueError):raise ValueError("INVALID_ROW") from None
            if rid==1:continue
            cells={}
            for elem in row.findall(f"{PREFIX}c"):
                idx=cell_column(elem.attrib.get("r",""))
                if idx in cells:raise ValueError("DUPLICATE_CELL")
                cells[idx]=decode_cell(elem,strings)
            first=cells.get(1,(None,"empty"))
            second=cells.get(2,(None,"empty"))
            if first[1]=="numeric" and second[1]=="numeric":
                groupcodes.add(first[0])
                eligible_rows+=1
            else:
                notes.append(cells)
    if eligible_rows!=189 or len(notes)!=9:
        raise ValueError("FROZEN_S8_ROW_UNIVERSE_CHANGED")
    if len(notes)>MAX_NOTE_ROWS:
        raise ValueError("TOO_MANY_NOTES")
    a=characterize_codebook(groupcodes,notes)
    return {
        "research_id":"R072",
        "stage":"E2_POSTEXPLORATORY_AUTHOR_INDEPENDENT_LEGEND_CODEBOOK_REV008",
        "protocol":"protocols/R072_E2_S8_REV008_INDEPENDENT_LEGEND_CODEBOOK_BINDING_2026-10-17.md",
        "source_sha256":EXACT_SHA,
        "candidate_numeric_rows":eligible_rows,
        "other_noncandidate_note_rows":len(notes),
        **a,
        "published_table1_response_counts_used_to_assign_treatment":False,
        "author_profile_codebook_fully_verified_for_causal_replication":False,
        "IMAGE_STANDING_STERN_HUMAN_MECHANISM":"NOT_ESTABLISHED",
        "E3":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    try:
        raw,mode=retrieve()
        if mode not in ("PLOS_DIRECT_PUBLISHER","PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT"):
            raise ValueError("SOURCE_CHAIN_NOT_ACCEPTED")
        result=original_data_gate(raw)
    except (ValueError,OSError) as exc:
        result={"research_id":"R072","status":"SOURCE_OR_CODEBOOK_GATE_UNRESOLVED",
                "safe_error":str(exc)[:70] if isinstance(exc,ValueError) else "NETWORK_UNAVAILABLE",
                "raw_human_data_disclosed":False,"pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]=="SOURCE_OR_CODEBOOK_GATE_UNRESOLVED":
        raise RuntimeError("Unable to verify original source for independent codebook gate")


if __name__=="__main__":
    main()
