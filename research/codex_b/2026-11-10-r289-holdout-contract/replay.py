#!/usr/bin/env python3
"""Offline S85 source-mutation replay; new output directory required."""
import argparse
import csv
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from stopping import expected_tree,require
from test_contract import CSV_PATH,JSON_PATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
R=ROOT/"research/validation/r289_s85_train_selected_aspiration_20261030.js"
B=ROOT/"research/evidence_audit/b_r289_s85_independent_convolution_20261030.py"
ORIGINAL_CSV="research/R289/R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv"
ORIGINAL_JSON="research/R289/R289_EXACT_SATISFICING_RESULTS.json"
PIN_SHA="fe2ab597282865232058ec3c8968e72817c6eaca2d1848d93e24d1543c212cde"
EDITS={
 "hindsight_evaluation":[('const net=add(e3,mul(p5,sub(e5,e3)));','const net=f(rr.reduce((s,z)=>s+BigInt(z.weight*Math.max(z.h3net2,z.h5net2)),0n),2n*den);')],
 "ties_choose_H5":[('if(x.difference2>0)win','if(x.difference2>=0)win'),('if(d>0)win','if(d>=0)win'),('if(d>0)positive','if(d>=0)positive')],
 "single_route_tie_control":[('if(x.difference2>0)win','if(x.difference2>=0)win')]}


def sha(raw):return hashlib.sha256(raw).hexdigest()


def capture():
    raw=(HERE/"pins.json").read_bytes();require(sha(raw)==PIN_SHA,"PIN_MANIFEST_CHANGED")
    pins=json.loads(raw);inputs={};found={}
    for name,pinned in pins.items():
        data=(ROOT/name).read_bytes();blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        tracked=subprocess.check_output(["git","rev-parse","HEAD:"+name],cwd=ROOT,text=True).strip()
        require(blob==pinned==tracked,"PINNED_INPUT_CHANGED:"+name)
        inputs[name]=data;found[name]={"bytes":len(data),"sha256":sha(data),"git_blob":blob}
    for path in [HERE/"pins.json",*sorted(HERE.glob("*.py"))]:
        data=path.read_bytes();found[str(path.relative_to(ROOT))]={"bytes":len(data),"sha256":sha(data)}
    return inputs,found


def source_parity(inputs):
    paired=list(csv.DictReader(io.StringIO(inputs[str(CSV_PATH.relative_to(ROOT))].decode())))
    lookup={(r["distribution"],r["source"]):r for r in paired}
    original=list(csv.DictReader(io.StringIO(inputs[ORIGINAL_CSV].decode())))
    require(len(lookup)==243 and len(original)==486,"PARITY_COVERAGE")
    seen=set()
    for row in original:
        key=(row["distribution"],row["complete_ordered_four_offer_source"]);h=row["aspiration"]
        require(key in lookup and h in ("3","5") and (key,h) not in seen,"PARITY_ID")
        seen.add((key,h));entry=lookup[key]
        require(F(row["complete_source_probability"])==F(int(entry["weight"]),int(entry["den"])) and
                F(row["net_payoff"])==F(int(entry["h"+h+"net2"]),2),"PARITY_PAYOFF_OR_MASS")
    old=json.loads(inputs[ORIGINAL_JSON]);population=0
    expected={(r["distribution"],r["training_episodes"]):r for r in expected_tree()["worlds"]}
    for row in old["worlds"]:
        current=expected[(row["distribution"],1)]
        require(row["expected_net_payoff"]==current["expected_H"+str(row["aspiration"])] and
                row["first_offer_baseline_mean"]==current["first_only"],"POPULATION_BASELINE_PARITY")
        population+=2
    require(population==12,"POPULATION_BASELINE_COVERAGE")
    return {"original_rows":len(seen),"paired_rows":len(lookup),"population_fields":population}


