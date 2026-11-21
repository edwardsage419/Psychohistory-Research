from hashlib import sha256
import json

import pytest

from psychohistory.contracts import canonical
from psychohistory.decision_records import DecisionRecords
from test_decision_records import now, snapshot


def preference(value='Choose a shorter commute when costs are comparable'):
    return {
        'values': [{'label': 'Travel time', 'value': value}],
        'applicability': 'Fictional career offers with comparable costs',
        'provenance': 'User-stated during synthetic review',
        'adopted_version_id': None,
    }


def v05_snapshot(**updates):
    state, analysis = snapshot()
    state.update(workflow_version='0.5.0', **updates)
    analysis.update(hub_version='0.5.0', input_hash=sha256(canonical(state).encode()).hexdigest())
    return state, analysis


def reviewed_decision(tmp_path):
    root = tmp_path / 'personal'
    store = DecisionRecords(root)
    epoch = store.grant()['epoch']
    state, analysis = snapshot()
    decision_id = state['decision_id']
    original = store.save(epoch, state, analysis)
    store.action(epoch, decision_id, 'a', now(), 1)
    return root, store, epoch, decision_id, original


def test_hindsight_and_explicit_adoption_leave_the_original_decision_unchanged(tmp_path):
    _, store, epoch, decision_id, original = reviewed_decision(tmp_path)
    phrase = 'A new bus route appeared after the decision'
    review = store.review(epoch, decision_id, 'Fictional chosen outcome', now(), 'synthetic', hindsight={
        'evidence': phrase, 'current_preferences': preference(),
    })

    assert review['hindsight']['evidence'] == phrase
    assert store.preferences(epoch) == []
    with pytest.raises(ValueError):
        store.adopt_preferences(epoch, decision_id, 1, False)
    with pytest.raises(ValueError):
        store.adopt_preferences(epoch, decision_id, 2, True)
    adopted = store.adopt_preferences(epoch, decision_id, 1, True)
    assert store.adopt_preferences(epoch, decision_id, 1, True) == adopted
    assert store.preferences(epoch) == [adopted]
    assert adopted['source_kind'] == 'synthetic'
    assert adopted['preferences'] == preference()

    history = store.get(epoch, decision_id)
    assert history['snapshots'] == [original]
    assert history['action']['coverage'] == {'a': 'CHOSEN', 'b': 'UNOBSERVED'}
    assert history['reviews'][0]['observation'] == 'Fictional chosen outcome'
    assert history['reviews'][0]['adopted_preferences'] == adopted


def test_hindsight_can_record_process_quality_separately_from_the_observed_outcome(tmp_path):
    _, store, epoch, decision_id, original = reviewed_decision(tmp_path)
    outcome = 'The fictional employer later withdrew the offer'
    assessment = 'The decision checked the deadline and uncertainty before committing'
    review = store.review(epoch, decision_id, outcome, now(), 'synthetic', hindsight={
        'process_quality': assessment,
    })

    assert review['observation'] == outcome
    assert review['hindsight'] == {'evidence': None, 'current_preferences': None, 'process_quality': assessment}
    assert store.get(epoch, decision_id)['snapshots'] == [original]
    with pytest.raises(ValueError):
        store.adopt_preferences(epoch, decision_id, 1, True)


def test_exports_round_trip_preference_versions_and_keep_v04_archive_contract(tmp_path):
    root, store, epoch, decision_id, _ = reviewed_decision(tmp_path)
    old = store.export(epoch)
    assert old['backup_version'] == '1.0.0'
    assert store.restore(epoch, old)['eligible'] is True

    store.review(epoch, decision_id, 'Synthetic outcome', now(), 'synthetic', hindsight={
        'evidence': None, 'current_preferences': preference(),
    })
    before_adoption = store.export(epoch)
    adopted = store.adopt_preferences(epoch, decision_id, 1, True)
    backup = store.export(epoch)
    assert backup['backup_version'] == '1.1.0'
    assert json.loads(backup['payload'])['coverage']['preference_versions'] is True
    assert store.restore(epoch, old)['eligible'] is False
    assert store.restore(epoch, before_adoption)['eligible'] is False

    (root / 'records.sqlite3').unlink()
    assert store.restore(epoch, backup)['eligible'] is True
    assert not (root / 'records.sqlite3').exists()
    assert store.restore(epoch, backup, confirm=True)['decision_count'] == 1
    assert store.preferences(epoch) == [adopted]
    assert store.get(epoch, decision_id)['snapshots'][0]['analysis'] is None


