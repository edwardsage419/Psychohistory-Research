"""Bounded synthetic R077 candidate replay; never invokes a human data run()."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def require(condition,reason):
    if not condition:raise ValueError(reason)


def capture():
    pins=json.loads((HERE/'pins.json').read_text());out={}
    for name,blob in pins.items():
        raw=(ROOT/name).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(actual==blob==subprocess.check_output(['git','rev-parse','HEAD:'+name],cwd=ROOT,text=True).strip(),'FROZEN_SOURCE_CHANGED:'+name)
        out[name]={'git_blob':blob,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    for p in [HERE/'pins.json',*sorted(HERE.glob('*.py'))]:
        raw=p.read_bytes();out[str(p.relative_to(ROOT))]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    return out


def replay(output):
    output.mkdir(parents=True,exist_ok=False);before=capture();commands=[]
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
    def execute(tag,args):
        result=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=60)
        streams={}
        for name,raw in (('stdout',result.stdout),('stderr',result.stderr)):
            filename=tag+'.'+name
            if raw:(output/filename).write_bytes(raw)
            streams[name]={'file':filename if raw else None,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        commands.append({'tag':tag,'argv':args,'cwd':str(ROOT),'exit_code':result.returncode,'streams':streams})
        (output/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        return result
    tests=[('candidate12',HERE/'test_candidate.py',12),
           ('originalR073',ROOT/'research/R073/test_r073_human_ipd_memory_loso.py',23),
           ('originalR077',ROOT/'research/R077/test_r077_fourth_real_human_source_only_e3.py',24),
           ('existing_exact_kernel',ROOT/'research/codex_b/2026-11-10-r077-exact-paired-ties/test_exact_pair.py',12)]
    for tag,path,count in tests:
        r=execute(tag,python+[str(path)])
        require(r.returncode==0 and f'Ran {count} tests'.encode() in r.stderr and r.stderr.rstrip().endswith(b'OK'),'TEST_FAILED:'+tag)
    old=execute('original_regression_FAIL_RETAINED',python+[str(ROOT/'research/codex_b/2026-11-10-r077-exact-paired-ties/legacy_regression.py')])
    require(old.returncode==1 and b'FAILED (failures=11)' in old.stderr and b'ERROR:' not in old.stderr,'ORIGINAL_35_11_REPRODUCTION_CHANGED')
    code=(HERE/'candidate.py').read_text();mutants=[]
    with tempfile.TemporaryDirectory(prefix='r077-exact-candidate-') as td:
        for name,old_line,new_line,test in [
            ('rounded_conditional','return (c+20*p0)/(n+20)','return F(float((c+20*p0)/(n+20)))','test_tiny_genuine_direction_not_rounded_or_toleranced'),
            ('decimal_prevalence','exact=F(positive,count)',"exact=F(str(fit['train_only_prevalence']))",'test_exact_source_ratio_and_unseen_state')]:
            require(code.count(old_line)==1,'MUTANT_PREIMAGE')
            mutant=Path(td)/(name+'.py');mutant.write_text(code.replace(old_line,new_line))
            loader="import sys,types,unittest;from pathlib import Path;m=types.ModuleType('candidate');m.__file__=sys.argv[2];sys.modules['candidate']=m;exec(compile(Path(sys.argv[1]).read_text(),sys.argv[2],'exec'),m.__dict__);sys.path.insert(0,str(Path(sys.argv[2]).parent));from test_candidate import CandidateTests;r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([CandidateTests(sys.argv[3])]));sys.exit(0 if r.wasSuccessful() else 1)"
            r=execute('bad_repair_'+name,python+['-c',loader,str(mutant),str(HERE/'candidate.py'),test])
            require(r.returncode==1 and b'FAILED (failures=1)' in r.stderr and b'ERROR:' not in r.stderr,'BAD_REPAIR_NOT_DETECTED')
            mutants.append({'name':name,'old':old_line,'new':new_line,'sha256':hashlib.sha256(mutant.read_bytes()).hexdigest(),'exit_code':1})
    # Explicitly retain the repository's absent root-discovery coverage.
    root=execute('root_unittest_discovery',python+['-m','unittest','discover','-v'])
    require(root.returncode==5 and b'Ran 0 tests' in root.stderr,'ROOT_DISCOVERY_CHANGED_REVIEW_REQUIRED')
    from candidate import score_exact_brier,original
    from case import legacy_fit,target_cases,integer_witness
    from test_candidate import tiny_case,PAIR
    diagnostics=[]
    for positions,sessions in target_cases():
        old_pair=original.score_with_frozen_source(legacy_fit(),sessions)['paired_differences'][PAIR]
        result=score_exact_brier(legacy_fit(),sessions)
        diagnostics.append({'positive_positions':positions,'old_pair':old_pair,'corrected_pair':result['scores']['paired_differences'][PAIR],
                            'exact_pair':result['exact_Brier']['paired_differences'][PAIR],
                            'integer_witness':integer_witness([e[4] for e in next(iter(sessions.values()))['events']])})
    (output/'synthetic35-diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    require(sum(d['old_pair']['sessions_better']==2 for d in diagnostics)==11,'OLD_FALSE_VOTE_COUNT')
    require(all(d['corrected_pair']['sessions_equal']==2 and d['exact_pair']['Brier_delta_all_original_sessions_equal']=='0' for d in diagnostics),'EXACT_TIE_REPAIR')
    fit,sessions,delta=tiny_case();tiny=score_exact_brier(fit,sessions)
    after=capture();require(before==after,'SOURCE_CHANGED_DURING_REPLAY')
    result={'status':'COMPLETE_SYNTHETIC_EXACT_BRIER_CANDIDATE','utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
            'optimized':bool(sys.flags.optimize),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'positive_unittest_method_executions':71,'candidate_methods':12,'original_R073_R077_methods':47,'existing_kernel_methods':12,
            'original_regression':'FAIL_RETAINED_11_OF_35','corrected_tie_orders':35,'original_false_improvement_orders':11,
            'tiny_true_delta':str(delta),'tiny_corrected_worse_sessions':tiny['scores']['paired_differences'][PAIR]['sessions_worse'],
            'bad_repairs_detected':mutants,'root_discovery':'NOT_A_PASS_EXIT5_NO_TESTS_RAN','full_repository_tests':'NOT_RUN_NO_GLOBAL_SUITE',
            'sources_before_after_equal':True,'sources':before,'historical_human_impact':'UNKNOWN','human_rescoring':'NOT_RUN',
            'production_adoption':'NOT_RUN_REQUIRES_OWNER_AND_CHATGPT_REVIEW','new_human_scores':0,'new_E2_E3':0,
            'external_team_replications':0,'scientific_queue_closures':0,'CI':'NOT_RUN','R073_PESEN_protocols':'FROZEN_UNCHANGED'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','python','optimized','positive_unittest_method_executions','original_regression','corrected_tie_orders','tiny_true_delta','historical_human_impact')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    replay(p.parse_args().output.resolve())
