"""R142 h=0 third-method exact payoff matrix factorization; no external dependencies."""
import json
from fractions import Fraction as F
from math import prod

THETAS = (-2, -1, 0, 1, 2)
KAPPAS = (F(3, 4), F(99, 100), F(1), F(101, 100), F(5, 4))


def payoff(theta, kappa, own, other):
    return F(0) if own == 0 else F(theta) - kappa + 2 * other


def equilibria(theta, kappa, strict=False):
    result = []
    for a in (0, 1):
        for b in (0, 1):
            own = payoff(theta, kappa, a, b)
            other = payoff(theta, kappa, b, a)
            gain_a = payoff(theta, kappa, 1 - a, b) - own
            gain_b = payoff(theta, kappa, 1 - b, a) - other
            if (gain_a < 0 and gain_b < 0) if strict else (gain_a <= 0 and gain_b <= 0):
                result.append([a, b])
    return result


def main():
    rows = []
    for kappa in KAPPAS:
        states = [{'theta': theta, 'pure_ne': equilibria(theta, kappa),
                   'strict_pure_ne': equilibria(theta, kappa, True)} for theta in THETAS]
        counts = [len(x['pure_ne']) for x in states]
        rows.append({'kappa': str(kappa), 'states': states, 'local_ne_counts': counts,
                     'global_h0_pure_bne': prod(counts)})
    lookup = {r['kappa']: r for r in rows}
    assert [lookup[k]['global_h0_pure_bne'] for k in ('3/4', '1', '5/4')] == [4, 8, 4]
    assert lookup['99/100']['global_h0_pure_bne'] == 4
    assert lookup['101/100']['global_h0_pure_bne'] == 4
    assert len(equilibria(-1, F(1))) == 2
    assert len(equilibria(1, F(1))) == 2
    assert len(equilibria(0, F(3, 4))) == 2
    # At kappa=1, weak pure NE must not be discarded as strict-NE failures.
    weak_vs_strict = [(s['theta'], len(s['pure_ne']), len(s['strict_pure_ne']))
                      for s in lookup['1']['states']]
    assert any(p > q for _, p, q in weak_vs_strict)
    print(json.dumps({'research': 'R142', 'scope': 'h0 E1 finite exact',
                      'rows': rows, 'kappa_1_weak_vs_strict': weak_vs_strict,
                      'new_E2': 0, 'new_E3': 0}, indent=2))


if __name__ == '__main__':
    main()
