#!/usr/bin/env python3
"""R065 M: hash-pinned seven-model native-vs-reviewed-reset two-clock trial.

Re-run Phase L shared-fold fits under the untouched original native author
clock and under *only* seven reviewed literal reset changes in an in-memory
copy. This is retrospective internal heldout, NOT external validation.
"""
from __future__ import annotations

import argparse
import json
import math
import types
from pathlib import Path

from r065_phase_k_native_objectives import (
    EXPECTED_PLAYS, MODEL_IDS, load_native, prepare_frames, verified_upstream,
)
from r065_phase_l_native_heldout import evaluate_model, sum_author_nll

ORIGINAL_CLOCK = (23, 45, 67, 89, 111)
BOUNDARY_CLOCK = (18, 35, 52, 69, 86, 103, 120)
SOURCE_NEEDLE = "if row ['day'] in [23, 45, 67, 89, 111]:"
REPLACEMENT_COUNT = 7
PHASE_L_TOL = 1e-7
PARITY_TOL = 1e-8


def modify_only_reset_days(source: str, clock: tuple[int, ...]) -> str:
    """Fail closed except seven literal occurrences in the hash-pinned file."""
    if (clock not in (ORIGINAL_CLOCK, BOUNDARY_CLOCK) or
        source.count(SOURCE_NEEDLE) != REPLACEMENT_COUNT):
        raise ValueError('FAIL CLOSED: source reset selector/clock differs')
    replacement = "if row ['day'] in [" + ", ".join(map(str, clock)) + "]:"
    changed = source.replace(SOURCE_NEEDLE, replacement)
    if changed.count(replacement) != REPLACEMENT_COUNT:
        raise ValueError('FAIL CLOSED: adapter replacement count differs')
    # Reversibility is a direct check that all and only the seven reset
    # predicates changed. The untouched author file is never overwritten.
    if changed.replace(replacement, SOURCE_NEEDLE) != source:
        raise ValueError('FAIL CLOSED: adapter changed more than reset days')
    return changed


def load_reviewed_clock(source_dir: Path, clock: tuple[int, ...]):
    """Import an in-memory reviewed adaptation of exact verified author code."""
    verified_upstream(source_dir)
    source_file = source_dir / 'objectives.py'
    source_text = source_file.read_text(encoding='utf-8')
    modified = modify_only_reset_days(source_text, clock)
    module = types.ModuleType('r065_reviewed_author_reset_' +
                              '_'.join(str(d) for d in clock))
    module.__file__ = str(source_file) + '#REVIEWED_IN_MEMORY_RESET_ONLY'
    exec(compile(modified, module.__file__, 'exec'), module.__dict__)
    for model_id in MODEL_IDS:
        cfg = module.get_model_specs(model_id)
        if not callable(cfg['objective']) or len(cfg['params']) != len(cfg['types']):
            raise ValueError('invalid reviewed author objective specification')
    return module


def check_author_clock_parity(author, reviewed_author_clock, frames: list) -> None:
    """Two numerical probes on all real participants for each model."""
    if len(frames) != 24:
        raise ValueError('expected 24 verified real source participants')
    for number in MODEL_IDS:
        native = author.get_model_specs(number)
        reviewed = reviewed_author_clock.get_model_specs(number)
        if native['types'] != reviewed['types'] or native['params'] != reviewed['params']:
            raise ValueError('FAIL CLOSED: author/reviewed parameter specs differ')
        for probe in (0, 1):
            params = ([0.0] * len(native['types']) if probe == 0 else
                      [-2.0 if param == '0_30' else 0.5
                       for param in native['types']])
            a = sum_author_nll(native['objective'], params, frames)
            b = sum_author_nll(reviewed['objective'], params, frames)
            if abs(a-b) > PARITY_TOL:
                raise ValueError('FAIL CLOSED: native/adapted author clock parity '
                                 + str(number) + '/' + str(probe))


