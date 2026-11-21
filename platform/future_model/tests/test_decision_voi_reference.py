"""Reference arithmetic separate from the developer's research-card cases."""

from fractions import Fraction
from itertools import combinations, product

from psychohistory.decision_v05 import DecisionHubV05


def evidence(value, high=None):
    return {'lower': value, 'upper': value if high is None else high, 'kind': 'synthetic', 'source': '独立留出构造'}


def setup(rewards, prior, quality, *, allowed=None, cost='0.25'):
    actions = tuple(rewards)
    states = [f's{i}' for i in range(len(prior))]
    signals = [f'z{i}' for i in range(len(quality[0]))]
    scenario_data = [{'id': name, 'label': name, 'kind': 'synthetic', 'source': '独立留出构造',
                      'utilities': {a: {**evidence(row[index]), 'unit': '分'} for a, row in rewards.items()}}
                     for index, name in enumerate(states)]
    information = {
        'signals': [{'id': z, 'label': z} for z in signals],
        'prior': {key: evidence(*value) if isinstance(value, tuple) else evidence(value)
                  for key, value in zip(states, prior, strict=True)},
        'likelihoods': {s: {z: evidence(value) for z, value in zip(signals, row, strict=True)}
                        for s, row in zip(states, quality, strict=True)},
        'cost': {**evidence(cost), 'unit': '分'},
        'unrestricted_actions': allowed is None,
        'action_source': '独立留出构造',
        'actions_by_signal': {z: {'option_ids': ids, 'kind': 'synthetic', 'source': '独立留出构造'}
                              for z, ids in zip(signals, allowed, strict=True)} if allowed is not None else {},
        'parameter_domain': 'rectangle',
        'parameter_domain_source': '各概率行可独立组合',
        'timing_basis': '先收到信号再行动，没有等待损失',
        'fixed_policy': dict(zip(signals, reversed(actions))),
    }
    return {
        'decision_id': 'e' * 32, 'revision': 1, 'question': '如何比较可行动作和调查？', 'confirmed': True,
        'constraints_confirmed': True, 'deadline': '同一天',
        'objectives': [{'id': 'score', 'label': '合成效用', 'unit': '分', 'direction': 'max'}],
        'options': [{'id': a, 'label': a} for a in actions],
        'scenarios': scenario_data, 'scenario_basis': '同一晚上的同尺度效用', 'information': information,
    }


def expectation(policy, prior, quality, rewards):
    return sum(Fraction(prior[s]) * Fraction(quality[s][z]) * Fraction(rewards[policy[z]][s])
               for s, z in product(range(len(prior)), range(len(policy))))


def invoked(state):
    outcome = DecisionHubV05().analyze(state)
    return {item['model_id']: item for item in outcome['methods']}


def test_reference_unpublished_three_state_three_signal_heldout():
    rewards = {'a': (8, 2, 5), 'b': (2, 9, 4), 'c': (1, 3, 9), 'excluded': (200, 200, 200)}
    prior = ('0.2', '0.3', '0.5')
    quality = (('0.1', '0.8', '0.1'), ('0.4', '0.5', '0.1'), ('0.6', '0.3', '0.1'))
    allowed = [['a', 'c', 'excluded'], ['a', 'b', 'c'], ['a', 'b']]
    state = setup(rewards, prior, quality, allowed=allowed)
    state['constraints'] = [{'id': 'gate', 'label': '上限', 'unit': '分', 'operator': '<=', 'threshold': 1, 'source': '独立留出构造'}]
    for option in state['options']:
        option['measurements'] = {'gate': {**evidence(2 if option['id'] == 'excluded' else 1), 'unit': '分'}}

    results = invoked(state)

    viable = ('a', 'b', 'c')
    free = [expectation((a, a, a), prior, quality, rewards) for a in viable]
    rules = list(product(*(tuple(a for a in row if a in viable) for row in allowed)))
    best_after = max(expectation(policy, prior, quality, rewards) for policy in rules)
    point = results['voi_point']['result']
    assert results['voi_point']['status'] == 'EXECUTED'
    assert Fraction(point['baseline_value']) == max(free)
    assert Fraction(point['information_value']) == best_after
    assert Fraction(point['net_value']) == best_after - max(free) - Fraction(1, 4)
    assert point['evsi'] is None
    assert 'excluded' not in point['signals']['z0']['actions']
    assert results['voi_fixed_policy']['status'] == 'INELIGIBLE'


def test_reference_prior_switches_and_full_policy_search_replay():
    gains = {'a': (2, 7), 'b': (8, 1), 'c': (5, 5)}
    quality = (('0.8', '0.2'), ('0.25', '0.75'))
    lower, upper = Fraction('0.2'), Fraction('0.79')
    cost = Fraction('0.25')
    state = setup(gains, (('0.2', '0.79'), ('0.21', '0.8')), quality)
    free_policies = [(a, a) for a in gains]
    all_policies = list(product(gains, repeat=2))

    # Independent one-dimensional method: each full policy is a line, and all
    # possible changes in the upper envelopes lie at pairwise line intersections.
    def line(policy):
        initial = expectation(policy, (0, 1), quality, gains)
        return initial, expectation(policy, (1, 0), quality, gains) - initial

    def switches(family):
        return {(b2 - b1) / (m1 - m2) for (b1, m1), (b2, m2) in combinations(map(line, family), 2) if m1 != m2}

    points = {lower, upper, *(p for p in switches(all_policies) | switches(free_policies) if lower <= p <= upper)}
    advantages = {
        policy: [expectation(policy, (p, 1 - p), quality, gains) - cost
                 - max(expectation(base, (p, 1 - p), quality, gains) for base in free_policies)
                 for p in sorted(points)]
        for policy in all_policies
    }
    oracle = [max(column) for column in zip(*advantages.values(), strict=True)]
    minima = {policy: min(values) for policy, values in advantages.items()}

    results = invoked(state)

    bounds = results['voi_oracle_bounds']['result']['net_bounds']
    assert (Fraction(bounds['lower']), Fraction(bounds['upper'])) == (min(oracle), max(oracle))
    observed = results['voi_maximin']['result']['policies']
    assert {tuple(item['policy'].values()): Fraction(item['minimum_advantage']) for item in observed} == minima
    actual_fixed = results['voi_fixed_policy']['result']['net_bounds']
    assert (Fraction(actual_fixed['lower']), Fraction(actual_fixed['upper'])) == (
        min(advantages[('c', 'b')]), max(advantages[('c', 'b')]),
    )
