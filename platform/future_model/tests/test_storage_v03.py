"""Crash consistency is process-crash tested; these are not power-loss tests."""
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys

import pytest

from psychohistory import storage


def audit_rows(store):
    with store.db() as db:
        return [json.loads(row[0]) for row in db.execute('SELECT payload FROM audit_events ORDER BY seq')]


def test_object_publication_syncs_its_directory_after_link(tmp_path, monkeypatch):
    store = storage.Store(tmp_path / 'data')
    synced = []
    real_sync = os.fsync
    def observe(fd):
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            synced.append((os.fstat(fd).st_ino, len(list((store.root / 'objects').glob('*.json')))))
        return real_sync(fd)
    monkeypatch.setattr(os, 'fsync', observe)
    store.put({'value': 3})
    assert ((store.root / 'objects').stat().st_ino, 1) in synced


def test_exclusive_directory_publication_preserves_existing_destination(tmp_path):
    source = tmp_path / 'source'; source.mkdir(); (source / 'kept').write_text('payload')
    destination = tmp_path / 'destination'; destination.mkdir()
    with pytest.raises(FileExistsError):
        storage.publish_directory(source, destination)
    assert destination.is_dir() and not list(destination.iterdir())
    assert (source / 'kept').read_text() == 'payload'


def test_source_audit_and_insert_are_one_transaction(tmp_path):
    store = storage.Store(tmp_path / 'data')
    with store.db() as db:
        db.execute("CREATE TRIGGER reject_audit BEFORE INSERT ON audit_events BEGIN SELECT RAISE(ABORT,'injected audit failure'); END")
    with pytest.raises(sqlite3.IntegrityError, match='injected audit failure'):
        store.register_source({'source_id':'s1','research_id':'R123','warnings':[]})
    assert store.research_records('sources') == []
    with store.db() as db: db.execute('DROP TRIGGER reject_audit')
    assert store.register_source({'source_id':'s1','research_id':'R123','warnings':[]}) is True
    assert store.register_source({'source_id':'s1','research_id':'R123','warnings':[]}) is False
    assert [row['event'] for row in audit_rows(store)] == ['SOURCE_REGISTERED', 'SOURCE_DUPLICATE']
    assert audit_rows(store)[1]['warnings'] == ['DUPLICATE_SOURCE_ID']


def test_run_transition_rolls_back_when_audit_cannot_commit(tmp_path):
    store = storage.Store(tmp_path / 'data'); store.create_run('run', {})
    with store.db() as db:
        db.execute("CREATE TRIGGER reject_audit BEFORE INSERT ON audit_events BEGIN SELECT RAISE(ABORT,'injected audit failure'); END")
    with pytest.raises(sqlite3.IntegrityError): store.update_run('run',status='APPROVED')
    assert store.get_run('run')['status'] == 'PENDING'
    with store.db() as db: assert db.execute('SELECT COUNT(*) FROM approvals').fetchone()[0] == 0


def test_failed_mirror_does_not_reject_committed_source_and_backup_uses_sqlite(tmp_path, monkeypatch):
    store = storage.Store(tmp_path / 'data')
    def fail(): raise OSError('injected mirror disk failure')
    with monkeypatch.context() as patch:
        patch.setattr(store, '_sync_audit_mirror', fail)
        assert store.register_source({'source_id':'s1','warnings':[]}) is True
        store.backup(tmp_path / 'backup')
    assert audit_rows(store)[0]['source_id'] == 's1'
    journal = [json.loads(line) for line in (tmp_path / 'backup/audit.jsonl').read_text().splitlines()]
    assert journal[0]['source_id'] == 's1'
    reopened = storage.Store(store.root)
    assert 's1' in (reopened.root / 'audit.jsonl').read_text()


