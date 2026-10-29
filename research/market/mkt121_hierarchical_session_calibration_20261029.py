#!/usr/bin/env python3
"""Exact synthetic preference likelihood and selective calibration. No personal data or dependencies."""
from fractions import Fraction as F
from itertools import product

HIGH = F(9, 10)
LOW = F(1, 2)
P_GOOD = F(1, 2)
P_HIGH_IF_G = {0: F(1, 4), 1: F(3, 4)}
ANSWERS = tuple(product((0, 1), repeat=4))


def likelihood(h, obs, model):
    if model == 'iid':
        p = F(7, 10)
        v = F(1)
        for a in obs:
            v *= p if a == h else 1-p
        return v
    total = F(0)
    if model == 'hierarchical':
        states = [(g, P_GOOD) for g in (0, 1)]
    elif model == 'session_only':
        states = [(None, F(1))]
    elif model == 'global_only':
        states = [(g, P_GOOD) for g in (0, 1)]
    else:
        raise ValueError(model)
    for g, pg in states:
        for q1, q2 in product((0, 1), repeat=2):
            if model == 'global_only' and q1 != q2:
                continue
            if model == 'global_only':
                pq = F(1, 2)
            else:
                ph = F(1, 2) if g is None else P_HIGH_IF_G[g]
                pq = (ph if q1 else 1-ph) * (ph if q2 else 1-ph)
            v = pg * pq
            for a, q in zip(obs, (q1, q1, q2, q2)):
                p = HIGH if q else LOW
                v *= p if a == h else 1-p
            total += v
    return total


def posterior(obs, model):
    a, b = likelihood(0, obs, model), likelihood(1, obs, model)
    return b/(a+b)


def selection(model, threshold):
    covered = wrong = F(0)
    for obs in ANSWERS:
        p1 = posterior(obs, model)
        if max(p1, 1-p1) < threshold:
            continue
        for h in (0, 1):
            mass = F(1, 2) * likelihood(h, obs, 'hierarchical')
            covered += mass
            if h != int(p1 > F(1, 2)):
                wrong += mass
    return covered, wrong/covered if covered else None


def run():
    checks = 0
    def verify(cond, label):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(label)
    models = ('hierarchical', 'session_only', 'global_only', 'iid')
    for m in models:
        for h in (0, 1):
            verify(sum((likelihood(h, obs, m) for obs in ANSWERS), F(0)) == 1, f'{m} normalization')
            for obs in ANSWERS:
                verify(likelihood(h, obs, m) == likelihood(1-h, tuple(1-x for x in obs), m), f'{m} label symmetry')
        for obs in ANSWERS:
            verify(posterior(obs, m) + posterior(tuple(1-x for x in obs), m) == 1, f'{m} posterior symmetry')
    verify(posterior((1,)*4, 'iid') == F(2401, 2482), 'iid anchor')
    for m in models:
        for t in (F(3,4), F(4,5), F(9,10), F(19,20)):
            cover, err = selection(m, t)
            verify(F(0) <= cover <= 1, 'coverage bounds')
            verify(err is None if cover == 0 else F(0) <= err <= 1, 'error bounds')
    for bad in ((0, 1, 2, 0), (0, 1), (0, 0, 0, -1)):
        verify(bad not in ANSWERS, 'invalid response rejected')
    print(f'PASS: {checks} exact checks; no stochastic simulation')
    for obs in ((1,1,1,1), (1,1,0,0), (1,0,1,0), (1,1,1,0)):
        print('obs', ''.join(map(str,obs)), ' '.join(f'{m}:{posterior(obs,m)}={float(posterior(obs,m)):.6f}' for m in models))
    for t in (F(3,4), F(4,5), F(9,10), F(19,20)):
        print('threshold',t, ' '.join(f'{m}:cover={selection(m,t)[0]} err={selection(m,t)[1]}' for m in models))

if __name__ == '__main__':
    run()
