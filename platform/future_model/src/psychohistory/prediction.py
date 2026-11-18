"""Frozen synthetic Bernoulli comparison protocol and proper scoring rules."""

import hashlib
import math
from collections import Counter
from fractions import Fraction

from .contracts import canonical
from .degroot import PUBLISHED_WEIGHTS, DeGroot, source_reference
from .state import Snapshot


PROTOCOL_VERSION = 'synthetic-degroot-comparison-1.0.0'
DATASET_VERSION = 'synthetic-two-study-sessions-1.0.0'
CANDIDATE = DeGroot.model_id
BASELINE = 'train-prevalence'
METRICS = ('brier', 'log_loss')
TARGET = 'simulated-agent-event'
UNITS = 'binary-indicator'
SEMANTICS = 'synthetic-bernoulli-event-per-session-trial'
SCOPE = 'SYNTHETIC_ONLY'
_STUDIES = (('aligned-signal', 'Aligned signal'), ('weak-reversed-signal', 'Weak reversed signal'))
_PARTITIONS = (('train', 8, 4), ('validation', 4, 12), ('test', 8, 20))
_TRIALS_PER_SESSION = 6
_CUTOFF = 19
_EPSILON = 1e-12
_SCORE_BOUNDS = {'brier': 1, 'log_loss': -math.log(_EPSILON)}
_WEIGHT_SCENARIOS = (('Equal study weights', 1, 1), ('Emphasize aligned signal', 4, 1),
                     ('Emphasize weak reversed signal', 1, 4))
_ROW_FIELDS = frozenset({
    'row_id', 'study_id', 'session_id', 'split', 'target', 'units', 'semantics', 'target_time',
    'feature_time', 'observed_at', 'available_at', 'opinions', 'outcome', 'scope',
})


