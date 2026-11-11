#!/usr/bin/env python3
"""S96 module-export replay and complete-group false-accept reproduction."""
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from moments import prediction,require
from test_contract import CSV_PATH,JSON_PATH,bad_cases

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
R=ROOT/'research/validation/r300_s96_exact_misspecified_hmm_20261031.js'
B=ROOT/'research/evidence_audit/b_r300_s96_hidden_path_oracle_20261031.js'
ORIGINAL='research/R300/R300_EXACT_HMM_FORWARD_RESULTS.json'
PIN_SHA='09431d875e59be5d259afe6fafceaadb9ee2ab318231b364d3e2f203d1ddd114'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def capture():
    raw=(HERE/'pins.json').read_bytes();require(sha(raw)==PIN_SHA,'PIN_MANIFEST_CHANGED')
    pins=json.loads(raw);inputs={};fingerprints={}
    for name,pinned in pins.items():
        data=(ROOT/name).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        tracked=subprocess.check_output(['git','rev-parse','HEAD:'+name],cwd=ROOT,text=True).strip()
        require(blob==pinned==tracked,'PINNED_INPUT_CHANGED:'+name)
        inputs[name]=data;fingerprints[name]={'bytes':len(data),'sha256':sha(data),'git_blob':blob}
    for p in [HERE/'pins.json',HERE/'native_adapter.js',*sorted(HERE.glob('*.py'))]:
        data=p.read_bytes();fingerprints[str(p.relative_to(ROOT))]={'bytes':len(data),'sha256':sha(data)}
    return inputs,fingerprints


def original_parity(raw):
    doc=json.loads(raw);seen=set();checks=0
    for world in doc['worlds']:
        a=F(world['stay_probability'])
        for row in world['complete_source_records']:
            if row['prefix_length']!='4':continue
            prefix=row['prefix_bits'];key=world['world'],prefix
            require(key not in seen and len(prefix)==4,'ORIGINAL_PREFIX_ID');seen.add(key)
            mass,p=prediction(a,F(3,4),prefix)
            require(F(row['prefix_evidence'])==mass and F(row['predictive_next_observed_1'])==p,'ORIGINAL_PREFIX_PARITY')
            checks+=2
    require(len(seen)==32,'ORIGINAL_PREFIX_COVERAGE')
    return {'original_length4_prefixes':len(seen),'fraction_checks':checks}


