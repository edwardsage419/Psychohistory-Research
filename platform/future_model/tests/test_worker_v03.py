"""Real POSIX process controls and versioned sealed worker regressions."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest


PROJECT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, 'PYTHONPATH': str(PROJECT / 'src')}


def wait_file(path, process, timeout=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists():
            return path.read_text()
        if process.poll() is not None:
            pytest.fail(f'Child exited {process.returncode}: {process.stderr.read() if process.stderr else ""}')
        time.sleep(.01)
    pytest.fail('Worker readiness deadline expired')


def alive(pid):
    status = subprocess.run(['ps', '-o', 'stat=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(status) and not status.startswith('Z')


def await_gone(pid):
    deadline = time.monotonic() + 5
    while alive(pid) and time.monotonic() < deadline:
        time.sleep(.02)
    assert not alive(pid), f'Owned process {pid} survived'


def test_native_cpu_hard_limit_enforced_even_when_soft_signal_ignored(tmp_path):
    ready = tmp_path / 'cpu.json'
    code = '''import json,os,signal,sys
from pathlib import Path
from psychohistory.worker_lifecycle import configure_worker
limits=configure_worker(int(sys.argv[2]),cpu_seconds=1)
signal.signal(signal.SIGXCPU,signal.SIG_IGN)
Path(sys.argv[1]).write_text(json.dumps(limits))
while True:pass
'''
    worker = subprocess.Popen([sys.executable, '-c', code, str(ready), str(os.getpid())],
                              start_new_session=True, env=ENV, stderr=subprocess.PIPE, text=True)
    try:
        limits = json.loads(wait_file(ready, worker))
        assert limits['cpu'] == 'RLIMIT_CPU'
        assert limits['cpu_hard_seconds'] == 2
        assert limits['memory'] == ('RLIMIT_AS' if sys.platform == 'linux' else 'NOT_ENFORCED')
        worker.wait(timeout=8)
        assert worker.returncode == -signal.SIGKILL
    finally:
        if worker.poll() is None:
            os.killpg(worker.pid, signal.SIGKILL)
        worker.wait()


def test_owned_session_cancel_terminates_descendant_group(tmp_path):
    from psychohistory.worker_lifecycle import terminate_owned_group
    ready = tmp_path / 'group.json'
    code = '''import json,os,subprocess,sys,time
from pathlib import Path
from psychohistory.worker_lifecycle import configure_worker
configure_worker(int(sys.argv[2]))
child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
Path(sys.argv[1]).write_text(json.dumps({'parent':os.getpid(),'child':child.pid}))
while True:time.sleep(1)
'''
    worker = subprocess.Popen([sys.executable, '-c', code, str(ready), str(os.getpid())],
                              start_new_session=True, env=ENV, stderr=subprocess.PIPE, text=True)
    child = None
    try:
        receipt = json.loads(wait_file(ready, worker))
        child = receipt['child']
        terminate_owned_group(worker, signal.SIGTERM)
        worker.wait(timeout=5)
        await_gone(child)
    finally:
        if worker.poll() is None:
            os.killpg(worker.pid, signal.SIGKILL)
        worker.wait()
        if child and alive(child):
            os.kill(child, signal.SIGKILL)


def test_parent_watcher_kills_group_after_abrupt_owner_death(tmp_path):
    ready = tmp_path / 'orphan.json'
    child_code = '''import json,os,subprocess,sys,time
from pathlib import Path
from psychohistory.worker_lifecycle import watch_parent
watch_parent(int(sys.argv[2]))
child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
Path(sys.argv[1]).write_text(json.dumps({'worker':os.getpid(),'child':child.pid}))
while True:time.sleep(1)
'''
    # Disabling prctl exercises the same parent watcher used on native Darwin.
    owner_code = '''import os,subprocess,sys,time
subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2],str(os.getpid())],start_new_session=True)
while True:time.sleep(1)
'''
    owner = subprocess.Popen([sys.executable, '-c', owner_code, child_code, str(ready)],
                             env=ENV, stderr=subprocess.PIPE, text=True)
    receipt = None
    try:
        receipt = json.loads(wait_file(ready, owner))
        owner.kill();owner.wait(timeout=5)
        await_gone(receipt['worker']);await_gone(receipt['child'])
    finally:
        if owner.poll() is None:
            owner.kill();owner.wait()
        if receipt:
            for pid in receipt.values():
                if alive(pid):os.kill(pid,signal.SIGKILL)


def test_group_signal_never_targets_callers_group():
    from psychohistory.worker_lifecycle import terminate_owned_group
    process = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(60)'])
    try:
        with pytest.raises(ValueError, match='session'):
            terminate_owned_group(process, signal.SIGTERM)
        assert process.poll() is None
    finally:
        process.kill();process.wait()


def test_trajectory_submission_has_no_holdout_and_blocks_stale_identity(tmp_path):
    from psychohistory.runtime import Scheduler
    from psychohistory.storage import Store
    from psychohistory.v02_execution import RUN_KIND_TRAJECTORY
    store = Store(tmp_path / 'data')
    config = {'model_id':'r123-degroot','model_version':'1.0.0','source_id':'source',
              'source':{},'parameters':{},'start':None,'branch_from':None}
    with Scheduler(store, trajectory_verifier=lambda config: None) as scheduler:
        run = scheduler.submit_trajectory(config, '0' * 64)
        assert run['kind'] == RUN_KIND_TRAJECTORY
        assert run.get('holdout_id') is None and run.get('holdout_started_at') is None
        scheduler.approve(run['id'])
        final = scheduler.wait(run['id'], 5)
        assert final['status'] == 'BLOCKED'
        assert final['result_hash'] is None


def test_trajectory_submission_requires_verifier_and_valid_timeout(tmp_path):
    from psychohistory.runtime import Scheduler
    from psychohistory.storage import Store
    with Scheduler(Store(tmp_path / 'data')) as scheduler:
        assert hasattr(scheduler, 'submit_trajectory'), 'Trajectory execution entry point missing'
        with pytest.raises(ValueError):scheduler.submit_trajectory({}, '0' * 64)
        with pytest.raises(ValueError):scheduler.submit_trajectory({}, '0' * 64, timeout=float('nan'))


def sealed_launch(tmp_path, *, kind='prediction-comparison-v1', changed=None, expected=None):
    from psychohistory.v02_execution import digest, source_snapshot
    from psychohistory.prediction import protocol_spec
    files = source_snapshot()
    files.update({name: text.encode().hex() for name, text in (changed or {}).items()})
    configuration = {'protocol_id':'p','source_id':'s','spec':protocol_spec(3)}
    output = tmp_path / 'sealed.json'
    worker = subprocess.Popen([sys.executable,'-I','-S','-B','-c',
                               bytes.fromhex(files['v02_worker.py']).decode(), str(output),
                               str(os.getpid()), expected or digest(files)],
                              stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              start_new_session=True, env={'LC_ALL':'C.UTF-8'})
    worker.stdin.write(json.dumps({'files':files,'config':configuration,'kind':kind}));worker.stdin.close()
    return worker, output, configuration


def test_sealed_worker_retains_v2_result_and_enforces_native_limits(tmp_path):
    from psychohistory.prediction import run_comparison
    worker, output, config = sealed_launch(tmp_path)
    worker.wait(timeout=10)
    assert worker.returncode == 0
    payload = json.loads(output.read_text())
    assert payload['ok'],payload
    expected = run_comparison(config['spec'])
    assert {key:payload['result'][key] for key in expected} == expected
    assert payload['result']['input'] == config
    assert payload['limits']['isolated_python'] is True
    assert payload['limits']['cpu'] == 'RLIMIT_CPU'
    assert payload['limits']['memory'] == ('RLIMIT_AS' if sys.platform == 'linux' else 'NOT_ENFORCED')
    assert payload['limits']['process_group'] == 'OWNED_SESSION'


@pytest.mark.parametrize('case',['fingerprint','kind','checkout-import'])
def test_sealed_worker_rejects_unpinned_or_unallowlisted_execution(tmp_path,case):
    from psychohistory.v02_execution import digest
    if case == 'fingerprint':worker,output,_ = sealed_launch(tmp_path,expected='0'*64)
    elif case == 'kind':worker,output,_ = sealed_launch(tmp_path,kind='unknown-plugin')
    else:
        worker,output,_ = sealed_launch(tmp_path,changed={
            'prediction.py':'from . import arbitrary_checkout_module\n',
            'arbitrary_checkout_module.py':'raise RuntimeError("DISALLOWED_MODULE_EXECUTED")\n'})
    worker.wait(timeout=5)
    assert worker.returncode == 0
    payload = json.loads(output.read_text())
    assert payload['ok'] is False
    assert 'DISALLOWED_MODULE_EXECUTED' not in payload['error']


def test_real_legacy_scheduler_timeout_and_cancel_own_process_group(tmp_path):
    from psychohistory.runtime import Scheduler
    from psychohistory.storage import Store
    with Scheduler(Store(tmp_path/'real-lifecycle')) as scheduler:
        run = scheduler.submit({'rounds':100,'population':1000}, timeout=.001)
        scheduler.approve(run['id'])
        final = scheduler.wait(run['id'],5)
        assert final['status'] == 'FAILED' and 'timeout' in final['error'].lower()
        await_gone(final['worker_pid'])
        run = scheduler.submit({'rounds':100,'population':1000})
        scheduler.approve(run['id'])
        deadline = time.monotonic()+5
        while scheduler.get(run['id'])['status'] != 'RUNNING' and time.monotonic() < deadline:
            time.sleep(.001)
        active = scheduler.get(run['id'])
        assert active['status'] == 'RUNNING'
        scheduler.cancel(run['id'])
        assert scheduler.get(run['id'])['status'] == 'CANCELED'
        await_gone(active['worker_pid'])
        assert not list(scheduler.staging.glob('*.json'))


def test_real_sealed_scheduler_death_prevents_orphan_publication(tmp_path):
    helper = tmp_path/'sealed-owner.py'
    ready = tmp_path/'scheduler.json'
    helper.write_text('''import json,sys,time
from pathlib import Path
from psychohistory.storage import Store
from psychohistory.runtime import Scheduler
from psychohistory.prediction import protocol_spec
from psychohistory.v02_execution import digest,source_snapshot
q=Scheduler(Store(sys.argv[1]),comparison_verifier=lambda config:None)
config={'protocol_id':'p','source_id':'s','spec':protocol_spec(3)}
r=q.submit_comparison(config,'holdout',digest(source_snapshot()))
q.approve(r['id'])
while q.get(r['id'])['status']!='RUNNING':time.sleep(.001)
Path(sys.argv[2]).write_text(json.dumps(q.get(r['id'])))
while True:time.sleep(1)
''')
    root = tmp_path/'sealed-death'
    owner = subprocess.Popen([sys.executable,str(helper),str(root),str(ready)],
                             env=ENV,stderr=subprocess.PIPE,text=True)
    run = None
    try:
        run = json.loads(wait_file(ready,owner))
        owner.kill();owner.wait(timeout=5)
        await_gone(run['worker_pid'])
        assert not list((root/'staging').glob('*.json'))
        from psychohistory.storage import Store
        from psychohistory.runtime import Scheduler
        with Scheduler(Store(root),comparison_verifier=lambda config:None) as scheduler:
            recovered = scheduler.get(run['id'])
            assert recovered['status']=='FAILED'
            assert recovered['holdout_started_at'] is not None
            assert recovered['result_hash'] is None
    finally:
        if owner.poll() is None:owner.kill();owner.wait()
        if run and alive(run['worker_pid']):os.killpg(run['worker_pid'],signal.SIGKILL)


def test_real_sealed_scheduler_timeout_and_cancel_remove_worker(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    from psychohistory.prediction import protocol_spec
    from psychohistory.v02_execution import digest,source_snapshot
    with Scheduler(Store(tmp_path/'sealed-stops'),comparison_verifier=lambda config:None) as scheduler:
        config={'protocol_id':'p','source_id':'s','spec':protocol_spec(4)}
        run=scheduler.submit_comparison(config,'first',digest(source_snapshot()))
        scheduler.store.update_run(run['id'],timeout=.001)
        scheduler.approve(run['id'])
        outcome=scheduler.wait(run['id'],5)
        assert outcome['status']=='FAILED' and 'timeout' in outcome['error'].lower()
        await_gone(outcome['worker_pid'])
        run=scheduler.submit_comparison(config,'second',digest(source_snapshot()))
        scheduler.approve(run['id'])
        deadline=time.monotonic()+5
        while scheduler.get(run['id'])['status']!='RUNNING' and time.monotonic()<deadline:time.sleep(.001)
        active=scheduler.get(run['id'])
        assert active['status']=='RUNNING'
        scheduler.cancel(run['id'])
        assert scheduler.get(run['id'])['status']=='CANCELED'
        await_gone(active['worker_pid'])
        assert not list(scheduler.staging.glob('*.json'))


def test_failed_sealed_computation_retains_confirmed_control_receipt(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    from psychohistory.prediction import protocol_spec
    from psychohistory.v02_execution import digest,source_snapshot
    spec = protocol_spec(4)
    spec['candidate'] = 'unregistered'
    config={'protocol_id':'p','source_id':'s','spec':spec}
    with Scheduler(Store(tmp_path/'failed-receipt'),comparison_verifier=lambda config:None) as scheduler:
        run=scheduler.submit_comparison(config,'failure',digest(source_snapshot()))
        scheduler.approve(run['id'])
        outcome=scheduler.wait(run['id'],5)
        assert outcome['status']=='FAILED'
        assert outcome.get('limits',{}).get('cpu')=='RLIMIT_CPU'
        assert outcome['limits']['process_group']=='OWNED_SESSION'


@pytest.mark.parametrize('model,parameters',[
    ('r123-degroot',{'opinions':['0','1'],'weights':[['1/2','1/2'],['1/4','3/4']],'steps':3}),
    ('r132-replicator',{'initial':['1/4','3/4'],'payoff':[['2','2'],['1','1']],
                        'method':'rk4','steps':3,'step_size':'1/8'}),
])
def test_real_trajectory_worker_publishes_pinned_envelope_and_independent_continuation(tmp_path,model,parameters):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    from psychohistory.v02_execution import digest,source_snapshot,RUN_KIND_TRAJECTORY
    from psychohistory.trajectories import normalize,validate_result
    config={'model_id':model,'model_version':'1.0.0','source_id':'synthetic-test-source',
            'source':{'research_id':model.split('-')[0].upper()},
            'parameters':normalize(model,'1.0.0',parameters),'start':None,'branch_from':None}
    store=Store(tmp_path/'trajectory')
    with Scheduler(store,trajectory_verifier=lambda config:None) as scheduler:
        first=scheduler.submit_trajectory(config,digest(source_snapshot()))
        scheduler.approve(first['id'])
        done=scheduler.wait(first['id'],10)
        assert done['status']=='COMPLETED',done
        result=store.get(done['result_hash'])
        validate_result(done,result)
        assert done['kind']==RUN_KIND_TRAJECTORY
        assert done.get('holdout_id') is None and done.get('holdout_started_at') is None
        assert result['input']==config and result['code_sha256']==done['code_sha256']
        assert done['limits']['isolated_python'] is True
        continuation={**config,'start':{'state':result['state'],'snapshot_hash':result['snapshot']['content_hash']},
                      'branch_from':done['id']}
        second=scheduler.submit_trajectory(continuation,digest(source_snapshot()))
        scheduler.approve(second['id'])
        continued=scheduler.wait(second['id'],10)
        assert continued['status']=='COMPLETED',continued
        branch=store.get(continued['result_hash'])
        assert branch['trajectory'][0]==result['trajectory'][-1]
        assert branch['snapshot']['payload']['parent_hash']==result['snapshot']['content_hash']
        assert store.get(done['result_hash'])==result
