#!/usr/bin/env python3
"""F009 phase35: purely synthetic revocation ordering and restore model.
No real cryptographic signatures, identities, devices, or network access.
"""
from dataclasses import dataclass, field
from itertools import permutations, product
from copy import deepcopy
import json

@dataclass(frozen=True)
class Event:
    epoch: int
    kind: str
    parent: int
    token: str

CHAIN = (
    Event(1, "GRANT", 0, "a1"),
    Event(2, "REVOKE", 1, "r2"),
    Event(3, "GRANT", 2, "a3"),
)

@dataclass
class Replica:
    events: dict = field(default_factory=dict)
    conflict: bool = False
    trusted_high_water: int | None = 0

    def ingest(self, event: Event):
        if event.epoch < 1 or event.kind not in ("GRANT", "REVOKE"):
            self.conflict = True
            return
        previous = self.events.get(event.epoch)
        if previous is not None and previous != event:
            self.conflict = True
        else:
            self.events[event.epoch] = event

    def restore(self, backup: dict, trusted_high_water: int | None):
        self.events = deepcopy(backup)
        self.trusted_high_water = trusted_high_water
        self.conflict = False

    def decision(self):
        if self.conflict or self.trusted_high_water is None:
            return "UNKNOWN"
        if not self.events:
            return "UNKNOWN"
        top = max(self.events)
        if top < self.trusted_high_water:
            return "UNKNOWN"
        if set(self.events) != set(range(1, top + 1)):
            return "UNKNOWN"
        for epoch in range(1, top + 1):
            event = self.events[epoch]
            if event.parent != epoch - 1:
                return "UNKNOWN"
        # In a real system, signatures, legal authority and chain hashes must be checked.
        return "REVIEW" if self.events[top].kind == "GRANT" else "REJECT"


def run():
    assertions = 0
    def ck(condition, msg):
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(msg)

    # A naive last-arrival-wins cache can undo an earlier revocation.
    naive = "UNKNOWN"
    for event in (CHAIN[0], CHAIN[1], CHAIN[0]):
        naive = "REVIEW" if event.kind == "GRANT" else "REJECT"
    ck(naive == "REVIEW", "naive stale grant replay demonstration")

    # All six delivery permutations converge with a complete, internally consistent chain.
    outcomes = {"REVIEW": 0, "UNKNOWN": 0, "REJECT": 0}
    for triple in product(permutations(CHAIN), repeat=3):
        replicas = [Replica() for _ in range(3)]
        for replica, order in zip(replicas, triple):
            for event in order:
                replica.ingest(event)
            ck(replica.decision() == "REVIEW", "complete chain must converge")
        outcomes[replicas[0].decision()] += 1
    ck(outcomes == {"REVIEW": 216, "UNKNOWN": 0, "REJECT": 0}, "permutation count")

    # Missing intermediate revocation must prevent epoch-3 regrant from being accepted.
    partial = Replica()
    partial.ingest(CHAIN[0]); partial.ingest(CHAIN[2])
    ck(partial.decision() == "UNKNOWN", "missing intermediate revocation")
    partial.ingest(CHAIN[1]); ck(partial.decision() == "REVIEW", "recovered chain")

    revoked = Replica()
    revoked.ingest(CHAIN[0]); revoked.ingest(CHAIN[1]);
    ck(revoked.decision() == "REJECT", "latest revoke")
    revoked.ingest(CHAIN[0]); ck(revoked.decision() == "REJECT", "stale grant replay")

    # Equal-epoch divergent events require explicit dispute handling.
    conflicting = Replica()
    for event in CHAIN: conflicting.ingest(event)
    conflicting.ingest(Event(2, "GRANT", 1, "forged"))
    ck(conflicting.decision() == "UNKNOWN", "same-epoch conflicting event")

    # Trusted independent high-water mark prevents a restored old backup being accepted.
    rollback = Replica()
    rollback.restore({1: CHAIN[0]}, trusted_high_water=3)
    ck(rollback.decision() == "UNKNOWN", "rollback below trusted high-water")
    rollback.restore({1: CHAIN[0]}, trusted_high_water=None)
    ck(rollback.decision() == "UNKNOWN", "lost independent anchor")
    rollback.restore({1: CHAIN[0]}, trusted_high_water=0)
    ck(rollback.decision() == "REVIEW", "unanchored old snapshot can appear valid")

    # Out-of-order arrivals without a valid chain never authorize the final grant.
    broken = Replica()
    broken.ingest(CHAIN[0]); broken.ingest(CHAIN[1]); broken.ingest(Event(3, "GRANT", 1, "badparent"))
    ck(broken.decision() == "UNKNOWN", "broken parent chain")
    print(json.dumps({"status": "PASS", "synthetic_permutation_cases": 216,
                      "replica_decisions_checked": 648, "assertions": assertions,
                      "all_complete_chains": outcomes, "new_E2": 0, "new_E3": 0}, ensure_ascii=False))

if __name__ == "__main__":
    run()
