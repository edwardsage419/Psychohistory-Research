"""Deterministic trajectory envelopes executed using sealed model source bytes."""

from decimal import Context, Decimal, localcontext
from fractions import Fraction
import json
import math

from .contracts import canonical
from .degroot import DeGroot
from . import replicator
from .state import Snapshot


SCHEMA = 'mechanism-trajectory-1.0.0'
R123 = DeGroot.model_id
R132 = replicator.Replicator.model_id
RESEARCH = {R123: 'R123', R132: 'R132'}
EVIDENCE = {'kind': 'UNKNOWN', 'scope': 'EMPIRICAL',
            'interpretation': 'Empirical predictive and causal validity remain unknown.'}


def normalize(model_id, model_version, parameters):
    if model_id not in RESEARCH or model_version != '1.0.0':
        raise ValueError('Unregistered mechanism model or version')
    if model_id == R132:
        return replicator.normalize_parameters(parameters)
    if not isinstance(parameters, dict) or parameters.keys() != {'opinions', 'weights', 'steps'}:
        raise ValueError('DeGroot requires opinions, weights and steps')
    steps = parameters['steps']
    if type(steps) is not int or not 1 <= steps <= 32:
        raise ValueError('DeGroot steps must be integers from 1 to 32')
    state = DeGroot().initial_state(parameters['opinions'], parameters['weights'])
    return {'opinions': state['opinions'], 'weights': state['weights'], 'steps': steps}


def validate_start(model_id, start):
    if start is None:
        return
    if (not isinstance(start, dict) or start.keys() != {'state', 'snapshot_hash'}
            or not isinstance(start['snapshot_hash'], str) or len(start['snapshot_hash']) != 64
            or any(c not in '0123456789abcdef' for c in start['snapshot_hash'])):
        raise ValueError('Invalid trajectory checkpoint identity')
    if model_id == R123:
        DeGroot().restore_state(canonical(start['state']))
    else:
        replicator.validate_state(start['state'])


def _degroot(parameters, start):
    model = DeGroot()
    if start is None:
        initial = model.initial_state(parameters['opinions'], parameters['weights'])
    else:
        initial = model.restore_state(canonical(start['state']))
        initial['weights'] = parameters['weights']
    path = model.simulate(initial, parameters['steps'])
    if any(state != model.analytic_at(initial, index) for index, state in enumerate(path)):
        raise ArithmeticError('DeGroot trajectory differs from its analytic recurrence')
    return {
        'time_kind': 'discrete-round', 'method': 'weighted-average',
        'trajectory': [{'time': str(s['time']), 'values': s['opinions']} for s in path],
        'diagnostics': {'reference': 'exact gap recurrence', 'max_abs_error': 0,
                        'particular_consensus': model.consensus(initial)},
        'state': json.loads(model.serialize_state(path[-1])),
    }


def compute(config):
    model_id = config['model_id']
    version = config['model_version']
    parameters = normalize(model_id, version, config['parameters'])
    if parameters != config['parameters']:
        raise ValueError('Trajectory parameter identity changed')
    start = config['start']
    validate_start(model_id, start)
    if model_id == R123:
        output = _degroot(parameters, start)
    else:
        output = replicator.run_trajectory(parameters, start['state'] if start else None)
    return {
        **output, 'snapshot': _snapshot(config, output['state'], output['time_kind'],
                                         len(output['trajectory'])), 'schema': SCHEMA,
        'model_id': model_id, 'model_version': version, 'source': config['source'],
        'scope': 'SYNTHETIC_ONLY', 'evidence': EVIDENCE.copy(), 'parameters': parameters,
    }


def _snapshot(config, state, time_kind, samples):
    start = config['start']
    return Snapshot.create(
        config['model_id'], config['model_version'], state, 'continued' if start else 'root',
        start['snapshot_hash'] if start else None,
        [{'kind': 'trajectory-completed', 'samples': samples}],
        {'schema': SCHEMA, 'scope': 'SYNTHETIC_ONLY', 'source_id': config['source_id'],
         'time_kind': time_kind},
    ).to_dict()


