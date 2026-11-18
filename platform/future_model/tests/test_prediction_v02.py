import copy
import hashlib
import math
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest


def test_exact_trajectory_matches_published_case_and_closed_form():
    from psychohistory.degroot import DeGroot

    plugin = DeGroot()
    state = plugin.initial_state()
    path = plugin.simulate(state, 3)
    assert [s['opinions'] for s in path] == [
        ['0', '1'], ['1/2', '3/4'], ['5/8', '11/16'], ['21/32', '43/64'],
    ]
    assert [s['time'] for s in path] == [0, 1, 2, 3]
    assert plugin.analytic_at(state, 3) == path[-1]
    assert plugin.restore_state(plugin.serialize_state(path[2])) == path[2]
    assert plugin.verify_reference()['stationary_weights'] == ['1/3', '2/3']
    assert plugin.verify_reference()['consensus_limit'] == '2/3'


def test_periodic_swap_and_identity_distinguish_consensus_for_one_input():
    from psychohistory.degroot import DeGroot

    plugin = DeGroot()
    swap = ((0, 1), (1, 0))
    opposed = plugin.initial_state(weights=swap)
    equal = plugin.initial_state(('1/2', '1/2'), swap)
    identity = plugin.initial_state(weights=((1, 0), (0, 1)))
    leader = plugin.initial_state(weights=((1, 0), ('1/2', '1/2')))
    assert plugin.analytic_at(opposed, 5)['opinions'] == ['1', '0']
    assert plugin.consensus(opposed)['limit'] is None
    assert plugin.consensus(equal) == {
        'universal_consensus': False, 'universal_individual_convergence': False,
        'particular_consensus': True, 'limit': ['1/2', '1/2'],
    }
    assert plugin.consensus(identity)['limit'] == ['0', '1']
    assert plugin.consensus(identity)['universal_individual_convergence'] is True
    assert plugin.consensus(leader)['limit'] == ['0', '0']


def test_large_allowed_denominators_remain_exact_at_time_boundary():
    from psychohistory.degroot import DeGroot

    plugin = DeGroot()
    state = plugin.initial_state(
        ('1/4294967291', '1/4294967279'),
        (('1/65521', '65520/65521'), ('65518/65519', '1/65519')),
    )
    trajectory = plugin.simulate(state, 32)
    final = plugin.analytic_at(state, 32)
    low, high = sorted(map(Fraction, state['opinions']))
    assert final == trajectory[-1] == plugin.restore_state(plugin.serialize_state(final))
    assert all(low <= Fraction(value) <= high for value in final['opinions'])
    with pytest.raises(ValueError):
        plugin.advance_state(final)


@pytest.mark.parametrize('weights', [((0.5, 0.5), (1, 0)), ((1, 1), (0, 1)), ((1, 0), ('-1/2', '3/2'))])
def test_rejects_weights_outside_exact_row_stochastic_contract(weights):
    from psychohistory.degroot import DeGroot

    with pytest.raises(ValueError):
        DeGroot().initial_state(weights=weights)


