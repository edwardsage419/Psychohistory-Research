#!/usr/bin/env python3
"""R343 finite two-layer projection and aggregation. Constructed E1 only."""
import argparse
import csv
import io
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
GRAPHS=tuple(format(i,"03b") for i in range(8))
EDGES=("01","02","12")
CSV_PATH=ROOT/"R343_ALL_192_ARTIFICIAL_LAYER_EDGE_ATOMS.csv"
JSON_PATH=ROOT/"R343_EXACT_64_LAYER_PAIRS.json"

def worlds():
    output=[]
    for layer0 in GRAPHS:
        for layer1 in GRAPHS:
            union="".join("1" if a=="1" or b=="1" else "0" for a,b in zip(layer0,layer1))
            intersection="".join("1" if a=="1" and b=="1" else "0" for a,b in zip(layer0,layer1))
            output.append({"layer0_bits":layer0,"layer1_bits":layer1,
                           "union_bits":union,"intersection_bits":intersection})
    return output

def artifacts():
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(("layer0_bits","layer1_bits","edge","layer0","layer1","union","intersection"))
    w=worlds()
    for x in w:
        for k,edge in enumerate(EDGES):
            writer.writerow((x["layer0_bits"],x["layer1_bits"],edge,
                             x["layer0_bits"][k],x["layer1_bits"][k],
                             x["union_bits"][k],x["intersection_bits"][k]))
    result={
        "schema":"R343_frozen_three_node_two_layer_projection_v1",
        "worlds":w,
        "checks":{
            "worlds":64,
            "source_rows":192,
            "unique_union_graphs":8,
            "union_111_preimages":27,
            "union_000_preimages":1,
            "union_111_intersection_000_preimages":8,
            "layer_swap_invariant_worlds":64,
        },
    }
    return out.getvalue().encode("utf-8"),(json.dumps(result,indent=2,ensure_ascii=True)+"\n").encode("utf-8")

def audit():
    a,b=artifacts()
    assert CSV_PATH.read_bytes()==a,"CSV mismatch"
    assert JSON_PATH.read_bytes()==b,"JSON mismatch"

class FrozenTests(unittest.TestCase):
    def test_universe(self):
        self.assertEqual(len(worlds()),64)
        self.assertEqual(len(artifacts()[0].decode().splitlines()),193)
    def test_bitwise_rules(self):
        for x in worlds():
            for k in range(3):
                a,b=int(x["layer0_bits"][k]),int(x["layer1_bits"][k])
                self.assertEqual(int(x["union_bits"][k]),a|b)
                self.assertEqual(int(x["intersection_bits"][k]),a&b)
    def test_unique_unions(self):
        self.assertEqual(len({x["union_bits"] for x in worlds()}),8)
    def test_preimage_counts(self):
        w=worlds()
        self.assertEqual(sum(x["union_bits"]=="111" for x in w),27)
        self.assertEqual(sum(x["union_bits"]=="000" for x in w),1)
        self.assertEqual(sum(x["union_bits"]=="111" and x["intersection_bits"]=="000" for x in w),8)
    def test_swap_invariance(self):
        lookup={(x["layer0_bits"],x["layer1_bits"]):x for x in worlds()}
        for x in worlds():
            y=lookup[(x["layer1_bits"],x["layer0_bits"])]
            self.assertEqual(x["union_bits"],y["union_bits"])
            self.assertEqual(x["intersection_bits"],y["intersection_bits"])
    def test_byte_replay(self):
        audit()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--write",action="store_true")
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.write:
        a,b=artifacts()
        CSV_PATH.write_bytes(a)
        JSON_PATH.write_bytes(b)
    if args.audit:
        audit()
        print("R343_PRODUCTION_BYTE_REPLAY=PASS")
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FrozenTests))
        if not result.wasSuccessful():raise SystemExit(1)
    if not (args.write or args.test or args.audit):p.print_help()

if __name__=="__main__":
    main()
