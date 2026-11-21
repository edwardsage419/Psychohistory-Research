"""Consent-scoped personal records, kept outside the research store."""

from contextlib import contextmanager
from datetime import UTC, datetime
from hashlib import sha256
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import stat
from uuid import uuid4

from .contracts import canonical
from .decision_preferences import AdoptedPreference, Hindsight
from .decision_state import DecisionState, HUB_VERSION, SCHEMA_VERSION
from .storage import checked_path, fsync_directory


_ID = re.compile(r'[0-9a-f]{32}')
_SCHEMA = 1
_BACKUP_VERSION = '1.0.0'
_V05_WORKFLOW = '0.5.0'
_V05_BACKUP_VERSION = '1.1.0'
_COVERAGE = {
    'current_state': True, 'edit_history': True, 'confirmations': True,
    'action': True, 'reviews': True, 'sources': True,
}
_EXTERNAL_BACKUPS = 'Application deletion covers local records. Keep externally saved copies private and delete them separately.'


def _digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def _decision_id(value):
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ValueError('Invalid decision identity')
    return value


def _time(value):
    if not isinstance(value, str) or 'T' not in value:
        raise ValueError('Use an ISO 8601 timestamp with a timezone')
    try:
        timestamp = datetime.fromisoformat(value)
        if timestamp.tzinfo is None:
            raise ValueError('Missing timezone')
        return timestamp.astimezone(UTC)
    except (OverflowError, ValueError) as exc:
        raise ValueError('Use an ISO 8601 timestamp with a timezone') from exc


def _options(state):
    options = state.get('options')
    if not isinstance(options, list) or not options:
        raise ValueError('At least one option is required')
    ids = [row.get('id') for row in options if isinstance(row, dict)]
    if len(ids) != len(options) or any(not isinstance(value, str) or not value.strip() for value in ids):
        raise ValueError('Options require valid identities')
    if len(set(ids)) != len(ids):
        raise ValueError('Option identities must be unique')
    return ids


def _state_identity(state):
    if not isinstance(state, dict) or state.get('schema_version') != SCHEMA_VERSION or state.get('confirmed') is not True:
        raise ValueError('A confirmed decision state is required')
    try:
        if state.get('workflow_version') == _V05_WORKFLOW:
            from .decision_v05 import DecisionStateV05

            validated = DecisionStateV05.model_validate(state)
        else:
            validated = DecisionState.model_validate(state)
    except ValueError as exc:
        raise ValueError('The saved decision does not satisfy the decision schema') from exc
    _options(state)
    return validated.decision_id, validated.revision


def _check_origin(original, state):
    if original['question'] != state['question'] or original.get('understanding_receipt') != state.get('understanding_receipt'):
        raise ValueError('Revisions must preserve the original question and understanding receipt')


def _valid_analysis(state, analysis):
    version = _V05_WORKFLOW if state.get('workflow_version') == _V05_WORKFLOW else HUB_VERSION
    return (
        isinstance(analysis, dict) and analysis.get('hub_version') == version
        and analysis.get('decision_id') == state['decision_id']
        and type(analysis.get('revision')) is int and analysis['revision'] == state['revision']
        and analysis.get('input_hash') == _digest(state)
        and analysis.get('status') in ('CLARIFY', 'ANALYZED', 'UNRESOLVED')
    )


def _present(snapshot):
    public = {key: value for key, value in snapshot.items() if key != 'analysis_hash'}
    analysis = public['analysis']
    try:
        valid = _valid_analysis(public['state'], analysis) and snapshot.get('analysis_hash') == _digest(analysis)
    except (TypeError, ValueError):
        valid = False
    if not valid:
        return {**public, 'analysis': None, 'analysis_status': 'RECOMPUTE_REQUIRED'}
    return {**public, 'analysis_status': 'AVAILABLE'}


def _checkpoints(record):
    return len(record['snapshots']), int(record['action'] is not None) + len(record['reviews'])


