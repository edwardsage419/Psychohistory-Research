#!/usr/bin/env python3
"""12 session LOSO one-step human C/D group-frequency model comparison.

Original author's submission Git data. Real PD payoffs [R3,T4,S0,P1].
This is NOT human individual-level strategy inference or full-round forecast.
"""
from __future__ import annotations
import argparse,csv,io,json,math
from collections import Counter,defaultdict
from pathlib import Path

from r067_author_ipd_submission_audit import FILES,audit_csv_bytes,SUBMISSION_COMMIT
from r067_strategy_dynamics import replicator_step,logit_response_step,best_response_step,delta

REAL_PD=((3.0,0.0),(4.0,1.0))
TREATMENTS=("fix","rand")
CLASSES=("persistence","replicator","dynamic_logit","best_response",
         "train_only_treatment_prevalence")
H=(0.01,0.05,0.1,0.2)
L=(0.5,1.0,2.0,5.0)
ETA=(0.01,0.05,0.1,0.2)
N_ROUNDS=100


def variants(model):
    if model in ("persistence","train_only_treatment_prevalence"):
        return [("no_parameter",{})]
    if model=="replicator":
        return [(f"dt={x}",{"dt":x}) for x in H]
    if model=="dynamic_logit":
        return [(f"lambda={l},eta={e}",{"lam":l,"eta":e}) for l in L for e in ETA]
    if model=="best_response":
        return [(f"eta={x}",{"eta":x}) for x in ETA]
    raise ValueError("unknown model family")


def predict(model,x,param,constant=None):
    if not math.isfinite(x) or x<0 or x>1:
        raise ValueError("source cooperation share not in unit interval")
    if model=="persistence":
        return x
    if model=="train_only_treatment_prevalence":
        if constant is None or not math.isfinite(constant) or not 0<=constant<=1:
            raise ValueError("missing train-only treatment prior")
        return constant
    if model=="replicator":
        return replicator_step(x,REAL_PD,dt=param["dt"])
    if model=="dynamic_logit":
        return logit_response_step(x,REAL_PD,lam=param["lam"],eta=param["eta"])
    if model=="best_response":
        return best_response_step(x,REAL_PD,eta=param["eta"])
    raise ValueError("unknown model")


def load_session_series(folder:Path):
    counts=defaultdict(Counter)
    cooperators=defaultdict(Counter)
    participants=defaultdict(set)
    participant_rounds=set()
    by_treat=Counter()
    for filename,(size,sha) in FILES.items():
        raw=(folder/filename).read_bytes()
        schema=audit_csv_bytes(filename,raw)
        if (schema["actions_player_other_or_missing"] or
            schema["invalid_round_values"] or
            schema["session_player_round_repeat_rows"] or
            schema["missing_session_or_player_rows"] or
            schema["records_who_played_other_or_missing"] or
            schema["records_treatment_other_or_missing"]):
            raise ValueError("original C/D action or identity integrity violation")
        expected_tr="fix" if filename=="fix.csv" else "rand"
        rdr=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
        for row in rdr:
            if row["treatment"]!=expected_tr:
                raise ValueError("mismatched treatment in pinned source file")
            session=(expected_tr,row["session"])
            player=row["player"]
            rd=float(row["round"])
            if not rd.is_integer() or not 1<=rd<=N_ROUNDS:
                raise ValueError("round outside original 1..100")
            rd=int(rd)
            key=(*session,player,rd)
            if key in participant_rounds:
                raise ValueError("player/round duplicate")
            participant_rounds.add(key)
            counts[session][rd]+=1
            cooperators[session][rd]+=int(row["action_player"]=="C")
            participants[session].add(player)
            by_treat[expected_tr]+=1
    if (len(participants)!=12 or sum(len(z) for z in participants.values())!=188 or
        by_treat["fix"]!=9200 or by_treat["rand"]!=9600):
        raise ValueError("real twelve session original participant universe changed")
    series={}
    for session,people in participants.items():
        if len(counts[session])!=N_ROUNDS or len(people)<2:
            raise ValueError("missing round or too few participants")
        if any(counts[session][t]!=len(people) for t in range(1,N_ROUNDS+1)):
            raise ValueError("one or more persons missing round from source")
        series[session]=tuple(cooperators[session][t]/len(people)
                              for t in range(1,N_ROUNDS+1))
    if len([k for k in series if k[0]=="fix"])!=6 or len([k for k in series if k[0]=="rand"])!=6:
        raise ValueError("missing experiment treatment session")
    return series,{"source_decisions":sum(by_treat.values()),
                   "sessions":len(series),"subjects":sum(map(len,participants.values())),
                   "cooperation_fixed_total":sum(cooperators[s].total() for s in series if s[0]=="fix"),
                   "cooperation_shuffled_total":sum(cooperators[s].total() for s in series if s[0]=="rand"),
                   "observed_rounds_per_session":N_ROUNDS,
                   "conditional_transition_scores":(N_ROUNDS-1)*len(series),
                   "source_submission_tag_commit":SUBMISSION_COMMIT,
                   "individual_participant_rows_exported":False}


