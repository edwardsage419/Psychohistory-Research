"""MKT064: standard-library-only synthetic snapshot/replay integrity checks.
This is a model of the documented loading boundary, not execution of eventsource-py.
"""
from dataclasses import dataclass

EVENTS = ((1, 5), (2, 7))

@dataclass(frozen=True)
class Snapshot:
    version: int
    state: int
    schema: int = 1
    branch: str = "A"


def full_replay(events=EVENTS):
    return sum(delta for _, delta in events)


def documented_load(snapshot, events=EVENTS, schema=1):
    """Use matching-schema snapshot, then apply events strictly after its version."""
    if snapshot is None or snapshot.schema != schema:
        return full_replay(events)
    return snapshot.state + sum(delta for version, delta in events if version > snapshot.version)


def candidate_guard(snapshot, events=EVENTS, branch="A", schema=1):
    """Proposed extra guard; not claimed to be implemented upstream."""
    if snapshot is None:
        return True
    versions = tuple(version for version, _ in events)
    return (snapshot.schema == schema and snapshot.branch == branch
            and versions == tuple(range(1, len(events) + 1))
            and 0 <= snapshot.version <= len(events)
            and snapshot.state == sum(delta for version, delta in events
                                      if version <= snapshot.version))


def main():
    cases = {
        "valid": (Snapshot(2, 12), 12, True),
        "premature_uncommitted": (Snapshot(3, 112), 112, False),
        "stale_version": (Snapshot(1, 12), 19, False),
        "same_version_wrong_state": (Snapshot(2, 99), 99, False),
        "different_branch": (Snapshot(2, -8, branch="B"), -8, False),
        "schema_mismatch_fallback": (Snapshot(2, 99, schema=2), 12, False),
    }
    checks = 0
    assert full_replay() == 12; checks += 1
    assert documented_load(None) == 12; checks += 1
    assert candidate_guard(None); checks += 1
    for name, (snapshot, expected_state, accepted) in cases.items():
        actual = documented_load(snapshot)
        assert actual == expected_state, (name, actual, expected_state); checks += 1
        assert candidate_guard(snapshot) == accepted, name; checks += 1
        assert (actual == full_replay()) == (name in {"valid", "schema_mismatch_fallback"}), name; checks += 1
    assert not candidate_guard(Snapshot(2, 12), branch="B"); checks += 1
    assert not candidate_guard(Snapshot(2, 12), events=((1, 5), (3, 7))); checks += 1
    assert candidate_guard(Snapshot(1, 5)); checks += 1
    print(f"MKT064_SYNTHETIC_CHECKS={checks}; FAILURES=0; UPSTREAM_PACKAGE_EXECUTED=NO")
    for name, (snap, _, _) in cases.items():
        print(f"{name}: reconstructed={documented_load(snap)} guard={candidate_guard(snap)}")


if __name__ == "__main__":
    main()
