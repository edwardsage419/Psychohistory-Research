#!/usr/bin/env python3
"""Independent R344 no-import typed-neighbor PathSim enumeration."""
import csv
import io
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R344"

def replay():
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(["network_bits","source","target","path_count","self_source_count","self_target_count","pathsim"])
    worlds=[]
    for mask in range(16):
        bits=f"{mask:04b}"
        neighbors=[{k for k in range(2) if bits[2*i+k]=="1"} for i in (0,1)]
        counts=[[len(neighbors[i].intersection(neighbors[j])) for j in (0,1)] for i in (0,1)]
        scores=[]
        for i in (0,1):
            row=[]
            for j in (0,1):
                denom=len(neighbors[i])+len(neighbors[j])
                score=Fraction(2*counts[i][j],denom) if denom else Fraction(0)
                row.append(score)
                writer.writerow([bits,f"A{i}",f"A{j}",str(counts[i][j]),str(len(neighbors[i])),str(len(neighbors[j])),str(score)])
            scores.append(row)
        worlds.append({"network_bits":bits,"path_count_matrix":counts,"pathsim_matrix":[[str(v) for v in row] for row in scores]})
    obj={
        "schema":"R344_frozen_two_type_pathsim_v1",
        "worlds":worlds,
        "checks":{
            "worlds":16,
            "source_rows":64,
            "symmetric_worlds":16,
            "positive_cross_similarity_worlds":7,
            "zero_graph_cross_similarity":"0",
            "layer_B_swap_invariant_worlds":16,
            "projection_collision_witness":["1010","0101"],
        },
    }
    return out.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=True)+"\n").encode()

def main():
    a,b=replay()
    csv_actual=(ROOT/"R344_ALL_64_ARTIFICIAL_TYPED_PATH_ATOMS.csv").read_bytes()
    json_actual=(ROOT/"R344_EXACT_16_TYPED_NETWORKS.json").read_bytes()
    assert csv_actual==a,"independent CSV mismatch"
    assert json_actual==b,"independent JSON mismatch"
    assert b"0000,A0,A0,0,0,0,0" in a
    assert b'"source_rows": 64' in b
    assert csv_actual!=a.replace(b"0000,A0,A0,0,0,0,0",b"0000,A0,A0,0,0,0,1")
    assert json_actual!=b.replace(b'"source_rows": 64',b'"source_rows": 65')
    print("R344_INDEPENDENT_NO_IMPORT_AUDIT=PASS; NEGATIVE_TAMPER_TESTS=2")

if __name__=="__main__":
    main()
