"""Research only. Run with directory containing two pinned native files."""
import ast, hashlib, importlib.util, itertools, json, operator, sys
from pathlib import Path
from types import SimpleNamespace
import pydantic
from pydantic import ValidationError

ROOT = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent
HASHES = {'decision_state.py':'0840855431fbc88fe212785584277aa01be74d93','decision_feasibility.py':'6181d6c578c7ef251e9708d0ffcf65e95d35f88f'}
for name, expected in HASHES.items():
    b = (ROOT/name).read_bytes()
    if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=expected:
        raise ValueError('source identity mismatch: '+name)
spec=importlib.util.spec_from_file_location('native_state',ROOT/'decision_state.py')
state=importlib.util.module_from_spec(spec);sys.modules[spec.name]=state;spec.loader.exec_module(state)
# Execute unchanged native function ASTs. Registry construction/import intentionally excluded.
tree=ast.parse((ROOT/'decision_feasibility.py').read_text())
nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.Assign)) and not (isinstance(n,ast.ImportFrom) and n.level) and not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='METHOD' for t in n.targets))]
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(ROOT/'decision_feasibility.py'),'exec'),ns)
ops={'<=':operator.le,'<':operator.lt,'>=':operator.ge,'>':operator.gt}

def project(ledger, host):
    # Trusted synthetic fixture; never accept LLM-supplied confirmation flags.
    if not (host['confirmed'] and host['coverage'] and host['active']): return None
    if any(x['session']!=host['session'] or x['revision']!=host['revision'] or x['generation']!=host['generation'] or not x['confirmed'] for x in ledger): return None
    roles={'constraint','action','measurement'}
    if any(x['role'] not in roles or x['actor']!='self' or x['modality'] not in {'asserted','proposed'} for x in ledger): return None
    d={'decision_id':'0'*32,'revision':host['revision'],'question':'虚构预算决策','confirmed':True,'constraints_confirmed':True,'constraints':[],'options':[]}
    measurements=[]
    for x in ledger:
        if x['role']=='constraint': d['constraints'].append(x['value'])
        elif x['role']=='action': d['options'].append({**x['value'],'measurements':{}})
        else: measurements.append(x['value'])
    if not d['options'] or not d['constraints']: return None
    for m in measurements:
        matches=[o for o in d['options'] if o['id']==m['option']]
        if len(matches)!=1 or m['constraint'] in matches[0]['measurements']: return None
        matches[0]['measurements'][m['constraint']]=m['quantity']
    try: return state.DecisionState.model_validate(d)
    except ValidationError: return None

def fixture(op,threshold,lo,hi):
    h=dict(session='fixture',revision=1,generation=1,active=True,coverage=True,confirmed=True)
    common=dict(session='fixture',revision=1,generation=1,confirmed=True,actor='self',modality='asserted')
    c=dict(id='budget',label='费用',unit='CNY',operator=op,threshold=str(threshold),source='synthetic fixture',horizon='month')
    v=dict(lower=str(lo),upper=str(hi),unit='CNY',kind='synthetic',source='synthetic fixture',horizon='month')
    l=[dict(common,role='constraint',value=c),dict(common,role='action',value=dict(id='A',label='方案A')),dict(common,role='measurement',value=dict(option='A',constraint='budget',quantity=v))]
    return l,h

def run():
    counts={};n=0;controls=[]
    for op,t,lo,hi in itertools.product(ops,range(5),range(5),range(5)):
        if lo>hi: continue
        l,h=fixture(op,t,lo,hi);s=project(l,h)
        if s is None: raise AssertionError('valid state rejected')
        row=ns['evaluate'](SimpleNamespace(state=s))['feasibility'][0]
        truth=[ops[op](x,t) for x in range(lo,hi+1)]
        want='ACCEPT' if all(truth) else 'REJECT' if not any(truth) else 'UNRESOLVED'
        if row['status']!=want: raise AssertionError((op,t,lo,hi,row,want))
        counts[want]=counts.get(want,0)+1;n+=1
    def control(name,mut,expect):
        l,h=fixture('<=',2,1,2);mut(l,h);s=project(l,h)
        actual='BLOCKED' if s is None else ns['evaluate'](SimpleNamespace(state=s))['feasibility'][0]['status']
        if actual!=expect: raise AssertionError((name,actual,expect))
        controls.append(dict(name=name,result=actual))
    control('coverage missing',lambda l,h:h.update(coverage=False),'BLOCKED')
    control('owner confirmation missing',lambda l,h:h.update(confirmed=False),'BLOCKED')
    control('revoked',lambda l,h:h.update(active=False),'BLOCKED')
    control('stale revision',lambda l,h:h.update(revision=2),'BLOCKED')
    control('stale generation',lambda l,h:h.update(generation=2),'BLOCKED')
    control('foreign session',lambda l,h:h.update(session='elsewhere'),'BLOCKED')
    control('unconfirmed claim',lambda l,h:l[0].update(confirmed=False),'BLOCKED')
    control('third party',lambda l,h:l[0].update(actor='other'),'BLOCKED')
    control('conditional constraint',lambda l,h:l[0].update(modality='conditional'),'BLOCKED')
    control('omitted all constraints',lambda l,h:l.pop(0),'BLOCKED')
    control('unknown option reference',lambda l,h:l[2]['value'].update(option='B'),'BLOCKED')
    control('unknown constraint reference',lambda l,h:l[2]['value'].update(constraint='other'),'BLOCKED')
    control('duplicate measurement',lambda l,h:l.append(l[2]),'BLOCKED')
    control('reversed bounds',lambda l,h:l[2]['value']['quantity'].update(lower='4'),'BLOCKED')
    control('boolean numeric',lambda l,h:l[0]['value'].update(threshold=True),'BLOCKED')
    control('nonfinite',lambda l,h:l[0]['value'].update(threshold='NaN'),'BLOCKED')
    control('fabricated field',lambda l,h:l[0]['value'].update(approved=True),'BLOCKED')
    control('wrong unit',lambda l,h:l[2]['value']['quantity'].update(unit='USD'),'UNRESOLVED')
    control('wrong horizon',lambda l,h:l[2]['value']['quantity'].update(horizon='year'),'UNRESOLVED')
    control('missing measurement source',lambda l,h:l[2]['value']['quantity'].update(source=''),'UNRESOLVED')
    control('missing constraint source',lambda l,h:l[0]['value'].update(source=''),'UNRESOLVED')
    control('missing measurement',lambda l,h:l.pop(2),'UNRESOLVED')
    control('unknown quantity',lambda l,h:l[2]['value']['quantity'].update(kind='unknown',lower=None,upper=None),'UNRESOLVED')
    control('unknown with invented value',lambda l,h:l[2]['value']['quantity'].update(kind='unknown'),'BLOCKED')
    # Counterexample: schema and source strings do not prove real coverage or source truth.
    l,h=fixture('<=',2,1,2);l[0]['value']['source']='invented evidence label';s=project(l,h)
    counter=ns['evaluate'](SimpleNamespace(state=s))['feasibility'][0]['status']
    if counter!='ACCEPT': raise AssertionError('counterexample')
    return dict(environment=dict(python=sys.version.split()[0],pydantic=pydantic.__version__,supported=False),sources=HASHES,cases=n,counts=counts,controls=controls,source_string_counterexample=counter,scope='Native DecisionState import and unchanged AST functions; not complete registry, hub, Qwen, or real user consent')
if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
