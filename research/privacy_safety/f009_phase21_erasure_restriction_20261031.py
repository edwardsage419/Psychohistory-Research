"""Finite fictional request-state audit. Not a legal compliance implementation."""
from itertools import product
from collections import Counter


def decide(verified, erase, restrict, legal_hold, review, backup):
    if not verified:
        return 'VERIFY_IDENTITY'
    if erase and restrict:
        if review == 'approve_restrict':
            return 'RESTRICT_PROCESSING'
        if review == 'approve_erase' and not legal_hold:
            return 'ERASURE_PENDING_BACKUP' if backup else 'ERASE_ELIGIBLE'
        return 'CONFLICT_HUMAN_REVIEW'
    if restrict:
        return 'RESTRICT_PROCESSING'
    if erase:
        if legal_hold:
            return 'LEGAL_BASIS_REVIEW'
        return 'ERASURE_PENDING_BACKUP' if backup else 'ERASE_ELIGIBLE'
    return 'NO_REQUEST'


def run():
    checks = 0
    counts = Counter()
    for verified, erase, restrict, legal_hold, review, backup in product(
        (False, True), (False, True), (False, True), (False, True),
        ('none', 'approve_erase', 'approve_restrict'), (False, True)
    ):
        outcome = decide(verified, erase, restrict, legal_hold, review, backup)
        counts[outcome] += 1
        assert outcome in {
            'VERIFY_IDENTITY','RESTRICT_PROCESSING','ERASURE_PENDING_BACKUP',
            'ERASE_ELIGIBLE','CONFLICT_HUMAN_REVIEW','LEGAL_BASIS_REVIEW','NO_REQUEST'
        }
        checks += 1
        if not verified:
            assert outcome == 'VERIFY_IDENTITY'
            checks += 1
        if outcome == 'ERASE_ELIGIBLE':
            assert verified and erase and not legal_hold and not backup
            checks += 1
        if outcome == 'ERASURE_PENDING_BACKUP':
            assert verified and erase and not legal_hold and backup
            checks += 1
        if verified and erase and restrict and review == 'none':
            assert outcome == 'CONFLICT_HUMAN_REVIEW'
            checks += 1
        if verified and erase and legal_hold and not restrict:
            assert outcome == 'LEGAL_BASIS_REVIEW'
            checks += 1
        if outcome == 'RESTRICT_PROCESSING':
            assert verified and restrict
            checks += 1
    assert sum(counts.values()) == 96
    checks += 1
    print(f'F009_PHASE21_SYNTHETIC_PASS checks={checks} states=96 outcomes={dict(sorted(counts.items()))}')


if __name__ == '__main__':
    run()
