"""Independently recompute the frozen comparison and check the archived Linux results."""

import argparse
import hashlib
import json
import math
import platform
import sqlite3
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from psychohistory.contracts import canonical
from psychohistory.degroot import DeGroot
from psychohistory.prediction import protocol_spec, run_comparison, synthetic_rows


PROJECT = Path(__file__).resolve().parents[1]
LINUX = PROJECT / 'reports/v02'
SEED = 207


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def published_opinions(left, right, rounds):
    mean = (left + 2 * right) / 3
    gap = (left - right) / 4**rounds
    return mean + 2 * gap / 3, mean - gap / 3


def score(rows, forecast, epsilon):
    pairs = [(forecast(row), row['outcome']) for row in rows]
    return {
        'brier': float(sum((p - y) ** 2 for p, y in pairs) / len(pairs)),
        'log_loss': math.fsum(-math.log(max(epsilon, float(p if y else 1 - p)))
                              for p, y in pairs) / len(pairs),
    }


def check_scores(actual, expected, label):
    require(actual.keys() == expected.keys(), f'{label}: metric names differ')
    for name, value in expected.items():
        require(math.isclose(actual[name], value, rel_tol=0, abs_tol=2e-15),
                f'{label} {name}: expected {value}, got {actual[name]}')


def independently_evaluate(spec, result):
    rows = synthetic_rows(spec)
    by_split = {name: [row for row in rows if row['split'] == name]
                for name in ('train', 'validation', 'test')}
    require(len({row['row_id'] for row in rows}) == spec['budget']['rows'],
            'Duplicate row identities or unexpected dataset size')
    for a, b in combinations(by_split.values(), 2):
        require({r['session_id'] for r in a}.isdisjoint(r['session_id'] for r in b),
                'A session spans distinct partitions')
    cutoff = spec['split']['cutoff']
    for row in rows:
        require(row['available_at'] <= cutoff and row['available_at'] < row['target_time']
                and (row['target_time'] > cutoff) == (row['split'] == 'test'),
                'An input or label violates the time cutoff')

    epsilon = spec['metrics']['log_loss']['epsilon']
    studies = [study['study_id'] for study in spec['dataset']['studies']]

    def forecast(row, horizon):
        left, right = map(Fraction, row['opinions'])
        return published_opinions(left, right, horizon)[0]

    def partition(name, study):
        return [row for row in by_split[name] if row['study_id'] == study]

    validation = {}
    for horizon in spec['parameters']['horizons']:
        validation[horizon] = {study: score(partition('validation', study),
                                           lambda row: forecast(row, horizon), epsilon)['brier']
                               for study in studies}
    selected = min(validation, key=lambda h: (math.fsum(validation[h].values()), h))
    require(result['selection']['horizon'] == selected
            and result['selection']['split'] == 'validation'
            and result['selection']['test_used_for_selection'] is False,
            'Validation-only selection disagrees')
    for detail in result['selection']['validation_scores']:
        check_scores(detail['study_brier'], validation[detail['horizon']], 'validation Brier')

    recalculated = {}
    for study in result['study_results']:
        name = study['study_id']
        train = partition('train', name)
        test = partition('test', name)
        prevalence = Fraction(sum(r['outcome'] for r in train), len(train))
        require(study['baseline'] == {'prevalence': float(prevalence),
                                     'training_n': len(train),
                                     'training_events': sum(r['outcome'] for r in train)}
                and study['n'] == len(test)
                and study['evidence']['kind'] == 'UNKNOWN',
                f'{name}: baseline, holdout size or evidence differs')
        recalculated[name] = {
            'r123-degroot': score(test, lambda row: forecast(row, selected), epsilon),
            'train-prevalence': score(test, lambda row: prevalence, epsilon),
        }
        for model, scores in recalculated[name].items():
            check_scores(study['metrics'][model], scores, f'{name} {model}')

    scenarios = spec['weight_sensitivity']
    require(len(scenarios) == len(result['weight_sensitivity']), 'Weight scenarios differ')
    for scenario, actual in zip(scenarios, result['weight_sensitivity'], strict=True):
        weights = scenario['weights']
        normalized = {study: weight / sum(weights.values()) for study, weight in weights.items()}
        require(actual['weights'] == normalized and actual['label'] == scenario['label']
                and actual['evidence']['kind'] == 'UNKNOWN', 'Sensitivity metadata differs')
        for model, metrics in actual['metrics'].items():
            expected = {metric: math.fsum(normalized[study] * recalculated[study][model][metric]
                                          for study in studies) for metric in metrics}
            check_scores(metrics, expected, f"{scenario['label']} {model}")
    require(result['evidence']['kind'] == 'UNKNOWN' and result['scope'] == 'SYNTHETIC_ONLY',
            'Scientific evidence or permission changed')
    return recalculated


