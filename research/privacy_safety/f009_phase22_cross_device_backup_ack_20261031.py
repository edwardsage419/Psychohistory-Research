#!/usr/bin/env python3
"""Exhaustive fictional device and backup deletion-state policy experiment."""
from collections import Counter
from itertools import product

DEVICE = ("ACK", "PENDING", "UNREACHABLE")
BACKUP = ("ERASED", "QUARANTINED", "LIVE")


def policy(devices, backups, restore_requested, legal_hold, authenticated_acks):
    if legal_hold:
        return "REVIEW_LEGAL_BASIS"
    if not authenticated_acks:
        return "VERIFY_ACK_AUTHENTICITY"
    if any(d != "ACK" for d in devices):
        return "PENDING_DEVICE_ACK"
    if any(b == "LIVE" for b in backups):
        return "PENDING_BACKUP_ERASURE"
    if any(b == "QUARANTINED" for b in backups):
        return "RESTRICTED_BACKUP_WAIT"
    if restore_requested:
        return "RESTORE_BLOCKED"
    return "ALL_SCOPED_ACK_CANDIDATE"


def main():
    outcomes = Counter()
    checks = 0
    for devices in product(DEVICE, repeat=3):
        for backups in product(BACKUP, repeat=2):
            for restore_requested, legal_hold, authenticated_acks in product((False, True), repeat=3):
                action = policy(devices, backups, restore_requested, legal_hold, authenticated_acks)
                outcomes[action] += 1
                checks += 1
                if action == "ALL_SCOPED_ACK_CANDIDATE":
                    assert devices == ("ACK",) * 3
                    assert backups == ("ERASED",) * 2
                    assert authenticated_acks and not restore_requested and not legal_hold
                    checks += 3
                if any(b == "LIVE" for b in backups) and not legal_hold and authenticated_acks and devices == ("ACK",) * 3:
                    assert action == "PENDING_BACKUP_ERASURE"
                    checks += 1
                if restore_requested and backups == ("ERASED",) * 2 and devices == ("ACK",) * 3 and authenticated_acks and not legal_hold:
                    assert action == "RESTORE_BLOCKED"
                    checks += 1
    assert sum(outcomes.values()) == 3**3 * 3**2 * 2**3
    checks += 1
    assert outcomes["ALL_SCOPED_ACK_CANDIDATE"] == 1
    checks += 1
    print(f"F009 phase22 SYNTHETIC PASS: {sum(outcomes.values())} states, {checks} assertions")
    for key in sorted(outcomes):
        print(f"{key}: {outcomes[key]}")
    return outcomes


if __name__ == "__main__":
    main()
