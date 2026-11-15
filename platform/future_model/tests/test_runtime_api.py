import time
from pathlib import Path
import pytest


def test_scheduler_execution_failure_cancel_timeout(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    store=Store(tmp_path/'runs')
    with Scheduler(store) as q:
        a=q.submit({'seed':4,'rounds':3,'population':8,'intervention':.2})
        assert q.get(a['id'])['status']=='PENDING'
        q.approve(a['id']);done=q.wait(a['id'],10)
        assert done['status']=='COMPLETED'
        assert done['worker_pid']!=__import__('os').getpid()
        assert store.get(done['result_hash'])['scientific_status']=='SYNTHETIC_ONLY'
        bad=q.submit({'rounds':0});q.approve(bad['id'])
        assert q.wait(bad['id'],10)['status']=='FAILED'
        cancel=q.submit({});q.cancel(cancel['id']);assert q.get(cancel['id'])['status']=='CANCELED'
        timeout=q.submit({'rounds':100,'population':1000},timeout=.001);q.approve(timeout['id'])
        assert q.wait(timeout['id'],10)['status']=='FAILED'
        assert 'timeout' in q.get(timeout['id'])['error'].lower()
        running=q.submit({'rounds':100,'population':1000});q.approve(running['id'])
        until=time.monotonic()+5
        while q.get(running['id'])['status']!='RUNNING' and time.monotonic()<until:time.sleep(.01)
        q.cancel(running['id']);assert q.get(running['id'])['status']=='CANCELED'
        with pytest.raises(ValueError):q.approve(cancel['id'])
        with pytest.raises(ValueError):q.submit({},timeout=9999)
    assert len(store.runs())==5


def test_service_auth_admission_and_provenance(tmp_path):
    from psychohistory.api import create_app
    from fastapi.testclient import TestClient
    repo=Path(__file__).resolve().parents[3]
    app=create_app(tmp_path/'api-data',repo,'test-local-token')
    with TestClient(app) as c:
        assert c.get('/api/v1/models').status_code==401
        headers={'Authorization':'Bearer test-local-token'}
        assert c.get('/api/v1/models',headers=headers).status_code==200
        assert c.post('/api/v1/runs',headers=headers,json={'permission':'REAL_EXPERIMENT'}).status_code==403
        assert c.post('/api/v1/runs',headers=headers,json={'population':100000}).status_code==422
        assert c.post('/api/v1/runs',headers={**headers,'Origin':'https://attacker.example'},json={}).status_code==403
        r=c.post('/api/v1/runs',headers=headers,json={'seed':9,'rounds':3,'population':8}).json()
        assert r['status']=='PENDING'
        assert c.post(f"/api/v1/runs/{r['id']}/approve",headers=headers).status_code==200
        until=time.monotonic()+10
        while time.monotonic()<until:
            done=c.get(f"/api/v1/runs/{r['id']}",headers=headers).json()
            if done['status'] in {'COMPLETED','FAILED'}:break
            time.sleep(.03)
        assert done['status']=='COMPLETED',done
        result=c.get(f"/api/v1/runs/{r['id']}/result",headers=headers).json()
        assert result['input']['seed']==9 and result['versions']['individual']=='1.0.0'
        assert done['code_sha256'] and done['logs'] and done['protocol']=='synthetic-paired-1.0.0'
        a=c.post('/api/v1/assets/discover',headers=headers,json={'path':'research/R233/R233_FINAL_ACCEPTANCE_STATUS.json'})
        assert a.status_code==200
        assert c.post('/api/v1/assets/discover',headers=headers,json={'path':'../../etc/passwd'}).status_code==422
        assert c.get('/api/v1/assets',headers=headers).json()[0]['permission']=='BROWSE_ONLY'
        assert c.get('/api/v1/health').json()['scientific_status']=='SYNTHETIC_ONLY'


def test_crash_recovery_blocks_unowned_worker(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data');s.create_run('lost',{});s.update_run('lost',status='APPROVED');s.update_run('lost',status='RUNNING')
    with Scheduler(s) as q:
        assert q.get('lost')['status']=='FAILED'
        assert 'restart' in q.get('lost')['error']


def test_api_rejects_oversize_undeclared_fields_and_traversal(tmp_path):
    from psychohistory.api import create_app
    from fastapi.testclient import TestClient
    repo=Path(__file__).resolve().parents[3]
    with TestClient(create_app(tmp_path/'api',repo,'local-test-token')) as c:
        headers={'Authorization':'Bearer local-test-token'}
        assert c.post('/api/v1/runs',headers=headers,json={'frozen_protocol_change':True}).status_code==422
        assert c.post('/api/v1/runs',headers=headers,content='x'*17000).status_code==413
        assert c.get('/api/v1/runs/../../token',headers=headers).status_code!=200
        assert c.get('/api/v1/assets',headers={'Authorization':'Bearer wrong'}).status_code==401
        assert c.get('/api/v1/runs?limit=0',headers=headers).status_code==422
        assert c.get('/api/v1/runs?offset=-1',headers=headers).status_code==422


def test_scheduler_single_owner_and_backup_refuses_running(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    with Scheduler(s) as q:
        with pytest.raises(ValueError):Scheduler(Store(s.root))
        r=q.submit({'rounds':100,'population':1000});q.approve(r['id'])
        with pytest.raises(ValueError):q.backup(tmp_path/'backup')
        q.cancel(r['id'])
