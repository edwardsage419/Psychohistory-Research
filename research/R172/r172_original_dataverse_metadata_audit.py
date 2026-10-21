"""R172 official public Harvard Dataverse metadata access-only probe.

No raw observations fetched, no risk set or censoring inferred and no model
performance claimed. An audited no-access outcome remains a source gate.
"""
from __future__ import annotations
from urllib.request import Request,urlopen
from urllib.parse import quote,urlparse
from pathlib import Path
import json,hashlib

BASE="https://dataverse.harvard.edu"
PID="doi:10.7910/DVN/WFO1N1"
MAX_METADATA=3_000_000

def fetch_metadata():
    url=BASE+"/api/datasets/:persistentId/?persistentId="+quote(PID,safe="")
    report={"research_id":"R172","query_PID":PID,"official_API_url":url,
            "status":"METADATA_NOT_YET_ACCESSED",
            "raw_historical_data_acquired":False,
            "original_country_year_rows_inspected":0,
            "event_risk_sets_verified":False,
            "real_event_models_fitted":False,
            "heldout_historical_prediction_scored":False}
    try:
        request=Request(url,headers={
            "User-Agent":"Psychohistory-Research/1.0 event-history source metadata audit",
            "Accept":"application/json"})
        with urlopen(request,timeout=40) as response:
            resolved=response.geturl()
            if urlparse(resolved).hostname!="dataverse.harvard.edu":
                raise ValueError("unsafe redirected metadata source")
            raw=response.read(MAX_METADATA+1)
            if len(raw)>MAX_METADATA:raise ValueError("oversized unexpected source metadata")
        d=json.loads(raw)
        if d.get("status")!="OK" or "data" not in d:
            raise ValueError("Dataverse API did not return a successful data record")
        obj=d["data"]
        version=obj.get("latestVersion") or {}
        rawfiles=version.get("files") or []
        concise=[]
        for item in rawfiles:
            x=item.get("dataFile",{})
            concise.append({
                "id":x.get("id"),
                "filename":x.get("filename"),
                "filesize":x.get("filesize"),
                "contentType":x.get("contentType"),
                "md5":x.get("md5"),
                "restricted":x.get("restricted"),
                "storageIdentifier_present":bool(x.get("storageIdentifier"))
            })
        report.update({
            "status":"PUBLIC_METADATA_OBTAINED_NOT_RAW_DATA",
            "resolved_URL":resolved,
            "source_dataset_id":obj.get("id"),
            "persistentId":obj.get("persistentId"),
            "metadata_sha256":hashlib.sha256(raw).hexdigest(),
            "metadata_raw_bytes":len(raw),
            "version_number":version.get("versionNumber"),
            "version_minor_number":version.get("versionMinorNumber"),
            "license":version.get("license"),
            "terms_of_use":version.get("termsOfUse"),
            "file_count":len(concise),
            "file_descriptors":concise,
        })
        print("R172_OFFICIAL_METADATA",json.dumps({
          "status":report["status"],"file_count":report["file_count"],
          "version":[report["version_number"],report["version_minor_number"]],
          "license":report["license"]},ensure_ascii=False))
        for file in concise:print("R172_PUBLIC_FILE_DESCRIPTOR",json.dumps(file,ensure_ascii=False))
    except Exception as exc:
        report.update({"status":"METADATA_ACCESS_BLOCKED_OR_ERROR",
                       "error":type(exc).__name__+": "+str(exc)})
        print("R172_METADATA_ACCESS_BARRIER",report["error"])
    file=Path("R172_ORIGINAL_HARVARD_DATAVERSE_METADATA_AUDIT.json")
    file.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R172_AUDIT_FILE_SHA256",hashlib.sha256(file.read_bytes()).hexdigest())
    return report

if __name__=="__main__":
    fetch_metadata()
