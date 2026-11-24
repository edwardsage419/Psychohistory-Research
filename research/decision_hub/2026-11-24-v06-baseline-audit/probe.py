"""Pinned v0.6 function fragments, not a full API or production test."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace as NS
from decimal import Decimal
import json, sys
import fragment as f

def fnv(s):
    h=2166136261
    b=s.encode('utf-16-le')
    for i in range(0,len(b),2): h=((h^int.from_bytes(b[i:i+2],'little'))*16777619)&0xffffffff
    return f'{h:08x}'

# Exact source contents modulo trailing whitespace at the splice boundaries.
s=Path(f.__file__).read_text()
ranges=[('BOUNDS =','def public_claims(','1d859fa7'),('def public_claims(','class Projector:','fd2547cf'),('    def _project(','GATE_ID =','73d3b4ca'),('GATE_ID =',None,'6ecd3f9a')]
for a,b,h in ranges:
    t=s[s.index(a):s.index(b) if b else len(s)]
    if a in ('BOUNDS =','    def _project('):t=t.rstrip()
    assert fnv(t)==h,(a,fnv(t))

# Only serialization/attribute adapter; deliberately not the real Pydantic state.
class State:
    def __init__(self,d):
        self.d=deepcopy(d)
        for k,v in d.items():setattr(self,k,v)
        self.constraints=[NS(horizon=None,**c) for c in d['constraints']]
        self.options=[NS(id=o['id'],label=o['label'],measurements={k:NS(horizon=None,**v) for k,v in o['measurements'].items()}) for o in d['options']]
    def model_dump(self,mode):return deepcopy(self.d)
    def model_copy(self,update):return State({**self.d,**update})
    @classmethod
    def model_validate(cls,d):return cls(d)
f.DecisionStateV05=State

def claim(i,field,value,unit,role='constraint',subject='',status='USER_CONFIRMED'):
    return dict(claim_id=i,claim=dict(field=field,value=value,unit=unit,role=role,subject=subject,source=f'fixture:{i}',kind='fact'),status=status,supersedes=None,recorded_at='fixture',confirmed_at='fixture' if status=='USER_CONFIRMED' else None)

def row(entries,dismissed=(),context=True,coupled=False,num_options=2):
    base=State(dict(question='synthetic choice',decision_id='fixture',revision=1,understanding_receipt=None,options=[],constraints=[],objectives=[],scenarios=[],weights={},shared_offsets={},reference_option_id=None,intended_option_id=None,plan_note=None,evidence=[],information=None,deadline=None,intent=None))
    opts={k:dict(id=k,label=k,status='CONFIRMED' if i<num_options else 'PROVISIONAL') for i,k in enumerate('AB')}
    return NS(ledger=NS(trace=lambda:dict(entries=entries,groups=[])),dismissed=set(dismissed),base=base,options=opts,context_confirmed=context,coupled=coupled,saved_revision=0,overrides=None,selected_plan=None,selected_option_id=None)

def observe(r):
    state=f.Projector()._project(r)
    gate=f.evaluate(NS(state=state))['feasibility'] if state.confirmed else None
    return dict(confirmed=state.confirmed,constraints_confirmed=state.constraints_confirmed,projected=[c.id for c in state.constraints],status={x['option_id']:x['status'] for x in gate} if gate else None,active=[x['id'] for x in f.active_claims(f.public_claims(r))],objectives=[o['id'] for o in state.d['objectives']])

def run():
    rows=[]
    for dim,field,metric,unit,threshold,a,b in [('cost','cost_max','cost','yuan','100','80','120'),('hours','hours_max','hours','hours/week','40','30','50'),('onsite','onsite_max','onsite','days/week','2','1','4'),('income','income_min','income','yuan/month','3000','4000','2000')]:
        measures=[claim('mA',metric,a,unit,'measurement','A'),claim('mB',metric,b,unit,'measurement','B')]
        for label,status,dismiss in [('pending','PROVISIONAL',[]),('confirmed','USER_CONFIRMED',[]),('dismissed','PROVISIONAL',['limit']),('explicit_no_constraint',None,[])]:
            entries=measures+([claim('limit',field,threshold,unit,status=status)] if status else [])
            out=observe(row(entries,dismissed=dismiss))
            want=None if label=='pending' else {'A':'ACCEPT','B':'REJECT'} if label=='confirmed' else {'A':'ACCEPT','B':'ACCEPT'}
            assert out['status']==want,(dim,label,out)
            rows.append(dict(dimension=dim,case=label,**out))
    checks=[]
    for name,kwargs in [('no context',{'context':False}),('coupled',{'coupled':True}),('one option',{'num_options':1})]:
        out=observe(row([],**kwargs));assert not out['confirmed'];checks.append(dict(name=name,**out))
    # A condition of unspecified activation is not universally binding. It also cannot be silently treated as absent.
    conditional=claim('cond','onsite_max','2','days/week','conditional',status='USER_CONFIRMED')
    out=observe(row([conditional,claim('mA','onsite','1','days/week','measurement','A'),claim('mB','onsite','4','days/week','measurement','B')]))
    assert out['confirmed'] and out['status']=={'A':'ACCEPT','B':'ACCEPT'} and not out['projected'];checks.append(dict(name='unsupported conditional excluded',**out))
    # Distinguish an objective from the only measured proxy; no actual ranking executed.
    out=observe(row([claim('goal','goal','生活质量','',role='goal'),claim('mA','income','4000','yuan/month','measurement','A'),claim('mB','income','3000','yuan/month','measurement','B')]))
    assert out['objectives']==['talk-income'];checks.append(dict(name='goal proxy objective generated',**out))
    return dict(python=sys.version.split()[0],cases=rows,controls=checks,dismissal_pairs=4,confirmed_exclusions=4,dismissed_accepts_b=4,scope='Original public_claims, active_claims, _project, build_state and evaluate functions; mock trace and model serialization, not full API, schema, language parser or decision hub')
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
