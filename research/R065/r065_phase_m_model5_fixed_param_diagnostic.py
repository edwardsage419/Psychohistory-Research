#!/usr/bin/env python3
"""Post-hoc R065 M5 FAIL-CLOSED diagnostic: replay four fixed latent vectors.

No optimization, clock selection, fit re-ranking, or protocol revision occurs.
The four input parameter vectors were extracted from original L/M runner
artifacts before this diagnostic was designed.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from r065_phase_k_native_objectives import EXPECTED_PLAYS, load_native, prepare_frames
from r065_phase_l_native_heldout import FOLD_A, FOLD_B, sum_author_nll

TRAIN_ABS_TOL = 1e-8
HELDOUT_MEAN_TOL = 1e-9

# Explicit input source artifacts:
# Phase L run 38843245182 -> artifact 12022142139 (model_5.json)
# Phase M run 38844279247 -> artifact 12022816570 (model_5.json)
SAVED_MODELS = {
    'PHASE_L_FOLD_A': {
        'params': [1.3481999702307128, -3.2978825809152252,
                   -2.357735540916652, 1.0763862322566489,
                   0.08133425260642331],
        'train_nll': 431.3305695660382,
        'test_mean_nll': 0.6360526708211005,
        'fold': 'A',
    },
    'PHASE_L_FOLD_B': {
        'params': [2.0271204337118673, -2.5679486520377153,
                   -0.7618270700129777, 8.0, 2.541352672849412],
        'train_nll': 413.5733573690336,
        'test_mean_nll': 0.6710599876238054,
        'fold': 'B',
    },
    'PHASE_M_FOLD_A': {
        'params': [1.3482144861570793, -3.2978875997311885,
                   -2.357859694497238, 1.0763789467988167,
                   0.08132971131747178],
        'train_nll': 431.3305695539493,
        'test_mean_nll': 0.6360528702863637,
        'fold': 'A',
    },
    'PHASE_M_FOLD_B': {
        'params': [2.027866980348166, -2.5680342394444113,
                   -0.7612693478778935, 8.0, 2.543650144445993],
        'train_nll': 413.57335900110917,
        'test_mean_nll': 0.6710638279760015,
        'fold': 'B',
    },
}


def evaluate_saved_params(model_objective, frames, plays, saved=SAVED_MODELS):
    if len(frames) != 24 or len(plays) != 24 or sum(plays) != EXPECTED_PLAYS:
        raise ValueError('invalid 24 participant source universe')
    if len(saved) != 4:
        raise ValueError('expected exactly four stored parameter vectors')
    output = {}
    for label, case in saved.items():
        fold = case['fold']
        if fold not in ('A', 'B') or len(case['params']) != 5:
            raise ValueError('invalid fixed original Model5 vector')
        if not all(math.isfinite(x) and -8 <= x <= 8 for x in case['params']):
            raise ValueError('nonfinite or out-of-bounds frozen vector')
        testing = FOLD_A if fold == 'A' else FOLD_B
        training = FOLD_B if fold == 'A' else FOLD_A
        n_test = sum(plays[i] for i in testing)
        n_train = sum(plays[i] for i in training)
        if (len(testing) != 12 or len(training) != 12 or
            (n_test, n_train) != ((667,660) if fold=='A' else (660,667))):
            raise ValueError('heldout fold membership changed')
        params = case['params']
        train_loss = sum_author_nll(model_objective, params, [frames[i] for i in training])
        test_loss = sum_author_nll(model_objective, params, [frames[i] for i in testing]) / n_test
        train_err = train_loss - case['train_nll']
        test_err = test_loss - case['test_mean_nll']
        passed = abs(train_err) <= TRAIN_ABS_TOL and abs(test_err) <= HELDOUT_MEAN_TOL
        output[label] = {
            'fold': fold, 'replayed_train_total_nll': train_loss,
            'replayed_heldout_mean_nll': test_loss,
            'train_total_nll_error': train_err,
            'heldout_mean_nll_error': test_err, 'passed': passed,
        }
    return {
        'stage': 'R065_PHASE_M_MODEL5_FIXED_PARAM_DIAGNOSTIC',
        'scope': 'POSTHOC_SOURCE_PINNED_FIXED_PARAMS_NO_OPTIMIZER',
        'status': ('FOUR_PARAMETER_VECTORS_REPLAY_PASS' if all(x['passed'] for x in output.values())
                   else 'FAIL_CLOSED_FIXED_PARAMS_DISAGREE'),
        'subject_count': 24, 'play_trials': EXPECTED_PLAYS,
        'replays': output,
        'phase_m_model5_clock_comparison': 'STILL_FAIL_CLOSED',
        'phase_m_seven_model_complete': False,
        'pesen_v01': 'FROZEN',
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--upstream-dir', type=Path, required=True)
    ap.add_argument('--processed', type=Path, required=True)
    ap.add_argument('--raw-dir', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    native = load_native(args.upstream_dir)
    spec = native.get_model_specs(5)
    if len(spec['params']) != 5:
        raise ValueError('source model5 parameter contract changed')
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    frames, count = prepare_frames(args.processed.read_bytes(), args.raw_dir, manifest)
    plays = [int((f['task_type']=='play').sum()) for f in frames]
    if count != EXPECTED_PLAYS:
        raise ValueError('source play universe mismatch')
    result = evaluate_saved_params(spec['objective'], frames, plays)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True))
    if result['status'] != 'FOUR_PARAMETER_VECTORS_REPLAY_PASS':
        raise RuntimeError('fixed parameter replay failed; Phase M remains blocked')


if __name__ == '__main__':
    main()
