#!/usr/bin/env python3
"""Synthetic E1 policy grid for lost high-water anchor and backup restoration.
No cryptography, actual device validation, or legal erasure assertion.
"""
from collections import Counter
from itertools import product


def decide(anchor, tombstone, ack_a, ack_b, backup, witness):
    values = (tombstone, ack_a, ack_b, backup)
    if anchor is None:
        # Even two independently authenticated witnesses would need human
        # reconciliation before claiming irreversible deletion.
        return 'REVIEW_ONLY' if witness == 'quorum_epoch3' and values == (3, 3, 3, 3) else 'UNKNOWN'
    if any(v < anchor for v in values):
        return 'REJECT_STALE'
    if any(v > anchor for v in values):
        return 'UNKNOWN_ANCHOR_CONFLICT'
    return 'ELIGIBLE_REVIEW' if anchor == 3 and values == (3, 3, 3, 3) else 'UNKNOWN_LOW_ANCHOR'


def run():
    counts = Counter()
    for anchor, tombstone, a, b, backup, witness in product(
            (None, 2, 3), (2, 3), (2, 3), (2, 3), (2, 3),
            ('none', 'quorum_epoch3', 'conflicting')):
        result = decide(anchor, tombstone, a, b, backup, witness)
        counts[result] += 1
        assert result != 'ELIGIBLE_REVIEW' or (anchor == 3 and (tombstone, a, b, backup) == (3, 3, 3, 3))
        assert anchor is not None or result in ('UNKNOWN', 'REVIEW_ONLY')
    assert sum(counts.values()) == 144
    assert decide(None, 3, 3, 3, 3, 'none') == 'UNKNOWN'
    assert decide(None, 3, 3, 3, 3, 'quorum_epoch3') == 'REVIEW_ONLY'
    assert decide(3, 2, 2, 2, 2, 'quorum_epoch3') == 'REJECT_STALE'
    assert decide(2, 2, 2, 2, 2, 'none') == 'UNKNOWN_LOW_ANCHOR'
    assert decide(3, 3, 3, 3, 3, 'none') == 'ELIGIBLE_REVIEW'
    assert counts['ELIGIBLE_REVIEW'] == 3  # witness state does not alter trusted-anchor result
    assert counts['REVIEW_ONLY'] == 1
    return dict(states=144, assertions=296, counts=dict(sorted(counts.items())),
                evidence='synthetic_E1_only', anchor_trust='assumed_not_verified')


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, ensure_ascii=False))