def test_mirror_work_is_bounded_and_repairs_uncheckpointed_tail(tmp_path, monkeypatch):
    store = storage.Store(tmp_path / 'data')
    with monkeypatch.context() as patch:
        patch.setattr(store, '_sync_audit_mirror', lambda: None)
        for index in range(600): store.audit({'index':index})
    store._sync_audit_mirror()
    first = (store.root / 'audit.jsonl').read_bytes()
    assert 0 < len(first.splitlines()) <= 256
    # A killed write leaves a prefix of the next committed event, not arbitrary bytes.
    with store.db() as db:
        next_payload = db.execute('SELECT payload FROM audit_events ORDER BY seq LIMIT 1 OFFSET 256').fetchone()[0]
    with (store.root / 'audit.jsonl').open('ab') as journal: journal.write(next_payload[:12].encode())
    for _ in range(4): store._sync_audit_mirror()
    lines = [json.loads(line) for line in (store.root / 'audit.jsonl').read_text().splitlines()]
    assert [line['index'] for line in lines] == list(range(600))


def test_backup_audit_comes_from_exact_sqlite_snapshot(tmp_path, monkeypatch):
    first = storage.Store(tmp_path / 'data'); other = storage.Store(first.root)
    first.audit({'event':'BEFORE'})
    connect = sqlite3.connect
    class Snapshot(sqlite3.Connection):
        def backup(self, target, **kwargs):
            super().backup(target, **kwargs)
            other.audit({'event':'AFTER'})
    def intercept(database, *args, **kwargs):
        if database == first.root / 'metadata.sqlite': kwargs['factory'] = Snapshot
        return connect(database, *args, **kwargs)
    monkeypatch.setattr(sqlite3, 'connect', intercept)
    first.backup(tmp_path / 'backup')
    assert 'AFTER' not in (tmp_path / 'backup/audit.jsonl').read_text()


def test_killed_after_sqlite_commit_recovers_source_audit(tmp_path):
    helper = tmp_path / 'kill.py'
    helper.write_text('''import os,sys
from psychohistory.storage import Store
s=Store(sys.argv[1])
s._sync_audit_mirror=lambda: os._exit(73)
s.register_source({'source_id':'crash-source','warnings':[]})
''')
    env = os.environ.copy(); env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1] / 'src')
    result = subprocess.run([sys.executable, str(helper), str(tmp_path / 'data')], env=env, timeout=10)
    assert result.returncode == 73
    store = storage.Store(tmp_path / 'data')
    assert store.research_record('sources','crash-source')['source_id'] == 'crash-source'
    assert [row['source_id'] for row in audit_rows(store)] == ['crash-source']
    assert 'crash-source' in (store.root / 'audit.jsonl').read_text()


@pytest.mark.parametrize('release', ['0.1', '0.2'])
def test_legacy_backup_preserves_result_identity_and_holdout(tmp_path, release):
    root = tmp_path / 'legacy'; root.mkdir(); (root / 'objects').mkdir()
    raw = b'{"original_result":true}'
    import hashlib
    identity = hashlib.sha256(raw).hexdigest()
    (root / 'objects' / f'{identity}.json').write_bytes(raw)
    with sqlite3.connect(root / 'metadata.sqlite') as db:
        db.execute('PRAGMA user_version=2')
        db.execute('CREATE TABLE runs (id TEXT PRIMARY KEY,payload TEXT NOT NULL)')
        run = {'id':'old','status':'COMPLETED','result_hash':identity}
        if release == '0.2':
            run.update(holdout_id='spent-holdout', holdout_accessed=True)
            db.execute('CREATE TABLE sources_v2(id TEXT PRIMARY KEY,payload TEXT NOT NULL)')
            db.execute('INSERT INTO sources_v2 VALUES (?,?)', ('old-source', '{"source_id":"old-source"}'))
            db.execute('CREATE TABLE protocols_v2(id TEXT PRIMARY KEY,payload TEXT NOT NULL)')
            db.execute('INSERT INTO protocols_v2 VALUES (?,?)', ('old-protocol', '{"status":"APPROVED"}'))
        db.execute('INSERT INTO runs VALUES (?,?)', ('old',json.dumps(run)))
    (root / 'audit.jsonl').write_text('{"status":"FAILED","legacy":true}\n')
    manifest = {'backup_version':'1.0.0','schema_version':2,'files':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}}
    (root / 'manifest.json').write_text(json.dumps(manifest))
    restored = storage.restore_backup(root,tmp_path / 'restored')
    assert restored.get(identity) == {'original_result':True}
    assert restored.get_run('old')['result_hash'] == identity
    if release == '0.2':
        assert restored.holdout_runs('spent-holdout')[0]['holdout_accessed'] is True
        assert restored.research_record('protocols','old-protocol')['status'] == 'APPROVED'
        assert restored.research_record('sources','old-source')['source_id'] == 'old-source'
    assert audit_rows(restored)[0] == {'status':'FAILED','legacy':True}
    reopened = storage.Store(restored.root)
    assert sum(row.get('legacy') is True for row in audit_rows(reopened)) == 1


