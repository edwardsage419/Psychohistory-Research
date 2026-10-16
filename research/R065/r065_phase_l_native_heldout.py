#!/usr/bin/env python3
"""R065 Phase L: native author seven-model retrospective two-fold heldout audit.

The two stratified participant folds, initializations, optimizer and stopping
rules are frozen in protocols/R065_PHASE_L_SEVEN_NATIVE_HELDOUT_2026-10-16.md.
Only anonymized aggregate fold metrics leave this process.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from r065_phase_k_native_objectives import (
    EXPECTED_PLAYS, MODEL_IDS, load_native, prepare_frames,
)

FOLD_A = tuple(list(range(0, 12, 2)) + list(range(12, 24, 2)))
FOLD_B = tuple(list(range(1, 12, 2)) + list(range(13, 24, 2)))
BOUNDS = (-8.0, 8.0)
MAXITER = 80
MAXFUN = 900
FTOL = 1e-8
GTOL = 1e-5


def validate_folds(a: tuple[int, ...] = FOLD_A,
                   b: tuple[int, ...] = FOLD_B) -> None:
    if (len(a) != 12 or len(b) != 12 or len(set(a)) != 12 or
        len(set(b)) != 12 or set(a) & set(b) or
        set(a) | set(b) != set(range(24)) or
        sum(i < 12 for i in a) != 6 or sum(i >= 12 for i in a) != 6 or
        sum(i < 12 for i in b) != 6 or sum(i >= 12 for i in b) != 6):
        raise ValueError('FAIL CLOSED: invalid disjoint stratified folds')


def get_starts(types: list[str]) -> list[list[float]]:
    if not types or any(t not in ('01', '05_1', '0_30') for t in types):
        raise ValueError('unexpected parameter type')
    return [[-4.0 if t == '0_30' else 0.0 for t in types],
            [-2.0 if t == '0_30' else 1.0 for t in types]]


def sum_author_nll(obj, params, frames) -> float:
    """Entire grouped objective is trained/scored on exactly supplied people."""
    if not frames:
        raise ValueError('empty participant list')
    total = math.fsum(float(obj(params, person, transform=True)) for person in frames)
    if not math.isfinite(total) or total < -1e-8:
        raise ValueError('nonfinite or negative native author objective')
    return total


def choose_converged(candidates: list[dict]) -> dict | None:
    valid = [c for c in candidates if c['success'] and
             math.isfinite(c['train_total_nll']) and
             all(math.isfinite(v) and BOUNDS[0]-1e-9 <= v <= BOUNDS[1]+1e-9
                 for v in c['params'])]
    return min(valid, key=lambda c: c['train_total_nll']) if valid else None


def fit_one_fold(obj, types: list[str], train_frames: list) -> dict:
    from scipy.optimize import minimize
    if not train_frames:
        raise ValueError('missing training participants')
    candidates = []
    for start_index, start in enumerate(get_starts(types)):
        def objective(theta):
            return sum_author_nll(obj, theta, train_frames)
        try:
            opt = minimize(
                objective, start, method='L-BFGS-B',
                bounds=[BOUNDS] * len(types),
                options={'maxiter': MAXITER, 'maxfun': MAXFUN,
                         'ftol': FTOL, 'gtol': GTOL})
            score = float(opt.fun)
            params = [float(x) for x in opt.x]
            sane = math.isfinite(score) and all(math.isfinite(p) for p in params)
            record = {
                'start': start_index,
                'success': bool(opt.success) and sane,
                'train_total_nll': score if math.isfinite(score) else None,
                'nit': int(opt.nit), 'nfev': int(opt.nfev),
                'params': params if sane else [],
                'message': str(opt.message)[:160],
            }
        except (ArithmeticError, ValueError, OverflowError) as error:
            record = {
                'start': start_index, 'success': False,
                'train_total_nll': None, 'nit': 0, 'nfev': 0,
                'params': [], 'message': 'optimizer exception: ' + type(error).__name__,
            }
        candidates.append(record)
    chosen = choose_converged(candidates)
    return {'candidates': candidates, 'selected': chosen}


def evaluate_model(module, model_number: int, frames: list,
                   play_counts: list[int]) -> dict:
    validate_folds()
    if (model_number not in MODEL_IDS or len(frames) != 24 or
        len(play_counts) != 24 or any(n < 1 for n in play_counts) or
        sum(play_counts) != EXPECTED_PLAYS):
        raise ValueError('invalid full source universe')
    spec = module.get_model_specs(model_number)
    types = spec['types']
    if len(types) != len(spec['params']):
        raise ValueError('invalid author parameter specification')
    objective = spec['objective']
    out = {'model_number': model_number, 'param_types': types,
           'param_count': len(types), 'folds': []}
    heldout_total = 0.0
    heldout_play = 0
    for fold_name, test_ids, train_ids in (
        ('A', FOLD_A, FOLD_B), ('B', FOLD_B, FOLD_A)
    ):
        train = [frames[i] for i in train_ids]
        test = [frames[i] for i in test_ids]
        fitted = fit_one_fold(objective, types, train)
        # Never test a model with no validated converged training candidate.
        selected = fitted['selected']
        folded = {
            'test_fold': fold_name, 'training_subjects': len(train),
            'heldout_subjects': len(test),
            'training_play': sum(play_counts[i] for i in train_ids),
            'heldout_play': sum(play_counts[i] for i in test_ids),
            'starts': [{k: v for k, v in cand.items() if k != 'params'}
                       for cand in fitted['candidates']],
        }
        if selected is None:
            folded['status'] = 'UNRESOLVED_NO_CONVERGED_START'
        else:
            fold_score = sum_author_nll(objective, selected['params'], test)
            folded.update({
                'status': 'PASS',
                'chosen_start': selected['start'],
                'train_total_nll': selected['train_total_nll'],
                'heldout_total_nll': fold_score,
                'heldout_mean_nll': fold_score / folded['heldout_play'],
                'native_unbounded_params': selected['params'],
            })
            heldout_total += fold_score
            heldout_play += folded['heldout_play']
        out['folds'].append(folded)
    if all(fold['status'] == 'PASS' for fold in out['folds']) and heldout_play == EXPECTED_PLAYS:
        out['status'] = 'TWO_FOLD_COMPLETE'
        out['heldout_total_nll'] = heldout_total
        out['heldout_mean_nll'] = heldout_total / heldout_play
    else:
        out['status'] = 'UNRESOLVED'
        out['heldout_mean_nll'] = None
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream-dir', type=Path, required=True)
    parser.add_argument('--processed', type=Path, required=True)
    parser.add_argument('--raw-dir', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--model-number', type=int, choices=MODEL_IDS, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    module = load_native(args.upstream_dir)
    frames, nplay = prepare_frames(args.processed.read_bytes(), args.raw_dir, manifest)
    if nplay != EXPECTED_PLAYS:
        raise ValueError('incorrect source universe')
    plays = [int((f['task_type'] == 'play').sum()) for f in frames]
    outcome = evaluate_model(module, args.model_number, frames, plays)
    rendered = {
        'stage': 'R065_PHASE_L', 'scope': 'RETROSPECTIVE_24_PERSON_NATIVE_HOLDOUT',
        'source_pinned': True, 'participants': 24, 'play_trials': nplay,
        'author_clock_only': True, 'optimizer': {
            'method': 'L-BFGS-B', 'starts': 2, 'latent_bounds': list(BOUNDS),
            'maxiter': MAXITER, 'maxfun': MAXFUN, 'ftol': FTOL, 'gtol': GTOL,
        }, 'model': outcome, 'pesen_v01': 'FROZEN',
    }
    args.output.write_text(json.dumps(rendered, indent=2, ensure_ascii=False) + '\n',
                           encoding='utf-8')
    # Results are anonymized aggregate fold metrics. Exit nonzero on unresolved fits.
    print(json.dumps({'stage': rendered['stage'], 'model': args.model_number,
                      'status': outcome['status'],
                      'folds': [{k: v for k, v in f.items()
                                 if k in ('test_fold', 'status', 'heldout_play',
                                          'heldout_mean_nll', 'training_play')}
                                for f in outcome['folds']],
                      'heldout_mean_nll': outcome['heldout_mean_nll']},
                     sort_keys=True))
    if outcome['status'] != 'TWO_FOLD_COMPLETE':
        raise RuntimeError('Phase L inconclusive: optimization convergence gate failed')


if __name__ == '__main__':
    main()
