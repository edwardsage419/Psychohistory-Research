#!/usr/bin/env python3
"""MKT122. Exact synthetic repeated-session split audit; Python standard library only.

Each session has a private latent binary label repeated four times. The session ID
has no predictive meaning for a new session. The memorizer uses labels from seen
sessions and predicts zero for an unseen session. No real user data are used.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product

N_SESSIONS = 16
N_REPLIES = 4
ROWS = tuple((session, reply, session % 2)
             for session in range(N_SESSIONS)
             for reply in range(N_REPLIES))


def train_memorizer(rows):
    memory = {}
    for session, _reply, label in rows:
        if session in memory and memory[session] != label:
            raise ValueError('conflicting labels within a session')
        memory[session] = label
    return memory


def predict(memory, session):
    return memory.get(session, 0)


def assess(train, test):
    memory = train_memorizer(train)
    errors = sum(predict(memory, s) != y for s, _r, y in test)
    overlap = set(s for s, _, _ in train) & set(s for s, _, _ in test)
    return F(errors, len(test)), len(overlap), len(memory)


def run():
    checks = 0
    def check(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(label)

    check(len(ROWS) == 64, '64 artificial replies')
    check(len(set((s, r) for s, r, _ in ROWS)) == 64, 'unique reply keys')
    check(Counter(y for _, _, y in ROWS) == {0: 32, 1: 32}, 'balanced labels')
    check(all(len([1 for s, _, _ in ROWS if s == g]) == 4 for g in range(16)), 'four replies per session')

    row_scores = []
    group_scores = []
    for fold in range(4):
        # Row-wise split deliberately leaks each session into both partitions.
        row_train = tuple(row for row in ROWS if row[1] != fold)
        row_test = tuple(row for row in ROWS if row[1] == fold)
        row_error, row_overlap, _ = assess(row_train, row_test)
        check(len(row_train) == 48 and len(row_test) == 16, 'row fold sizes')
        check(row_overlap == 16, 'row fold has all sessions overlapping')
        check(row_error == 0, 'memorization looks perfect with row split')
        row_scores.append(row_error)

        # Group split evaluates new sessions with no shared session identifiers.
        group_train = tuple(row for row in ROWS if (row[0] // 2) % 4 != fold)
        group_test = tuple(row for row in ROWS if (row[0] // 2) % 4 == fold)
        group_error, group_overlap, _ = assess(group_train, group_test)
        check(len(group_train) == 48 and len(group_test) == 16, 'group fold sizes')
        check(group_overlap == 0, 'no group overlap')
        check(group_error == F(1, 2), 'unseen session error is one half')
        group_scores.append(group_error)

    # Conditional on one reply being held out, each other reply is independently
    # in training with probability 1/2. Exactly one of eight masks has no train.
    other_masks = tuple(product((0, 1), repeat=3))
    check(len(other_masks) == 8, 'eight masks for other three replies')
    no_train = sum(not any(mask) for mask in other_masks)
    check(no_train == 1, 'one mask has no training sibling')
    # For balanced session labels, fallback zero errs in half the unseen groups.
    expected_error = F(no_train, 8) * F(1, 2)
    check(expected_error == F(1, 16), 'expected independent row split error')
    check(1 - expected_error == F(15, 16), 'expected accuracy 93.75%')

    # Negative controls: enforce grouped split and reject mixed-session split.
    row_train = tuple(row for row in ROWS if row[1] != 0)
    row_test = tuple(row for row in ROWS if row[1] == 0)
    group_train = tuple(row for row in ROWS if (row[0] // 2) % 4 != 0)
    group_test = tuple(row for row in ROWS if (row[0] // 2) % 4 == 0)
    def enforce_disjoint(train, test):
        overlap = {s for s, _, _ in train} & {s for s, _, _ in test}
        if overlap:
            raise ValueError(f'group leakage: {len(overlap)} overlapping sessions')
    try:
        enforce_disjoint(row_train, row_test)
    except ValueError:
        rejected = True
    else:
        rejected = False
    check(rejected, 'overlapping sessions rejected')
    enforce_disjoint(group_train, group_test)
    check(True, 'grouped partition accepted')
    # Deliberate training-label conflict must fail instead of silently overwriting.
    try:
        train_memorizer(((0, 0, 0), (0, 1, 1)))
    except ValueError:
        rejected = True
    else:
        rejected = False
    check(rejected, 'conflicting session label rejected')
    check(sum(row_scores, F(0)) == 0, 'four row folds error zero')
    check(sum(group_scores, F(0)) / 4 == F(1, 2), 'four grouped folds error one half')

    print(f'PASS checks={checks}; synthetic sessions={N_SESSIONS}; replies={len(ROWS)}')
    print('row_fold_errors=' + ','.join(map(str, row_scores)))
    print('group_fold_errors=' + ','.join(map(str, group_scores)))
    print(f'row_fold_mean_accuracy={1-sum(row_scores,F(0))/4}')
    print(f'group_fold_mean_accuracy={1-sum(group_scores,F(0))/4}')
    print(f'independent_random_row_split_expected_accuracy={1-expected_error}')
    print('negative_controls=2 rejected; no real data; no external model trained')

if __name__ == '__main__':
    run()
