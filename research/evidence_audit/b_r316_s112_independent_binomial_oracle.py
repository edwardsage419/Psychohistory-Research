#!/usr/bin/env python3
"""Independent nonblind R316 S112 oracle. No import of R scorer or R316 module."""
import copy
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research/R316/R316_EXACT_128_GRAPH_LIKELIHOODS.json'
RECEIPT = ROOT / 'research/validation/R316_S112_OBSERVATION_COARSENING_EXACT.json'
SOURCE_BLOB = '36da587adbc6e1d92824a5fd39516e506569166c'
FREEZE = 'af948405bc682f10cdf6f3add73ab2f35e10c0b4'
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
BLOCKS = (0, 0, 1, 1)
REGIMES = (('A', Fraction(3, 4), Fraction(1, 4)), ('D', Fraction(1, 4), Fraction(3, 4)))
MAPS = ('full', 'within_cross', 'signed_difference', 'within_only', 'cross_only', 'total_only')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def observed(name, w, c, mask):
    return {'full': mask, 'within_cross': (w, c), 'signed_difference': w-c,
            'within_only': w, 'cross_only': c, 'total_only': w+c}[name]


def verify_source(source):
    require(source['schema'] == 'r316_sbm_known_block_4node_all_graphs_exact_E1_v1', 'schema')
    require(source['source_scope'] == 'SYNTHETIC_EXACT_E1_ONLY' and source['original_catalogue_id'] == '04-019', 'source scope')
    require(source['fixed_blocks'] == list(BLOCKS) and source['dyads'] == [list(p) for p in PAIRS], 'block/dyad identity')
    require(source['source_atom_count'] == 768 and source['graph_count'] == 128, 'source count')
    require(len(source['regimes']) == 2, 'regime count')
    for i, (name, pw, pc) in enumerate(REGIMES):
        r = source['regimes'][i]
        require(r['regime'] == name and Fraction(r['within_p']) == pw and Fraction(r['cross_p']) == pc, 'regime parameters')
        require(len(r['complete_graphs']) == 64, 'graph coverage')
        seen = set()
        total = Fraction(0)
        for g in r['complete_graphs']:
            m = g['mask']
            require(type(m) is int and 0 <= m < 64 and m not in seen, 'unique mask')
            seen.add(m)
            bits = tuple(int(ch) for ch in f'{m:06b}')
            w = bits[0] + bits[5]
            c = sum(bits[1:5])
            require(g['edge_vector'] == ''.join(map(str, bits)) and g['within_edges'] == w and g['cross_edges'] == c, 'edge identity')
            q = Fraction(1)
            for j, (u, v) in enumerate(PAIRS):
                p = pw if BLOCKS[u] == BLOCKS[v] else pc
                q *= p if bits[j] else 1-p
            require(Fraction(g['probability']) == q, 'original source probability')
            total += q
        require(seen == set(range(64)) and total == 1, 'full coverage/normalization')


def oracle():
    # Independent count-based binomial derivation, not an aggregation of source probabilities.
    masses = {name: defaultdict(lambda: [Fraction(0), Fraction(0)]) for name in MAPS}
    for regime_idx, (_, pw, pc) in enumerate(REGIMES):
        for w in range(3):
            for c in range(5):
                individual = pw**w * (1-pw)**(2-w) * pc**c * (1-pc)**(4-c)
                multiplicity = comb(2, w) * comb(4, c)
                for name in MAPS:
                    if name == 'full':
                        # A full labeled graph is one bin, repeated once per graph with these counts.
                        for mask in range(64):
                            bits = tuple(int(x) for x in f'{mask:06b}')
                            if bits[0] + bits[5] == w and sum(bits[1:5]) == c:
                                masses[name][mask][regime_idx] += individual
                    else:
                        masses[name][observed(name, w, c, 0)][regime_idx] += multiplicity * individual
    result = {}
    for name, bins in masses.items():
        require(sum(v[0] for v in bins.values()) == sum(v[1] for v in bins.values()) == 1, 'oracle normalization')
        accuracy = sum((max(v) for v in bins.values()), Fraction(0)) / 2
        tv = sum((abs(v[0]-v[1]) for v in bins.values()), Fraction(0)) / 2
        require(accuracy == (1 + tv)/2, 'Bayes identity')
        result[name] = {'bins': len(bins), 'accuracy': str(accuracy), 'total_variation': str(tv)}
    return {'schema': 'r316_s112_equal_prior_observation_coarsening_E1_v1',
            'source_blob_sha1': SOURCE_BLOB, 'freeze_commit': FREEZE,
            'evidence_grade': 'E1_SYNTHETIC_ONLY', 'graph_count': 128,
            'observations': result}


def verify(source, receipt):
    verify_source(source)
    require(receipt == oracle(), 'independent oracle receipt mismatch')


def mutations(source, receipt):
    tests = []
    def attempt(label, change):
        s, r = copy.deepcopy(source), copy.deepcopy(receipt)
        change(s, r)
        try:
            verify(s, r)
        except (ValueError, KeyError, TypeError, IndexError):
            tests.append(label)
            return
        raise RuntimeError('MUTATION ACCEPTED: ' + label)
    attempt('duplicate_mask', lambda s, r: s['regimes'][0]['complete_graphs'][1].update(mask=0))
    attempt('missing_mask', lambda s, r: s['regimes'][0]['complete_graphs'].pop())
    attempt('wrong_edge_vector', lambda s, r: s['regimes'][0]['complete_graphs'][33].update(edge_vector='000000'))
    attempt('wrong_likelihood', lambda s, r: s['regimes'][0]['complete_graphs'][33].update(probability='1/4096'))
    attempt('wrong_within_count', lambda s, r: s['regimes'][0]['complete_graphs'][33].update(within_edges=1))
    attempt('false_source_scope', lambda s, r: s.update(source_scope='HUMAN_E2'))
    attempt('wrong_accuracy', lambda s, r: r['observations']['total_only'].update(accuracy='1/2'))
    attempt('false_E2_upgrade', lambda s, r: r.update(evidence_grade='E2_HUMAN'))
    return tests


def main():
    raw = SOURCE.read_bytes()
    sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(sha == SOURCE_BLOB, 'source Git blob mismatch')
    source = json.loads(raw)
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    verify(source, receipt)
    passed = mutations(source, receipt)
    print(json.dumps({'status':'PASS','route':'nonblind_independent_binomial',
        'source_blob_sha1':sha,'graphs':128,'observation_maps':6,
        'mutations_rejected':len(passed),'mutation_names':passed,
        'evidence':'E1_ONLY','E2':0,'E3':0}, sort_keys=True))


if __name__ == '__main__':
    main()
