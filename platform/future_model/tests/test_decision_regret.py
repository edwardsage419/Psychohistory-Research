from dataclasses import replace
from decimal import Decimal

import pytest

from psychohistory.decision_hub import DecisionHub
from psychohistory.decision_registry import Context
from psychohistory.decision_regret import METHODS
from psychohistory.decision_state import DecisionState, Objective, Option, Quantity, Scenario


def method(model_id):
    return next(entry for entry in METHODS if entry.model_id == model_id)


def context(matrix, *, dependence='rectangle', radius=None, reference=None):
    options = [Option(id=key, label=key.upper()) for key in matrix]
    scenarios = []
    for index in range(len(next(iter(matrix.values())))):
        utilities = {}
        for key, row in matrix.items():
            value = row[index]
            if value is None:
                continue
            lower, upper = value if isinstance(value, tuple) else (value, value)
            utilities[key] = Quantity(
                lower=Decimal(str(lower)), upper=Decimal(str(upper)), unit='分',
                kind='synthetic', source='合成测试',
            )
        scenarios.append(Scenario(
            id=f's{index + 1}', label=f'S{index + 1}', utilities=utilities, probability=None,
            source='合成测试', kind='synthetic',
        ))
    state = DecisionState(
        decision_id='0' * 32, revision=1, question='合成方案比较', confirmed=True,
        constraints_confirmed=True, deadline='今年年底', options=options,
        scenarios=scenarios, scenario_basis='同一年度，按同一效用量尺计算，效用越高越好。',
        scenario_dependence=dependence, scenario_dependence_source='合成假设',
        precision_radius=Decimal(radius) if radius is not None else None,
        reference_option_id=reference,
    )
    return Context(state=state, feasible=tuple(options))


def calculate(model_id, ctx):
    entry = method(model_id)
    assert entry.validate(ctx) == []
    return entry.execute(ctx)


def test_point_minimax_and_maximin_can_disagree():
    result = calculate('C029', context({'x': (100, 0), 'y': (55, 40)}, reference='x'))

    assert result['regret'] == {'x': ['0', '40'], 'y': ['45', '0']}
    assert result['leaders'] == ['x']
    assert result['maximin_leaders'] == ['y']
    assert result['scenario_best'] == [['x'], ['y']]
    assert result['worst_scenarios'] == {'x': ['S2'], 'y': ['S1']}
    assert result['reference'] == {'option_id': 'x', 'scenario_gains': ['0', '40']}


def test_point_regret_keeps_coleaders_and_all_worst_worlds():
    result = calculate('C029', context({'a': (5, 1, 1), 'b': (1, 5, 5), 'c': (5, 0, 0)}))

    assert result['leaders'] == ['a', 'b']
    assert result['scenario_best'] == [['a', 'c'], ['b'], ['b']]
    assert result['worst_scenarios']['a'] == ['S2', 'S3']
    assert result['reference'] is None


def test_point_regrets_recompute_when_a_feasible_competitor_is_added():
    initial = calculate('C029', context({'a': (8, 2), 'b': (5, 5)}))
    expanded = calculate('C029', context({'a': (8, 2), 'b': (5, 5), 'c': (2, 8)}))

    assert initial['regret']['a'] == ['0', '3']
    assert expanded['regret']['a'] == ['0', '6']


def test_regret_comparison_uses_only_hard_feasible_options():
    ctx = context({'a': (8, 2), 'b': (5, 5), 'unresolved': (100, 100)})
    ctx = replace(ctx, feasible=ctx.feasible[:-1])

    result = calculate('C029', ctx)

    assert result['scenario_best'] == [['a'], ['b']]
    assert result['regret'] == {'a': ['0', '3'], 'b': ['3', '0']}


@pytest.mark.parametrize('model_id', ['C029', 'C030', 'C031'])
@pytest.mark.parametrize('problem', [
    'missing', 'unknown', 'units', 'inverted', 'unconfirmed', 'scenario_source', 'cell_source', 'horizon',
])
def test_regret_requires_a_complete_comparable_utility_table(model_id, problem):
    ctx = context({'a': (8, 2), 'b': (5, 5)}, radius='0.5')
    utilities = ctx.state.scenarios[0].utilities
    if problem == 'missing':
        del utilities['b']
    elif problem == 'unknown':
        utilities['b'].kind = 'unknown'
    elif problem == 'units':
        utilities['b'].unit = '元'
    elif problem == 'inverted':
        utilities['b'].lower = Decimal(6)
    elif problem == 'unconfirmed':
        ctx.state.scenario_basis = None
    elif problem == 'scenario_source':
        ctx.state.scenarios[0].source = ''
    elif problem == 'cell_source':
        utilities['b'].source = ''
    else:
        utilities['a'].horizon = '今年年底'
        utilities['b'].horizon = '明年年底'

    assert method(model_id).validate(ctx)


def test_point_regret_requires_point_inputs():
    ctx = context({'a': ((7, 9), 2), 'b': (5, 5)})

    assert method('C029').validate(ctx)
    assert method('C031').validate(ctx)


def test_interval_bounds_use_competitors_and_equality_leaves_order_unresolved():
    ctx = context({'a': ((7, 9), (1, 3)), 'b': ((5, 6), (5, 6)), 'c': ((2, 3), (7, 9))})

    result = calculate('C030', ctx)

    assert result['regret_bounds'] == {
        'a': [['0', '0'], ['4', '8']],
        'b': [['1', '4'], ['1', '4']],
        'c': [['4', '7'], ['0', '0']],
    }
    assert result['worst_regret_bounds'] == {'a': ['4', '8'], 'b': ['1', '4'], 'c': ['4', '7']}
    assert result['leaders'] == ['b']
    assert result['strict_leaders'] == []
    assert result['midpoint_leaders'] == ['b']


