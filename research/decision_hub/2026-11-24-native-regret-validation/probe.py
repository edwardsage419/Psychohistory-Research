"""Native regret fragments; finite synthetic controls, no production registry."""
import hashlib, importlib.util, itertools, json, sys, copy
from pathlib import Path
from fractions import Fraction as F
from types import SimpleNamespace
import pydantic
ROOT=Path(sys.argv[1]); S=ROOT/'decision_state.py'; R=ROOT/'decision_regret.py'
STATE='0840855431fbc88fe212785584277aa01be74d93'; REGRET='e56689a54897d95eaa126540c23fca51cc0eede7'
def git_hash(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if git_hash(S)!=STATE: raise ValueError('state identity')
blocks=[('_validate','_utilities','cbfb81b5'),('_point_regret','_point_results','d0608b41'),('_regret_bounds','_interval_results','6d83554f'),('_precision_threshold','_witness_options','fcdf6f26')]
def fnv(s):
 b=s.encode('utf-16-le');h=2166136261
 for i in range(0,len(b),2):h=((h^int.from_bytes(b[i:i+2],'little'))*16777619)&0xffffffff
 return f'{h:x}'
if R.exists():
 if git_hash(R)!=REGRET:raise ValueError('regret identity')
 s=R.read_text();parts=[s[s.index('def '+a+'('):s.index('def '+b+'(')] for a,b,_ in blocks];mode='FULL_SOURCE_VERIFIED_FRAGMENT_EXECUTION'
else:
 s=(Path(__file__).parent/'fragment.py').read_text();starts=[s.index('def '+a+'(') for a,_,_ in blocks]+[len(s)];parts=[s[a:b] for a,b in zip(starts,starts[1:])];mode='CONNECTOR_FRAGMENT_FNV_MATCH'
if [fnv(x) for x in parts]!=[x[2] for x in blocks]:raise ValueError('fragment identity')
ns={};exec('from fractions import Fraction\ntype Points = dict[str, tuple[Fraction, ...]]\ntype Bound = tuple[Fraction, Fraction]\ntype Intervals = dict[str, tuple[Bound, ...]]\n'+''.join(parts),ns)
spec=importlib.util.spec_from_file_location('native_state31',S);st=importlib.util.module_from_spec(spec);sys.modules[spec.name]=st;spec.loader.exec_module(st)
keys=['A','B']; cells=list(itertools.combinations_with_replacement(range(3),2));stats=dict(point_cases=0,interval_cases=0,corner_worlds=0,precision_cases=0,strict_certificates=0,no_certificate_but_all_corners_strict=0,certificate_false=0);example=None
for p in itertools.product(range(3),repeat=4):
 points={k:tuple(F(x) for x in p[2*i:2*i+2]) for i,k in enumerate(keys)};actual=ns['_point_regret'](points);want={k:tuple(max(0,points[keys[1-i]][j]-points[k][j]) for j in range(2)) for i,k in enumerate(keys)}
 if actual!=want:raise AssertionError('point')
 stats['point_cases']+=1;worst={k:max(v) for k,v in actual.items()};lead=min(worst,key=worst.get);other=keys[1-keys.index(lead)]
 if worst[lead]==worst[other]:continue
 threshold=ns['_precision_threshold'](points,lead)
 for radius in map(F,['0','1/4','1/2','1','2']):
  intervals={k:tuple((v-radius,v+radius) for v in row) for k,row in points.items()};bounds=ns['_regret_bounds'](intervals);cert=max(x[1] for x in bounds[lead])<max(x[0] for x in bounds[other]);stats['precision_cases']+=1;stats['strict_certificates']+=cert
  if cert!=(radius<threshold):raise AssertionError('threshold')
  # Corner test only; strict corner dominance alone is not an interior proof.
  all_strict=True
  for a,b,c,d in itertools.product(*[tuple(set(x)) for k in keys for x in intervals[k]]):
   wA=max(0,c-a,d-b);wB=max(0,a-c,b-d);all_strict &= (wA<wB if lead=='A' else wB<wA)
  if cert and not all_strict:stats['certificate_false']+=1;raise AssertionError('certificate')
  if not cert and all_strict:
   stats['no_certificate_but_all_corners_strict']+=1
   if example is None:example=dict(points=p,leader=lead,radius=str(radius),threshold=str(threshold))
for q in itertools.product(cells,repeat=4):
 intervals={k:tuple(tuple(map(F,x)) for x in q[2*i:2*i+2]) for i,k in enumerate(keys)};v=ns['_regret_bounds'](intervals);observed={k:[[],[]] for k in keys};maxima={k:[] for k in keys}
 for a,b,c,d in itertools.product(*[tuple(set(x)) for x in q]):
  stats['corner_worlds']+=1;r={'A':[max(0,c-a),max(0,d-b)],'B':[max(0,a-c),max(0,b-d)]}
  for k in keys:
   for j in range(2):observed[k][j].append(r[k][j])
   maxima[k].append(max(r[k]))
 for k in keys:
  if v[k]!=tuple((min(x),max(x)) for x in observed[k]):raise AssertionError('cell bounds')
  if (max(x[0] for x in v[k]),max(x[1] for x in v[k]))!=(min(maxima[k]),max(maxima[k])):raise AssertionError('worst bounds')
 stats['interval_cases']+=1
q=lambda n:dict(lower=n,upper=n,unit='utility',kind='synthetic',source='fixture',horizon='year')
base=dict(decision_id='0'*32,revision=1,question='虚构选择',confirmed=True,constraints_confirmed=True,options=[dict(id=k,label=k) for k in keys],scenarios=[dict(id='s1',label='s1',kind='synthetic',source='fixture',utilities={'A':q(2),'B':q(1)})],scenario_basis='fixture common cardinal utility',scenario_dependence='rectangle',scenario_dependence_source='fixture',precision_radius='0.25')
controls=[]
def control(name,mut,expected,feasible=keys):
 d=copy.deepcopy(base);mut(d);s=st.DecisionState.model_validate(d);ctx=SimpleNamespace(state=s,feasible=tuple(o for o in s.options if o.id in feasible));errs=[ns[f](ctx) for f in ('_validate_points','_validate','_validate_precision')];actual=[not e for e in errs]
 if actual!=expected:raise AssertionError((name,actual,expected,errs))
 controls.append(dict(name=name,ready=actual,rectangle=ns['_rectangle'](ctx),errors=errs))
control('valid',lambda d:None,[True,True,True]);control('no basis',lambda d:d.update(scenario_basis=None),[False]*3);control('no scenarios',lambda d:d.update(scenarios=[]),[False]*3);control('missing cell',lambda d:d['scenarios'][0]['utilities'].pop('B'),[False]*3);control('unit conflict',lambda d:d['scenarios'][0]['utilities']['B'].update(unit='other'),[False]*3);control('horizon conflict',lambda d:d['scenarios'][0]['utilities']['B'].update(horizon='month'),[False]*3);control('missing source',lambda d:d['scenarios'][0]['utilities']['B'].update(source=''),[False]*3);control('interval utility',lambda d:d['scenarios'][0]['utilities']['B'].update(upper=2),[False,True,False]);control('missing radius',lambda d:d.update(precision_radius=None),[True,True,False]);control('single feasible',lambda d:None,[True,True,False],['A']);control('zero feasible',lambda d:None,[False]*3,[]);control('unknown scenario',lambda d:d['scenarios'][0].update(kind='unknown'),[False]*3);control('unknown dependence',lambda d:d.update(scenario_dependence='unknown',scenario_dependence_source=None),[True]*3);control('unverified source string',lambda d:d.update(scenario_dependence_source='invented'),[True]*3)
print(json.dumps(dict(mode=mode,python=sys.version.split()[0],pydantic=pydantic.__version__,state_blob=STATE,regret_blob=REGRET,fragment_hashes=[x[2] for x in blocks],stats=stats,example=example,controls=controls,scope='Synthetic; 3 native validators and mathematical fragments, not full native method execution'),ensure_ascii=False,indent=2))
