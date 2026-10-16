#!/usr/bin/env python3
"""Post-failure diagnosis: exact original ZIP, only aggregate anomaly counts.

Never exports rows, user IDs, artist IDs or tagging sequences.
"""
import argparse,csv,hashlib,io,json
from pathlib import Path
from r069_hetrec_lastfm_source_audit import fetch_source,safe_archive


def analyze(raw):
    files=safe_archive(raw)
    out={}
    for name,cols in (("user_friends.dat",("userID","friendID")),
                      ("user_taggedartists-timestamps.dat",
                       ("userID","artistID","tagID","timestamp"))):
        rd=csv.DictReader(io.StringIO(files[name].decode("utf-8-sig"),newline=""),delimiter="\t")
        if rd.fieldnames!=list(cols):
            raise ValueError("UNEXPECTED_ORIGINAL_HEADER")
        anomaly={col:{"nonpositive_integer_rows":0,"nonnumeric_rows":0,
                      "negative_rows":0,"zero_rows":0} for col in cols}
        rows=0
        for row in rd:
            rows+=1
            if rows>200000:raise ValueError("REAL_SOURCE_TOO_MANY_ROWS")
            for col in cols:
                try:
                    v=int(row[col])
                except (ValueError,TypeError):
                    anomaly[col]["nonnumeric_rows"]+=1
                    continue
                if v<=0:
                    anomaly[col]["nonpositive_integer_rows"]+=1
                if v==0:
                    anomaly[col]["zero_rows"]+=1
                if v<0:
                    anomaly[col]["negative_rows"]+=1
        out[name]={"rows":rows,"numeric_field_anomalies":anomaly}
    return {"stage":"R069_HETREC_POST_FAILURE_INTEGER_DIAGNOSTIC",
            "status":"AGGREGATE_DIAGNOSTIC_ONLY_NOT_SOURCE_ACCEPTANCE",
            "original_zip_md5":hashlib.md5(raw).hexdigest(),
            "original_zip_sha256":hashlib.sha256(raw).hexdigest(),
            "tables":out,
            "causal_influence_inference":"NOT_PERFORMED",
            "no_user_or_artist_ids_exported":True,"pesen_v01":"FROZEN"}


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    try:
        output=analyze(fetch_source())
    except (ValueError,OSError,UnicodeError) as e:
        output={"stage":"R069_HETREC_POST_FAILURE_INTEGER_DIAGNOSTIC",
                "status":"UNRESOLVED",
                "error_type":type(e).__name__,
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,sort_keys=True))
    if output["status"]!="AGGREGATE_DIAGNOSTIC_ONLY_NOT_SOURCE_ACCEPTANCE":
        raise RuntimeError("diagnostic is unresolved")


if __name__=="__main__":main()
