#!/usr/bin/env python3
"""R072 REV004: publisher SHA-locked human XLSX anonymous column domains only.

Input includes human records but NONE are printed, archived, or emitted.
This is a structural eligibility check, NOT a reconstruction of 189 requests,
and NOT a result about indirect reciprocity in people.
"""
from __future__ import annotations
from collections import Counter
from decimal import Decimal,InvalidOperation
import argparse,hashlib,io,json
from pathlib import Path
from zipfile import ZipFile
from r072_plos_s8_signed_redirect_rev002 import retrieve,audit as audit_original
from r072_plos_s8_anonymous_schema_rev003 import (
  EXACT_SHA, safe_xml, shared_strings, SHEET_RE, MAX_COLS, MAX_ROWS, PREFIX,
  CELL_REF, TOKEN_WORDS, row_header_semantics
)

EXPECTED_PUBLISHED_REQUESTS=189
EXPECTED_PUBLISHED_TREATMENT_COUNTS=(96,93)


def decode_cell(cell,shared):
    if cell.find(f"{PREFIX}f") is not None:
        raise ValueError("FORMULAS_IN_ORIGINAL_NOT_EVALUATED")
    typ=cell.attrib.get("t","n")
    val=cell.find(f"{PREFIX}v")
    inline=cell.find(f"{PREFIX}is")
    if typ=="s":
        if val is None or val.text is None:
            return None,"empty"
        try:
            k=int(val.text)
            if k<0 or k>=len(shared):raise ValueError()
            content=shared[k]
        except (ValueError,TypeError,IndexError):
            raise ValueError("INVALID_SHARED_STRING_INDEX") from None
        return (content,"text") if content.strip() else (None,"empty")
    if typ=="inlineStr":
        content="".join(x.text or "" for x in inline.iter(f"{PREFIX}t")) if inline is not None else ""
        return (content,"text") if content.strip() else (None,"empty")
    if typ in ("str","e","b"):
        content=val.text if val is not None else ""
        return (content,"text") if content and content.strip() else (None,"empty")
    if typ!="n":
        raise ValueError("UNKNOWN_SAFE_CELL_TYPE")
    if val is None or val.text is None or not val.text.strip():
        return None,"empty"
    try:
        numeric=Decimal(val.text)
        if not numeric.is_finite():raise ValueError()
    except (InvalidOperation,ValueError):
        raise ValueError("UNSAFE_NUMERIC_CELL") from None
    return numeric,"numeric"


def cell_column(ref):
    if not CELL_REF.fullmatch(ref):
        raise ValueError("INVALID_CELL_COORDINATE")
    index=0
    for x in ref:
        if x.isdigit():break
        index=index*26+ord(x)-64
    if not 1<=index<=MAX_COLS:raise ValueError("CELL_COLUMN_OUT_OF_BOUND")
    return index


def column_report(cells,expected_total):
    observed=[v for v,t in cells if t!="empty"]
    count=Counter(t for v,t in cells)
    nonempty=len(observed)
    numeric=[v for v,t in cells if t=="numeric"]
    domains={}
    for permitted in ((0,1),(1,2),(0,1,2)):
        domains["all_nonempty_numeric_in_"+str(permitted)]=bool(observed) and (
            len(numeric)==len(observed) and all(v in permitted for v in numeric))
    counts01=None
    if nonempty==expected_total and domains["all_nonempty_numeric_in_(0, 1)"] and len(set(numeric))==2:
        tally=Counter(numeric)
        counts01={"zero":tally[Decimal(0)],"one":tally[Decimal(1)]}
    return {
      "observed_nonempty":nonempty,
      "missing_or_empty":expected_total-nonempty,
      "numeric_cell_count":count["numeric"],
      "text_cell_count":count["text"],
      "distinct_nonempty_value_count":len(set(observed)),
      "fixed_small_integer_numeric_domains":domains,
      "complete_binary_01_histogram_only_if_all_rows_and_both_codes_present":counts01,
    }