def test_revoke_or_delete_removes_future_preference_versions(tmp_path):
    _, store, epoch, decision_id, _ = reviewed_decision(tmp_path)
    store.review(epoch, decision_id, 'Fictional outcome', now(), 'real', hindsight={
        'evidence': 'A later observation', 'current_preferences': preference(),
    })
    store.adopt_preferences(epoch, decision_id, 1, True)
    backup = store.export(epoch)
    store.delete(epoch, decision_id)
    assert store.preferences(epoch) == []
    assert store.restore(epoch, backup)['eligible'] is False

    store.revoke(epoch)
    with pytest.raises(PermissionError):
        store.preferences(epoch)
    assert store.preferences(store.grant()['epoch']) == []


def test_a_saved_plan_neither_executes_nor_constrains_the_observed_actual_choice(tmp_path):
    store = DecisionRecords(tmp_path / 'personal')
    epoch = store.grant()['epoch']
    state, analysis = v05_snapshot(intended_option_id='b', plan_note='Ask for a written offer', preferences=preference())
    decision_id = state['decision_id']
    prior = store.save(epoch, state, analysis)
    assert store.get(epoch, decision_id)['action'] is None
    with pytest.raises(ValueError, match='v0.5'):
        store.action(epoch, decision_id, 'a', now(), 1, allow_v05=False)
    with pytest.raises(ValueError, match='v0.5'):
        store.save(epoch, *snapshot(decision_id, 2))

    store.action(epoch, decision_id, 'a', now(), 1)
    with pytest.raises(ValueError, match='v0.5'):
        store.review(epoch, decision_id, 'Sent through legacy route', now(), 'real', allow_v05=False)
    store.review(epoch, decision_id, 'Fictional outcome for the chosen alternative', now(), 'synthetic')
    record = store.get(epoch, decision_id)
    assert record['snapshots'] == [prior]
    assert record['snapshots'][0]['state']['intended_option_id'] == 'b'
    assert record['action']['option_id'] == 'a'
    assert record['action']['coverage']['b'] == 'UNOBSERVED'
    assert store.export(epoch)['backup_version'] == '1.1.0'


def test_future_adoption_can_be_linked_only_with_unchanged_preference_data(tmp_path):
    _, store, epoch, decision_id, _ = reviewed_decision(tmp_path)
    store.review(epoch, decision_id, 'Synthetic outcome', now(), 'synthetic', hindsight={'current_preferences': preference()})
    adopted = store.adopt_preferences(epoch, decision_id, 1, True)
    version_id = adopted['version_id']
    linked = {**preference(), 'adopted_version_id': version_id}

    with pytest.raises(ValueError, match='preference version'):
        store.save(epoch, *v05_snapshot(preferences={**linked, 'applicability': 'Unrelated context'}))
    with pytest.raises(ValueError, match='preference version'):
        store.save(epoch, *v05_snapshot(preferences={**linked, 'adopted_version_id': 'f' * 32}))
    future = store.save(epoch, *v05_snapshot(preferences=linked))
    assert future['state']['preferences'] == linked
    assert future['state'].get('weights') is None

    store.delete(epoch, decision_id)
    assert store.preferences(epoch) == []
    assert store.get(epoch, future['decision_id'])['snapshots'][0]['state']['preferences'] == linked
    with pytest.raises(ValueError, match='preference version'):
        store.save(epoch, *v05_snapshot(preferences=linked))
