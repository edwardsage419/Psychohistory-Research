"""R172 original historical-event episode dataset source-bytes audit.

Public original Harvard Dataverse v1.1 DOI:10.7910/DVN/WFO1N1, CC0-1.0.
Original file IDs and MD5s were read from the official public Dataverse API.
This probes raw bytes only, not an inferred event/hazard result.
"""
from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urlparse
from hashlib import md5,sha256
import csv,io,json

FILES=(
 (10875177,"Replication dataset.tab",428013,"4343114d56124f88bce9d9cc3ce81523",
  "Original_Replication_dataset.tab"),
 (10875178,"Replication code (Stata file)",17387,"2dd571e5f94bd1f79158dcd2b53b0b94",
  "Original_Replication_code_Stata.do"),
)
SOURCE=Path(__file__).resolve().parent/"source"
RESULT=Path(__file__).resolve().parent/"R172_ORIGINAL_EVENT_DATA_BYTE_AUDIT.json"


def get_file(fileid,maxsize):
    url=f"https://dataverse.harvard.edu/api/access/datafile/{fileid}"
    req=Request(url,headers={"User-Agent":"Psychohistory-R172-original-source-audit/1.0",
                             "Accept":"application/octet-stream,text/tab-separated-values,*/*"})
    with urlopen(req,timeout=45) as r:
        final=r.geturl()
        host=urlparse(final).hostname or ""
        if urlparse(final).scheme!="https" or not (
            host=="dataverse.harvard.edu" or
            host.endswith(".harvard.edu") or host.endswith(".amazonaws.com")):
            raise ValueError("unexpected external original data redirection: "+final)
        content=r.read(maxsize+1)
    if len(content)>maxsize:raise ValueError("official file exceeds predeclared byte limit")
    return content,final


def inspect_tab(raw):
    decoded=raw.decode("utf-8-sig")
    lines=decoded.splitlines()
    reader=csv.DictReader(io.StringIO(decoded),delimiter="\t")
    fields=reader.fieldnames or []
    rows=list(reader)
    return {
        "field_count":len(fields),
        "all_original_field_names":fields,
        "row_count":len(rows),
        "first_three_rows_without_personal_data":rows[:3],
        "line_count":len(lines),
        "duplicated_field_names":len(fields)!=len(set(fields)),
        "empty_columns":[f for f in fields if all(not (r.get(f) or "").strip() for r in rows)]
    }


def audit():
    report={
       "research_id":"R172",
       "study":"Pérez-Liñán and Mainwaring, democratic trajectories in the third wave",
       "official_dataverse_DOI":"10.7910/DVN/WFO1N1",
       "dataverse_version":"1.1",
       "license_from_prior_official_metadata":"CC0-1.0",
       "raw_country_year_rows_scored_for_predictions":0,
       "event_and_censoring_definitions_validated":False,
       "original_historical_regime_hazard_fitted":False,
       "out_of_sample_predictions_scored":False,
       "status":"NOT_YET_DOWNLOADED",
       "file_records":[]
    }
    SOURCE.mkdir(parents=True,exist_ok=True)
    success=True
    for fid,label,expected_size,expected_md5,localname in FILES:
        rec={"source_file_id":fid,"source_display_name":label,
             "expected_original_bytes":expected_size,
             "expected_source_MD5":expected_md5,
             "local_filename":localname}
        try:
            raw,final=get_file(fid,expected_size+1024)
            rec.update({"actual_bytes":len(raw),"actual_MD5":md5(raw).hexdigest(),
                        "actual_SHA256":sha256(raw).hexdigest(),"resolved_URL":final})
            if len(raw)!=expected_size or md5(raw).hexdigest()!=expected_md5:
                raise ValueError("downloaded bytes do not match official original file metadata")
            (SOURCE/localname).write_bytes(raw)
            rec["status"]="ORIGINAL_FILE_BYTES_VERIFIED"
            if fid==10875177:
                rec["structural_tab_audit"]=inspect_tab(raw)
        except Exception as exc:
            rec["status"]="SOURCE_BYTES_UNAVAILABLE_OR_MISMATCH"
            rec["failure"]=type(exc).__name__+": "+str(exc)
            success=False
        print("R172_ORIGINAL_SOURCE_FILE",json.dumps(rec,ensure_ascii=False))
        report["file_records"].append(rec)
    report["status"]="SOURCE_BYTES_AUTHENTIC_COMPLETE_NOT_EVENT_MODELED" if success else "SOURCE_BYTE_ACCESS_OR_INTEGRITY_BLOCKED"
    RESULT.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("R172_ORIGINAL_AUDIT_STATUS",report["status"])
    print("R172_ORIGINAL_AUDIT_SHA256",sha256(RESULT.read_bytes()).hexdigest())


if __name__=="__main__":
    audit()
