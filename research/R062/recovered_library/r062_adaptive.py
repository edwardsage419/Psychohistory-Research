#!/usr/bin/env python3
"""R062 replay: reliability-gated VS compared with frozen R061 RW/VS.

Author-original task1.csv/task2.csv required for raw replay. Git blob SHA1 is
verified by inherited fail-closed parser. Data are never bundled here.

Do not interpret private-Q agreement as ground-truth demonstrator reliability.
"""
import argparse
import json
import math
from collections import defaultdict, Counter
from pathlib import Path
import r061_replay_frozen as old

SOURCE = old.SOURCE
GRID = old.GRID
CATEGORIES = old.CATEGORIES
GATE_THRESHOLD = 0.10


def parse_data(data: bytes, task: int, check_provenance=True):
    return old.parse_data(data, task, check_provenance)


def score_subject(sessions, params, mode='adaptive', gate_threshold=GATE_THRESHOLD):
    """Predict private choice before own outcome; demo reward never observed.

    Qpriv is updated ONLY after own reward. The reliability beta posterior is
    judged against Qpriv (no self-reinforcing demonstrator evidence).
    Crucially, gating and Q updates do not consult skill labels or future cgb.
    """
    if mode not in ('rw', 'fixed', 'adaptive'):
        raise ValueError('Unknown family')
    ap, beta, kappa, eta = params
    total = n = brier = 0.0
    strata = {k: [0.0, 0, 0.0] for k in CATEGORIES}
    diagnostics = Counter()
    for _, events in sorted(sessions.items()):
        Q = {}
        private_Q = {}
        prev = {}
        reliabilities = {}
        n_private = {}
        for e in events:
            state = e['state']; chosen = e['choice']; other = 1 - chosen
            if state not in Q:
                Q[state] = [0.0, 0.0]
                private_Q[state] = [0.0, 0.0]
                reliabilities[state] = [1, 1]
                n_private[state] = 0
            q = Q[state]
            qp = private_Q[state]
            counts = reliabilities[state]
            if e['demo']:
                if mode != 'rw':
                    gate = 1.0 if mode == 'fixed' else counts[0] / (counts[0] + counts[1])
                    social_rate = eta * gate
                    q[chosen] += social_rate * (1 - q[chosen])
                    q[other] += social_rate * (-1 - q[other])
                    diagnostics['rate_sum'] += social_rate
                    diagnostics['gates'] += 1
                if mode == 'adaptive':
                    # Independent evaluator: ONLY privately rewarded learning.
                    if n_private[state] > 0 and abs(qp[1] - qp[0]) >= gate_threshold:
                        favored = int(qp[1] > qp[0])
                        counts[int(chosen != favored)] += 1 # 0=good, 1=bad
                        diagnostics['updates'] += 1
                    else:
                        diagnostics['skips'] += 1
                continue
            last = prev.get(state)
            signed = 0 if last is None else (1 if last == 1 else -1)
            logit = beta * (q[1] - q[0] + kappa * signed)
            loss = old.softplus(-logit if chosen == 1 else logit)
            prob = 1 / (1 + math.exp(-logit))
            brier_i = (chosen - prob) ** 2
            total += loss
            brier += brier_i
            n += 1
            category = ('private' if e['condition'] == 'Private' else
                        'skilled' if e['skill'] == 'skilled.dem' else 'unskilled')
            row = strata[category]
            row[0] += loss; row[1] += 1; row[2] += brier_i
            reward = e['out']
            q[chosen] += ap * (reward - q[chosen])
            q[other] += ap * (-reward - q[other])
            qp[chosen] += ap * (reward - qp[chosen])
            qp[other] += ap * (-reward - qp[other])
            n_private[state] += 1
            prev[state] = chosen
    if n < 1:
        raise ValueError('No private outcomes')
    return {'loss': total / n, 'brier': brier / n, 'n': n,
            'strata': strata, 'diagnostics': dict(diagnostics)}


def cross_validate(people):
    """All sessions for held-out subject are excluded from hyperparam selection."""
    ids = sorted(people, key=lambda x: int(x))
    scores = {}
    for sid in ids:
        scores[sid] = {
            'rw': [score_subject(people[sid], grid, 'rw') if grid[3] == 0 else None for grid in GRID],
            'fixed': [score_subject(people[sid], grid, 'fixed') for grid in GRID],
            'adaptive': [score_subject(people[sid], grid, 'adaptive') for grid in GRID],
        }
    result = []
    for held in ids:
        row = {'id': held}
        for family in ('rw', 'fixed', 'adaptive'):
            eligible = [j for j, score in enumerate(scores[held][family]) if score is not None]
            ix = min(eligible, key=lambda j: sum(scores[other][family][j]['loss'] for other in ids if other != held))
            row[family] = {**scores[held][family][ix], 'params': GRID[ix]}
        result.append(row)
    return result


def summarize(task, cv):
    output = {'task': task, 'sha': SOURCE[task]['sha'], 'participants': len(cv),
              'observations': sum(z['rw']['n'] for z in cv), 'models': {}, 'strata': {}}
    for fam in ('rw', 'fixed', 'adaptive'):
        output['models'][fam] = {
            'logloss': sum(z[fam]['loss'] for z in cv) / len(cv),
            'brier': sum(z[fam]['brier'] for z in cv) / len(cv),
            'params': dict(Counter(str(z[fam]['params']) for z in cv)),
        }
    for cat in CATEGORIES:
        out = {'n': sum(z['rw']['strata'][cat][1] for z in cv)}
        for fam in ('rw', 'fixed', 'adaptive'):
            out[f'{fam}_logloss'] = sum(z[fam]['strata'][cat][0] for z in cv) / out['n'] if out['n'] else None
            out[f'{fam}_brier'] = sum(z[fam]['strata'][cat][2] for z in cv) / out['n'] if out['n'] else None
        output['strata'][cat] = out
    output['adaptive_better_than_rw'] = sum(z['adaptive']['loss'] < z['rw']['loss'] - 1e-12 for z in cv)
    output['adaptive_better_than_fixed'] = sum(z['adaptive']['loss'] < z['fixed']['loss'] - 1e-12 for z in cv)
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task1', type=Path, required=True)
    p.add_argument('--task2', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    result = []
    for task, filepath in ((1, a.task1), (2, a.task2)):
        people, checks = parse_data(filepath.read_bytes(), task, True)
        cv = cross_validate(people)
        result.append({'summary': summarize(task, cv), 'checks': checks,
                       'people': cv})
    a.out.write_text(json.dumps({'provenance': 'AUTHOR_RAW_LOCAL_VERIFIED',
                                 'results': result}, indent=2, ensure_ascii=False) + '\n', encoding='utf8')
    print(json.dumps([z['summary'] for z in result], ensure_ascii=False))

if __name__ == '__main__':
    main()