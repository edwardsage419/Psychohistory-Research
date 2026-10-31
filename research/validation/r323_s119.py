#!/usr/bin/env python3
"""R323 S119: frozen finite do(N) experiment, E1 artificial only."""
import argparse,csv,hashlib,io,itertools,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"research/R323/R323_ALL_128_ORIGINAL_VBN_STATES.csv"
HERE=Path(__file__).resolve().parent
CSV=HERE/"R323_S119_DO_NORM_256_ROWS.csv"
JSON=HERE/"R323_S119_EXACT_RESULTS.json"
SHA="1b92efb314aae036e773be92e28793f8fcd60809"
POL=("vbn_cascade","direct_product","unconstrained_norm","value_feasible")
FIELDS=("world_id","policy","V","T","R","E","C","natural_norm","natural_action","do_norm","do_action","weight")
def source():
    raw=SOURCE.read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if actual!=SHA:raise ValueError("original R323 blob changed")
    rows=list(csv.DictReader(io.StringIO(raw.decode())))
    if len(rows)!=128:raise ValueError("source count")
    seen=set()
    for r in rows:
        w=int(r["world_id"]);s=tuple(int(r[k]) for k in ("V","T","R","E","C"))
        if w not in range(4) or r["policy"]!=POL[w] or any(x not in (0,1) for x in s) or (w,s) in seen:raise ValueError("source identity")
        seen.add((w,s))
        V,T,R,E,C=s; chain=V*T*R*E
        n=(chain if w in (0,2) else (0 if w==1 else V))
        a=(n*C if w==0 else (chain*C if w==1 else (n if w==2 else V*C)))
        if (r["weight"],r["latent_norm"],r["action"])!=("1/32",str(n),str(a)):raise ValueError("source natural action")
    return rows
def action(w,s,n):
    V,T,R,E,C=s
    return (n*C, V*T*R*E*C, n, V*C)[w]
def fraction(a,b):return str(F(a,b))
def calculate():
    rows=[];original=source()
    for r in original:
        w=int(r["world_id"]);s=tuple(int(r[k]) for k in ("V","T","R","E","C"))
        for n in (0,1):
            rows.append({"world_id":r["world_id"],"policy":r["policy"],"V":r["V"],"T":r["T"],"R":r["R"],"E":r["E"],"C":r["C"],"natural_norm":r["latent_norm"],"natural_action":r["action"],"do_norm":str(n),"do_action":str(action(w,s,n)),"weight":"1/64"})
    states=list(itertools.product((0,1),repeat=5))
    worlds=[]
    for i,p in enumerate(POL):
        x=sum(action(i,s,0) for s in states);y=sum(action(i,s,1) for s in states)
        worlds.append({"world_id":i,"policy":p,"rows":64,"do0_action_positive":x,"do1_action_positive":y,"average_intervention_effect":fraction(y-x,32)})
    pairs={}
    for i,p in enumerate(POL):
        for j in range(i+1,4):
            pairs[p+"|"+POL[j]]=sum(action(i,s,n)!=action(j,s,n) for s in states for n in (0,1))
    d0=sum(action(0,s,0)!=action(1,s,0) for s in states)
    d1=sum(action(0,s,1)!=action(1,s,1) for s in states)
    summary={"schema":"r323_s119_structural_do_norm_e1_v1","source_blob":SHA,"evidence":"E1_ARTIFICIAL_ONLY","rows":256,"worlds":worlds,"pairwise_action_disagreements":pairs,"cascade_vs_direct":{"observational_disagreements":0,"do0_disagreements":d0,"do1_disagreements":d1,"total_disagreements":d0+d1,"tv":fraction(d0+d1,64),"equal_prior_accuracy":str((1+F(d0+d1,64))/2),"do0_tv":fraction(d0,32),"do1_tv":fraction(d1,32),"do0_accuracy":str((1+F(d0,32))/2),"do1_accuracy":str((1+F(d1,32))/2)},"real_human_E2":"NOT_ESTABLISHED","historical_E3":"NOT_ESTABLISHED","external_independent_replication":"NOT_RUN"}
    stream=io.StringIO(newline="");writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader();writer.writerows(rows)
    return stream.getvalue().encode(),(json.dumps(summary,indent=2,ensure_ascii=False)+"\n").encode()
def main():
    p=argparse.ArgumentParser();p.add_argument("--emit",action="store_true");a=p.parse_args()
    c,j=calculate()
    if a.emit:
        if CSV.exists() or JSON.exists():raise FileExistsError("refuse overwrite")
        CSV.write_bytes(c);JSON.write_bytes(j)
    elif CSV.read_bytes()!=c or JSON.read_bytes()!=j:raise AssertionError("S119 persisted bytes differ")
    print("R323_S119_REPLAY_PASS",len(c),len(j))
if __name__=="__main__":main()