def _record_digest(record):
    return _digest({
        'decision_id': record['decision_id'], 'action': record['action'], 'reviews': record['reviews'],
        'snapshots': [
            {field: snapshot[field] for field in ('decision_id', 'revision', 'state', 'confirmed_at')}
            for snapshot in record['snapshots']
        ],
    })


def _event_times(value, earliest, recorded):
    occurred = _time(value)
    if not _time(earliest) <= occurred <= recorded:
        raise ValueError('Event time must follow its prerequisite and cannot be in the future')
    return occurred.isoformat()


def _signature(payload, key):
    return hmac.new(key, payload.encode(), sha256).hexdigest()


def _coverage(options, chosen):
    return {option: 'CHOSEN' if option == chosen else 'UNOBSERVED' for option in options}


def _uses_v05(record):
    return any(snapshot['state'].get('workflow_version') == _V05_WORKFLOW for snapshot in record['snapshots']) or any(
        'hindsight' in review for review in record['reviews']
    )


def _backup_version(records):
    return _V05_BACKUP_VERSION if any(map(_uses_v05, records)) else _BACKUP_VERSION


def _check_adoption(adopted, review, decision_id, review_index):
    adoption = AdoptedPreference.model_validate(adopted)
    hindsight = review.get('hindsight', {})
    if adoption.model_dump(mode='json') != adopted or adoption.decision_id != decision_id or (
        adoption.review_index != review_index or adoption.source_kind != review['kind']
        or adopted['preferences'] != hindsight.get('current_preferences')
        or _time(adoption.adopted_at) < _time(review['recorded_at'])
    ):
        raise ValueError('The export contains an unrelated future preference adoption')


def _validate_exported_record(record):
    if not isinstance(record, dict) or set(record) != {'decision_id', 'snapshots', 'action', 'reviews'}:
        raise ValueError('The export contains an invalid decision record')
    decision_id = _decision_id(record['decision_id'])
    snapshots, action, reviews = record['snapshots'], record['action'], record['reviews']
    if not isinstance(snapshots, list) or not snapshots or not isinstance(reviews, list):
        raise ValueError('The export contains incomplete decision history')
    for revision, snapshot in enumerate(snapshots, 1):
        if not isinstance(snapshot, dict) or set(snapshot) != {
            'decision_id', 'revision', 'state', 'analysis', 'analysis_status', 'confirmed_at',
        }:
            raise ValueError('The export contains an invalid decision snapshot')
        if _state_identity(snapshot['state']) != (decision_id, revision) or (
            snapshot['decision_id'], snapshot['revision']
        ) != (decision_id, revision) or type(snapshot['revision']) is not int:
            raise ValueError('The export contains mismatched decision identities')
        _check_origin(snapshots[0]['state'], snapshot['state'])
        _time(snapshot['confirmed_at'])
    if action is None:
        if reviews:
            raise ValueError('The export contains observations without an actual action')
        return decision_id
    if not isinstance(action, dict) or set(action) != {'option_id', 'revision', 'coverage', 'occurred_at', 'recorded_at'}:
        raise ValueError('The export contains an invalid actual action')
    latest = snapshots[-1]
    options, chosen = _options(latest['state']), action['option_id']
    if type(action['revision']) is not int or action['revision'] != latest['revision'] or chosen not in options:
        raise ValueError('The export contains an action unrelated to the latest revision')
    if action['coverage'] != _coverage(options, chosen):
        raise ValueError('The export contains invalid observation coverage')
    _event_times(action['occurred_at'], latest['confirmed_at'], _time(action['recorded_at']))
    fields = {'option_id', 'observation', 'kind', 'observed_at', 'recorded_at'}
    for index, review in enumerate(reviews, 1):
        if not isinstance(review, dict) or not fields <= set(review) <= fields | {'hindsight', 'adopted_preferences'}:
            raise ValueError('The export contains an invalid observation')
        if review['option_id'] != chosen or review['kind'] not in ('real', 'synthetic') or (
            not isinstance(review['observation'], str) or not review['observation'].strip()
        ):
            raise ValueError('The export contains an observation unrelated to the actual action')
        _event_times(review['observed_at'], action['occurred_at'], _time(review['recorded_at']))
        if 'hindsight' in review and Hindsight.model_validate(review['hindsight']).model_dump(mode='json') != review['hindsight']:
            raise ValueError('The export contains an invalid hindsight entry')
        if 'adopted_preferences' in review:
            _check_adoption(review['adopted_preferences'], review, decision_id, index)
    return decision_id


