#!/usr/bin/env python3
"""R065 G: exact LOSO M2/M3 scores from anonymized block-by-stake counts.

The result is conditional on supplied aggregated counts. This program does not
validate the original author trial CSV or identify a causal stake effect.
"""
import argparse
import json
import math
from pathlib import Path

SOURCE_BLOB = '01bf211468abe093618dfa5e5c39e883230c9c03'
DAYS = (4, 21, 38, 55, 72, 89, 106, 123)
EXPECTED_N = 226
HIGH_FIRST_N, LOW_FIRST_N = 121, 105


def cell_score(n: int, k: int, prior: float = 4.0) -> tuple[float, float]:
    """Total held-out log-loss and Brier for one sample per subject in cell."""
    if type(n) is not int or type(k) is not int or n < 2 or not 0 <= k <= n:
        raise ValueError('invalid cell n,k')
    if not math.isfinite(prior) or prior <= 0:
        raise ValueError('invalid prior')
    denominator = n - 1 + 2 * prior
    p1 = (k - 1 + prior) / denominator if k else None
    p0 = (k + prior) / denominator if k < n else None
    loss = -k * math.log(p1) if k else 0.0
    if k < n:
        loss -= (n-k) * math.log1p(-p0)
    brier = k * (1-p1)**2 if k else 0.0
    if k < n:
        brier += (n-k) * p0**2
    return loss, brier


def certificate(table: list[dict], prior: float = 4.0) -> dict:
    if len(table) != 8:
        raise ValueError('eight blocks required')
    for j, block in enumerate(table):
        if (block.get('block') != j+1 or block.get('day') != DAYS[j]):
            raise ValueError('block/day order mismatch')
        h, l = block.get('high_n'), block.get('low_n')
        hk, lk = block.get('high_copied'), block.get('low_copied')
        expected_high = HIGH_FIRST_N if j % 2 == 0 else LOW_FIRST_N
        if h != expected_high or l != EXPECTED_N-expected_high:
            raise ValueError('alternating counterbalance design mismatch')
        for n, k in ((h, hk), (l, lk)):
            cell_score(n, k, prior)
    total = sum(x['high_n'] + x['low_n'] for x in table)
    if total != 8 * EXPECTED_N:
        raise ValueError('invalid trial population')
    if sum(x['high_copied'] + x['low_copied'] for x in table) != 684:
        raise ValueError('critical-copying total mismatches original aggregate')
    if table[5]['high_copied'] + table[5]['low_copied'] != 73:
        raise ValueError('day89 copied count mismatch')
    summary = {}
    for name in ('M2', 'M3'):
        subtotal = [0., 0.]
        for x in table:
            cells = [(x['high_n']+x['low_n'], x['high_copied']+x['low_copied'])] if name == 'M2' else [
                (x['high_n'],x['high_copied']), (x['low_n'],x['low_copied'])]
            for n, k in cells:
                score = cell_score(n, k, prior)
                subtotal[0] += score[0]
                subtotal[1] += score[1]
        summary[name] = {'logloss': subtotal[0]/total, 'brier': subtotal[1]/total}
    # In each fixed block the observed stake is determined by counterbalance
    # sequence: high iff first_high == (block number is odd).
    return {
        'source_blob_sha1': SOURCE_BLOB,
        'source_validation_level': 'AGGREGATE_COUNTS_ONLY',
        'n_subjects': EXPECTED_N, 'diagnostic_rows': total,
        'high_first': HIGH_FIRST_N, 'low_first': LOW_FIRST_N,
        'total_copied': 684, 'day89_copied': 73,
        'prior_beta_symmetric': prior, 'scores': summary,
        'M3_minus_M2': {key: summary['M3'][key]-summary['M2'][key] for key in ('logloss','brier')},
        'design_alias': 'At a fixed block, stake label uniquely determines high-first/low-first sequence; M3 cannot isolate stakes from sequence-by-block differences.',
        'not_identified': ['individual-level paired-bootstrap covariance', 'M0/M1 all-subject-out score from marginal cell totals', 'causal stake effects', 'latent cognitive learning strategies']
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cells', required=True, type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--prior', type=float, default=4.0)
    args = p.parse_args()
    input_data = json.loads(args.cells.read_text(encoding='utf-8'))
    if input_data.get('source_blob_sha1') != SOURCE_BLOB:
        raise ValueError('aggregation source identity mismatch')
    r = certificate(input_data['cells'], args.prior)
    rendered = json.dumps(r, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')

if __name__ == '__main__':
    main()
