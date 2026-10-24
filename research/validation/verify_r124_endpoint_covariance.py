#!/usr/bin/env python3
"""R124 independent exact Pearson endpoint-covariance audit, E1 only."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research' / 'R124'
BLOBS = {
    'r124_homophily_baseline_assortativity_causal_ambiguity.py': '382859d6dcf55201e316a12da276d0ab04514842',
    'test_r124_homophily_baseline_assortativity_causal_ambiguity.py': '652d43c34852e08bccdd0b083d2119c0c06d5ea3',
    'R124_FIRSTPARTY_HOMOPHILY_NEWMan_2003_BASELINE_OPPORTUNITY_SYNTHETIC_IDENTIFICATION_REPORT_2026-10-19.md': '99bc82d03045ec90f2719272280b1ef10d7d738f',
}
FIELDS = ('n', 'edge_bits', 'label_bits', 'labels', 'edge_count',
          'pearson_r', 'original_newman_r', 'status')


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def check_sources(expected=BLOBS):
    for name, sha in expected.items():
        if blob_sha((SOURCE / name).read_bytes()) != sha:
            raise AssertionError('SOURCE_BLOB_MISMATCH ' + name)


def pearson_r(labels, edges):
    """Independent binary Pearson correlation of two oriented edge endpoints."""
    if not edges:
        return None, 'EMPTY_GRAPH'
    m = len(edges)
    p = F(sum(int(labels[u] == 'A') + int(labels[v] == 'A')
              for u, v in edges), 2 * m)
    variance = p * (1 - p)
    if variance == 0:
        return None, 'UNDEFINED_SINGLE_ENDPOINT_CATEGORY'
    xy = F(sum(labels[u] == labels[v] == 'A' for u, v in edges), m)
    return (xy - p*p) / variance, 'DEFINED'


def controls():
    labels = ('A','A','A','B','B','B')
    triangles = tuple(combinations(range(3),2)) + tuple(combinations(range(3,6),2))
    k33 = tuple((u,v) for u in range(3) for v in range(3,6))
    k6 = tuple(combinations(range(6),2))
    assert pearson_r(labels, triangles) == (F(1), 'DEFINED')
    assert pearson_r(labels, k33) == (F(-1), 'DEFINED')
    assert pearson_r(('A',)*5+('B',), k6) == (F(-1,5), 'DEFINED')
    assert pearson_r(('A','A','B'), ((0,1),)) == (None, 'UNDEFINED_SINGLE_ENDPOINT_CATEGORY')
    assert pearson_r(('A','B'), ()) == (None, 'EMPTY_GRAPH')
    global_baseline = F(3*2+3*2, 6*5)
    focal_baseline = F(sum(labels[u]==labels[v] for u,v in triangles),len(triangles))
    assert (global_baseline, focal_baseline) == (F(2,5), F(1))
    return 6


def render(verify_original=False):
    original = None
    if verify_original:
        sys.path.insert(0, str(SOURCE))
        import r124_homophily_baseline_assortativity_causal_ambiguity as original
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    totals = {2:0, 3:0, 4:0}
    nonempty = 0
    empty = 0
    undefined = 0
    for n in (2,3,4):
        pairs = tuple(combinations(range(n),2))
        for bits in range(1 << len(pairs)):
            edges = tuple(pair for i,pair in enumerate(pairs) if bits & (1<<i))
            for labels in product(('A','B'), repeat=n):
                if set(labels) != {'A','B'}:
                    continue
                totals[n] += 1
                result, status = pearson_r(labels,edges)
                if not edges:
                    empty += 1
                else:
                    nonempty += 1
                if status == 'UNDEFINED_SINGLE_ENDPOINT_CATEGORY':
                    undefined += 1
                if original is not None and edges:
                    reference = original.newman_mixing_direct(n,labels,edges)['assortativity']
                    if reference != result:
                        raise AssertionError(f'R124_COVARIANCE_MISMATCH n={n} bits={bits} labels={labels}')
                else:
                    reference = result
                label_bits = sum((1<<i) for i,v in enumerate(labels) if v=='B')
                writer.writerow({'n':n,'edge_bits':bits,'label_bits':label_bits,
                                 'labels':''.join(labels),'edge_count':len(edges),
                                 'pearson_r':'NA' if result is None else str(result),
                                 'original_newman_r':'NA' if reference is None else str(reference),
                                 'status':status})
    assert totals == {2:4,3:48,4:896} and nonempty==926 and empty==22
    return out.getvalue().encode('utf-8'), totals, nonempty, empty, undefined


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.verify:
        check_sources()
    raw, totals, nonempty, empty, undefined = render(args.verify)
    controls_count = controls()
    path = Path(args.output)
    if args.verify:
        assert path.read_bytes() == raw, 'RAW_CSV_BYTE_MISMATCH'
        assert path.read_bytes()+b'X' != raw, 'CSV_TAMPER_REJECTION_FAILED'
        fake = dict(BLOBS)
        fake['r124_homophily_baseline_assortativity_causal_ambiguity.py'] = '0'*40
        try:
            check_sources(fake)
        except AssertionError as exc:
            assert 'SOURCE_BLOB_MISMATCH' in str(exc)
        else:
            raise AssertionError('FALSE_SOURCE_BLOB_REJECTION_FAILED')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    print(f'R124_AUDIT_PASS total={sum(totals.values())} nonempty={nonempty} '
          f'empty={empty} undefined_nonempty={undefined} controls={controls_count} '
          f'csv_sha256={hashlib.sha256(raw).hexdigest()} verify={args.verify}')


if __name__=='__main__':
    main()