def test_explicit_guards_survive_optimized_python():
    env = {**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1] / 'src')}
    script = """
from psychohistory.degroot import DeGroot
from psychohistory.prediction import protocol_spec, synthetic_rows, validate_split
p = DeGroot()
spec = protocol_spec(7)
rows = synthetic_rows(spec)
rows[0]['available_at'] = spec['split']['cutoff'] + 1
for operation in (
    lambda: p.initial_state(weights=((1, 1), (0, 1))),
    lambda: p.simulate(p.initial_state(), 33),
    lambda: validate_split(rows, spec),
):
    try:
        operation()
    except ValueError:
        continue
    raise SystemExit('invalid input accepted')
"""
    result = subprocess.run([sys.executable, '-O', '-S', '-c', script], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_comparison_provenance_selection_metrics_and_replay():
    from psychohistory.contracts import canonical
    from psychohistory.degroot import DeGroot
    from psychohistory.prediction import protocol_spec, run_comparison, synthetic_rows
    from psychohistory.state import Snapshot

    spec = protocol_spec(7)
    rows = synthetic_rows(spec)
    result = run_comparison(spec)
    assert result == run_comparison(copy.deepcopy(spec))
    assert result['provenance']['protocol_sha256'] == hashlib.sha256(canonical(spec).encode()).hexdigest()
    assert result['provenance']['input_sha256'] == hashlib.sha256(canonical(rows).encode()).hexdigest()
    assert set(result['metrics']) == {'r123-degroot', 'train-prevalence'}
    assert result['scope'] == 'SYNTHETIC_ONLY' and result['evidence']['kind'] == 'UNKNOWN'
    assert result['selection']['split'] == 'validation'
    assert result['selection']['test_used_for_selection'] is False
    assert len(result['study_results']) == 2
    for study in result['study_results']:
        training = [row for row in rows if row['split'] == 'train' and row['study_id'] == study['study_id']]
        assert study['baseline']['prevalence'] == sum(r['outcome'] for r in training) / len(training)
        assert study['split'] == 'test'
    assert len(result['weight_sensitivity']) == 3
    equal, aligned, reversed_signal = [entry['metrics'] for entry in result['weight_sensitivity']]
    assert aligned['r123-degroot']['brier'] < aligned['train-prevalence']['brier']
    assert reversed_signal['r123-degroot']['brier'] > reversed_signal['train-prevalence']['brier']
    assert result['metrics'] == equal
    base = Snapshot.from_dict(result['trajectory']['base'])
    branches = [Snapshot.from_dict(branch) for branch in result['trajectory']['branches']]
    assert len(branches) == 2
    assert all(branch.restore()['parent_hash'] == base.content_hash for branch in branches)
    assert base.restore()['state']['time'] == 0
    model = DeGroot()
    for branch in branches:
        data = branch.restore()
        events = data['events']
        replayed = model.simulate(events[0]['state'], data['state']['time'])
        assert [event['state'] for event in events] == replayed
        assert data['state'] == replayed[-1]
    assert branches[0].restore()['state']['opinions'] != branches[1].restore()['state']['opinions']


@pytest.mark.parametrize('mutate', [
    lambda rows, spec: rows.__setitem__(1, copy.deepcopy(rows[0])),
    lambda rows, spec: rows[0].update(session_id=next(r['session_id'] for r in rows if r['split'] == 'test')),
    lambda rows, spec: rows[0].update(available_at=spec['split']['cutoff'] + 1),
    lambda rows, spec: rows[0].update(target_time=spec['split']['cutoff'] + 1),
    lambda rows, spec: rows[0].update(units='percentage-points'),
    lambda rows, spec: rows[0].update(semantics='continuous-observation'),
    lambda rows, spec: rows[0].update(predictor_outcome=rows[0]['outcome']),
])
def test_split_validation_fails_closed_on_leakage_and_incompatible_rows(mutate):
    from psychohistory.prediction import protocol_spec, synthetic_rows, validate_split

    spec = protocol_spec(7)
    rows = synthetic_rows(spec)
    mutate(rows, spec)
    with pytest.raises(ValueError):
        validate_split(rows, spec)


def test_frozen_protocol_rejects_test_tuning_and_measurement_changes():
    from psychohistory.prediction import protocol_spec, run_comparison

    spec = protocol_spec(7)
    spec['parameters']['selection_split'] = 'test'
    with pytest.raises(ValueError):
        run_comparison(spec)


def test_validation_chooses_horizon_even_when_another_would_win_on_test():
    from psychohistory.prediction import evaluate, protocol_spec, run_comparison, synthetic_rows

    # For seed 1, horizon 3 would score better on test than the validation choice of horizon 1.
    spec = protocol_spec(1)
    rows = synthetic_rows(spec)
    result = run_comparison(spec)
    forecasts = {}
    for row in rows:
        if row['split'] == 'test':
            left, right = map(Fraction, row['opinions'])
            # The first row of the cubed published matrix is (11/32, 21/32).
            forecasts[row['row_id']] = {'kind': 'BERNOULLI', 'probability': float((11 * left + 21 * right) / 32)}
    assert result['selection']['horizon'] == 1
    assert math.isclose(result['metrics']['r123-degroot']['brier'], 0.2596875)
    assert evaluate(rows, forecasts, spec)['metrics']['brier'] < result['metrics']['r123-degroot']['brier']


def test_proper_scoring_boundary_and_unknown_forecasts():
    from psychohistory.prediction import evaluate, protocol_spec, synthetic_rows

    spec = protocol_spec(7)
    rows = synthetic_rows(spec)
    test_rows = [row for row in rows if row['split'] == 'test']
    forecasts = {row['row_id']: {'kind': 'BERNOULLI', 'probability': 1 - row['outcome']} for row in test_rows}
    result = evaluate(rows, forecasts, spec, 'test')
    assert result['metrics']['brier'] == 1
    assert math.isclose(result['metrics']['log_loss'], -math.log(1e-12), abs_tol=1e-12)
    forecasts[test_rows[0]['row_id']] = {'kind': 'UNKNOWN'}
    result = evaluate(rows, forecasts, spec, 'test')
    assert result['metrics'] is None and result['uncertainty']['kind'] == 'UNKNOWN'
    forecasts[test_rows[0]['row_id']]['probability'] = 0.5
    with pytest.raises(ValueError):
        evaluate(rows, forecasts, spec, 'test')


def test_log_loss_is_zero_for_certain_correct_predictions():
    from psychohistory.prediction import evaluate, protocol_spec, synthetic_rows

    spec = protocol_spec(7)
    rows = synthetic_rows(spec)
    forecasts = {r['row_id']: {'kind': 'BERNOULLI', 'probability': r['outcome']} for r in rows if r['split'] == 'test'}
    assert evaluate(rows, forecasts, spec)['metrics'] == {'brier': 0, 'log_loss': 0}


@pytest.mark.parametrize('field,value', [
    ('target', 'actual-human-behavior'), ('units', 'percentage-points'), ('window', [19, 21]),
    ('semantics', 'empirical-training'), ('evidence', 'E2'), ('split', 'validation'),
])
def test_aggregation_rejects_incompatible_constructs_and_evidence_upgrades(field, value):
    from psychohistory.prediction import aggregate, protocol_spec, run_comparison

    studies = run_comparison(protocol_spec(7))['study_results']
    studies[1][field] = value
    with pytest.raises(ValueError):
        aggregate(studies, {study['study_id']: 1 for study in studies})


def test_aggregation_keeps_unknown_and_normalizes_declared_weights():
    from psychohistory.prediction import aggregate, protocol_spec, run_comparison

    studies = run_comparison(protocol_spec(7))['study_results']
    left, right = [study['study_id'] for study in studies]
    combined = aggregate(studies, {left: 2, right: 1})
    brier = [study['metrics']['r123-degroot']['brier'] for study in studies]
    assert math.isclose(combined['metrics']['r123-degroot']['brier'], (2 * brier[0] + brier[1]) / 3)
    assert combined['weights'] == {left: 2 / 3, right: 1 / 3}
    studies[1]['metrics']['r123-degroot'] = None
    combined = aggregate(studies, {left: 2, right: 1})
    assert combined['metrics']['r123-degroot'] is None
    assert combined['evidence']['kind'] == 'UNKNOWN'
