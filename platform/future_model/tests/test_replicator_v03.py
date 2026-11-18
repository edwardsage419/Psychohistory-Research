import json
import math
import os
import subprocess
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest


HAWK = [['-2', '2'], ['0', '1']]
STAG = [['4', '0'], ['3', '3']]
LOGISTIC = [['2', '2'], ['1', '1']]
RPS = [['0', '-1', '1'], ['1', '0', '-1'], ['-1', '1', '0']]


def parameters(payoff, initial, method, steps, step_size=None):
    result = dict(payoff=payoff, initial=initial, method=method, steps=steps)
    if step_size is not None:
        result['step_size'] = step_size
    return result


def test_exact_recovery_of_taylor_jonker_equations_and_payoff_baseline():
    from psychohistory.replicator import exact_eq2, exact_eq3, exact_eq4

    initial = ['1/2', '1/2']
    offset = [['1', '5'], ['3', '4']]
    assert exact_eq2(initial, HAWK) == (Fraction('-1/8'), Fraction('1/8'))
    assert exact_eq2(initial, offset) == (Fraction('-1/8'), Fraction('1/8'))
    assert exact_eq3(initial, HAWK) == (Fraction('2/5'), Fraction('3/5'))
    assert exact_eq3(initial, offset) == (Fraction('8/17'), Fraction('9/17'))
    assert exact_eq4(initial, HAWK) == (Fraction('-1/10'), Fraction('1/10'))


def test_original_generations_keep_exact_integer_time_and_zero_support():
    from psychohistory.replicator import run_trajectory

    result = run_trajectory(parameters(RPS, ['1/2', '1/2', '0'], 'eq3', 2))
    assert result['time_kind'] == 'discrete-generation'
    assert result['method'] == 'eq3'
    assert result['trajectory'] == [
        {'time': '0', 'values': ['1/2', '1/2', '0']},
        {'time': '1', 'values': ['1/4', '3/4', '0']},
        {'time': '2', 'values': ['1/16', '15/16', '0']},
    ]
    assert result['diagnostics']['max_mass_error'] == 0


@pytest.mark.parametrize('payoff,initial', [
    (HAWK, ['1', '0']),
    ([['0', '0'], ['-2', '-2']], ['1', '0']),
    ([['-1', '-1'], ['-1', '-1']], ['1/2', '1/2']),
])
def test_original_generation_checks_all_multipliers_and_positive_denominator(payoff, initial):
    from psychohistory.replicator import exact_eq3, exact_eq4

    for equation in (exact_eq3, exact_eq4):
        with pytest.raises(ValueError, match='multipliers|denominator'):
            equation(initial, payoff)


@pytest.mark.parametrize('updates', [
    {'initial': ['0.25', '3/4']}, {'initial': ['01/4', '3/4']},
    {'initial': ['1/3', '3/4']}, {'initial': ['-1/4', '5/4']},
    {'initial': [0.25, '3/4']}, {'initial': ['1/4', '1/4', '1/4', '1/4']},
    {'payoff': [['2', '2'], ['1']]}, {'payoff': [['65', '2'], ['1', '1']]},
    {'method': 'latest'}, {'steps': True}, {'steps': 4097}, {'steps': 0},
    {'step_size': '0'}, {'step_size': '2'}, {'step_size': '1/0'},
    {'steps': 401, 'step_size': '1/20'}, {'surprise': 1},
])
def test_strict_rational_and_bounded_parameters(updates):
    from psychohistory.replicator import normalize_parameters

    candidate = parameters(LOGISTIC, ['1/4', '3/4'], 'rk4', 40, '1/40')
    with pytest.raises(ValueError):
        normalize_parameters(candidate | updates)


def test_normalization_reduces_fractions_and_separates_clocks():
    from psychohistory.replicator import normalize_parameters

    original = parameters(LOGISTIC, ['2/8', '6/8'], 'rk4', 40, '2/80')
    normalized = normalize_parameters(original)
    assert normalized['initial'] == ['1/4', '3/4']
    assert normalized['step_size'] == '1/40'
    assert original['initial'] == ['2/8', '6/8']
    with pytest.raises(ValueError):
        normalize_parameters(original | {'method': 'eq3', 'steps': 2})


