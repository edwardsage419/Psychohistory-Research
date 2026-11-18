"""SQLite metadata, immutable objects and verified consistent disaster recovery."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
import threading
import time
from .contracts import canonical

SCHEMA=2
HASH=re.compile(r'^[0-9a-f]{64}$')
TERMINAL={'COMPLETED','FAILED','CANCELED','BLOCKED'}


def checked_path(path):
    path=Path(os.path.abspath(path))
    if any(p.is_symlink() for p in [path,*path.parents]):raise ValueError('Symlink storage paths forbidden')
    return path


def digest(raw):return hashlib.sha256(raw).hexdigest()


def write_new(path, raw):
    checked_path(path)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'wb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())

class Store:
    def __init__(self,root):
        self.root=checked_path(root)
        self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
        self.lock=threading.RLock()
        checked_path(self.root/'objects').mkdir(exist_ok=True,mode=0o700)
        for n in ['metadata.sqlite','audit.jsonl']:checked_path(self.root/n)
        with self.db() as db:
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
            db.execute('PRAGMA user_version=2')

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

    def audit(self,event):
        raw=(canonical({'at':time.time(),**event})+'\n').encode()
        with self.lock:
            path=checked_path(self.root/'audit.jsonl')
            fd=os.open(path,os.O_WRONLY|os.O_APPEND|os.O_CREAT|getattr(os,'O_NOFOLLOW',0),0o600)
            with os.fdopen(fd,'ab') as f:f.write(raw);f.flush();os.fsync(f.fileno())

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
        return h

    def get(self,h):
        if not isinstance(h,str) or not HASH.fullmatch(h):raise ValueError('Invalid artifact identity')
        p=checked_path(self.root/'objects'/f'{h}.json');raw=p.read_bytes()
        if digest(raw)!=h:raise ValueError('Artifact hash mismatch')
        return json.loads(raw)

    def create_run(self,run_id,config,**identity):
        data={'id':run_id,'status':'PENDING','config':config,'created_at':time.time(),'started_at':None,'ended_at':None,
              'logs':[],'error':None,'result_hash':None,'permission':'SYNTHETIC_ONLY',**identity}
        with self.db() as db:db.execute('INSERT INTO runs VALUES (?,?)',(run_id,canonical(data)))
        self.audit({'run_id':run_id,'status':'PENDING'})
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
        self.audit({'run_id':run_id,'status':data['status'],'error':data['error']})
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
                journal=checked_path(self.root/'audit.jsonl')
                write_new(stage/'audit.jsonl',journal.read_bytes() if journal.exists() else b'')
                manifest={'backup_version':'1.0.0','schema_version':SCHEMA,'files':{p.relative_to(stage).as_posix():digest(p.read_bytes()) for p in sorted(stage.rglob('*')) if p.is_file()}}
                write_new(stage/'manifest.json',canonical(manifest).encode())
                stage.rename(dest)
            except BaseException:
                shutil.rmtree(stage)
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
        stage.rename(dest)
    except BaseException:
        shutil.rmtree(stage);raise
    restored=Store(dest);restored.audit({'restore':'COMPLETED','backup_manifest_sha256':digest(canonical(manifest).encode())})
    return restored