def run(output):
    output.mkdir(parents=True,exist_ok=False);inputs,before=capture();commands=[]
    python=[sys.executable,"-B"]+(["-O"] if sys.flags.optimize else [])

    def execute(tag,args,cwd=ROOT):
        child=subprocess.run(args,cwd=cwd,capture_output=True,timeout=60);streams={}
        for suffix,raw in (("stdout",child.stdout),("stderr",child.stderr)):
            name=tag+"."+suffix
            if raw:(output/name).write_bytes(raw)
            streams[suffix]={"bytes":len(raw),"sha256":sha(raw),"file":name if raw else None}
        commands.append({"tag":tag,"argv":args,"cwd":str(cwd),"exit_code":child.returncode,"streams":streams})
        (output/"commands.json").write_text(json.dumps(commands,indent=2)+"\n");return child

    tests=execute("new-12-tests",python+["-m","unittest","discover","-s",str(HERE),"-p","test_contract.py","-v"])
    require(tests.returncode==0 and re.search(rb"Ran 12 tests in",tests.stderr) is not None,"NEW_TESTS_FAIL")
    archive=execute("audit-archive",python+[str(HERE/"audit.py"),str(CSV_PATH),str(JSON_PATH)])
    require(archive.returncode==0,"ARCHIVE_CONTRACT_FAIL");proof=json.loads(archive.stdout)
    identity={};mutants=[];controls=[]
    with tempfile.TemporaryDirectory(prefix="codex-b-r289-native-") as temporary:
        sandbox=Path(temporary);r=sandbox/"original_R.js";b=sandbox/"original_B.py"
        r.write_bytes(inputs[str(R.relative_to(ROOT))]);b.write_bytes(inputs[str(B.relative_to(ROOT))])
        node=execute("node-version",["node","--version"]);require(node.returncode==0,"NODE_UNAVAILABLE")
        emitted=sandbox/"emitted";emitted.mkdir()
        native=execute("original-R-emit",["node",str(r),"--emit"],emitted);require(native.returncode==0,"NATIVE_R_FAIL")
        for path in (CSV_PATH,JSON_PATH):
            raw=(emitted/path.name).read_bytes();require(raw==inputs[str(path.relative_to(ROOT))],"NATIVE_BYTE_MISMATCH")
            identity[path.name]={"bytes":len(raw),"sha256":sha(raw),"byte_equal":True}
        regenerated=execute("audit-emitted",python+[str(HERE/"audit.py"),str(emitted/CSV_PATH.name),str(emitted/JSON_PATH.name)])
        require(regenerated.returncode==0 and json.loads(regenerated.stdout)==proof,"EMITTED_CONTRACT_FAIL")
        b_test=execute("original-B-test",python+[str(b),"--test"]);require(b_test.returncode==0 and json.loads(b_test.stdout)=={"tests":9,"status":"PASS","worlds":6},"ORIGINAL_B_SELFTEST")
        b_run=execute("original-B-worlds",python+[str(b)]);require(b_run.returncode==0,"ORIGINAL_B_FAIL")
        expected={(r["distribution"],r["training_episodes"]):r for r in expected_tree()["worlds"]};b_fields=0
        for row in json.loads(b_run.stdout):
            target=expected[(row["distribution"],row["training_episodes"])]
            require(all(type(value) is type(target[key]) and value==target[key] for key,value in row.items()),"ORIGINAL_B_VS_DP")
            b_fields+=sum(type(v) is str and k!="distribution" for k,v in row.items())
        require(b_fields==48,"B_COMPARISON_FIELD_COUNT")
        for name,edits in EDITS.items():
            folder=sandbox/name;folder.mkdir();code=inputs[str(R.relative_to(ROOT))].decode()
            for old,new in edits:
                require(code.count(old)==1,"MUTATION_PREIMAGE");code=code.replace(old,new)
            script=folder/"mutant.js";script.write_text(code)
            source=execute("source-"+name,["node",str(script),"--emit"],folder)
            if name=="single_route_tie_control":
                require(source.returncode==1 and b"Error: route mismatch" in source.stderr,"OLD_CONTROL_FAILED")
                mutants.append({"name":name,"original_exit":1,"old_correct_rejection":True,"new_artifact_gate":"NOT_RUN_SOURCE_DID_NOT_EMIT"})
                continue
            require(source.returncode==0,"MUTANT_NOT_FALSE_ACCEPTED")
            doc=json.loads((folder/JSON_PATH.name).read_bytes())
            require(len(doc["mutation_tests"])==6 and all(x["rejected"] is True for x in doc["mutation_tests"]),"REPORTED_MUTATION_FLAGS_CHANGED")
            require((folder/CSV_PATH.name).read_bytes()==inputs[str(CSV_PATH.relative_to(ROOT))],"MUTANT_CHANGED_LEDGER")
            checked=execute("new-"+name,python+[str(HERE/"audit.py"),str(folder/CSV_PATH.name),str(folder/JSON_PATH.name)])
            rejected=json.loads(checked.stdout);require(checked.returncode==2 and rejected["status"]=="REJECTED","MUTANT_UNDETECTED")
            (output/(name+"-mutant-results.json")).write_bytes((folder/JSON_PATH.name).read_bytes())
            mutants.append({"name":name,"original_exit":0,"reported_negative_controls_all_true":True,
                            "new_exit":2,"reason":rejected["reason"],"source_sha256":sha(code.encode()),"edits":edits,
                            "uniform_m1":doc["worlds"][0]})
        for name in ("duplicate_source","weight_999","E2_bool","duplicate_JSON_key"):
            table=list(csv.reader(io.StringIO(inputs[str(CSV_PATH.relative_to(ROOT))].decode())))
            doc=json.loads(inputs[str(JSON_PATH.relative_to(ROOT))])
            if name=="duplicate_source":table[-1]=table[1][:]
            elif name=="weight_999":table[1][2]="999"
            elif name=="E2_bool":doc["new_E2"]=False
            stream=io.StringIO(newline="");csv.writer(stream,lineterminator="\n").writerows(table)
            raw=json.dumps(doc)
            if name=="duplicate_JSON_key":raw=raw[:-1]+',"new_E2":0}'
            a,j=sandbox/"bad.csv",sandbox/"bad.json";a.write_text(stream.getvalue());j.write_text(raw)
            result=execute(name,python+[str(HERE/"audit.py"),str(a),str(j)])
            failure=json.loads(result.stdout);require(result.returncode==2 and failure["status"]=="REJECTED","BAD_RECEIPT_ACCEPTED")
            controls.append({"name":name,"exit_code":2,"reason":failure["reason"],"csv_sha256":sha(a.read_bytes()),"json_sha256":sha(j.read_bytes())})
    parity=source_parity(inputs);_,after=capture();require(before==after,"SOURCE_CHANGED_DURING_REPLAY")
    result={"status":"PASS_INDEPENDENT_HOLDOUT_CONTRACT_AND_SOURCE_MUTANTS","utc":datetime.now(timezone.utc).isoformat(),
            "source_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
            "python":sys.version,"optimized":bool(sys.flags.optimize),"node":node.stdout.decode().strip(),
            "new_unittest_methods":12,"result_leaf_checks":136,"world_fraction_fields":60,
            "native_identity":identity,"source_mutants":mutants,"persisted_bad_controls":controls,
            "source_parity":parity,"old_B_fraction_fields_checked":48,"old_B_selfreported_tests":9,
            "old_B_asserts_under_O":"DISABLED_NOT_UNITTEST_EXECUTIONS","sources_before_after_equal":True,"sources":before,
            "original_numerical_discrepancy_found":False,"original_production_adoption":"NOT_RUN",
            "full_repository_tests":"NOT_RUN","original_R289_test_suite":"NOT_RUN","other_platforms":"NOT_RUN","CI":"NOT_RUN",
            "new_human_scores":0,"new_E2_E3":0,"external_team_replications":0,"formal_queue_closures":0,
            "R073":"FROZEN_UNCHANGED","PESEN_v0.1":"FROZEN_UNCHANGED"}
    (output/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","optimized","new_unittest_methods","native_identity","source_parity","old_B_fraction_fields_checked")},indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",type=Path,required=True)
    run(parser.parse_args().output.resolve())
