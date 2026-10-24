"""R335 constructed three-person public unanimity and information gate replay."""
import argparse
import csv
import io
import json
import unittest
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"R335_ALL_384_ARTIFICIAL_GROUP_ATOMS.csv"
RESULT=ROOT/"R335_EXACT_128_CONDITIONS.json"
HEADER=["policy","truth","s1","s2","s3","leader","pressure","audit","public1","public2","public3","decision","correct"]
EXPECTED={"rows":384,"conditions":128,"pressure_unanimous":64,"concealed_private_dissent":48,
    "pressure0_matches_open":64,"pressure_overrides_majority":32,"audit_changes_pressure":16,
    "correct_open":64,"correct_pressure":64,"correct_audit":80}

def build():
    rows,worlds=[],[]
    checks={k:0 for k in EXPECTED}
    for truth,s1,s2,s3,leader,pressure,audit in product((0,1),repeat=7):
        majority=int(s1+s2+s3>=2)
        public_open=(s1,s2,s3)
        public_pressure=(leader,leader,leader) if pressure else public_open
        chosen_pressure=leader if pressure else majority
        chosen_audit=truth if pressure and audit else chosen_pressure
        for name,public,decision in (
            ("OPEN",public_open,majority),
            ("PRESSURE",public_pressure,chosen_pressure),
            ("AUDIT",public_pressure,chosen_audit)):
            rows.append([name,truth,s1,s2,s3,leader,pressure,audit,*public,decision,int(decision==truth)])
        u_open=int(s1==s2==s3)
        u_pressure=int(pressure==1 or u_open)
        worlds.append(dict(truth=truth,s1=s1,s2=s2,s3=s3,leader=leader,pressure=pressure,audit=audit,
            open_decision=majority,pressure_decision=chosen_pressure,audit_decision=chosen_audit,
            open_correct=int(majority==truth),pressure_correct=int(chosen_pressure==truth),
            audit_correct=int(chosen_audit==truth),open_unanimous=u_open,
            pressure_unanimous=u_pressure,audit_unanimous=u_pressure))
        checks["conditions"]+=1
        checks["rows"]+=3
        checks["pressure_unanimous"]+=int(pressure==1)
        checks["concealed_private_dissent"]+=int(pressure==1 and not u_open)
        checks["pressure0_matches_open"]+=int(pressure==0)
        checks["pressure_overrides_majority"]+=int(pressure==1 and chosen_pressure!=majority)
        checks["audit_changes_pressure"]+=int(chosen_audit!=chosen_pressure)
        checks["correct_open"]+=int(majority==truth)
        checks["correct_pressure"]+=int(chosen_pressure==truth)
        checks["correct_audit"]+=int(chosen_audit==truth)
    return rows,dict(schema="R335_frozen_public_unanimity_v1",conditions=worlds,checks=checks)

def render():
    rows,obj=build()
    buf=io.StringIO(newline="")
    writer=csv.writer(buf,lineterminator="\r\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buf.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=False)+"\n").encode()

def audit():
    cb,jb=render()
    assert SOURCE.read_bytes()==cb,"CSV byte replay mismatch"
    assert RESULT.read_bytes()==jb,"JSON byte replay mismatch"
    rows,obj=build()
    assert obj["checks"]==EXPECTED
    assert len(rows)==384 and len(obj["conditions"])==128
    assert all(isinstance(v,int) and v in (0,1) for row in rows for v in row[1:])

class Tests(unittest.TestCase):
    def test_counts(self): self.assertEqual((len(build()[0]),len(build()[1]["conditions"])),(384,128))
    def test_falsifiers(self): self.assertEqual(build()[1]["checks"],EXPECTED)
    def test_binary(self): self.assertTrue(all(x in (0,1) for r in build()[0] for x in r[1:]))
    def test_oracle_only_under_gate(self):
        for w in build()[1]["conditions"]:
            if not(w["pressure"] and w["audit"]):
                self.assertEqual(w["audit_decision"],w["pressure_decision"])
    def test_byte_replay(self): audit()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    args=parser.parse_args()
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not result.wasSuccessful():raise SystemExit(1)
    if args.audit:
        audit()
        print("R335 PRODUCTION_REPLAY_PASS 384 artificial atoms 128 conditions")
