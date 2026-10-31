#!/usr/bin/env python3
"""F009 phase37: synthetic revoked-root migration evidence gate.

REVIEW is human review eligibility only, never permission to perform an action.
All roots, signatures, timestamps and approvals are fictional booleans.
"""
from itertools import product
from collections import Counter

STATUSES = ("ACTIVE", "REVOKED", "UNKNOWN")
TIMINGS = ("BEFORE", "AFTER", "UNVERIFIED")


def strict(status, timing, trusted_time, independent_recovery,
           new_root_signature, complete_chain, high_watermark, old_grant_cached):
    if status == "REVOKED" and (timing == "AFTER" or old_grant_cached):
        return "REJECT"
    if (status == "UNKNOWN" or timing != "BEFORE" or not trusted_time
            or not independent_recovery or not new_root_signature
            or not complete_chain or not high_watermark or old_grant_cached):
        return "UNKNOWN"
    return "REVIEW"


def permissive(status, timing, trusted_time, independent_recovery,
               new_root_signature, complete_chain, high_watermark, old_grant_cached):
    return new_root_signature and complete_chain


def check(condition, message):
    if not condition:
        raise ValueError(message)


def run():
    counts = Counter()
    loose_accepted = 0
    unsafe_loose = 0
    for args in product(STATUSES, TIMINGS, (False, True), (False, True),
                        (False, True), (False, True), (False, True), (False, True)):
        decision = strict(*args)
        counts[decision] += 1
        if permissive(*args):
            loose_accepted += 1
            unsafe_loose += decision != "REVIEW"
        if decision == "REVIEW":
            check(args[1] == "BEFORE" and all(args[2:7]) and not args[7], "review evidence")
            check(args[0] in ("ACTIVE", "REVOKED"), "review root")
    check(sum(counts.values()) == 576, "coverage")
    check(counts["REVIEW"] == 2, "review count")
    check(loose_accepted == 144, "loose count")
    check(unsafe_loose == 142, "loose extra")
    check(strict("REVOKED", "AFTER", True, True, True, True, True, False) == "REJECT", "revoked late")
    check(strict("REVOKED", "BEFORE", True, True, True, True, True, True) == "REJECT", "cached old")
    check(strict("UNKNOWN", "BEFORE", True, True, True, True, True, False) == "UNKNOWN", "unknown root")
    check(strict("REVOKED", "BEFORE", True, True, True, True, True, False) == "REVIEW", "revoked historical review")
    check(strict("ACTIVE", "BEFORE", False, True, True, True, True, False) == "UNKNOWN", "time unknown")
    print("F009 PHASE37 PASS", dict(sorted(counts.items())),
          "permissive_accept", loose_accepted,
          "permissive_without_review_eligibility", unsafe_loose)


if __name__ == "__main__":
    run()
