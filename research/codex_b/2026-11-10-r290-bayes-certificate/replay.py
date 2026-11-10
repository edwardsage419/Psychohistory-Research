#!/usr/bin/env python3
"""Offline S86 Bayes-contract replay. Output must be a NEW directory."""
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

from certificate import DGP,derive,require
from test_certificate import CSV_PATH,JSON_PATH,bad_cases

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
R=ROOT/"research/validation/r290_s86_finite_likelihood_20261030.py"
B=ROOT/"research/evidence_audit/b_r290_s86_independent_binomial_oracle_20261030.py"
LEDGER=ROOT/"research/evidence_audit/b_r290_s86_source_ledger_gate_20261030.py"
ORIGINAL_CSV="research/R290/R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv"
ORIGINAL_JSON="research/R290/R290_EXACT_SIGNAL_DETECTION_RESULTS.json"
PIN_SHA="8f1ca36b6f77672f2c1fdb610ec3d96d800203a6e9bd368900da558892812675"


def sha(raw):return hashlib.sha256(raw).hexdigest()


def capture():
    raw=(HERE/"pins.json").read_bytes();require(sha(raw)==PIN_SHA,"PIN_MANIFEST_CHANGED")
    pins=json.loads(raw);inputs={};fingerprints={}
    for name,pinned in pins.items():
        data=(ROOT/name).read_bytes();blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        tracked=subprocess.check_output(["git","rev-parse","HEAD:"+name],cwd=ROOT,text=True).strip()
        require(blob==pinned==tracked,"PINNED_INPUT_CHANGED:"+name)
        inputs[name]=data;fingerprints[name]={"bytes":len(data),"sha256":sha(data),"git_blob":blob}
    for p in [HERE/"pins.json",*sorted(HERE.glob("*.py"))]:
        raw=p.read_bytes();fingerprints[str(p.relative_to(ROOT))]={"bytes":len(raw),"sha256":sha(raw)}
    return inputs,fingerprints


def original_parity(inputs,certificates):
    rows=list(csv.DictReader(io.StringIO(inputs[ORIGINAL_CSV].decode())))
    require(len(rows)==120,"ORIGINAL_CELL_COVERAGE")
    costs={w:[F(0)]*32 for w in certificates};mass={w:F(0) for w in certificates};seen=set()
    for row in rows:
        name,world=row["dgp"],row["world"];pi=F(row["signal_prior"])
        fp,fn=int(row["cost_false_positive"]),int(row["cost_false_negative"])
        truth,x=int(row["truth"]),int(row["evidence_x"])
        require(world==f"{name}_PI{pi.numerator}of{pi.denominator}_FP{fp}_FN{fn}" and world in certificates and truth in (0,1) and x in range(5),"ORIGINAL_CELL_ID")
        key=world,truth,x;require(key not in seen,"ORIGINAL_CELL_DUPLICATE");seen.add(key)
        vector=DGP[name][truth];q=F(vector[x],DGP[name][2]);joint=q*(pi if truth else 1-pi)
        require(F(row["conditional_probability"])==q and F(row["joint_source_probability"])==joint,"ORIGINAL_CELL_MASS")
        mass[world]+=joint
        for mask in range(32):costs[world][mask]+=joint*(fp if truth==0 and mask&(1<<x) else fn if truth==1 and not mask&(1<<x) else 0)
    for world,proof in certificates.items():
        require(mass[world]==1 and costs[world]==[F(n,proof["denominator"]) for n in proof["loss_numerators"]],"ORIGINAL_32_RULE_MATRIX")
    doc=json.loads(inputs[ORIGINAL_JSON]);checks=0
    require(len(doc["results"])==12,"ORIGINAL_BASELINE_COVERAGE")
    for row in doc["results"]:
        p=certificates[row["world"]];d=p["denominator"];t=p["best_cutoff_t"]
        expected={"bayes_risk":F(p["minimum_numerator"],d),"exact_independent_cell_minimum":F(p["minimum_numerator"],d),
                  "best_single_cutoff_risk":F(p["cutoff_numerators"][t],d),"fixed_t3_risk":F(p["cutoff_numerators"][3],d)}
        require(all(F(row[k])==v for k,v in expected.items()) and row["smallest_best_single_cutoff"]==t,"ORIGINAL_BASELINE")
        checks+=5
        require(len(row["roc_thresholds"])==6,"ORIGINAL_CUTOFF_COVERAGE")
        for cutoff in row["roc_thresholds"]:
            require(F(cutoff["weighted_risk"])==F(p["cutoff_numerators"][cutoff["t"]],d),"ORIGINAL_CUTOFF_RISK");checks+=1
    return {"source_cells":len(seen),"rule_loss_values":384,"baseline_fields":checks}