@pytest.mark.parametrize('payoff,initial,time,expected', [
    (LOGISTIC, ['1/4', '3/4'], 2, 0.7112345942275939),
    (STAG, ['4/5', '1/5'], 4, 0.974581599604),
    (STAG, ['1/4', '3/4'], 4, 0.000003280588),
    (HAWK, ['1/2', '1/2'], 4, 0.343202279538),
    (HAWK, ['1/4', '3/4'], 4, 0.326657175596),
])
def test_rk4_and_separated_variable_analytic_solution_match_archived_endpoints(payoff, initial, time, expected):
    from psychohistory.replicator import run_trajectory

    result = run_trajectory(parameters(payoff, initial, 'rk4', time * 120, '1/120'))
    assert result['time_kind'] == 'continuous-ode'
    assert result['trajectory'][-1]['time'] == str(time)
    assert math.isclose(result['trajectory'][-1]['values'][0], expected, abs_tol=1e-8)
    analytic = result['diagnostics']['analytic_reference']
    assert analytic['kind'] == 'ANALYTIC'
    assert math.isclose(analytic['final_first_share'], expected, abs_tol=1e-11)
    assert analytic['absolute_error'] < 1e-8


def test_rps_reports_distinct_invariant_drift_for_euler_and_rk4():
    from psychohistory.replicator import run_trajectory

    initial = ['1/2', '3/10', '1/5']
    euler = run_trajectory(parameters(RPS, initial, 'euler', 40, '3/10'))
    rk4 = run_trajectory(parameters(RPS, initial, 'rk4', 40, '3/10'))
    invariant_key = 'product_invariant'
    for result in (euler, rk4):
        assert result['diagnostics'][invariant_key]['theoretical_initial'] == 0.03
        assert result['diagnostics']['max_mass_error'] < 1e-12
    assert math.isclose(euler['diagnostics'][invariant_key]['final_drift'], -0.010113456173247867, abs_tol=1e-12)
    assert math.isclose(rk4['diagnostics'][invariant_key]['final_drift'], 1.0209743605410493e-7, abs_tol=1e-12)


def test_euler_large_step_exposes_false_extinction_without_clipping():
    from psychohistory.replicator import run_trajectory

    report = run_trajectory(parameters(HAWK, ['1/2', '1/2'], 'euler', 1, '4'))
    assert report['trajectory'][-1] == {'time': '4', 'values': [0, 1]}
    reference = report['diagnostics']['analytic_reference']
    assert math.isclose(reference['final_first_share'], 0.343202279538, abs_tol=1e-12)
    warnings = report['diagnostics']['warnings']
    assert any(item['code'] == 'FALSE_EXTINCTION' and item['time'] == '4' for item in warnings)
    with pytest.raises(ValueError, match='simplex'):
        run_trajectory(parameters(STAG, ['1/2', '1/2'], 'euler', 1, '4'))


def test_positive_shares_below_binary_float_range_remain_visible():
    from psychohistory.replicator import run_trajectory

    spec = parameters([['0', '0'], ['64', '64']], ['1/2', '1/2'], 'euler', 3200, '1/160')
    report = run_trajectory(spec)
    value = report['trajectory'][-1]['values'][0]
    assert value == report['state']['values'][0]
    assert 0 < Decimal(value) < Decimal('1e-400')
    reference = report['diagnostics']['analytic_reference']
    assert 0 < Decimal(reference['final_first_share']) < Decimal('1e-400')
    assert Decimal(reference['absolute_error']) > 0
    assert not report['diagnostics']['warnings']


def test_continuous_replay_is_independent_of_caller_decimal_context():
    from psychohistory.replicator import run_trajectory

    spec = parameters(HAWK, ['1/3', '2/3'], 'rk4', 10, '2/11')
    expected = run_trajectory(spec)
    with localcontext() as context:
        context.prec = 10
        assert run_trajectory(spec) == expected


