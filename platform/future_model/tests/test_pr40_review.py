"""Regression cases from the autonomous PR #40 engineering review."""
import gc
import hashlib
import json
import tracemalloc
import pytest


def test_discrete_probability_contract_requires_json_arrays():
    from psychohistory.contracts import uncertainty
    with pytest.raises(ValueError):
        uncertainty('DISCRETE', values=['a','b'], probabilities={.4:'a',.6:'b'})
    with pytest.raises(ValueError):
        uncertainty('DISCRETE', values={'a':1,'b':2}, probabilities=[.4,.6])
    with pytest.raises(ValueError):
        uncertainty('UNKNOWN',values=[0,1],probabilities=[.4,.6])


@pytest.mark.parametrize('state',[None,[],{'states':[0,None]},{'states':'01'},{'states':[False,1]}])
def test_plugin_restore_validates_individual_state(state):
    from psychohistory.plugins import Individual
    raw=json.dumps({'schema_version':'1.0.0','model_id':'individual','model_version':'1.0.0','state':state})
    with pytest.raises(ValueError):Individual().restore_state(raw)


def test_group_restore_validates_proportion_and_valid_roundtrips():
    from psychohistory.plugins import Individual,Group
    for plugin,state in [(Individual(),{'states':[0,1]}),(Group(),{'exposure':.3})]:
        assert plugin.restore_state(plugin.serialize_state(state))==state
    for state in [{'exposure':2},{'exposure':float('nan')},[]]:
        with pytest.raises(ValueError):Group().restore_state(json.dumps({'schema_version':'1.0.0','model_id':'group','model_version':'1.0.0','state':state}))


def test_correct_snapshot_hash_does_not_replace_envelope_validation():
    from psychohistory.state import Snapshot
    from psychohistory.contracts import canonical
    valid=Snapshot.create('individual','1.0.0',{'states':[1]},'main',None,[],{'python':'3.12'}).restore()
    for mutation in [lambda v:v.pop('model_id'),lambda v:v.update(parent_hash='not-a-sha'),lambda v:v.update(branch=''),lambda v:v.update(events={})]:
        value=json.loads(canonical(valid));mutation(value);raw=canonical(value)
        snap=Snapshot(raw,hashlib.sha256(raw.encode()).hexdigest())
        with pytest.raises(ValueError):snap.restore()


def test_restore_streams_objects_instead_of_materializing_archive(tmp_path):
    from psychohistory.storage import Store,restore_backup
    s=Store(tmp_path/'data')
    ids=[s.put({'index':i,'payload':'x'*(2*1024**2)}) for i in range(8)]
    s.backup(tmp_path/'backup');gc.collect();tracemalloc.start()
    restored=restore_backup(tmp_path/'backup',tmp_path/'restored')
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    assert peak<10*1024**2, f'Restore buffered archive: peak={peak}'
    assert all(restored.get(h)['index']==i for i,h in enumerate(ids))


def cli(root,*args):
    import os,subprocess,sys
    from pathlib import Path
    env=os.environ.copy();env['PYTHONPATH']=str(Path(__file__).resolve().parents[1]/'src')
    return subprocess.run([sys.executable,'-m','psychohistory.cli','--data',str(root),*args],env=env,text=True,capture_output=True,timeout=15)


@pytest.mark.parametrize('command',['runs','status','result','submit'])
def test_short_cli_commands_never_dispatch_unrelated_approved_work(tmp_path,command):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    with Scheduler(s) as q:r=q.submit({'rounds':100,'population':100})
    s.update_run(r['id'],status='APPROVED')
    s.create_run('complete',{});s.update_run('complete',status='APPROVED');s.update_run('complete',status='RUNNING');s.update_run('complete',status='COMPLETED',result_hash=s.put({'synthetic':True}))
    before=s.get_run(r['id'])
    args=[command]+([r['id']] if command=='status' else ['complete'] if command=='result' else [])
    result=cli(s.root,*args)
    assert result.returncode==0,result.stderr
    assert s.get_run(r['id'])==before


def test_cli_read_works_while_web_scheduler_owns_root(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    with Scheduler(s) as q:
        r=q.submit({})
        result=cli(s.root,'status',r['id'])
        assert result.returncode==0,result.stderr
        assert json.loads(result.stdout)['status']=='PENDING'


def test_cli_explicit_approval_preserves_unrelated_queue_and_exit_truth(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    with Scheduler(s) as q:
        old=q.submit({'rounds':100,'population':100});target=q.submit({'rounds':1,'population':2});bad=q.submit({})
    s.update_run(old['id'],status='APPROVED');s.update_run(bad['id'],code_sha256='0'*64)
    before=s.get_run(old['id'])
    result=cli(s.root,'approve',target['id'])
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)['status']=='COMPLETED'
    assert s.get_run(old['id'])==before
    denied=cli(s.root,'approve',bad['id'])
    assert denied.returncode!=0
    assert s.get_run(bad['id'])['status']=='BLOCKED'


def test_active_api_never_loses_old_pending_work(tmp_path):
    from fastapi.testclient import TestClient
    from psychohistory.api import create_app
    from psychohistory.storage import Store
    from pathlib import Path
    root=tmp_path/'data';s=Store(root);s.create_run('old-pending',{})
    for i in range(201):s.create_run(f'terminal-{i}',{});s.update_run(f'terminal-{i}',status='CANCELED')
    with TestClient(create_app(root,Path(__file__).resolve().parents[3],'test-token')) as c:
        active=c.get('/api/v1/runs/active',headers={'Authorization':'Bearer test-token'})
        assert active.status_code==200
        assert [r['id'] for r in active.json()]==['old-pending']


@pytest.mark.skipif(__import__('sys').platform!='linux',reason='Linux parent-death guard; native macOS NOT_RUN')
def test_killed_scheduler_cannot_leave_worker_publishing_results(tmp_path):
    import os,signal,subprocess,sys,time
    from pathlib import Path
    root=tmp_path/'data';helper=tmp_path/'owner.py'
    helper.write_text('''from psychohistory.storage import Store
from psychohistory.runtime import Scheduler
import sys,time
if __name__=='__main__':
    q=Scheduler(Store(sys.argv[1]));r=q.submit({'rounds':100,'population':100})
    q.approve(r['id'])
    while q.get(r['id'])['status']!='RUNNING':time.sleep(.001)
    print(q.get(r['id'])['worker_pid'],flush=True)
    while True:time.sleep(1)
''')
    env=os.environ.copy();env['PYTHONPATH']=str(Path(__file__).resolve().parents[1]/'src')
    owner=subprocess.Popen([sys.executable,str(helper),str(root)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    worker=None
    try:
        import select
        assert select.select([owner.stdout],[],[],10)[0], 'Owner did not report a worker within 10 seconds'
        worker=int(owner.stdout.readline().strip());owner.kill();owner.wait(timeout=5)
        until=time.monotonic()+5
        while time.monotonic()<until:
            stat=Path(f'/proc/{worker}/stat')
            if not stat.exists() or stat.read_text().split()[2]=='Z':break
            time.sleep(.02)
        assert not list((root/'staging').glob('*.json')),'Worker published after its scheduler was killed'
        assert not stat.exists() or stat.read_text().split()[2]=='Z','Orphan worker still running'
    finally:
        if owner.poll() is None:owner.kill();owner.wait()
        if worker:
            stat=Path(f'/proc/{worker}/stat')
            if stat.exists() and stat.read_text().split()[2]!='Z':os.kill(worker,signal.SIGKILL)
