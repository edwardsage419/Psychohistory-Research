"""R333: frozen artificial triadic feedback, deterministic Python replay."""
import argparse, csv, io, json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CSV = ROOT / "R333_ALL_160_ARTIFICIAL_TRIADIC_STATES.csv"
RESULTS = ROOT / "R333_EXACT_32_TRIADIC_WORLDS.json"
HEADER = ["mechanism","initial_p","initial_b","initial_e","do_b1","time","p","b","e"]

def trace(model, p, b, e, intervention):
    seq = [(p,b,e)]
    for t in range(1,5):
        p,b,e = (p^e), (intervention if t==1 else p^b), ((b^e) if model=="cyclic" else e)
        seq.append((p,b,e))
    return seq

def generate():
    rows, worlds, paths = [], [], {}
    for model in ("cyclic","feedforward"):
        for p in range(2):
            for b in range(2):
                for e in range(2):
                    for d in range(2):
                        seq=trace(model,p,b,e,d)
                        paths[(model,p,b,e,d)]=seq
                        for t, (pp,bb,ee) in enumerate(seq):
                            rows.append([model,p,b,e,d,t,pp,bb,ee])
                        pp,bb,ee=seq[-1]
                        worlds.append(dict(mechanism=model,initial_p=p,initial_b=b,initial_e=e,do_b1=d,final_p=pp,final_b=bb,final_e=ee))
    checks=dict(equal_b1=0,different_p2=0,different_b3=0,cyclic_e2_do=0,feedforward_e2_do=0)
    for p in range(2):
        for b in range(2):
            for e in range(2):
                c0=paths[("cyclic",p,b,e,0)]
                c1=paths[("cyclic",p,b,e,1)]
                f0=paths[("feedforward",p,b,e,0)]
                f1=paths[("feedforward",p,b,e,1)]
                checks["cyclic_e2_do"] += c0[2][2] != c1[2][2]
                checks["feedforward_e2_do"] += f0[2][2] != f1[2][2]
                for c,f in ((c0,f0),(c1,f1)):
                    checks["equal_b1"] += c[1][1] == f[1][1]
                    checks["different_p2"] += c[2][0] != f[2][0]
                    checks["different_b3"] += c[3][1] != f[3][1]
    return rows,dict(schema="R333_frozen_triads_v1",worlds=worlds,checks=checks)

def render():
    rows,obj=generate()
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\r\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return stream.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=False)+"\n").encode()

def audit():
    csv_data,json_data=render()
    assert CSV.read_bytes()==csv_data, "CSV byte replay mismatch"
    assert RESULTS.read_bytes()==json_data, "JSON byte replay mismatch"
    rows,obj=generate()
    assert len(rows)==160 and len(obj["worlds"])==32
    assert obj["checks"]==dict(equal_b1=16,different_p2=8,different_b3=8,cyclic_e2_do=8,feedforward_e2_do=0)

class Tests(unittest.TestCase):
    def test_counts(self):
        rows,obj=generate()
        self.assertEqual((len(rows),len(obj["worlds"])),(160,32))
    def test_falsifiers(self):
        self.assertEqual(generate()[1]["checks"],dict(equal_b1=16,different_p2=8,different_b3=8,cyclic_e2_do=8,feedforward_e2_do=0))
    def test_intervention(self):
        for m in ("cyclic","feedforward"):
            for p in range(2):
                for b in range(2):
                    for e in range(2):
                        self.assertEqual(trace(m,p,b,e,0)[1][1],0)
                        self.assertEqual(trace(m,p,b,e,1)[1][1],1)
    def test_byte_replay(self):
        audit()
    def test_binary(self):
        self.assertTrue(all(all(v in (0,1) for v in row[1:5]+row[6:]) for row in generate()[0]))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--audit",action="store_true")
    args=ap.parse_args()
    if args.test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful(): raise SystemExit(1)
    if args.audit:
        audit()
        print("R333 PRODUCTION_REPLAY_PASS 160 rows 32 worlds")
