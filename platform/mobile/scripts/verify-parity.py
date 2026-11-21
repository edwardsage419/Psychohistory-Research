#!/usr/bin/env python3
"""Compare the same synthetic v0.5 contract on the fixed Python and JS engines."""
import argparse
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys

MOBILE = Path(__file__).resolve().parents[1]
PLATFORM = MOBILE.parent / 'future_model'
sys.path[:0] = [str(PLATFORM / 'src'), str(PLATFORM / 'tests')]

from psychohistory.decision_state import Constraint, Objective, Quantity
from psychohistory.decision_v05 import DecisionHubV05, DecisionStateV05
import test_decision_regret as regret
import test_decision_scoring as scoring
import test_decision_timing as timing
import test_decision_voi as voi

GATE = 'c028_interval_feasibility'
OBJECTIVE = Objective(id='utility', label='长期效用', unit='分', direction='max')


def approved(context):
    raw = context.state.model_dump(mode='json')
    if not raw['objectives']:
        raw['objectives'] = [OBJECTIVE.model_dump(mode='json')]
    return DecisionStateV05.model_validate({**raw, 'confirmed': True, 'constraints_confirmed': True})


def cases():
    yield 'point-regret', approved(regret.context({'x': (100, 0), 'y': (55, 40)}, reference='x', radius='1')), ['C029', 'C031']
    yield 'precision-sharp-equality', approved(regret.context({
        'a': (8, 2), 'b': ('5.5', '5.5'), 'c': ('2.5', 8),
    }, radius='.75')), ['C031']
    yield 'interval-regret', approved(regret.context({'a': ((7, 9), 2), 'b': (5, 5)})), ['C030']
    yield 'interval-dependence-unknown', approved(regret.context({'a': ((7, 9), 2), 'b': (5, 5)}, dependence='constrained')), ['C030']
    yield 'weighted-threshold', approved(scoring.context(weights={
        'growth': scoring.bounds('.3', '.7'), 'resources': scoring.bounds('.3', '.7'),
    })), ['comparability', 'pareto', 'weight_sensitivity', 'c034_joint_robustness']
    yield 'joint-score-intervals', approved(scoring.context(
        a=[scoring.score('.73', '.88'), scoring.score('.45', '.61')],
        b=[scoring.score('.40', '.54'), scoring.score('.72', '.9')],
    )), ['pareto', 'c034_joint_robustness']
    state = approved(scoring.context())
    state.constraints = [Constraint(id='limit', label='最低限度', unit='元', operator='>', threshold='1.000000000001', source='合成')]
    state.options[0].measurements = {'limit': Quantity(lower='1.000000000001', upper='1.000000000001', unit='元', kind='synthetic', source='合成')}
    state.options[1].measurements = {'limit': Quantity(lower='2', upper='2', unit='错误单位', kind='synthetic', source='合成')}
    yield 'strict-hard-gate-and-units', state, [GATE, 'pareto']
    for name, cost in [('positive', '0.5'), ('equal-cost', '0.9'), ('cost-reversal', '0.95')]:
        yield f'evsi-{name}', approved(voi.fixture(cost=cost)), ['voi_point']
    zero = voi.fixture(s=('1', '1'), t=('0', '0'))
    zero.state.information.unrestricted_actions = False
    zero.state.information.actions_by_signal = {'yes': voi.action_set('a', 'b')}
    yield 'zero-signal', approved(zero), ['voi_point']
    unavailable = voi.fixture()
    unavailable.state.information.unrestricted_actions = False
    unavailable.state.information.actions_by_signal = {'yes': voi.action_set('a')}
    yield 'positive-signal-no-action', approved(unavailable), ['voi_point']
    unknown = voi.fixture()
    unknown.state.information.prior['good'].source = ''
    yield 'probability-no-source', approved(unknown), ['voi_point']
    for name, at, inclusive in [('inclusive', '.5', True), ('strict', '.5', False), ('near', '.499999999999', True)]:
        state = approved(timing.ctx({'wait_duration': timing.timed('.5')}, rules={'b': {'cutoff': timing.cutoff(at, inclusive)}}))
        yield f'time-{name}', state, ['timing_actions']
    for name, early_good, early_bad in [('early-good', '.8', '.2'), ('late-good', '.2', '.8'), ('independent', '.5', '.5')]:
        completion = {scenario: [{'duration': '0', 'probability': share}, {
            'duration': '.5', 'probability': str(1 - Decimal(share)),
        }] for scenario, share in [('good', early_good), ('bad', early_bad)]}
        state = approved(timing.ctx(investigate=timing.investigation('conditional', completion_by_state=completion),
                                    information=timing.info(), rules={'b': {'cutoff': timing.cutoff('.3', False)}}))
        yield f'duration-{name}', state, ['timing_investigation']
    for name, duration, cost in [('delay-threshold', '.25', '.5'), ('delay-value-tie', '.5', '.45')]:
        payload = timing.investigation('deterministic', duration=timing.timed(duration)) | {'cost': timing.timed(cost)}
        yield name, approved(timing.ctx(investigate=payload, information=timing.info())), ['timing_investigation']
    investigation = timing.investigation('deterministic', duration=timing.timed('.3'))
    state = approved(timing.ctx(investigate=investigation, information=timing.info(), rules={'b': {'cutoff': timing.cutoff('.3', False)}}))
    yield 'strict-survey-opportunity', state, ['timing_investigation']
    no_exit = approved(timing.ctx({'decision_deadline': timing.cutoff('.3', False)},
                                  investigate=timing.investigation('joint', joint=timing.direct_rows(('.5', '1')))))
    yield 'duration-joint-no-exit', no_exit, ['timing_investigation']
    zero_late = approved(timing.ctx({'decision_deadline': timing.cutoff('.3', False)},
                                    investigate=timing.investigation('joint', joint=timing.direct_rows(('0', '1'), ('.5', '0')))))
    yield 'duration-joint-zero-late', zero_late, ['timing_investigation']
    expired = approved(timing.ctx(rules={'a': {'cutoff': timing.cutoff('0', False)}}))
    yield 'expired-current-scope', expired, ['timing_actions', 'C029']


