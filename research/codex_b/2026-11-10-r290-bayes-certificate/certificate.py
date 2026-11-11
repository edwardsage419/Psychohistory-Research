"""Independent integer loss-matrix and learned-rule-law certificate for S86.

No R/B program imports. All 32 deterministic five-bin rules are evaluated, then
training weights are aggregated by learned rule before independent test scoring.
"""
import csv
from fractions import Fraction as F
from functools import lru_cache
import io
import json

DGP={"MONOTONE":((8,6,4,2,1),(1,2,4,6,8),21),
     "CENTERED":((8,2,1,2,8),(1,3,13,3,1),21),
     "IDENTICAL":((1,2,3,2,1),(1,2,3,2,1),9)}
PRIORS=(F(1,2),F(3,4))
FIELDS=("dgp","m","noise_draws","signal_draws","probability")


def require(condition,reason):
    if not condition:raise ValueError(reason)


def parameters(pi,fp,fn):
    require(type(pi) is F and pi in PRIORS and type(fp) is int and type(fn) is int and
            (fp,fn) in ((1,1),(1,3)),"UNFROZEN_PRIOR_OR_COST")


def loss_certificate(name,pi,fp,fn):
    require(type(name) is str and name in DGP,"UNFROZEN_DGP");parameters(pi,fp,fn)
    noise,signal,denominator=DGP[name];a,b=pi.numerator,pi.denominator
    losses=[sum((b-a)*fp*noise[x] if mask&(1<<x) else a*fn*signal[x] for x in range(5)) for mask in range(32)]
    minimum=min(losses);masks=[sum(1<<x for x in range(t,5)) for t in range(6)]
    cutoffs=[losses[mask] for mask in masks];best_t=min(range(6),key=lambda t:(cutoffs[t],t))
    return {"denominator":b*denominator,"loss_numerators":losses,"minimum_numerator":minimum,
            "minimizing_masks":[mask for mask,value in enumerate(losses) if value==minimum],
            "cutoff_masks":masks,"cutoff_numerators":cutoffs,"best_cutoff_t":best_t,
            "best_constant_numerator":min(losses[0],losses[31])}


def trained_mask(a,b,pi,fp,fn):
    parameters(pi,fp,fn)
    require(type(a) is str and type(b) is str and len(a)==len(b) and len(a) in (1,2) and
            set(a+b)<=set("01234"),"UNFROZEN_TRAINING_SEQUENCE")
    numerator,denominator=pi.numerator,pi.denominator
    return sum(1<<x for x in range(5) if numerator*fn*(b.count(str(x))+1)>
               (denominator-numerator)*fp*(a.count(str(x))+1))


@lru_cache(maxsize=2)
def _derive(csv_raw):
    table=list(csv.reader(io.StringIO(csv_raw.decode("utf-8"),newline=""),strict=True))
    require(len(table)==1951 and tuple(table[0])==FIELDS,"LEDGER_HEADER_OR_COUNT")
    groups={(name,m):[] for name in DGP for m in (1,2)};seen=set();mass={key:0 for key in groups}
    for row in table[1:]:
        require(len(row)==5,"LEDGER_WIDTH")
        name,m_text,a,b,probability=row
        require(name in DGP and m_text in ("1","2"),"LEDGER_WORLD")
        m=int(m_text)
        require(len(a)==len(b)==m and set(a+b)<=set("01234"),"LEDGER_SEQUENCE")
        key=(name,m,a,b);require(key not in seen,"DUPLICATE_SOURCE");seen.add(key)
        noise,signal,den=DGP[name];weight=1
        for x in a:weight*=noise[int(x)]
        for x in b:weight*=signal[int(x)]
        require(probability==str(F(weight,den**(2*m))),"LEDGER_PROBABILITY")
        groups[name,m].append((a,b,weight));mass[name,m]+=weight
    require(len(seen)==1950 and all(len(rows)==5**(2*m) and mass[name,m]==DGP[name][2]**(2*m)
            for (name,m),rows in groups.items()),"LEDGER_UNIVERSE")
    results=[];proofs={};histograms={}
    for name in DGP:
        for pi in PRIORS:
            for fp,fn in ((1,1),(1,3)):
                world=f"{name}_PI{pi.numerator}of{pi.denominator}_FP{fp}_FN{fn}"
                proof=loss_certificate(name,pi,fp,fn);proofs[world]=proof
                losses=proof["loss_numerators"];minimum=proof["minimum_numerator"];risk_den=proof["denominator"]
                for m in (1,2):
                    weights=[0]*32
                    for a,b,weight in groups[name,m]:weights[trained_mask(a,b,pi,fp,fn)]+=weight
                    train_den=DGP[name][2]**(2*m)
                    require(sum(weights)==train_den,"RULE_LAW_MASS")
                    total=sum(weight*cost for weight,cost in zip(weights,losses))
                    gaps=sum(weight*(cost-minimum) for weight,cost in zip(weights,losses))
                    require(all(cost>=minimum for cost in losses) and gaps==total-train_den*minimum,"OPTIMALITY_GAP_IDENTITY")
                    histograms[world+"|"+str(m)]={"weights":weights,"denominator":train_den,"gap_numerator":gaps,"risk_denominator":risk_den}
                    best_t=proof["best_cutoff_t"]
                    results.append({"world":world,"m":m,"sources":5**(2*m),"training_mass":"1",
                        "expected_heldout_risk":str(F(total,train_den*risk_den)),"oracle_risk":str(F(minimum,risk_den)),
                        "regret":str(F(gaps,train_den*risk_den)),
                        "best_fixed_cutoff_risk":str(F(proof["cutoff_numerators"][best_t],risk_den)),
                        "best_fixed_cutoff_t":best_t,"fixed_t3_risk":str(F(proof["cutoff_numerators"][3],risk_den)),
                        "best_constant_risk":str(F(proof["best_constant_numerator"],risk_den))})
    expected={"research_id":"R290_S86","prescore_commit":"90998f553dcc2697fdbf61a6355b9b4ffc3e5e95",
              "evidence":"E1_ARTIFICIAL_ONLY","original_R290_unchanged":True,"R073":"FROZEN","PESEN":"FROZEN",
              "new_E2":0,"new_E3":0,"worlds":12,"results":results}
    return json.dumps({"expected":expected,"loss_certificates":proofs,"rule_histograms":histograms,"source_rows":1950})


def derive(csv_raw):
    require(type(csv_raw) is bytes,"LEDGER_BYTES_REQUIRED")
    return json.loads(_derive(csv_raw))
