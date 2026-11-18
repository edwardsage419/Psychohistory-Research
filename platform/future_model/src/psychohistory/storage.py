"""SQLite metadata, immutable objects and verified consistent disaster recovery."""
from contextlib import contextmanager
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile
import threading
import time
from .contracts import canonical

SCHEMA=2
HASH=re.compile(r'^[0-9a-f]{64}$')
TERMINAL={'COMPLETED','FAILED','CANCELED','BLOCKED'}
AUDIT_BATCH_ROWS = 256
AUDIT_BATCH_BYTES = 1024 * 1024


def checked_path(path):
    path=Path(os.path.abspath(path))
    if any(p.is_symlink() for p in [path,*path.parents]):raise ValueError('Symlink storage paths forbidden')
    return path


def digest(raw):return hashlib.sha256(raw).hexdigest()


def file_digest(path):
    with checked_path(path).open('rb') as incoming:
        return hashlib.file_digest(incoming, 'sha256').hexdigest()


def fsync_directory(path):
    fd = os.open(checked_path(path), os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_new(path, raw):
    """Publish complete, flushed bytes exclusively; never expose a partial file."""
    path = checked_path(path)
    fd, temporary = tempfile.mkstemp(prefix='.publish-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        os.link(temporary, path, follow_symlinks=False)
        fsync_directory(path.parent)
    finally:
        Path(temporary).unlink(missing_ok=True)


def publish_directory(source, destination):
    """Atomic no-replace directory publication on supported POSIX platforms."""
    source, destination = checked_path(source), checked_path(destination)
    if (source / 'objects').is_dir():
        fsync_directory(source / 'objects')
    fsync_directory(source)
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        rename = libc.renameat2
        rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        result = rename(-100, os.fsencode(source), -100, os.fsencode(destination), 1)
    elif sys.platform == 'darwin' and hasattr(libc, 'renamex_np'):
        rename = libc.renamex_np
        rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        result = rename(os.fsencode(source), os.fsencode(destination), 4)
    else:
        raise OSError('Exclusive directory publication unsupported on this platform')
    if result:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), str(destination))
    fsync_directory(destination.parent)