def _sample(point, dimensions):
    if not isinstance(point, dict) or point.keys() not in ({'time', 'values'}, {'time', 'values', 'exact_values'}):
        raise ValueError('Trajectory contains an invalid observation')
    if not isinstance(point['time'], str) or len(point['time']) > 60:
        raise ValueError('Trajectory observation time is invalid')
    values = point['values']
    if not isinstance(values, list) or len(values) != dimensions:
        raise ValueError('Trajectory observation dimension is invalid')
    if any(type(x) not in (str, int, float) or len(str(x)) > 4096
           or (isinstance(x, float) and not math.isfinite(x)) for x in values):
        raise ValueError('Trajectory contains invalid state values')
    fractions = [Fraction(str(x)) for x in values]
    if any(not 0 <= x <= 1 for x in fractions):
        raise ValueError('Trajectory escaped its unit interval')
    if 'exact_values' in point:
        scientific = point['exact_values']
        if (not isinstance(scientific, list) or len(scientific) != dimensions
                or any(type(x) is not str or len(x) > 60 for x in scientific)):
            raise ValueError('Trajectory canonical decimals are invalid')
        decoded = [Fraction(x) for x in scientific]
        if any(not 0 <= x <= 1 or abs(x - y) > Fraction('1e-15')
               for x, y in zip(decoded, fractions, strict=True)):
            raise ValueError('Trajectory plot values differ from canonical decimals')
        fractions = decoded
    return Fraction(point['time']), fractions


def validate_result(run, result, *, replay=False):
    config = run['config']
    parameters = config['parameters']
    model_id = config['model_id']
    expected = {
        'schema': SCHEMA, 'model_id': model_id, 'model_version': config['model_version'],
        'source': config['source'], 'scope': 'SYNTHETIC_ONLY', 'evidence': EVIDENCE,
        'input': config, 'code_sha256': run['code_sha256'], 'parameters': parameters,
    }
    if not isinstance(result, dict) or any(result.get(k) != v for k, v in expected.items()):
        raise ValueError('Trajectory artifact identity mismatch')
    start = config['start']
    state = result.get('state')

    if model_id == R123:
        final = DeGroot().restore_state(canonical(state))
        if final['weights'] != parameters['weights']:
            raise ValueError('DeGroot checkpoint has different influence weights')
        time_kind, method, dimensions = 'discrete-round', 'weighted-average', 2
        initial = DeGroot().restore_state(canonical(start['state'])) if start else None
        first_time = Fraction(initial['time']) if initial else Fraction(0)
        first_values = initial['opinions'] if initial else parameters['opinions']
        final_values = final['opinions']
        step = Fraction(1)
    else:
        final = replicator.validate_state(state)
        method = parameters['method']
        time_kind = 'discrete-generation' if method == 'eq3' else 'continuous-ode'
        dimensions = len(parameters['initial'])
        initial = start['state'] if start else None
        first_time = Fraction(initial['time']) if initial else Fraction(0)
        first_values = initial['values'] if initial else parameters['initial']
        final_values = final['values']
        step = Fraction(parameters.get('step_size', '1'))
        completed = initial['completed_steps'] if initial else 0
        if (final['method'] != method or final['time_kind'] != time_kind
                or final['completed_steps'] != completed + parameters['steps']):
            raise ValueError('Replicator checkpoint method, time kind or step count differs')

    if (result.get('time_kind'), result.get('method')) != (time_kind, method):
        raise ValueError('Trajectory method or time semantics mismatch')
    points = result.get('trajectory')
    if not isinstance(points, list) or len(points) != parameters['steps'] + 1:
        raise ValueError('Trajectory sample count mismatch')
    if result.get('snapshot') != _snapshot(config, state, time_kind, len(points)):
        raise ValueError('Trajectory snapshot identity mismatch')
    _validate_diagnostics(model_id, method, result.get('diagnostics'))
    tolerance = Fraction('1e-12') if time_kind == 'continuous-ode' else Fraction(0)
    for index, point in enumerate(points):
        time, values = _sample(point, dimensions)
        if ('exact_values' in point) != (time_kind == 'continuous-ode'):
            raise ValueError('Trajectory is missing canonical values for its time semantics')
        if time != first_time + index * step:
            raise ValueError('Trajectory time grid mismatch')
        if model_id == R132 and abs(sum(values) - 1) > tolerance:
            raise ValueError('Trajectory escaped its probability simplex')
        reference = first_values if index == 0 else final_values if index == len(points) - 1 else None
        if reference is not None and any(abs(x - Fraction(str(y))) > tolerance
                                        for x, y in zip(values, reference, strict=True)):
            raise ValueError('Trajectory state differs from its initial or final checkpoint')
    if Fraction(final['time']) != first_time + parameters['steps'] * step:
        raise ValueError('Final checkpoint time differs from trajectory')
    if replay and result != {**compute(config), 'input': config, 'code_sha256': run['code_sha256']}:
        raise ValueError('Trajectory or diagnostics differ from bounded deterministic replay')


