#!/usr/bin/env python3
"""Synthetic E1 gate for erasure proof and alias recovery authorization."""
from itertools import product
from collections import Counter

def gate(stale_backup, valid_tombstone, valid_alias, independent_approval, owner_notice, old_key_revoked):
    if not stale_backup:
        return 'NO_RESTORE_NEEDED'
    if not valid_tombstone or not valid_alias:
        return 'UNKNOWN_QUARANTINE'
    if not independent_approval or not owner_notice or not old_key_revoked:
        return 'REJECT_PENDING_AUTHORIZATION'
    return 'REVIEW_ONLY'

counts = Counter(gate(*bits) for bits in product((False,True), repeat=6))
assert sum(counts.values()) == 64
assert counts['NO_RESTORE_NEEDED'] == 32
assert counts['REVIEW_ONLY'] == 1
assert counts['UNKNOWN_QUARANTINE'] == 24
assert counts['REJECT_PENDING_AUTHORIZATION'] == 7
assert gate(True,False,True,True,True,True) == 'UNKNOWN_QUARANTINE'
assert gate(True,True,True,False,True,True) == 'REJECT_PENDING_AUTHORIZATION'
assert gate(True,True,True,True,True,True) == 'REVIEW_ONLY'
assert 'AUTO_ALLOW' not in counts
print({'states':64,'counts':dict(sorted(counts.items())),'assertions':8,'status':'PASS'})
