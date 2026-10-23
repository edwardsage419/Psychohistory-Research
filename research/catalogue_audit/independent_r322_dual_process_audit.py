#!/usr/bin/env python3
"""R322 independent truth-table and count audit; never imports the R322 generator."""
import csv,itertools,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]/"R322"
policies=("default_only","gated_intervention","analytic_only","lookup_equivalent")
def run():
    with (HERE/"R322_ALL_256_ORIGINAL_BINARY_STATES.csv").open(encoding="utf-8",newline="") as f:rows=list(csv.DictReader(f))
    result=json.loads((HERE/"R322_EXACT_FOUR_POLICY_WORLDS.json").read_text(encoding="utf-8"))
    assert len(rows)==256 and len(result["worlds"])==4
    states=list(itertools.product((0,1),repeat=6))
    outputs={}
    for i,policy in enumerate(policies):
        correct=changed=interventions=0
        arr=[]
        for j,(h,a,y,d,r,w) in enumerate(states):
            if policy=="default_only":out=h;inter=0
            elif policy=="analytic_only":out=a;inter=1
            elif policy=="gated_intervention":
                inter=int((h!=a) and bool(d) and bool(r) and bool(w));out=a if inter else h
            else:out=h if (h==a or d*r*w==0) else a;inter=0
            correct+=int(out==y);changed+=int(out!=h);interventions+=inter;arr.append(out)
            row=rows[i*64+j]
            expected=[str(i),policy,*map(str,(h,a,y,d,r,w)),"1/64",str(out),str(int(out==y)),str(inter)]
            assert list(row.values())==expected,(i,j,row)
        outputs[policy]=arr
        obj=result["worlds"][i]
        assert (obj["world_id"],obj["policy"],obj["state_count"])==(i,policy,64)
        assert (obj["correct_count"],obj["changed_from_default_count"],obj["intervention_count"])==(correct,changed,interventions)
        assert (obj["correct_fraction"],obj["changed_fraction"],obj["intervention_fraction"])==("1/2",str(changed//64) if changed in (0,64) else ("1/16" if changed==4 else "1/2"),str(interventions//64) if interventions in (0,64) else "1/16")
    pairwise={}
    for i,p in enumerate(policies):
        for q in policies[i+1:]:
            pairwise[p+"|"+q]=sum(x!=y for x,y in zip(outputs[p],outputs[q]))
    assert pairwise==result["pairwise_output_disagreement_counts"]
    assert outputs["gated_intervention"]==outputs["lookup_equivalent"]
    assert result["original_source_rows"]==256 and result["original_catalogue_id"]=="01-012"
    print("R322_INDEPENDENT_TRUTH_TABLE_PASS 256 rows four policies equivalence and error boundaries")
if __name__=="__main__":run()
