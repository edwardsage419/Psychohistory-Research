#!/usr/bin/env python3
"""R323 independent no-import complete VBN truth table audit."""
import csv,itertools,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]/"R323"
names=("vbn_cascade","direct_product","unconstrained_norm","value_feasible")
def run():
    with (HERE/"R323_ALL_128_ORIGINAL_VBN_STATES.csv").open(encoding="utf-8",newline="") as f:rows=list(csv.DictReader(f))
    result=json.loads((HERE/"R323_EXACT_FOUR_VBN_WORLDS.json").read_text(encoding="utf-8"))
    assert len(rows)==128 and len(result["worlds"])==4
    states=list(itertools.product((0,1),repeat=5))
    outputs={}
    for i,name in enumerate(names):
        ncount=acount=c0=0;acts=[]
        for j,(V,T,R,E,C) in enumerate(states):
            chain=V*T*R*E
            if i==0:n=chain;a=chain*C
            elif i==1:n=0;a=V*T*R*E*C
            elif i==2:n=chain;a=chain
            else:n=V;a=V*C
            ncount+=n;acount+=a;c0+=int(C==0 and a==1);acts.append(a)
            row=rows[i*32+j]
            assert list(row.values())==[str(i),name,*map(str,(V,T,R,E,C)),"1/32",str(n),str(a)],(i,j,row)
        outputs[name]=acts
        w=result["worlds"][i]
        assert (w["world_id"],w["policy"],w["state_count"])==(i,name,32)
        assert (w["personal_norm_positive_count"],w["action_positive_count"],w["action_when_C_zero_count"])==(ncount,acount,c0)
        assert F(w["personal_norm_rate"])==F(ncount,32) and F(w["action_rate"])==F(acount,32)
    pairs={}
    for i,p in enumerate(names):
        for q in names[i+1:]:pairs[p+"|"+q]=sum(a!=b for a,b in zip(outputs[p],outputs[q]))
    assert pairs==result["pairwise_action_disagreement_counts"]
    assert outputs["vbn_cascade"]==outputs["direct_product"]
    assert result["original_catalogue_id"]=="01-015" and result["original_source_rows"]==128
    print("R323_INDEPENDENT_VBN_AUDIT_PASS 128 rows four policies six pairwise checks")
if __name__=="__main__":run()
