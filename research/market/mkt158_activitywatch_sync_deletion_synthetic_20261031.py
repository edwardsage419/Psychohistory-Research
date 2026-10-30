#!/usr/bin/env python3
"""Finite synthetic ActivityWatch-like sync experiment. No ActivityWatch import or data."""
from copy import deepcopy


def pull(owner_snapshot, replica):
    """Model documented event-copy behavior without deletion propagation."""
    for event_id, value in owner_snapshot.items():
        replica[event_id] = value
    return replica


def correction_allowed(age_days):
    """Illustrative seven-day destination-cursor boundary, not upstream code."""
    return age_days <= 7


def main():
    checks = 0
    owner = {"evt-1": {"duration": 30, "label": "fictional-work"}}
    desktop = {}
    pull(owner, desktop)
    assert "evt-1" in desktop
    checks += 1

    # Deletion on owner is not a deletion command on the replica.
    del owner["evt-1"]
    pull(owner, desktop)
    assert "evt-1" not in owner and "evt-1" in desktop
    checks += 1

    # A stale copy can reappear if blindly restored into an empty owner.
    owner.clear()
    pull(deepcopy(desktop), owner)
    assert "evt-1" in owner
    checks += 1

    # An explicit tombstone, held outside old snapshots, can guard restore.
    tombstones = {"evt-1"}
    safe_restored = {k: v for k, v in desktop.items() if k not in tombstones}
    assert safe_restored == {}
    checks += 1

    # A timestamp cursor may prevent older corrections from being reconciled.
    for age in range(15):
        assert correction_allowed(age) == (age <= 7)
        checks += 1
    assert correction_allowed(7) and not correction_allowed(8)
    checks += 1

    # A destination with two copies retains both unless deduplication runs.
    copies = [(100, 30, "fictional-work"), (100, 30, "fictional-work")]
    assert len(copies) == 2
    checks += 1
    assert len(set(copies)) == 1
    checks += 1

    # Equal observable event tuples need not imply equal underlying events.
    distinct_event_ids = {"evt-A", "evt-B"}
    assert len(distinct_event_ids) == 2 and len(set(copies)) == 1
    checks += 1

    print(f"MKT158 SYNTHETIC PASS: {checks} assertions; stale replica and restore demonstrated")
    return checks


if __name__ == "__main__":
    main()
