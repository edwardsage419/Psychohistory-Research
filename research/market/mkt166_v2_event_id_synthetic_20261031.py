#!/usr/bin/env python3
"""Synthetic mirror of the fixed ActivityWatch v2 merge_events branch.
No external services, real personal data, or native Rust execution.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    id: int | None
    timestamp: int
    payload: str

def merge_events(existing: list[Event], new: list[Event]) -> list[Event]:
    """Model Rust BTreeMap<i64,Event> overwrite and unkeyed Vec append."""
    keyed: dict[int, Event] = {}
    unkeyed: list[Event] = []
    for event in [*existing, *new]:
        if event.id is None:
            unkeyed.append(event)
        else:
            keyed[event.id] = event
    return sorted([*keyed.values(), *unkeyed], key=lambda e: e.timestamp)

def main() -> None:
    checks = 0
    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(label)

    a = Event(1, 100, 'old')
    b = Event(2, 200, 'other')
    revised = Event(1, 100, 'revised')
    merged = merge_events([a, b], [revised])
    check(len(merged) == 2, 'keyed replacement count')
    check(merged[0].payload == 'revised', 'new keyed entry wins')
    check(merged[1] == b, 'unrelated keyed entry retained')
    check(merge_events([a], [a]) == [a], 'same keyed entry idempotent')
    check(merge_events([a], []) == [a], 'empty new list does not delete old')

    no_id = Event(None, 100, 'unkeyed')
    unkeyed_once = merge_events([no_id], [no_id])
    check(len(unkeyed_once) == 2, 'unkeyed repeated event appended')
    check(unkeyed_once[0] == no_id, 'first unkeyed retained')
    check(unkeyed_once[1] == no_id, 'second unkeyed retained')
    repeated = [no_id]
    for i in range(2, 6):
        repeated = merge_events(repeated, [no_id])
        check(len(repeated) == i, f'unkeyed repeated pass {i}')

    reused = Event(1, 300, 'different-event-after-restore')
    collided = merge_events([a], [reused])
    check(len(collided) == 1, 'id reuse collapses keyed entries')
    check(collided[0] == reused, 'later reused id replaces old record')
    check(collided[0] != a, 'old event no longer present in artificial merge')

    same_ts_a = Event(3, 50, 'first')
    same_ts_b = Event(4, 50, 'second')
    equal_ts = merge_events([same_ts_a], [same_ts_b])
    check(len(equal_ts) == 2, 'equal timestamps with different ids retained')
    check({e.id for e in equal_ts} == {3, 4}, 'two ids preserved')
    check(all(e.timestamp == 50 for e in equal_ts), 'equal timestamp preserved')

    print({'status':'PASS', 'assertions':checks, 'keyed_repeat_count':len(merge_events([a],[a])),
           'unkeyed_repeat_count':len(unkeyed_once), 'id_reuse_count':len(collided),
           'evidence':'synthetic_E1_only', 'native_rust':'NOT_RUN'})

if __name__ == '__main__':
    main()
