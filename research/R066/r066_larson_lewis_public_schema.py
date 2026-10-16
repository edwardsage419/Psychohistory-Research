#!/usr/bin/env python3
"""R066 empirical-source schema audit: public Larson–Lewis V1.0 source files.

NO respondent identifiers, responses, individual outcomes, edges or source file
contents are emitted. The archive includes only structural counts and SHA256.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOI = "doi:10.7910/DVN/RAHSVM"
VERSION = (1,0)
DATE_RELEASED = "2026-07-29T00:35:44Z"
FILES = {
    "data": ("Data_LarsonLewis_nws.tab", 14101729, 444658),
    "script": ("LL_SpecialIssue_Replication.R", 14101728, 72914),
    "codebook": ("Uganda_Codebook_NWS_2026.docx", 14101730, 30623),
}
MAX_BYTES = 10_000_000
MAX_ROWS = 100_000
MAX_COLS = 2_000
SAFE_COLUMN = re.compile(r"^[a-zA-Z][A-Za-z0-9_]{0,79}$")
TOPIC = re.compile(r"att|refug|base|end|follow|treat|interven|vill|network|friend|neighbor|node|degree|edge|distance|^id$|_id$|^bl|^el|wave",re.I)
NS_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_header(header: str) -> str:
    if SAFE_COLUMN.fullmatch(header):
        return header
    return "[unusual-header-redacted]"


def scan_tabular(raw: bytes):
    if len(raw)>MAX_BYTES:
        raise ValueError("source tabular exceeds maximum bytes")
    reader=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),delimiter="\t")
    try:
        headers=next(reader)
    except StopIteration:
        raise ValueError("empty data file") from None
    if not (1 <= len(headers) <= MAX_COLS) or any(not h.strip() for h in headers):
        raise ValueError("empty or invalid column names")
    if len(set(headers)) != len(headers):
        raise ValueError("duplicate tabular column name")
    count=0
    for row in reader:
        count+=1
        if count>MAX_ROWS or len(row)!=len(headers):
            raise ValueError("row count/shape violates frozen limits")
    if not count:
        raise ValueError("no data rows")
    candidate=[safe_header(h) for h in headers if TOPIC.search(h)]
    return {"rows":count,"columns":len(headers),"candidate_fieldnames":candidate[:250],
            "candidate_fields_total":len(candidate),
            "candidate_fieldnames_truncated":len(candidate)>250,
            "all_fields_nonempty_unique":True,"row_width_mismatches":0}


def scan_r_script(raw: bytes):
    if len(raw)>MAX_BYTES:
        raise ValueError("oversized R script")
    code=raw.decode("utf-8-sig")
    lower=code.lower()
    return {
        "line_count":len(code.splitlines()),
        "safe_search_counts":{name:lower.count(name) for name in (
            "read.csv","read.table","read_dta","haven::","network",
            "igraph","attitude","refugee","village","treat","edge")},
    }


def scan_docx(raw: bytes):
    if len(raw)>MAX_BYTES:
        raise ValueError("oversized codebook")
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            if z.testzip() is not None:
                raise ValueError("codebook ZIP integrity failed")
            xml=z.read("word/document.xml")
    except (zipfile.BadZipFile,KeyError):
        raise ValueError("source codebook not valid DOCX package") from None
    if len(xml)>MAX_BYTES:
        raise ValueError("codebook XML too large")
    root=ET.fromstring(xml)
    paras=root.findall(".//"+NS_W+"p")
    tables=root.findall(".//"+NS_W+"tbl")
    textnodes=root.findall(".//"+NS_W+"t")
    joined=" ".join((t.text or "") for t in textnodes).lower()
    return {"paragraphs":len(paras),"tables":len(tables),"text_nodes":len(textnodes),
            "safe_keyword_counts":{x:joined.count(x) for x in (
                "attitude","refugee","baseline","endline","network",
                "treatment","village","friendship","respondent")}}
            

def parse_metadata(catalog: dict):
    if (catalog.get("status")!="OK" or
        not isinstance(catalog.get("data"),dict)):
        raise ValueError("metadata API not successful")
    version=catalog["data"].get("latestVersion")
    if (not isinstance(version,dict) or
        (version.get("versionNumber"),version.get("versionMinorNumber"))!=VERSION or
        version.get("versionState")!="RELEASED" or
        version.get("releaseTime")!=DATE_RELEASED):
        raise ValueError("published V1.0 release drift")
    records=version.get("files")
    if not isinstance(records,list) or len(records)!=3:
        raise ValueError("source catalog file universe changed")
    actual={}
    for item in records:
        df=item.get("dataFile",{})
        if not isinstance(df,dict):
            raise ValueError("incomplete dataset file metadata")
        actual[df.get("id")]=(df.get("filename"),df.get("filesize"),item.get("restricted"))
    for name,identifier,size in FILES.values():
        if actual.get(identifier)!=(name,size,False):
            raise ValueError("pinned ID/size/license access changed: "+name)
    license_meta=version.get("license",{})
    if not isinstance(license_meta,dict) or license_meta.get("name")!="CC0 1.0":
        raise ValueError("dataset public license changed")
    return True


def audit_files(folder: Path, catalog: dict):
    parse_metadata(catalog)
    info={}
    scanners={"data":scan_tabular,"script":scan_r_script,"codebook":scan_docx}
    for label,(filename,identifier,size) in FILES.items():
        raw=(folder/filename).read_bytes()
        actual=len(raw)
        if actual!=size:
            raise ValueError(f"SIZE_MISMATCH_OR_FORMAT_CONVERSION: {label} {actual} vs {size}")
        info[label]={"public_datafile_id":identifier,"filename":filename,"size_bytes":actual,
                     "sha256":digest(raw),"schema":scanners[label](raw)}
    return {
        "study":"R066","stage":"E2_LARSON_LEWIS_V1_0_REAL_FILE_SCHEMA",
        "doi":DOI,"fixed_version":"1.0","fixed_release":DATE_RELEASED,
        "source_integrity":"SOURCE_SCHEMA_PASS",
        "files":info,
        "source_privacy":"NO_INDIVIDUAL_ROW_OR_EDGE_OUTPUT",
        "empirical_identification_ready":"NOT_DETERMINED_FROM_SCHEMA_ALONE",
        "fit_performed":False,"pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-dir",type=Path,required=True)
    ap.add_argument("--metadata",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    catalog=json.loads(args.metadata.read_text(encoding="utf-8"))
    try:
        result=audit_files(args.source_dir,catalog)
    except (ValueError,OSError,UnicodeError,csv.Error,ET.ParseError) as exc:
        result={"study":"R066","stage":"E2_LARSON_LEWIS_V1_0_REAL_FILE_SCHEMA",
                "source_integrity":"SOURCE_OR_SCHEMA_BLOCKED",
                "reason_type":type(exc).__name__,"reason":str(exc)[:250],
                "fit_performed":False,"pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"stage":result["stage"],"source_integrity":result["source_integrity"],
                      "summary":{k:{"rows":v["schema"].get("rows"),
                                    "columns":v["schema"].get("columns")}
                                 for k,v in result.get("files",{}).items()}},sort_keys=True))
    if result["source_integrity"]!="SOURCE_SCHEMA_PASS":
        raise RuntimeError("original V1.0 source schema audit failed; no empirical claim")


if __name__=="__main__":
    main()
