#!/usr/bin/env python3
"""Bounded E1 illustration of ActivityWatch duplicate device identity and resume ordering.
This is a synthetic model, not execution of upstream Rust.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Remote:
    device_id: str
    hostname: str
    file_bytes: int
    events: tuple[int, ...]


def resume_from_latest(destination, source):
    """Simplified monotonic event-time resume, intentionally omits historical backfill."""
    latest = max(destination, default=-1)
    return tuple(sorted(set(destination) | {t for t in source if t > latest}))


def choose_largest(remotes):
    selected = {}
    for remote in remotes:
        old = selected.get(remote.device_id)
        if old is None or remote.file_bytes > old.file_bytes:
            selected[remote.device_id] = remote
    return selected


def run():
    short = Remote('devA', 'old hostname', 10, (6, 7))
    full = Remote('devA', 'new hostname', 100, tuple(range(1, 9)))
    first_short = resume_from_latest(resume_from_latest((), short.events), full.events)
    first_full = resume_from_latest(resume_from_latest((), full.events), short.events)
    assert first_short == (6, 7, 8)
    assert first_full == full.events
    assert first_short != first_full
    assert len(full.events) - len(first_short) == 5
    assert choose_largest((short, full))['devA'] == full
    assert choose_largest((full, short))['devA'] == full
    assert len(choose_largest((short, full))) == 1

    # File size is only a heuristic for coverage; a larger recent-only DB
    # can omit an older, smaller DB's unique events.
    recent_large = Remote('devB', 'recent', 100, (6, 7, 8))
    older_small = Remote('devB', 'older', 10, (1, 2, 3, 4, 5))
    selected = choose_largest((older_small, recent_large))['devB']
    assert selected == recent_large
    assert set(older_small.events).isdisjoint(selected.events)
    assert len(set(older_small.events) - set(selected.events)) == 5
    assert len(set(older_small.events) | set(selected.events)) == 8
    assert len(selected.events) == 3
    assert selected.file_bytes > older_small.file_bytes
    return dict(assertions=13, old_short_first=list(first_short), old_full_first=list(first_full),
                chosen_full=choose_largest((short, full))['devA'].hostname,
                counterexample_larger_recent_only=list(selected.events),
                unique_older_omitted=5, evidence='synthetic_E1_only')


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, ensure_ascii=False))
