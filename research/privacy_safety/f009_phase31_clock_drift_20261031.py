#!/usr/bin/env python3
"""Artificial clock drift and authorization expiry policy enumeration."""
from itertools import product
EXPIRY = 1100


def guarded(now, online, fresh, epoch, trusted):
    if trusted and now >= EXPIRY or online and fresh and not epoch:
        return 'REJECT'
    if not trusted or not online or not fresh:
        return 'UNKNOWN'
    return 'REVIEW' if epoch and now < EXPIRY else 'UNKNOWN'


def run():
    counts = dict(REVIEW=0, UNKNOWN=0, REJECT=0)
    n = naive_only = checks = 0
    for drift, now, online, fresh, epoch, trusted in product((-30, 0, 30), (1075, 1100, 1125), (False, True), (False, True), (False, True), (False, True)):
        naive = now + drift <= EXPIRY
        decision = guarded(now, online, fresh, epoch, trusted)
        counts[decision] += 1
        n += naive
        naive_only += naive and decision != 'REVIEW'
        assert decision in counts; checks += 1
        assert decision != 'REVIEW' or now < EXPIRY and all((online, fresh, epoch, trusted)); checks += 1
        assert not (trusted and now >= EXPIRY) or decision == 'REJECT'; checks += 1
        assert not (online and fresh and not epoch) or decision == 'REJECT'; checks += 1
    assert sum(counts.values()) == 144; checks += 1
    for inputs, expected in [((1125, True, True, True, True), 'REJECT'), ((1075, True, True, True, True), 'REVIEW'), ((1075, False, True, True, True), 'UNKNOWN'), ((1075, True, False, True, True), 'UNKNOWN'), ((1075, True, True, True, False), 'UNKNOWN'), ((1075, True, True, False, True), 'REJECT')]:
        assert guarded(*inputs) == expected; checks += 1
    assert 1125 - 30 <= EXPIRY and guarded(1125, True, True, True, True) == 'REJECT'; checks += 1
    print(f'PASS {checks} assertions; 144 states; naive={n}; naive_only={naive_only}; guarded={counts}')


if __name__ == '__main__':
    run()
