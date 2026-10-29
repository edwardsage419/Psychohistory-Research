#!/usr/bin/env python3
"""Nonblind fixed-source R248 S44 replay with explicit receipt coverage guards.

python -B research/codex_audit/r248_s44_replay/run_audit.py . --output /tmp/r248-s44
Writes only output and temporary copies. Concurrent runs need separate output dirs.
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

R='research/validation/r248_s44_finite_trajectory_exact_20261029.js'
B='research/evidence_audit/b_r248_s44_independent_formula_20261029.py'
E='research/operations/e078_r248_s44_source_receipt_third_route_20261029.js'
CSV='research/R248/R248_ALL_405_EXACT_MAP_IVP_TIME_SOURCES.csv'
RECEIPT='research/validation/R248_S44_FINITE_TRAJECTORY_EXACT_RECEIPT_2026-10-29.json'
FORMAL='research/R248/R248_FINAL_ACCEPTANCE_STATUS.json'
SOURCES=(R,B,E,CSV,RECEIPT,FORMAL)
META={'prescore_freeze_commit':'57e1f35d4263839178c6e86a4a314f92a32546d2',
      'source_git_blob':'c5eec783ab4199a1824a7fe36b0dfef1bde2b18b'}
KEYS={'research_id','evidence','original_source_rows','trajectories','comparison_points',
      'assertions','failures','summary','rows','new_E2','new_E3','R073','PESEN_v0_1'}
WORLDS=('AFFINE_CONTRACT_ZERO','AFFINE_CONTRACT_ONE','AFFINE_ALTERNATE_CONTRACT',
        'AFFINE_EXPAND_ZERO','IDENTITY_EVERY_POINT_FIXED','LOGISTIC_R2',
        'LOGISTIC_R3_BORDER','LOGISTIC_R4_REPELLER','CUBIC_NONHYPERBOLIC_ATTRACTOR')
INITIALS=('-1/2','-1/4','0','1/4','1/2','2/3','3/4','1','5/4')


def require(ok,message):
    if not ok:raise ValueError(message)


def check_receipt(generated,archive):
    require(type(generated) is dict and set(generated)==KEYS,'computed field coverage')
    require(type(archive) is dict and set(archive)==KEYS|set(META),'archive field coverage')
    for k,v in META.items():require(archive[k]==v,'frozen metadata '+k)
    rows=archive['rows']
    require(type(rows) is list and len(rows)==81,'81 rows required')
    seen=set()
    for row in rows:
        require(type(row) is dict,'row object required')
        key=(row['world'],row['x0'])
        require(key not in seen and key[0] in WORLDS and key[1] in INITIALS,'duplicate/unknown cohort')
        seen.add(key)
        require(type(row['distances']) is list and len(row['distances'])==5,'five distances required')
    require(seen=={(w,x) for w in WORLDS for x in INITIALS},'cohort coverage')
    actual=json.dumps(generated,sort_keys=True,allow_nan=False)
    expected=json.dumps({k:archive[k] for k in KEYS},sort_keys=True,allow_nan=False)
    require(actual==expected,'computed JSON mismatch')


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();root,out=a.root.resolve(),a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'execution.json').unlink(missing_ok=True);commands=[]
    def run(label,command,diagnostic=None):
        proc=subprocess.run(command,cwd=root,text=True,capture_output=True,timeout=60)
        (out/(label+'.stdout')).write_text(proc.stdout);(out/(label+'.stderr')).write_text(proc.stderr)
        commands.append({'label':label,'command':command,'cwd':str(root),'exit_code':proc.returncode})
        if diagnostic is None:require(proc.returncode==0,label+' failed; see stderr')
        else:require(proc.returncode!=0 and diagnostic in proc.stderr,label+' unexpected failure')
        return proc
    def node(script,*args):return ['node',str(root/script),*map(str,args)]
    def python(receipt):return [sys.executable,'-B',str(root/B),str(receipt)]
    raw=(root/CSV).read_bytes();csv_sha=hashlib.sha256(raw).hexdigest()
    require(csv_sha==json.loads((root/FORMAL).read_text())['source_sha256'],'source SHA')
    archive=json.loads((root/RECEIPT).read_text())
    generated=json.loads(run('r_node',node(R,root/CSV)).stdout)
    check_receipt(generated,archive)
    b=json.loads(run('b_python_full_receipt',python(root/RECEIPT)).stdout)
    require(b['cross_runtime_comparisons']==486 and b['trajectories']==81 and b['points']==405
            and b['failures']==0,'B full comparison coverage')
    e=json.loads(run('e078_node',node(E,root/CSV,root/RECEIPT)).stdout)
    require(e['assertions']==2886 and e['failures']==0,'E078 outcome')
    characterized=[]
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        for name,mutate,comparisons in (
            ('truncated',lambda d:d['rows'][0]['distances'].pop(),485),
            ('duplicate',lambda d:d['rows'].append(copy.deepcopy(d['rows'][0])),486)):
            bad=copy.deepcopy(archive);mutate(bad)
            path=tmp/(name+'.json');path.write_text(json.dumps(bad))
            accepted=json.loads(run('old_b_accepts_'+name,python(path)).stdout)
            require(accepted['cross_runtime_comparisons']==comparisons,'old B characterization changed')
            try:check_receipt(generated,bad)
            except ValueError:guard_rejected=True
            else:raise ValueError('new guard accepted '+name)
            characterized.append({'case':name,'old_B_exit_code':0,'old_B_comparisons':comparisons,
                                  'mutant_rows':len(bad['rows']),
                                  'first_distance_length':len(bad['rows'][0]['distances']),
                                  'new_guard_rejected':guard_rejected})
        bad=copy.deepcopy(archive);bad['rows'][0]['distances'][4]='999'
        path=tmp/'bad_value.json';path.write_text(json.dumps(bad))
        run('negative_b_distance',python(path),'AssertionError: distance mismatch')
        run('negative_e078_distance',node(E,root/CSV,path),'Error: receipt distance')
    blobs={};hashes={}
    for path in SOURCES:
        raw=(root/path).read_bytes()
        hashes[path]=hashlib.sha256(raw).hexdigest()
        blobs[path]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    result={'status':'COMPLETE','scope':'NONBLIND_INTERNAL_FINITE_ARTIFICIAL_E1',
            'python':sys.version,'node':subprocess.check_output(['node','--version'],text=True).strip(),
            'platform':platform.platform(),'seed':'N/A; deterministic exact rational trajectories',
            'positive_archived_clis':3,'positive_cli_failures':0,'B_full_receipt_comparisons':486,
            'R_assertions':generated['assertions'],'E078_result':e,
            'computed_JSON_matches_archive':True,'archive_metadata_verified':META,
            'raw_R_full_JSON_match':False,
            'metadata_note':'R does not emit the two archive-only provenance fields; explicitly verified separately',
            'old_B_false_acceptance_characterizations':characterized,
            'incorrect_distance_negative_clis_rejected':2,
            'source_sha256':hashes,'source_git_blob':blobs,'commands':commands,
            'full_repository_tests':'NOT_RUN','native_original_model_unittests':'NOT_RUN',
            'ci_status':'NOT_RUN','new_E2':0,'new_E3':0,'external_team_replications':0}
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=out,delete=False) as tmp:
        tmp.write(json.dumps(result,indent=2)+'\n');staged=Path(tmp.name)
    staged.replace(out/'execution.json')
    print(json.dumps({'status':'COMPLETE','B_cross_runtime_comparisons':486,
                      'positive_archived_clis':3,'old_B_false_acceptances_confirmed':2,
                      'new_guard_rejects_both':True,'wrong_distance_clis_rejected':2},indent=2))


if __name__=='__main__':main()