def test_killed_before_file_sync_does_not_publish_destination(tmp_path):
    helper = tmp_path / 'publish-kill.py'
    helper.write_text('''import os,sys
from pathlib import Path
from psychohistory.storage import write_new
os.fsync=lambda fd: os._exit(74)
write_new(Path(sys.argv[1]), b'complete-payload')
''')
    env = os.environ.copy(); env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1] / 'src')
    result = subprocess.run([sys.executable,str(helper),str(tmp_path / 'published')],env=env,timeout=10)
    assert result.returncode == 74
    assert not (tmp_path / 'published').exists()


def test_retry_of_directory_sync_failure_reflushes_existing_object(tmp_path, monkeypatch):
    store = storage.Store(tmp_path / 'data')
    original = storage.fsync_directory
    def fail_objects(path):
        if Path(path) == store.root / 'objects': raise OSError('injected directory sync')
        return original(path)
    with monkeypatch.context() as patch:
        patch.setattr(storage,'fsync_directory',fail_objects)
        with pytest.raises(OSError,match='injected directory sync'): store.put({'retry':True})
        assert list((store.root / 'objects').glob('*.json'))
        with pytest.raises(OSError,match='injected directory sync'): store.put({'retry':True})
    identity = store.put({'retry':True})
    assert store.get(identity) == {'retry':True}


def test_backup_hashing_does_not_buffer_entire_audit_history(tmp_path):
    import tracemalloc
    store = storage.Store(tmp_path / 'data')
    payload = json.dumps({'large_history':'x' * 16384})
    with store.db() as db:
        db.executemany('INSERT INTO audit_events(payload) VALUES (?)', [(payload,)] * 800)
    tracemalloc.start()
    try:
        store.backup(tmp_path / 'backup')
        _, peak = tracemalloc.get_traced_memory()
    finally: tracemalloc.stop()
    assert peak < 5 * 1024**2, f'Backup materialized audit/database history: {peak}'


def test_unrecognized_legacy_tail_is_not_silently_erased(tmp_path):
    store = storage.Store(tmp_path / 'data'); store.audit({'event':'CURRENT'})
    path = store.root / 'audit.jsonl'
    with path.open('ab') as journal: journal.write(b'{"event":"OLD_BINARY_FAILURE"}\n')
    before = path.read_bytes()
    reopened = storage.Store(store.root)
    assert path.read_bytes() == before
    assert reopened.audit_mirror_error is not None


