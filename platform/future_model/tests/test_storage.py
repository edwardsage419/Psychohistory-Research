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


def test_restore_rejects_manifest_traversal_and_source_anomalies(tmp_path):
    from psychohistory.storage import Store,restore_backup
    from psychohistory.evidence import scan_asset
    s=Store(tmp_path/'data');s.backup(tmp_path/'backup')
    path=tmp_path/'backup/manifest.json';m=json.loads(path.read_text());m['files']['../../outside']='0'*64;path.write_text(json.dumps(m))
    with pytest.raises(ValueError):restore_backup(tmp_path/'backup',tmp_path/'restore')
    repo=tmp_path/'repo';(repo/'research').mkdir(parents=True)
    (repo/'research/broken.json').write_text('{invalid')
    with pytest.raises(ValueError):scan_asset(repo,'research/broken.json')
    (repo/'research/link.json').symlink_to(path)
    with pytest.raises(ValueError):scan_asset(repo,'research/link.json')


def test_registry_coexists_versions_and_frozen_state_roundtrip():
    from psychohistory.plugins import Registry,Individual
    class NewIndividual(Individual):version='1.1.0'
    registry=Registry();registry.register(Individual());registry.register(NewIndividual())
    assert registry.get('individual','1.0.0').version=='1.0.0'
    assert registry.get('individual','1.1.0').version=='1.1.0'
    old=registry.get('individual','1.0.0');new=registry.get('individual','1.1.0')
    raw=old.serialize_state({'states':[0,1]})
    assert old.restore_state(raw)=={'states':[0,1]}
    with pytest.raises(ValueError):new.restore_state(raw)


def test_failed_object_flush_leaves_no_partial_publication(tmp_path, monkeypatch):
    import errno
    from psychohistory import storage

    store = storage.Store(tmp_path / 'data')
    payload = {'synthetic': True}
    expected = storage.digest(storage.canonical(payload).encode())
    path = store.root / 'objects' / f'{expected}.json'

    def fail_flush(fd):
        assert not path.exists(), 'Artifact was published before the file was flushed'
        raise OSError(errno.EIO, 'injected artifact flush failure')

    with monkeypatch.context() as patch:
        patch.setattr(storage.os, 'fsync', fail_flush)
        with pytest.raises(OSError, match='injected artifact flush failure'):
            store.put(payload)
    assert not path.exists()
    assert store.put(payload) == expected
    assert store.get(expected) == payload
    assert store.backup(tmp_path / 'backup')['files'][f'objects/{expected}.json'] == expected


def test_backup_source_registration_snapshot_is_consistent(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    from psychohistory import sources, storage
    from psychohistory.workflow import Workflow

    origin = storage.Store(tmp_path / 'data')
    second_connection = storage.Store(origin.root)
    repo = Path(__file__).resolve().parents[3]
    registration_started = Event()
    capture = sources.capture
    connect = sqlite3.connect

    def observe_capture(*args, **kwargs):
        record = capture(*args, **kwargs)
        registration_started.set()
        return record

    class SnapshotProbe(sqlite3.Connection):
        def backup(self, target, **kwargs):
            super().backup(target, **kwargs)
            filling = pool.submit(Workflow(second_connection, repo).register_source, 'R123')
            future.append(filling)
            assert registration_started.wait(timeout=10)
            # With the snapshot locked the other Store can only commit after backup.
            from concurrent.futures import TimeoutError
            try:
                filling.result(timeout=0.3)
            except TimeoutError:
                pass

    def connect_with_probe(database, *args, **kwargs):
        if database == origin.root / 'metadata.sqlite':
            kwargs['factory'] = SnapshotProbe
        return connect(database, *args, **kwargs)

    future = []
    monkeypatch.setattr(sources, 'capture', observe_capture)
    monkeypatch.setattr(sqlite3, 'connect', connect_with_probe)
    with ThreadPoolExecutor(max_workers=1) as pool:
        origin.backup(tmp_path / 'backup')
        registered = future[0].result(timeout=10)
    restored = storage.restore_backup(tmp_path / 'backup', tmp_path / 'restored')
    assert restored.research_records('sources') == []
    assert registered['source_id'] not in (restored.root / 'audit.jsonl').read_text()
    assert origin.research_record('sources', registered['source_id'])['research_id'] == 'R123'
