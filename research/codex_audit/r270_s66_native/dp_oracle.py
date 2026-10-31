"""Independent S66 prefix-state DP and integer-Beta factorial integration.

No imports from R/B; no list of all 64 replicated sequences or run compositions.
All published R/B outputs were known before implementation (nonblind).
"""
from collections import defaultdict
from fractions import Fraction as F
from math import factorial as fact

def require(ok,message):
    if not ok:raise ValueError(message)

def counts():
    # Prefix state: number of ones, adjacent-equality count, last bit.
    states={(0,0,0):1,(1,0,1):1}
    for _ in range(1,6):
        nxt=defaultdict(int)
        for (k,t,last),n in states.items():
            for bit in (0,1):nxt[k+bit,t+int(last==bit),bit]+=n
        states=nxt
    grouped=defaultdict(int)
    for (k,t,last),n in states.items():grouped[k,t]+=n
    require(sum(grouped.values())==64,'DP source mass')
    return dict(grouped)

def calculate():
    grouped=counts();tails={};alarms={}
    for a,b in ((1,1),(2,2),(1,3)):
        key=f'{a},{b}';ps=[]
        for obs in range(64):
            bits=f'{obs:06b}';K=bits.count('1');T=sum(bits[i]==bits[i+1] for i in range(5));A=a+K;B=b+6-K
            # B(A+k,B+6-k) / B(A,B), for each ordered replicate type.
            weights={(k,t):n*F(fact(A+k-1)*fact(B+5-k)*fact(A+B-1),
                                    fact(A+B+5)*fact(A-1)*fact(B-1)) for (k,t),n in grouped.items()}
            require(sum(weights.values(),F())==1,'predictive normalization')
            ps.append(sum((p for (k,t),p in weights.items() if t<=T),F()))
        tails[key]=[str(p) for p in ps]
        for theta in (F(1,4),F(1,2),F(3,4)):
            mass=[theta**i.bit_count()*(1-theta)**(6-i.bit_count()) for i in range(64)]
            require(sum(mass,F())==1,'generating normalization')
            for alpha in (F(1,20),F(1,10),F(1,5)):
                selected=[i for i,p in enumerate(ps) if p<=alpha];risk=sum((mass[i] for i in selected),F())
                alarms[f'{key}|{theta}|{alpha}']={'alarm_sequence_count':len(selected),'alarm_probability':str(risk),'probability_minus_nominal':str(risk-alpha)}
    return {'research':'R270_S66','evidence':'E1_ARTIFICIAL',
            'protocol':'R270_S66_PRIOR_PREDICTIVE_PPC_FALSE_ALARM_PRESCORE_FREEZE_2026-10-29.md',
            'observation_count_per_prior':64,'replicates_per_observation':64,
            'priors':['1,1','2,2','1,3'],'generating_thetas':['1/4','1/2','3/4'],
            'thresholds':['1/20','1/10','1/5'],'lower_tails':tails,'alarms':alarms}

def verify(data):
    expected=calculate()
    def check(value,want,path):
        require(type(value) is type(want),'type mismatch '+path)
        if type(want) is dict:
            require(set(value)==set(want),'keys mismatch '+path)
            for key in want:check(value[key],want[key],path+'/'+key)
        elif type(want) is list:
            require(len(value)==len(want),'length mismatch '+path)
            for i,(v,w) in enumerate(zip(value,want)):check(v,w,path+'/'+str(i))
        else:require(value==want,'value mismatch '+path)
    check(data,expected,'receipt')
    return {'status':'COMPLETE','exact_tails':192,'alarm_probabilities':27,
            'method':'prefix-state DP with factorial Beta integration',
            'predictive_normalizations':192,'generating_normalizations':9,
            'evidence':'NONBLIND_INTERNAL_ARTIFICIAL_E1','external_team_replications':0}
