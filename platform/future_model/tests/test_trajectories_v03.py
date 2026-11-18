from pathlib import Path
import time

from fastapi.testclient import TestClient

from psychohistory.api import create_app


REPO = Path(__file__).resolve().parents[3]
HEADERS = {'Authorization': 'Bearer test-token'}
LOGISTIC = {'initial': ['1/4', '3/4'], 'payoff': [['2', '2'], ['1', '1']],
            'method': 'rk4', 'steps': 8, 'step_size': '1/8'}


def settle(client, identity):
    approved = client.post(f'/api/v3/experiments/{identity}/approve')
    assert approved.status_code == 200, approved.json()
    for _ in range(300):
        response = client.get(f'/api/v3/experiments/{identity}').json()
        if response['status'] in {'COMPLETED', 'FAILED', 'BLOCKED', 'CANCELED'}:
            assert response['status'] == 'COMPLETED', response
            return response
        time.sleep(0.02)
    raise AssertionError('Trajectory experiment did not reach terminal state')


def start(client, research, model, parameters, parent=None):
    source = client.post('/api/v2/sources', json={'research_id': research}).json()
    response = client.post('/api/v3/experiments', json={
        'source_id': source['source_id'], 'model_id': model, 'model_version': '1.0.0',
        'parameters': parameters, 'branch_from': parent,
    })
    assert response.status_code == 201, response.json()
    item = response.json()
    assert item['status'] == 'PENDING'
    return item


def test_trajectory_versions_and_approval_are_separate_from_legacy(tmp_path):
    with TestClient(create_app(tmp_path, REPO, 'test-token'), headers=HEADERS) as client:
        models = client.get('/api/v3/models')
        assert models.status_code == 200
        assert {(m['model_id'], m['version']) for m in models.json()} == {
            ('r123-degroot', '1.0.0'), ('r132-replicator', '1.0.0')}
        item = start(client, 'R132', 'r132-replicator', LOGISTIC)
        identity = item['id']
        assert client.get(f'/api/v1/runs/{identity}').status_code == 404
        assert client.get(f'/api/v2/experiments/{identity}').status_code == 404
        assert client.get(f'/api/v3/experiments/{identity}/result').status_code == 422
        run = settle(client, identity)
        result = client.get(f'/api/v3/experiments/{identity}/result').json()
        artifact = result['result']
        assert run['result_hash'] == result['artifact_sha256']
        assert artifact['source']['research_id'] == 'R132' and artifact['source']['origin'] == 'MAIN'
        assert all(len(f['blob']) == 40 and len(f['sha256']) == 64 for f in artifact['source']['files'])
        assert artifact['scope'] == 'SYNTHETIC_ONLY' and artifact['evidence']['kind'] == 'UNKNOWN'
        assert len(artifact['trajectory']) == 9


def test_compatible_comparison_checkpoint_and_unrelated_target_rejection(tmp_path):
    with TestClient(create_app(tmp_path, REPO, 'test-token'), headers=HEADERS) as client:
        model = 'r132-replicator'
        left = start(client, 'R132', model, LOGISTIC)['id']
        right = start(client, 'R132', model, {**LOGISTIC, 'method': 'euler'})['id']
        for item in (left, right):
            settle(client, item)
        pair = {'left': left, 'right': right, 'metric': 'trajectory'}
        match = client.post('/api/v3/compare', json=pair)
        assert match.status_code == 200, match.json()
        assert match.json()['samples'] == 9
        assert match.json()['max_abs_difference'] > 0
        assert client.post('/api/v3/compare', json={**pair, 'metric': 'brier'}).status_code == 422

        prior = client.get(f'/api/v3/experiments/{left}/result').json()
        branch = start(client, 'R132', model, {**LOGISTIC, 'steps': 3}, left)['id']
        settle(client, branch)
        resumed = client.get(f'/api/v3/experiments/{branch}/result').json()['result']
        assert resumed['snapshot']['payload']['parent_hash'] == prior['result']['snapshot']['content_hash']
        assert resumed['trajectory'][0] == prior['result']['trajectory'][-1]
        assert client.get(f'/api/v3/experiments/{left}/result').json() == prior

        opinions = {'opinions': ['0', '1'], 'weights': [['1/2', '1/2'], ['1/4', '3/4']], 'steps': 8}
        other = start(client, 'R123', 'r123-degroot', opinions)['id']
        settle(client, other)
        assert client.post('/api/v3/compare', json={**pair, 'right': other}).status_code == 422


