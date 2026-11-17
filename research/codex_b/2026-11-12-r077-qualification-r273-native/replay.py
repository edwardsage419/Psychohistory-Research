"""Bounded R273 archived native CLIs; no real data, no new model or estimator."""
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from source_join import require,identical_bytes,compare_sources,compare_risks

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
R='research/validation/r273_s69_paired_target_rank_20261030.js'
B='research/evidence_audit/b_r273_s69_grouped_oracle_20261030.js'
ORIGINAL='research/R273/r273_exact_cross_population_prediction.py'
CSV='research/validation/R273_S69_ALL_576_PAIRED_SOURCE_ROWS_2026-10-30.csv'
JSON='research/validation/R273_S69_PAIRED_TARGET_RANK_EXACT_RESULTS_2026-10-30.json'
BASE_CSV='research/R273/R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv'
BASE_JSON='research/R273/R273_EXACT_CROSS_POPULATION_RESULTS.json'
BASE_RECEIPT='research/R273/R273_MACHINE_RECEIPT.json'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def capture():
    pins=json.loads((HERE/'pins.json').read_text());inputs={};fingerprints={}
    for name,pin in pins.items():
        raw=(ROOT/name).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(blob==pin['git_blob']==subprocess.check_output(['git','rev-parse','HEAD:'+name],cwd=ROOT,text=True).strip(),'SOURCE_IDENTITY:'+name)
        require(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'SOURCE_BYTES:'+name)
        inputs[name]=raw;fingerprints[name]=pin
    for p in [HERE/'pins.json',*sorted(HERE.glob('*.py'))]:
        raw=p.read_bytes();fingerprints[str(p.relative_to(ROOT))]={'bytes':len(raw),'sha256':sha(raw)}
    return inputs,fingerprints


def bad_receipts(doc):
    def copied():return json.loads(json.dumps(doc))
    bad={}
    d=copied();d['world_results'][1]=dict(d['world_results'][0]);bad['duplicate_world']=(d,'row duplicate/type')
    d=copied();d['world_results'].pop();bad['missing_world']=(d,'world count')
    d=copied();d['world_results'][0]['empirical_p_laplace_better']='9/8';bad['wrong_probability']=(d,'empirical_p_laplace_better')
    d=copied();d['real_human_E2']=1;bad['false_E2']=(d,'top real_human_E2')
    d=copied();d['world_results'][0]['source_types']=True;bad['boolean_count']=(d,'source_types')
    d=copied();d['world_results'][0]['wrong_rank_weight']+=1;bad['wrong_rank']=(d,'wrong_rank_weight')
    d=copied();d['s69_protocol_commit']='changed';bad['wrong_freeze']=(d,'top s69_protocol_commit')
    d=copied();d['world_results'][0]['tie_weight']+=1;bad['wrong_tie']=(d,'tie_weight')
    return bad


