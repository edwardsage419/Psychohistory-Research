#!/usr/bin/env python3
"""Offline S78 native replay, paired-field false-accept reproduction and GF2 gate."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from algebra import require
from audit import B_PATH
from test_certificate import CSV_PATH, JSON_PATH, bad_cases, write_case

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R = ROOT/"research/validation/r282_s78_schedule_observability_20261030.js"
INVERSE = ROOT/"research/evidence_audit/b_r282_s78_inverse_schedule_oracle_20261030.js"
PIN_SHA = "556f72b24cedb66adeee5147b7e6b09da59019161def42ab4d733277e5989954"


def sha(raw): return hashlib.sha256(raw).hexdigest()


def capture():
    raw = (HERE/"pins.json").read_bytes(); require(sha(raw) == PIN_SHA,"PIN_MANIFEST_CHANGED")
    pins = json.loads(raw); inputs,found = {},{}
    for name,pinned in pins.items():
        data = (ROOT/name).read_bytes()
        blob = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        tracked = subprocess.check_output(["git","rev-parse","HEAD:"+name],cwd=ROOT,text=True).strip()
        require(blob == pinned == tracked,"PINNED_INPUT_CHANGED:"+name)
        inputs[name] = data;found[name] = {"bytes":len(data),"sha256":sha(data),"git_blob":blob}
    for path in [HERE/"pins.json",*sorted(HERE.glob("*.py"))]:
        data = path.read_bytes();found[str(path.relative_to(ROOT))] = {"bytes":len(data),"sha256":sha(data)}
    return inputs,found


def run(output):
    output.mkdir(parents=True,exist_ok=False)
    inputs,before = capture();commands=[]
    python=[sys.executable,"-B"]+(["-O"] if sys.flags.optimize else [])

    def execute(tag,args):
        child=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=60)
        streams={}
        for suffix,raw in (("stdout",child.stdout),("stderr",child.stderr)):
            name=tag+"."+suffix
            if raw:(output/name).write_bytes(raw)
            streams[suffix]={"bytes":len(raw),"sha256":sha(raw),"file":name if raw else None}
        commands.append({"tag":tag,"argv":args,"cwd":str(ROOT),"exit_code":child.returncode,"streams":streams})
        (output/"commands.json").write_text(json.dumps(commands,indent=2)+"\n")
        return child

    tests=execute("new-12-tests",python+["-m","unittest","discover","-s",str(HERE),"-p","test_certificate.py","-v"])
    require(tests.returncode==0 and re.search(rb"Ran 12 tests in",tests.stderr) is not None,"NEW_TESTS_FAIL")
    archive=execute("new-audit-archive",python+[str(HERE/"audit.py"),str(CSV_PATH),str(JSON_PATH)])
    require(archive.returncode==0,"NEW_ARCHIVE_FAIL");proof=json.loads(archive.stdout)
    negatives=[];identities={}
    with tempfile.TemporaryDirectory(prefix="codex-b-r282-native-") as temporary:
        sandbox=Path(temporary);r,b,inverse=sandbox/"original_R.js",sandbox/"original_B.js",sandbox/"original_inverse.js"
        for path,source in ((r,R),(b,B_PATH),(inverse,INVERSE)):path.write_bytes(inputs[str(source.relative_to(ROOT))])
        node_version=execute("node-version",["node","--version"]);require(node_version.returncode==0,"NODE_UNAVAILABLE")
        native=execute("original-R-emit",["node",str(r),str(sandbox/"emitted")]);require(native.returncode==0,"NATIVE_R_FAIL")
        for path in (CSV_PATH,JSON_PATH):
            raw=(sandbox/"emitted"/path.name).read_bytes();old=inputs[str(path.relative_to(ROOT))]
            require(raw==old,"NATIVE_BYTE_MISMATCH:"+path.name)
            identities[path.name]={"bytes":len(raw),"sha256":sha(raw),"byte_equal":True}
        for label,csv_path,json_path in (("archive",CSV_PATH,JSON_PATH),("emitted",sandbox/"emitted"/CSV_PATH.name,sandbox/"emitted"/JSON_PATH.name)):
            old=execute("original-B-"+label,["node",str(b),str(csv_path),str(json_path)])
            require(old.returncode==0 and json.loads(old.stdout)==proof["original_B"],"NATIVE_B_FAIL")
            inv=execute("original-inverse-"+label,["node",str(inverse),str(json_path)])
            require(inv.returncode==0 and len(json.loads(inv.stdout))==4,"NATIVE_INVERSE_FAIL")
        emitted=execute("new-audit-emitted",python+[str(HERE/"audit.py"),str(sandbox/"emitted"/CSV_PATH.name),str(sandbox/"emitted"/JSON_PATH.name)])
        require(emitted.returncode==0 and json.loads(emitted.stdout)==proof,"EMITTED_PROOF_MISMATCH")
        for name,csv_raw,json_raw in bad_cases():
            case=sandbox/name;case.mkdir();a,j=write_case(case,csv_raw,json_raw)
            old=execute("old-"+name,["node",str(b),str(a),str(j)])
            control=name in ("CSV_transition","TV_corruption")
            if control:
                expected=b"Error: INVERSE_TRANSITION" if name=="CSV_transition" else b"Error: INVERSE_ORACLE_MISMATCH"
                require(old.returncode==1 and expected in old.stderr,"OLD_CONTROL_CHANGED")
            else: require(old.returncode==0 and json.loads(old.stdout)==proof["original_B"],"OLD_FALSE_ACCEPT_NOT_REPRODUCED")
            new=execute("new-"+name,python+[str(HERE/"audit.py"),str(a),str(j)])
            result=json.loads(new.stdout)
            require(new.returncode==2 and result["status"]=="REJECTED","NEW_MUTATION_ACCEPTED:"+name)
            negatives.append({"case":name,"old_exit":old.returncode,"old_false_accept":not control,
                              "new_exit":new.returncode,"new_reason":result["reason"],
                              "csv_sha256":sha(csv_raw),"json_sha256":sha(json_raw)})
        # Wrong rank cap destroys the exact t2 count without touching model/data.
        mutant=sandbox/"mutant";mutant.mkdir()
        for name in ("algebra.py","audit.py","test_certificate.py"):(mutant/name).write_bytes((HERE/name).read_bytes())
        path=mutant/"algebra.py";source=path.read_text();old="return len(basis)";new="return min(1, len(basis))"
        require(source.count(old)==1,"RANK_MUTATION_PREIMAGE");path.write_text(source.replace(old,new))
        code='import sys,unittest;sys.path.insert(0,sys.argv[1]);from test_certificate import AlgebraTests;r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([AlgebraTests("test_exact_count_formula")]));sys.exit(0 if r.wasSuccessful() else 1)'
        wrong=execute("rank-cap-negative",python+["-c",code,str(mutant)])
        require(wrong.returncode==1 and b"FAILED (failures=1)" in wrong.stderr and b"ERROR:" not in wrong.stderr,"RANK_MUTANT_NOT_DETECTED")
        mutant_sha=sha(path.read_bytes())
    _,after=capture();require(before==after,"SOURCE_CHANGED_DURING_REPLAY")
    result={"status":"PASS_GF2_PAIRING_AND_FALSE_ACCEPT_REPLAY","utc":datetime.now(timezone.utc).isoformat(),
            "source_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
            "python":sys.version,"optimized":bool(sys.flags.optimize),"node":node_version.stdout.decode().strip(),
            "new_unittest_methods":12,"source_rows":192,"symbolic_output_bit_checks":768,"paired_integer_fields":4,
            "native_identity":identities,"old_false_accepts":sum(x["old_false_accept"] for x in negatives),
            "old_correct_rejections":2,"new_bad_inputs_rejected":len(negatives),"negative_controls":negatives,
            "own_rank_mutant":{"exit_code":1,"sha256":mutant_sha,"wrong":"rank capped at1"},
            "sources_before_after_equal":True,"sources":before,
            "original_scientific_numeric_discrepancy_found":False,"original_gate_adoption":"NOT_RUN",
            "full_repository_tests":"NOT_RUN","other_platforms":"NOT_RUN","CI":"NOT_RUN",
            "new_human_scores":0,"new_E2_E3":0,"external_team_replications":0,"formal_queue_closures":0,
            "R073":"FROZEN_UNCHANGED","PESEN_v0.1":"FROZEN_UNCHANGED"}
    (output/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","optimized","new_unittest_methods","native_identity","old_false_accepts","new_bad_inputs_rejected")},indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",type=Path,required=True)
    run(parser.parse_args().output.resolve())
