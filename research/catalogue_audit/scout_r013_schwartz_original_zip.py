#!/usr/bin/env python3
"""Bounded historical R013 ZIP member audit for Schwartz mention, not model E2."""
import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ARCHIVE=ROOT/"archives/library-originals/心理史学_R013_正式研究包_2026-10-14.zip"
SHA="d18eaa9a721fe9850ba93590fd9c112be70ae7282e7cc7b1341ee53f2e265d8c"
TERMS=("schwartz","基本价值","基本人类价值","价值观","human values","pvq","circumplex","价值结构","r013")
EXT=(".md",".txt",".json",".csv",".py",".html",".yaml",".yml")
OUT=ROOT/"docs/R293_R013_ORIGINAL_ZIP_MEMBERS_SCHWARTZ_EVIDENCE_AUDIT_2026-10-23.json"

def inspect():
    raw=ARCHIVE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SHA
    archive=zipfile.ZipFile(io.BytesIO(raw))
    assert archive.testzip() is None
    entries=[]
    for info in archive.infolist():
        if info.is_dir():continue
        record={"name":info.filename,"bytes":info.file_size,"crc":info.CRC}
        if info.file_size>2_000_000:
            record["scanned"]="SKIP_TOO_LARGE"
        elif not info.filename.lower().endswith(EXT):
            record["scanned"]="SKIP_BINARY"
        else:
            member=archive.read(info)
            decoded=member.decode("utf-8",errors="replace").lower()
            record["sha256"]=hashlib.sha256(member).hexdigest()
            record["scanned"]="FULL_TEXT_UTF8_REPLACEMENT"
            record["hits"]={term:decoded.count(term) for term in TERMS if decoded.count(term)}
            # Do not treat mention frequency as study or scientific replication.
            record["source_has_substantive_code"]=bool(info.filename.lower().endswith(".py") and "schwartz" in decoded)
        entries.append(record)
    result={"archive":str(ARCHIVE.relative_to(ROOT)),"archive_sha256":SHA,
            "zip_crc": "PASS", "member_count":len(entries),
            "member_scan":entries,
            "scoped_conclusion":"KEYWORD_AND_BYTES_PROVENANCE_ONLY_NO_E1_OR_E2_OR_ORIGINAL_AUTHOR_REPLICATION",
            "historical_R013_zip_exists":True,
            "new_real_human_E2":0}
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--emit",action="store_true",required=True)
    opts=parser.parse_args()
    result=inspect()
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"archive":result["archive"],"members":result["member_count"],"zip_crc":result["zip_crc"],"output":str(OUT.relative_to(ROOT))},ensure_ascii=False))
