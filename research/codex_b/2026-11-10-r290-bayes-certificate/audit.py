"""S86 full artifact gate against integer loss/rule-law certificates."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from certificate import derive,require


def strict_json(raw):
    def unique(pairs):
        found={}
        for key,value in pairs:
            require(key not in found,"DUPLICATE_JSON_KEY");found[key]=value
        return found
    def invalid(_):raise ValueError("NONFINITE_JSON_CONSTANT")
    return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid)


def normalized(doc,expected):
    require(type(doc) is dict and set(doc)==set(expected),"ROOT_SCHEMA")
    rows=doc["results"];require(type(rows) is list and len(rows)==24,"RESULT_COVERAGE")
    allowed={(r["world"],r["m"]) for r in expected["results"]};indexed={}
    for row in rows:
        require(type(row) is dict and type(row.get("world")) is str and type(row.get("m")) is int,"WORLD_KEY_TYPE")
        key=(row["world"],row["m"])
        require(key in allowed and key not in indexed,"FROZEN_WORLD_KEY_OR_DUPLICATE")
        indexed[key]=row
    require(set(indexed)==allowed,"WORLD_UNIVERSE")
    result=dict(doc);result["results"]={world+"|"+str(m):row for (world,m),row in indexed.items()}
    return result


def compare(actual,expected,path="root"):
    require(type(actual) is type(expected),"FIELD_TYPE:"+path)
    if type(expected) is dict:
        require(set(actual)==set(expected),"FIELD_SCHEMA:"+path)
        return sum(compare(actual[k],value,path+"."+k) for k,value in expected.items())
    require(actual==expected,"FIELD_VALUE:"+path)
    return 1


def audit(csv_path,json_path):
    csv_raw,json_raw=Path(csv_path).read_bytes(),Path(json_path).read_bytes()
    derived=derive(csv_raw);expected=derived["expected"];actual=strict_json(json_raw)
    checked=compare(normalized(actual,expected),normalized(expected,expected))
    return {"status":"PASS_COMPLETE_BAYES_AND_RULE_LAW_CERTIFICATE","source_rows":1950,
            "result_leaf_checks":checked,"scientific_fraction_fields":144,"frozen_world_sample_pairs":24,
            "complete_binary_rule_losses":384,"cutoff_rule_losses":72,
            "loss_certificates":derived["loss_certificates"],"rule_histograms":derived["rule_histograms"],
            "input_sha256":{"csv":hashlib.sha256(csv_raw).hexdigest(),"json":hashlib.sha256(json_raw).hexdigest()},
            "new_human_scores":0,"new_E2_E3":0,"formal_scientific_reacceptance":"NOT_RUN"}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("csv");p.add_argument("json");a=p.parse_args()
    try:r=audit(a.csv,a.json)
    except (OSError,ValueError,KeyError,TypeError,UnicodeError,csv.Error) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)[:200]}));raise SystemExit(2)
    print(json.dumps(r,indent=2))