def compare_linux(native, linux, path, rounding):
    require(type(native) is type(linux), f'{path}: Linux value type differs')
    if type(native) is dict:
        require(native.keys() == linux.keys(), f'{path}: Linux object keys differ')
        for key in native:
            compare_linux(native[key], linux[key], f'{path}.{key}', rounding)
    elif type(native) is list:
        require(len(native) == len(linux), f'{path}: Linux array length differs')
        for i, value in enumerate(native):
            compare_linux(value, linux[i], f'{path}[{i}]', rounding)
    elif native != linux:
        require(type(native) is float and math.isclose(native, linux, rel_tol=0, abs_tol=2e-15),
                f'{path}: Linux {linux!r} differs from native {native!r}')
        rounding.append({'field': path, 'linux': linux, 'native': native})


def verify(receipts):
    plugin = DeGroot()
    initial = plugin.initial_state()
    steps = plugin.simulate(initial, 32)
    expect = [[str(x) for x in published_opinions(Fraction(0), Fraction(1), i)] for i in range(33)]
    require([s['opinions'] for s in steps] == expect, 'Exact 32-round closed form disagrees')
    require(plugin.consensus(initial)['limit'] == ['2/3', '2/3'], 'Incorrect exact consensus')
    saved = plugin.restore_state(plugin.serialize_state(steps[16]))
    require(plugin.simulate(saved, 16) == steps[16:], 'Resumed exact trajectory differs')

    modes = [read(receipts / f'guards-{tag}.json') for tag in ('normal', 'flag', 'env')]
    require([m.pop('optimization') for m in modes] == [0, 1, 1] and modes[0] == modes[1] == modes[2],
            'Scientific guards differ when optimized')
    cli = read(receipts / 'cli.json')
    same_cli = read(receipts / 'cli-optimize.json')
    require(cli['artifact_sha256'] == same_cli['artifact_sha256'], 'Optimized CLI artifact changed')

    spec = protocol_spec(SEED)
    native = run_comparison(spec)
    require(native == run_comparison(spec), 'Native re-execution differs')
    verified_scores = independently_evaluate(spec, native)
    archived = read(LINUX / 'browser-synthetic-result.json')
    linux = {key: archived[key] for key in native}
    rounding = []
    compare_linux(native, linux, 'comparison', rounding)
    require(archived['input']['spec'] == spec, 'Linux frozen protocol differs')
    sources = read(LINUX / 'SOURCE_SHA256.json')
    source_hashes = {}
    for name in ('degroot.py', 'prediction.py'):
        path = f'platform/future_model/src/psychohistory/{name}'
        source_hashes[path] = digest((PROJECT / 'src/psychohistory' / name).read_bytes())
        require(source_hashes[path] == sources[path], f'{name}: Linux source identity differs')
    result = {
        'status': 'PASS',
        'platform': platform.platform(),
        'python': platform.python_version(),
        'sqlite': sqlite3.sqlite_version,
        'scientific_sources': source_hashes,
        'linux_archived_artifact_file_sha256': digest((LINUX / 'browser-synthetic-result.json').read_bytes()),
        'linux_scientific_projection_sha256': digest(canonical(linux).encode()),
        'native_scientific_projection_sha256': digest(canonical(native).encode()),
        'floating_point_differences': rounding,
        'native_cli_artifact_sha256': cli['artifact_sha256'],
        'linux_cli_artifact_sha256': read(LINUX / 'cli.json')['artifact_sha256'],
        'independent_study_scores': verified_scores,
        'exact_trajectory': expect,
        'scientific_result': native,
    }
    (receipts / 'cross-platform.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('exact_trajectory', 'scientific_result')}, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipts', type=Path)
    verify(parser.parse_args().receipts)