def run(output):
    output.mkdir(parents=True,exist_ok=False);inputs,before=capture();commands=[]
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])

    def execute(tag,args):
        child=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=60);streams={}
        for suffix,raw in (('stdout',child.stdout),('stderr',child.stderr)):
            name=tag+'.'+suffix
            if raw:(output/name).write_bytes(raw)
            streams[suffix]={'bytes':len(raw),'sha256':sha(raw),'file':name if raw else None}
        commands.append({'tag':tag,'argv':args,'cwd':str(ROOT),'exit_code':child.returncode,'streams':streams})
        (output/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return child

    tests=execute('new-12-tests',python+['-m','unittest','discover','-s',str(HERE),'-p','test_contract.py','-v'])
    require(tests.returncode==0 and re.search(rb'Ran 12 tests in',tests.stderr) is not None,'NEW_TESTS_FAIL')
    archive=execute('new-audit-archive',python+[str(HERE/'audit.py'),str(CSV_PATH),str(JSON_PATH)])
    require(archive.returncode==0,'ARCHIVE_AUDIT_FAIL');proof=json.loads(archive.stdout)
    identity={};negatives=[]
    with tempfile.TemporaryDirectory(prefix='codex-b-r300-native-') as temporary:
        folder=Path(temporary);r,b,adapter=folder/'original_R.js',folder/'original_B.js',folder/'new_adapter.js'
        for path,original in ((r,R),(b,B)):path.write_bytes(inputs[str(original.relative_to(ROOT))])
        adapter.write_bytes((HERE/'native_adapter.js').read_bytes())
        node=execute('node-version',['node','--version']);require(node.returncode==0,'NODE_UNAVAILABLE')
        emitted=folder/'emitted'
        native=execute('new-adapter-original-R-export',['node',str(adapter),'emit',str(r),str(emitted)])
        require(native.returncode==0 and json.loads(native.stdout)=={'adapter':'NEW_CODEX_B_CALLS_ORIGINAL_EXPORT','rows':288,'groups':18},'ORIGINAL_R_EXPORT_FAILED')
        for path in (CSV_PATH,JSON_PATH):
            raw=(emitted/path.name).read_bytes();require(raw==inputs[str(path.relative_to(ROOT))],'EXPORTED_BYTE_MISMATCH')
            identity[path.name]={'bytes':len(raw),'sha256':sha(raw),'byte_equal':True}
        expected_old={'status':'PASS','rows':288,'groups':18,'exact_source_fields':2016,
                      'method':'full hidden-path 4/5 state enumeration','blind':'NONBLIND','external_replication':'NOT_RUN'}
        for label,a,j in (('archive',CSV_PATH,JSON_PATH),('emitted',emitted/CSV_PATH.name,emitted/JSON_PATH.name)):
            old=execute('new-adapter-old-B-'+label,['node',str(adapter),'audit',str(b),str(a),str(j)])
            require(old.returncode==0 and json.loads(old.stdout)==expected_old,'ORIGINAL_B_EXPORT_FAILED')
        again=execute('new-audit-emitted',python+[str(HERE/'audit.py'),str(emitted/CSV_PATH.name),str(emitted/JSON_PATH.name)])
        require(again.returncode==0 and json.loads(again.stdout)==proof,'EMITTED_AUDIT_MISMATCH')
        for name,csv_raw,json_raw in bad_cases():
            a,j=folder/'bad.csv',folder/'bad.json';a.write_bytes(csv_raw);j.write_bytes(json_raw)
            old=execute('old-'+name,['node',str(adapter),'audit',str(b),str(a),str(j)])
            rejected_before=name in ('missing_group','source_mass','group_risk')
            if rejected_before:
                marker={'missing_group':b'Error: result cardinality','source_mass':b'Error: source mismatch true_prefix_mass','group_risk':b'Error: group risk'}[name]
                require(old.returncode==1 and marker in old.stderr,'OLD_REJECTION_CHANGED')
            else:require(old.returncode==0 and json.loads(old.stdout)==expected_old,'OLD_FALSE_ACCEPT_NOT_REPRODUCED')
            new=execute('new-'+name,python+[str(HERE/'audit.py'),str(a),str(j)])
            failure=json.loads(new.stdout);require(new.returncode==2 and failure['status']=='REJECTED','BAD_ARTIFACT_ACCEPTED')
            negatives.append({'case':name,'old_exit':old.returncode,'old_false_accept':not rejected_before,
                              'new_exit':2,'new_reason':failure['reason'],'csv_sha256':sha(csv_raw),'json_sha256':sha(json_raw)})
        mutant=folder/'mutant';mutant.mkdir()
        for name in ('moments.py','audit.py','test_contract.py'):(mutant/name).write_bytes((HERE/name).read_bytes())
        p=mutant/'moments.py';code=p.read_text();old='kappa**size*rho**gaps';new='kappa**(size//2)*rho**gaps'
        require(code.count(old)==1,'MOMENT_MUTATION_PREIMAGE');p.write_text(code.replace(old,new))
        command='import sys,unittest;sys.path.insert(0,sys.argv[1]);from test_contract import MomentTests;r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([MomentTests("test_hand_anchors")]));sys.exit(0 if r.wasSuccessful() else 1)'
        wrong=execute('wrong-noise-moment-negative',python+['-c',command,str(mutant)])
        require(wrong.returncode==1 and b'FAILED (failures=1)' in wrong.stderr and b'ERROR:' not in wrong.stderr,'MOMENT_MUTANT_NOT_DETECTED')
        mutant_sha=sha(p.read_bytes())
    parity=original_parity(inputs[ORIGINAL]);_,after=capture();require(before==after,'SOURCE_CHANGED_DURING_REPLAY')
    result={'status':'PASS_COMPLETE_HMM_GROUPS_AND_INDEPENDENT_MOMENT_REPLAY','utc':datetime.now(timezone.utc).isoformat(),
            'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'python':sys.version,'optimized':bool(sys.flags.optimize),'node':node.stdout.decode().strip(),'new_unittest_methods':12,
            'source_fraction_checks':2016,'result_leaf_checks':176,'unique_model_groups':18,'native_export_identity':identity,
            'original_author_CLI':'NOT_ARCHIVED_MODULE_EXPORTS_ONLY','new_native_adapter':'CALLS_UNMODIFIED_ORIGINAL_EXPORTS_NOT_AN_ORIGINAL_CLI',
            'old_false_accepts':5,'old_correct_rejections':3,'new_bad_inputs_rejected':8,'negative_controls':negatives,
            'own_wrong_moment_mutant':{'exit_code':1,'sha256':mutant_sha},'original_parity':parity,'sources_before_after_equal':True,'sources':before,
            'original_numerical_discrepancy_found':False,'full_repository_tests':'NOT_RUN','original_R300_full_suite':'NOT_RUN','other_platforms':'NOT_RUN',
            'production_adoption':'NOT_RUN','CI':'NOT_RUN','new_human_scores':0,'new_E2_E3':0,'external_team_replications':0,'formal_queue_closures':0,
            'R073':'FROZEN_UNCHANGED','PESEN_v0.1':'FROZEN_UNCHANGED'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','optimized','new_unittest_methods','native_export_identity','old_false_accepts','new_bad_inputs_rejected','original_parity')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output.resolve())
