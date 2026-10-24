"""R336 finite artificial inoculation and topic-specific support replay."""
import argparse
import csv
import io
import json
import unittest
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"R336_ALL_96_ARTIFICIAL_ATTACK_ATOMS.csv"
RESULT=ROOT/"R336_EXACT_48_CONDITIONS.json"
HEADER=["mode","weak","refutation","same_topic","attack_intensity","policy","defense","baseline_post","post_belief","retained_gain"]
EXPECTED={"worlds":48,"rows":96,"same_topic_agreement":24,"novel_transfer_advantage":4,"no_weak_equal_baseline":24,"no_refutation_equal_baseline":24}
def build():
    rows,conditions=[],[]
    checks={key:0 for key in EXPECTED}
    for m,w,r,s,a in product((0,1,2),(0,1),(0,1),(0,1),(1,2)):
        d=0 if not m or not w or not r else ((2 if m==1 else 3) if s else (1 if m==1 else 2))
        c=d if s else 0
        b=6-2*a
        t=6-max(0,2*a-d)
        u=6-max(0,2*a-c)
        conditions.append(dict(mode=m,weak=w,refutation=r,same_topic=s,attack_intensity=a,baseline_post=b,transfer_post=t,support_post=u,transfer_defense=d,support_defense=c))
        rows.append([m,w,r,s,a,"INOCULATION_TRANSFER",d,b,t,t-b])
        rows.append([m,w,r,s,a,"TOPIC_SPECIFIC_SUPPORT",c,b,u,u-b])
        checks["worlds"]+=1
        checks["rows"]+=2
        checks["same_topic_agreement"]+=int(bool(s) and t==u)
        checks["novel_transfer_advantage"]+=int(not s and t>u)
        checks["no_weak_equal_baseline"]+=int(not w and t==b and u==b)
        checks["no_refutation_equal_baseline"]+=int(not r and t==b and u==b)
    return rows,{"schema":"R336_frozen_inoculation_transfer_v1","conditions":conditions,"checks":checks}
def render():
    rows,obj=build()
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return stream.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=True)+"\n").encode()
def audit():
    cb,jb=render()
    assert SOURCE.read_bytes()==cb,"CSV byte replay mismatch"
    assert RESULT.read_bytes()==jb,"JSON byte replay mismatch"
    assert build()[1]["checks"]==EXPECTED,"frozen checks mismatch"
class Tests(unittest.TestCase):
    def test_counts(self): self.assertEqual(build()[1]["checks"],EXPECTED)
    def test_complete_worlds(self):
        c=build()[1]["conditions"]
        self.assertEqual(len({(x["mode"],x["weak"],x["refutation"],x["same_topic"],x["attack_intensity"]) for x in c}),48)
    def test_same_topic(self): self.assertTrue(all(x["transfer_post"]==x["support_post"] for x in build()[1]["conditions"] if x["same_topic"]))
    def test_negative_controls(self): self.assertTrue(all(x["transfer_post"]==x["baseline_post"] and x["support_post"]==x["baseline_post"] for x in build()[1]["conditions"] if not x["weak"] or not x["refutation"]))
    def test_saturation(self):
        c=build()[1]["conditions"]
        lookup=lambda m,a:next(x["transfer_post"] for x in c if x["mode"]==m and x["weak"]==x["refutation"]==x["same_topic"]==1 and x["attack_intensity"]==a)
        self.assertEqual((lookup(2,2),lookup(1,2),lookup(2,1),lookup(1,1)),(5,4,6,6))
    def test_byte_replay(self): audit()
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:
        outcome=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not outcome.wasSuccessful():raise SystemExit(1)
    if args.audit:
        audit()
        print("R336 PRODUCTION_REPLAY_PASS 96 artificial atoms 48 worlds")
