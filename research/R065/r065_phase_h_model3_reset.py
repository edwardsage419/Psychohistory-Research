#!/usr/bin/env python3
"""R065 Phase H: Model 3 reset-date sensitivity on fixed original raw files.

A standard-library source-equivalent reimplementation of the author's copy-last
objective, NOT native scipy/numpy execution or refitting. Fixed beta=5.
No raw participant records or per-participant outcomes are written to output.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

SOURCE_REPO = 'arielevy8/obs-learning-fishing'
SOURCE_COMMIT = 'fd5f435b5368b69916e7acc6a9991aa5f46b3ddb'
OBJECTIVES_BLOB = '5e98133fa274ef2a112b24f6fdcd802d4f9d3eec'
FIT_UTILS_BLOB = '6046f083a1181b10a7d991c8c9fd2e53c1f2b487'
AUTHOR_RESET = (23, 45, 67, 89, 111)
BLOCK_RESET = (18, 35, 52, 69, 86, 103, 120)
BETA = 5.0
# Fixed ex ante, in this exact order. The original participant files are NOT republished.
SAMPLE_BLOBS = {
    'MEVVC.csv': '4e56c2d130d29c5dd9a30cb78587672acd084cc5',
    'Q3A3A.csv': 'c7e5d21544d1f5e673c8b6ec905ad59a70cd4d1c',
    '1XAVL.csv': '9b1f5c8d506480d473fd8a1d71e999f36d40a7ba',
    'JCGCF.csv': '62b70b81a551af31f91fa7fbd9b79dfb785b3766',
    'SMZVB.csv': '96cff2cd222739ac3becef728754107b6d3845cb',
    '8X46Z.csv': 'bfc4d832826d3de03c643bc0640d9e883976b26c',
    '2MZGN.csv': '5b509dcd748be3fc7354e76f946cb44fd6b7d180',
    '6Q6XN.csv': '214c78ffc3d58f8fed420f3dae80e71ddd546a36',
    '47ZAD.csv': '561bb3b072362a80c43b242d236bf34624c8911d',
    'YC4CP.csv': 'a1b0ddc977df858aebb25e1a13a4f4457e4da973',
}


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def source_trials(raw: bytes, expected_blob: str) -> list[dict]:
    if git_blob_sha1(raw) != expected_blob:
        raise ValueError('FAIL CLOSED: raw participant Git blob mismatch')
    from io import StringIO
    reader = csv.DictReader(StringIO(raw.decode('utf-8-sig'), newline=''))
    required = {'phase', 'day', 'task_type', 'available_boats', 'boat_chosen_id'}
    if not required.issubset(reader.fieldnames or ()):
        raise ValueError('raw source required trial fields missing')
    trials = []
    for row in reader:
        if row['phase'] != 'experimental':
            continue
        try:
            day_float, chosen_float = float(row['day']), float(row['boat_chosen_id'])
            available = json.loads(row['available_boats'])
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError('malformed experimental trial') from exc
        if (not day_float.is_integer() or int(day_float) != len(trials) + 1 or
            not chosen_float.is_integer() or
            row['task_type'] not in ('observe', 'play') or
            not isinstance(available, list) or len(available) != 2 or
            len(set(available)) != 2 or not all(type(x) is int and x in (0, 1, 2) for x in available) or
            int(chosen_float) not in available):
            raise ValueError('malformed or nonconsecutive original experimental trials')
        trials.append({'day': int(day_float), 'type': row['task_type'],
                       'available': available, 'chosen': int(chosen_float)})
    if len(trials) != 136:
        raise ValueError('expected exactly 136 experimental trials')
    return trials


def predict(trials: list[dict], reset_days: tuple[int, ...], beta: float = BETA) -> list[dict]:
    """Equivalent to source model_3_objective with transform=False.

    The original uses `softmax(raw_probs, beta)` and log(p_actual + 1e-10).
    Observations update last_observed; play trials do not update it.
    """
    if not math.isfinite(beta) or beta < 0 or len(set(reset_days)) != len(reset_days):
        raise ValueError('invalid beta/reset specification')
    prior_action = None
    reset_set = set(reset_days)
    output = []
    for row in trials:
        if row['day'] in reset_set:
            prior_action = None
        chosen = row['chosen']
        available = row['available']
        if row['type'] == 'observe':
            prior_action = chosen
        elif row['type'] == 'play':
            if prior_action is None or prior_action not in available:
                p = 0.5
            else:
                # Author model3: softmax([1,0], beta), pair of available boats.
                prob_match = 1.0 / (1.0 + math.exp(-beta))
                p = prob_match if chosen == prior_action else 1.0 - prob_match
            output.append({'day': row['day'], 'p': p,
                           'nll': -math.log(p + 1e-10),
                           'history_available': prior_action is not None and prior_action in available})
        else:
            raise ValueError('unexpected trial type')
    return output


def summarize(all_trials: list[list[dict]]) -> dict:
    if not all_trials:
        raise ValueError('no sample trials')
    n_play = changed = changed_day89 = day89_author_uniform = 0
    day89_boundary_history = 0
    author_total = boundary_total = day89_author_total = day89_boundary_total = 0.0
    for trials in all_trials:
        source = predict(trials, AUTHOR_RESET)
        corrected = predict(trials, BLOCK_RESET)
        if len(source) != len(corrected):
            raise ValueError('inconsistent play count')
        source_89 = [r for r in source if r['day'] == 89]
        boundary_89 = [r for r in corrected if r['day'] == 89]
        if len(source_89) != 1 or len(boundary_89) != 1:
            raise ValueError('missing day89 play')
        n_play += len(source)
        author_total += sum(r['nll'] for r in source)
        boundary_total += sum(r['nll'] for r in corrected)
        changed += sum(abs(a['p'] - b['p']) > 1e-12 for a, b in zip(source, corrected))
        changed_day89 += int(abs(source_89[0]['p'] - boundary_89[0]['p']) > 1e-12)
        day89_author_total += source_89[0]['nll']
        day89_boundary_total += boundary_89[0]['nll']
        day89_author_uniform += int(abs(source_89[0]['p'] - 0.5) < 1e-12)
        day89_boundary_history += int(boundary_89[0]['history_available'])
    n_sub = len(all_trials)
    return {
        'study': 'R065_PHASE_H',
        'upstream_repository': SOURCE_REPO, 'upstream_commit': SOURCE_COMMIT,
        'upstream_model3_objectives_git_blob': OBJECTIVES_BLOB,
        'upstream_fit_utils_git_blob': FIT_UTILS_BLOB,
        'selected_raw_files_count': n_sub,
        'raw_source_git_blob_sha1_ordered': list(SAMPLE_BLOBS.values()),
        'source_reset_days': list(AUTHOR_RESET),
        'alternative_reset_days': list(BLOCK_RESET),
        'fixed_beta': BETA,
        'number_of_scored_play_trials': n_play,
        'source_model3_total_nll': author_total,
        'alternative_model3_total_nll': boundary_total,
        'source_model3_mean_nll': author_total / n_play,
        'alternative_model3_mean_nll': boundary_total / n_play,
        'alternative_minus_source_mean_nll': (boundary_total - author_total) / n_play,
        'changed_play_probabilities_count': changed,
        'changed_day89_participants': changed_day89,
        'day89_source_uniform_count': day89_author_uniform,
        'day89_alternative_history_available_count': day89_boundary_history,
        'day89_source_mean_nll': day89_author_total / n_sub,
        'day89_alternative_mean_nll': day89_boundary_total / n_sub,
        'day89_alternative_minus_source_nll': (day89_boundary_total - day89_author_total) / n_sub,
        'scope': 'Fixed beta source-equivalent reimplementation on 10 nonrandom author raw trials. NOT native author code or parameter refit, NOT representative causal evidence.',
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-dir', type=Path, required=True,
                    help='directory with ten unmodified upstream raw experiment files')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    trials = [source_trials((args.source_dir / name).read_bytes(), sha)
              for name, sha in SAMPLE_BLOBS.items()]
    result = summarize(trials)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'subjects': len(trials),
                      'play_trials': result['number_of_scored_play_trials']}))


if __name__ == '__main__':
    main()
