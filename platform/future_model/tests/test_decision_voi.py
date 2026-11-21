from decimal import Decimal

import pytest

from psychohistory.decision_registry import Context
from psychohistory.decision_state import Option, Quantity, Scenario
from psychohistory.decision_v05 import DecisionStateV05
from psychohistory.decision_voi import InformationInput, METHODS, Probability, Signal, SignalActions
from psychohistory import decision_voi_math


def probability(lower, upper=None, *, kind='synthetic', source='人工模型'):
    return dict(lower=lower, upper=lower if upper is None else upper, kind=kind, source=source)


def quantity(value, *, unit='分', kind='synthetic', source='人工模型'):
    return Quantity(lower=value, upper=value, unit=unit, kind=kind, source=source)


def fixture(*, p=('0.5', '0.5'), s=('0.9', '0.9'), t=('0.7', '0.7'), cost='0.5', verified=False):
    options = [Option(id='a', label='A'), Option(id='b', label='B')]
    kind = 'fact' if verified else 'synthetic'
    scenarios = [
        Scenario(id='good', label='有利', kind=kind, source='人工模型',
                 utilities={'a': quantity(6, kind=kind), 'b': quantity(10, kind=kind)}),
        Scenario(id='bad', label='不利', kind=kind, source='人工模型',
                 utilities={'a': quantity(6, kind=kind), 'b': quantity(0, kind=kind)}),
    ]
    def comp(value):
        return str(1 - Decimal(value))

    info = InformationInput(
        signals=[dict(id='yes', label='正'), dict(id='no', label='负')],
        prior={'good': probability(*p, kind=kind), 'bad': probability(comp(p[1]), comp(p[0]), kind=kind)},
        likelihoods={
            'good': {'yes': probability(*s, kind=kind), 'no': probability(comp(s[1]), comp(s[0]), kind=kind)},
            'bad': {'yes': probability(comp(t[1]), comp(t[0]), kind=kind), 'no': probability(*t, kind=kind)},
        },
        cost=quantity(cost, kind=kind), unrestricted_actions=True, action_source='可行性依据',
        timing_basis='立即完成且无等待损失', parameter_domain='rectangle', parameter_domain_source='区间行可独立组合',
        fixed_policy={'yes': 'b', 'no': 'a'},
    )
    state = DecisionStateV05(decision_id='1' * 32, revision=1, question='模拟调查', deadline='同日',
                             options=options, scenarios=scenarios, scenario_basis='同一日期与基数效用标尺', information=info)
    return Context(state, tuple(options))


def method(model_id):
    return next(x for x in METHODS if x.model_id == model_id)


def run(model_id, ctx):
    value = method(model_id)
    assert value.validate(ctx) == []
    return value.execute(ctx)


def test_point_asymmetric_signal_cost_and_threshold():
    result = run('voi_point', fixture())
    assert {key: result[key] for key in ('baseline_value', 'information_value', 'evsi', 'evpi', 'net_value', 'decision')} == {
        'baseline_value': '6', 'information_value': '6.9', 'evsi': '0.9', 'evpi': '2', 'net_value': '0.4', 'decision': 'POSITIVE',
    }
    assert result['baseline_actions'] == ['a']
    assert {key: item['actions'] for key, item in result['signals'].items()} == {'yes': ['b'], 'no': ['a']}
    assert result['break_even_cost'] == {'lower': '0.9', 'upper': '0.9', 'unit': '分'}
    assert result['evidence_status'] == 'SYNTHETIC'
    assert run('voi_point', fixture(cost='0.9'))['decision'] == 'TIE'


@pytest.mark.parametrize(('q', 'expected'), [('0.5', '0'), ('0.6', '0'), ('0.8', '1'), ('1', '2')])
def test_symmetric_signal_value_at_card_boundaries(q, expected):
    result = run('voi_point', fixture(s=(q, q), t=(q, q)))
    assert result['evsi'] == expected
    if q == '0.6':
        assert result['signals']['yes']['actions'] == ['a', 'b']


def test_reversed_signal_is_usable_and_label_invariant():
    reversed_signal = run('voi_point', fixture(s=('0.1', '0.1'), t=('0.2', '0.2')))
    relabeled = run('voi_point', fixture(s=('0.9', '0.9'), t=('0.8', '0.8')))
    assert reversed_signal['evsi'] == relabeled['evsi'] == '1.2'
    assert reversed_signal['signals']['no']['actions'] == relabeled['signals']['yes']['actions'] == ['b']


