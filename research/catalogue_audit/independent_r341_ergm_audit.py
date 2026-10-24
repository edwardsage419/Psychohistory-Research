#!/usr/bin/env python3
"""R341 independent exact graph audit, without importing production."""
import csv
import io
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R341"

def replay():
    csv_out=io.StringIO(newline="")
    writer=csv.writer(csv_out,lineterminator="\n")
    writer.writerow(["a","b","graph_bits","edges","triangles","unnormalized_weight","probability"])
    worlds=[]
    for a,b in ((1,1),(1,2),(2,1),(2,2)):
        graph_rows=[]
        for mask in range(8):
            bits=f"{mask:03b}"
            e=sum(int(c) for c in bits)
            t=int(mask==7)
            weight=(a**e)*(b**t)
            graph_rows.append((bits,e,t,weight))
        z=sum(row[3] for row in graph_rows)
        ps=[]
        for bits,e,t,w in graph_rows:
            p=Fraction(w,z)
            ps.append(p)
            writer.writerow([str(a),str(b),bits,str(e),str(t),str(Fraction(w)),str(p)])
        marginal=sum((p for p,(bits,e,t,w) in zip(ps,graph_rows) if bits[0]=="1"),Fraction(0))
        # Compare the two conditional edge odds from the exact graph weights.
        weights={bits:w for bits,e,t,w in graph_rows}
        odds_ratio=Fraction(weights["111"],weights["011"])/Fraction(weights["100"],weights["000"])
        worlds.append({
            "a":str(a),"b":str(b),"Z":str(Fraction(z)),
            "edge_marginal":str(marginal),"triangle_probability":str(ps[-1]),
            "closure_odds_ratio":str(odds_ratio),
            "graph_probabilities":[str(p) for p in ps],
        })
    results={
        "schema":"R341_frozen_three_node_ergm_v1",
        "worlds":worlds,
        "checks":{
            "worlds":4,"source_rows":32,"normalization_worlds":4,
            "expected_partition_functions":["8","9","27","35"],
            "baseline_independent_worlds":2,"closure_contrast_worlds":2,
        },
    }
    return csv_out.getvalue().encode(),(json.dumps(results,indent=2,ensure_ascii=True)+"\n").encode()

def main():
    expected_csv,expected_json=replay()
    actual_csv=(ROOT/"R341_ALL_32_ARTIFICIAL_GRAPH_ATOMS.csv").read_bytes()
    actual_json=(ROOT/"R341_EXACT_4_GRAPH_WORLDS.json").read_bytes()
    assert actual_csv==expected_csv, "independent CSV replay failed"
    assert actual_json==expected_json, "independent JSON replay failed"
    assert b"1,2,111,3,1,2,2/9" in expected_csv
    assert b'"source_rows": 32' in expected_json
    assert actual_csv!=expected_csv.replace(b"1,2,111,3,1,2,2/9",b"1,2,111,3,1,2,1/9")
    assert actual_json!=expected_json.replace(b'"source_rows": 32',b'"source_rows": 33')
    print("R341_INDEPENDENT_NO_IMPORT_AUDIT=PASS; NEGATIVE_TAMPER_TESTS=2")

if __name__=="__main__":
    main()
