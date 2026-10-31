#!/usr/bin/env python3
"""Artificial offline revocation and replay policy enumeration, no real credentials."""
from itertools import product

# All values are artificial. Epochs are not cryptographically authenticated.
def naive_accept(offline: bool, cached_receipt: bool, signature_valid: bool,
                 revocation_delivered: bool, version_current: bool,
                 witness_current: bool) -> bool:
    return cached_receipt and signature_valid

def guarded_status(offline: bool, cached_receipt: bool, signature_valid: bool,
                   revocation_delivered: bool, version_current: bool,
                   witness_current: bool) -> str:
    if not signature_valid:
        return 'REJECT'
    if not cached_receipt:
        return 'UNKNOWN'
    if offline or not revocation_delivered or not version_current or not witness_current:
        return 'UNKNOWN'
    return 'ELIGIBLE_FOR_HUMAN_REVIEW'

def main() -> None:
    counts = {'REJECT':0,'UNKNOWN':0,'ELIGIBLE_FOR_HUMAN_REVIEW':0}
    accepted_naive = 0
    false_ready = 0
    checks = 0
    for args in product((False,True), repeat=6):
        offline, cached, sig, delivered, current, witness = args
        status = guarded_status(*args)
        counts[status] += 1
        naive = naive_accept(*args)
        accepted_naive += naive
        false_ready += naive and status != 'ELIGIBLE_FOR_HUMAN_REVIEW'
        checks += 1
        assert status in counts
        checks += 1
        assert (status == 'ELIGIBLE_FOR_HUMAN_REVIEW') == (
            cached and sig and not offline and delivered and current and witness)
        checks += 1
        assert not (status == 'ELIGIBLE_FOR_HUMAN_REVIEW' and offline)
    assert sum(counts.values()) == 64
    checks += 1
    assert accepted_naive == 16
    checks += 1
    assert counts['ELIGIBLE_FOR_HUMAN_REVIEW'] == 1
    checks += 1
    assert false_ready == 15
    checks += 1
    assert guarded_status(True,True,True,False,True,True) == 'UNKNOWN'
    checks += 1
    assert guarded_status(False,True,True,True,False,True) == 'UNKNOWN'
    checks += 1
    assert guarded_status(False,True,False,True,True,True) == 'REJECT'
    checks += 1
    print({'status':'PASS','states':64,'assertions':checks,'naive_accepted':accepted_naive,
           'guarded':counts,'naive_extra':false_ready,'evidence':'synthetic_E1_only',
           'real_signature_validation':'NOT_RUN'})

if __name__ == '__main__':
    main()
