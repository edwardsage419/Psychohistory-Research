"""R173 first-hand original source access-only audit for cross-societal data.

D-PLACE/dplace-data, commit 9bfed2c8c206be00f55f71516f262bbca2234e5a,
CC-BY-4.0; also cite the original EA/SCCS sources and Kirby et al 2016.
No source dataset is an experiment, and this script does not estimate an
association, infer a treatment effect or issue any prediction.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha1,sha256
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request,urlopen
import csv,io,json,re,sys,zipfile

REPO="D-PLACE/dplace-data"
COMMIT="9bfed2c8c206be00f55f71516f262bbca2234e5a"
ORIGINAL_FILES={
 "datasets/EA/data.csv":(11274445,"ca16bd039a0b0bc0b430e257b0f47cec53c05e8c"),
 "datasets/EA/variables.csv":(29887,"badeb7299525b51190f740e1ce0bcbeba6c20856"),
 "datasets/EA/codes.csv":(76781,"0ac9eb7863f90f8e3c0ed33ea506ca491cd212d1"),
 "datasets/EA/societies.csv":(162348,"9a7e3ff625c7c9e2fb879cd914747c98cfc75888"),
 "datasets/EA/societies_mapping.csv":(22352,"31d34ee88fae59789a3cff6bf9625d09daef9555"),
 "datasets/SCCS/societies_mapping.csv":(7725,"21281b89a015911c9d1dd1198b6618b82cc6bc8c"),
}
HERE=Path(__file__).resolve().parent
SOURCE=HERE/"source"
RESULT=HERE/"R173_ORIGINAL_DPLACE_EA_SCCS_SOURCE_AUDIT.json"

def blob(raw):
    return sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

def authenticated(path,raw):
    if path not in ORIGINAL_FILES:raise ValueError("unregistered primary file")
    n,h=ORIGINAL_FILES[path]
    if len(raw)!=n or blob(raw)!=h:
        raise ValueError("primary original source file identity differs from pinned Git blob "+path)
    return {"bytes":len(raw),"git_blob_sha1":h,"sha256":sha256(raw).hexdigest()}

def fetch():
    for path in ORIGINAL_FILES:
        url=f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{path}"
        request=Request(url,headers={"User-Agent":"Psychohistory-R173-CCBY-original-source-audit/1.0"})
        with urlopen(request,timeout=65) as r:
            final=r.geturl()
            if urlparse(final).scheme!="https" or urlparse(final).hostname!="raw.githubusercontent.com":
                raise ValueError("unexpected remote source redirect: "+final)
            raw=r.read(ORIGINAL_FILES[path][0]+1)
        identity=authenticated(path,raw)
        file=SOURCE/path.split("datasets/",1)[1]
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_bytes(raw)
        print("R173_PINNED_SOURCE",path,json.dumps(identity,sort_keys=True))

def read_source(path):
    file=SOURCE/path.split("datasets/",1)[1]
    raw=file.read_bytes()
    authenticated(path,raw)
    return raw

def rows(path):
    raw=read_source(path).decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(raw))
    cols=reader.fieldnames or []
    if not cols or len(cols)!=len(set(cols)):
        raise ValueError("invalid first-hand source field names")
    return cols,list(reader)

def run():
    refs={path:authenticated(path,read_source(path)) for path in ORIGINAL_FILES}
    ea_data_columns,observations=rows("datasets/EA/data.csv")
    ea_soc_columns,societies=rows("datasets/EA/societies.csv")
    variable_cols,variables=rows("datasets/EA/variables.csv")
    code_cols,codes=rows("datasets/EA/codes.csv")
    mapping_cols,ea_map=rows("datasets/EA/societies_mapping.csv")
    sccs_cols,sccs_map=rows("datasets/SCCS/societies_mapping.csv")
    var_lookup={r["id"]:r for r in variables}
    selected={}
    for variable in ("EA003","EA005","EA006"):
        if variable not in var_lookup:
            raise ValueError("prespecified original variable absent: "+variable)
        selected[variable]={
          "title":var_lookup[variable]["title"],
          "kind":var_lookup[variable]["type"],
          "source_codes":[{"code":r["code"],"name":r["name"]} for r in codes if r.get("var_id")==variable]
        }
    mappings=[(r.get("id",""),r.get("related","")) for r in ea_map]
    cross_refs=[(id,rel) for id,rel in mappings if "SCCS:" in rel]
    result={
      "research_id":"R173",
      "status":"FIRST_HAND_REAL_CROSS_CULTURAL_SOURCE_AUTHENTICITY_AND_SCHEMA_ONLY",
      "source_repository":REPO,"source_pinned_commit":COMMIT,
      "license":"CC-BY-4.0 - cite original ethnographic sources and Kirby et al 2016",
      "raw_authenticated_sources":refs,
      "EA_data_column_names":ea_data_columns,
      "EA_data_rows":len(observations),
      "EA_society_column_names":ea_soc_columns,
      "EA_society_rows":len(societies),
      "EA_society_distinct_IDs":len({r["id"] for r in societies}),
      "EA_variable_rows":len(variables),
      "EA_code_rows":len(codes),
      "EA_mapping_rows":len(ea_map),
      "EA_mapping_entries_explicitly_referencing_SCCS":len(cross_refs),
      "EA_mapping_distinct_IDs_explicitly_referencing_SCCS":len({id for id,_ in cross_refs}),
      "SCCS_mapping_rows":len(sccs_map),
      "source_EA_selected_definition_and_eligible_codes":selected,
      "original_real_cross_societal_association_scored":False,
      "original_SCCS_to_EA_mapping_uniquely_validated":False,
      "independent_historical_or_behavioral_prediction_scored":False,
      "new_E2_predictions":0,"new_E3_predictions":0
    }
    RESULT.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("R173_PUBLIC_SOURCE_STRUCTURE",json.dumps({
      k:result[k] for k in ("EA_data_column_names","EA_data_rows",
        "EA_society_rows","EA_society_distinct_IDs","EA_variable_rows","EA_code_rows",
        "EA_mapping_entries_explicitly_referencing_SCCS","SCCS_mapping_rows")
    },ensure_ascii=False,sort_keys=True))
    print("R173_PUBLIC_SOURCE_AUDIT_SHA256",sha256(RESULT.read_bytes()).hexdigest())
    return result

def archive():
    files=["r173_original_dplace_source_audit.py",RESULT.name]
    files+=["source/"+path.split("datasets/",1)[1] for path in ORIGINAL_FILES]
    with zipfile.ZipFile(HERE/"R173_First_Hand_DPLACE_Original_EA_SCCS_Source_Audit.zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            item=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            item.compress_type=zipfile.ZIP_DEFLATED
            item.external_attr=0o644<<16
            z.writestr(item,(HERE/name).read_bytes())
    print("R173_SOURCE_ARCHIVE_SHA256",
       sha256((HERE/"R173_First_Hand_DPLACE_Original_EA_SCCS_Source_Audit.zip").read_bytes()).hexdigest())

if __name__=="__main__":
    if len(sys.argv)==2 and sys.argv[1]=="--fetch":fetch()
    elif len(sys.argv)==2 and sys.argv[1]=="--audit-and-archive":run();archive()
    else:raise SystemExit("usage: script.py --fetch|--audit-and-archive")