def _validate_diagnostics(model_id, method, diagnostics):
    if not isinstance(diagnostics, dict):
        raise ValueError('Trajectory diagnostics are missing')
    if model_id == R123:
        if (diagnostics.get('reference') != 'exact gap recurrence' or diagnostics.get('max_abs_error') != 0
                or not isinstance(diagnostics.get('particular_consensus'), dict)):
            raise ValueError('DeGroot analytic diagnostics are incomplete')
        return
    if (type(diagnostics.get('max_mass_error')) not in (int, float)
            or not 0 <= diagnostics['max_mass_error'] <= 1e-12
            or not isinstance(diagnostics.get('warnings'), list)):
        raise ValueError('Replicator simplex diagnostics are incomplete')
    if method == 'eq3':
        if (diagnostics.get('arithmetic') != 'exact-fraction' or diagnostics.get('source_equation') != 'Eq3'
                or diagnostics.get('increment_equation') != 'Eq4' or diagnostics['max_mass_error'] != 0):
            raise ValueError('Replicator discrete equation diagnostics differ')
    elif diagnostics.get('numerical_method') != method or diagnostics.get('source_equation') != 'Eq2':
        raise ValueError('Replicator continuous equation diagnostics differ')


def _exact_origin(result):
    start = result['input']['start']
    if result['model_id'] == R132:
        state = start['state'] if start else None
        values = state['values'] if state else result['parameters']['initial']
    else:
        state = start['state']['state'] if start else None
        values = state['opinions'] if state else result['parameters']['opinions']
    return Fraction(state['time'] if state else 0), tuple(Fraction(value) for value in values)


def compare(left, right, metric):
    if metric != 'trajectory':
        raise ValueError('Trajectory mechanisms have no common forecast target; Brier and Log Loss belong to v2')
    dimensions = len(left['trajectory'][0]['values'])
    keys = ('model_id', 'model_version', 'scope', 'time_kind', 'source')
    if any(left[k] != right[k] for k in keys):
        raise ValueError('Models, scientific sources or time semantics are incompatible')
    if left['model_id'] == R132 and left['parameters']['payoff'] != right['parameters']['payoff']:
        raise ValueError('The trajectories have different payoff matrices')
    if left['model_id'] == R123 and left['parameters']['weights'] != right['parameters']['weights']:
        raise ValueError('The trajectories have different influence weights')
    first, second = left['trajectory'], right['trajectory']
    if len(first) != len(second) or _exact_origin(left) != _exact_origin(right):
        raise ValueError('Trajectory comparison requires the same exact initial state and observation times')
    points = []
    maximum = Fraction(0)
    for a, b in zip(first, second, strict=True):
        time_a, values_a = _sample(a, dimensions)
        time_b, values_b = _sample(b, dimensions)
        if time_a != time_b:
            raise ValueError('Trajectory observation grids are incompatible')
        difference = max(abs(x - y) for x, y in zip(values_a, values_b, strict=True))
        maximum = max(maximum, difference)
        points.append({'time': a['time'], 'max_abs_difference': float(difference)})
    with localcontext(Context(prec=42)):
        maximum_decimal = Decimal(maximum.numerator) / Decimal(maximum.denominator)
    return {
        'metric': 'trajectory', 'model_id': left['model_id'], 'time_kind': left['time_kind'],
        'methods': [left['method'], right['method']], 'samples': len(points), 'points': points,
        'max_abs_difference': float(maximum), 'max_abs_difference_decimal': str(maximum_decimal),
        'diagnostics': [left['diagnostics'], right['diagnostics']],
        'scope': 'SYNTHETIC_ONLY',
    }