def test_publication_rejects_forged_checkpoint_and_interior_trajectory():
    from copy import deepcopy

    import pytest

    from psychohistory import trajectories
    from psychohistory.state import Snapshot

    config = {'model_id': 'r132-replicator', 'model_version': '1.0.0', 'source_id': 'a' * 64,
              'source': {}, 'parameters': LOGISTIC, 'start': None, 'branch_from': None}
    run = {'config': config, 'code_sha256': 'b' * 64}
    complete = {**trajectories.compute(config), 'input': config, 'code_sha256': 'b' * 64}

    forged = deepcopy(complete)
    state = forged['state']
    state['method'] = 'euler'
    state['completed_steps'] = 1
    snap = forged['snapshot']['payload']
    forged['snapshot'] = Snapshot.create(
        snap['model_id'], snap['model_version'], state, snap['branch'], snap['parent_hash'],
        snap['events'], snap['environment'],
    ).to_dict()
    with pytest.raises(ValueError, match='checkpoint'):
        trajectories.validate_result(run, forged)

    altered = deepcopy(complete)
    altered['trajectory'][1]['values'] = [1, 0]
    altered['trajectory'][1]['exact_values'] = ['1', '0']
    with pytest.raises(ValueError, match='replay'):
        trajectories.validate_result(run, altered, replay=True)
    with pytest.raises(ValueError, match='diagnostics'):
        trajectories.validate_result(run, {**complete, 'diagnostics': {}})


def test_comparison_rejects_distinct_exact_origins_with_equal_plot_values():
    import pytest
    from psychohistory.trajectories import compare, compute

    specs = [
        {**LOGISTIC, 'initial': initial, 'payoff': [['0', '0'], ['0', '0']]}
        for initial in (['1000000000/2000000001', '1000000001/2000000001'],
                        ['1000000001/2000000003', '1000000002/2000000003'])
    ]
    records = []
    for parameters in specs:
        config = {'model_id': 'r132-replicator', 'model_version': '1.0.0', 'source_id': 'a' * 64,
                  'source': {}, 'parameters': parameters, 'start': None, 'branch_from': None}
        records.append({**compute(config), 'input': config})
    assert records[0]['trajectory'][0]['values'] == records[1]['trajectory'][0]['values']
    with pytest.raises(ValueError, match='exact initial state'):
        compare(*records, 'trajectory')
    branches = []
    for record in records:
        checkpoint = {'state': record['state'], 'snapshot_hash': record['snapshot']['content_hash']}
        config = {**record['input'], 'start': checkpoint, 'branch_from': 'a' * 32}
        branches.append({**compute(config), 'input': config})
    assert branches[0]['trajectory'][0]['values'] == branches[1]['trajectory'][0]['values']
    with pytest.raises(ValueError, match='exact initial state'):
        compare(*branches, 'trajectory')


def test_comparison_measures_below_plot_precision_against_exact_decimal_path():
    from psychohistory.trajectories import compare, compute

    parameters = {**LOGISTIC, 'steps': 1, 'step_size': '1/1000000000'}
    records = []
    for method in ('euler', 'rk4'):
        config = {'model_id': 'r132-replicator', 'model_version': '1.0.0', 'source_id': 'a' * 64,
                  'source': {}, 'parameters': {**parameters, 'method': method},
                  'start': None, 'branch_from': None}
        records.append({**compute(config), 'input': config})
    assert records[0]['trajectory'][-1]['values'] == records[1]['trajectory'][-1]['values']
    result = compare(*records, 'trajectory')
    assert 4.68e-20 < result['max_abs_difference'] < 4.70e-20
    assert result['max_abs_difference_decimal'] == '4.6874999996093749995117E-20'
