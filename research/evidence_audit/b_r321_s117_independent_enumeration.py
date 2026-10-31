#!/usr/bin/env python3
"""Independent E1 exact counterfactual audit of R321 S117. No original generator imports."""
import itertools
import json
from fractions import Fraction as Q

PAIRS = ((Q(1, 4), Q(3, 4)), (Q(1, 3), Q(2, 3)))

def audit():
    results = []
    for p0, p1 in PAIRS:
        for k in (2, 3):
            for truth in ('H0', 'H1'):
                p = p0 if truth == 'H0' else p1
                d = {key: Q(0) for key in ('S_H0', 'S_H1', 'F_H0', 'F_H1', 'S_error', 'F_error', 'disagree', 'disagree_early', 'disagree_censored', 'observed_steps', 'A_censor', 'A_error', 'A_decided')}
                for bits in itertools.product((0, 1), repeat=7):
                    mass = p ** sum(bits) * (1-p) ** (7-sum(bits))
                    score, stop, a = 0, 7, None
                    for t, bit in enumerate(bits, 1):
                        score += 2*bit-1
                        if abs(score) >= k:
                            stop, a = t, ('H1' if score > 0 else 'H0')
                            break
                    fixed = 'H1' if sum(bits) >= 4 else 'H0'
                    seq = a or fixed
                    d['S_'+seq] += mass
                    d['F_'+fixed] += mass
                    d['S_error'] += mass * (seq != truth)
                    d['F_error'] += mass * (fixed != truth)
                    d['observed_steps'] += mass * stop
                    if seq != fixed:
                        d['disagree'] += mass
                        d['disagree_early' if a else 'disagree_censored'] += mass
                    if a is None:
                        d['A_censor'] += mass
                    else:
                        d['A_decided'] += mass
                        d['A_error'] += mass * (a != truth)
                assert d['S_H0']+d['S_H1'] == d['F_H0']+d['F_H1'] == 1
                assert d['disagree_censored'] == 0
                results.append(dict(world_id=len(results), p0=str(p0), p1=str(p1), K=k, truth=truth, source_paths=128,
                                    **{name:str(value) for name,value in d.items()},
                                    S_minus_F_error=str(d['S_error']-d['F_error']),
                                    A_conditional_error=str(d['A_error']/d['A_decided'])))
    return results

if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
