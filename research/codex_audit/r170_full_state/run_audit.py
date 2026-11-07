#!/usr/bin/env python3
"""R170 nonblind full-state cross-language audit, no historical source edits.

python -B research/codex_audit/r170_full_state/run_audit.py . --output /tmp/r170
Distinct concurrent runs must use distinct output directories.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

JS='research/validation/r170_observation_ladder_20261026.js'
PY='research/evidence_audit/r170_b_edge_utterance_20261026.py'
RECEIPT='research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json'
SUMMARY='research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json'
SOURCES=(JS,PY,RECEIPT,SUMMARY)
GRAPHS=('path','star','cycle','complete')
INITIALS=('split','alternate','bilingual')
NOISES=('0','1/4','1/2')
MODES=('both_confirm','listener_only')
ALL_STATES=tuple(''.join(x) for x in product('123',repeat=4))
UNIVERSE=set(product(GRAPHS,INITIALS,NOISES,MODES,range(4)))


def require(ok,message):
    if not ok:raise ValueError(message)


def index_export(export):
    require(type(export) is dict and type(export.get('records')) is list,'snapshot list')
    rows=export['records']
    require(len(rows)==288,'288 snapshots required')
    indexed={}
    for row in rows:
        require(type(row) is dict and set(row)=={'graph','initial','nu','mode','t','law'},'snapshot fields')
        require(all(type(row[k]) is str for k in ('graph','initial','nu','mode'))
                and type(row['t']) is int,'snapshot identity types')
        key=tuple(row[k] for k in ('graph','initial','nu','mode','t'))
        require(key in UNIVERSE and key not in indexed,'duplicate/unknown snapshot')
        require(type(row['law']) is dict and bool(row['law']),'state law required')
        law={}
        for state,mass in row['law'].items():
            require(type(state) is str and re.fullmatch('[123]{4}',state) is not None,'invalid inventory state')
            require(type(mass) is str,'exact rational string required')
            value=F(mass)
            require(str(value)==mass and 0<value<=1,'canonical positive mass required')
            law[state]=value
        require(sum(law.values(),F())==1,'state law normalization')
        indexed[key]=law
    require(set(indexed)==UNIVERSE,'snapshot universe')
    return indexed


def compare_states(js,py):
    a,b=index_export(js),index_export(py)
    comparisons=0
    for key in UNIVERSE:
        for state in ALL_STATES:
            require(a[key].get(state,F())==b[key].get(state,F()),'state mass mismatch '+str((key,state)))
            comparisons+=1
    return {'snapshots':288,'state_mass_comparisons':comparisons,
            'nonzero_entries_per_route':sum(len(law) for law in a.values()),
            'exact_normalization_checks':576,'unreachable_zero_states_included':True}


def tv(a,b):
    return sum((abs(a.get(k,F())-b.get(k,F())) for k in set(a)|set(b)),F())/2


def count_law(law):
    out={}
    for state,p in law.items():
        count=state.count('3')
        out[count]=out.get(count,F())+p
    return out


def lex_witness(export,numeric=False):
    states=index_export(export)
    controls=sorted(product(NOISES,MODES),key=lambda x:(F(x[0]) if numeric else x[0],x[1]))
    for graph,initial in sorted(product(GRAPHS,INITIALS)):
        for t in (1,2,3):
            for a,b in combinations(controls,2):
                u,v=states[(graph,initial,*a,t)],states[(graph,initial,*b,t)]
                d1,d4=tv(count_law(u),count_law(v)),tv(u,v)
                if d1==0 and d4>0:
                    return {'graph':graph,'initial':initial,'t':t,'control_a':list(a),
                            'control_b':list(b),'tv_O1':str(d1),'tv_O4':str(d4)}
    return None


def main():
    parser=argparse.ArgumentParser();parser.add_argument('root',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root,out=args.root.resolve(),args.output.resolve()
    out.mkdir(parents=True,exist_ok=True);(out/'execution.json').unlink(missing_ok=True)
    here=Path(__file__).resolve().parent;commands=[]
    def run(label,command,filename):
        p=subprocess.run(command,cwd=root,text=True,capture_output=True,timeout=60)
        (out/filename).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
        commands.append({'label':label,'command':command,'cwd':str(root),'exit_code':p.returncode,'stdout_file':filename})
        require(p.returncode==0,label+' failed; see stderr')
        return json.loads(p.stdout)
    r=run('original_r_cli',['node',str(root/JS)],'R_replayed_receipt.json')
    b=run('original_b_cli',[sys.executable,'-B',str(root/PY)],'B_full_receipt.json')
    archived=json.loads((root/RECEIPT).read_text())
    summary=json.loads((root/SUMMARY).read_text())
    require(r==archived,'R CLI receipt differs from archived receipt')
    for key in ('aggregate','strata','first_witness','mutation_t1_full_TV'):
        require(r[key]==b[key],'R/B summary mismatch '+key)
    require(b['worlds']==72 and b['state_snapshots']==288 and b['normalized_snapshots']==288,'B coverage')
    require(b['monolingual_nu0_first_step_equal']==r['monolingual_nu0_first_step_equal_strata']==8,'monolingual control')
    require(r['mutation_t1_full_TV']=='1/24','mutation control')
    js=run('js_state_export',['node',str(here/'export_js_states.js'),str(root/JS)],'JS_full_state_export.json')
    py=run('python_state_export',[sys.executable,'-B',str(here/'export_python_states.py'),str(root/PY)],'Python_full_state_export.json')
    for payload,path in ((js,JS),(py,PY)):
        require(payload['source_sha256']==hashlib.sha256((root/path).read_bytes()).hexdigest(),'adapter source identity')
    exact=compare_states(js,py)
    negatives=[]
    for label,mutate in (
        ('duplicate_snapshot',lambda d:d['records'].__setitem__(1,copy.deepcopy(d['records'][0]))),
        ('missing_snapshot',lambda d:d['records'].pop()),
        ('boolean_time',lambda d:d['records'][0].update(t=False)),
        ('wrong_probability',lambda d:d['records'][0]['law'].update({next(iter(d['records'][0]['law'])):'999'})),
    ):
        bad=copy.deepcopy(py);mutate(bad)
        try:compare_states(js,bad)
        except ValueError:negatives.append({'case':label,'rejected':True})
        else:raise ValueError('false acceptance '+label)
    literal,numeric=lex_witness(js),lex_witness(js,numeric=True)
    require(literal==lex_witness(py) and numeric==lex_witness(py,numeric=True),'lexical witness route disagreement')
    hashes={};blobs={}
    for path in SOURCES:
        raw=(root/path).read_bytes();hashes[path]=hashlib.sha256(raw).hexdigest()
        blobs[path]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    braw=(out/'B_full_receipt.json').read_bytes()
    artifacts={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in out.glob('*.json') if p.name!='execution.json'}
    result={'status':'COMPLETE','full_frozen_extension_acceptance':'PARTIAL',
            'python':sys.version,'node':subprocess.check_output(['node','--version'],text=True).strip(),
            'platform':platform.platform(),'seed':'N/A; exact finite enumeration',
            'positive_original_clis':2,'positive_export_adapters':2,'full_state_comparison':exact,
            'R_archived_receipt_matches':True,'B_complete_receipt_matches_historical_digest':
                hashlib.sha256(braw).hexdigest()==summary['full_local_receipt_sha256'],
            'B_complete_receipt_matches_historical_bytes':len(braw)==summary['full_local_receipt_bytes'],
            'B_source_matches_historical_digest':hashes[PY]==summary['script_sha256_local'],
            'historical_witness':r['first_witness'],'literal_lex_first_witness':literal,
            'numeric_control_lex_first_witness':numeric,
            'historical_witness_matches_either_order':r['first_witness'] in (literal,numeric),
            'witness_order_limit':'Historical witness differs under both tested name-based lexical conventions. Frozen key/type order is unspecified; full compliance is NOT_ESTABLISHED/PARTIAL, not a uniquely proven ordering violation.',
            'negative_controls':negatives,'commands':commands,'source_sha256':hashes,
            'source_git_blob':blobs,'artifact_manifest':artifacts,
            'adapter_sha256':{n:hashlib.sha256((here/n).read_bytes()).hexdigest()
                              for n in ('export_js_states.js','export_python_states.py')},
            'evidence_scope':'NONBLIND_INTERNAL_ARTIFICIAL_E1; same-project algorithm comparison',
            'new_E2':0,'new_E3':0,'external_team_replications':0,'ci_status':'NOT_RUN',
            'original_111_tests':'NOT_RUN','original_1MB_result_reaudit':'NOT_RUN','full_repo_tests':'NOT_RUN'}
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=out,delete=False) as tmp:
        tmp.write(json.dumps(result,indent=2)+'\n');staged=Path(tmp.name)
    staged.replace(out/'execution.json')
    print(json.dumps({'status':'COMPLETE','protocol_acceptance':'PARTIAL',
                      'snapshots':288,'state_mass_comparisons':exact['state_mass_comparisons'],
                      'nonzero_entries':exact['nonzero_entries_per_route'],
                      'B_receipt_historical_hash_match':result['B_complete_receipt_matches_historical_digest'],
                      'witness_order_match':result['historical_witness_matches_either_order']},indent=2))


if __name__=='__main__':main()
