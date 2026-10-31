#!/usr/bin/env python3
"""R323 S119 no-import nonblind independent oracle and mutation audit. E1 only."""
import copy,csv,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/"research/R323/R323_ALL_128_ORIGINAL_VBN_STATES.csv"
CSV=ROOT/"research/validation/R323_S119_DO_NORM_256_ROWS.csv"
JSON=ROOT/"research/validation/R323_S119_EXACT_RESULTS.json"
SHA="1b92efb314aae036e773be92e28793f8fcd60809"
POL=("vbn_cascade","direct_product","unconstrained_norm","value_feasible")
FIELDS=("world_id","policy","V","T","R","E","C","natural_norm","natural_action","do_norm","do_action","weight")
def gate(ok,label):
    if not ok:raise ValueError(label)
def oracle(w,V,T,R,E,C,n):
    chain=int(all((V,T,R,E)))
    natural=(chain if w in (0,2) else (0 if w==1 else V))
    natural_action=(chain*C if w in (0,1) else (chain if w==2 else V*C))
    intervened=(n*C if w==0 else (chain*C if w==1 else (n if w==2 else V*C)))
    return natural,natural_action,intervened
def check(rows,summary,original):
    gate(len(rows)==256 and len(original)==128,"count")
    gate(summary.get("schema")=="r323_s119_structural_do_norm_e1_v1" and summary.get("rows")==256 and summary.get("source_blob")==SHA,"schema/source")
    gate(summary.get("evidence")=="E1_ARTIFICIAL_ONLY" and summary.get("real_human_E2")=="NOT_ESTABLISHED" and summary.get("historical_E3")=="NOT_ESTABLISHED" and summary.get("external_independent_replication")=="NOT_RUN","grade")
    seen=set();byworld={w:[] for w in range(4)}
    for r in rows:
        gate(set(r)==set(FIELDS),"fields")
        try:w=int(r["world_id"]);V,T,R,E,C=(int(r[k]) for k in ("V","T","R","E","C"));n=int(r["do_norm"])
        except (ValueError,TypeError):raise ValueError("numeric")
        key=(w,V,T,R,E,C,n)
        gate(w in range(4) and all(z in (0,1) for z in (V,T,R,E,C,n)) and key not in seen,"coverage")
        seen.add(key)
        gate(r["policy"]==POL[w] and r["weight"]=="1/64","policy/weight")
        x=oracle(w,V,T,R,E,C,n)
        gate((r["natural_norm"],r["natural_action"],r["do_action"])==tuple(map(str,x)),"action")
        byworld[w].append(r)
    gate(len(seen)==256,"full coverage")
    orig_seen=set()
    for r in original:
        w=int(r["world_id"]);V,T,R,E,C=(int(r[k]) for k in ("V","T","R","E","C"))
        key=(w,V,T,R,E,C)
        gate(w in range(4) and key not in orig_seen and r["policy"]==POL[w] and r["weight"]=="1/32","original identity")
        orig_seen.add(key);x=oracle(w,V,T,R,E,C,0)
        gate((r["latent_norm"],r["action"])==tuple(map(str,x[:2])),"original natural")
    gate(len(orig_seen)==128,"original coverage")
    for w in range(4):
        gate(sum(F(r["weight"]) for r in byworld[w])==1,"mass")
        z=sum(int(r["do_action"]) for r in byworld[w] if r["do_norm"]=="0")
        o=sum(int(r["do_action"]) for r in byworld[w] if r["do_norm"]=="1")
        gate(summary["worlds"][w]=={"world_id":w,"policy":POL[w],"rows":64,"do0_action_positive":z,"do1_action_positive":o,"average_intervention_effect":str(F(o-z,32))},"world")
    pair={}
    states=list(itertools.product((0,1),repeat=5))
    for i in range(4):
        for j in range(i+1,4):
            pair[POL[i]+"|"+POL[j]]=sum(oracle(i,*s,n)[2]!=oracle(j,*s,n)[2] for s in states for n in (0,1))
    gate(summary.get("pairwise_action_disagreements")==pair,"pairwise")
    d0=sum(oracle(0,*s,0)[2]!=oracle(1,*s,0)[2] for s in states)
    d1=sum(oracle(0,*s,1)[2]!=oracle(1,*s,1)[2] for s in states)
    v=F(d0+d1,64)
    expected={"observational_disagreements":0,"do0_disagreements":d0,"do1_disagreements":d1,"total_disagreements":d0+d1,"tv":str(v),"equal_prior_accuracy":str((1+v)/2),"do0_tv":str(F(d0,32)),"do1_tv":str(F(d1,32)),"do0_accuracy":str((1+F(d0,32))/2),"do1_accuracy":str((1+F(d1,32))/2)}
    gate(summary.get("cascade_vs_direct")==expected,"TV/classifier")
    return pair
def main():
    raw=SOURCE.read_bytes();gate(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==SHA,"source Git blob")
    rows=list(csv.DictReader(CSV.open(encoding="utf-8",newline="")))
    summary=json.loads(JSON.read_text(encoding="utf-8"))
    original=list(csv.DictReader(SOURCE.open(encoding="utf-8",newline="")))
    pairs=check(rows,summary,original)
    cases=[]
    cases.append(("omission",rows[:-1],summary,original))
    cases.append(("duplicate",rows[:-1]+[rows[0]],summary,original))
    a=copy.deepcopy(rows);a[0]["do_norm"]="1";cases.append(("assignment",a,summary,original))
    a=copy.deepcopy(rows);a[1]["do_action"]=str(1-int(a[1]["do_action"]));cases.append(("action",a,summary,original))
    a=copy.deepcopy(rows);a[0]["weight"]="1/32";cases.append(("weight",a,summary,original))
    b=copy.deepcopy(summary);b["evidence"]="E2_HUMAN";cases.append(("grade",rows,b,original))
    b=copy.deepcopy(summary);b["cascade_vs_direct"]["tv"]="1";cases.append(("TV",rows,b,original))
    a=copy.deepcopy(original);a[0]["action"]="1";cases.append(("original",rows,summary,a))
    a=copy.deepcopy(rows);a[0]["policy"]="direct_product";cases.append(("policy",a,summary,original))
    rejected=[]
    for name,r,s,o in cases:
        try:check(r,s,o)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise AssertionError("mutation accepted "+name)
    print(json.dumps({"status":"PASS_NONBLIND_E1","original_rows":len(original),"intervention_rows":len(rows),"pairwise":pairs,"rejected_mutations":rejected},sort_keys=True))
if __name__=="__main__":main()
