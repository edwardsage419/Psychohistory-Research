#!/usr/bin/env python3
"""Synthetic common-mode witness failure gate for F009 phase27.
No user data, network access, cryptographic keys, or paid services.
"""
import itertools
import json

STATES = ('fresh', 'stale', 'unknown')
DOMAINS = ('provider_A', 'provider_A', 'provider_B')

def naive(status):
    return sum(x == 'fresh' for x in status) >= 2

def strict(status, revoked, epoch_current):
    if revoked or not epoch_current:
        return False
    domains = {domain for domain, state in zip(DOMAINS, status) if state == 'fresh'}
    return len(domains) >= 2

def main():
    counts = {'states': 0, 'naive_accept': 0, 'strict_accept': 0,
              'naive_only': 0, 'strict_outside_naive': 0}
    for status, revoked, epoch_current in itertools.product(
            itertools.product(STATES, repeat=3), (False, True), (False, True)):
        counts['states'] += 1
        n = naive(status)
        s = strict(status, revoked, epoch_current)
        counts['naive_accept'] += int(n)
        counts['strict_accept'] += int(s)
        counts['naive_only'] += int(n and not s)
        counts['strict_outside_naive'] += int(s and not n)
        assert not s or (not revoked and epoch_current)
        assert not s or ('fresh' in status[:2] and status[2] == 'fresh')
    assert counts == {'states':108,'naive_accept':28,'strict_accept':5,
                      'naive_only':23,'strict_outside_naive':0}
    assert naive(('fresh','fresh','unknown'))
    assert not strict(('fresh','fresh','unknown'),False,True)
    assert strict(('fresh','unknown','fresh'),False,True)
    assert not strict(('fresh','unknown','fresh'),True,True)
    assert not strict(('fresh','unknown','fresh'),False,False)
    print(json.dumps({'model':'three witness IDs; two share provider_A',
                      'candidate_gate':'two distinct provider domains plus current epoch and no revocation',
                      **counts,'scope':'synthetic E1; provider independence and signatures assumed, not verified'},indent=2))

if __name__ == '__main__':main()
