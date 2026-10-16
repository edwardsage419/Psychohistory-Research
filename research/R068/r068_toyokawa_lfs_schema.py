#!/usr/bin/env python3
"""Source-pinned 2022 human social-learning raw schema audit.

Privacy: outputs only public column names, nonidentifying total counts,
source sha256 and status; no participant values, choices or group breakdown.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re
from pathlib import Path

COMMIT="6fca0b26c33af3a5b3c415719fa3df0dced15149"
FILE_SPEC={
 "allBehaviour1022_group.csv": {
   "size":4144197,
   "sha256":"b01af9eb32945c57b6a9528c2f7e291e955819c1df799cfc942708473cd4ceb3",
   "pointer_blob":"fc3d579f02f248b4a62b24a545f596ecd703b754"},
 "allBehaviour1022_indiv.csv": {
   "size":2306541,
   "sha256":"06ddbf5dbe64893f841ef6801c6e1e00553869eb774ee05740b8cf0d1f6801c1",
   "pointer_blob":"d260e6b6858d29dfe11215c9543ea97d98a07282"},
}
STEM="experimentalAnalysis/"
MAX_BYTES=8_000_000
MAX_ROWS=250_000
MAX_COLS=400
SAFE_HEADER=re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]{0,74}$")
TOPIC=re.compile(r"(?i)(subject|participant|player|agent|group|round|trial|choice|select|social|freq|reward|payoff|feedback|risk|option|success|correct|imit|learn|majority|model|performance|time|treatment)")
MISSING={"","NA","NaN","."}

def git_blob_sha(raw:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def pointer_contract(raw:bytes,expected_oid:str,expected_size:int)->bool:
    pattern=f"version https://git-lfs.github.com/spec/v1\noid sha256:{expected_oid}\nsize {expected_size}\n".encode()
    return raw==pattern

def safe_header(s:str)->str:
    return s if SAFE_HEADER.fullmatch(s) else "[NONSTANDARD_HEADER_REDACTED]"

def audit_csv(raw:bytes):
    if len(raw)>MAX_BYTES:
        raise ValueError("FILE_TOO_LARGE")
    if raw.startswith(b"version https://git-lfs.github.com/spec/v1"):
        raise ValueError("LFS_POINTER_IS_NOT_REAL_DATA")
    content=raw.decode("utf-8-sig")
    reader=csv.reader(io.StringIO(content,newline=""),delimiter=",")
    try:
        head=next(reader)
    except StopIteration:
        raise ValueError("EMPTY_CSV") from None
    if not (1<=len(head)<=MAX_COLS) or len(set(head))!=len(head):
        raise ValueError("INVALID_OR_DUPLICATE_COLUMNS")
    n=0; missing=0
    for row in reader:
        n+=1
        if n>MAX_ROWS or len(row)!=len(head):
            raise ValueError("RAGGED_OR_OVERSIZED_CSV")
        missing+=sum(x.strip() in MISSING for x in row)
    if n<2:
        raise ValueError("NO_BEHAVIORAL_DATA")
    return {
        "data_rows":n,"column_count":len(head),
        "safe_field_names":[safe_header(x) for x in head],
        "candidate_measurement_field_names":[safe_header(x) for x in head if TOPIC.search(x)],
        "total_missing_cells_literal_convention":missing,
        "row_width_errors":0,
        "per_person_values_exported":False,
    }


def audit_pinned_source(src_dir:Path, pointer_dir:Path|None=None):
    out={}
    for name,spec in FILE_SPEC.items():
        original=(src_dir/name).read_bytes()
        if pointer_dir is not None:
            pointer=(pointer_dir/name).read_bytes()
            if (not pointer_contract(pointer,spec["sha256"],spec["size"]) or
                git_blob_sha(pointer)!=spec["pointer_blob"]):
                raise ValueError("GIT_LFS_POINTER_OID_OR_BLOB_MISMATCH")
        if len(original)!=spec["size"] or hashlib.sha256(original).hexdigest()!=spec["sha256"]:
            raise ValueError("LFS_REAL_PAYLOAD_SHA_OR_SIZE_MISMATCH")
        out[name]={
            "public_repository_path":STEM+name,
            "pinned_expected_bytes":spec["size"],
            "pinned_payload_sha256":spec["sha256"],
            "pinned_pointer_git_blob":spec["pointer_blob"],
            "schema":audit_csv(original),
        }
    return {
        "research_id":"R068",
        "stage":"E2_TOYOKAWA_LFS_SOURCE_SCHEMA",
        "status":"SOURCE_SHA_AND_SCHEMA_PASS",
        "protocol":"protocols/R068_E2_TOYOKAWA_EXPERIMENT_LFS_SOURCE_2026-10-16.md",
        "upstream_repo":"WataruToyokawa/ToyokawaGaissmaier2021",
        "upstream_commit":COMMIT,
        "files":out,
        "individual_observations_redistributed":False,
        "actual_demonstrator_frequency_per_trial_verified":False,
        "actual_demonstrator_payoff_per_trial_verified":False,
        "e2_exact_three_demonstrator_majority_model_identification":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,required=True)
    p.add_argument("--pointer-dir",type=Path)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=audit_pinned_source(a.source_dir,a.pointer_dir)
    except (OSError,ValueError,UnicodeError,csv.Error) as exc:
        result={
            "research_id":"R068","stage":"E2_TOYOKAWA_LFS_SOURCE_SCHEMA",
            "status":"SOURCE_UNRESOLVED",
            "error_type":type(exc).__name__,
            "error_code":str(exc)[:90] if isinstance(exc,ValueError) else "IO_OR_DECODING_ERROR",
            "human_trial_model_fit_performed":False,
            "pesen_v01":"FROZEN",
        }
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"stage":result["stage"],"status":result["status"],
                     "nonidentifying_files":{n:{"rows":f["schema"]["data_rows"],
                                             "columns":f["schema"]["column_count"],
                                             "candidate_fields":f["schema"]["candidate_measurement_field_names"]}
                         for n,f in result.get("files",{}).items()}},sort_keys=True))
    if result["status"]!="SOURCE_SHA_AND_SCHEMA_PASS":
        raise RuntimeError("R068 original human experimental payload not yet verified")


if __name__=="__main__":
    main()