def test_zero_event_requires_no_policy_or_posterior():
    ctx = fixture(s=('1', '1'), t=('0', '0'))
    info = ctx.state.information
    info.unrestricted_actions = False
    info.actions_by_signal = {'yes': action_set('a', 'b')}
    result = run('voi_point', ctx)
    assert result['evsi'] == '0'
    assert result['signals']['no']['probability'] == '0'
    assert result['signals']['no']['actions'] == []
    assert result['signals']['no']['posterior'] is None


def action_set(*option_ids):
    return SignalActions(option_ids=list(option_ids), kind='synthetic', source='可行性依据')


def test_investigation_restrictions_can_cost_free_baseline_actions():
    ctx = fixture(p=('0.8', '0.8'))
    info = ctx.state.information
    info.unrestricted_actions = False
    info.actions_by_signal = {'yes': action_set('a'), 'no': action_set('a')}
    result = run('voi_point', ctx)
    assert result['baseline_actions'] == ['b']
    assert result['evsi'] is None
    assert result['net_value'] == '-2.5'
    assert result['decision'] == 'NEGATIVE'


@pytest.mark.parametrize('error', ['source', 'likelihood_sum', 'prior_sum', 'utility', 'cost_unit', 'unknown_timing', 'missing_actions'])
def test_point_gate_reports_incomplete_or_inconsistent_inputs(error):
    ctx = fixture()
    info = ctx.state.information
    if error == 'source':
        info.prior['good'].source = ''
    elif error == 'likelihood_sum':
        info.likelihoods['good']['yes'].lower = info.likelihoods['good']['yes'].upper = Decimal(0)
    elif error == 'prior_sum':
        info.prior['bad'].lower = info.prior['bad'].upper = Decimal(0)
    elif error == 'utility':
        del ctx.state.scenarios[0].utilities['b']
    elif error == 'cost_unit':
        info.cost.unit = '元'
    elif error == 'unknown_timing':
        info.timing_basis = None
    else:
        info.unrestricted_actions = False
    assert method('voi_point').validate(ctx)


def test_oracle_bounds_include_interior_baseline_switch():
    result = run('voi_oracle_bounds', fixture(p=('0.4', '0.7')))
    assert result['net_bounds'] == {'lower': '-0.14', 'upper': '0.94'}
    assert result['break_even_cost'] == {'lower': '0.36', 'upper': '1.44', 'unit': '分'}
    assert result['decision'] == 'CONDITIONAL'
    assert result['extrema']['upper']['prior']['good'] == '0.6'


def test_oracle_zero_at_interior_uninformative_joint_mass():
    ctx = fixture(s=('0.1', '0.9'), t=('0.4', '0.4'))
    result = run('voi_oracle_bounds', ctx)
    assert result['net_bounds']['lower'] == '-0.5'


def test_fixed_policy_joint_bounds_and_strict_cost_equality():
    ctx = fixture(p=('0.5', '0.7'), s=('0.85', '0.95'), t=('0.65', '0.75'))
    result = run('voi_fixed_policy', ctx)
    assert result['net_bounds']['lower'] == '0.15'
    assert result['worst_against_baseline'] == {'a': '0.15', 'b': '0.25'}
    assert result['decision'] == 'POSITIVE'
    ctx.state.information.cost = quantity('0.65')
    equal = run('voi_fixed_policy', ctx)
    assert equal['net_bounds']['lower'] == '0'
    assert equal['decision'] == 'CONDITIONAL'


def test_deterministic_maximin_and_randomized_certificate_scopes():
    ctx = fixture(p=('0.5', '0.7'), s=('0.85', '0.95'), t=('0.65', '0.75'))
    result = run('voi_maximin', ctx)
    policies = {tuple(policy['policy'].values()): policy['minimum_advantage'] for policy in result['policies']}
    assert policies == {('a', 'a'): '-1.5', ('a', 'b'): '-2.71', ('b', 'a'): '0.15', ('b', 'b'): '-1.5'}
    assert result['optimal_policies'] == [{'yes': 'b', 'no': 'a'}]
    certificate = run('voi_randomized_certificate', ctx)
    assert certificate['certificate_status'] == 'CERTIFIED'
    assert certificate['net_bounds'] == {'lower': '0.15', 'upper': '0.15'}
    assert certificate['unique_policy'] is True
    assert certificate['witness']['prior']['good'] == '0.5'


