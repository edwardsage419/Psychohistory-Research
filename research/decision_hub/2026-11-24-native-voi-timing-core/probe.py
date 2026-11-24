"""Research-only tests of pinned native VOI and timing fragments."""
import itertools as it, json, sys
from fractions import Fraction as F
from decimal import Decimal as D
from types import SimpleNamespace as NS
from pathlib import Path
import voi as v
import timing as t
import probability as p


def point(x): return (x,x)
def row(lo,hi): return ((lo,hi),(1-hi,1-lo))
def problem(prior,l0,l1,u,c,actions=((0,1),(0,1))):
    return v.Problem(('s0','s1'),('z0','z1'),('A','B'),prior,(l0,l1),u,actions,c)
def direct(prior,likelihood,u,c,policy):
    baseline=max(sum(prior[s]*u[s][a] for s in range(2)) for a in range(2))
    return sum(prior[s]*likelihood[s][z]*u[s][policy[z]] for s in range(2) for z in range(2) if policy[z]>=0)-c-baseline

def run():
    counts=dict(point_cases=0,point_policy_checks=0,positive_net=0,zero_net=0,negative_net=0,interval_cases=0,interval_policy_checks=0,probability_rows=0,probability_valid=0,probability_invalid=0,timing_cases=0,timing_break_even_cases=0,timing_no_positive=0,timing_boundary_profitable=0)
    g=list(map(F,['0','1/2','1'])); util=[(tuple(F(x) for x in b[:2]),tuple(F(x) for x in b[2:])) for b in it.product([0,1],repeat=4)]
    for a,b,c in it.product(g,repeat=3):
        prior=(a,1-a);likelihood=((b,1-b),(c,1-c))
        for u,cost,actions in it.product(util,[F(0),F(1,4),F(1)], [((0,1),(0,1)),((0,),(1,))]):
            q=problem(row(a,a),row(b,b),row(c,c),u,cost,actions);mass=v.point_world(q);pv=v.payoffs(q,mass)
            assert sum(mass)==1
            pol=v.policies(q); values=[direct(prior,likelihood,u,cost,k) for k in pol]
            for k,w in zip(pol,values):
                assert v.net(q,pv,k)==w;counts['point_policy_checks']+=1
            n=v.net(q,pv);assert n==max(values)
            counts['point_cases']+=1;counts['positive_net' if n>0 else 'negative_net' if n<0 else 'zero_net']+=1
    intervals=list(it.combinations_with_replacement(g,2))
    for bounds in it.product(intervals,repeat=3):
        for u in util:
            q=problem(*(row(*b) for b in bounds),u,F(1,4));worlds=v.fixed_worlds(q)
            oracle=set(tuple(a*z for a,rr in zip((x,1-x),((y,1-y),(z,1-z))) for z in rr) for x,y,z in it.product(*[tuple(set(b)) for b in bounds]))
            assert set(worlds)==oracle
            for policy in v.policies(q):
                native=min(v.net(q,v.payoffs(q,m),policy) for m in worlds)
                vals=[direct((x,1-x),((y,1-y),(z,1-z)),u,F(1,4),policy) for x,y,z in it.product(*[[x for x in g if b[0]<=x<=b[1]] for b in bounds])]
                assert native==min(vals);counts['interval_policy_checks']+=1
            counts['interval_cases']+=1
    for bounds in it.product(intervals,repeat=3):
        raw={str(i):NS(kind='synthetic',source='fixture',lower=D(str(float(b[0]))),upper=D(str(float(b[1])))) for i,b in enumerate(bounds)}; errors=[]; kinds=set()
        got=p._probability_row(tuple(raw),raw,'fixture',errors,kinds)
        xs=[x for x in it.product(g,repeat=3) if sum(x)==1 and all(b[0]<=y<=b[1] for b,y in zip(bounds,x))]
        counts['probability_rows']+=1
        if not xs:assert got is None and errors;counts['probability_invalid']+=1
        else:
            assert got==tuple((min(x[i] for x in xs),max(x[i] for x in xs)) for i in range(3)) and not errors;counts['probability_valid']+=1
    cut=lambda at,inc=True,kind='synthetic',source='fixture': NS(at=F(at),inclusive=inc,kind=kind,source=source)
    for lo,hi in it.combinations_with_replacement(range(5),2):
        for due,inc in it.product(range(5),[True,False]):
            pr=NS(lower=F(lo),upper=F(hi),kind='synthetic',source='fixture');actual=t._relative(pr,cut(due,inc))
            flags=[(x<=due if inc else x<due) for x in range(lo,hi+1)];expected='WITHIN' if all(flags) else 'AFTER' if not any(flags) else 'STRADDLES'
            assert actual==expected;counts['timing_cases']+=1
    # Independent finite policy enumeration: each fixed policy has a linear payoff and earliest expiry.
    profiles=[(F(a),F(b)) for a,b in it.product([0,2,4],[0,1,2])]
    for cutoffA,cutoffB,inc,base,cost in it.product([1,3],[2,4],[True,False],[0,2],[0,1]):
        tm=NS(horizon=cut(4),decision_deadline=None,actions={'A':NS(cutoff=cut(cutoffA,inc)), 'B':NS(cutoff=cut(cutoffB,inc))},time_unit='day')
        for x,y in it.product(profiles,repeat=2):
            lines={'z0':{'A':x,'B':y},'z1':{'A':(F(1),F(1)),'B':(F(2),F(0))}}
            expected=[]
            for pol in it.product(['A','B'],repeat=2):
                intercept=sum(lines[z][a][0] for z,a in zip(lines,pol))-base-cost;rate=sum(lines[z][a][1] for z,a in zip(lines,pol))
                if intercept<=0:continue
                cap=min([F(4)]+[tm.actions[a].cutoff.at for a in pol]);end=min(cap,intercept/rate) if rate else cap
                expected.append(end)
            got=t._break_even(tm,lines,F(base),F(cost));counts['timing_break_even_cases']+=1
            if not expected:assert got is None;counts['timing_no_positive']+=1
            else:
                latest=max(expected);assert F(got['at'])==latest
                eligible=lambda a: latest<tm.actions[a].cutoff.at or (latest==tm.actions[a].cutoff.at and inc)
                profitable=any(all(eligible(a) for a in pol) and sum(lines[z][a][0]-latest*lines[z][a][1] for z,a in zip(lines,pol))>base+cost for pol in it.product(['A','B'],repeat=2))
                assert got['profitable_at_boundary']==profitable;counts['timing_boundary_profitable']+=profitable
    controls=[]
    def check(name,condition):
        assert condition,name;controls.append(name)
    raw={'a':NS(kind='unknown',source='fixture',lower=None,upper=None),'b':NS(kind='synthetic',source='fixture',lower=D('1'),upper=D('1'))};err=[]
    check('unknown probability rejected',p._probability_row(('a','b'),raw,'fixture',err,set()) is None and bool(err))
    raw['a']=NS(kind='synthetic',source='',lower=D('0'),upper=D('0'));err=[]
    check('missing probability source rejected',p._probability_row(('a','b'),raw,'fixture',err,set()) is None and bool(err))
    raw['a'].source='invented';err=[]
    check('nonempty invented source accepted (negative control)',p._probability_row(('a','b'),raw,'fixture',err,set()) is not None and not err)
    check('missing cutoff is unknown',t._relative(NS(kind='synthetic',source='fixture',lower=F(0),upper=F(1)),None)=='UNKNOWN')
    check('unconfirmed time is unknown',t.immediate_availability(NS(confirmed=False),'A')=='UNKNOWN')
    q=problem(row(F(0),F(0)),row(F(0),F(0)),row(F(0),F(0)),((F(1),F(0)),(F(0),F(1))),F(0),((),(0,1)))
    check('zero mass branch permits no action',v.net(q,v.payoffs(q,v.point_world(q)))==0)
    check('zero mass policy sentinel',v.policies(q)==((-1,0),(-1,1)))
    # Native shared core assumes validated input; a positive-mass empty action row fails.
    q=problem(row(F(0),F(0)),row(F(1),F(1)),row(F(1),F(1)),((F(1),F(0)),(F(0),F(1))),F(0),((),(0,1)))
    try:v.net(q,v.payoffs(q,v.point_world(q)));failed=False
    except ValueError:failed=True
    check('positive mass empty action row fails',failed)
    return dict(python=sys.version.split()[0],counts=counts,controls=controls,scope='native fragments with synthetic fixtures; not full model validators or registry; timing _exact is research adapter')
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
