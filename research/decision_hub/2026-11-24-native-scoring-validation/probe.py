"""Native scoring fragments, synthetic exploratory evaluation only."""
import hashlib, importlib.util, itertools as it, json, sys, copy
from pathlib import Path
from fractions import Fraction as F
from types import SimpleNamespace as NS
import pydantic
root=Path(sys.argv[1]); S=root/'decision_state.py'; R=root/'decision_scoring.py'
state_blob='0840855431fbc88fe212785584277aa01be74d93'; scoring_blob='7832116703246bafc98831a6039d14c0d691cdd1'
def git_hash(p):
 b=p.read_bytes(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fnv(s):
 h=2166136261;b=s.encode('utf-16-le')
 for i in range(0,len(b),2):h=((h^int.from_bytes(b[i:i+2],'little'))*16777619)&0xffffffff
 return f'{h:x}'
blocks=[('_documented','_basic_errors','debc69fe'),('_basic_errors','_comparability','87614760'),('_score_bounds','_pareto','c262bcda'),('_weight_errors','_strict_relation','a122830c'),('_c034_errors','_joint_witness','936e6850')]
if git_hash(S)!=state_blob:raise ValueError('state identity')
if R.exists():
 if git_hash(R)!=scoring_blob:raise ValueError('source identity')
 s=R.read_text();parts=[s[s.index('def '+a+'('):s.index('def '+b+'(')] for a,b,_ in blocks];mode='FULL_SOURCE_VERIFIED_FRAGMENT_EXECUTION'
else:
 s=(Path(__file__).parent/'fragment.py').read_text();starts=[s.index('def '+a+'(') for a,_,_ in blocks]+[len(s)];parts=[s[a:b] for a,b in zip(starts,starts[1:])];mode='CONNECTOR_FRAGMENT_FNV_MATCH'
if [fnv(p) for p in parts]!=[x[2] for x in blocks]:raise ValueError('fragment mismatch')
spec=importlib.util.spec_from_file_location('native_state32',S);st=importlib.util.module_from_spec(spec);sys.modules[spec.name]=st;spec.loader.exec_module(st)
ns={k:getattr(st,k) for k in ['DecisionState','Objective','Option','Quantity','Weight']};ns['Context']=NS;exec('from fractions import Fraction\nfrom typing import NamedTuple\n'+''.join(parts),ns)
q=lambda lo,hi=None:dict(lower=lo,upper=lo if hi is None else hi,unit='utility',kind='synthetic',source='fixture',horizon='year')
base=dict(decision_id='0'*32,revision=1,question='虚构多目标决策',confirmed=True,constraints_confirmed=True,objectives=[dict(id=k,label=k,unit='utility',direction='max') for k in ['x','y']],options=[dict(id='A',label='A',scores={'x':q(2),'y':q(0)}),dict(id='B',label='B',scores={'x':q(0),'y':q(2)})],weights_confirmed=True,weights={k:dict(lower='0.25',upper='0.75') for k in ['x','y']},score_basis='fixture common cardinal scale',score_dependence='rectangle',score_dependence_source='fixture',score_transform='identity')
stats=dict(pareto_cases=0,pareto_worlds=0,weight_cases=0,weight_bound_sets=0,weight_grid_evaluations=0,clipping_cases=0,clipping_grid_evaluations=0,clipping_nonconstant=0);rels={};controls=[]
# Exact rectangular bounds. For every rectangular endpoint world compute point relation independently.
cells=list(it.combinations_with_replacement(range(3),2)); keys=['x','y']
for c in it.product(cells,repeat=4):
 for dirs in it.product(['max','min'],repeat=2):
  d=copy.deepcopy(base)
  for j,k in enumerate(keys):
   d['objectives'][j]['direction']=dirs[j]
   for i in range(2):d['options'][i]['scores'][k]=q(*c[2*i+j])
  s=st.DecisionState.model_validate(d);a,b=s.options;got=ns['_pareto_relation'](a,b,s);worlds=[]
  for a0,a1,b0,b1 in it.product(*[tuple(set(x)) for x in c]):
   ds=[(a0-b0)*(1 if dirs[0]=='max' else -1),(a1-b1)*(1 if dirs[1]=='max' else -1)]
   worlds.append('A_DOMINATES' if min(ds)>=0 and max(ds)>0 else 'B_DOMINATES' if max(ds)<=0 and min(ds)<0 else 'EQUAL' if ds==[0,0] else 'INCOMPARABLE')
  want=worlds[0] if len(set(worlds))==1 else 'UNRESOLVED'
  if got!=want:raise AssertionError((c,dirs,got,want))
  stats['pareto_cases']+=1;stats['pareto_worlds']+=len(worlds);rels[got]=rels.get(got,0)+1
# Three-dimensional weights on half-step bounds. All vertices of the box-simplex have half-step coordinates.
grid=[F(0),F(1,2),F(1)];bds=list(it.combinations_with_replacement(grid,2));simplex=[w for w in it.product(grid,repeat=3) if sum(w)==1]
for bounds in it.product(bds,repeat=3):
 ws=[w for w in simplex if all(lo<=v<=hi for v,(lo,hi) in zip(w,bounds))]
 if not ws:continue
 stats['weight_bound_sets']+=1
 for coeff in it.product(map(F,[-1,0,1]),repeat=3):
  vals=[sum(a*b for a,b in zip(coeff,w)) for w in ws];stats['weight_grid_evaluations']+=len(vals)
  for maximum,want in [(False,min(vals)),(True,max(vals))]:
   v,w=ns['_extreme'](list(coeff),list(bounds),maximum=maximum)
   if v!=want or sum(w)!=1 or not all(lo<=x<=hi for x,(lo,hi) in zip(w,bounds)):raise AssertionError('weight')
  stats['weight_cases']+=1
# Shared additive score error with clipping. All breakpoints in half-step grid.
grid=[F(i,2) for i in range(-2,4)]
for a,b in it.product(grid,repeat=2):
 for lo,hi in it.combinations_with_replacement(grid,2):
  low,high=ns['_clipping_cell'](a,b,NS(lower=lo,upper=hi));xs=[x for x in grid if lo<=x<=hi];vals=[min(F(1),max(F(0),a+x))-min(F(1),max(F(0),b+x)) for x in xs]
  if (low.difference,high.difference)!=(min(vals),max(vals)):raise AssertionError('clip')
  stats['clipping_cases']+=1;stats['clipping_grid_evaluations']+=len(xs);stats['clipping_nonconstant']+=min(vals)!=max(vals)
def control(name,mut,want):
 d=copy.deepcopy(base);mut(d);s=st.DecisionState.model_validate(d);ctx=NS(state=s,feasible=s.options);actual=[not ns[f](ctx) for f in ['_basic_errors','_weight_sensitivity_errors','_c034_errors']];pair=ns['_pareto_relation'](*s.options,s)
 if actual!=want:raise AssertionError((name,actual,want))
 controls.append(dict(name=name,validator_ready=actual,pair=pair))
control('valid',lambda d:None,[True]*3)
control('unconfirmed weights',lambda d:d.update(weights_confirmed=False),[True,False,False])
control('no common scale',lambda d:d.update(score_basis=None),[True,False,False])
control('missing weight',lambda d:d['weights'].pop('x'),[True,False,False])
control('infeasible sum',lambda d:d.update(weights={k:dict(lower='0.7',upper='0.8') for k in keys}),[True,False,False])
control('interval score',lambda d:d['options'][0]['scores']['x'].update(lower=1),[True,False,True])
control('missing score',lambda d:d['options'][0]['scores'].pop('x'),[True,False,False])
control('unit mismatch',lambda d:d['options'][0]['scores']['x'].update(unit='other'),[True,False,False])
control('time mismatch',lambda d:d['options'][0]['scores']['x'].update(horizon='month'),[True,False,False])
control('unknown dependence',lambda d:d.update(score_dependence='unknown'),[True,True,False])
control('unknown transform',lambda d:d.update(score_transform='unknown'),[True,True,False])
control('min objective',lambda d:d['objectives'][0].update(direction='min'),[True,True,False])
control('missing dependence source',lambda d:d.update(score_dependence_source=None),[True,True,False])
control('unverified basis text',lambda d:d.update(score_basis='invented'),[True,True,True])
control('shared offset missing',lambda d:d.update(score_dependence='shared_additive'),[True,True,False])
low,high=ns['_clipping_cell'](F(3,4),F(1,4),NS(lower=F(0),upper=F(1)));example={'nominal_difference':'1/2','identity_difference':'1/2','clipped_bounds':[str(low.difference),str(high.difference)]}
print(json.dumps(dict(mode=mode,python=sys.version.split()[0],pydantic=pydantic.__version__,state_blob=state_blob,scoring_blob=scoring_blob,fragment_hashes=[x[2] for x in blocks],stats=stats,pareto_relations=rels,controls=controls,example=example),ensure_ascii=False,indent=2))