def run(output):
    output.mkdir(parents=True,exist_ok=False);inputs,before=capture();commands=[]
    python=[sys.executable,"-B"]+(["-O"] if sys.flags.optimize else [])
    # Legacy JSON B uses asserts and its limitation is already documented. Keep
    # all its original guards active, without propagating parent optimization.
    legacy=[sys.executable,"-I","-B"]

    def execute(tag,args):
        child=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=60);streams={}
        for suffix,raw in (("stdout",child.stdout),("stderr",child.stderr)):
            name=tag+"."+suffix
            if raw:(output/name).write_bytes(raw)
            streams[suffix]={"bytes":len(raw),"sha256":sha(raw),"file":name if raw else None}
        commands.append({"tag":tag,"argv":args,"cwd":str(ROOT),"exit_code":child.returncode,"streams":streams})
        (output/"commands.json").write_text(json.dumps(commands,indent=2)+"\n");return child

    tests=execute("new-12-tests",python+["-m","unittest","discover","-s",str(HERE),"-p","test_certificate.py","-v"])
    require(tests.returncode==0 and re.search(rb"Ran 12 tests in",tests.stderr) is not None,"NEW_TESTS_FAIL")
    archive=execute("new-audit-archive",python+[str(HERE/"audit.py"),str(CSV_PATH),str(JSON_PATH)])
    require(archive.returncode==0,"ARCHIVE_AUDIT_FAIL");proof=json.loads(archive.stdout)
    negatives=[]
    with tempfile.TemporaryDirectory(prefix="codex-b-r290-native-") as temporary:
        folder=Path(temporary);r,b,ledger=folder/"original_R.py",folder/"original_B.py",folder/"original_ledger_B.py"
        for path,original in ((r,R),(b,B),(ledger,LEDGER)):path.write_bytes(inputs[str(original.relative_to(ROOT))])
        original_tests=execute("original-4-tests",python+[str(r),"--test"])
        require(original_tests.returncode==0 and re.search(rb"Ran 4 tests in",original_tests.stderr) is not None,"ORIGINAL_TESTS_FAIL")
        emit=execute("original-R-emit",python+[str(r),"--emit"])
        require(emit.returncode==0 and emit.stdout==inputs[str(JSON_PATH.relative_to(ROOT))],"NATIVE_JSON_BYTE_MISMATCH")
        regenerated=folder/"emitted.json";regenerated.write_bytes(emit.stdout)
        again=execute("new-audit-emitted",python+[str(HERE/"audit.py"),str(CSV_PATH),str(regenerated)])
        require(again.returncode==0 and json.loads(again.stdout)==proof,"EMITTED_AUDIT_MISMATCH")
        old=execute("old-B-good-normal",legacy+[str(b),str(JSON_PATH)])
        require(old.returncode==0 and json.loads(old.stdout)["world_sample_combinations"]==24 and len(json.loads(old.stdout)["rejected_mutations"])==7,"ORIGINAL_B_FAIL")
        old_ledger=execute("old-ledger-good-normal",legacy+[str(ledger),str(CSV_PATH)])
        require(old_ledger.returncode==0 and json.loads(old_ledger.stdout)["verified_sources"]==1950 and len(json.loads(old_ledger.stdout)["rejected_mutations"])==5,"ORIGINAL_LEDGER_FAIL")
        for name,csv_raw,json_raw in bad_cases():
            a,j=folder/"bad.csv",folder/"bad.json";a.write_bytes(csv_raw);j.write_bytes(json_raw)
            source_control=name=="source_mass";correct_rejection=name in ("risk_zero","regret_negative","source_mass")
            child=execute("old-"+name,legacy+([str(ledger),str(a)] if source_control else [str(b),str(j)]))
            if correct_rejection:
                marker={"risk_zero":b"independent binomial risk mismatch","regret_negative":b"regret or oracle","source_mass":b"source mass mismatch"}[name]
                require(child.returncode==1 and marker in child.stderr,"OLD_CORRECT_CONTROL_CHANGED")
            else:require(child.returncode==0 and json.loads(child.stdout)["status"]=="PASS","OLD_FALSE_ACCEPT_NOT_REPRODUCED")
            new=execute("new-"+name,python+[str(HERE/"audit.py"),str(a),str(j)])
            failure=json.loads(new.stdout);require(new.returncode==2 and failure["status"]=="REJECTED","NEW_BAD_ARTIFACT_ACCEPTED")
            negatives.append({"case":name,"old_exit":child.returncode,"old_false_accept":not correct_rejection,
                              "old_gate":"source_ledger" if source_control else "binomial_result",
                              "new_exit":new.returncode,"reason":failure["reason"],"csv_sha256":sha(csv_raw),"json_sha256":sha(json_raw)})
        mutant=folder/"mutant";mutant.mkdir()
        for filename in ("certificate.py","audit.py","test_certificate.py"):(mutant/filename).write_bytes((HERE/filename).read_bytes())
        p=mutant/"certificate.py";source=p.read_text();old="minimum=min(losses)";new="minimum=max(losses)"
        require(source.count(old)==1,"MINIMUM_MUTATION_PREIMAGE");p.write_text(source.replace(old,new))
        code='import sys,unittest;sys.path.insert(0,sys.argv[1]);from test_certificate import CertificateTests;r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([CertificateTests("test_first_world_minimum_and_witnesses")]));sys.exit(0 if r.wasSuccessful() else 1)'
        bad=execute("optimizer-max-negative",python+["-c",code,str(mutant)])
        require(bad.returncode==1 and b"FAILED (failures=1)" in bad.stderr and b"ERROR:" not in bad.stderr,"WRONG_OPTIMIZER_NOT_DETECTED")
        mutant_sha=sha(p.read_bytes())
    parity=original_parity(inputs,proof["loss_certificates"]);_,after=capture();require(before==after,"SOURCE_CHANGED_DURING_REPLAY")
    result={"status":"PASS_COMPLETE_BAYES_RULE_LAW_AND_FALSE_OPTIMALITY_REPLAY","utc":datetime.now(timezone.utc).isoformat(),
            "source_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"python":sys.version,"optimized":bool(sys.flags.optimize),
            "positive_unittest_methods":{"original":4,"new":12},"result_leaf_checks":273,"scientific_fraction_fields":144,
            "native_JSON":{"bytes":len(emit.stdout),"sha256":sha(emit.stdout),"byte_equal":True},
            "native_training_CSV_emitter":"NOT_ARCHIVED_NOT_CLAIMED","original_parity":parity,
            "old_false_accepts":5,"old_correct_rejections":3,"new_bad_inputs_rejected":8,"negative_controls":negatives,
            "legacy_B_mode":"NORMAL_ISOLATED_I_B_NO_O_EVEN_IF_PARENT_OPTIMIZED","legacy_12_negative_controls_run":True,
            "legacy_class_swap_control":"RISK_ZERO_NOT_ACTUAL_CLASS_COUNT_SWAP","own_optimizer_mutant":{"exit_code":1,"sha256":mutant_sha},
            "sources_before_after_equal":True,"sources":before,"original_numerical_discrepancy_found":False,
            "original_R290_full_suite":"NOT_RUN","full_repository_tests":"NOT_RUN","other_platforms":"NOT_RUN","production_adoption":"NOT_RUN","CI":"NOT_RUN",
            "new_human_scores":0,"new_E2_E3":0,"external_team_replications":0,"formal_queue_closures":0,"R073":"FROZEN_UNCHANGED","PESEN_v0.1":"FROZEN_UNCHANGED"}
    (output/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","optimized","positive_unittest_methods","native_JSON","old_false_accepts","new_bad_inputs_rejected","original_parity")},indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--output",type=Path,required=True);run(p.parse_args().output.resolve())