def _sha256(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _scientific_evidence():
    return {'kind': 'UNKNOWN', 'scope': 'EMPIRICAL', 'interpretation': 'Empirical predictive validity remains unknown.'}


def protocol_spec(seed: int, candidate: str = CANDIDATE) -> dict:
    """Return a fresh JSON copy of the sole registered profile for the seed."""
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError('Seed must be an integer in [0, 2**32)')
    if candidate != CANDIDATE:
        raise ValueError('Unregistered prediction candidate')
    split = {
        'group_unit': 'session', 'cutoff': _CUTOFF, 'time_unit': 'discrete-round',
        'labels': 'Train and validation labels precede cutoff; test labels follow cutoff.',
        'feature_lags': {'feature_time': 3, 'observed_at': 2, 'available_at': 1},
    }
    for partition, sessions, target_time in _PARTITIONS:
        split[partition] = {
            'target_window': [target_time, target_time],
            'session_groups': [f'{study_id}:{partition}:{index:02}'
                               for study_id, _ in _STUDIES for index in range(1, sessions + 1)],
        }
    return {
        'protocol_version': PROTOCOL_VERSION, 'dataset_version': DATASET_VERSION, 'seed': seed,
        'scope': SCOPE, 'candidate': CANDIDATE, 'model_version': DeGroot.version,
        'dataset': {'kind': 'BUILTIN_SYNTHETIC', 'draws': 'SHA-256 keyed by version, seed, session, and trial',
                    'studies': [{'study_id': study_id, 'label': label} for study_id, label in _STUDIES]},
        'baseline': {'model_id': BASELINE, 'fit_split': 'train', 'method': 'within-study training prevalence'},
        'split': split,
        'target': {'name': TARGET, 'units': UNITS, 'semantics': SEMANTICS, 'distribution': 'BERNOULLI',
                   'positive_outcome': 1, 'negative_outcome': 0, 'forecast_units': 'probability'},
        'metrics': {'brier': {'lower_is_better': True, 'formula': 'mean((p - y)^2)'},
                    'log_loss': {'lower_is_better': True, 'log_base': 'e', 'epsilon': _EPSILON,
                                 'formula': 'mean(-ln(max(epsilon, probability assigned to the outcome)))'}},
        'parameters': {
            'weights': [list(row) for row in PUBLISHED_WEIGHTS], 'forecast_agent': 0,
            'horizons': [1, 2, 3], 'selection_split': 'validation', 'selection_metric': 'brier',
            'horizon_unit': 'opinion-update round', 'selection_weighting': 'equal study',
            'tie_break': 'shortest horizon',
        },
        'weight_sensitivity': [
            {'label': label, 'weights': {study_id: weight for (study_id, _), weight in zip(_STUDIES, (a, b))}}
            for label, a, b in _WEIGHT_SCENARIOS
        ],
        'budget': {'studies': len(_STUDIES), 'session_groups': len(_STUDIES) * sum(n for _, n, _ in _PARTITIONS),
                   'trials_per_session': _TRIALS_PER_SESSION,
                   'rows': len(_STUDIES) * sum(n for _, n, _ in _PARTITIONS) * _TRIALS_PER_SESSION,
                   'candidate_configurations': 3, 'test_evaluations_per_model_and_study': 1},
    }


def _validate_spec(spec):
    if not isinstance(spec, dict):
        raise ValueError('Frozen protocol must be a JSON object')
    reference = protocol_spec(spec.get('seed'), spec.get('candidate'))
    try:
        encoded = canonical(spec)
    except (TypeError, ValueError) as exc:
        raise ValueError('Frozen protocol must be finite JSON') from exc
    if encoded != canonical(reference):
        raise ValueError('Protocol differs from the registered frozen profile')
    return reference


def synthetic_rows(spec: dict) -> list[dict]:
    """Materialize the registered fixture with partition-local deterministic draws."""
    spec = _validate_spec(spec)
    rows = []
    for partition, _, target_time in _PARTITIONS:
        for session_id in spec['split'][partition]['session_groups']:
            study_id = session_id.split(':')[0]
            feature_time = target_time - 3
            for trial in range(1, _TRIALS_PER_SESSION + 1):
                digest = hashlib.sha256(f'{DATASET_VERSION}:{spec["seed"]}:{session_id}:{trial}'.encode()).digest()
                left, right = (int.from_bytes(digest[i:i + 4], 'big') % 9 + 1 for i in (0, 4))
                draw = int.from_bytes(digest[8:16], 'big')
                if study_id == 'aligned-signal':
                    event_probability = Fraction(left + 3 * right, 40)
                else:
                    event_probability = Fraction(19 - right, 24)
                outcome = int(draw * event_probability.denominator < event_probability.numerator * 2**64)
                rows.append({
                    'row_id': f'{session_id}:{trial:02}', 'study_id': study_id, 'session_id': session_id,
                    'split': partition, 'target': TARGET, 'units': UNITS, 'semantics': SEMANTICS,
                    'feature_time': feature_time, 'observed_at': feature_time + 1, 'available_at': feature_time + 2,
                    'target_time': target_time, 'opinions': [str(Fraction(x, 10)) for x in (left, right)],
                    'outcome': outcome, 'scope': SCOPE,
                })
    return rows


def validate_split(rows: list[dict], spec: dict) -> dict[str, list[dict]]:
    """Validate the complete fixture envelope before fitting, selecting, or scoring."""
    spec = _validate_spec(spec)
    if not isinstance(rows, list) or len(rows) != spec['budget']['rows']:
        raise ValueError('Row count differs from the frozen fixture budget')
    expected_partitions = {
        session: partition for partition, _, _ in _PARTITIONS
        for session in spec['split'][partition]['session_groups']
    }
    expected_rows = {f'{session}:{i:02}' for session in expected_partitions for i in range(1, _TRIALS_PER_SESSION + 1)}
    by_partition = {partition: [] for partition, _, _ in _PARTITIONS}
    row_ids = set()
    cutoff = spec['split']['cutoff']
    feature_lags = spec['split']['feature_lags']
    study_ids = {study_id for study_id, _ in _STUDIES}
    plugin = DeGroot()
    for row in rows:
        if not isinstance(row, dict) or row.keys() != _ROW_FIELDS:
            raise ValueError('Row must match the frozen feature/outcome schema')
        identity = row['row_id']
        if not isinstance(identity, str) or identity in row_ids or identity not in expected_rows:
            raise ValueError('Duplicate or unregistered row identity')
        row_ids.add(identity)
        session, partition, study = row['session_id'], row['split'], row['study_id']
        if (not all(isinstance(value, str) for value in (session, partition, study))
                or session not in expected_partitions or partition != expected_partitions[session]
                or study not in study_ids or not session.startswith(f'{study}:') or identity.rsplit(':', 1)[0] != session):
            raise ValueError('Session belongs to a different study or split')
        if (row['target'], row['units'], row['semantics'], row['scope']) != (TARGET, UNITS, SEMANTICS, SCOPE):
            raise ValueError('Incompatible target, units, semantics, or evidence scope')
        event, observed, available, target = (row[key] for key in ('feature_time', 'observed_at', 'available_at', 'target_time'))
        start, end = spec['split'][partition]['target_window']
        if (not all(type(time) is int for time in (event, observed, available, target))
                or not 0 <= event <= observed <= available <= cutoff or not available < target
                or not start <= target <= end or (partition == 'test') != (target > cutoff)):
            raise ValueError('Future information, label leakage, or incompatible target window')
        if any(row[key] != target - lag for key, lag in feature_lags.items()):
            raise ValueError('Feature timing differs from the frozen measurement window')
        if type(row['outcome']) is not int or row['outcome'] not in (0, 1):
            raise ValueError('Bernoulli outcomes must be binary integers')
        if not isinstance(row['opinions'], list) or not all(type(value) is str for value in row['opinions']):
            raise ValueError('Features must be a JSON list of rational strings')
        if plugin.initial_state(row['opinions'])['opinions'] != row['opinions']:
            raise ValueError('Feature probabilities must use canonical rational strings')
        by_partition[partition].append(row)
    return by_partition


def _score(rows, forecasts):
    if not isinstance(forecasts, dict) or forecasts.keys() != {row['row_id'] for row in rows}:
        raise ValueError('Forecast identities must match the scored rows exactly')
    brier, log_loss = [], []
    unknown = Counter()
    for row in rows:
        forecast = forecasts[row['row_id']]
        if not isinstance(forecast, dict):
            raise ValueError('Forecast must declare its uncertainty kind')
        kind = forecast.get('kind')
        if kind in ('UNKNOWN', 'UNIDENTIFIABLE'):
            if forecast.keys() != {'kind'}:
                raise ValueError('Unknown or unidentifiable forecasts cannot contain quantified estimates')
            unknown[kind] += 1
            continue
        if kind != 'BERNOULLI' or forecast.keys() != {'kind', 'probability'}:
            raise ValueError('Forecast must be a supported Bernoulli probability')
        p, y = forecast['probability'], row['outcome']
        if type(p) not in (int, float) or not 0 <= p <= 1:
            raise ValueError('Bernoulli probability must be finite and in [0,1]')
        brier.append((p - y) ** 2)
        log_loss.append(-math.log(max(_EPSILON, p if y else 1 - p)))
    metrics = None if unknown else {'brier': math.fsum(brier) / len(rows), 'log_loss': math.fsum(log_loss) / len(rows)}
    result = {'n': len(rows), 'n_scored': len(brier), 'metrics': metrics}
    if unknown:
        result['uncertainty'] = {'kind': 'UNIDENTIFIABLE' if set(unknown) == {'UNIDENTIFIABLE'} else 'UNKNOWN',
                                 'counts': dict(unknown)}
    return result


def evaluate(rows: list[dict], forecasts: dict, spec: dict, partition: str = 'test') -> dict:
    """Validate all splits and score only the requested partition against keyed forecasts."""
    split = validate_split(rows, spec)
    if not isinstance(partition, str) or partition not in split:
        raise ValueError('Unregistered scoring partition')
    return {'split': partition, **_score(split[partition], forecasts)}


def _normalize_weights(study_ids, weights):
    if not isinstance(weights, dict) or weights.keys() != study_ids:
        raise ValueError('Weights must explicitly name each study exactly once')
    if any(type(w) not in (float, int) or not 0 <= w <= 1e12 for w in weights.values()):
        raise ValueError('Study weights must be finite and nonnegative, at most 1e12')
    total = math.fsum(weights.values())
    if not total:
        raise ValueError('At least one study must have positive weight')
    return {study: weights[study] / total for study in sorted(study_ids)}


def aggregate(study_results: list[dict], weights: dict) -> dict:
    """Combine like-for-like held-out metrics with explicit study weights."""
    if not isinstance(study_results, list) or not study_results:
        raise ValueError('At least one study result is required')
    signature = {'target': TARGET, 'units': UNITS, 'window': [20, 20], 'semantics': SEMANTICS,
                 'split': 'test', 'scope': SCOPE, 'evidence': _scientific_evidence()}
    scored = {}
    for study in study_results:
        if not isinstance(study, dict) or any(study.get(key) != value for key, value in signature.items()):
            raise ValueError('Cannot combine incompatible study target, unit, window, semantics, split, or evidence')
        study_id, metrics = study.get('study_id'), study.get('metrics')
        if (not isinstance(study_id, str) or not study_id.strip() or study_id in scored
                or not isinstance(metrics, dict) or metrics.keys() != {CANDIDATE, BASELINE}):
            raise ValueError('Study identity or registered models are invalid')
        for scores in metrics.values():
            if scores is None:
                continue
            if (not isinstance(scores, dict) or scores.keys() != set(METRICS)
                    or any(type(scores[metric]) not in (int, float) or not 0 <= scores[metric] <= bound
                           for metric, bound in _SCORE_BOUNDS.items())):
                raise ValueError('Study metrics must be finite and within the scoring bounds')
        scored[study_id] = metrics
    normalized = _normalize_weights(scored.keys(), weights)
    combined = {}
    for model in (CANDIDATE, BASELINE):
        included = [(scored[study][model], weight) for study, weight in normalized.items() if weight > 0]
        combined[model] = None if any(scores is None for scores, _ in included) else {
            metric: math.fsum(scores[metric] * weight for scores, weight in included) for metric in METRICS
        }
    return {'weights': normalized, 'metrics': combined, 'evidence': _scientific_evidence()}


def _forecasts(rows, probability):
    return {row['row_id']: {'kind': 'BERNOULLI', 'probability': probability(row)} for row in rows}


def _candidate_probability(plugin, spec, row, horizon):
    parameters = spec['parameters']
    initial = plugin.initial_state(row['opinions'], parameters['weights'])
    final = plugin.simulate(initial, horizon)[-1]
    return float(Fraction(final['opinions'][parameters['forecast_agent']]))


def _fit_on_training(train):
    positives = sum(row['outcome'] for row in train)
    return {'prevalence': positives / len(train), 'training_n': len(train), 'training_events': positives}


def _select_on_validation(plugin, spec, rows_by_study):
    scores = []
    for horizon in spec['parameters']['horizons']:
        study_scores = {}
        for study, validation in rows_by_study.items():
            forecasts = _forecasts(validation, lambda row: _candidate_probability(plugin, spec, row, horizon))
            study_scores[study] = _score(validation, forecasts)['metrics']['brier']
        scores.append({'horizon': horizon, 'study_brier': study_scores,
                       'brier': math.fsum(study_scores.values()) / len(study_scores)})
    chosen = min(scores, key=lambda item: (item['brier'], item['horizon']))
    return {'split': 'validation', 'horizon': chosen['horizon'], 'test_used_for_selection': False,
            'metric': 'brier', 'validation_scores': scores}


def _study_rows(rows, study_id):
    return [row for row in rows if row['study_id'] == study_id]


def _trajectory(plugin, spec):
    environment = {'protocol_version': spec['protocol_version'], 'scope': 'THEORETICAL', 'time_unit': 'discrete-round'}
    initial = plugin.initial_state()
    base = Snapshot.create(plugin.model_id, plugin.version, initial, 'base', None, [], environment)
    branches = []
    branch_weights = (('published-weights', PUBLISHED_WEIGHTS), ('equal-weights', (('1/2', '1/2'), ('1/2', '1/2'))))
    for name, weights in branch_weights:
        state = plugin.initial_state(base.restore()['state']['opinions'], weights)
        steps = plugin.simulate(state, 4)
        if any(step != plugin.analytic_at(state, index) for index, step in enumerate(steps)):
            raise ArithmeticError('Branch trajectory disagrees with the independent analytic recurrence')
        events = [{'type': 'branch_initialization' if index == 0 else 'opinion_update',
                   'time': step['time'], 'state': step} for index, step in enumerate(steps)]
        snapshot = Snapshot.create(plugin.model_id, plugin.version, steps[-1], name, base.content_hash, events, environment)
        branches.append(snapshot.to_dict())
    return {'base': base.to_dict(), 'branches': branches}


def run_comparison(spec: dict) -> dict:
    """Execute the registered comparison and return a deterministic JSON report."""
    spec = _validate_spec(spec)
    rows = synthetic_rows(spec)
    split = validate_split(rows, spec)
    plugin = DeGroot()
    baselines = {study_id: _fit_on_training(_study_rows(split['train'], study_id)) for study_id, _ in _STUDIES}
    validation = {study_id: _study_rows(split['validation'], study_id) for study_id, _ in _STUDIES}
    selection = _select_on_validation(plugin, spec, validation)

    study_results = []
    for study_id, label in _STUDIES:
        test = _study_rows(split['test'], study_id)
        candidate = _forecasts(test, lambda row: _candidate_probability(plugin, spec, row, selection['horizon']))
        baseline = _forecasts(test, lambda row: baselines[study_id]['prevalence'])
        study_results.append({
            'study_id': study_id, 'study_label': label, 'split': 'test', 'n': len(test),
            'target': TARGET, 'units': UNITS, 'window': list(spec['split']['test']['target_window']),
            'semantics': SEMANTICS, 'scope': SCOPE, 'evidence': _scientific_evidence(),
            'baseline': baselines[study_id],
            'metrics': {CANDIDATE: _score(test, candidate)['metrics'], BASELINE: _score(test, baseline)['metrics']},
        })
    weight_sensitivity = [
        {'label': scenario['label'], **aggregate(study_results, scenario['weights'])}
        for scenario in spec['weight_sensitivity']
    ]
    return {
        'scope': SCOPE, 'evidence': _scientific_evidence(), 'metrics': weight_sensitivity[0]['metrics'],
        'study_results': study_results, 'weight_sensitivity': weight_sensitivity,
        'selection': selection, 'trajectory': _trajectory(plugin, spec),
        'mathematical_verification': plugin.verify_reference(),
        'provenance': {'protocol_version': PROTOCOL_VERSION, 'protocol_sha256': _sha256(spec),
                       'dataset_version': DATASET_VERSION, 'input_sha256': _sha256(rows), 'seed': spec['seed'],
                       'source_reference': source_reference(), 'budget': spec['budget'].copy(),
                       'split_counts': {partition: len(partition_rows) for partition, partition_rows in split.items()}},
        'limitations': [
            'The two fixtures contain synthetic session outcomes generated from distinct, declared mechanisms.',
            'DeGroot supplies a scalar opinion update. The benchmark uses agent 0’s finite-round opinion as a Bernoulli forecast.',
            'Weight sensitivity describes these two studies under declared weights. Sampling uncertainty is unestimated.',
            'The trajectory branches illustrate theoretical weight scenarios. Empirical forecasting and causal effects remain unknown.',
        ],
    }