@pytest.mark.parametrize('method,step_size', [('eq3', None), ('rk4', '1/40'), ('euler', '1/40')])
def test_serialize_restore_has_identical_continuation_and_independent_branches(method, step_size):
    from psychohistory.replicator import Replicator, run_trajectory

    plugin = Replicator()
    spec = parameters(LOGISTIC, ['1/4', '3/4'], method, 2, step_size)
    intervention = parameters(STAG, ['1/4', '3/4'], method, 2, step_size)
    first = run_trajectory(spec)
    restored = plugin.restore_state(plugin.serialize_state(first['state']))
    resumed = run_trajectory(spec, start=restored)
    unbroken = run_trajectory(spec | {'steps': 4})
    assert resumed['state'] == unbroken['state']
    assert resumed['trajectory'] == unbroken['trajectory'][2:]
    different = run_trajectory(intervention, start=restored)
    assert different['trajectory'][0] == resumed['trajectory'][0]
    assert different['state']['values'] != resumed['state']['values']
    assert restored == first['state']


def test_continuous_branch_can_change_solver_and_grid_without_resetting_time():
    from psychohistory.replicator import run_trajectory

    initial = ['1/4', '3/4']
    root = run_trajectory(parameters(LOGISTIC, initial, 'euler', 2, '1/10'))
    branch = run_trajectory(parameters(LOGISTIC, initial, 'rk4', 2, '1/7'), start=root['state'])
    assert branch['trajectory'][0] == root['trajectory'][-1]
    assert [point['time'] for point in branch['trajectory']] == ['1/5', '12/35', '17/35']
    assert branch['state']['method'] == 'rk4'
    assert branch['state']['completed_steps'] == 4


def test_resume_rejects_clock_changes_and_version_or_simplex_corruption():
    from psychohistory.replicator import Replicator, run_trajectory

    initial = ['1/4', '3/4']
    discrete = run_trajectory(parameters(LOGISTIC, initial, 'eq3', 2))['state']
    continuous = parameters(LOGISTIC, initial, 'rk4', 2, '1/40')
    with pytest.raises(ValueError, match='time kind'):
        run_trajectory(continuous, start=discrete)
    plugin = Replicator()
    for mutation in (
        {'model_version': '99.0.0'}, {'values': ['1', '1']}, {'time': '1/2'}, {'completed_steps': 20}
    ):
        with pytest.raises(ValueError):
            plugin.restore_state(json.dumps(discrete | mutation))


def test_independent_archived_checks_are_explicit_and_executable():
    from psychohistory.replicator import verify_archived_cases

    checks = verify_archived_cases()
    assert checks['exact']['phase_a_cases'] == 84
    assert checks['exact']['phase_b_cases'] == 75
    assert checks['exact']['phase_b_valid_discrete_cases'] == 69
    assert checks['analytic']['cases'] == 216
    assert checks['analytic']['max_absolute_error'] < 1e-6
    assert checks['euler_false_extinction']['numeric_share'] == 0
    assert [grid['steps'] for grid in checks['rps_drift']] == [40, 80, 160, 320]
    assert 0 < checks['rps_drift'][-1]['rk4'] < 1e-10


def test_optimized_python_guards_are_executed_with_no_site_packages():
    env = {**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1] / 'src')}
    script = """
from psychohistory.replicator import exact_eq3, run_trajectory
spec = dict(initial=['1/2', '1/2'], payoff=[['-2', '2'], ['0', '1']], method='euler', steps=1, step_size='4')
if run_trajectory(spec)['diagnostics']['warnings'][0]['code'] != 'FALSE_EXTINCTION':
    raise SystemExit('False extinction was hidden')
try:
    exact_eq3(['1', '0'], spec['payoff'])
except ValueError:
    pass
else:
    raise SystemExit('Invalid reproduction rule was accepted')
"""
    run = subprocess.run([sys.executable, '-O', '-S', '-c', script], env=env, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
