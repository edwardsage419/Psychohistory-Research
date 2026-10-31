#!/usr/bin/env python3
"""Synthetic identity and history-backfill checks. No ActivityWatch runtime is imported."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Replica:
    device_id: str
    bucket: str
    display_name: str
    file_bytes: int
    event_ids: frozenset[int]


def choose_largest_by_device(replicas):
    selected = {}
    for replica in replicas:
        if replica.device_id not in selected or replica.file_bytes > selected[replica.device_id].file_bytes:
            selected[replica.device_id] = replica
    return selected


def resume_from_newest(destination, source):
    cursor = max(destination, default=-1)
    return destination | {event for event in source if event > cursor}


def proposed_backfill(destination, sources, expected_device, expected_bucket):
    """Research-only full-identity union; event IDs assumed stable and genuine."""
    if any(s.device_id != expected_device or s.bucket != expected_bucket for s in sources):
        raise ValueError("source provenance mismatch")
    result = set(destination)
    for source in sources:
        result.update(source.event_ids)
    return result


def audit():
    checks = 0
    def ck(value, message):
        nonlocal checks
        checks += 1
        assert value, message

    short = Replica('device_A', 'watcher', 'Office Phone', 90, frozenset({6, 7, 8}))
    long = Replica('device_A', 'watcher', 'office_phone', 300, frozenset(range(1, 9)))
    picked = choose_largest_by_device([short, long])
    ck(len(picked) == 1, 'same-device dedupe')
    ck(picked['device_A'] == long, 'larger selected')
    ck(picked == choose_largest_by_device([long, short]), 'order independent')
    old = resume_from_newest({7, 8}, long.event_ids)
    ck(old == {7, 8}, 'newest cursor misses historical prefix')
    fixed = proposed_backfill({7, 8}, [long], 'device_A', 'watcher')
    ck(fixed == set(range(1, 9)), 'prefix backfill')
    ck(fixed - old == set(range(1, 7)), 'six missing old events')

    # File size is not a historical-coverage certificate.
    recent_big = Replica('device_A', 'watcher', 'office_phone', 400, frozenset({6, 7, 8}))
    old_small = Replica('device_A', 'watcher', 'Office Phone', 100, frozenset({1, 2, 3, 4, 5}))
    ck(choose_largest_by_device([recent_big, old_small])['device_A'] == recent_big, 'size winner')
    ck(proposed_backfill(set(), [recent_big], 'device_A', 'watcher') == {6, 7, 8}, 'winner missing prefix')
    ck(proposed_backfill(set(), [recent_big, old_small], 'device_A', 'watcher') == set(range(1, 9)), 'two verified replicas union')

    # Equal first and last timestamps still permit an interior hole.
    interior = {1, 2, 4, 5}
    ck((min(interior), max(interior)) == (1, 5), 'same range endpoints')
    ck(3 not in interior, 'interior gap')
    ck(proposed_backfill(interior, [Replica('device_A', 'watcher', 'Office Phone', 100, frozenset({1, 2, 3, 4, 5}))], 'device_A', 'watcher') == set(range(1, 6)), 'interior recovered')

    # Similar display names across distinct device IDs are never provenance evidence.
    other = Replica('device_B', 'watcher', 'office_phone', 500, frozenset({9}))
    ck(len(choose_largest_by_device([long, other])) == 2, 'distinct devices retained')
    ck(long.display_name.lower().replace(' ', '_') == other.display_name, 'name alias collision')
    try:
        proposed_backfill(set(), [long, other], 'device_A', 'watcher')
    except ValueError:
        checks += 1
    else:
        raise AssertionError('different-device merge must reject')
    try:
        proposed_backfill(set(), [Replica('device_A', 'other', 'Office Phone', 100, frozenset({10}))], 'device_A', 'watcher')
    except ValueError:
        checks += 1
    else:
        raise AssertionError('different-bucket merge must reject')

    ck(proposed_backfill({1, 2}, [long, long], 'device_A', 'watcher') == set(range(1, 9)), 'duplicate source idempotent')
    ck(resume_from_newest(set(), {1, 2}) == {1, 2}, 'empty destination')
    ck(resume_from_newest({1, 3}, {1, 2, 3}) == {1, 3}, 'interior not repaired by cursor')
    ck(proposed_backfill({1, 3}, [long], 'device_A', 'watcher') == set(range(1, 9)), 'interior repaired')
    return checks

if __name__ == '__main__':
    print(f'MKT165 synthetic checks PASS: {audit()}')
