#!/usr/bin/env python3
"""F009 phase36: synthetic cross-root grant/revoke/rotate/regrant replica safety."""
from itertools import product, permutations
from collections import Counter

EVENTS = (
    (1, 'A', 'GRANT', 'GENESIS'),
    (2, 'A', 'REVOKE', 1),
    (3, 'A+B', 'ROTATE_TO_B', 2),
    (4, 'B', 'REGRANT', 3),
)

def decide(observed, trusted_highwater=4, anchor_ok=True):
    if not anchor_ok or trusted_highwater is None:
        return 'UNKNOWN'
    epochs = [e[0] for e in observed]
    if len(epochs) != len(set(epochs)):
        return 'UNKNOWN'
    if any(e not in EVENTS for e in observed):
        return 'UNKNOWN'
    # A previously observed revocation remains effective until a complete
    # verified successor authorization chain is present.
    if any(e[2] == 'REVOKE' for e in observed) and not all(e in observed for e in EVENTS):
        return 'REJECT'
    if trusted_highwater > 4 or trusted_highwater < 0:
        return 'UNKNOWN'
    if any(e[0] > trusted_highwater for e in observed):
        return 'UNKNOWN'
    if set(observed) != set(EVENTS) or trusted_highwater != 4:
        return 'UNKNOWN'
    return 'REVIEW'  # review only; never automatic authorization

def main():
    subsets = [tuple(EVENTS[i] for i in range(4) if mask & (1 << i)) for mask in range(16)]
    counts = Counter(decide(s) for s in subsets)
    assert counts['REVIEW'] == 1
    assert counts['REJECT'] == 7
    assert counts['UNKNOWN'] == 8
    assert decide((EVENTS[3],)) == 'UNKNOWN'
    assert decide((EVENTS[1], EVENTS[3])) == 'REJECT'
    assert decide(EVENTS, anchor_ok=False) == 'UNKNOWN'
    assert decide(EVENTS, trusted_highwater=3) == 'UNKNOWN'
    assert decide(EVENTS + (EVENTS[3],)) == 'UNKNOWN'
    assert decide(EVENTS[:3]) == 'REJECT'
    for ordering in permutations(EVENTS):
        assert decide(ordering) == 'REVIEW'
    replica_cases = Counter()
    for trio in product(subsets, repeat=3):
        replica_cases[tuple(decide(s) for s in trio)] += 1
    assert sum(replica_cases.values()) == 4096
    assert replica_cases[('REVIEW','REVIEW','REVIEW')] == 1
    print({'single_replica':dict(counts), 'three_replica_combinations':sum(replica_cases.values()),
           'all_three_review':replica_cases[('REVIEW','REVIEW','REVIEW')]})
    print('PASS synthetic controls and 24 complete-order permutations')

if __name__ == '__main__':
    main()
