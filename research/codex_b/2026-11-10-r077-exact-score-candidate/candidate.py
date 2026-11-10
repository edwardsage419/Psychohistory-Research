"""Callable R077 exact-Brier candidate, preserving original log loss.

No raw-data entrypoint, fitting, downloads, historical writes or approval claim.
Exact probabilities implement the frozen mathematical count formulas, rather
than claiming to preserve every binary-float intermediate of the frozen code.
"""
from fractions import Fraction as F
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/R077'))
import r077_fourth_real_human_source_only_e3 as original
sys.path.insert(0,str(ROOT/'research/codex_b/2026-11-10-r077-exact-paired-ties'))
from exact_pair import session_risks,summarize,as_float_pair

MODELS=original.MODEL_NAMES
INDICES={MODELS[1]:(0,),MODELS[2]:(1,),MODELS[3]:(0,1),MODELS[4]:(0,1,2,3)}


def require(condition,reason):
    if not condition:raise ValueError(reason)


def source_prevalence(fit):
    """Recover an exact source ratio; require all four tables to agree.

    Consistency is not source authentication. Upstream must still establish
    donor membership, complete timelines and original dataset identity.
    """
    require(type(fit) is dict,'SOURCE_FIT')
    tables=fit.get('state_counts')
    require(type(tables) is dict and set(tables)==set(INDICES),'SOURCE_TABLES')
    for model,table in tables.items():
        require(type(table) is dict and bool(table),'SOURCE_TABLE_EMPTY')
        for key,count in table.items():
            require(type(key) is tuple and len(key)==len(INDICES[model]) and
                    all(type(v) is int and v in (0,1) for v in key),'SOURCE_STATE')
            require(type(count) is tuple and len(count)==2 and
                    all(type(v) is int for v in count) and 0<=count[0]<=count[1] and count[1]>0,'SOURCE_COUNTS')
    full=tables[MODELS[4]]
    for model,indices in INDICES.items():
        marginal={}
        for key,(c,n) in full.items():
            projected=tuple(key[i] for i in indices)
            old_c,old_n=marginal.get(projected,(0,0))
            marginal[projected]=(old_c+c,old_n+n)
        require(marginal==tables[model],'SOURCE_MARGINAL_INCONSISTENT')
    positive=sum(c for c,n in full.values());count=sum(n for c,n in full.values())
    require(0<positive<count,'SOURCE_DEGENERATE')
    require(type(fit.get('train_target_count')) is int and fit['train_target_count']==count,'SOURCE_COUNT')
    prevalence=fit.get('train_only_prevalence')
    exact=F(positive,count)
    require(type(prevalence) is float and math.isfinite(prevalence) and prevalence==float(exact),'SOURCE_PREVALENCE')
    return exact


def exact_prediction(model,event,fit,p0):
    """Internal: caller has validated source and five strict binary integers."""
    if model==MODELS[0]:return p0
    if model in INDICES:
        key=tuple(event[i] for i in INDICES[model])
        c,n=fit['state_counts'][model].get(key,(0,0))
        return (c+20*p0)/(n+20)
    if model==MODELS[5]:return F(19 if event[1] else 1,20)
    if model==MODELS[6]:return F(19 if event[0]==event[1] else 1,20)
    raise ValueError('UNKNOWN_MODEL')


def rational_strings(value):
    if type(value) is dict:return {k:rational_strings(v) for k,v in value.items()}
    return str(value) if type(value) is F else value


def score_exact_brier(fit,sessions):
    """Return compatible public scores plus an exact, anonymous certificate.

    Only Brier fields/votes are replaced. Original log loss and public metadata
    are computed by the unchanged scorer on the same inputs. No tolerance decides
    direction. The certificate preserves nonzero deltas even if JSON floats round.
    """
    require(original.ALPHA==20.0 and original.NOISE==0.05,'FROZEN_PARAMETERS')
    p0=source_prevalence(fit)
    require(type(sessions) is dict and bool(sessions),'EMPTY_SESSIONS')
    groups={0:[],1:[]}
    for sid,info in sessions.items():
        require(type(info) is dict and set(info)=={'treatment','events'},'SESSION_FIELDS')
        tr=info['treatment']
        require(type(tr) is int and tr in (0,1),'SESSION_TREATMENT')
        es=info['events']
        require(type(es) in (list,tuple) and bool(es),'EMPTY_EVENTS')
        for e in es:
            require(type(e) in (list,tuple) and len(e)==5 and
                    all(type(v) is int and v in (0,1) for v in e),'INVALID_EVENT')
        groups[tr].append(sid)
    require(all(groups.values()),'BOTH_TREATMENTS_REQUIRED')
    public=original.score_with_frozen_source(fit,sessions)
    risks={sid:{} for sid in sessions}
    exact_models={}
    for model in MODELS:
        for sid,info in sessions.items():
            records=[(e[4],p,p) for e in info['events']
                     for p in [exact_prediction(model,e,fit,p0)]]
            risks[sid][model]=session_risks(records)['candidate_Brier']
        mean=sum((risks[s][model] for s in sessions),F(0))/len(sessions)
        per_tr={str(tr):sum((risks[s][model] for s in ids),F(0))/len(ids) for tr,ids in groups.items()}
        public['models'][model]['all_original_sessions_equal_Brier']=float(mean)
        for tr,value in per_tr.items():
            public['models'][model]['per_treatment_original_session_equal'][tr]['Brier']=float(value)
        exact_models[model]={'all_original_sessions_equal_Brier':mean,'per_treatment_Brier':per_tr}
    exact_pairs={}
    for model,reference in original.PAIRS:
        paired_sessions={sid:{'treatment':info['treatment'],'records':[
            (e[4],exact_prediction(model,e,fit,p0),exact_prediction(reference,e,fit,p0))
            for e in info['events']]} for sid,info in sessions.items()}
        paired=summarize(paired_sessions)['paired']
        key=model+'_VS_'+reference
        public['paired_differences'][key]=as_float_pair(paired)
        exact_pairs[key]=paired
    return {'scores':public,'exact_Brier':rational_strings({
        'models':exact_models,'paired_differences':exact_pairs,'source_prevalence':p0})}