class Store:
    def __init__(self,root):
        self.root=checked_path(root)
        self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
        self.lock=threading.RLock()
        self.audit_mirror_error = None
        checked_path(self.root/'objects').mkdir(exist_ok=True,mode=0o700)
        for n in ['metadata.sqlite','audit.jsonl']:checked_path(self.root/n)
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            version=db.execute('PRAGMA user_version').fetchone()[0]
            if version>SCHEMA:raise ValueError('Future metadata schema rejected')
            db.execute('CREATE TABLE IF NOT EXISTS assets (sha256 TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            columns={x[1] for x in db.execute('PRAGMA table_info(assets)')}
            if 'registered_at' not in columns:db.execute('ALTER TABLE assets ADD COLUMN registered_at REAL NOT NULL DEFAULT 0')
            db.execute('CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS approvals (id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, decision TEXT NOT NULL, at REAL NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS versions (identity TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS sources_v2 (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS protocols_v2 (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            db.execute("CREATE INDEX IF NOT EXISTS runs_v2_holdout ON runs (json_extract(payload, '$.holdout_id'))")
            db.execute('CREATE TABLE IF NOT EXISTS audit_events (seq INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS audit_mirror (id INTEGER PRIMARY KEY CHECK(id=1), last_seq INTEGER NOT NULL, byte_offset INTEGER NOT NULL)')
            # Import legacy JSONL once, in this same migration transaction. Keep
            # original event text, ordering and failure evidence; do not alter objects.
            if db.execute('SELECT 1 FROM audit_mirror WHERE id=1').fetchone() is None:
                last_seq = offset = 0
                journal = checked_path(self.root / 'audit.jsonl')
                if journal.exists():
                    with journal.open('rb') as incoming:
                        while raw := incoming.readline(AUDIT_BATCH_BYTES + 1):
                            if len(raw) > AUDIT_BATCH_BYTES or not raw.endswith(b'\n'):
                                raise ValueError('Legacy audit contains an oversized or incomplete event; preserve and repair before migration')
                            payload = raw[:-1].decode('utf-8')
                            if not isinstance(json.loads(payload), dict):
                                raise ValueError('Legacy audit event must be an object')
                            last_seq = db.execute('INSERT INTO audit_events(payload) VALUES (?)', (payload,)).lastrowid
                            offset += len(raw)
                db.execute('INSERT INTO audit_mirror VALUES (1,?,?)', (last_seq, offset))
            db.execute('PRAGMA user_version=2')
        fsync_directory(self.root)
        self._mirror_after_commit()

    @contextmanager
    def db(self):
        with self.lock:
            checked_path(self.root/'metadata.sqlite')
            db=sqlite3.connect(self.root/'metadata.sqlite',timeout=10)
            try:
                db.execute('PRAGMA foreign_keys=ON')
                yield db
                db.commit()
            except BaseException:
                db.rollback();raise
            finally:db.close()

    @staticmethod
    def _insert_audit(db, event):
        payload = canonical({'at': time.time(), **event})
        if len(payload.encode()) + 1 > AUDIT_BATCH_BYTES:
            raise ValueError('Audit event exceeds 1 MiB budget')
        db.execute('INSERT INTO audit_events(payload) VALUES (?)', (payload,))

    def audit(self,event):
        with self.db() as db:
            self._insert_audit(db, event)
        self._mirror_after_commit()

    def _mirror_after_commit(self):
        # The SQLite commit is the operation's truth. A derivative mirror failure
        # must never turn a committed source or terminal task into an apparent failure.
        try:
            self._sync_audit_mirror()
            self.audit_mirror_error = None
        except (OSError, sqlite3.Error, ValueError) as error:
            self.audit_mirror_error = f'{type(error).__name__}: {error}'

    @staticmethod
    def _validate_audit_tail(db, journal, seq, offset):
        if os.fstat(journal.fileno()).st_size <= offset:
            return
        # Only our own interrupted append is safely recoverable from SQLite.
        # Unknown bytes can contain old-binary failure evidence not in SQLite.
        journal.seek(offset)
        tail = journal.read(AUDIT_BATCH_BYTES + 1)
        expected = bytearray()
        for _, payload in db.execute('SELECT seq,payload FROM audit_events WHERE seq>? ORDER BY seq LIMIT ?', (seq, AUDIT_BATCH_ROWS)):
            raw = (payload + '\n').encode()
            if len(expected) + len(raw) > AUDIT_BATCH_BYTES:
                break
            expected.extend(raw)
        if len(tail) > AUDIT_BATCH_BYTES or not expected.startswith(tail):
            raise ValueError('Unrecognized audit mirror tail preserved; archive and reconcile legacy writes before mirror repair or backup')

    def _validate_backup_audit(self):
        """Reject evidence outside SQLite; do not silently omit a legacy tail."""
        fd = os.open(checked_path(self.root / 'audit.lock'), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'rb') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise ValueError('Backup audit mirror is busy; retry after its checkpoint completes') from None
            with self.db() as db:
                seq, offset = db.execute('SELECT last_seq,byte_offset FROM audit_mirror WHERE id=1').fetchone()
                path = checked_path(self.root / 'audit.jsonl')
                if path.exists():
                    with path.open('rb') as journal:
                        self._validate_audit_tail(db, journal, seq, offset)

    def _sync_audit_mirror(self):
        """At most 256 events / 1 MiB per call, serialized across Store instances.

        The mirror checkpoint commits only after file fsync. An interrupted append
        is truncated to the old checkpoint then replayed from committed SQLite.
        """
        with self.lock:
            fd = os.open(checked_path(self.root / 'audit.lock'), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, 'rb') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.db() as db:
                    db.execute('PRAGMA busy_timeout=0')
                    db.execute('BEGIN IMMEDIATE')
                    seq, offset = db.execute('SELECT last_seq,byte_offset FROM audit_mirror WHERE id=1').fetchone()
                    path = checked_path(self.root / 'audit.jsonl')
                    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
                    with os.fdopen(fd, 'r+b') as outgoing:
                        current_size = os.fstat(outgoing.fileno()).st_size
                        if current_size < offset:
                            seq = offset = 0  # Missing/truncated derivative: rebuild incrementally.
                        elif current_size > offset:
                            self._validate_audit_tail(db, outgoing, seq, offset)
                        outgoing.truncate(offset)
                        outgoing.seek(offset)
                        size = 0
                        for next_seq, payload in db.execute('SELECT seq,payload FROM audit_events WHERE seq>? ORDER BY seq LIMIT ?', (seq, AUDIT_BATCH_ROWS)):
                            raw = (payload + '\n').encode()
                            if size + len(raw) > AUDIT_BATCH_BYTES:
                                break
                            outgoing.write(raw)
                            size += len(raw); seq = next_seq
                        outgoing.flush(); os.fsync(outgoing.fileno())
                        fsync_directory(self.root)
                        db.execute('UPDATE audit_mirror SET last_seq=?,byte_offset=? WHERE id=1', (seq, offset + size))

    @staticmethod
    def _export_audit(db, destination):
        """Stream only the audit events belonging to this SQLite backup snapshot."""
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        seq = offset = 0
        with os.fdopen(fd, 'wb') as outgoing:
            for seq, payload in db.execute('SELECT seq,payload FROM audit_events ORDER BY seq'):
                raw = (payload + '\n').encode()
                outgoing.write(raw); offset += len(raw)
            outgoing.flush(); os.fsync(outgoing.fileno())
        db.execute('UPDATE audit_mirror SET last_seq=?,byte_offset=? WHERE id=1', (seq, offset))

    @contextmanager
    def snapshot_lock(self):
        """Keep backup snapshots and audited source registration mutually exclusive."""
        with self.lock:
            path = checked_path(self.root / 'backup.lock')
            fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, 'rb') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                yield

    def schema_version(self):
        with self.db() as db:return db.execute('PRAGMA user_version').fetchone()[0]

    def register_asset(self, asset):
        with self.db() as db:
            duplicate=db.execute('SELECT 1 FROM assets WHERE sha256=?',(asset['sha256'],)).fetchone() is not None
            db.execute('INSERT OR IGNORE INTO assets VALUES (?,?,?)',(asset['sha256'],canonical(asset),time.time()))
        return {'duplicate':duplicate,'asset':asset}

    def assets(self):
        with self.db() as db:return [json.loads(x[0]) for x in db.execute('SELECT payload FROM assets ORDER BY sha256')]

    def research_records(self, collection):
        table = {"sources": "sources_v2", "protocols": "protocols_v2"}[collection]
        with self.db() as db:
            return [json.loads(row[0]) for row in db.execute(
                f"SELECT payload FROM {table} ORDER BY rowid DESC")]

    def research_record(self, collection, identity):
        table = {"sources": "sources_v2", "protocols": "protocols_v2"}[collection]
        with self.db() as db:
            row = db.execute(f"SELECT payload FROM {table} WHERE id=?", (identity,)).fetchone()
        if not row:
            raise KeyError(f"Unknown {collection} identity")
        return json.loads(row[0])

    def register_research_record(self, collection, identity, record):
        table = {"sources": "sources_v2", "protocols": "protocols_v2"}[collection]
        with self.db() as db:
            cursor = db.execute(f"INSERT OR IGNORE INTO {table} VALUES (?,?)",
                                (identity, canonical(record)))
            return cursor.rowcount == 1

    def register_source(self, record, warnings=None):
        """Register an immutable source and its audit event in one transaction."""
        with self.db() as db:
            cursor = db.execute('INSERT OR IGNORE INTO sources_v2 VALUES (?,?)',
                                (record['source_id'], canonical(record)))
            inserted = cursor.rowcount == 1
            messages = list(record.get('warnings', []) if warnings is None else warnings)
            if not inserted and 'DUPLICATE_SOURCE_ID' not in messages:
                messages.append('DUPLICATE_SOURCE_ID')
            self._insert_audit(db, {'event': 'SOURCE_REGISTERED' if inserted else 'SOURCE_DUPLICATE',
                                   'source_id': record['source_id'], 'warnings': messages})
        self._mirror_after_commit()
        return inserted

    def approve_protocol(self, identity, source_verifier):
        with self.db() as db:
            row = db.execute("SELECT payload FROM protocols_v2 WHERE id=?", (identity,)).fetchone()
            if row is None:
                raise KeyError("Unknown protocol")
            record = json.loads(row[0])
            source_verifier(record)
            if record["status"] != "APPROVED":
                record.update(status="APPROVED", approved_at=time.time())
                db.execute("UPDATE protocols_v2 SET payload=? WHERE id=?", (canonical(record), identity))
        return record

    def holdout_runs(self, identity):
        with self.db() as db:
            return [json.loads(row[0]) for row in db.execute(
                "SELECT payload FROM runs WHERE json_extract(payload, '$.holdout_id')=? ORDER BY rowid DESC",
                (identity,))]

    def put(self,value,access='PUBLIC_SYNTHETIC'):
        if access!='PUBLIC_SYNTHETIC':raise PermissionError('BLOCKED: nonpublic data persistence requires separate storage approval')
        raw=canonical(value).encode()
        if len(raw)>32*1024*1024:raise ValueError('Artifact budget exceeded')
        h=digest(raw);p=checked_path(self.root/'objects'/f'{h}.json')
        with self.lock:
            if not p.exists():
                # A killed writer can leave staging bytes, which backup never treats as objects.
                staging = checked_path(self.root / 'artifact-staging')
                staging.mkdir(exist_ok=True, mode=0o700)
                with tempfile.TemporaryDirectory(dir=staging) as temporary:
                    pending = Path(temporary) / 'payload'
                    write_new(pending, raw)
                    try:
                        os.link(pending, p, follow_symlinks=False)
                    except FileExistsError:
                        pass  # Verify the winning writer's object below.
            if digest(checked_path(p).read_bytes()) != h:
                raise ValueError('Existing immutable object corrupted')
            # A previous attempt may have linked successfully and failed its
            # directory flush; deduplication must not bypass durability on retry.
            fsync_directory(p.parent)
        return h

    def get(self,h):
        if not isinstance(h,str) or not HASH.fullmatch(h):raise ValueError('Invalid artifact identity')
        p=checked_path(self.root/'objects'/f'{h}.json');raw=p.read_bytes()
        if digest(raw)!=h:raise ValueError('Artifact hash mismatch')
        return json.loads(raw)

    def create_run(self,run_id,config,**identity):
        data={'id':run_id,'status':'PENDING','config':config,'created_at':time.time(),'started_at':None,'ended_at':None,
              'logs':[],'error':None,'result_hash':None,'permission':'SYNTHETIC_ONLY',**identity}
        with self.db() as db:
            db.execute('INSERT INTO runs VALUES (?,?)',(run_id,canonical(data)))
            self._insert_audit(db, {'run_id':run_id,'status':'PENDING'})
        self._mirror_after_commit()
        return data

    def get_run(self,run_id):
        with self.db() as db:r=db.execute('SELECT payload FROM runs WHERE id=?',(run_id,)).fetchone()
        if not r:raise KeyError('Run not found')
        return json.loads(r[0])

    def runs(self,limit=200,offset=0,kind=None):
        if type(limit)!=int or not 1<=limit<=200 or type(offset)!=int or offset<0:raise ValueError('Invalid history page')
        with self.db() as db:
            return [json.loads(row[0]) for row in db.execute(
                "SELECT payload FROM runs WHERE (? IS NULL OR COALESCE(json_extract(payload,'$.kind'),'legacy')=?) ORDER BY rowid DESC LIMIT ? OFFSET ?",
                (kind,kind,limit,offset))]

    def active_runs(self,kind=None):
        with self.db() as db:
            return [json.loads(x[0]) for x in db.execute("SELECT payload FROM runs WHERE json_extract(payload,'$.status') IN ('PENDING','APPROVED','RUNNING') AND (? IS NULL OR COALESCE(json_extract(payload,'$.kind'),'legacy')=?) ORDER BY rowid",(kind,kind))]


    def update_run(self,run_id,**changes):
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT payload FROM runs WHERE id=?',(run_id,)).fetchone()
            if not row:raise KeyError('Run not found')
            data=json.loads(row[0])
            if data['status'] in TERMINAL:raise ValueError('Terminal run history is immutable')
            previous = data['status']
            new=changes.get('status',previous)
            allowed={'PENDING':{'PENDING','APPROVED','CANCELED','BLOCKED','FAILED'},'APPROVED':{'APPROVED','RUNNING','CANCELED','BLOCKED','FAILED'},'RUNNING':{'RUNNING','COMPLETED','FAILED','CANCELED'}}
            if new not in allowed[data['status']]:raise ValueError('Illegal task transition')
            if new in TERMINAL:changes['ended_at']=time.time()
            data.update(changes)
            db.execute('UPDATE runs SET payload=? WHERE id=?',(canonical(data),run_id))
            if new=='APPROVED' and previous!='APPROVED':db.execute('INSERT INTO approvals(run_id,decision,at) VALUES (?,?,?)',(run_id,'APPROVED_SYNTHETIC',time.time()))
            self._insert_audit(db, {'run_id':run_id,'status':data['status'],'error':data['error']})
        self._mirror_after_commit()
        return data

    def lock_versions(self,versions):
        with self.db() as db:
            for name,value in versions.items():
                identity=f'{name}@{value}';db.execute('INSERT OR IGNORE INTO versions VALUES (?,?)',(identity,canonical({'component':name,'version':value})))

    def backup(self,destination):
        dest=checked_path(destination)
        if dest.exists():raise ValueError('Backup destination must be new')
        with self.snapshot_lock():
            if any(x['status'] in {'APPROVED','RUNNING'} for x in self.active_runs()):
                self.audit({'backup':'FAILED','reason':'active tasks'})
                raise ValueError('Backup requires quiescent scheduler')
            dest.parent.mkdir(parents=True,exist_ok=True)
            stage=Path(tempfile.mkdtemp(prefix='.backup-',dir=dest.parent));(stage/'objects').mkdir(mode=0o700)
            try:
                self._validate_backup_audit()
                with self.db() as db:
                    with sqlite3.connect(stage/'metadata.sqlite') as target:db.backup(target)
                for p in (self.root/'objects').iterdir():
                    checked_path(p)
                    if not re.fullmatch(r'[0-9a-f]{64}\.json',p.name):raise ValueError('Unexpected object file')
                    raw=p.read_bytes()
                    if digest(raw)!=p.stem:raise ValueError('Cannot back up corrupt object')
                    write_new(stage/'objects'/p.name,raw)
                with sqlite3.connect(stage/'metadata.sqlite') as db:
                    if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite backup integrity failure')
                    for row in db.execute('SELECT payload FROM runs'):
                        run=json.loads(row[0]);h=run.get('result_hash')
                        if run['status']=='COMPLETED' and not h:raise ValueError('Completed run missing result reference')
                        if h and (not HASH.fullmatch(h) or not (stage/'objects'/f'{h}.json').is_file()):raise ValueError('Missing referenced run artifact')
                    self._export_audit(db, stage / 'audit.jsonl')
                with (stage / 'metadata.sqlite').open('rb') as database:
                    os.fsync(database.fileno())
                manifest={'backup_version':'1.0.0','schema_version':SCHEMA,'files':{p.relative_to(stage).as_posix():file_digest(p) for p in sorted(stage.rglob('*')) if p.is_file()}}
                write_new(stage/'manifest.json',canonical(manifest).encode())
                self._validate_backup_audit()
                publish_directory(stage, dest)
            except BaseException:
                shutil.rmtree(stage, ignore_errors=True)
                self.audit({'backup':'FAILED','destination_name':dest.name});raise
        self.audit({'backup':'COMPLETED','manifest_sha256':digest(canonical(manifest).encode())})
        return manifest


def restore_backup(source,destination):
    source=checked_path(source);dest=checked_path(destination)
    if dest.exists():raise ValueError('Restore requires a new empty destination; preserve existing audit history')
    manifest=json.loads(checked_path(source/'manifest.json').read_bytes())
    if manifest.get('backup_version')!='1.0.0' or manifest.get('schema_version')!=SCHEMA:raise ValueError('Incompatible backup format')
    files=manifest.get('files',{})
    if not isinstance(files,dict) or not {'metadata.sqlite','audit.jsonl'}<=files.keys():raise ValueError('Incomplete backup')
    if not isinstance(files,dict):raise ValueError('Invalid backup file index')
    for relative,h in files.items():
        if relative not in {'metadata.sqlite','audit.jsonl'} and not re.fullmatch(r'objects/[0-9a-f]{64}\.json',relative):raise ValueError('Unsafe backup manifest path')
        if not isinstance(h,str) or not HASH.fullmatch(h):raise ValueError('Invalid manifest digest')
        if relative.startswith('objects/') and Path(relative).stem!=h:raise ValueError('Object identity mismatch')
    dest.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.restore-',dir=dest.parent))
    try:
        (stage/'objects').mkdir()
        for relative,expected in files.items():
            source_file=checked_path(source/relative)
            target=stage/relative
            fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
            sha=hashlib.sha256();size=0
            with os.fdopen(fd,'wb') as outgoing,source_file.open('rb') as incoming:
                while chunk:=incoming.read(256*1024):
                    size+=len(chunk)
                    if relative.startswith('objects/') and size>32*1024**2:raise ValueError('Backup object exceeds artifact budget')
                    sha.update(chunk);outgoing.write(chunk)
                if sha.hexdigest()!=expected:raise ValueError('Backup integrity failure')
                outgoing.flush();os.fsync(outgoing.fileno())
        with sqlite3.connect(stage/'metadata.sqlite') as db:
            if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok' or db.execute('PRAGMA user_version').fetchone()[0]!=SCHEMA:raise ValueError('SQLite restore validation failed')
            for row in db.execute('SELECT payload FROM runs'):
                run=json.loads(row[0]);h=run.get('result_hash')
                if run.get('status')=='COMPLETED' and not h:raise ValueError('Completed run missing result reference')
                if h and f'objects/{h}.json' not in files:raise ValueError('Missing run artifact')
        # Migration (including historical JSONL import) may still reject a
        # checksummed backup. Finish every fallible initialization step before
        # publishing the destination, so failure leaves retries possible.
        restored = Store(stage)
        restored.audit({'restore':'COMPLETED','backup_manifest_sha256':digest(canonical(manifest).encode())})
        publish_directory(stage, dest)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True);raise
    restored.root = dest
    return restored
