"""Exact two-agent specialization of the DeGroot fixed-weight opinion update."""

import json
import math
import re
from fractions import Fraction

from .contracts import SCHEMA_VERSION, canonical


PUBLISHED_WEIGHTS = (('1/2', '1/2'), ('1/4', '3/4'))
MAX_TIME = 32
_RATIONAL = re.compile(r'(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?')
_REFERENCE_COMMIT = '7ea6eab94433e3669b6f492d802bb35316dc90d6'
_REFERENCE_PATH = 'research/R123/R123_PHASE_A_ORIGINAL_DEGROOT_BERGER_58_TEST_226_MATRIX_CI_ACCEPTANCE.json'
_REFERENCE_SHA256 = 'd4f8a676c9976e11dfb7dc15a13fd3c1798a911b5bb7f12f1d309ea94d41566f'


def source_reference():
    return {
        'research_id': 'R123', 'commit': _REFERENCE_COMMIT, 'path': _REFERENCE_PATH,
        'sha256': _REFERENCE_SHA256, 'doi': '10.1080/01621459.1974.10480137',
        'publication': 'Morris H. DeGroot (1974), Reaching a Consensus, JASA 69(345), 118–121',
        'example_page': 120,
        'scope': 'THEORETICAL',
    }


def _pair(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError('The model requires exactly two agents and a 2×2 weight matrix')
    return value


def _fraction(value):
    if type(value) in (int, Fraction):
        result = Fraction(value)
    elif type(value) is str and len(value) <= 660 and _RATIONAL.fullmatch(value):
        result = Fraction(value)
    else:
        raise ValueError('Expected an exact nonnegative rational')
    if not 0 <= result <= 1:
        raise ValueError('Opinions and weights must lie in [0,1]')
    return result


def _state(opinions, weights, time):
    return {'time': time, 'opinions': [str(x) for x in opinions],
            'weights': [[str(w) for w in row] for row in weights]}


def _validated_values(opinions, weights, time):
    if type(time) is not int or not 0 <= time <= MAX_TIME:
        raise ValueError('Invalid discrete model time')
    values = tuple(_fraction(value) for value in _pair(opinions))
    matrix = tuple(tuple(_fraction(weight) for weight in _pair(row)) for row in _pair(weights))
    if any(sum(row) != 1 or any(weight.denominator >= 2**16 for weight in row) for row in matrix):
        raise ValueError('Rows must sum exactly to 1 with weight denominators below 2**16')
    shared_denominator = math.lcm(*(value.denominator for value in values))
    if shared_denominator.bit_length() > 64 + 32 * time:
        raise ValueError('Opinion denominators exceed the bound for this discrete time')
    return values, matrix


def _state_values(state):
    if not isinstance(state, dict) or set(state) != {'time', 'opinions', 'weights'}:
        raise ValueError('Expected a DeGroot state with time, opinions, and weights')
    opinions, weights = _validated_values(state['opinions'], state['weights'], state['time'])
    if state != _state(opinions, weights, state['time']):
        raise ValueError('State must use canonical rational strings')
    return opinions, weights


def _end_time(time, steps):
    if type(steps) is not int or not 0 <= steps <= MAX_TIME - time:
        raise ValueError(f'Steps must stay within the discrete time range 0–{MAX_TIME}')
    return time + steps


class DeGroot:
    model_id = 'r123-degroot'
    version = '1.0.0'
    capabilities = (
        'describe', 'initial_state', 'validate_input', 'validate_state', 'advance_state', 'simulate',
        'inspect', 'serialize_state', 'restore_state', 'analytic_at', 'consensus', 'verify_reference',
    )

    def describe(self):
        reference = source_reference()
        return {
            'model_id': self.model_id, 'version': self.version, 'capabilities': list(self.capabilities),
            'source': 'BUILTIN_THEORETICAL_R123', 'source_sha256': reference['sha256'],
            'source_reference': reference, 'dependency_identity': 'python-stdlib-fractions',
            'assumptions': ['Two scalar opinions in [0,1]', 'A fixed row-stochastic weight matrix per trajectory',
                            'Simultaneous updates in discrete time'],
            'scale': 'two agents / discrete round', 'input': 'rational opinions and 2×2 weights',
            'output': 'exact rational opinion trajectory', 'permission': 'SYNTHETIC_ONLY',
            'parameters': {'published_weights': [list(row) for row in PUBLISHED_WEIGHTS], 'max_time': MAX_TIME},
            'evidence': 'UNKNOWN',
        }

    def validate_input(self, opinions, weights=PUBLISHED_WEIGHTS):
        _validated_values(opinions, weights, 0)

    def initial_state(self, opinions=('0', '1'), weights=PUBLISHED_WEIGHTS):
        values, matrix = _validated_values(opinions, weights, 0)
        return _state(values, matrix, 0)

    def validate_state(self, state):
        _state_values(state)

    def inspect(self, state):
        self.validate_state(state)
        return json.loads(canonical(state))

    def serialize_state(self, state):
        self.validate_state(state)
        return canonical({'schema_version': SCHEMA_VERSION, 'model_id': self.model_id,
                          'model_version': self.version, 'state': state})

    def restore_state(self, serialized):
        if not isinstance(serialized, str) or len(serialized) > 2000:
            raise ValueError('Expected a bounded DeGroot state envelope')
        payload = json.loads(serialized)
        if (not isinstance(payload, dict)
                or set(payload) != {'schema_version', 'model_id', 'model_version', 'state'}
                or payload['schema_version'] != SCHEMA_VERSION
                or payload['model_id'] != self.model_id or payload['model_version'] != self.version):
            raise ValueError('Incompatible DeGroot state identity')
        return self.inspect(payload['state'])

    def advance_state(self, state):
        opinions, weights = _state_values(state)
        new_time = _end_time(state['time'], 1)
        updated = tuple(sum(weight * opinion for weight, opinion in zip(row, opinions)) for row in weights)
        if not (min(opinions) <= min(updated) <= max(updated) <= max(opinions)):
            raise ArithmeticError('Exact convex-hull invariant failed')
        return _state(updated, weights, new_time)

    def simulate(self, state, steps):
        current = self.inspect(state)
        _end_time(current['time'], steps)
        trajectory = [current]
        for _ in range(steps):
            current = self.advance_state(current)
            trajectory.append(current)
        return trajectory

    def analytic_at(self, state, steps):
        """Use invariant weighted mean and gap recursion, independently of matrix iteration."""
        (left, right), weights = _state_values(state)
        time = _end_time(state['time'], steps)
        toward_right, toward_left = weights[0][1], weights[1][0]
        total = toward_right + toward_left
        if not total:
            return _state((left, right), weights, time)
        mean = (toward_left * left + toward_right * right) / total
        gap = (left - right) * (1 - total) ** steps
        return _state((mean + toward_right * gap / total, mean - toward_left * gap / total), weights, time)

    def consensus(self, state):
        (left, right), weights = _state_values(state)
        toward_right, toward_left = weights[0][1], weights[1][0]
        total = toward_right + toward_left
        convergent = bool(0 < total < 2)
        if convergent:
            mean = (toward_left * left + toward_right * right) / total
            limit = [str(mean), str(mean)]
        elif total == 0 or left == right:
            limit = [str(left), str(right)]
        else:
            limit = None
        return {'universal_consensus': convergent, 'universal_individual_convergence': total != 2,
                'particular_consensus': convergent or left == right, 'limit': limit}

    def verify_reference(self):
        """Check the archived stationary weights and the independent exact finite-time solution."""
        state = self.initial_state()
        opinions, weights = _state_values(state)
        off_diagonal_sum = weights[0][1] + weights[1][0]
        stationary = [weights[1][0] / off_diagonal_sum, weights[0][1] / off_diagonal_sum]
        limit = self.consensus(state)['limit']
        trajectory = self.simulate(state, MAX_TIME)
        if (stationary != [Fraction(1, 3), Fraction(2, 3)] or limit != ['2/3', '2/3']
                or sum(opinion * weight for opinion, weight in zip(opinions, stationary)) != Fraction(2, 3)
                or any(step != self.analytic_at(state, time) for time, step in enumerate(trajectory))):
            raise ArithmeticError('R123 mathematical reference cross-check failed')
        return {'scope': 'THEORETICAL', 'method': 'iterative fractions and independent gap recurrence',
                'stationary_weights': [str(value) for value in stationary], 'consensus_limit': limit[0],
                'checked_through_round': MAX_TIME, 'source_reference': source_reference()}