FIELDS = {
    GATE: ('feasibility',),
    'comparability': ('status', 'score_gaps'),
    'pareto': ('status', 'pairs', 'frontier'),
    'weight_sensitivity': ('pairs',),
    'c034_joint_robustness': ('pairs',),
    'C029': ('leaders', 'worst_regret', 'regret', 'maximin_leaders', 'reference'),
    'C030': ('leaders', 'regret_bounds', 'worst_regret_bounds', 'strict_leaders', 'midpoint_leaders', 'bound_type'),
    'C031': ('leaders', 'precision_threshold', 'strict_leaders', 'sharp_threshold', 'witness', 'regret_bounds', 'worst_regret_bounds'),
    'voi_point': ('baseline_value', 'information_value', 'evsi', 'evpi', 'net_value', 'decision', 'signals', 'evidence_status', 'baseline_actions', 'break_even_cost', 'gross_advantage'),
    'timing_actions': ('strategies', 'leaders', 'probabilities_used'),
    'timing_investigation': ('status', 'immediate_value', 'investigation_value', 'net_value', 'duration_probabilities',
                             'scenario_probabilities', 'probability_provenance', 'immediate_availability',
                             'threshold', 'policy', 'late_mass_sensitivity', 'immediate_leaders'),
}


def receipt(name, state, method_ids):
    desktop = DecisionHubV05().analyze(state)
    expect = {}
    for row in desktop['methods']:
        model_id = row['model_id']
        if model_id in method_ids:
            result = row['result']
            expect[model_id] = {'status': row['status'], 'result': {
                key: result[key] for key in FIELDS[model_id]
            } if result is not None else None}
    return dict(name=name, state=state.model_dump(mode='json'), input_hash=desktop['input_hash'],
                temporal_scope=desktop['temporal_scope'], expect=expect)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--print-cases', action='store_true', help='emit the shared inputs and expected Python fields')
    args = parser.parse_args()
    payload = json.dumps([receipt(*case) for case in cases()], ensure_ascii=False)
    if args.print_cases:
        print(payload)
    else:
        subprocess.run(['node', 'scripts/verify-parity.mjs'], cwd=MOBILE, input=payload, text=True, check=True)


if __name__ == '__main__':
    main()
