#!/usr/bin/env python3
"""Synthetic fault-domain dependency audit; no signatures or personal data."""
from itertools import product

# Three nominal providers, but A and B depend on the same root of trust.
WITNESSES = (("A", "root_x"), ("B", "root_x"), ("C", "root_y"))


def naive(valid):
    return sum(valid) >= 2


def guarded(valid, roots_ok, epoch_current, no_revocation):
    if not epoch_current or not no_revocation:
        return False
    domains = {root for (provider, root), is_valid in zip(WITNESSES, valid)
               if is_valid and roots_ok[root]}
    return len(domains) >= 2


def run():
    checks = 0
    naive_count = guarded_count = extra = 0
    for flags in product((False, True), repeat=3):
        for root_x, root_y, epoch_current, no_revocation in product((False, True), repeat=4):
            roots_ok = {"root_x": root_x, "root_y": root_y}
            n = naive(flags)
            g = guarded(flags, roots_ok, epoch_current, no_revocation)
            assert not g or n
            checks += 1
            naive_count += n
            guarded_count += g
            extra += n and not g
    assert checks == 128
    checks += 1
    assert (naive_count, guarded_count, extra) == (64, 3, 61)
    checks += 1
    assert naive((True, True, False))
    checks += 1
    assert not guarded((True, True, False), {"root_x": True, "root_y": True}, True, True)
    checks += 1
    assert guarded((True, False, True), {"root_x": True, "root_y": True}, True, True)
    checks += 1
    assert not guarded((True, False, True), {"root_x": False, "root_y": True}, True, True)
    checks += 1
    print(f"F009 phase28 synthetic states=128 assertions={checks} PASS; naive={naive_count} guarded={guarded_count} extra={extra}")


if __name__ == "__main__":
    run()
