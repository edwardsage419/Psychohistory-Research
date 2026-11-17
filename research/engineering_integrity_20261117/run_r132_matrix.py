import hashlib,json,os,subprocess,sys,time
from pathlib import Path
repo=Path(__file__).resolve().parents[2];logs=repo/'research/engineering_integrity_20261117/logs';logs.mkdir(exist_ok=True)
rows=[]
def run(name,args,env=None):
 p=subprocess.run(args,cwd=repo,env=env,capture_output=True,text=True,timeout=180)
 (logs/f'{name}.stdout').write_text(p.stdout);(logs/f'{name}.stderr').write_text(p.stderr)
 row={'name':name,'argv':args,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()};rows.append(row)
 if p.returncode:raise RuntimeError(row)
for mode in ['normal','optimized','environment']:
 env=os.environ.copy();env['PYTHONPATH']=str(repo/'research/R132');env.pop('PYTHONOPTIMIZE',None)
 if mode=='environment':env['PYTHONOPTIMIZE']='1'
 command=[sys.executable]+(['-O'] if mode=='optimized' else [])
 run(f'r132-phase-a-{mode}',command+['-m','unittest','-v','research/R132/test_r132_replicator_1978_exact_invariants_and_trajectories.py'],env)
 receipt=logs/f'r132-phase-b-{mode}.json'
 run(f'r132-phase-b-{mode}',command+['research/R132/r132_phase_b_ci_attest.py','--output',str(receipt)],env)
 r=json.loads(receipt.read_text())
 if r['actual_native_test_run']['tests_run']!=70 or r['actual_native_test_run']['returncode']!=0:raise RuntimeError('native test result mismatch')
 rows[-1].update(actual_tests=70,receipt=receipt.name,receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest(),optimization_level=r['optimization_level'])
base=os.environ.copy();base['PYTHONPATH']=str(repo/'research/R132');base.pop('PYTHONOPTIMIZE',None)
run('r132-integrity-controls',[sys.executable,'-m','unittest','-v','research/R132/test_r132_phase_b_attestation_integrity.py'],base)
(logs.parent/'R132_TEST_MATRIX.json').write_text(json.dumps({'rows':rows,'phase_a_tests_per_mode':70,'phase_b_native_tests_per_mode':70,'fault_injection_modes':['normal','python -O','PYTHONOPTIMIZE=1'],'fault_injection_cases_per_mode':24,'new_empirical_evidence':0},indent=2))
print('R132 Phase A/B matrix and integrity controls: PASS',len(rows),'commands')