def test_randomized_certificate_preserves_ties_at_a_matching_witness():
    ctx = fixture(s=('0.1', '0.9'), t=('0.1', '0.9'), cost='0')
    ctx.state.scenarios[0].utilities['a'] = quantity(10)
    ctx.state.scenarios[1].utilities['a'] = quantity(0)
    ctx.state.scenarios[0].utilities['b'] = quantity(0)
    ctx.state.scenarios[1].utilities['b'] = quantity(10)
    # Constant free policies both reach zero. A corner where the likelihood rows coincide
    # bounds every randomized policy by zero, but all signal actions are tied there.
    certificate = run('voi_randomized_certificate', ctx)
    assert certificate['certificate_status'] == 'CERTIFIED'
    assert certificate['unique_policy'] is False


def test_randomized_optimum_remains_unknown_when_witness_bounds_do_not_match():
    ctx = fixture(p=('0.1', '0.9'), s=('1', '1'), t=('0', '0'), cost='0')
    ctx.state.scenarios[0].utilities = {'a': quantity(1), 'b': quantity(0)}
    ctx.state.scenarios[1].utilities = {'a': quantity(0), 'b': quantity(1)}

    adaptive = run('voi_oracle_bounds', ctx)
    deterministic = run('voi_maximin', ctx)
    randomized = run('voi_randomized_certificate', ctx)

    assert adaptive['net_bounds'] == {'lower': '0', 'upper': '0'}
    assert deterministic['net_bounds'] == {'lower': '-0.8', 'upper': '-0.8'}
    assert randomized['net_bounds'] == {'lower': '-0.8', 'upper': '0'}
    assert randomized['certificate_status'] == 'UNKNOWN'
    assert randomized['unique_policy'] is None


def test_reported_evidence_needs_an_explicit_receipt_for_verified_points():
    ctx = fixture(verified=True)
    assert run('voi_point', ctx)['evidence_status'] == 'CONDITIONAL'
    ctx.state.information.verification_source = '用户复核凭据'
    assert run('voi_point', ctx)['evidence_status'] == 'VERIFIED'
    ctx.state.information.cost.kind = 'assumption'
    assert run('voi_point', ctx)['evidence_status'] == 'CONDITIONAL'


def test_ineligible_options_are_never_used_even_when_listed_for_a_signal():
    ctx = fixture()
    ctx = Context(ctx.state, ctx.feasible[:1])
    ctx.state.information.unrestricted_actions = False
    ctx.state.information.actions_by_signal = {'yes': action_set('a', 'b'), 'no': action_set('a')}
    result = run('voi_point', ctx)
    assert result['baseline_actions'] == result['signals']['yes']['actions'] == ['a']
    assert result['net_value'] == '-0.5'
    assert method('voi_fixed_policy').validate(ctx)


def test_invalid_fixed_mapping_does_not_disable_independent_methods():
    ctx = fixture()
    ctx.state.information.fixed_policy = {'yes': 'not_an_option', 'no': 'a'}

    assert method('voi_fixed_policy').validate(ctx)
    assert run('voi_point', ctx)['evsi'] == '0.9'
    assert run('voi_maximin', ctx)['optimal_policies'] == [{'yes': 'b', 'no': 'a'}]


def test_large_uncertainty_is_refused_before_building_dense_equations(monkeypatch):
    state = fixture().state
    types = tuple(str(i) for i in range(12))
    state.options = [Option(id=key, label=key) for key in types]
    state.scenarios = [Scenario(id=key, label=key, kind='synthetic', source='人工容量案例',
                                utilities={a: quantity(int(a) + int(key)) for a in types}) for key in types]
    state.information.signals = [Signal(id=key, label=key) for key in types]
    state.information.fixed_policy = {key: '0' for key in types}
    free_probability = Probability(**probability(0, 1))
    state.information.prior = dict.fromkeys(types, free_probability)
    state.information.likelihoods = {key: dict.fromkeys(types, free_probability) for key in types}

    def no_dense_equations(_):
        pytest.fail('oversized input reached dense equation construction')

    monkeypatch.setattr(decision_voi_math, '_constraints', no_dense_equations)
    ctx = Context(state, tuple(state.options))
    assert method('voi_oracle_bounds').validate(ctx)
    assert method('voi_fixed_policy').validate(ctx)


@pytest.mark.parametrize('domain', ['unknown', 'constrained'])
def test_joint_uncertainty_requires_an_evidenced_domain(domain):
    ctx = fixture(p=('0.5', '0.7'))
    ctx.state.information.parameter_domain = domain
    assert method('voi_oracle_bounds').validate(ctx)
    assert method('voi_fixed_policy').validate(ctx)
