import json
from pathlib import Path
import time
import pytest


def fill_terminal(store,n=201):
    for i in range(n):
        store.create_run(f'new-{i}',{});store.update_run(f'new-{i}',status='CANCELED')


def test_old_live_tasks_remain_authoritative_and_paginated(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    with Scheduler(s) as first:
        old=first.submit({'rounds':1,'population':2})['id']
    fill_terminal(s)
    assert any(r['id']==old for r in s.runs(limit=100,offset=200))
    with Scheduler(s) as q:
        q.approve(old)
        assert q.wait(old,10)['status']=='COMPLETED'
        for _ in range(16):q.submit({})
        with pytest.raises(ValueError):q.submit({})


def test_old_running_recovered_and_old_approved_blocks_backup(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    s.create_run('old',{});s.update_run('old',status='APPROVED');s.update_run('old',status='RUNNING')
    fill_terminal(s)
    with Scheduler(s) as q:assert q.get('old')['status']=='FAILED'
    s.create_run('approved',{});s.update_run('approved',status='APPROVED')
    with pytest.raises(ValueError):s.backup(tmp_path/'backup')


def test_missing_referenced_object_fails_backup_truthfully(tmp_path):
    from psychohistory.storage import Store
    s=Store(tmp_path/'data');h=s.put({'a':1});s.create_run('r',{})
    s.update_run('r',status='APPROVED');s.update_run('r',status='RUNNING');s.update_run('r',status='COMPLETED',result_hash=h)
    (s.root/'objects'/f'{h}.json').unlink();s.put({'unrelated':True})
    with pytest.raises(ValueError):s.backup(tmp_path/'backup')
    assert not (tmp_path/'backup/manifest.json').exists()
    assert 'FAILED' in (s.root/'audit.jsonl').read_text()


def test_code_pin_changes_block_old_approval(tmp_path):
    from psychohistory.storage import Store
    from psychohistory.runtime import Scheduler
    s=Store(tmp_path/'data')
    with Scheduler(s) as q:
        r=q.submit({'rounds':1,'population':2});s.update_run(r['id'],code_sha256='0'*64)
        q.approve(r['id']);done=q.wait(r['id'],10)
        assert done['status']=='BLOCKED'
        assert 'identity' in done['error'].lower()
        assert done['result_hash'] is None


def test_pin_check_rejects_worker_output_from_other_code(tmp_path):
    from psychohistory.runtime import validate_execution_identity
    from psychohistory.engine import run_experiment,code_identity
    import platform
    result=run_experiment(rounds=1,population=2)
    run={'code_sha256':code_identity(),'protocol':'synthetic-paired-1.0.0','data_version':'generated-1.0.0','platform_version':'0.1.0','environment':{'python':platform.python_version(),'os':platform.system(),'machine':platform.machine()},'versions':result['versions'],'config':result['input']}
    validate_execution_identity(run,result)
    result['environment']['core_code_sha256']='0'*64
    with pytest.raises(ValueError):validate_execution_identity(run,result)


def good_record():
    from psychohistory.contracts import uncertainty
    return {'schema_version':'1.0.0','record_id':'test','record_type':'individual.states','subject_ref':['a','b'],
        'payload':{'states':[0,1]},'units':'binary','uncertainty':uncertainty('UNKNOWN',units='binary',target='individual.states'),
        'dependencies':['joint-population-state'],'time_context':{'simulation_time':0,'round':0,'event_time':0,'observed_at':0,'available_at':0,'cutoff':0,'target_time':1},
        'access_policy':'PUBLIC_SYNTHETIC','provenance':{'source':'SYNTHETIC','seed':1}}

@pytest.mark.parametrize('mutation',[
    lambda r:r.update(subject_ref='ab'),lambda r:r.update(dependencies='unknown'),
    lambda r:r['uncertainty'].update(units='kg'),lambda r:r['uncertainty'].update(dependencies=['different-joint-state']),
    lambda r:r['uncertainty'].pop('source'),lambda r:r['uncertainty'].update(kind='DISCRETE',values=[0,1],probabilities=[.5,.5]),
    lambda r:r.update(record_id=''),lambda r:r['time_context'].update(round=.5),lambda r:r.update(provenance=[]),
])
def test_malformed_exchange_is_rejected(mutation):
    from psychohistory.adapters import PopulationAdapter
    r=good_record();mutation(r)
    with pytest.raises(ValueError):PopulationAdapter().adapt(r)


def test_every_snapshot_parent_resolves_after_roundtrip(tmp_path):
    from psychohistory.engine import run_experiment
    from psychohistory.storage import Store,restore_backup
    from psychohistory.state import Snapshot
    s=Store(tmp_path/'data');h=s.put(run_experiment(rounds=2,population=4));s.backup(tmp_path/'backup')
    value=restore_backup(tmp_path/'backup',tmp_path/'restored').get(h)
    snapshots=[value['root_snapshot']]
    for branch in value['branches'].values():
        snapshots.append(branch['initial_snapshot']);snapshots.extend(x['snapshot'] for x in branch['history'])
    index={x['content_hash']:x for x in snapshots}
    for x in snapshots:
        node=Snapshot.from_dict(x).restore();parent=node['parent_hash']
        assert parent is None or parent in index
