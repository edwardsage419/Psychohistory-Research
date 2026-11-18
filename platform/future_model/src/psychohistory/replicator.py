"""Bounded Taylor–Jonker replicator equations and numerical trajectories."""

import json
import math
import re
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction

from .contracts import SCHEMA_VERSION, canonical


MODEL_ID = 'r132-replicator'
MODEL_VERSION = '1.0.0'
TIME_KINDS = {'eq3': 'discrete-generation', 'euler': 'continuous-ode', 'rk4': 'continuous-ode'}
MAX_STEPS = 4096
MAX_GENERATIONS = 8
MAX_GENERATIONS_TOTAL = 32
MAX_TIME = 20
MAX_PAYOFF = 64
MAX_STEP_SIZE = {'euler': Fraction(4), 'rk4': Fraction(1, 2)}
_PARAMETER_BITS = 31
_EXACT_BITS = 4096
_TIME_BITS = 96
_NUMERIC_CONTEXT = Context(prec=42, rounding=ROUND_HALF_EVEN, Emin=-9999, Emax=9999)
_MASS_TOLERANCE = Decimal('1e-32')
_FRACTION = re.compile(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?')
_DECIMAL = re.compile(r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:E[+-][1-9][0-9]{0,4})?')
_STATE_FIELDS = {'schema_version', 'model_id', 'model_version', 'time_kind', 'method',
                 'time', 'values', 'completed_steps'}

_HAWK = (('-2', '2'), ('0', '1'))
_STAG = (('4', '0'), ('3', '3'))
_LOGISTIC = (('2', '2'), ('1', '1'))
_RPS = (('0', '-1', '1'), ('1', '0', '-1'), ('-1', '1', '0'))
_ARCHIVE_GAMES = (_HAWK, _STAG, _LOGISTIC)
_REFERENCE_COMMIT = 'dd05f32f79efc2f4f4f37117cc039dca1008ed76'
_ARCHIVE_RECEIPTS = (
    ('A', 'R132_PHASE_A_70_TEST_84_EXACT_STATES_RPS_ARTIFACT_CI_ACCEPTANCE.json',
     'a779b3e219147d5664bd41ed0278833e0034773ccead892e1b7edbb8c0123ac1'),
    ('B', 'R132_PHASE_B_70_TEST_216_TRAJECTORIES_CI_ACCEPTANCE.json',
     '4401f9426307ce3ea1763e009166edabd1db1722718c849337bc62478b97ca54'),
)


def source_reference():
    return {'research_id': 'R132', 'commit': _REFERENCE_COMMIT, 'doi': '10.1016/0025-5564(78)90077-9',
            'publication': 'Taylor and Jonker (1978), Evolutionarily Stable Strategies and Game Dynamics',
            'printed_pages': [149, 150, 151], 'scope': 'THEORETICAL',
            'receipts': [{'phase': phase, 'path': f'research/R132/{file}', 'sha256': digest}
                         for phase, file, digest in _ARCHIVE_RECEIPTS]}


def _rational(value, bits=_PARAMETER_BITS):
    max_text = 2 * (bits * 30103 // 100000 + 1) + 2
    if type(value) is not str or len(value) > max_text or not _FRACTION.fullmatch(value):
        raise ValueError('Expected a bounded rational string')
    number = Fraction(value)
    if max(number.numerator.bit_length(), number.denominator.bit_length()) > bits:
        raise ValueError('Rational exceeds the arithmetic budget')
    return number


def _game(initial, payoff):
    if type(initial) not in (tuple, list) or len(initial) not in (2, 3):
        raise ValueError('Two or three strategies are required')
    size = len(initial)
    if (type(payoff) not in (tuple, list) or len(payoff) != size
            or any(type(row) not in (tuple, list) or len(row) != size for row in payoff)):
        raise ValueError('Payoff must be a square matrix matching the strategy count')
    shares = tuple(_rational(value) for value in initial)
    matrix = tuple(tuple(_rational(value) for value in row) for row in payoff)
    if any(value < 0 for value in shares) or sum(shares) != 1:
        raise ValueError('Initial shares must lie on the exact simplex')
    if any(abs(value) > MAX_PAYOFF for row in matrix for value in row):
        raise ValueError(f'Absolute payoffs must be at most {MAX_PAYOFF}')
    return shares, matrix


def normalize_parameters(parameters):
    """Validate the released model budget and return canonical rational inputs."""
    if not isinstance(parameters, dict) or type(parameters.get('method')) is not str:
        raise ValueError('A supported trajectory method is required')
    method = parameters['method']
    if method not in TIME_KINDS:
        raise ValueError('Trajectory method must be eq3, euler, or rk4')
    fields = {'initial', 'payoff', 'method', 'steps'}
    if parameters.keys() != (fields if method == 'eq3' else fields | {'step_size'}):
        raise ValueError('Trajectory parameters differ from the method schema')
    steps = parameters['steps']
    maximum = MAX_GENERATIONS if method == 'eq3' else MAX_STEPS
    if type(steps) is not int or not 1 <= steps <= maximum:
        raise ValueError(f'Steps must be an integer from 1 through {maximum} for {method}')
    initial, payoff = _game(parameters['initial'], parameters['payoff'])
    result = {'initial': [str(value) for value in initial],
              'payoff': [[str(value) for value in row] for row in payoff], 'method': method, 'steps': steps}
    if method != 'eq3':
        size = _rational(parameters['step_size'])
        if not 0 < size <= MAX_STEP_SIZE[method] or steps * size > MAX_TIME:
            raise ValueError('Step size or continuous time exceeds the method budget')
        result['step_size'] = str(size)
    return result


def _payoffs(shares, matrix):
    return tuple(sum(a * b for a, b in zip(row, shares)) for row in matrix)


def _field(shares, matrix):
    payoffs = _payoffs(shares, matrix)
    mean = sum(p * f for p, f in zip(shares, payoffs))
    return tuple(p * (f - mean) for p, f in zip(shares, payoffs))


def _check_reproduction(multipliers, denominator):
    if any(m < 0 for m in multipliers) or denominator <= 0:
        raise ValueError('Original Eq3/Eq4 requires nonnegative birth multipliers and a positive denominator')


def _generation(shares, matrix):
    multipliers = tuple(1 + payoff for payoff in _payoffs(shares, matrix))
    weighted = tuple(p * rate for p, rate in zip(shares, multipliers))
    denominator = sum(weighted)
    _check_reproduction(multipliers, denominator)
    return tuple(value / denominator for value in weighted)


def _increment(shares, matrix):
    payoffs = _payoffs(shares, matrix)
    mean = sum(p * f for p, f in zip(shares, payoffs))
    _check_reproduction((1 + f for f in payoffs), 1 + mean)
    return tuple(p * (f - mean) / (1 + mean) for p, f in zip(shares, payoffs))


def exact_eq2(initial, payoff):
    """Original continuous field on rational inputs, returned as Fractions."""
    return _field(*_game(initial, payoff))


def exact_eq3(initial, payoff):
    """Original discrete reproduction map on rational inputs."""
    return _generation(*_game(initial, payoff))


def exact_eq4(initial, payoff):
    """Original discrete increment, evaluated directly from Eq4."""
    return _increment(*_game(initial, payoff))


def _decimal(number):
    return Decimal(number.numerator) / Decimal(number.denominator)


def _decimal_text(value):
    return str(value.normalize()) if value else '0'


def _reported_number(value):
    converted = float(value or 0)
    return _decimal_text(value) if not converted and value else converted


def _exact_bounds(values):
    if (any(value < 0 for value in values) or sum(values) != 1
            or any(value.denominator.bit_length() > _EXACT_BITS for value in values)):
        raise ValueError('Exact generation is outside the simplex or arithmetic budget')


def _numeric_bounds(values):
    if (any(not value.is_finite() or not 0 <= value <= 1 for value in values)
            or abs(sum(values) - 1) > _MASS_TOLERANCE):
        raise ValueError('Numerical integration left the simplex; reduce the step size')


def _state_values(state):
    if not isinstance(state, dict) or state.keys() != _STATE_FIELDS:
        raise ValueError('Expected a versioned replicator state envelope')
    if (state['schema_version'] != SCHEMA_VERSION or state['model_id'] != MODEL_ID
            or state['model_version'] != MODEL_VERSION):
        raise ValueError('Incompatible replicator state identity')
    method = state['method']
    if type(method) is not str or method not in TIME_KINDS or state['time_kind'] != TIME_KINDS[method]:
        raise ValueError('Invalid method or time kind for replicator state')
    time = _rational(state['time'], _TIME_BITS)
    steps = state['completed_steps']
    if (str(time) != state['time'] or type(steps) is not int or time < 0
            or steps < 0 or (steps == 0) != (time == 0)):
        raise ValueError('Invalid replicator state time or step count')
    values = state['values']
    if type(values) is not list or len(values) not in (2, 3):
        raise ValueError('Invalid replicator state strategy count')
    if method == 'eq3':
        if time != steps or steps > MAX_GENERATIONS_TOTAL:
            raise ValueError('Discrete state time must match its generation count')
        shares = tuple(_rational(value, _EXACT_BITS) for value in values)
        _exact_bounds(shares)
        if [str(value) for value in shares] != values:
            raise ValueError('Discrete state must use canonical rational strings')
    else:
        if steps > MAX_STEPS or time > MAX_TIME or time > steps * MAX_STEP_SIZE['euler']:
            raise ValueError('Continuous state exceeds its time or step budget')
        if any(type(value) is not str or len(value) > 60 or not _DECIMAL.fullmatch(value) for value in values):
            raise ValueError('Continuous state must use bounded decimal strings')
        shares = tuple(Decimal(value) for value in values)
        _numeric_bounds(shares)
        if [_decimal_text(value) for value in shares] != values:
            raise ValueError('Continuous state must use canonical decimal strings')
    return time, shares, steps


def validate_state(state):
    """Check a saved model state without running the model."""
    with localcontext(_NUMERIC_CONTEXT):
        _state_values(state)
    return state


def _make_state(shares, time, method, steps):
    values = [str(value) if method == 'eq3' else _decimal_text(value) for value in shares]
    return {'schema_version': SCHEMA_VERSION, 'model_id': MODEL_ID, 'model_version': MODEL_VERSION,
            'method': method, 'time_kind': TIME_KINDS[method], 'time': str(time),
            'values': values, 'completed_steps': steps}


def _numeric_step(shares, matrix, step, method):
    def advance(field, size):
        point = tuple(value + size * drift for value, drift in zip(shares, field))
        _numeric_bounds(point)
        return point

    first = _field(shares, matrix)
    if method == 'euler':
        return advance(first, step)
    second = _field(advance(first, step / 2), matrix)
    third = _field(advance(second, step / 2), matrix)
    fourth = _field(advance(third, step), matrix)
    average = tuple((a + 2 * b + 2 * c + d) / 6 for a, b, c, d in zip(first, second, third, fourth))
    return advance(average, step)


def _scalar_coefficients(matrix):
    (a, b), (c, d) = matrix
    return (a - c) - (b - d), b - d


def _analytic_share(matrix, initial, elapsed):
    """Solve the two-strategy reference by logit or inversion of the separated integral."""
    slope, intercept = _scalar_coefficients(matrix)
    if elapsed == 0 or initial in (0, 1) or (not slope and not intercept):
        return initial, 'fixed-state'
    b = _decimal(intercept)
    time = _decimal(elapsed)
    if not slope:
        return 1 / (1 + (1 - initial) / initial * (-b * time).exp()), 'closed-form logistic'

    a = _decimal(slope)
    root = _decimal(-intercept / slope)
    direction = a * (initial - root)
    if not direction:
        return initial, 'fixed-state'
    # The logarithmic primitive has these singular coefficients in degenerate games.
    if not intercept or not slope + intercept:
        return None, 'The bounded analytic reference excludes degenerate endpoint coefficients'
    boundary = root if (initial < root < 1 if direction > 0 else 0 < root < initial) else Decimal(direction > 0)
    end_coefficient = _decimal(slope + intercept)

    def primitive(value):
        return (value.ln() / b - (1 - value).ln() / end_coefficient
                - a * abs(a * (value - root)).ln() / (b * end_coefficient))

    target = primitive(initial) + time
    inside, outside = initial, boundary
    for _ in range(112):
        middle = (inside + outside) / 2
        if middle in (inside, outside):
            break
        if primitive(middle) < target:
            inside = middle
        else:
            outside = middle
    return (inside + outside) / 2, 'separated-variable integral'


def _is_rps_invariant(matrix):
    return (len(matrix) == 3 and all(sum(column) == 0 for column in zip(*matrix))
            and all(matrix[i][j] == -matrix[j][i] for i in range(3) for j in range(3)))


def _trajectory_report(states, first_time, step, method, matrix):
    exact = method == 'eq3'
    path = [{'time': str(first_time + index * step),
             'values': [str(value) if exact else _reported_number(value) for value in shares]}
            for index, shares in enumerate(states)]
    if not exact:
        for point, shares in zip(path, states, strict=True):
            point['exact_values'] = [_decimal_text(value) for value in shares]
    diagnostics = {'max_mass_error': float(max(abs(sum(shares) - 1) for shares in states)), 'warnings': []}
    if exact:
        diagnostics.update(arithmetic='exact-fraction', source_equation='Eq3', increment_equation='Eq4')
        return path, diagnostics
    diagnostics.update(arithmetic='decimal42', source_equation='Eq2', numerical_method=method)
    for index, (before, after) in enumerate(zip(states, states[1:]), start=1):
        vanished = [i for i, (left, right) in enumerate(zip(before, after)) if left > 0 and right == 0]
        if vanished:
            diagnostics['warnings'].append({
                'code': 'FALSE_EXTINCTION', 'time': path[index]['time'], 'strategies': vanished,
                'message': 'The numerical step reached zero from positive support. The finite-time continuous model preserves that support.',
            })
    if len(matrix) == 2:
        analytic, reference_method = _analytic_share(matrix, states[0][0], step * (len(states) - 1))
        if analytic is None:
            diagnostics['analytic_reference'] = {'kind': 'UNKNOWN', 'reason': reference_method}
        else:
            diagnostics['analytic_reference'] = {'kind': 'ANALYTIC', 'method': reference_method,
                                                 'final_first_share': _reported_number(analytic),
                                                 'absolute_error': _reported_number(abs(states[-1][0] - analytic))}
    if _is_rps_invariant(matrix) and all(value > 0 for value in states[0]):
        product = math.prod(states[0])
        drift = [math.prod(shares) - product for shares in states]
        diagnostics['product_invariant'] = {'kind': 'EXACT_CONTINUOUS_INVARIANT',
                                             'theoretical_initial': _reported_number(product),
                                             'final_drift': _reported_number(drift[-1]),
                                             'max_absolute_drift': _reported_number(max(map(abs, drift)))}
    return path, diagnostics


def run_trajectory(parameters, start=None):
    """Run one bounded segment. A restored segment may change payoffs or its continuous solver."""
    spec = normalize_parameters(parameters)
    initial, matrix = _game(spec['initial'], spec['payoff'])
    method, steps = spec['method'], spec['steps']
    exact = method == 'eq3'
    step = Fraction(1) if exact else Fraction(spec['step_size'])
    with localcontext(_NUMERIC_CONTEXT):
        if start is None:
            first_time, previous_steps = Fraction(0), 0
            shares = initial if exact else tuple(_decimal(value) for value in initial)
        else:
            first_time, shares, previous_steps = _state_values(start)
            if start['time_kind'] != TIME_KINDS[method] or len(shares) != len(initial):
                raise ValueError('Restored state must retain its time kind and strategy count')
        end_time = first_time + steps * step
        total_steps = previous_steps + steps
        limit = MAX_GENERATIONS_TOTAL if exact else MAX_STEPS
        if (total_steps > limit or (not exact and end_time > MAX_TIME)
                or max(end_time.numerator.bit_length(), end_time.denominator.bit_length()) > _TIME_BITS):
            raise ValueError('Restored trajectory exceeds the cumulative time or step budget')
        states = [shares]
        if exact:
            for _ in range(steps):
                shares = _generation(shares, matrix)
                _exact_bounds(shares)
                states.append(shares)
        else:
            numeric_matrix = tuple(tuple(_decimal(value) for value in row) for row in matrix)
            numeric_step = _decimal(step)
            for _ in range(steps):
                shares = _numeric_step(shares, numeric_matrix, numeric_step, method)
                states.append(shares)
        trajectory, diagnostics = _trajectory_report(states, first_time, step, method, matrix)
        final = _make_state(shares, end_time, method, total_steps)
    return {'time_kind': TIME_KINDS[method], 'method': method, 'trajectory': trajectory, 'state': final,
            'diagnostics': diagnostics, 'scope': 'THEORETICAL', 'evidence': {'kind': 'UNKNOWN', 'scope': 'EMPIRICAL'}}


def _pairwise_field(shares, matrix):
    return tuple(
        weight * sum(other_weight * sum((a - b) * p for a, b, p in zip(row, other_row, shares))
                     for other_weight, other_row in zip(shares, matrix))
        for weight, row in zip(shares, matrix)
    )


def _check_exact_grid():
    cyclic = (('-1/2', '1', '-1'), ('-1', '-1/2', '1'), ('1', '-1', '-1/2'))
    alpha = (('2', '1', '5'), ('5', '1', '0'), ('1', '4', '3'))
    count_a = shifts = scales = rps_checks = 0
    points = [(Fraction(i, 6), Fraction(j, 6), Fraction(6 - i - j, 6))
              for i in range(7) for j in range(7 - i)]
    for payoff in (cyclic, alpha, _RPS):
        _, matrix = _game(('1', '0', '0'), payoff)
        for shares in points:
            field = _field(shares, matrix)
            expected = _pairwise_field(shares, matrix)
            generation = _generation(shares, matrix)
            increments = _increment(shares, matrix)
            if (field != expected or sum(field) != 0
                    or generation != tuple(value + delta for value, delta in zip(shares, increments))
                    or any(p == 0 and (v != 0 or x != 0) for p, v, x in zip(shares, field, generation))):
                raise ArithmeticError('R132 Phase A exact equations disagree')
            for offset in (-1, 0, 2):
                moved = tuple(tuple(value + offset for value in row) for row in matrix)
                if _field(shares, moved) != field:
                    raise ArithmeticError('Continuous Eq2 changed under a common payoff offset')
                shifts += 1
            for factor in (Fraction(1, 2), 2, 3):
                scaled = tuple(tuple(value * factor for value in row) for row in matrix)
                if _field(shares, scaled) != tuple(value * factor for value in field):
                    raise ArithmeticError('Continuous Eq2 failed positive time rescaling')
                scales += 1
            if payoff == _RPS and all(shares):
                if sum(drift / share for drift, share in zip(field, shares)) != 0:
                    raise ArithmeticError('The RPS log-product derivative must vanish')
                rps_checks += 1
            count_a += 1

    count_b = valid_discrete_b = 0
    for payoff in _ARCHIVE_GAMES:
        _, matrix = _game(('1', '0'), payoff)
        slope, offset = _scalar_coefficients(matrix)
        for index in range(25):
            left = Fraction(index, 24)
            shares = (left, 1 - left)
            scalar = left * (1 - left) * (slope * left + offset)
            if _field(shares, matrix) != (scalar, -scalar):
                raise ArithmeticError('R132 Phase B exact field differs from algebraic two-strategy reduction')
            count_b += 1
            birth_rates = [1 + left * a + (1 - left) * b for a, b in matrix]
            if min(birth_rates) < 0 or sum(x * rate for x, rate in zip(shares, birth_rates)) <= 0:
                continue
            if _generation(shares, matrix) != tuple(x + delta for x, delta in zip(shares, _increment(shares, matrix))):
                raise ArithmeticError('R132 Phase B original Eq3 differs from Eq4')
            valid_discrete_b += 1
    if (count_a, shifts, scales, rps_checks, count_b, valid_discrete_b) != (84, 252, 252, 10, 75, 69):
        raise ArithmeticError('R132 archived exact checking grid differs')
    return {'phase_a_cases': count_a, 'phase_a_shift_checks': shifts, 'phase_a_scale_checks': scales,
            'phase_a_rps_log_product_checks': rps_checks, 'phase_b_cases': count_b,
            'phase_b_valid_discrete_cases': valid_discrete_b}


def _check_analytic_grid():
    initials = ('1/10', '1/4', '2/5', '3/5', '4/5', '9/10')
    endpoints = tuple(Fraction(t) for t in ('1/4', '1/2', 1, 2, 3, 4, 5, 6, 8, 10, 12, 16))
    frozen_samples = {(_HAWK, '1/4', 4): Decimal('0.326657175596'),
                      (_STAG, '4/5', 4): Decimal('0.974581599604'),
                      (_LOGISTIC, '1/4', 2): Decimal('0.7112345942275939')}
    count = 0
    worst = Decimal(0)
    with localcontext(_NUMERIC_CONTEXT):
        step = Decimal(1) / 120
        for payoff in _ARCHIVE_GAMES:
            _, matrix = _game(('1', '0'), payoff)
            numeric_matrix = tuple(tuple(_decimal(value) for value in row) for row in matrix)
            for sample in initials:
                start = _decimal(Fraction(sample))
                shares = (start, 1 - start)
                position = 0
                for endpoint in endpoints:
                    goal = int(endpoint * 120)
                    for _ in range(goal - position):
                        shares = _numeric_step(shares, numeric_matrix, step, 'rk4')
                    position = goal
                    analytic, _ = _analytic_share(matrix, start, endpoint)
                    error = abs(shares[0] - analytic)
                    worst = max(worst, error)
                    archived = frozen_samples.get((payoff, sample, endpoint))
                    if archived is not None and abs(analytic - archived) > Decimal('1e-11'):
                        raise ArithmeticError('R132 analytic endpoint differs from the frozen reference')
                    count += 1
    if count != 216 or worst >= Decimal('1e-6'):
        raise ArithmeticError('R132 archived continuous trajectory comparison failed')
    return {'cases': count, 'max_absolute_error': float(worst), 'archived_tolerance': 1e-6}


def verify_archived_cases():
    """Independently check the bounded R132 grids and numerical artifacts in CI."""
    exact = _check_exact_grid()
    analytic = _check_analytic_grid()
    hawk = {'initial': ['1/2', '1/2'], 'payoff': _HAWK, 'steps': 1}
    original = run_trajectory({**hawk, 'method': 'eq3'})
    euler = run_trajectory({**hawk, 'method': 'euler', 'step_size': '4'})
    euler_share = euler['trajectory'][-1]['values'][0]
    analytic_share = euler['diagnostics']['analytic_reference']['final_first_share']
    shifted = [['1', '5'], ['3', '4']]
    shifted_share = exact_eq3(hawk['initial'], shifted)[0]
    if (original['state']['values'][0] != '2/5' or shifted_share != Fraction(8, 17)
            or exact_eq2(hawk['initial'], hawk['payoff']) != exact_eq2(hawk['initial'], shifted) or euler_share != 0
            or abs(analytic_share - 0.343202279538) > 1e-11
            or not any(warning['code'] == 'FALSE_EXTINCTION' for warning in euler['diagnostics']['warnings'])):
        raise ArithmeticError('R132 archived Hawk–Dove false-extinction check failed')
    rps_drifts = []
    for steps, euler_expected, rk4_expected in (
        (40, -0.010113456173247867, 1.0209743605410493e-7),
        (80, -0.004351948133490012, 4.184748152169515e-9),
        (160, -0.0019804898633752656, 1.9291522199149647e-10),
        (320, -0.0009416188628425283, 9.913899562397077e-12),
    ):
        rps = {'initial': ['1/2', '3/10', '1/5'], 'payoff': _RPS,
               'steps': steps, 'step_size': str(Fraction(12, steps))}
        scores = {method: run_trajectory({**rps, 'method': method})['diagnostics']['product_invariant']['final_drift']
                  for method in ('euler', 'rk4')}
        if abs(scores['euler'] - euler_expected) > 1e-12 or abs(scores['rk4'] - rk4_expected) > 1e-12:
            raise ArithmeticError('R132 archived RPS numerical drift check failed')
        rps_drifts.append({'steps': steps, **scores})
    return {'scope': 'THEORETICAL', 'source_reference': source_reference(), 'exact': exact, 'analytic': analytic,
            'euler_false_extinction': {'numeric_share': euler_share, 'analytic_share': analytic_share,
                                       'original_eq3_share': original['state']['values'][0],
                                       'shifted_eq3_share': str(shifted_share)},
            'rps_drift': rps_drifts}


class Replicator:
    model_id, version = MODEL_ID, MODEL_VERSION
    capabilities = ('describe', 'validate_input', 'simulate', 'advance_state', 'validate_state',
                    'inspect', 'serialize_state', 'restore_state')

    def describe(self):
        return {'model_id': self.model_id, 'version': self.version, 'capabilities': list(self.capabilities),
                'source': 'BUILTIN_THEORETICAL_R132', 'source_sha256': _ARCHIVE_RECEIPTS[-1][2],
                'source_reference': source_reference(), 'dependency_identity': 'python-stdlib-fraction-decimal',
                'scale': 'two or three strategy shares, continuous time or discrete generations',
                'assumptions': ['Fixed payoff matrix within a trajectory segment', 'Random matching',
                                'No mutation or migration'],
                'input': 'rational simplex shares, payoff matrix, and chosen time mechanism',
                'output': 'theoretical trajectory, state, and numerical diagnostics',
                'parameters': {'time_kinds': TIME_KINDS.copy(), 'max_time': MAX_TIME, 'max_steps': MAX_STEPS,
                               'max_generations': MAX_GENERATIONS, 'max_payoff': MAX_PAYOFF},
                'permission': 'SYNTHETIC_ONLY', 'evidence': 'UNKNOWN'}

    def validate_input(self, parameters):
        return normalize_parameters(parameters)

    def simulate(self, parameters, start=None):
        return run_trajectory(parameters, start)

    def advance_state(self, parameters, start=None):
        spec = normalize_parameters(parameters)
        return run_trajectory({**spec, 'steps': 1}, start)['state']

    def validate_state(self, state):
        return validate_state(state)

    def inspect(self, state):
        return json.loads(self.serialize_state(state))

    def serialize_state(self, state):
        return canonical(validate_state(state))

    def restore_state(self, serialized):
        if type(serialized) is not str or len(serialized) > 8000:
            raise ValueError('Expected a bounded serialized replicator state')
        return validate_state(json.loads(serialized))
