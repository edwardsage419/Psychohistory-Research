#!/usr/bin/env python3
"""R065 K: exact-source native author seven-objective execution gate.

This is a source-pinned execution smoke test, NOT seven-model fitting or held-out
prediction. It consumes (and never publishes) 24 original author CSV files.
"""
from __future__ import annotations

import argparse
import importlib.util
import hashlib
import io
import json
import math
import sys
from pathlib import Path

EXPECTED_OBJECTIVES = '5e98133fa274ef2a112b24f6fdcd802d4f9d3eec'
EXPECTED_UTILS = '6046f083a1181b10a7d991c8c9fd2e53c1f2b487'
MODEL_IDS = tuple(range(1, 8))
EXPECTED_PLAYS = 1327


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def verified_upstream(source_dir: Path) -> Path:
    """Require exact original upstream source bytes prior to import execution."""
    for filename, expected in [('objectives.py', EXPECTED_OBJECTIVES),
                               ('fit_utils.py', EXPECTED_UTILS)]:
        raw = (source_dir / filename).read_bytes()
        if git_blob_sha1(raw) != expected:
            raise ValueError('FAIL CLOSED: upstream native source mismatch: ' + filename)
    return source_dir / 'objectives.py'


def load_native(source_dir: Path):
    path = verified_upstream(source_dir)
    if str(source_dir.resolve()) not in sys.path:
        sys.path.insert(0, str(source_dir.resolve()))
    spec = importlib.util.spec_from_file_location('r065_author_native_objectives', path)
    if spec is None or spec.loader is None:
        raise ValueError('failed to construct verified author module')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for number in MODEL_IDS:
        cfg = module.get_model_specs(number)
        if len(cfg['params']) != len(cfg['types']) or not callable(cfg['objective']):
            raise ValueError('invalid author model specification')
    return module


def prepare_frames(processed: bytes, raw_dir: Path, manifest: dict):
    """Use the Phase J frozen IDs and per-file hashes; keep all rows private."""
    import pandas as pd
    from r065_critical_replay import parse_verified
    from r065_phase_h_model3_reset import source_trials
    from r065_phase_j_screened_replay import select_eligible, verify_manifest
    selected = select_eligible(parse_verified(processed), strict=True)
    ids = selected['first_high'] + selected['first_low']
    blobs = verify_manifest(manifest)
    if len(ids) != len(blobs) or len(ids) != 24 or len(set(ids)) != 24:
        raise ValueError('invalid selected participant set')
    frames = []
    nplay = 0
    for pid, sha in zip(ids, blobs):
        raw = (raw_dir / (pid + '.csv')).read_bytes()
        validated = source_trials(raw, sha)
        df = pd.read_csv(io.BytesIO(raw))
        df = df[df['phase'] == 'experimental'].reset_index(drop=True)
        if len(df) != len(validated) or len(df) != 136:
            raise ValueError('source parser and native pandas disagree')
        if [int(x) for x in df['day']] != list(range(1, 137)):
            raise ValueError('native day sequence disagrees with expected trials')
        native_plays = int((df['task_type'] == 'play').sum())
        if native_plays != sum(x['type'] == 'play' for x in validated):
            raise ValueError('native play count disagrees with source parser')
        nplay += native_plays
        frames.append(df)
    if nplay != EXPECTED_PLAYS or nplay != manifest['scored_play_trials']:
        raise ValueError('play universe mismatch')
    return frames, nplay


def evaluate_native(module, frames: list, manifest: dict, nplay: int):
    """Execute unmodified author functions; assert established Model3 parity."""
    if not frames or nplay != EXPECTED_PLAYS:
        raise ValueError('invalid native scoring universe')
    scores = {}
    for number in MODEL_IDS:
        cfg = module.get_model_specs(number)
        params = [0.0] * len(cfg['params'])
        total = math.fsum(float(cfg['objective'](params, df, transform=True))
                          for df in frames)
        if not math.isfinite(total) or total < 0:
            raise ValueError('nonfinite author objective ' + str(number))
        scores[str(number)] = {'unfitted_zero_vector_total_nll': total}
    beta = float(manifest['models']['author']['beta_optimal'])
    m3 = module.get_model_specs(3)['objective']
    native_opt = math.fsum(float(m3([beta], df, transform=False)) for df in frames)
    native_fixed = math.fsum(float(m3([5.0], df, transform=False)) for df in frames)
    assert_model3_anchor(native_opt, native_fixed, manifest, nplay)
    return {
        'stage': 'R065_PHASE_K',
        'status': 'EXACT_SOURCE_NATIVE_SMOKE_PASS',
        'model_ids': list(MODEL_IDS),
        'subjects': len(frames),
        'scored_play_trials': nplay,
        'source_objectives_git_blob': EXPECTED_OBJECTIVES,
        'source_fit_utils_git_blob': EXPECTED_UTILS,
        'models': scores,
        'native_model3_author_beta': beta,
        'native_model3_mean_nll': native_opt / nplay,
        'native_model3_fixed_beta5_mean_nll': native_fixed / nplay,
        'interpretation': 'Unmodified author native objectives at unfitted neutral parameters; only Model3 in-sample anchor checked. No model selection, refit, hierarchical EM, or held-out prediction.',
        'pesen_v01': 'FROZEN',
    }


def assert_model3_anchor(native_opt: float, native_fixed: float, manifest: dict,
                         nplay: int, atol: float = 1e-8):
    if nplay != EXPECTED_PLAYS or not all(map(math.isfinite, (native_opt, native_fixed))):
        raise ValueError('invalid native Model3 score')
    source = manifest['models']['author']
    for observed, field in [(native_opt, 'in_sample_mean_nll'),
                            (native_fixed, 'fixed_beta5_mean_nll')]:
        expected = float(source[field])
        if not math.isfinite(expected) or abs(observed/nplay - expected) > atol:
            raise ValueError('FAIL CLOSED: native Model3 disagrees with Phase J: ' + field)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--upstream-dir', type=Path, required=True)
    ap.add_argument('--processed', type=Path, required=True)
    ap.add_argument('--raw-dir', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    module = load_native(args.upstream_dir)
    frames, nplay = prepare_frames(args.processed.read_bytes(), args.raw_dir, manifest)
    results = evaluate_native(module, frames, manifest, nplay)
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'native_models': 7,
                      'subjects': results['subjects'], 'play': nplay}))


if __name__ == '__main__':
    main()