class DecisionRecords:
    """User-private SQLite files with a separately retained consent and deletion ledger."""

    def __init__(self, root):
        self.root = checked_path(root)
        self._ledger = self.root / 'consent.sqlite3'
        self._records = self.root / 'records.sqlite3'

    def _check_root(self):
        checked_path(self.root)
        if any((directory / 'metadata.sqlite').exists() for directory in (self.root, *self.root.parents)):
            raise ValueError('Personal decisions require a separate directory from research storage')
        if self.root.exists():
            info = self.root.stat()
            if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
                raise ValueError('Personal decisions require an owner-only directory')

    def _check_file(self, path):
        for entry in (path, *(path.with_name(path.name + suffix) for suffix in ('-journal', '-wal', '-shm'))):
            checked_path(entry)
            try:
                info = entry.stat()
            except FileNotFoundError:
                continue
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077 or info.st_nlink != 1:
                raise ValueError('Personal storage files must be private regular files')

    def _create_file(self, path):
        self._check_file(path)
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            return
        os.close(fd)
        fsync_directory(self.root)

    @contextmanager
    def _database(self, *, write=False):
        self._check_root()
        self._check_file(self._ledger)
        mode = 'rw' if write else 'ro'
        db = sqlite3.connect(self._ledger.as_uri() + f'?mode={mode}', uri=True, timeout=10)
        try:
            if write:
                self._write_settings(db, 'main')
                db.execute('PRAGMA main.synchronous=EXTRA')
            db.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
            yield db
            db.commit()
        finally:
            db.close()

    @staticmethod
    def _write_settings(db, schema):
        if db.execute(f'PRAGMA {schema}.journal_mode').fetchone()[0] != 'delete':
            raise ValueError('Personal storage requires SQLite rollback journals')
        db.execute(f'PRAGMA {schema}.secure_delete=ON')

    @staticmethod
    def _authorization(db):
        version = db.execute('PRAGMA main.user_version').fetchone()[0]
        if version == 0:
            if db.execute('SELECT 1 FROM main.sqlite_master').fetchone():
                raise ValueError('Unrecognized personal consent ledger')
            return None, None
        if version != _SCHEMA:
            raise ValueError('Unrecognized personal consent ledger')
        row = db.execute('SELECT epoch, signing_key FROM main.consent').fetchone()
        if row is None or (row[0] is None) != (row[1] is None):
            raise ValueError('Unrecognized personal consent ledger')
        if row[0] is not None and (not isinstance(row[1], bytes) or len(row[1]) != 32):
            raise ValueError('Unrecognized personal consent ledger')
        return row

    @contextmanager
    def _authorized(self, epoch, *, write=False):
        self._check_root()
        self._check_file(self._ledger)
        if not self._ledger.exists():
            raise PermissionError('Active personal storage consent is required')
        with self._database(write=write) as db:
            active, key = self._authorization(db)
            if active is None or not isinstance(epoch, str) or active != epoch:
                raise PermissionError('Active personal storage consent is required')
            yield db, key

    def status(self):
        self._check_root()
        self._check_file(self._ledger)
        if not self._ledger.exists():
            return {'authorized': False, 'epoch': None}
        with self._database() as db:
            epoch, _ = self._authorization(db)
            return {'authorized': epoch is not None, 'epoch': epoch}

    def grant(self):
        self._check_root()
        self._check_file(self._records)
        if self._records.exists() and not self._ledger.exists():
            raise ValueError('Existing personal records require their original consent ledger')
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._check_root()
        self._create_file(self._ledger)
        with self._database(write=True) as db:
            epoch, _ = self._authorization(db)
            if db.execute('PRAGMA main.user_version').fetchone()[0] == 0:
                if self._records.exists():
                    raise ValueError('Existing personal records require their original consent ledger')
                db.execute('CREATE TABLE consent (id INTEGER PRIMARY KEY CHECK (id=1), epoch TEXT, signing_key BLOB)')
                db.execute('''CREATE TABLE history (
                    identity TEXT PRIMARY KEY, revision INTEGER NOT NULL, events INTEGER NOT NULL,
                    deleted INTEGER NOT NULL, content_hash TEXT
                )''')
                db.execute('INSERT INTO consent VALUES (1, NULL, NULL)')
                db.execute('PRAGMA main.user_version=1')
            if epoch is None:
                epoch = uuid4().hex
                db.execute('UPDATE consent SET epoch=?, signing_key=?', (epoch, secrets.token_bytes(32)))
            return {'authorized': True, 'epoch': epoch}

    def _content(self, db, *, write=False, create=False):
        self._check_file(self._records)
        if not self._records.exists():
            if not create:
                return False
            self._create_file(self._records)
        if not any(row[1] == 'personal' for row in db.execute('PRAGMA database_list')):
            mode = 'rw' if write else 'ro'
            db.execute('ATTACH DATABASE ? AS personal', (self._records.as_uri() + f'?mode={mode}',))
            if write:
                # SQLite commits the attached records and consent ledger together in
                # rollback-journal mode. Apply secure deletion to both files.
                self._write_settings(db, 'personal')
        version = db.execute('PRAGMA personal.user_version').fetchone()[0]
        if version == 0 and db.execute('SELECT 1 FROM personal.sqlite_master').fetchone() is None:
            if not create:
                return False
            db.execute('CREATE TABLE personal.records (decision_id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            db.execute('PRAGMA personal.user_version=1')
        elif version != _SCHEMA:
            raise ValueError('Unrecognized personal record store')
        return True

    @staticmethod
    def _history(db, decision_id):
        identity = _digest(decision_id)
        return db.execute(
            'SELECT revision, events, deleted, content_hash FROM main.history WHERE identity=?', (identity,),
        ).fetchone()

    @staticmethod
    def _record(db, decision_id):
        row = db.execute('SELECT payload FROM personal.records WHERE decision_id=?', (decision_id,)).fetchone()
        return json.loads(row[0]) if row else None

    @staticmethod
    def _write_record(db, record):
        decision_id = record['decision_id']
        db.execute('INSERT OR REPLACE INTO personal.records VALUES (?,?)', (decision_id, canonical(record)))
        db.execute('INSERT OR REPLACE INTO main.history VALUES (?,?,?,0,?)', (
            _digest(decision_id), *_checkpoints(record), _record_digest(record),
        ))

    @staticmethod
    def _matches_record(record, expected):
        try:
            return _checkpoints(record) == expected[:2] and _record_digest(record) == expected[3]
        except (TypeError, KeyError, ValueError):
            return False

    @classmethod
    def _verify_record(cls, record, expected):
        if not cls._matches_record(record, expected):
            raise ValueError('Personal history is incomplete or corrupted. Restore the latest authenticated export.')
        return record

    def _get_record(self, db, decision_id, *, write=False):
        history = self._history(db, _decision_id(decision_id))
        if history is None or history[2]:
            raise KeyError('Unknown decision')
        record = self._record(db, decision_id) if self._content(db, write=write) else None
        return self._verify_record(record, history)

    @staticmethod
    def _render(record):
        return {**record, 'snapshots': [_present(item) for item in record['snapshots']]}

    def _all(self, db, *, write=False):
        expected = {key: tuple(history) for key, *history in db.execute(
            'SELECT identity, revision, events, deleted, content_hash FROM main.history WHERE deleted=0'
        )}
        records = []
        if self._content(db, write=write):
            for decision_id, payload in db.execute('SELECT decision_id,payload FROM personal.records ORDER BY decision_id'):
                counts = expected.pop(_digest(decision_id), None)
                if counts is None:
                    raise ValueError('Personal record is not authorized by the local ledger')
                records.append(self._verify_record(json.loads(payload), counts))
        if expected:
            raise ValueError('Personal history is incomplete. Restore the latest authenticated export.')
        return records

    def _adoptions(self, db, *, write=False):
        return [
            review['adopted_preferences'] for record in self._all(db, write=write)
            for review in record['reviews'] if 'adopted_preferences' in review
        ]

    def _check_preference_version(self, db, snapshot, previous=None):
        if snapshot is None or snapshot == previous or not snapshot.get('adopted_version_id'):
            return
        version_id = snapshot['adopted_version_id']
        for adoption in self._adoptions(db, write=True):
            if adoption['version_id'] == version_id and snapshot == {**adoption['preferences'], 'adopted_version_id': version_id}:
                return
        raise ValueError('The selected preference version is unavailable or its values or applicability were edited')

    def revoke(self, epoch):
        with self._authorized(epoch, write=True) as (db, _):
            if self._content(db, write=True):
                db.execute('DELETE FROM personal.records')
            db.execute('UPDATE main.history SET revision=0, events=0, deleted=1, content_hash=NULL')
            db.execute('UPDATE main.consent SET epoch=NULL, signing_key=NULL')
        return {'authorized': False, 'epoch': None, 'scope': 'local_store', 'external_backups': _EXTERNAL_BACKUPS}

    def save(self, epoch, state, analysis):
        with self._authorized(epoch, write=True) as (db, _):
            state = json.loads(canonical(state))
            analysis = json.loads(canonical(analysis))
            decision_id, revision = _state_identity(state)
            if not _valid_analysis(state, analysis):
                raise ValueError('Analysis does not match the confirmed decision revision')
            history = self._history(db, decision_id)
            preferences = state.get('preferences')
            if history is None:
                if revision != 1:
                    raise ValueError('The first saved decision revision must be 1')
                self._check_preference_version(db, preferences)
                self._content(db, write=True, create=True)
                if self._record(db, decision_id) is not None:
                    raise ValueError('Decision has no active ledger entry')
                record = {'decision_id': decision_id, 'snapshots': [], 'action': None, 'reviews': []}
            else:
                if history[2]:
                    raise ValueError('Deleted decision identities cannot be reused')
                record = self._get_record(db, decision_id, write=True)
                _check_origin(record['snapshots'][0]['state'], state)
                if revision <= history[0]:
                    existing = record['snapshots'][revision - 1]
                    if state == existing['state']:
                        return _present(existing)
                    raise ValueError('A saved revision cannot be replaced')
                if record['action'] is not None:
                    raise ValueError('Predecision snapshots are closed after recording the actual action')
                if revision != history[0] + 1:
                    raise ValueError('Revisions must be saved in consecutive order')
                latest = record['snapshots'][-1]['state']
                if latest.get('workflow_version') == _V05_WORKFLOW and state.get('workflow_version') != _V05_WORKFLOW:
                    raise ValueError('Use the v0.5 workbench to revise this decision')
                self._check_preference_version(db, preferences, latest.get('preferences'))
            snapshot = {
                'decision_id': decision_id, 'revision': revision, 'state': state, 'analysis': analysis,
                'analysis_hash': _digest(analysis), 'confirmed_at': datetime.now(UTC).isoformat(),
            }
            record['snapshots'].append(snapshot)
            self._write_record(db, record)
            return _present(snapshot)

    def list(self, epoch):
        with self._authorized(epoch) as (db, _):
            return [
                {key: record['snapshots'][-1]['state'][key] for key in ('decision_id', 'question', 'revision')}
                for record in self._all(db)
            ]

    def get(self, epoch, decision_id):
        with self._authorized(epoch) as (db, _):
            return self._render(self._get_record(db, decision_id))

    def action(self, epoch, decision_id, option_id, occurred_at, revision, *, allow_v05=True):
        with self._authorized(epoch, write=True) as (db, _):
            record = self._get_record(db, decision_id, write=True)
            if not allow_v05 and _uses_v05(record):
                raise ValueError('Use the v0.5 workbench to record this action')
            latest = record['snapshots'][-1]
            if type(revision) is not int or revision != latest['revision']:
                raise ValueError('The action must name the latest confirmed revision')
            options = _options(latest['state'])
            if option_id not in options:
                raise ValueError('Choose an option from the latest confirmed revision')
            recorded = datetime.now(UTC)
            occurred = _event_times(occurred_at, latest['confirmed_at'], recorded)
            action = record['action']
            if action is not None:
                if action['option_id'] == option_id and action['occurred_at'] == occurred:
                    return action
                raise ValueError('The recorded actual action is immutable')
            action = {
                'option_id': option_id, 'occurred_at': occurred, 'recorded_at': recorded.isoformat(),
                'revision': revision,
                'coverage': _coverage(options, option_id),
            }
            record['action'] = action
            self._write_record(db, record)
            return action

    def review(self, epoch, decision_id, observation, observed_at, kind, *, hindsight=None, allow_v05=True):
        with self._authorized(epoch, write=True) as (db, _):
            record = self._get_record(db, decision_id, write=True)
            if not allow_v05 and (hindsight is not None or _uses_v05(record)):
                raise ValueError('Use the v0.5 workbench to record this review')
            action = record['action']
            if action is None:
                raise ValueError('Record the actual action before reviewing it')
            if not isinstance(kind, str) or kind.lower() not in ('real', 'synthetic'):
                raise ValueError('Specify whether the review is real or synthetic')
            if not isinstance(observation, str) or not observation.strip():
                raise ValueError('An observation is required')
            recorded = datetime.now(UTC)
            review = {
                'option_id': action['option_id'], 'observation': observation, 'kind': kind.lower(),
                'observed_at': _event_times(observed_at, action['occurred_at'], recorded),
                'recorded_at': recorded.isoformat(),
            }
            if hindsight is not None:
                review['hindsight'] = Hindsight.model_validate(hindsight).model_dump(mode='json')
            for existing in record['reviews']:
                if all(existing.get(field) == review.get(field) for field in ('observation', 'kind', 'observed_at', 'hindsight')):
                    return existing
            record['reviews'].append(review)
            self._write_record(db, record)
            return review

    def preferences(self, epoch):
        with self._authorized(epoch) as (db, _):
            return sorted(self._adoptions(db), key=lambda version: (version['adopted_at'], version['version_id']), reverse=True)

    def adopt_preferences(self, epoch, decision_id, review_index, confirmed):
        with self._authorized(epoch, write=True) as (db, _):
            if confirmed is not True:
                raise ValueError('Explicit confirmation is required to adopt future preferences')
            record = self._get_record(db, decision_id, write=True)
            if type(review_index) is not int or not 1 <= review_index <= len(record['reviews']):
                raise ValueError('Select an existing review')
            review = record['reviews'][review_index - 1]
            preferences = review.get('hindsight', {}).get('current_preferences')
            if preferences is None:
                raise ValueError('The selected review has no current preference statement')
            if 'adopted_preferences' not in review:
                review['adopted_preferences'] = {
                    'version_id': uuid4().hex, 'adopted_at': datetime.now(UTC).isoformat(),
                    'decision_id': decision_id, 'review_index': review_index,
                    'source_kind': review['kind'], 'preferences': preferences,
                }
                self._write_record(db, record)
            return review['adopted_preferences']

    def delete(self, epoch, decision_id):
        with self._authorized(epoch, write=True) as (db, _):
            history = self._history(db, _decision_id(decision_id))
            if history is None:
                raise KeyError('Unknown decision')
            if self._content(db, write=True):
                db.execute('DELETE FROM personal.records WHERE decision_id=?', (decision_id,))
            db.execute('UPDATE main.history SET revision=0,events=0,deleted=1,content_hash=NULL WHERE identity=?',
                       (_digest(decision_id),))
        return {'decision_id': decision_id, 'deleted': True, 'external_backups': _EXTERNAL_BACKUPS}

    def export(self, epoch):
        with self._authorized(epoch) as (db, key):
            records = [self._render(record) for record in self._all(db)]
            version = _backup_version(records)
            coverage = {**_COVERAGE, 'analysis': all(
                item['analysis'] is not None for record in records for item in record['snapshots']
            )}
            if version == _V05_BACKUP_VERSION:
                coverage.update(plans=True, hindsight=True, preference_versions=True)
            data = {
                'backup_version': version, 'epoch': _digest(epoch),
                'exported_at': datetime.now(UTC).isoformat(), 'decisions': records,
                'coverage': coverage,
                'external_backups': _EXTERNAL_BACKUPS,
            }
            # Sign the text rather than a JSON object whose numbers a browser
            # may reserialize differently (for example, 0.0 as 0).
            payload = canonical(data)
            return {'backup_version': version, 'payload': payload, 'signature': _signature(payload, key)}

    def _restore_records(self, db, epoch, key, backup):
        if not isinstance(backup, dict) or backup.get('backup_version') not in (_BACKUP_VERSION, _V05_BACKUP_VERSION):
            raise ValueError('Unrecognized personal export format')
        version = backup['backup_version']
        payload = backup.get('payload')
        signature = backup.get('signature')
        if not isinstance(payload, str) or not isinstance(signature, str) or not re.fullmatch(r'[0-9a-f]{64}', signature):
            raise ValueError('The export is missing its signed payload')
        try:
            authenticated = hmac.compare_digest(signature, _signature(payload, key))
        except UnicodeError as exc:
            raise ValueError('The signed payload is invalid UTF-8') from exc
        if not authenticated:
            raise ValueError('The export could not be authenticated by the current consent grant')

        # Authentication limits the supported format to data emitted by export().
        # Current ledger checkpoints prevent rollback when an authentic copy is old.
        data = json.loads(payload)
        if not isinstance(data, dict) or data.get('backup_version') != version or data.get('epoch') != _digest(epoch):
            raise ValueError('The export belongs to a different format or consent grant')
        records = data.get('decisions')
        if not isinstance(records, list):
            raise ValueError('The export does not contain decision records')
        expected = db.execute('SELECT COUNT(*) FROM main.history WHERE deleted=0').fetchone()[0]
        if len(records) != expected:
            raise ValueError('The export does not cover the current personal history')
        seen = set()
        for record in records:
            decision_id = _validate_exported_record(record)
            history = self._history(db, decision_id)
            if history is None or history[2] or decision_id in seen:
                raise ValueError('The export contains deleted or unrecognized decisions')
            self._verify_record(record, history)
            seen.add(decision_id)
        if _backup_version(records) != version:
            raise ValueError('The export version does not match its decision records')
        return records

    def restore(self, epoch, backup, confirm=False):
        if type(confirm) is not bool:
            raise ValueError('Restore requires an explicit confirmation')
        with self._authorized(epoch, write=confirm) as (db, key):
            try:
                records = self._restore_records(db, epoch, key, backup)
            except ValueError as error:
                if confirm:
                    raise
                return {'mode': 'preview', 'isolated': True, 'eligible': False, 'decision_count': 0, 'reason': str(error)}
            if not confirm:
                return {'mode': 'preview', 'isolated': True, 'eligible': True, 'decision_count': len(records), 'reason': None}
            restored = 0
            if records:
                self._content(db, write=True, create=True)
                for record in records:
                    decision_id = record['decision_id']
                    try:
                        current = self._record(db, decision_id)
                    except json.JSONDecodeError:
                        current = None
                    if self._matches_record(current, self._history(db, decision_id)):
                        continue
                    for snapshot in record['snapshots']:
                        snapshot['analysis'] = None
                        snapshot.pop('analysis_status', None)
                    self._write_record(db, record)
                    restored += 1
            return {'mode': 'restored', 'isolated': False, 'decision_count': restored}
