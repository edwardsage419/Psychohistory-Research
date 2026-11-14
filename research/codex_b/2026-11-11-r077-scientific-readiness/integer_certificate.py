"""Independent integer/common-denominator audit of synthetic R077 cases.

No Fraction/Decimal or original/candidate imports, float operations or fitting.
Source rows produce integer tables; squared errors share an LCM denominator.
Only rational strings and aggregate comparisons are needed to audit B28.
"""
from math import gcd,lcm

MODELS=('M0_TREATMENT_PREVALENCE','M1_OWN_LAST','M2_OPPONENT_LAST',
        'M3_JOINT_LAST','M4_JOINT_TWO_LAGS','M5_TFT_NOISY','M6_WSLS_NOISY')
PAIRS=((3,1),(4,3),(1,0),(2,0),(5,0),(6,0))


def require(ok,reason):
    if not ok:raise ValueError(reason)


def reduced(a,b):
    require(type(a) is int and type(b) is int and b>0,'INTEGER_RATIO')
    g=gcd(a,b);return a//g,b//g


def text(ratio):
    a,b=ratio;return str(a) if b==1 else f'{a}/{b}'


def average(ratios):
    require(bool(ratios),'EMPTY_MEAN')
    d=lcm(*(b for a,b in ratios))
    return reduced(sum(a*(d//b) for a,b in ratios),d*len(ratios))


def difference(left,right):
    a,b=left;c,d=right;return reduced(a*d-c*b,b*d)


def check_event(e):
    require(type(e) in (tuple,list) and len(e)==5 and all(type(x) is int and x in (0,1) for x in e),'BINARY_EVENT')


def codes(e):
    a,b,c,d,_=e
    return (a,b,2*a+b,8*a+4*b+2*c+d)


def source_counts(source):
    require(type(source) in (tuple,list) and bool(source),'EMPTY_SOURCE')
    tables=[[[0,0] for _ in range(n)] for n in (2,2,4,16)]
    positive=0
    for e in source:
        check_event(e);positive+=e[4]
        for table,key in zip(tables,codes(e)):
            table[key][0]+=e[4];table[key][1]+=1
    require(0<positive<len(source),'DEGENERATE_SOURCE')
    return positive,len(source),tables


def _probability(compiled,model,e):
    C,N,tables=compiled
    if model==0:return reduced(C,N)
    if 1<=model<=4:
        c,n=tables[model-1][codes(e)[model-1]]
        # Algebraically eliminate p0: (c + 20*C/N)/(n+20).
        return reduced(c*N+20*C,N*(n+20))
    if model==5:return (19 if e[1] else 1),20
    if model==6:return (19 if e[0]==e[1] else 1),20
    raise ValueError('UNKNOWN_MODEL')


def probability(source,model,event):
    check_event(event);return _probability(source_counts(source),model,event)


def session_risk(compiled,model,events):
    probabilities=[_probability(compiled,model,e) for e in events]
    d=lcm(*(b for a,b in probabilities))
    squared=sum((a*(d//b)-e[4]*d)**2 for (a,b),e in zip(probabilities,events))
    denominator=len(events)*d*d
    return reduced(squared,denominator),{'common_probability_denominator':d,
        'squared_integer_sum':squared,'risk_denominator':denominator}


def integer_scores(source,sessions):
    """Synthetic-only comparison certificate; no source eligibility assertion."""
    compiled=source_counts(source)
    require(type(sessions) is dict and bool(sessions),'EMPTY_SESSIONS')
    groups={0:[],1:[]};risks={};witnesses={}
    for sid,info in sessions.items():
        require(type(info) is dict and set(info)=={'treatment','events'},'SESSION_FIELDS')
        tr=info['treatment'];events=info['events']
        require(type(tr) is int and tr in groups,'TREATMENT')
        require(type(events) in (tuple,list) and bool(events),'EMPTY_EVENTS')
        for e in events:check_event(e)
        groups[tr].append(sid);risks[sid]=[];witnesses[sid]=[]
        for model in range(7):
            risk,witness=session_risk(compiled,model,events)
            risks[sid].append(risk);witnesses[sid].append(witness)
    require(all(groups.values()),'BOTH_TREATMENTS')
    models={name:{'all_original_sessions_equal_Brier':text(average([r[m] for r in risks.values()])),
                  'per_treatment_Brier':{str(tr):text(average([risks[s][m] for s in ids])) for tr,ids in groups.items()}}
            for m,name in enumerate(MODELS)}
    pairs={}
    for m,r in PAIRS:
        deltas={s:difference(row[m],row[r]) for s,row in risks.items()}
        def group(ids):
            values=[deltas[s] for s in ids]
            return {'sessions':len(ids),'Brier_delta':text(average(values)),
                    'better':sum(a<0 for a,b in values),'equal':sum(a==0 for a,b in values),'worse':sum(a>0 for a,b in values)}
        g=group(list(sessions))
        pairs[MODELS[m]+'_VS_'+MODELS[r]]={
            'Brier_delta_all_original_sessions_equal':g['Brier_delta'],
            'sessions_better':g['better'],'sessions_equal':g['equal'],'sessions_worse':g['worse'],
            'sessions':g['sessions'],'per_treatment':{str(tr):group(ids) for tr,ids in groups.items()}}
    return {'exact_Brier':{'models':models,'paired_differences':pairs,'source_prevalence':text(reduced(compiled[0],compiled[1]))},
            'integer_session_witnesses':witnesses}
