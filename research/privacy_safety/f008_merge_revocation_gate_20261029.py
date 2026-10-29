#!/usr/bin/env python3
"""F008: illustrative CRDT merge-policy and revocation-gate model.
This does not execute Automerge or establish physical erasure.
"""
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Event:
    op: str
    epoch: int
    payload: str = ''


def candidate_merge(a, b, winner='a'):
    """Only the two documented conflict cases are modeled."""
    assert a.op in ('set', 'delete') and b.op in ('set', 'delete')
    if a.op == 'delete' and b.op == 'set':
        return b, (a, b)
    if a.op == 'set' and b.op == 'delete':
        return a, (a, b)
    if a.op == 'delete' and b.op == 'delete':
        return a, (a, b)
    return (a if winner == 'a' else b), (a, b)


def can_use(event, authoritative_epoch, grant_active):
    return (grant_active and event.op == 'set'
            and event.epoch == authoritative_epoch)


def run():
    n = 0
    stale = Event('set', 7, 'old-derived-data')
    deletion = Event('delete', 8)
    # Concurrent deletion and stale edit: documented merge rules retain edit.
    for x, y in ((deletion, stale), (stale, deletion)):
        result, retained = candidate_merge(x, y)
        assert result == stale; n += 1
        assert stale in retained; n += 1
        assert not can_use(result, 8, False); n += 1
        assert not can_use(result, 9, True); n += 1
    # Concurrent updates: visible winner is not an authorization decision.
    new = Event('set', 8, 'concurrent-value')
    for winner in ('a', 'b'):
        result, conflicts = candidate_merge(stale, new, winner)
        assert len(conflicts) == 2; n += 1
        assert stale in conflicts and new in conflicts; n += 1
        assert not can_use(result, 8, False); n += 1
        assert not can_use(stale, 8, True); n += 1
    # Regrant at epoch 9 does not authorize old data from epochs 7 or 8.
    fresh = Event('set', 9, 'newly-authorized')
    for event in (stale, new):
        assert not can_use(event, 9, True); n += 1
    assert can_use(fresh, 9, True); n += 1
    assert not can_use(fresh, 9, False); n += 1
    # A displayed empty document is insufficient to prove historical erasure.
    storage = {'visible': None, 'conflict_history': [stale], 'offline_copy': [stale]}
    assert storage['visible'] is None; n += 1
    assert len(storage['conflict_history']) > 0; n += 1
    assert len(storage['offline_copy']) > 0; n += 1
    assert not (not storage['conflict_history'] and not storage['offline_copy']); n += 1
    print(json.dumps({'research_id':'F008_PHASE3','scope':'SYNTHETIC_POLICY_ONLY',
      'checks_passed':n,'failures':0,'automerge_library_executed':False,
      'physical_erasure_verified':False,'new_E2':0,'new_E3':0},indent=2))


if __name__=='__main__':
    run()
