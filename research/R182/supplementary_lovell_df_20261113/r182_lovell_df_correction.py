#!/usr/bin/env python3
"""R182 postscore mathematical audit of FWL residualization inference denominators.

All records are artificial, regenerated from the original 2026-10-21 frozen design.
No modification of the frozen data, protocols, or original accepted results.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict, Counter
import json

DESIGNS = {
    "BALANCED": (2, 2, 2, 2),
    "POSITIVE": (4, 2, 2, 4),
    "NEGATIVE": (2, 4, 4, 2),
    "STRONG_POSITIVE": (6, 2, 2, 6),
}
# Index order (x,z) = (0,0), (0,1), (1,0), (1,1).
CELLS = ((0, 0), (0, 1), (1, 0), (1, 1))
A_VALUES = (F(0), F(1))
B_VALUES = (F(1, 4), F(1, 2))
C_VALUES = (F(-2), F(-1), F(0), F(1), F(2))
E_VALUES = (F(0), F(1, 4), F(1, 2))


def make_rows(counts, a, b, c, e):
    rows = []
    for (x, z), count in zip(CELLS, counts):
        if count <= 0 or count % 2:
            raise ValueError('cell counts must be positive and even')
        for j in range(count):
            eps = e if j % 2 == 0 else -e
            rows.append((F(x), F(z), a + b*x + c*z + eps))
    return rows


def residualized_slope_and_sse(rows):
    # Actual rowwise FWL computation using each z-group mean, no full OLS solver.
    by_z = defaultdict(list)
    for x, z, y in rows:
        by_z[z].append((x, y))
    means = {}
    for z, rr in by_z.items():
        n = len(rr)
        means[z] = (sum((r[0] for r in rr), F(0))/n,
                    sum((r[1] for r in rr), F(0))/n)
    residuals = [(x - means[z][0], y - means[z][1]) for x,z,y in rows]
    sxx = sum((rx * rx for rx, _ in residuals), F(0))
    if sxx == 0:
        raise ValueError('singular FWL design')
    beta = sum((rx * ry for rx,ry in residuals), F(0))/sxx
    SSE = sum(((ry-beta*rx)**2 for rx,ry in residuals), F(0))
    return beta, SSE, sxx


def independent_cell_sxx(counts):
    # Grouped-cell identity, separate from rowwise FWL residuals.
    n00, n01, n10, n11 = counts
    return F(n00*n10, n00+n10) + F(n01*n11, n01+n11)


def one_world(counts, a, b, c, e):
    rows = make_rows(counts, a, b, c, e)
    beta, sse, sxx = residualized_slope_and_sse(rows)
    n = len(rows)
    if not (beta == b and sse == n*e*e and sxx == independent_cell_sxx(counts)):
        raise ArithmeticError('full FWL coefficient / SSE / Sxx discrepancy')
    # Univariate, no-intercept OLS of residualized_y ~ residualized_x takes n-1 df.
    # Full original y ~ 1+x+z uses n-3 df. Both have exactly the same SSE, Sxx.
    full_df, naive_df = n-3, n-1
    true_full_se2 = sse/F(full_df*sxx)
    naive_se2 = sse/F(naive_df*sxx)
    if true_full_se2 != naive_se2 * F(naive_df,full_df):
        raise ArithmeticError('standard error correction mismatch')
    return {'N': n, 'Sxx': sxx, 'beta_x': beta, 'SSE': sse,
            'full_df': full_df, 'naive_df': naive_df,
            'corrected_se_squared': true_full_se2,
            'naive_se_squared': naive_se2,
            'naive_over_corrected_se_squared': (F(full_df,naive_df) if sse>0 else None)}


def calculate():
    total = 0
    stochastic_pos = 0
    deterministic_zero = 0
    examples = {}
    frequencies = Counter()
    for design, counts in DESIGNS.items():
        for a,b,c,e in product(A_VALUES,B_VALUES,C_VALUES,E_VALUES):
            res = one_world(counts,a,b,c,e)
            total += 1
            frequencies[design] += 1
            if res['SSE']==0:
                if e != 0 or res['naive_over_corrected_se_squared'] is not None:
                    raise ArithmeticError('zero-residual case mishandled')
                deterministic_zero += 1
            else:
                stochastic_pos += 1
            if a==0 and b==F(1,4) and c==-2 and e==F(1,4):
                examples[design] = {key: str(res[key]) for key in
                    ('N','Sxx','beta_x','SSE','full_df','naive_df',
                     'corrected_se_squared','naive_se_squared',
                     'naive_over_corrected_se_squared')}
    if total != 240 or stochastic_pos != 160 or deterministic_zero != 80:
        raise ArithmeticError('world totals mismatch')
    return {
        'source': 'R182 prescore frozen 2026-10-21 artificial count and coefficient grids',
        'primary_reference': 'Lovell (1963) JASA 58:993-1010, sect.4 Eq.(4.5); Cowles 1963 discussion pp32-33 Eq.(5.10)',
        'scope': 'postscore independent E1 degrees-of-freedom arithmetic, no inference validity claim',
        'worlds': total,
        'artificial_rows_total': sum(sum(counts)*60 for counts in DESIGNS.values()),
        'worlds_nonzero_residual': stochastic_pos,
        'worlds_zero_residual_undefined_se_ratio': deterministic_zero,
        'worlds_per_design': dict(frequencies),
        'correction': 'full_se^2 = naive_se^2 * (N-1)/(N-3)',
        'full_design_rank': 3,
        'naive_residualized_design_rank': 1,
        'fixed_artificial_world_cases': examples,
        'R073': 'FROZEN', 'PESEN_v0_1':'FROZEN',
        'real_behavior_E2_added': 0, 'external_history_E3_added': 0,
    }

if __name__ == '__main__':
    print(json.dumps(calculate(),ensure_ascii=False,indent=2,sort_keys=True))
