from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
import hashlib
import hmac
import json
import sqlite3
import stat
from uuid import uuid4

import pytest

from psychohistory.decision_records import DecisionRecords
from psychohistory.storage import Store


def snapshot(decision_id=None, revision=1, question='Which fictional project?', *, deadline=None, receipt=None):
    state = {
        'schema_version': '1.0.0', 'decision_id': decision_id or uuid4().hex,
        'revision': revision, 'confirmed': True, 'question': question,
        'options': [{'id': 'a', 'label': 'A'}, {'id': 'b', 'label': 'B'}],
        'deadline': deadline,
    }
    if receipt is not None:
        state['understanding_receipt'] = receipt
    digest = hashlib.sha256(json.dumps(state, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    analysis = {
        'hub_version': '0.4.0', 'decision_id': state['decision_id'],
        'revision': revision, 'input_hash': digest, 'status': 'ANALYZED',
    }
    return state, analysis


def now():
    return datetime.now(UTC).isoformat()


def test_private_storage_requires_explicit_consent(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    assert store.status() == {'authorized': False, 'epoch': None}
    with pytest.raises(PermissionError):
        store.save('ungranted', *snapshot())
    assert not root.exists()

    epoch = store.grant()['epoch']
    assert DecisionRecords(root).status() == {'authorized': True, 'epoch': epoch}
    assert stat.S_IMODE(root.stat().st_mode) == 0o700
    store.save(epoch, *snapshot())
    assert {stat.S_IMODE(path.stat().st_mode) for path in root.iterdir()} == {0o600}


def test_root_cannot_be_a_research_directory_or_symlink(tmp_path):
    research = tmp_path / 'research'
    research.mkdir(mode=0o700)
    (research / 'metadata.sqlite').touch()
    with pytest.raises(ValueError):
        DecisionRecords(research).grant()
    with pytest.raises(ValueError):
        DecisionRecords(research / 'nested').grant()
    alias = tmp_path / 'alias'
    alias.symlink_to(research)
    with pytest.raises(ValueError):
        DecisionRecords(alias).grant()


def test_revisions_are_confirmed_contiguous_and_immutable(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision = state['decision_id']
    with pytest.raises(ValueError):
        store.save(epoch, {**state, 'confirmed': False}, analysis)
    with pytest.raises(ValueError):
        store.save(epoch, state, {**analysis, 'input_hash': '0' * 64})
    with pytest.raises(ValueError):
        store.save(epoch, *snapshot(decision, 2))

    original = store.save(epoch, state, analysis)
    assert store.save(epoch, state, analysis) == original
    with pytest.raises(ValueError):
        store.save(epoch, *snapshot(decision, 1, 'Trying to replace history'))
    store.save(epoch, *snapshot(decision, 2, deadline='Next month'))
    assert store.list(epoch) == [{'decision_id': decision, 'question': 'Which fictional project?', 'revision': 2}]
    assert [item['state']['deadline'] for item in store.get(epoch, decision)['snapshots']] == [None, 'Next month']


def test_new_revisions_preserve_the_original_question_and_understanding_receipt(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    receipt = {'mode': 'GUIDED_CONFIRMATION', 'suggestions': [
        {'field': 'options', 'source': 'Fictional original text', 'value': 'A'}
    ]}
    original, analysis = snapshot(receipt=receipt)
    decision = original['decision_id']
    store.save(epoch, original, analysis)
    with pytest.raises(ValueError):
        store.save(epoch, *snapshot(decision, 2, 'A different original question', receipt=receipt))
    with pytest.raises(ValueError):
        store.save(epoch, *snapshot(decision, 2, receipt={'mode': 'GUIDED_CONFIRMATION'}))
    store.save(epoch, *snapshot(decision, 2, deadline='Next month', receipt=receipt))
    assert store.get(epoch, decision)['snapshots'][1]['state']['understanding_receipt'] == receipt


def test_actual_choice_freezes_predecision_history_and_limits_observations(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision = state['decision_id']
    store.save(epoch, state, analysis)
    with pytest.raises(ValueError):
        store.review(epoch, decision, 'Early observation', now(), 'real')
    with pytest.raises(ValueError):
        store.action(epoch, decision, 'invented-option', now(), 1)
    with pytest.raises(ValueError):
        store.action(epoch, decision, 'a', (datetime.now(UTC) - timedelta(days=1)).isoformat(), 1)

    action_time = now()
    assert store.action(epoch, decision, 'a', action_time, 1)['coverage'] == {'a': 'CHOSEN', 'b': 'UNOBSERVED'}
    with pytest.raises(ValueError):
        store.action(epoch, decision, 'b', now(), 1)
    with pytest.raises(ValueError):
        store.save(epoch, *snapshot(decision, 2))
    with pytest.raises(ValueError):
        store.review(epoch, decision, 'Before the choice', (datetime.now(UTC) - timedelta(days=1)).isoformat(), 'real')

    store.review(epoch, decision, 'Hypothetical example', now(), 'synthetic')
    store.review(epoch, decision, 'Fictional outcome log', now(), 'real')
    record = store.get(epoch, decision)
    assert [(item['option_id'], item['kind']) for item in record['reviews']] == [('a', 'synthetic'), ('a', 'real')]
    assert record['action']['coverage']['b'] == 'UNOBSERVED'


def test_actual_choice_must_name_the_revision_the_user_saw(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision = state['decision_id']
    store.save(epoch, state, analysis)
    store.save(epoch, *snapshot(decision, 2, deadline='Next month'))

    action_time = now()
    with pytest.raises(ValueError, match='revision'):
        store.action(epoch, decision, 'a', action_time, revision=1)
    assert store.get(epoch, decision)['action'] is None
    accepted = store.action(epoch, decision, 'a', action_time, revision=2)
    assert accepted['revision'] == 2
    assert store.action(epoch, decision, 'a', action_time, revision=2) == accepted
    with pytest.raises(ValueError, match='revision'):
        store.action(epoch, decision, 'a', action_time, revision=1)


def test_withdrawal_removes_content_and_rejects_old_writes_and_backups(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot(question='UNIQUE FICTIONAL PRIVATE MARKER')
    store.save(epoch, state, analysis)
    backup = store.export(epoch)
    store.revoke(epoch)

    assert DecisionRecords(root).status() == {'authorized': False, 'epoch': None}
    assert all(b'UNIQUE FICTIONAL PRIVATE MARKER' not in path.read_bytes() for path in root.iterdir())
    with pytest.raises(PermissionError):
        store.save(epoch, *snapshot())
    new_epoch = store.grant()['epoch']
    assert new_epoch and new_epoch != epoch
    assert store.list(new_epoch) == []
    assert store.restore(new_epoch, backup)['eligible'] is False
    with pytest.raises(ValueError):
        store.restore(new_epoch, backup, confirm=True)


def test_delete_tombstone_blocks_reuse_and_restore(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision = state['decision_id']
    store.save(epoch, state, analysis)
    backup = store.export(epoch)
    store.delete(epoch, decision)

    assert store.list(epoch) == []
    with pytest.raises(KeyError):
        store.get(epoch, decision)
    with pytest.raises(ValueError):
        store.save(epoch, state, analysis)
    assert store.restore(epoch, backup)['eligible'] is False
    with pytest.raises(ValueError):
        store.restore(epoch, backup, confirm=True)


def test_restore_preview_does_not_create_content_and_recovery_drops_derivations(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision = state['decision_id']
    store.save(epoch, state, analysis)
    store.save(epoch, *snapshot(decision, 2))
    store.action(epoch, decision, 'b', now(), 2)
    store.review(epoch, decision, 'Fictional review', now(), 'real')
    backup = store.export(epoch)
    data = json.loads(backup['payload'])
    assert data['decisions'][0]['snapshots'][0]['analysis'] == analysis
    assert data['coverage']['reviews'] is True
    (root / 'records.sqlite3').unlink()

    assert store.restore(epoch, backup) == {
        'mode': 'preview', 'isolated': True, 'eligible': True, 'decision_count': 1, 'reason': None,
    }
    assert not (root / 'records.sqlite3').exists()
    assert store.restore(epoch, backup, confirm=True)['decision_count'] == 1
    record = store.get(epoch, decision)
    assert record['snapshots'][0]['state'] == state
    assert record['snapshots'][0]['analysis'] is None
    assert record['snapshots'][0]['analysis_status'] == 'RECOMPUTE_REQUIRED'
    assert record['action']['option_id'] == 'b'
    assert record['reviews'][0]['observation'] == 'Fictional review'
    assert json.loads(backup['payload'])['decisions'][0]['snapshots'][0]['analysis'] == analysis
    assert store.restore(epoch, backup, confirm=True)['decision_count'] == 0


def test_restore_rejects_incomplete_or_inauthentic_backups(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    store.save(epoch, state, analysis)
    old = store.export(epoch)
    store.save(epoch, *snapshot(state['decision_id'], 2))
    current = store.export(epoch)
    tampered = {**current, 'payload': current['payload'].replace('Which fictional project?', 'Replacement content')}
    unlike_store = DecisionRecords(tmp_path / 'other')

    assert store.restore(epoch, old)['eligible'] is False
    assert store.restore(epoch, tampered)['eligible'] is False
    assert unlike_store.restore(unlike_store.grant()['epoch'], current)['eligible'] is False


def test_exports_preceding_a_new_decision_cannot_recover_an_incomplete_store(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    store.save(epoch, *snapshot())
    initial = store.export(epoch)
    store.save(epoch, *snapshot())
    (root / 'records.sqlite3').unlink()

    assert store.restore(epoch, initial)['eligible'] is False
    with pytest.raises(ValueError):
        store.restore(epoch, initial, confirm=True)
    assert not (root / 'records.sqlite3').exists()


def test_authenticated_corrupt_record_shape_is_ineligible_for_restore(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    store.save(epoch, state, analysis)
    export = store.export(epoch)
    data = json.loads(export['payload'])
    data['decisions'][0]['snapshots'][0]['confirmed_at'] = None
    export['payload'] = json.dumps(data)
    with sqlite3.connect(root / 'consent.sqlite3') as db:
        key = db.execute('SELECT signing_key FROM consent').fetchone()[0]
    export['signature'] = hmac.new(key, export['payload'].encode(), hashlib.sha256).hexdigest()
    (root / 'records.sqlite3').unlink()

    assert store.restore(epoch, export)['eligible'] is False
    with pytest.raises(ValueError):
        store.restore(epoch, export, confirm=True)
    assert not (root / 'records.sqlite3').exists()


def test_corrupted_derivations_are_hidden_from_history_and_exports(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    store.save(epoch, state, analysis)
    with sqlite3.connect(root / 'records.sqlite3') as db:
        payload = json.loads(db.execute('SELECT payload FROM records').fetchone()[0])
        payload['snapshots'][0]['analysis']['input_hash'] = 'f' * 64
        db.execute('UPDATE records SET payload=?', (json.dumps(payload),))

    assert store.get(epoch, state['decision_id'])['snapshots'][0]['analysis_status'] == 'RECOMPUTE_REQUIRED'
    assert json.loads(store.export(epoch)['payload'])['coverage']['analysis'] is False


def test_latest_export_repairs_corrupted_content_with_the_same_revision_count(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    store.save(epoch, state, analysis)
    backup = store.export(epoch)
    with sqlite3.connect(root / 'records.sqlite3') as db:
        payload = json.loads(db.execute('SELECT payload FROM records').fetchone()[0])
        payload['snapshots'][0]['state']['question'] = 'Corrupted content'
        db.execute('UPDATE records SET payload=?', (json.dumps(payload),))

    with pytest.raises(ValueError):
        store.get(epoch, state['decision_id'])
    assert store.restore(epoch, backup, confirm=True)['decision_count'] == 1
    result = store.get(epoch, state['decision_id'])['snapshots'][0]
    assert result['state'] == state
    assert result['analysis'] is None


def test_export_signatures_survive_browser_json_number_normalization(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    analysis['fixture_chart'] = {'lower': 0.0, 'upper': 1.0}
    store.save(epoch, state, analysis)
    backup = store.export(epoch)
    assert '"lower":0.0' in backup['payload']
    assert epoch not in backup['payload']
    browser_copy = json.loads(json.dumps(backup), parse_float=lambda value: int(float(value)))
    assert store.restore(epoch, browser_copy)['eligible'] is True


def test_personal_records_are_excluded_from_research_backup(tmp_path):
    research = Store(tmp_path / 'research')
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    store.save(epoch, *snapshot(question='UNIQUE SYNTHETIC PRIVATE MARKER'))

    research.backup(tmp_path / 'research-backup')
    files = [path for path in (tmp_path / 'research-backup').rglob('*') if path.is_file()]
    assert {path.name for path in files} == {'metadata.sqlite', 'audit.jsonl', 'manifest.json'}
    assert all(b'UNIQUE SYNTHETIC PRIVATE MARKER' not in path.read_bytes() for path in files)


def test_competing_writers_cannot_overwrite_a_revision(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision = state['decision_id']
    store.save(epoch, state, analysis)

    def save(deadline):
        try:
            DecisionRecords(root).save(epoch, *snapshot(decision, 2, deadline=deadline))
        except ValueError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=2) as worker:
        assert sorted(worker.map(save, ['Competing edit A', 'Competing edit B'])) == [False, True]
    assert len(store.get(epoch, decision)['snapshots']) == 2


def test_matching_derivative_identity_does_not_hide_content_corruption(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    store.save(epoch, state, {**analysis, 'advice': ['original']})
    with sqlite3.connect(root / 'records.sqlite3') as db:
        payload = json.loads(db.execute('SELECT payload FROM records').fetchone()[0])
        payload['snapshots'][0]['analysis']['advice'] = ['corrupted']
        db.execute('UPDATE records SET payload=?', (json.dumps(payload),))
    assert store.get(epoch, state['decision_id'])['snapshots'][0]['analysis'] is None


def test_retried_identical_review_does_not_append_twice(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    store.save(epoch, state, analysis)
    store.action(epoch, state['decision_id'], 'a', now(), 1)
    observed_at = now()
    first = store.review(epoch, state['decision_id'], 'Fictional follow-up', observed_at, 'synthetic')
    assert store.review(epoch, state['decision_id'], 'Fictional follow-up', observed_at, 'synthetic') == first
    assert store.get(epoch, state['decision_id'])['reviews'] == [first]
