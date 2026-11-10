"""Independent observed-spin even-moment expansion for frozen symmetric HMM.

No forward filtering, latent-path enumeration or original R/B imports. The
initial hidden spin is fair; transition correlation rho=2a-1, noise mean k=2q-1.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import json

STAYS=(F(1,4),F(1,2),F(3,4))
QUALITIES=(F(1,2),F(3,4),F(1))
TRUE_STAYS=(F(1,2),F(3,4))
FIELDS=("world","true_stay","true_emission","prefix","candidate_stay","candidate_emission",
        "true_prefix_mass","true_next1","candidate_prefix_evidence","candidate_next1",
        "conditional_brier","weighted_brier","weighted_excess")


def require(condition,reason):
    if not condition:raise ValueError(reason)


def parameters(a,q):
    require(type(a) is F and a in STAYS and type(q) is F and q in QUALITIES,"UNFROZEN_HMM_PROFILE")


@lru_cache(maxsize=54)
def terms(a,q,n):
    rho,kappa=2*a-1,2*q-1;found=[]
    for size in range(0,n+1,2):
        for subset in combinations(range(n),size):
            gaps=sum(subset[i+1]-subset[i] for i in range(0,size,2))
            found.append((subset,kappa**size*rho**gaps))
    return tuple(found)


@lru_cache(maxsize=1024)
def _probability(a,q,bits):
    value=F(0)
    for subset,moment in terms(a,q,len(bits)):
        sign=-1 if sum(bits[i]=='0' for i in subset)%2 else 1
        value+=sign*moment
    return value/(2**len(bits))


def probability(a,q,bits):
    parameters(a,q)
    require(type(bits) is str and len(bits)<=5 and set(bits)<={'0','1'},"UNFROZEN_OBSERVED_BITS")
    return _probability(a,q,bits)


def prediction(a,q,bits):
    require(type(bits) is str and len(bits)<=4,"FORECAST_HISTORY_LENGTH")
    mass=probability(a,q,bits);zero=probability(a,q,bits+'0');one=probability(a,q,bits+'1')
    require(mass>0 and zero+one==mass,"MOMENT_PARTITION_IDENTITY")
    return mass,one/mass


def world_name(a):return "IID_HIDDEN_NEGATIVE_CONTROL" if a==F(1,2) else "PERSISTENT_HMM"


def group_key(row):return '|'.join(row[k] for k in ("world","true_stay","candidate_stay","candidate_emission"))


def source_key(row):return group_key(row)+'|'+row['prefix']


@lru_cache(maxsize=1)
def _expected_json():
    sources={};groups=[];prefixes=[f'{i:04b}' for i in range(16)]
    for true in TRUE_STAYS:
        truth={s:prediction(true,F(3,4),s) for s in prefixes}
        require(sum((mass for mass,p in truth.values()),F(0))==1,"TRUE_PREFIX_NORMALIZATION")
        oracle=sum((mass*p*(1-p) for mass,p in truth.values()),F(0))
        for a in STAYS:
            for q in QUALITIES:
                risk=excess=F(0)
                for prefix in prefixes:
                    mass,p=truth[prefix];candidate_mass,f=prediction(a,q,prefix)
                    loss=p*(1-f)**2+(1-p)*f**2;weighted=mass*loss;gap=mass*(f-p)**2
                    row=dict(zip(FIELDS,map(str,(world_name(true),true,F(3,4),prefix,a,q,mass,p,candidate_mass,f,loss,weighted,gap))))
                    sources[source_key(row)]=row;risk+=weighted;excess+=gap
                require(risk-oracle==excess and excess>=0,"PROPER_SCORE_IDENTITY")
                groups.append({"world":world_name(true),"true_stay":str(true),"candidate_stay":str(a),"candidate_emission":str(q),
                    "prefixes":16,"expected_brier":str(risk),"oracle_brier":str(oracle),"excess_brier":str(excess),"fixed_half_brier":"1/4"})
    doc={"research_id":"R300","extension":"S96-v1","freeze_commit":"e7d5d6e7f9a82210fb5151c77a492303e1b20110",
         "B_plan_commit":"cd0eb73dd9b52b9a98a0a40d9f9628257bc44752",
         "scope":"E1_EXACT_KNOWN_PARAMETER_MISSPECIFIED_HMM_FORECAST_RISK","source_rows":288,"distinct_true_prefixes":32,
         "group_count":18,"results":groups,"original_R300_acceptance":"UNCHANGED","R073":"FROZEN","PESEN_v0_1":"FROZEN",
         "new_E2":0,"new_E3":0,"external_replication":"NOT_RUN"}
    return json.dumps({"document":doc,"sources":sources})


def expected():return json.loads(_expected_json())
