#!/usr/bin/env python3
"""Fixed-source, nonblind R251/S47 and R252/S48 archived CLI replay.

python -B research/codex_audit/r251_r252_cli/run_audit.py . --output /tmp/r251-r252
Only output and temporary files are written. Use separate output dirs concurrently.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

R251='research/validation/r251_s47_finite_window_exact_20261029.js'
B251='research/evidence_audit/b_r251_s47_independent_fraction_20261029.py'
E251='research/operations/e081_r251_s47_exact_receipt_20261029.js'
R252='research/validation/r252_s48_exact_source_information_20261029.js'
B252='research/evidence_audit/b_r252_s48_independent_numeric_oracle_20261029.py'
E252='research/operations/e082_r252_s48_source_numeric_20261029.js'
CSV251='research/R251/R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv'
CSV252='research/R252/R252_ALL_576_ORIGINAL_SIXBIT_INFORMATION_SOURCES.csv'
J251='research/validation/R251_S47_FINITE_WINDOW_EXACT_RECEIPT_2026-10-29.json'
J252='research/validation/R252_S48_FINITE_SAMPLE_INFORMATION_RECEIPT_2026-10-29.json'
F251='research/R251/R251_FINAL_ACCEPTANCE_STATUS.json'
F252='research/R252/R252_FINAL_ACCEPTANCE_STATUS.json'
SOURCES=(R251,B251,E251,R252,B252,E252,CSV251,CSV252,J251,J252,F251,F252)
COMPUTATION_KEYS={'research_id','source_rows','independent_cohorts','source_field_checks','failed_checks','worlds'}


def require(ok,message):
    if not ok:raise ValueError(message)


def equal_json(actual,archive):
    require(json.dumps(actual,sort_keys=True,allow_nan=False)==json.dumps(archive,sort_keys=True,allow_nan=False),
            'full JSON mismatch')


def check_251(actual,archive):
    require(type(actual) is dict and set(actual)==COMPUTATION_KEYS,'R251 computation key coverage')
    for key,value in actual.items():
        require(key in archive,'archive missing '+key)
        equal_json(value,archive[key])
    return sorted(set(archive)-set(actual))


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();root,out=a.root.resolve(),a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'execution.json').unlink(missing_ok=True)
    commands=[]
    def run(label,command,diagnostic=None):
        proc=subprocess.run(command,cwd=root,text=True,capture_output=True,timeout=60)
        (out/(label+'.stdout')).write_text(proc.stdout);(out/(label+'.stderr')).write_text(proc.stderr)
        commands.append({'label':label,'command':command,'cwd':str(root),'exit_code':proc.returncode})
        if diagnostic is None:require(proc.returncode==0,label+' failed; see stderr')
        else:require(proc.returncode!=0 and diagnostic in proc.stderr,label+' unexpected rejection diagnostic')
        return proc
    def node(script,*args):return ['node',str(root/script),*map(str,args)]
    def python(script,*args):return [sys.executable,'-B',str(root/script),*map(str,args)]
    def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
    for csv,formal in ((CSV251,F251),(CSV252,F252)):
        require(digest(root/csv)==json.loads((root/formal).read_text())['source_sha256'],'source SHA mismatch')
    j251=json.loads((root/J251).read_text());j252=json.loads((root/J252).read_text())
    generated251=json.loads(run('r251',node(R251,root/CSV251)).stdout)
    ignored=check_251(generated251,j251)
    b251=json.loads(run('b251_full_receipt',python(B251,root/J251)).stdout)
    e251=json.loads(run('e081_full_receipt',node(E251,root/J251)).stdout)
    require(b251.get('status')=='PASS' and b251.get('mutation_rejected') is True,'B251 outcome')
    require(e251.get('status')=='PASS' and e251.get('checks')==410 and e251.get('failures')==0,'E081 outcome')
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);generated=tmp/'r252_generated.json'
        run('r252',node(R252,root/CSV252,generated))
        equal_json(json.loads(generated.read_text()),j252)
        generated252_bytes_equal=generated.read_bytes()==(root/J252).read_bytes()
        generated252_hash=digest(generated)
        b252=json.loads(run('b252_full_receipt',python(B252,'--receipt',root/J252)).stdout)
        e252=json.loads(run('e082_full_receipt',node(E252,root/CSV252,root/J252)).stdout)
        require(b252['records_checked']==288 and b252['independent_numeric_metric_comparisons']==1152
                and b252['mutant_rejected'] is True,'B252 coverage')
        require(e252['records']==288 and e252['metric_checks']==1152 and e252['mutant_rejected'] is True,
                'E082 coverage')
        bad251=copy.deepcopy(j251);bad251['worlds'][0]['strict4_cohorts']+=1
        bad251path=tmp/'bad251.json';bad251path.write_text(json.dumps(bad251))
        run('negative_b251',python(B251,bad251path),'AssertionError: independent formula mismatch: worlds')
        run('negative_e081',node(E251,bad251path),'Error: mismatch at check')
        bad252=copy.deepcopy(j252);bad252['records'][0]['metrics']['I_XY']['approx_bits']=999
        bad252path=tmp/'bad252.json';bad252path.write_text(json.dumps(bad252))
        run('negative_b252',python(B252,'--receipt',bad252path),'AssertionError:')
        run('negative_e082',node(E252,root/CSV252,bad252path),'Error: numeric INDEPENDENT_BITS|0|8 I_XY')
        badcsv251=tmp/'bad251.csv';raw=(root/CSV251).read_bytes();badcsv251.write_bytes(b'X'+raw[1:])
        run('negative_r251_source',node(R251,badcsv251),'Error: header')
        badcsv252=tmp/'bad252.csv';raw=(root/CSV252).read_bytes();badcsv252.write_bytes(b'X'+raw[1:])
        run('negative_r252_source',node(R252,badcsv252,tmp/'must_not_exist.json'),'Error: original SHA256 mismatch')
    hashes={path:digest(root/path) for path in SOURCES};blobs={}
    for path in SOURCES:
        raw=(root/path).read_bytes();blobs[path]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    result={'status':'COMPLETE','python':sys.version,
            'node':subprocess.check_output(['node','--version'],text=True).strip(),
            'platform':platform.platform(),'seed':'R251 N/A; R252 frozen deterministic xorshift32, 8 replicates',
            'archived_clis_passed':6,'archived_clis_failed':0,'negative_cli_controls_rejected':6,
            'R251':{'computed_fields_match_archive':True,'full_json_match':False,
                    'archive_only_fields':ignored,'source_field_checks':generated251['source_field_checks'],
                    'B_cli':b251,'E081_cli':e251},
            'R252':{'full_json_match':True,'generated_bytes_equal':generated252_bytes_equal,
                    'generated_sha256':generated252_hash,'B_cli':b252,'E082_cli':e252,
                    'approximation_tolerance_bits':1e-10},
            'source_sha256':hashes,'source_git_blob':blobs,'commands':commands,
            'evidence_scope':'NONBLIND_INTERNAL_ARTIFICIAL_E1; independent numeric is not exact prime-log proof',
            'new_E2':0,'new_E3':0,'external_team_replications':0,'ci_status':'NOT_RUN',
            'full_repo_tests':'NOT_RUN','original_native_model_unit_tests':'NOT_RUN'}
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=out,delete=False) as tmp:
        tmp.write(json.dumps(result,indent=2)+'\n');staged=Path(tmp.name)
    staged.replace(out/'execution.json')
    print(json.dumps({'status':'COMPLETE','archived_clis':6,'negative_cli_controls':6,
                      'R251_computation_match':True,'R251_full_json_match':False,
                      'R252_full_json_match':True,'R252_numeric_comparisons_per_oracle':1152},indent=2))


if __name__=='__main__':main()
