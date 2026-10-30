#!/usr/bin/env python3
"""TH166 exact synthetic sensitivity and published denominator arithmetic.

Python standard library only. Synthetic checks do not establish empirical
causal effects or E1/E2/E3 scientific acceptance.
"""
from fractions import Fraction as F


def main():
    zero, one = F(0), F(1)
    baseline = F(1, 2)
    low_effect, high_effect = F(1, 5), -F(1, 10)
    source_weights, target_weights = (F(3, 4), F(1, 4)), (F(1, 4), F(3, 4))

    def average(weights, effects):
        return sum((w * e for w, e in zip(weights, effects)), zero)

    source_ate = average(source_weights, (low_effect, high_effect))
    target_invariant = average(target_weights, (low_effect, high_effect))
    target_changed = average(target_weights, (low_effect, F(1, 5)))
    assert source_ate == F(1, 8)
    assert target_invariant == -F(1, 40)
    assert target_changed == F(1, 5)
    assert all(zero <= baseline + e <= one for e in
               (low_effect, high_effect, F(1, 5)))
    # Target H is unobserved under treatment; bounded Y implies H effect
    # from -1/2 to +1/2, and these endpoints are attainable.
    lower = average(target_weights, (low_effect, -baseline))
    upper = average(target_weights, (low_effect, one - baseline))
    assert (lower, upper) == (-F(13, 40), F(17, 40))
    assert lower <= target_invariant <= upper
    assert lower <= target_changed <= upper

    p_u = {0: F(1, 4), 1: F(3, 4)}

    def observed_mean(a, intercept, tau, gamma):
        return intercept + tau * a + gamma * p_u[a]

    confounded = tuple(observed_mean(a, F(1, 5), -F(1, 10), F(2, 5))
                       for a in (0, 1))
    unconfounded = tuple(observed_mean(a, F(3, 10), F(1, 10), zero)
                         for a in (0, 1))
    assert confounded == unconfounded == (F(3, 10), F(2, 5))
    assert confounded[1] - confounded[0] == F(1, 10)
    # This putative negative control is insensitive to U, and thus invalid
    # as a shared-bias detector in the confounded world.
    assert F(1, 4) - F(1, 4) == zero
    assert zero <= F(1, 5) - F(1, 10) <= one
    assert zero <= F(1, 5) + F(2, 5) <= one

    # Same observed two-group two-period data, different counterfactuals.
    observed = {('treated', 0): F(3, 10), ('treated', 1): F(3, 5),
                ('control', 0): F(3, 10), ('control', 1): F(2, 5)}
    did = (observed['treated', 1] - observed['treated', 0]
           - observed['control', 1] + observed['control', 0])
    assert did == F(1, 5)
    assert observed['treated', 1] - F(2, 5) == F(1, 5)
    assert observed['treated', 1] - F(3, 5) == zero

    # Published author's 2016 manuscript: 112 treated, 139 buffer,
    # 45 controls, 109 previously excluded, and endline households.
    assert 112 + 45 == 157
    assert 112 + 139 + 45 == 296
    assert 296 + 109 == 405
    assert 158 - 157 == 1  # NBER 2014 versus 2016; cause unknown.
    assert 8774 - 295 - 365 == 8114

    print('TH166 exact synthetic and public denominator checks: PASS')
    print('source', source_ate, 'target invariant', target_invariant,
          'target changed', target_changed, 'target bounds', (lower, upper))
    print('observed A group means', confounded,
          'negative control contrast', zero)
    print('DiD', did, 'causal effects under different worlds', F(1, 5), zero)
    print('randomized', 296, 'analyzed', 157, 'version gap', 1)


if __name__ == '__main__':
    main()
