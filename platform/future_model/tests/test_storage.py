import json
import sqlite3
from pathlib import Path
import pytest


def test_asset_scan_dedup_and_frozen_namespace(tmp_path):
    from psychohistory.evidence import scan_asset, Admission
    from psychohistory.storage import Store
    repo=Path(__file__).resolve().parents[3]
    relative='research/R233/R233_FINAL_ACCEPTANCE_STATUS.json'
    before=(repo/relative).read_bytes()
    a=scan_asset(repo,relative)
    assert a['sha256'] and a['permission']=='BROWSE_ONLY'
    assert a['scientific_status']['namespace']=='R_SERIES_ORIGINAL'
    assert a['scientific_status']['original_record']==json.loads(before)
    s=Store(tmp_path/'store')
    assert s.register_asset(a)['duplicate'] is False
    assert s.register_asset(a)['duplicate'] is True
    assert (repo/relative).read_bytes()==before
    with pytest.raises(ValueError):scan_asset(repo,'../escape')
    with pytest.raises(ValueError):scan_asset(repo,'research/nonexistent.json')
    with pytest.raises(PermissionError):Admission.require('REAL_EXPERIMENT')
    with pytest.raises(PermissionError):Admission.require('FROZEN_PROTOCOL_CHANGE')
    Admission.require('SYNTHETIC_ONLY')


def test_content_addressed_storage_and_security(tmp_path):
    from psychohistory.storage import Store
    s=Store(tmp_path/'data')
    h=s.put({'states':[1,0]})
    assert s.get(h)=={'states':[1,0]}
    assert s.put({'states':[1,0]})==h
    for name in ['../test','/etc/passwd','x'*64]:
        with pytest.raises(ValueError):s.get(name)
    with pytest.raises(PermissionError):s.put({'private':'sensitive'},access='RESTRICTED')
    (s.root/'objects'/f'{h}.json').write_text('{}')
    with pytest.raises(ValueError):s.get(h)
    other=tmp_path/'linked';other.symlink_to(s.root,target_is_directory=True)
    with pytest.raises(ValueError):Store(other)


def test_backup_restore_integrity_and_failure_audit(tmp_path):
    from psychohistory.storage import Store, restore_backup
    root=tmp_path/'original';s=Store(root)
    h=s.put({'synthetic':True})
    s.create_run('one',{'seed':1})
    s.update_run('one',status='FAILED',error='deliberate validation failure')
    backup=tmp_path/'backup';s.backup(backup)
    restored=restore_backup(backup,tmp_path/'restored')
    assert restored.get(h)=={'synthetic':True}
    assert restored.get_run('one')['status']=='FAILED'
    assert (restored.root/'audit.jsonl').read_text().find('FAILED')>=0
    with pytest.raises(ValueError):restore_backup(backup,root)
    (backup/'objects'/f'{h}.json').write_text('tampered')
    with pytest.raises(ValueError):restore_backup(backup,tmp_path/'bad-restore')


def test_migration_and_future_schema_rejection(tmp_path):
    from psychohistory.storage import Store
    root=tmp_path/'old';root.mkdir()
    with sqlite3.connect(root/'metadata.sqlite') as db:
        db.execute('CREATE TABLE assets (sha256 TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        db.execute('PRAGMA user_version=1')
    s=Store(root)
    assert s.schema_version()==2
    with sqlite3.connect(s.root/'metadata.sqlite') as db:db.execute('PRAGMA user_version=99')
    with pytest.raises(ValueError):Store(root)
