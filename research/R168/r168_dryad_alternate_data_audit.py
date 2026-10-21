"""R168 publicly available Derex 2015 Dryad original experiment retrieval gate.

This is independent of Derex et al Nature 2013; these datasets must never
be labeled replication of the Nature 2013 group-size experiment.
Dryad metadata and file IDs are read before any claim of empirical reuse.
"""
from __future__ import annotations
from urllib.request import urlopen,Request
from urllib.parse import quote,urljoin,urlparse
from urllib.error import HTTPError,URLError
import json,hashlib,pathlib,zipfile,io

DOI="doi:10.5061/dryad.1425c"
BASE="https://datadryad.org"
ROOT=pathlib.Path("dryad_source_audit")
ROOT.mkdir(exist_ok=True)
MAX_BYTES=8_000_000

def fetch(uri):
    req=Request(uri,headers={"User-Agent":"PsychohistoryResearch/1.0 source provenance check",
                  "Accept":"application/json, application/octet-stream, */*"})
    with urlopen(req,timeout=35) as r:
        b=r.read(MAX_BYTES+1)
        if len(b)>MAX_BYTES:raise ValueError("unanticipated source >8MB")
        return b,r.geturl(),r.headers.get("Content-Type","")

def run():
    out={"study":"Derex, Feron, Godelle, Raymond (2015)",
        "not_derex_2013_nature_group_size_experiment":True,
        "dataset_DOI":"10.5061/dryad.1425c",
        "download_status":"unavailable",
        "original_rows_scored":0,"independent_predictions":0}
    api=BASE+"/api/v2/datasets/"+quote(DOI,safe="")
    endpoints=[api,BASE+"/api/v2/files/21647/download"]
    try:
        metadata,actual,typ=fetch(api)
        j=json.loads(metadata)
        version=j.get("_links",{}).get("stash:version",{}).get("href")
        out["api_dataset_title"]=j.get("title")
        out["api_license"]=j.get("license")
        out["api_version_href"]=version
        out["api_http_content_type"]=typ
        out["metadata_sha256"]=hashlib.sha256(metadata).hexdigest()
        print("DRYAD_METADATA",json.dumps({k:out.get(k) for k in
            ("api_dataset_title","api_license","api_version_href","metadata_sha256")},ensure_ascii=False))
        if version:
            ub=urljoin(BASE,version)
            detail,_,_=fetch(ub)
            vj=json.loads(detail)
            out["version_number"]=vj.get("versionNumber")
            out["version_id"]=vj.get("id")
            file_href=vj.get("_links",{}).get("stash:files",{}).get("href")
            if file_href:
                fj=json.loads(fetch(urljoin(BASE,file_href))[0])
                out["file_descriptors"]=fj.get("_embedded",{}).get("stash:files",[])
            elif vj.get("id"):
                fj=json.loads(fetch(BASE+"/api/v2/versions/"+str(vj["id"])+"/files")[0])
                out["file_descriptors"]=fj.get("_embedded",{}).get("stash:files",[])
            print("DRYAD_FILE_DESCRIPTOR_KEYS",json.dumps([
                {k:item.get(k) for k in ("id","path","size","mimeType","digest","digestType","_links")}
                for item in out.get("file_descriptors",[])],ensure_ascii=False))
    except Exception as exc:
        out["metadata_error"]=type(exc).__name__+": "+str(exc)
        print("DRYAD_METADATA_FAILED",out["metadata_error"])

    try:
        data,actual,typ=fetch(endpoints[1])
        signature=("OOXML_ZIP" if data[:4]==b"PK"+bytes([3,4]) else
                   "OLE_XLS" if data[:8]==bytes.fromhex("D0CF11E0A1B11AE1") else
                   "HTML" if b"html" in data[:200].lower() else "UNKNOWN")
        out["data_bytes"]=len(data)
        out["data_sha256"]=hashlib.sha256(data).hexdigest()
        out["data_signature"]=signature
        out["data_type"]=typ
        out["data_resolved_url"]=actual
        if signature=="OOXML_ZIP":
            # Inspect ZIP structure only, avoiding any workbook modifications.
            z=zipfile.ZipFile(io.BytesIO(data))
            out["spreadsheet_xml_members"]=[x for x in z.namelist()
                if x.startswith("xl/worksheets/sheet") and x.endswith(".xml")]
            out["has_workbook_xml"]="xl/workbook.xml" in z.namelist()
            if not out["has_workbook_xml"]:raise ValueError("invalid XLSX structure")
            (ROOT/"Social_Learning_and_the_Replication_Process_ORIGINAL.xlsx").write_bytes(data)
            out["download_status"]="XLSX_AUTHENTIC_RAW_BYTES"
        else:
            out["download_status"]="UNEXPECTED_CONTENT"
        print("DRYAD_DATA_FETCH",json.dumps({k:out.get(k) for k in
            ("download_status","data_bytes","data_sha256","data_signature",
             "spreadsheet_xml_members")},ensure_ascii=False))
    except Exception as exc:
        out["download_error"]=type(exc).__name__+": "+str(exc)
        print("DRYAD_DOWNLOAD_FAILED",out["download_error"])
    # Second route uses the documented public dataset-package API; preserve
    # a separate status if the site blocks the browser download route.
    if out["download_status"]!="XLSX_AUTHENTIC_RAW_BYTES":
        package_api=api+"/download"
        try:
            bundle,final,typ=fetch(package_api)
            out["official_api_bundle_sha256"]=hashlib.sha256(bundle).hexdigest()
            out["official_api_bundle_size"]=len(bundle)
            out["official_api_bundle_url"]=final
            out["official_api_bundle_mime"]=typ
            if not bundle.startswith(b"PK"+bytes([3,4])):
                raise ValueError("Official public package is not a ZIP signature")
            z=zipfile.ZipFile(io.BytesIO(bundle))
            out["bundle_members"]=z.namelist()
            found=[n for n in z.namelist() if n.lower().endswith(".xlsx")]
            if not found:raise ValueError("Official package lacks referenced XLSX")
            if len(found)!=1:raise ValueError("Ambiguous multiple XLSX source files")
            raw=z.read(found[0])
            if raw[:4]!=b"PK"+bytes([3,4]):
                raise ValueError("Nested XLSX has unexpected signature")
            sheet=zipfile.ZipFile(io.BytesIO(raw))
            if "xl/workbook.xml" not in sheet.namelist():
                raise ValueError("Nested XLSX lacks workbook XML")
            original=ROOT/"Social_Learning_and_the_Replication_Process_ORIGINAL.xlsx"
            original.write_bytes(raw)
            out["download_status"]="XLSX_AUTHENTIC_RAW_BYTES_FROM_OFFICIAL_DATASET_ZIP"
            out["data_bytes"]=len(raw)
            out["data_sha256"]=hashlib.sha256(raw).hexdigest()
            out["data_signature"]="OOXML_ZIP"
            out["spreadsheet_xml_members"]=[n for n in sheet.namelist()
                                            if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
            print("DRYAD_PACKAGE_SUCCESS",json.dumps({
                "zip_bytes":len(bundle),"xlsx_bytes":len(raw),
                "xlsx_sha256":out["data_sha256"],"member":found[0]},ensure_ascii=False))
        except Exception as exc:
            out["official_api_error"]=type(exc).__name__+": "+str(exc)
            print("DRYAD_PUBLIC_PACKAGE_FAILED",out["official_api_error"])
    (ROOT/"R168_DRYAD_ALTERNATE_DATA_ACCESS.json").write_text(
        json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return out

if __name__=="__main__":run()
