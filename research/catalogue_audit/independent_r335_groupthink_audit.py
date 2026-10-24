"""R335 independent no-import replay with two tamper rejection controls."""
import csv
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R335"
SOURCE=ROOT/"R335_ALL_384_ARTIFICIAL_GROUP_ATOMS.csv"
RESULT=ROOT/"R335_EXACT_128_CONDITIONS.json"

def expected():
    rows,conditions=[],[]
    for truth in range(2):
        for bits in range(8):
            s1=(bits>>2)&1
            s2=(bits>>1)&1
            s3=bits&1
            for leader in range(2):
                for pressure in range(2):
                    for audit in range(2):
                        majority=1 if s1+s2+s3>1 else 0
                        pressured=leader if pressure else majority
                        audited=truth if pressure*audit else pressured
                        reports=(s1,s2,s3) if not pressure else (leader,leader,leader)
                        for name,public,decision in [
                            ("OPEN",(s1,s2,s3),majority),
                            ("PRESSURE",reports,pressured),
                            ("AUDIT",reports,audited)]:
                            rows.append([name,truth,s1,s2,s3,leader,pressure,audit,*public,decision,int(decision==truth)])
                        private_unanimous=int(s1==s2 and s2==s3)
                        public_unanimous=int(pressure==1 or private_unanimous)
                        conditions.append(dict(truth=truth,s1=s1,s2=s2,s3=s3,leader=leader,pressure=pressure,audit=audit,
                            open_decision=majority,pressure_decision=pressured,audit_decision=audited,
                            open_correct=int(majority==truth),pressure_correct=int(pressured==truth),
                            audit_correct=int(audited==truth),open_unanimous=private_unanimous,
                            pressure_unanimous=public_unanimous,audit_unanimous=public_unanimous))
    assert len(rows)==384 and len(conditions)==128
    checks=dict(rows=len(rows),conditions=len(conditions),
        pressure_unanimous=sum(w["pressure_unanimous"] for w in conditions if w["pressure"]==1),
        concealed_private_dissent=sum(w["pressure"]==1 and not w["open_unanimous"] for w in conditions),
        pressure0_matches_open=sum(w["pressure"]==0 and w["pressure_decision"]==w["open_decision"] for w in conditions),
        pressure_overrides_majority=sum(w["pressure"]==1 and w["pressure_decision"]!=w["open_decision"] for w in conditions),
        audit_changes_pressure=sum(w["audit_decision"]!=w["pressure_decision"] for w in conditions),
        correct_open=sum(w["open_correct"] for w in conditions),
        correct_pressure=sum(w["pressure_correct"] for w in conditions),
        correct_audit=sum(w["audit_correct"] for w in conditions))
    buf=io.StringIO(newline="")
    writer=csv.writer(buf,lineterminator="\r\n")
    writer.writerow(["policy","truth","s1","s2","s3","leader","pressure","audit","public1","public2","public3","decision","correct"])
    writer.writerows(rows)
    return buf.getvalue().encode(),(json.dumps(dict(schema="R335_frozen_public_unanimity_v1",conditions=conditions,checks=checks),indent=2,ensure_ascii=False)+"\n").encode(),checks

def validate(cb,jb):
    c,j,checks=expected()
    assert cb==c,"CSV tampering detected"
    assert jb==j,"JSON tampering detected"
    assert checks==dict(rows=384,conditions=128,pressure_unanimous=64,concealed_private_dissent=48,
        pressure0_matches_open=64,pressure_overrides_majority=32,audit_changes_pressure=16,
        correct_open=64,correct_pressure=64,correct_audit=80)

if __name__=="__main__":
    cb,jb=SOURCE.read_bytes(),RESULT.read_bytes()
    validate(cb,jb)
    bad=cb.replace(b"OPEN,0,0,0,0,0,0,0,0,0,0,0,1",b"OPEN,0,0,0,0,0,0,0,0,0,0,1,1",1)
    assert bad!=cb
    try:
        validate(bad,jb)
        raise RuntimeError("CSV tamper accepted")
    except AssertionError as e:
        assert "CSV tampering" in str(e)
    obj=json.loads(jb)
    obj["conditions"][0]["audit_correct"]=1-obj["conditions"][0]["audit_correct"]
    badj=(json.dumps(obj,indent=2,ensure_ascii=False)+"\n").encode()
    assert badj!=jb
    try:
        validate(cb,badj)
        raise RuntimeError("JSON tamper accepted")
    except AssertionError as e:
        assert "JSON tampering" in str(e)
    print("R335 INDEPENDENT_PASS 384 atoms 128 conditions six falsifiers two tamper rejections")
