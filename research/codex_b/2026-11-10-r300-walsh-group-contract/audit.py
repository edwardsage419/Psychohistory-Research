"""R300 S96 complete frozen-group/source contract against a moment oracle."""
import argparse
import csv
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
from moments import FIELDS,expected,group_key,source_key,require


def strict_json(raw):
    def unique(pairs):
        out={}
        for key,value in pairs:
            require(key not in out,"DUPLICATE_JSON_KEY");out[key]=value
        return out
    def invalid(_):raise ValueError("NONFINITE_JSON_CONSTANT")
    return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid)


def normalized(doc,reference):
    require(type(doc) is dict and set(doc)==set(reference),"ROOT_SCHEMA")
    require(type(doc['results']) is list and len(doc['results'])==18,"MODEL_GROUP_COUNT")
    allowed={group_key(row) for row in reference['results']};groups={}
    for row in doc['results']:
        require(type(row) is dict and all(type(row.get(k)) is str for k in ('world','true_stay','candidate_stay','candidate_emission')),"GROUP_ID_TYPE")
        key=group_key(row);require(key in allowed,"FROZEN_GROUP_ID");require(key not in groups,"DUPLICATE_GROUP")
        groups[key]=row
    require(set(groups)==allowed,"MODEL_GROUP_UNIVERSE")
    result=dict(doc);result['results']=groups;return result


def compare(actual,reference,path="root"):
    require(type(actual) is type(reference),"FIELD_TYPE:"+path)
    if type(reference) is dict:
        require(set(actual)==set(reference),"FIELD_SCHEMA:"+path)
        return sum(compare(actual[k],v,path+'.'+k) for k,v in reference.items())
    require(actual==reference,"FIELD_VALUE:"+path);return 1


def audit(csv_path,json_path):
    csv_raw,json_raw=Path(csv_path).read_bytes(),Path(json_path).read_bytes()
    oracle=expected();reference=oracle['document'];actual=normalized(strict_json(json_raw),reference)
    leaves=compare(actual,normalized(reference,reference))
    table=list(csv.reader(io.StringIO(csv_raw.decode('utf-8'),newline=''),strict=True))
    require(len(table)==289 and tuple(table[0])==FIELDS,"SOURCE_HEADER_OR_COUNT")
    seen=set();mass={k:F(0) for k in actual['results']};risk=mass.copy();excess=mass.copy()
    for cells in table[1:]:
        require(len(cells)==13,"SOURCE_WIDTH")
        row=dict(zip(FIELDS,cells));key=source_key(row)
        require(key in oracle['sources'],"FROZEN_SOURCE_KEY");require(key not in seen,"DUPLICATE_SOURCE");seen.add(key)
        require(row==oracle['sources'][key],"MOMENT_SOURCE_FIELDS")
        group=group_key(row);mass[group]+=F(row['true_prefix_mass']);risk[group]+=F(row['weighted_brier']);excess[group]+=F(row['weighted_excess'])
    require(seen==set(oracle['sources']),"SOURCE_UNIVERSE")
    for key,row in actual['results'].items():
        require(mass[key]==1 and risk[key]==F(row['expected_brier']) and excess[key]==F(row['excess_brier']),"SOURCE_GROUP_LINK")
    return {"status":"PASS_WALSH_HMM_COMPLETE_GROUP_CONTRACT","source_rows":len(seen),"source_fraction_checks":2016,
            "unique_model_groups":len(actual['results']),"distinct_true_prefixes":32,"result_leaf_checks":leaves,
            "group_risk_fraction_fields":72,"independent_method":"observed_spin_even_moment_Walsh_expansion",
            "even_terms_per_probability":{"length4":8,"length5":16},"expected_groups":reference['results'],
            "input_sha256":{"csv":hashlib.sha256(csv_raw).hexdigest(),"json":hashlib.sha256(json_raw).hexdigest()},
            "new_human_scores":0,"new_E2_E3":0,"formal_scientific_reacceptance":"NOT_RUN"}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv');p.add_argument('json');a=p.parse_args()
    try:r=audit(a.csv,a.json)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)[:200]}));raise SystemExit(2)
    print(json.dumps(r,indent=2))