def compare_clock_fits(native: dict, boundary: dict, phase_l_reference: dict):
    """Compare only successfully converged, matching two-fold records."""
    number = native['model_number']
    if number != boundary['model_number'] or number != phase_l_reference['model_number']:
        raise ValueError('FAIL CLOSED: model ID mismatch')
    if (native['status'] != 'TWO_FOLD_COMPLETE' or
        boundary['status'] != 'TWO_FOLD_COMPLETE'):
        raise ValueError('UNRESOLVED: at least one model/clock/fold did not converge')
    if len(native['folds']) != 2 or len(boundary['folds']) != 2 or len(phase_l_reference['folds']) != 2:
        raise ValueError('FAIL CLOSED: two-fold identity missing')
    differences = []
    count = 0
    for author_fold, candidate_fold, ref_fold in zip(
        native['folds'], boundary['folds'], phase_l_reference['folds']
    ):
        if (author_fold['test_fold'] != candidate_fold['test_fold'] or
            author_fold['test_fold'] != ref_fold['test_fold'] or
            author_fold['status'] != 'PASS' or
            candidate_fold['status'] != 'PASS' or
            author_fold['heldout_play'] != candidate_fold['heldout_play'] or
            author_fold['heldout_play'] != ref_fold['heldout_play'] or
            author_fold['heldout_play'] not in (660, 667)):
            raise ValueError('FAIL CLOSED: heldout fold identity/membership mismatch')
        if abs(author_fold['heldout_mean_nll'] - ref_fold['heldout_mean_nll']) > PHASE_L_TOL:
            raise ValueError('FAIL CLOSED: original clock does not reproduce Phase L')
        delta = candidate_fold['heldout_mean_nll'] - author_fold['heldout_mean_nll']
        if not math.isfinite(delta):
            raise ValueError('FAIL CLOSED: nonfinite fold delta')
        differences.append({
            'test_fold': author_fold['test_fold'],
            'heldout_play': author_fold['heldout_play'],
            'candidate_minus_author_nll_per_play': delta,
        })
        count += author_fold['heldout_play']
    if count != EXPECTED_PLAYS or set(d['test_fold'] for d in differences) != {'A', 'B'}:
        raise ValueError('FAIL CLOSED: play universe does not close')
    if abs(native['heldout_mean_nll'] - phase_l_reference['heldout_mean_nll']) > PHASE_L_TOL:
        raise ValueError('FAIL CLOSED: original clock overall anchor differs')
    paired = boundary['heldout_mean_nll'] - native['heldout_mean_nll']
    fold_weighted = math.fsum(d['heldout_play'] * d['candidate_minus_author_nll_per_play']
                              for d in differences) / count
    if not math.isfinite(paired) or abs(paired-fold_weighted) > PARITY_TOL:
        raise ValueError('FAIL CLOSED: aggregate delta not fold weighted')
    return {
        'model_number': number, 'status': 'TWO_CLOCK_COMPLETE',
        'author_heldout_mean_nll': native['heldout_mean_nll'],
        'candidate_heldout_mean_nll': boundary['heldout_mean_nll'],
        'candidate_minus_author_nll_per_play': paired,
        'fold_differences': differences,
    }


def execute(module_author, module_author_adapter, module_candidate,
            frames, play_counts, model_number, reference):
    """Do the two full fits, preserving anonymous optimizer diagnostics."""
    check_author_clock_parity(module_author, module_author_adapter, frames)
    original = evaluate_model(module_author, model_number, frames, play_counts)
    candidate = evaluate_model(module_candidate, model_number, frames, play_counts)
    result = {
        'stage': 'R065_PHASE_M', 'model_number': model_number,
        'source': 'fixed_hash_author_objectives_and_in_memory_seven_reset_adaptation',
        'author_reset_days': list(ORIGINAL_CLOCK),
        'candidate_reset_days': list(BOUNDARY_CLOCK),
        'participants': len(frames), 'play_trials': sum(play_counts),
        'native_author_clock': original,
        'reviewed_candidate_clock': candidate,
        'pesen_v01': 'FROZEN',
    }
    try:
        result['comparison'] = compare_clock_fits(original, candidate, reference)
    except ValueError as exc:
        result['comparison'] = {
            'model_number': model_number,
            'status': 'UNRESOLVED_OR_FAILED_CLOSED',
            'reason': str(exc)[:280],
        }
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--upstream-dir', type=Path, required=True)
    ap.add_argument('--processed', type=Path, required=True)
    ap.add_argument('--raw-dir', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--phase-l-results', type=Path, required=True)
    ap.add_argument('--model-number', type=int, choices=MODEL_IDS, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    author = load_native(args.upstream_dir)
    author_adapter = load_reviewed_clock(args.upstream_dir, ORIGINAL_CLOCK)
    candidate = load_reviewed_clock(args.upstream_dir, BOUNDARY_CLOCK)
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    reference = json.loads(args.phase_l_results.read_text(encoding='utf-8'))
    if (reference.get('stage') != 'R065_PHASE_L' or
        reference.get('sampling', {}).get('source_play_trials') != EXPECTED_PLAYS or
        reference.get('upstream', {}).get('native_source_objectives_blob') !=
            '5e98133fa274ef2a112b24f6fdcd802d4f9d3eec'):
        raise ValueError('FAIL CLOSED: invalid Phase L anchor file')
    selected = [x for x in reference['models']
                if x['model_number'] == args.model_number]
    if len(selected) != 1:
        raise ValueError('FAIL CLOSED: Phase L model missing or duplicated')
    frames, nplay = prepare_frames(args.processed.read_bytes(), args.raw_dir, manifest)
    if nplay != EXPECTED_PLAYS:
        raise ValueError('FAIL CLOSED: source play universe mismatch')
    plays = [int((f['task_type'] == 'play').sum()) for f in frames]
    result = execute(author, author_adapter, candidate, frames, plays,
                     args.model_number, selected[0])
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n',
                           encoding='utf-8')
    comparison = result['comparison']
    print(json.dumps({
        'stage': 'R065_PHASE_M',
        'model_number': args.model_number,
        'comparison': comparison,
        'author_native_fit_status': result['native_author_clock']['status'],
        'reviewed_candidate_fit_status': result['reviewed_candidate_clock']['status'],
    }, sort_keys=True))
    if comparison['status'] != 'TWO_CLOCK_COMPLETE':
        raise RuntimeError('Phase M model comparison unresolved: no PASS')


if __name__ == '__main__':
    main()
