#!/usr/bin/env python3
"""Original inline assertion controls using synthetic upstream snapshots only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import textwrap

import prepare


def controls(repo, receipt_path, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    output.mkdir(parents=True,exist_ok=False)
    receipt = json.loads(Path(receipt_path).read_bytes())
    source = json.loads(receipt['execution']['commands'][1]['streams']['stdout']['text'])
    wf = subprocess.check_output(['git','-C',str(repo),'show',prepare.BASE+':'+prepare.WORKFLOW]).decode()
    blocks = [textwrap.dedent(x) for x in re.findall(r"python - <<'PY'\n(.*?)\n          PY",wf,re.S)]
    if len(blocks) != 2:raise ValueError('HISTORICAL_INLINE_COVERAGE')
    records=[]
    with tempfile.TemporaryDirectory(prefix='r127-old-controls-') as directory:
        root=Path(directory);module_dir=root/'research/R127';module_dir.mkdir(parents=True)
        for name in ('test_r127_van_huyck_1990_min_effort_coordination_selection_exact.py',
                     'R127_VAN_HUYCK_1990_MIN_EFFORT_ORIGINAL_AER_TABLE2_AND_2X2_RISK_SCIENTIFIC_REPORT_2026-10-20.md'):
            (module_dir/name).write_bytes((repo/'research/R127'/name).read_bytes())
        functions=dict(zip(('published_1990_table2_verification','min_effort_security_and_payoff_rank',
                            'original_payoff_table_A','exhaustive_original_min_effort_payoff_audit',
                            'frozen_two_person_examples','exhaustive_two_player_symmetric_payoff_grid'),
                           ('original','equilibria','payoff_table','audit','toy','grid')))
        for name,section,key,value in [('valid',None,None,None),
            ('masked_e2','original','new_real_human_E2_prediction_scores',7),
            ('aggregate','original','source_reported_human_participants_not_reanalyzed',108),
            ('enumeration','audit','all_exact_individual_candidate_deviations',75118)]:
            upstream=copy.deepcopy(source)
            if section:upstream[section][key]=value
            module='import json\nDATA=json.loads('+repr(json.dumps(upstream))+')\n'+''.join(
                'def '+function+'():return DATA['+repr(field)+']\n' for function,field in functions.items())
            stub=module_dir/'r127_van_huyck_1990_min_effort_coordination_selection_exact.py';stub.write_text(module)
            for optimized in (False,True):
                expected=0 if name=='valid' or optimized else 1
                code='import sys;sys.path.insert(0,sys.argv[1]);\n'+blocks[1]
                command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['-c',code,str(module_dir)]
                child=subprocess.run(command,cwd=root,capture_output=True,timeout=60)
                label=name+('-optimized' if optimized else '-normal')
                for suffix,raw in (('stdout',child.stdout),('stderr',child.stderr)):(output/(label+'.'+suffix)).write_bytes(raw)
                if child.returncode!=expected:raise ValueError('OLD_CONTROL_CHANGED:'+label)
                record={'case':name,'optimized':optimized,'exit':child.returncode,'expected_exit':expected,
                        'inline_source_sha256':hashlib.sha256(blocks[1].encode()).hexdigest(),
                        'synthetic_module_sha256':hashlib.sha256(module.encode()).hexdigest(),
                        'stdout_sha256':hashlib.sha256(child.stdout).hexdigest(),
                        'stderr_sha256':hashlib.sha256(child.stderr).hexdigest()}
                if child.returncode==0:
                    path=module_dir/'R127_PHASE_A_1990_ORIGINAL_MIN_EFFORT_60_TEST_75117_DEVIATIONS_1296_2X2_CI_ACCEPTANCE.json'
                    old=json.loads(path.read_bytes());record['receipt_outer_E2']=old['new_real_person_level_E2_prediction_scores']
                    record['receipt_upstream_E2']=old['published_source_A_treatment_seven_experiments_p1_p10_only']['new_real_human_E2_prediction_scores']
                records.append(record)
        log_cases={'valid':'Ran 60 tests in 0.1s\n\nOK\n',
                   'wrong_count':'Ran 59 tests in 0.1s\n\nOK\n',
                   'trailing_ok':'Ran 60 tests in 0.1s\nFAILED (failures=1)\nOK\n',
                   'duplicate':'Ran 60 tests in 0.1s\nRan 60 tests in 0.1s\n\nOK\n'}
        for name,text in log_cases.items():
            path=root/'synthetic.log';path.write_text(text)
            if blocks[0].count("'/tmp/r127_real_unittests.log'")!=1:raise ValueError('LOG_PATH_PREIMAGE')
            code=blocks[0].replace("'/tmp/r127_real_unittests.log'",repr(str(path)))
            for optimized in (False,True):
                command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['-c',code]
                child=subprocess.run(command,cwd=root,capture_output=True)
                expected=0 if optimized or name in ('valid','trailing_ok') else 1
                if child.returncode!=expected:raise ValueError('OLD_LOG_CONTROL_CHANGED')
                label='log-'+name+('-optimized' if optimized else '-normal')
                for suffix,raw in (('stdout',child.stdout),('stderr',child.stderr)):(output/(label+'.'+suffix)).write_bytes(raw)
                records.append({'case':'log_'+name,'optimized':optimized,'exit':child.returncode,
                                'expected_exit':expected,'input_sha256':hashlib.sha256(text.encode()).hexdigest()})
    report={'workflow_blob':'4b22f653dc7516bb31ead23e45dcf7f62261d79d','controls':records,
            'scope':'Exact original inline code; log path redirected; stage2 upstream supplied by synthetic stub. Not real CI or a full pipeline bypass.',
            'original_math_rerun':False,'research_files_changed':False,'CI':'NOT_RUN'}
    (output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('repo',type=Path);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(controls(a.repo,a.receipt,a.output),indent=2))
