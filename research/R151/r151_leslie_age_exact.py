"""R151: project-created Leslie-like synthetic age cohort model.
Original Leslie 1945 / Keyfitz 1971 journal records checked, manuscripts not fully read.
All rates, examples and numeric results here are project-created E1 only.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json

HORIZON = 12
COHORTS = tuple((j, a, 12-j-a) for j in range(13) for a in range(13-j))
assert len(COHORTS) == 91
MULTIPLIERS = (F(0), F(1), F(3,2))
JUVENILE_SURVIVALS = (F(1,2), F(3,4))
ADULT_SURVIVALS = (F(1,2), F(2,3))
BASELINE = (F(1),F(3,4),F(2,3))
STABLE_SHARE = (F(4,9), F(1,3), F(2,9))
REPRODUCTIVE_VALUE = (F(1), F(4,3), F(1,2))

def rational(value):
    if type(value) is int:
        return F(value)
    if type(value) is F:
        return value
    raise TypeError("Only integers/Fraction allowed; bool and floats forbidden")

def state_vector(values):
    if not isinstance(values,(tuple,list)) or len(values)!=3:
        raise ValueError("exactly 3 age cohort coordinates needed")
    z=tuple(rational(v) for v in values)
    if any(v<0 for v in z):
        raise ValueError("negative cohort")
    return z

def params(k=F(1), sj=F(3,4), sa=F(2,3)):
    k,sj,sa=map(rational,(k,sj,sa))
    if k<0 or not 0<=sj<=1 or not 0<=sa<=1:
        raise ValueError("fertility and survival out of bounds")
    return k,sj,sa

def matrix_step(age,k=F(1),sj=F(3,4),sa=F(2,3),imm=(0,0,0)):
    j,a,o=state_vector(age)
    k,sj,sa=params(k,sj,sa)
    u=state_vector(imm)
    matrix=((F(0),k,k/2),(sj,F(0),F(0)),(F(0),sa,F(0)))
    return tuple(sum((matrix[i][z]*age[z] for z in range(3)),F(0))+u[i] for i in range(3))

def accounts_step(age,k=F(1),sj=F(3,4),sa=F(2,3),imm=(0,0,0)):
    j,a,o=state_vector(age)
    k,sj,sa=params(k,sj,sa)
    u=state_vector(imm)
    newborns=k*(a+o/2)
    juvenile_survivors=j*sj
    adult_survivors=a*sa
    deaths=(j-juvenile_survivors)+(a-adult_survivors)+o
    nxt=(newborns+u[0],juvenile_survivors+u[1],adult_survivors+u[2])
    assert sum(nxt)==sum((j,a,o))+newborns-deaths+sum(u)
    return nxt,dict(births=newborns,deaths=deaths,net_immigration=sum(u))

def run(initial,k=F(1),sj=F(3,4),sa=F(2,3),horizon=HORIZON,migration=(0,0,0)):
    if type(horizon) is not int or horizon<0 or horizon>128:
        raise ValueError("invalid horizon")
    age=state_vector(initial)
    k,sj,sa=params(k,sj,sa)
    m=state_vector(migration)
    path=[age]
    ledger=[]
    for t in range(horizon):
        inflow=m if t==0 else (F(0),F(0),F(0))
        new,account=accounts_step(age,k,sj,sa,inflow)
        assert new==matrix_step(age,k,sj,sa,inflow)
        ledger.append(account)
        path.append(new)
        age=new
    return path,ledger

def reproductive_value(age):
    age=state_vector(age)
    return sum((x*y for x,y in zip(REPRODUCTIVE_VALUE,age)),F(0))

def exact_closed_total(initial,t):
    if type(t) is not int or t<0 or t>128:
        raise ValueError("time out of range")
    age=state_vector(initial)
    C=reproductive_value(age)
    N0=sum(age)
    N1=sum(matrix_step(age,*BASELINE))
    a=N0-C
    b=3*C-N0-2*N1
    return C+(a+b*t)*F(-1,2)**t

def fraction_string(value):
    return str(value)

def annual_case(initial,k,sj,sa):
    trace,ledger=run(initial,k,sj,sa)
    return {
        "initial":list(initial),
        "fertility_multiplier":str(k),
        "juvenile_survival":str(sj),
        "adult_survival":str(sa),
        "age_trace":[[str(v) for v in state] for state in trace],
        "yearly_births":[str(z["births"]) for z in ledger],
        "yearly_deaths":[str(z["deaths"]) for z in ledger],
        "total_trace":[str(sum(state)) for state in trace],
    }

def ledger_recheck(rec):
    a=[tuple(F(v) for v in row) for row in rec["age_trace"]]
    k,sj,sa=F(rec["fertility_multiplier"]),F(rec["juvenile_survival"]),F(rec["adult_survival"])
    for t in range(HORIZON):
        nxt,acct=accounts_step(a[t],k,sj,sa)
        assert nxt==a[t+1]
        assert str(acct["births"])==rec["yearly_births"][t]
        assert str(acct["deaths"])==rec["yearly_deaths"][t]
        assert sum(a[t+1])==sum(a[t])+acct["births"]-acct["deaths"]
    return True

def output_data():
    cases=[annual_case(age,k,sj,sa) for age in COHORTS
           for k,sj,sa in product(MULTIPLIERS,JUVENILE_SURVIVALS,ADULT_SURVIVALS)]
    assert len(cases)==1092
    assert all(ledger_recheck(c) for c in cases)
    for cohort in COHORTS:
        age=state_vector(cohort)
        path,_=run(age,*BASELINE)
        C=reproductive_value(age)
        for t,step in enumerate(path):
            assert reproductive_value(step)==C
            assert sum(step)==exact_closed_total(age,t)
    examples={}
    for label,initial in {
        "young_only":(900,0,0),"adult_only":(0,900,0),
        "older_only":(0,0,900),"stationary":(400,300,200),
        "hidden_cohort":(120,360,420),
    }.items():
        t,_=run(initial,*BASELINE)
        examples[label]={"cohorts":list(initial),
                         "total_trace":[str(sum(x)) for x in t],
                         "eventual_limit":str(reproductive_value(initial))}
    migration={}
    for label,inc in {"none":(0,0,0),"young":(2,0,0),"adult":(0,2,0)}.items():
        tr,ledger=run((400,300,200),*BASELINE,migration=inc)
        migration[label]={"injection":list(inc),
                          "totals":[str(sum(s)) for s in tr],
                          "new_reproductive_value":str(reproductive_value(tr[1])),
                          "first_year_migration":str(ledger[0]["net_immigration"])}
    return {
        "research_id":"R151","original_data_reproduced":False,
        "source_full_leslie1945_article_read":False,
        "source_full_keyfitz1971_article_read":False,
        "all_project_synthetic":True,"new_E2":0,"new_E3":0,
        "horizon":HORIZON,"cases_count":len(cases),
        "cohort_initials":len(COHORTS),"fertility_levels":[str(x) for x in MULTIPLIERS],
        "juvenile_survival_levels":[str(x) for x in JUVENILE_SURVIVALS],
        "adult_survival_levels":[str(x) for x in ADULT_SURVIVALS],
        "stable_share":[str(x) for x in STABLE_SHARE],
        "left_reproductive_value":[str(x) for x in REPRODUCTIVE_VALUE],
        "baseline_charpoly":"(lambda-1)(lambda+1/2)^2",
        "examples":examples,"migration_age_comparisons":migration,
        "all_1092_full_trajectories":cases,
    }

def canonical_json():
    return json.dumps(output_data(),sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n"

if __name__=="__main__":
    print(canonical_json(),end="")
