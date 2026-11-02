#!/usr/bin/env python3
"""Non-invasive error injection against byte-identical archived R272 source."""
import argparse
import csv
import importlib.util
import json
import tempfile
from fractions import Fraction
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('mutation', choices=['mass_zero', 'duplicate_identity', 'oracle_zero'])
args = p.parse_args()
source = Path(__file__).resolve().parents[2] / 'research/R272/r272_exact_train_test_prediction.py'
spec = importlib.util.spec_from_file_location('r272_original', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if args.mutation == 'oracle_zero':
    module.independent_analytic = lambda p, m: (Fraction(0), Fraction(0), Fraction(0))
else:
    original = module.source_rows
    def tampered(p, m):
        for idx, item in enumerate(original(p, m)):
            item = dict(item)
            if idx == 0 and args.mutation == 'mass_zero':
                item['exact_original_source_probability'] = Fraction(0)
            if idx == 0 and args.mutation == 'duplicate_identity':
                item['original_full_sixbit_source'] = '000001'
            yield item
    module.source_rows = tampered

with tempfile.TemporaryDirectory(prefix='r272_mutated_') as d:
    module.HERE = Path(d)
    try:
        receipt = module.emit()
        results = json.loads((module.HERE / 'R272_EXACT_RESULTS.json').read_text())
        with (module.HERE / 'R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv').open() as f:
            rows = list(csv.DictReader(f))
        first = [r for r in rows if r['world'] == results['world_results'][0]['world']]
        out = dict(mode='optimized' if not __debug__ else 'normal', mutation=args.mutation,
                   outcome='ACCEPTED', receipt=receipt,
                   claims_verified=results['all_nine_analytical_binomial_scores_verified'],
                   source_count=len(rows), first_world_unique_sources=len(set(r['original_full_sixbit_source'] for r in first)),
                   first_world_mass=str(sum((Fraction(r['exact_original_source_probability']) for r in first), Fraction(0))),
                   first_world_score=results['world_results'][0]['exact_design_expected_train_mean_Brier'])
        print(json.dumps(out, sort_keys=True))
    except Exception as e:
        print(json.dumps(dict(mode='optimized' if not __debug__ else 'normal',
                              mutation=args.mutation, outcome='REJECTED',
                              error_type=type(e).__name__, error=str(e)[:120]), sort_keys=True))
