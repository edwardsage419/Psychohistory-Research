"""MKT128: exact synthetic off-policy overlap and clipping audit; Python stdlib only."""
from fractions import Fraction as F
from itertools import product


def validate(rows):
    if len({r[0] for r in rows}) != len(rows):
        raise ValueError('duplicate stratum')
    for name, p in rows:
        if not isinstance(p, F) or p <= 0 or p > 1:
            raise ValueError('invalid or unsupported propensity')


def moments(rows, cap=None):
    """One independent Bernoulli logged action per equally weighted stratum."""
    validate(rows)
    n = len(rows)
    probs = []
    values = []
    for bits in product((0, 1), repeat=n):
        prob = F(1)
        val = F(0)
        for bit, (_, p) in zip(bits, rows):
            prob *= p if bit else 1 - p
            if bit:
                weight = 1 / p
                val += min(weight, cap) if cap is not None else weight
        probs.append(prob)
        values.append(val / n)
    assert sum(probs) == 1
    mean = sum((p * v for p, v in zip(probs, values)), F(0))
    variance = sum((p * (v - mean)**2 for p, v in zip(probs, values)), F(0))
    return mean, variance, max(values), len(values)


def run():
    rows = [('common', F(1, 2)), ('rare', F(1, 100))]
    ipw = moments(rows)
    clipped = moments(rows, F(10))
    true_value = F(1)  # Both actions B have fixed potential reward 1.
    assert ipw == (F(1), F(25), F(51), 4), ipw
    assert clipped == (F(11, 20), F(199, 400), F(6), 4), clipped
    assert (clipped[0] - true_value)**2 == F(81, 400)
    assert ipw[1] / 200 == F(1, 8)
    assert clipped[1] / 200 + F(81, 400) == F(16399, 80000)
    assert ipw[1] / 20 == F(5, 4)
    assert clipped[1] / 20 + F(81, 400) == F(9095, 40000)
    # Zero support in rare stratum: two latent worlds share all observable logs.
    # The target always chooses B; common-stratum B reward is 1.
    # Rare-stratum B reward can be 0 or 1 without changing observed logs.
    assert (F(1) + F(0)) / 2 == F(1, 2)
    assert (F(1) + F(1)) / 2 == F(1)
    rejected = 0
    for bad in [[('common', F(1, 2)), ('rare', F(0))],
                [('common', F(1, 2)), ('rare', F(101, 100))],
                [('common', F(1, 2)), ('common', F(1, 100))]]:
        try:
            moments(bad)
        except ValueError:
            rejected += 1
    assert rejected == 3
    print('MKT128 PASS: 4 exact logging outcomes, 12 mathematical assertions, 3 rejected malformed controls')
    print('IPW mean, variance, max:', *(str(x) for x in ipw))
    print('CLIP10 mean, variance, max:', *(str(x) for x in clipped))
    print('MSE m=20:', str(ipw[1]/20), str(clipped[1]/20+F(81,400)))
    print('MSE m=200:', str(ipw[1]/200), str(clipped[1]/200+F(81,400)))


if __name__ == '__main__':
    run()