def scan_rows(raw):
    if hashlib.sha256(raw).hexdigest()!=EXACT_SHA:
        raise ValueError("SOURCE_SHA_DIFFERS_FROM_VALIDATED_S8")
    audit_original(raw,"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
    with ZipFile(io.BytesIO(raw)) as z:
        files=[name for name in z.namelist() if SHEET_RE.fullmatch(name)]
        if len(files)!=1:raise ValueError("EXPECTED_ONE_PUBLISHED_S8_SHEET_ONLY")
        strings=shared_strings(z)
        root=safe_xml(z.read(files[0]))
        container=root.find(f"{PREFIX}sheetData")
        if container is None:raise ValueError("MISSING_SHEETDATA")
        rows=container.findall(f"{PREFIX}row")
        if len(rows)>MAX_ROWS:raise ValueError("SHEET_EXCEEDS_ROW_LIMIT")
        data={}
        header=None
        for row in rows:
            try:rid=int(row.attrib["r"])
            except (KeyError,ValueError):raise ValueError("INVALID_ROW_INDEX") from None
            if rid<1 or rid in data or (header is not None and rid==1):
                raise ValueError("DUPLICATE_OR_INVALID_ROW_INDEX")
            cells={}
            for cell in row.findall(f"{PREFIX}c"):
                col=cell_column(cell.attrib.get("r",""))
                if col in cells:raise ValueError("DUPLICATE_COLUMN_PER_ROW")
                cells[col]=decode_cell(cell,strings)
            if rid==1:
                if header is not None:raise ValueError("DUPLICATE_FIRST_ROW")
                header=row_header_semantics(row,strings)
            else:
                data[rid]=cells
    if header is None:raise ValueError("MISSING_FIRST_ROW_HEADERS")
    if max((max(row.keys(),default=0) for row in data.values()),default=0)>10:
        raise ValueError("SOURCE_EXPECTED_MAX_TEN_COLUMNS")
    physical=len(data)
    rows_with_any=sum(any(kind!="empty" for v,kind in row.values()) for row in data.values())
    all_complete=sum(all(j in row and row[j][1]!="empty" for j in range(1,11))
                     for row in data.values())
    buckets=Counter(sum(kind!="empty" for v,kind in row.values()) for row in data.values())
    # Safe aggregated row completeness histogram; small unique bins redacted.
    row_hist={str(k):(n if n>=5 else "SUPPRESSED_LT5") for k,n in sorted(buckets.items())}
    cols=[]
    for ix in range(1,11):
        colcells=[record.get(ix,(None,"empty")) for record in data.values()]
        detail=column_report(colcells,physical)
        detail["anonymous_col_1_based"]=ix
        cols.append(detail)
    return {
      "study":"R072","stage":"E2_PLOS_S8_AUTHOR_UNIVERSE_AND_COLUMN_DOMAINS_REV004",
      "status":"R072_E2_REAL_COLUMN_DOMAINS_CHECKED",
      "source_DOI":"10.1371/journal.pone.0152076.s008",
      "source_SHA256":EXACT_SHA,
      "row_unit":"OOXML nonheader physical row, not verified author analytical sample",
      "physical_nonheader_rows":physical,
      "nonheader_rows_with_any_nonempty":rows_with_any,
      "nonheader_rows_complete_in_all_ten_columns":all_complete,
      "anonymous_nonempty_cell_row_histogram_suppressed_small":row_hist,
      "number_of_anonymized_columns":10,
      "anonymous_column_domains":cols,
      "published_table3_expected_n":EXPECTED_PUBLISHED_REQUESTS,
      "published_table3_expected_serving_neutral":list(EXPECTED_PUBLISHED_TREATMENT_COUNTS),
      "author_valid_189_row_inclusion_rule":"NOT_RECOVERED",
      "observed_row_universe_vs_published_n":
          "COUNT_MATCH_ONLY_NOT_VALIDATED_AUTHOR_INCLUSION" if rows_with_any==EXPECTED_PUBLISHED_REQUESTS
          else "ROW_UNIVERSE_MISMATCH_NOT_LICENSE_TO_DELETE_ROWS",
      "serving_profile_encoding":"NOT_MAPPED_TO_AUTHOR_CODEBOOK",
      "reply_outcome_encoding":"NOT_MAPPED_TO_AUTHOR_CODEBOOK",
      "author_table3_replication":"NOT_PERFORMED",
      "single_field_binary_histogram_never_treatment_assignment":True,
      "participant_rows_exported":False,
      "raw_header_or_category_values_exported":False,
      "raw_S8_bytes_in_research_repository":False,
      "R072_IMAGE_STANDING_STERN_REAL_HUMAN_MODEL":"NOT_FITTED",
      "independent_E3":"OPEN","PESEN_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        raw,source=retrieve()
        if source not in ("PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT","PLOS_DIRECT_PUBLISHER"):
            raise ValueError("SOURCE_ORIGIN_NOT_PLOS")
        result=scan_rows(raw)
    except (ValueError,OSError) as e:
        result={"study":"R072","stage":"E2_PLOS_S8_AUTHOR_UNIVERSE_AND_COLUMN_DOMAINS_REV004",
                "status":"COLUMN_DOMAINS_UNRESOLVED",
                "error":str(e)[:90] if isinstance(e,ValueError) else "NETWORK_OR_IO_FAILURE",
                "raw_human_values_exported":False,"PESEN_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    safe={k:result.get(k) for k in (
      "status","physical_nonheader_rows","nonheader_rows_with_any_nonempty",
      "nonheader_rows_complete_in_all_ten_columns",
      "observed_row_universe_vs_published_n","anonymous_column_domains","error")}
    print(json.dumps(safe,sort_keys=True))
    if result["status"]!="R072_E2_REAL_COLUMN_DOMAINS_CHECKED":
        raise RuntimeError("R072 real anonymized column-domain source gate not satisfied")


if __name__=="__main__":main()