@pytest.mark.parametrize('dependence', ['unknown', 'constrained'])
def test_interval_dependence_changes_sharpness_claim_and_keeps_conservative_bounds(dependence):
    ctx = context({'a': ((1, 3),), 'b': ((1, 3),)}, dependence=dependence)

    result = calculate('C030', ctx)

    assert result['bound_type'] == 'outer'
    assert result['worst_regret_bounds'] == {'a': ['0', '2'], 'b': ['0', '2']}


def test_interval_singleton_cannot_regret_its_own_utility_range():
    result = calculate('C030', context({'a': ((1, 3),)}))

    assert result['worst_regret_bounds'] == {'a': ['0', '0']}
    assert result['leaders'] == ['a']
    assert result['strict_leaders'] == []


@pytest.mark.parametrize(('radius', 'winner_bounds', 'strict', 'witness'), [
    ('0', ['2.5', '2.5'], ['b'], None),
    ('0.5', ['1.5', '3.5'], ['b'], None),
    ('0.749', ['1.002', '3.998'], ['b'], None),
    ('0.75', ['1', '4'], [], {'a': '7.5', 'b': '4', 'c': '4'}),
    ('0.751', ['0.998', '4.002'], [], {'a': '7.502', 'b': '4.002', 'c': '3.998'}),
    ('1', ['0.5', '4.5'], [], {'a': '8', 'b': '4.5', 'c': '3.5'}),
])
def test_precision_certificate_distinguishes_open_threshold_and_feasible_witness(
    radius, winner_bounds, strict, witness,
):
    ctx = context({'a': (8, 2), 'b': (5.5, 5.5), 'c': (2.5, 8)}, radius=radius)

    result = calculate('C031', ctx)

    assert result['precision_threshold'] == {'option_id': 'b', 'upper_exclusive': '0.75'}
    assert result['worst_regret_bounds']['b'] == winner_bounds
    assert result['leaders'] == ['b']
    assert result['strict_leaders'] == strict
    assert result['sharp_threshold'] is True
    if witness is None:
        assert result['witness'] is None
    else:
        assert result['witness']['worst_regret'] == witness


def test_precision_certificate_recalculates_when_a_center_changes():
    ctx = context({'a': (8, 2), 'b': (5.5, 5.5), 'c': (3.5, 8)}, radius='0.5')

    result = calculate('C031', ctx)

    assert result['precision_threshold']['upper_exclusive'] == '0.5'
    assert result['strict_leaders'] == []
    assert result['sharp_threshold'] is False
    assert result['witness'] is None


def test_precision_certificate_handles_uniformly_dominant_leader():
    result = calculate('C031', context({'a': (10, 20), 'b': (0, 0)}, radius='7.5'))

    assert result['precision_threshold']['upper_exclusive'] == '7.5'
    assert result['worst_regret_bounds'] == {'a': ['0', '5'], 'b': ['5', '35']}
    assert result['strict_leaders'] == []


def test_precision_certificate_does_not_round_high_precision_radius_to_equality():
    ctx = context(
        {'a': (8, 2), 'b': (5.5, 5.5), 'c': (2.5, 8)},
        radius='0.749999999999',
    )

    result = calculate('C031', ctx)

    assert result['strict_leaders'] == ['b']


def test_precision_counterexample_requires_supported_rectangular_dependence():
    ctx = context(
        {'a': (8, 2), 'b': (5.5, 5.5), 'c': (2.5, 8)},
        radius='0.75', dependence='constrained',
    )

    result = calculate('C031', ctx)

    assert result['bound_type'] == 'outer'
    assert result['sharp_threshold'] is False
    assert result['witness'] is None


def test_point_regret_is_unchanged_by_a_common_shift_and_increases_when_a_world_is_added():
    first = calculate('C029', context({'a': (8,), 'b': (5,)}))
    shifted = calculate('C029', context({'a': (-2,), 'b': (-5,)}))
    expanded = calculate('C029', context({'a': (-2, 0), 'b': (-5, 5)}))

    assert first['regret'] == shifted['regret'] == {'a': ['0'], 'b': ['3']}
    assert expanded['worst_regret'] == {'a': '5', 'b': '3'}


def test_interval_regret_collapses_to_point_regret():
    ctx = context({'a': ('-0.1', '0.2'), 'b': ('0.2', '0.1')})

    point = calculate('C029', ctx)
    interval = calculate('C030', ctx)

    assert point['worst_regret'] == {'a': '0.3', 'b': '0.1'}
    assert interval['worst_regret_bounds'] == {'a': ['0.3', '0.3'], 'b': ['0.1', '0.1']}
    assert point['leaders'] == interval['strict_leaders'] == ['b']


def test_decision_hub_replays_the_precision_threshold_and_witness():
    ctx = context({'a': (8, 2), 'b': (5.5, 5.5), 'c': (2.5, 8)}, radius='0.75')
    ctx.state.objectives = [Objective(id='utility', label='情景效用', unit='分', direction='max')]

    analysis = DecisionHub().analyze(ctx.state)

    methods = {entry['model_id']: entry for entry in analysis['methods']}
    assert {methods[model_id]['status'] for model_id in ('C029', 'C030', 'C031')} == {'EXECUTED'}
    precision = methods['C031']['result']
    assert precision['witness']['utilities'] == {'a': ['7.25', '1.25'], 'b': ['4.75', '4.75'], 'c': ['3.25', '8.75']}
    assert precision['charts'][0]['rows'] == [
        {'label': 'A', 'lower': '4.5', 'upper': '7.5'},
        {'label': 'B', 'lower': '1', 'upper': '4'},
        {'label': 'C', 'lower': '4', 'upper': '7'},
    ]