def treatment_prior(series,training,test_treatment):
    sample=[x for key in training if key[0]==test_treatment for x in series[key]]
    if not sample:
        raise ValueError("training lacks same-treatment empirical prevalence")
    return sum(sample)/len(sample)


def mse_next(series,session,model,param,constant=None):
    values=series[session]
    error=[]
    for a,b in zip(values[:-1],values[1:]):
        p=predict(model,a,param,constant=constant)
        if not 0<=p<=1 or not math.isfinite(p):
            raise ValueError("invalid one-step cooperation prediction")
        error.append((p-b)**2)
    if len(error)!=N_ROUNDS-1:
        raise ValueError("one-step source temporal universe not 99 transitions")
    return sum(error)/len(error)


def fit_on_other_sessions(series,heldout,model):
    train=[s for s in sorted(series) if s!=heldout]
    if len(train)!=len(series)-1 or len(train)<2:
        raise ValueError("heldout session was used in training or too few groups")
    if model=="train_only_treatment_prevalence":
        value=treatment_prior(series,train,heldout[0])
        return {"parameter":"train_only_prevalence",
                "training_MSE":sum(
                    mse_next(series,s,model,{},constant=treatment_prior(series,
                             [v for v in train if v!=s and v[0]==s[0]],s[0]))
                    for s in train)/len(train),
                "constant":value}
    scores=[]
    for i,(name,param) in enumerate(variants(model)):
        m=sum(mse_next(series,s,model,param) for s in train)/len(train)
        scores.append((m,i,name,param))
    score,_,name,param=min(scores,key=lambda z:(z[0],z[1]))
    return {"parameter":name,"training_MSE":score,"param":param}


def evaluate(series):
    if len(series)!=12 or len([s for s in series if s[0]=="fix"])!=6 or len([s for s in series if s[0]=="rand"])!=6:
        raise ValueError("must use all 12 original session groups, 6 per treatment")
    if any(len(x)!=N_ROUNDS for x in series.values()):
        raise ValueError("source horizon mismatch")
    results={}
    for model in CLASSES:
        scores=[]
        chosen=Counter()
        for heldout in sorted(series):
            fit=fit_on_other_sessions(series,heldout,model)
            chosen[fit["parameter"]]+=1
            y=mse_next(series,heldout,model,fit.get("param",{}),
                       constant=fit.get("constant"))
            scores.append((heldout[0],y))
        mean=lambda x:sum(x)/len(x)
        results[model]={
            "global_session_equal_MSE":mean([q for t,q in scores]),
            "fixed_partner_session_equal_MSE":mean([q for t,q in scores if t=="fix"]),
            "shuffled_partner_session_equal_MSE":mean([q for t,q in scores if t=="rand"]),
            "heldout_sessions":12,
            "heldout_transitions":12*(N_ROUNDS-1),
            "training_only_parameter_selection_frequency":dict(sorted(chosen.items())),
            "session_names_or_round_series_exported":False,
        }
    return results


def run(folder):
    series,counts=load_session_series(folder)
    # The payoff difference is constant -1 in the author's exact stage game.
    for x in (0.,.1,.5,.9,1.):
        if abs(delta(x,REAL_PD)+1)>1e-12:
            raise ValueError("theory payoff regression failure")
    return {
        "study":"R067","stage":"E2_HUMAN_IPD_12_SESSION_LOSO_ONE_STEP",
        "status":"HUMAN_LOSO_12_SESSION_ONE_STEP_COMPLETE",
        "protocol":"protocols/R067_E2_HUMAN_IPD_SESSION_HELDOUT_2026-10-16.md",
        "source_repository":"eladiomontero/PairwiseStrategies",
        "source_commit":SUBMISSION_COMMIT,
        "source_blobs":{k:v[1] for k,v in FILES.items()},
        "source_data_universe":counts,
        "actual_PD_payoffs":REAL_PD,
        "target":"observed session cooperation share next round conditional on observed current round",
        "LOSO_models":evaluate(series),
        "experimental_phenotype":"repeated human partner matching, not random assignment of model mechanism",
        "author_original_HMM_inference":"NOT_REPRODUCED",
        "source_vs_final_Dryad_v8":"UNKNOWN",
        "external_E3":"OPEN",
        "psyen":"PESEN_v0.1_FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        x=run(a.source_dir)
    except (OSError,ValueError,UnicodeError,csv.Error) as e:
        x={"study":"R067","stage":"E2_HUMAN_IPD_12_SESSION_LOSO_ONE_STEP",
           "status":"FAIL_CLOSED",
           "error_type":type(e).__name__,"error":str(e)[:200],
           "individual_rows_exported":False,"psyen":"PESEN_v0.1_FROZEN"}
    a.output.write_text(json.dumps(x,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":x["status"],
                      "global_session_macro_MSE":{k:v["global_session_equal_MSE"]
                       for k,v in x.get("LOSO_models",{}).items()}},sort_keys=True))
    if x["status"]!="HUMAN_LOSO_12_SESSION_ONE_STEP_COMPLETE":
        raise RuntimeError("real original human one-step conditional prediction failed")


if __name__=="__main__":
    main()
