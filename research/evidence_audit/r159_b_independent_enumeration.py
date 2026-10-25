"""Independent R159 E1 audit: eight explicit demonstrator triples, Fraction only."""
from fractions import Fraction as F
from itertools import product
import json

P0 = (F(1, 4), F(2, 5), F(3, 5), F(3, 4))
H = (F(0), F(1, 4), F(1, 2), F(1))
U = (F(0), F(1, 10), F(1, 4))


def three_demo(p):
    total = F(0)
    for triple in product((0, 1), repeat=3):
        count = sum(triple)
        if count >= 2:
            probability = F(1)
            for choice in triple:
                probability *= p if choice else 1-p
            total += probability
    return total


def next_frequency(p, h, u):
    # Independent sample enumeration; never calls the polynomial R159 map.
    social = three_demo(p)
    return (1-u) * ((1-h)*p + h*social) + u/2


def audit():
    cases = []
    transition_checks = 0
    polynomial_oracle_checks = 0
    mirror_checks = 0
    for h, u in product(H, U):
        slope = (next_frequency(F(1, 2)+F(1, 10000), h, u)
                 - next_frequency(F(1, 2)-F(1, 10000), h, u)) / F(2, 10000)
        a = (1-u) * (1+h/2)
        b = 2*(1-u)*h
        # Finite difference equals a - b*epsilon^2, checked independently.
        assert slope == a - b*F(1, 10000)**2
        regime = ('neutral_continuum' if h == 0 and u == 0 else
                  'bistable' if a > 1 else 'central_only')
        if regime == 'bistable':
            x2 = (a-1)/b
            assert 0 < x2 <= F(1, 4)
            assert 0 <= 3-2*a < 1
        else:
            x2 = None
            if regime == 'central_only':
                assert 0 <= a < 1
        cases.append(dict(h=str(h), u=str(u), regime=regime,
                          a=str(a), b=str(b), outer_x_squared=str(x2) if x2 else None))
        paths = []
        for p0 in P0:
            p = p0
            path = [p]
            for _ in range(6):
                # Exact, independent eight-configuration transition.
                p = next_frequency(p, h, u)
                path.append(p)
                transition_checks += 1
            paths.append(path)
        assert all(paths[1][t] + paths[2][t] == 1 for t in range(7))
        mirror_checks += 7
        for p in (F(1, 7), F(2, 5), F(3, 4), F(1, 2)):
            assert three_demo(p) == 3*p*p-2*p*p*p
            polynomial_oracle_checks += 1
    counts = {name: sum(c['regime'] == name for c in cases)
              for name in ('neutral_continuum', 'central_only', 'bistable')}
    assert counts == {'neutral_continuum': 1, 'central_only': 4, 'bistable': 7}
    assert transition_checks == 288 and mirror_checks == 84
    return dict(evidence='E1_SYNTHETIC', method='eight_triple_explicit_Fraction',
                parameter_cases=12, trajectories=48, transitions=transition_checks,
                mirror_checks=mirror_checks,
                polynomial_oracle_checks=polynomial_oracle_checks,
                regime_counts=counts, rows=cases,
                independent_of_R159_source_function=True,
                external_independent_replication=False)


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True, indent=2))