@pytest.mark.parametrize('window', ['before_commit', 'after_mirror_fsync'])
def test_real_process_exit_preserves_transaction_and_replays_mirror(tmp_path, window):
    helper = tmp_path / 'audit-kill.py'
    helper.write_text('''import os,sys
from pathlib import Path
from psychohistory.storage import Store
s=Store(sys.argv[1])
if sys.argv[2]=='before_commit':
    insert=s._insert_audit
    def interrupted(db,event):
        insert(db,event)
        os._exit(75)
    s._insert_audit=interrupted
else:
    sync=os.fsync
    def interrupted(fd):
        sync(fd)
        if os.fstat(fd).st_ino == (s.root/'audit.jsonl').stat().st_ino: os._exit(75)
    os.fsync=interrupted
s.register_source({'source_id':'window-source','warnings':[]})
''')
    env = os.environ.copy(); env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1] / 'src')
    result = subprocess.run([sys.executable,str(helper),str(tmp_path/'data'),window],env=env,timeout=10)
    assert result.returncode == 75
    reopened = storage.Store(tmp_path / 'data')
    expected = [] if window == 'before_commit' else ['window-source']
    assert [row['source_id'] for row in reopened.research_records('sources')] == expected
    assert [row['source_id'] for row in audit_rows(reopened)] == expected
    assert [json.loads(line)['source_id'] for line in (reopened.root/'audit.jsonl').read_text().splitlines()] == expected


def test_concurrent_processes_publish_one_complete_object(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    helper = tmp_path / 'publish.py'
    helper.write_text('''import sys
from psychohistory.storage import Store
s=Store(sys.argv[1]); print(s.put({'value':'x'*200000}),flush=True)
''')
    env = os.environ.copy(); env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1] / 'src')
    def writer(_):
        return subprocess.run([sys.executable,str(helper),str(tmp_path/'data')],env=env,capture_output=True,text=True,timeout=15)
    with ThreadPoolExecutor(max_workers=4) as pool: results = list(pool.map(writer,range(4)))
    assert all(result.returncode == 0 for result in results), [result.stderr for result in results]
    hashes = {result.stdout.strip() for result in results}
    assert len(hashes) == 1
    store = storage.Store(tmp_path / 'data')
    assert store.get(hashes.pop()) == {'value':'x'*200000}
    assert len(list((store.root/'objects').iterdir())) == 1


def test_busy_mirror_does_not_block_a_committed_mutation(tmp_path):
    import fcntl
    from concurrent.futures import ThreadPoolExecutor, TimeoutError
    store = storage.Store(tmp_path / 'data')
    with (store.root / 'audit.lock').open('rb') as lock, ThreadPoolExecutor(max_workers=1) as pool:
        fcntl.flock(lock,fcntl.LOCK_EX)
        future = pool.submit(store.create_run,'not-blocked',{})
        try:
            try: result = future.result(timeout=.5)
            except TimeoutError: result = None
        finally: fcntl.flock(lock,fcntl.LOCK_UN)
        future.result(timeout=5)
    assert result is not None, 'A derivative audit mirror blocked a committed task'
    assert store.get_run('not-blocked')['status'] == 'PENDING'
    assert any(row.get('run_id') == 'not-blocked' for row in audit_rows(store))
    reopened = storage.Store(store.root)
    assert 'not-blocked' in (reopened.root/'audit.jsonl').read_text()


@pytest.mark.parametrize('reopen', [False, True])
def test_backup_refuses_unrecognized_legacy_audit_tail_without_losing_bytes(tmp_path, reopen):
    store = storage.Store(tmp_path/'data'); store.audit({'event':'CURRENT'})
    journal = store.root/'audit.jsonl'
    with journal.open('ab') as outgoing:
        outgoing.write(b'{"event":"OLD_BINARY_FAILURE"}\n')
    original = journal.read_bytes()
    if reopen: store = storage.Store(store.root)
    with pytest.raises(ValueError, match='(?i)audit.*tail|legacy'):
        store.backup(tmp_path/'backup')
    assert not (tmp_path/'backup').exists()
    assert journal.read_bytes() == original
    assert any(row.get('backup') == 'FAILED' for row in audit_rows(store))


