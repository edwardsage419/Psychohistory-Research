"""Clone remote checkpoint, rebuild, rerun and restore real SQLite/artifacts.
No local checkout or previous task data is used as the recovery source.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--branch',default='feat/psychohistory-platform-v0.1')
    p.add_argument('--expected-sha',required=True)
    p.add_argument('--work-dir',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args()
    if a.work_dir.exists():raise ValueError('Recovery work directory must not already exist')
    a.work_dir.mkdir(parents=True)
    log=a.work_dir/'recovery.log';receipt={'status':'RUNNING','expected_sha':a.expected_sha,'steps':[]}
    def run(cmd,cwd=None,env=None):
        proc=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        with log.open('a') as f:f.write('$ '+' '.join(str(x) for x in cmd)+'\n'+proc.stdout+'\n')
        receipt['steps'].append({'command':[str(x) for x in cmd],'exit_code':proc.returncode})
        if proc.returncode:raise RuntimeError(f'Command failed ({proc.returncode}); real output in {log}')
        return proc.stdout
    try:
        clone=a.work_dir/'checkout'
        run(['git','clone','--depth','1','--single-branch','--branch',a.branch,'https://github.com/edwardsage419/Psychohistory-Research.git',str(clone)])
        sha=run(['git','rev-parse','HEAD'],clone).strip();receipt['restored_sha']=sha
        if sha!=a.expected_sha:raise ValueError('Remote checkpoint moved; no false exact-SHA claim')
        project=clone/'platform/future_model';env=os.environ.copy()
        env.pop('PH_VENV',None);env.pop('PYTHONPATH',None)
        env['PYTHONDONTWRITEBYTECODE']='1'
        run(['bash','scripts/install.sh'],project,env)
        run(['bash','scripts/verify.sh'],project,env)
        data=a.work_dir/'data'
        base=['bash','scripts/run.sh','--data',str(data),'--repo',str(clone)]
        output=json.loads(run(base+['demo','--seed','123','--rounds','6','--population','16'],project,env))
        result=output['result'];run_id=output['run']['id']
        fixture=json.loads((project/'examples/synthetic-result.json').read_text())
        if result!=fixture:raise ValueError('Recovered experiment differs from committed scientific payload')
        backup=a.work_dir/'backup';run(base+['backup',str(backup)],project,env)
        restored=a.work_dir/'restored-data'
        run(['bash','scripts/run.sh','--data',str(restored),'restore',str(backup)],project,env)
        result2=json.loads(run(['bash','scripts/run.sh','--data',str(restored),'result',run_id],project,env))
        if result2!=result:raise ValueError('Restored SQLite/artifact result differs')
        receipt.update(status='PASS',new_venv=True,npm_ci=True,remote_clone=True,experiment_reproduced=True,
                       sqlite_backup_restore=True,artifact_integrity=True,result_sha256=output['run']['result_hash'])
        print('Remote checkpoint recovery: PASS')
    except BaseException as exc:
        receipt.update(status='FAILED',error=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        receipt['log_sha256']=hashlib.sha256(log.read_bytes()).hexdigest() if log.exists() else None
        a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
