#!/usr/bin/env python3
"""R343 independent no-import bitmask multiplex projection replay."""
import csv
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R343"

def recreate():
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(["layer0_bits","layer1_bits","edge","layer0","layer1","union","intersection"])
    worlds=[]
    for i in range(8):
        for j in range(8):
            a,b=f"{i:03b}",f"{j:03b}"
            union=f"{i|j:03b}"
            intersection=f"{i&j:03b}"
            worlds.append({"layer0_bits":a,"layer1_bits":b,"union_bits":union,"intersection_bits":intersection})
            for k,edge in enumerate(("01","02","12")):
                writer.writerow([a,b,edge,a[k],b[k],union[k],intersection[k]])
    checks={
        "worlds":len(worlds),
        "source_rows":len(worlds)*3,
        "unique_union_graphs":len({w["union_bits"] for w in worlds}),
        "union_111_preimages":sum(w["union_bits"]=="111" for w in worlds),
        "union_000_preimages":sum(w["union_bits"]=="000" for w in worlds),
        "union_111_intersection_000_preimages":sum(w["union_bits"]=="111" and w["intersection_bits"]=="000" for w in worlds),
        "layer_swap_invariant_worlds":sum(all(w[key]==next(x for x in worlds if x["layer0_bits"]==w["layer1_bits"] and x["layer1_bits"]==w["layer0_bits"])[key] for key in ("union_bits","intersection_bits")) for w in worlds),
    }
    result={"schema":"R343_frozen_three_node_two_layer_projection_v1","worlds":worlds,"checks":checks}
    return out.getvalue().encode(),(json.dumps(result,indent=2,ensure_ascii=True)+"\n").encode()

def main():
    a,b=recreate()
    csv_actual=(ROOT/"R343_ALL_192_ARTIFICIAL_LAYER_EDGE_ATOMS.csv").read_bytes()
    json_actual=(ROOT/"R343_EXACT_64_LAYER_PAIRS.json").read_bytes()
    assert csv_actual==a,"independent CSV mismatch"
    assert json_actual==b,"independent JSON mismatch"
    assert b"000,000,01,0,0,0,0" in a
    assert b'"source_rows": 192' in b
    assert csv_actual!=a.replace(b"000,000,01,0,0,0,0",b"000,000,01,0,0,1,0")
    assert json_actual!=b.replace(b'"source_rows": 192',b'"source_rows": 193')
    print("R343_INDEPENDENT_NO_IMPORT_AUDIT=PASS; NEGATIVE_TAMPER_TESTS=2")

if __name__=="__main__":
    main()
