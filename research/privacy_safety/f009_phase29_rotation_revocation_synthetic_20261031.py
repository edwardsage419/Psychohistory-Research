#!/usr/bin/env python3
"""Synthetic trust-root rotation review gate. No real keys or user data."""
from itertools import product


def classify(key_epoch, current_epoch, key_status, receipt_version, current_version,
             timestamp_verified, invalidity_before_issue, signature_verified):
    if not signature_verified:
        return 'REJECT'
    if key_status == 'compromised' and invalidity_before_issue:
        return 'REJECT'
    if key_status == 'unknown':
        return 'UNKNOWN'
    if not timestamp_verified:
        return 'UNKNOWN'
    if receipt_version != current_version:
        return 'HISTORICAL_ONLY'
    if key_epoch != current_epoch:
        return 'HISTORICAL_ONLY' if key_status == 'rotated' else 'UNKNOWN'
    if key_status != 'active':
        return 'UNKNOWN'
    return 'ELIGIBLE_FOR_HUMAN_REVIEW'


def audit():
    statuses = {}
    checks = 0
    for epoch, status, version, timestamp, invalidity, signature in product(
        (1, 2), ('active', 'rotated', 'compromised', 'unknown'),
        (1, 2), (False, True), (False, True), (False, True)
    ):
        result = classify(epoch, 2, status, version, 2, timestamp, invalidity, signature)
        statuses[result] = statuses.get(result, 0) + 1
        checks += 1
        assert result in {'REJECT', 'UNKNOWN', 'HISTORICAL_ONLY', 'ELIGIBLE_FOR_HUMAN_REVIEW'}
        if not signature or (status == 'compromised' and invalidity):
            checks += 1
            assert result == 'REJECT'
        if result == 'ELIGIBLE_FOR_HUMAN_REVIEW':
            checks += 1
            assert epoch == 2 and status == 'active' and version == 2 and timestamp and signature
        if epoch == 1 and result == 'ELIGIBLE_FOR_HUMAN_REVIEW':
            raise AssertionError('stale epoch must not authorize current action')
    checks += 1
    assert sum(statuses.values()) == 128
    checks += 1
    assert classify(1, 2, 'rotated', 2, 2, True, False, True) == 'HISTORICAL_ONLY'
    checks += 1
    assert classify(1, 2, 'compromised', 2, 2, True, True, True) == 'REJECT'
    checks += 1
    assert classify(2, 2, 'active', 2, 2, False, False, True) == 'UNKNOWN'
    return checks, statuses

if __name__ == '__main__':
    n, counts = audit()
    print(f'F009 phase29 synthetic checks PASS: {n}; status counts: {counts}')
