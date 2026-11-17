"""Synthetic readiness audit only; no human input/download/scoring entrypoint."""
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


def require(ok,reason):
    if not ok:raise ValueError(reason)


def digest(raw):return hashlib.sha256(raw).hexdigest()


def capture():
    pins=json.loads((HERE/'pins.json').read_text());out={}
    for path,want in pins.items():
        raw=(ROOT/path).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(blob==want['git_blob']==subprocess.check_output(['git','rev-parse','HEAD:'+path],cwd=ROOT,text=True).strip(),'SOURCE_BLOB:'+path)
        require(len(raw)==want['bytes'] and digest(raw)==want['sha256'],'SOURCE_BYTES:'+path)
        out[path]=want
    for p in [HERE/'pins.json',*sorted(HERE.glob('*.py'))]:
        raw=p.read_bytes();out[str(p.relative_to(ROOT))]={'bytes':len(raw),'sha256':digest(raw)}
    return out


def run(output):
    output.mkdir(parents=True,exist_ok=False);before=capture();commands=[]
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
    def execute(tag,args):
        result=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=60);streams={}
        for kind,raw in (('stdout',result.stdout),('stderr',result.stderr)):
            name=tag+'.'+kind
            if raw:(output/name).write_bytes(raw)
            streams[kind]={'file':name if raw else None,'bytes':len(raw),'sha256':digest(raw)}
        commands.append({'tag':tag,'argv':args,'cwd':str(ROOT),'exit_code':result.returncode,'streams':streams})
        (output/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        return result
    r=execute('new7',python+[str(HERE/'test_readiness.py')])
    require(r.returncode==0 and b'Ran 7 tests' in r.stderr and r.stderr.rstrip().endswith(b'OK'),'NEW_TESTS')
    candidate_path=ROOT/'research/codex_b/2026-11-10-r077-exact-score-candidate/candidate.py'
    original_code=candidate_path.read_text();controls=[]
    with tempfile.TemporaryDirectory(prefix='r077-readiness-') as td:
        for name,old,new in (
            ('alpha21','return (c+20*p0)/(n+20)','return (c+21*p0)/(n+21)'),
            ('wrong_history','key=tuple(event[i] for i in INDICES[model])','key=tuple(event[(i+1)%4] for i in INDICES[model])')):
            require(original_code.count(old)==1,'MUTATION_PREIMAGE')
            p=Path(td)/(name+'.py');p.write_text(original_code.replace(old,new))
            loader="import sys,types,unittest;from pathlib import Path;m=types.ModuleType('candidate');m.__file__=sys.argv[2];sys.modules['candidate']=m;exec(compile(Path(sys.argv[1]).read_text(),sys.argv[2],'exec'),m.__dict__);sys.path.insert(0,sys.argv[3]);from test_readiness import ReadinessTests;r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([ReadinessTests('test_integer_whole_scores_match_candidate_at_frozen_dimensions')]));sys.exit(0 if r.wasSuccessful() else 1)"
            r=execute('bad_'+name,python+['-c',loader,str(p),str(candidate_path),str(HERE)])
            require(r.returncode==1 and b'FAILED (failures=' in r.stderr and b'ERROR:' not in r.stderr,'MUTANT_NOT_ASSERTION_DETECTED')
            controls.append({'case':name,'old':old,'new':new,'sha256':digest(p.read_bytes()),'exit_code':1})
    from fixtures import candidate,original,donor_fixture,small_identity_fixture,one_event_targets,count_shaped_targets
    from integer_certificate import integer_scores,MODELS
    boundaries=[];pair=MODELS[1]+'_VS_'+MODELS[0]
    for name,(fit,source) in (('N9_C1',small_identity_fixture()),('N18424_C5_original_donor',donor_fixture('identity')[:2])):
        targets=one_event_targets();new=candidate.score_exact_brier(fit,targets);proof=integer_scores(source,targets)
        e=(0,0,0,0,0);p=original.predict(MODELS[0],e,fit);q=original.predict(MODELS[1],e,fit)
        witness=next(iter(proof['integer_session_witnesses'].values()))
        boundaries.append({'case':name,'data_class':'ARTIFICIAL_ONLY','source_events':len(source),'source_positive':sum(e[4] for e in source),
            'one_target_per_session':True,'old_probability_hex':[p.hex(),q.hex()],
            'old_probability_exact_binary_ratios':[p.as_integer_ratio(),q.as_integer_ratio()],
            'old_pair':original.score_with_frozen_source(fit,targets)['paired_differences'][pair],
            'candidate_pair':new['scores']['paired_differences'][pair],
            'integer_exact_pair':proof['exact_Brier']['paired_differences'][pair],
            'M0_integer_witness':witness[0],'M1_integer_witness':witness[1]})
        require(new['exact_Brier']==proof['exact_Brier'],'BOUNDARY_CERTIFICATE')
    (output/'single-event-boundaries.json').write_text(json.dumps(boundaries,indent=2)+'\n')
    full=count_shaped_targets();small={k:v for k,v in full.items() if k in ('ARTIFICIAL_TARGET_00','ARTIFICIAL_TARGET_01','ARTIFICIAL_TARGET_07','ARTIFICIAL_TARGET_08','ARTIFICIAL_TARGET_14')}
    comparisons=[]
    for kind in ('identity','varied'):
        fit,source,shape=donor_fixture(kind)
        for name,targets in (('15_sessions_1040_events',full),('five_unequal_sessions',small)):
            expected=integer_scores(source,targets)['exact_Brier'];actual=candidate.score_exact_brier(fit,targets)['exact_Brier']
            require(expected==actual,'FULL_INTEGER_CERTIFICATE')
            comparisons.append({'source':kind,'target':name,'source_shape':shape,'target_sessions':len(targets),
                'target_events':sum(len(s['events']) for s in targets.values()),'certificate':expected})
    (output/'four-integer-certificates.json').write_text(json.dumps(comparisons,indent=2)+'\n')
    after=capture();require(before==after,'SOURCE_CHANGED')
    result={'status':'COMPLETE_SYNTHETIC_READINESS_MATH_AUDIT','utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
        'optimized':bool(sys.flags.optimize),'new_methods':7,'new_single_event_boundaries':2,'full_certificates':4,
        'methods_not_repeated':'PR18_35_order_campaign_PR28_71_method_campaign_PR29_engineering_suite',
        'independent_route':'INTEGER_SOURCE_COUNTS_LCM_SQUARED_LOSS_CROSS_PRODUCTS_NO_FRACTION_OR_ORIGINAL_IMPORTS',
        'bad_candidate_controls':controls,'sources_before_after_equal':True,'sources':before,
        'synthetic_count_shape_is_real_data_qualification':False,'historical_human_vote_impact':'UNKNOWN',
        'human_scoring':'NOT_RUN_NOT_AUTHORIZED','production_adoption':'NOT_RUN','new_E2_E3':0,'formal_queue_closures':0,
        'external_team_replication':False,'CI':'NOT_RUN','full_repository_tests':'NOT_RUN','other_platforms':'NOT_RUN',
        'frozen_originals_and_results':'UNCHANGED'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','python','optimized','new_methods','new_single_event_boundaries','full_certificates','historical_human_vote_impact')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    run(p.parse_args().output.resolve())