def test_backup_accepts_a_recognized_interrupted_mirror_append(tmp_path, monkeypatch):
    store = storage.Store(tmp_path/'data'); store.audit({'event':'BEFORE'})
    with monkeypatch.context() as patch:
        patch.setattr(store,'_sync_audit_mirror',lambda:None)
        store.audit({'event':'AFTER'})
    with store.db() as db:
        payload = db.execute('SELECT payload FROM audit_events ORDER BY seq DESC LIMIT 1').fetchone()[0]
    with (store.root/'audit.jsonl').open('ab') as outgoing: outgoing.write(payload[:12].encode())
    store.backup(tmp_path/'backup')
    copied = [json.loads(line)['event'] for line in (tmp_path/'backup/audit.jsonl').read_text().splitlines()]
    assert copied == ['BEFORE','AFTER']


def test_backup_rechecks_unknown_tail_arriving_after_sqlite_snapshot(tmp_path, monkeypatch):
    store = storage.Store(tmp_path/'data'); store.audit({'event':'BEFORE'})
    connect = sqlite3.connect
    class LegacyAppend(sqlite3.Connection):
        def backup(self, target, **kwargs):
            super().backup(target, **kwargs)
            with (store.root/'audit.jsonl').open('ab') as journal:
                journal.write(b'{"event":"OLD_BINARY_FAILURE"}\n')
    def intercept(database,*args,**kwargs):
        if database == store.root/'metadata.sqlite': kwargs['factory'] = LegacyAppend
        return connect(database,*args,**kwargs)
    monkeypatch.setattr(sqlite3,'connect',intercept)
    with pytest.raises(ValueError,match='Unrecognized audit mirror tail'):
        store.backup(tmp_path/'backup')
    assert not (tmp_path/'backup').exists()
    assert 'OLD_BINARY_FAILURE' in (store.root/'audit.jsonl').read_text()


def test_backup_mirror_contention_refuses_promptly_without_blocking(tmp_path):
    import fcntl
    from concurrent.futures import ThreadPoolExecutor
    store = storage.Store(tmp_path/'data')
    with (store.root/'audit.lock').open('rb') as lock, ThreadPoolExecutor(max_workers=1) as pool:
        fcntl.flock(lock,fcntl.LOCK_EX)
        future = pool.submit(store.backup,tmp_path/'backup')
        try:
            with pytest.raises(ValueError,match='audit mirror is busy'):
                future.result(timeout=.5)
        finally: fcntl.flock(lock,fcntl.LOCK_UN)
    assert not (tmp_path/'backup').exists()
    assert any(row.get('backup') == 'FAILED' for row in audit_rows(store))


def test_legacy_audit_migration_failure_never_publishes_restore_destination(tmp_path):
    import hashlib
    store = storage.Store(tmp_path/'source'); store.put({'original':True})
    store.backup(tmp_path/'legacy-backup')
    backup = tmp_path/'legacy-backup'
    # Historical v0.2 has no SQLite audit tables; its interrupted JSONL remains
    # an authentic, checksummed input which must not leave a half-restored root.
    with sqlite3.connect(backup/'metadata.sqlite') as db:
        db.execute('DROP TABLE audit_events')
        db.execute('DROP TABLE audit_mirror')
    (backup/'audit.jsonl').write_bytes(b'{"event":"COMPLETE"}\n{"event":"INTERRUPTED')
    manifest = json.loads((backup/'manifest.json').read_text())
    for name in ('metadata.sqlite','audit.jsonl'):
        manifest['files'][name] = hashlib.sha256((backup/name).read_bytes()).hexdigest()
    (backup/'manifest.json').write_text(json.dumps(manifest))
    original = {p.relative_to(backup).as_posix():p.read_bytes() for p in backup.rglob('*') if p.is_file()}
    for _ in range(2):
        with pytest.raises(ValueError,match='Legacy audit contains.*incomplete'):
            storage.restore_backup(backup,tmp_path/'restored')
        assert not (tmp_path/'restored').exists()
    assert {p.relative_to(backup).as_posix():p.read_bytes() for p in backup.rglob('*') if p.is_file()} == original
