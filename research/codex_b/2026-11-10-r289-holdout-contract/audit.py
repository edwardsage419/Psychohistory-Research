"""S85 full result contract against an independently generated stopping DP.

Historical flags are matched, not taken as evidence that a mutant was tested.
The public entry always computes its own expectation from the frozen mechanism.
"""
import argparse
from collections import defaultdict
import csv
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path

from stopping import NAMES,WEIGHTS,TAGS,joint_law,reward2,expected_tree,require

FIELDS=("distribution","source","weight","den","h3net2","h5net2","difference2")


def strict_json(raw):
    def unique(pairs):
        found={}
        for key,value in pairs:
            require(key not in found,"DUPLICATE_JSON_KEY");found[key]=value
        return found
    def invalid(_):raise ValueError("NONFINITE_JSON_CONSTANT")
    return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid)


def normalized(document):
    require(type(document) is dict and set(document)==set(expected_tree()),"ROOT_SCHEMA")
    copied=dict(document)
    for field,mkey in (("worlds","training_episodes"),("independent_polynomial","m")):
        require(type(document[field]) is list and len(document[field])==6,"WORLD_COVERAGE")
        records={}
        for row in document[field]:
            require(type(row) is dict and type(row.get("distribution")) is str and row["distribution"] in NAMES and
                    type(row.get(mkey)) is int and row[mkey] in (1,2),"WORLD_ID")
            key=row["distribution"]+"|"+str(row[mkey]);require(key not in records,"DUPLICATE_WORLD")
            records[key]=row
        copied[field]=records
    require(type(document["mutation_tests"]) is list and len(document["mutation_tests"])==6,"FLAG_COVERAGE")
    flags={}
    for row in document["mutation_tests"]:
        require(type(row) is dict and type(row.get("tag")) is str and row["tag"] in TAGS and row["tag"] not in flags,"FLAG_ID")
        flags[row["tag"]]=row
    copied["mutation_tests"]=flags
    return copied


def compare(actual,expected,path="root"):
    require(type(actual) is type(expected),"FIELD_TYPE:"+path)
    if type(expected) is dict:
        require(set(actual)==set(expected),"FIELD_SCHEMA:"+path)
        return sum(compare(actual[k],v,path+"."+k) for k,v in expected.items())
    require(actual==expected,"FIELD_VALUE:"+path)
    return 1


def audit(csv_path,json_path):
    csv_raw,json_raw=Path(csv_path).read_bytes(),Path(json_path).read_bytes()
    actual=strict_json(json_raw);expected=expected_tree()
    leaf_checks=compare(normalized(actual),normalized(expected))
    table=list(csv.reader(io.StringIO(csv_raw.decode("utf-8"),newline=""),strict=True))
    require(len(table)==244 and tuple(table[0])==FIELDS,"LEDGER_HEADER_OR_COUNT")
    seen=set();mass={name:F(0) for name in NAMES};laws={name:defaultdict(F) for name in NAMES}
    for row in table[1:]:
        require(len(row)==7,"LEDGER_WIDTH")
        name,source=row[:2]
        require(name in NAMES and len(source)==4 and set(source)<={"1","3","5"},"LEDGER_ID")
        identity=(name,source);require(identity not in seen,"DUPLICATE_SOURCE");seen.add(identity)
        weights=WEIGHTS[name];weight=1
        for offer in source:weight*=weights[(int(offer)-1)//2]
        denominator=sum(weights)**4
        h3,h5=reward2(source,3),reward2(source,5)
        require(row[2:]==list(map(str,(weight,denominator,h3,h5,h5-h3))),"LEDGER_MASS_OR_PAYOFF")
        probability=F(weight,denominator);mass[name]+=probability;laws[name][(h3,h5)]+=probability
    require(len(seen)==243 and all(sum(s[0]==name for s in seen)==81 and mass[name]==1 for name in NAMES),"LEDGER_UNIVERSE")
    require(all(dict(laws[name])==joint_law(name) for name in NAMES),"LEDGER_VS_STOPPING_DP")
    return {"status":"PASS_INDEPENDENT_STOPPING_HOLDOUT_CONTRACT","source_rows":len(seen),
            "result_leaf_checks":leaf_checks,"world_fraction_fields":60,"fresh_test_worlds":6,
            "joint_reward_supports":{n:len(joint_law(n)) for n in NAMES},
            "input_sha256":{"csv":hashlib.sha256(csv_raw).hexdigest(),"json":hashlib.sha256(json_raw).hexdigest()},
            "historical_flags":"MATCHED_NOT_REENACTED_SCIENTIFIC_CERTIFICATION",
            "new_human_scores":0,"new_E2_E3":0}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("csv");parser.add_argument("json")
    args=parser.parse_args()
    try:result=audit(args.csv,args.json)
    except (OSError,ValueError,KeyError,TypeError,UnicodeError,csv.Error) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)[:200]}));raise SystemExit(2)
    print(json.dumps(result,indent=2))