def run(output):
    output.mkdir(parents=True,exist_ok=False);inputs,before=capture();commands=[]
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
    def execute(tag,args,cwd=ROOT):
        r=subprocess.run(args,cwd=cwd,capture_output=True,timeout=60);streams={}
        for kind,raw in (('stdout',r.stdout),('stderr',r.stderr)):
            name=tag+'.'+kind
            if raw:(output/name).write_bytes(raw)
            streams[kind]={'file':name if raw else None,'bytes':len(raw),'sha256':sha(raw)}
        commands.append({'tag':tag,'argv':args,'cwd':str(cwd),'exit_code':r.returncode,'streams':streams})
        (output/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return r
    r=execute('new5tests',python+[str(HERE/'test_source_join.py')])
    require(r.returncode==0 and b'Ran 5 tests' in r.stderr and r.stderr.rstrip().endswith(b'OK'),'NEW_TESTS')
    node=execute('node_version',['node','--version']);require(node.returncode==0,'NODE_UNAVAILABLE')
    identities={};negative=[];expected_b={'worlds':9,'grouped_cells':135,'compared_fields':158}
    with tempfile.TemporaryDirectory(prefix='r273-native-') as td:
        temp=Path(td)
        for name in (R,B,ORIGINAL):(temp/Path(name).name).write_bytes(inputs[name])
        # Original --emit is normal isolated Python in both harness modes.
        # No optimized/assertion claim about the archived original is made.
        native=execute('original_R273_emit',[sys.executable,'-I','-B',str(temp/Path(ORIGINAL).name),'--emit'],temp)
        require(native.returncode==0,'ORIGINAL_EMIT_FAILED')
        for name in (BASE_CSV,BASE_JSON,BASE_RECEIPT):
            raw=(temp/Path(name).name).read_bytes();identical_bytes(raw,inputs[name])
            identities[name]={'bytes':len(raw),'sha256':sha(raw),'byte_identical':True}
        base_receipt=json.loads((temp/Path(BASE_RECEIPT).name).read_bytes())
        require(base_receipt['source_sha256']==sha(inputs[BASE_CSV]) and base_receipt['results_sha256']==sha(inputs[BASE_JSON]),'ORIGINAL_RECEIPT_DIGEST')
        require(json.loads(native.stdout)==base_receipt,'ORIGINAL_STDOUT_RECEIPT')
        selftest=execute('original_S69_selftest',['node',str(temp/Path(R).name),'--selftest'],temp)
        require(selftest.returncode==0 and selftest.stdout==b'PASS 9 worlds, 576 sources, analytic identities\n','S69_SELFTEST')
        for tag,flag,name in (('S69_csv','--csv',CSV),('S69_json','--json',JSON)):
            r=execute(tag,['node',str(temp/Path(R).name),flag],temp);require(r.returncode==0,'S69_EMIT')
            identical_bytes(r.stdout,inputs[name]);(temp/Path(name).name).write_bytes(r.stdout)
            identities[name]={'bytes':len(r.stdout),'sha256':sha(r.stdout),'byte_identical':True}
        archived=temp/'archived.json';archived.write_bytes(inputs[JSON])
        for label,path in (('archive',archived),('regenerated',temp/Path(JSON).name)):
            r=execute('original_B_'+label,['node',str(temp/Path(B).name),'--check',str(path)],temp)
            require(r.returncode==0 and json.loads(r.stdout)==expected_b,'NATIVE_B_CHECK')
        for name,(doc,marker) in bad_receipts(json.loads(inputs[JSON])).items():
            path=temp/(name+'.json');path.write_text(json.dumps(doc))
            r=execute('reject_'+name,['node',str(temp/Path(B).name),'--check',str(path)],temp)
            require(r.returncode==1 and b'Error:' in r.stderr and marker.encode() in r.stderr
                    and b'SyntaxError:' not in r.stderr and b'ReferenceError:' not in r.stderr,'BAD_RECEIPT_NOT_DOMAIN_REJECTED')
            negative.append({'case':name,'exit_code':1,'expected_domain_marker':marker,'artifact_sha256':sha(path.read_bytes())})
    joining=compare_sources(inputs[CSV],inputs[BASE_CSV]);risks=compare_risks(json.loads(inputs[JSON]),json.loads(inputs[BASE_JSON]))
    _,after=capture();require(before==after,'SOURCE_CHANGED_DURING_REPLAY')
    result={'status':'COMPLETE_BOUNDED_R273_NATIVE_REPLAY','utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
        'harness_optimized':bool(sys.flags.optimize),'node':node.stdout.decode().strip(),'new_unittest_methods':5,
        'original_python_emit_mode':'ISOLATED_NORMAL_I_B_IN_BOTH_HARNESS_MODES','original_unittest_suite':'NOT_RERUN',
        'source_identities':identities,'original_B_native':expected_b,'source_join':joining,'original_risk_field_checks':risks,
        'native_bad_receipts_rejected':negative,'sources_before_after_equal':True,'sources':before,
        'numerical_discrepancy_found':False,'new_mathematical_algorithm_claimed':False,
        'R077_human_scoring':'NOT_RUN_NOT_AUTHORIZED','new_human_E2_E3':0,'formal_queue_closures':0,'external_team_replications':0,
        'full_original_scientific_reacceptance':'NOT_RUN','production_integration':'NOT_RUN','CI':'NOT_RUN','other_platforms':'NOT_RUN',
        'R073_PESEN_protocols':'FROZEN_UNCHANGED'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','harness_optimized','node','new_unittest_methods','source_identities','original_B_native','source_join','original_risk_field_checks')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output.resolve())
