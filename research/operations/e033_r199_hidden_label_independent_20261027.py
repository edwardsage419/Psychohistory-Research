"""E033: independent exact enumeration of R199 synthetic HMM hidden-label Brier.
Uses only Python's standard library; no R/B code, personal data or paid services.
"""
from fractions import Fraction as Q
from itertools import product

STAY = Q(3, 4)
EXPECTED = {
    3: (Q(509, 2912), Q(1385, 2912), Q(1, 4), Q(219, 728), Q(219, 2912)),
    4: (Q(74348859, 430168816), Q(207122239, 430168816), Q(1, 4),
        Q(33193345, 107542204), Q(33193345, 430168816)),
}


def joint_mass(hidden, observed, emission):
    mass = Q(1, 2)
    for t, (x, y) in enumerate(zip(hidden, observed)):
        if t:
            mass *= STAY if x == hidden[t - 1] else 1 - STAY
        mass *= emission if x == y else 1 - emission
    return mass


def model(length, emission):
    paths = list(product((0, 1), repeat=length))
    joint = {(x, y): joint_mass(x, y, emission) for x in paths for y in paths}
    visible = {y: sum((joint[x, y] for x in paths), Q(0)) for y in paths}
    posterior = {(y, t): sum((joint[x, y] for x in paths if x[t] == 1), Q(0)) / visible[y]
                 for y in paths for t in range(length)}
    return paths, joint, visible, posterior


def main():
    checks, atoms, rows = 0, 0, []
    for length in (3, 4):
        models = {r: model(length, r) for r in (Q(3, 4), Q(1, 4))}
        for emission in (Q(3, 4), Q(1, 4)):
            paths, joint, visible, posterior = models[emission]
            other_visible, other_posterior = models[1 - emission][2:]
            atoms += len(joint)
            assert sum(joint.values(), Q(0)) == 1; checks += 1
            for y in paths:
                assert visible[y] == other_visible[y]; checks += 1
                for t in range(length):
                    assert posterior[y, t] + other_posterior[y, t] == 1; checks += 1
            risks = [Q(0), Q(0), Q(0)]
            for (x, y), mass in joint.items():
                for t in range(length):
                    for i, p in enumerate((posterior[y, t], other_posterior[y, t], Q(1, 2))):
                        risks[i] += mass * (p - x[t]) ** 2 / length
            excess = risks[1] - risks[0]
            identity = sum((visible[y] * (1 - 2 * posterior[y, t]) ** 2 / length
                            for y in paths for t in range(length)), Q(0))
            assert excess == identity; checks += 1
            assert risks[0] < risks[2]; checks += 1
            assert risks[1] > risks[2]; checks += 1
            actual = (*risks, excess, risks[2] - risks[0])
            for got, want in zip(actual, EXPECTED[length]):
                assert got == want, (length, emission, got, want)
                checks += 1
            rows.append((length, str(emission), *(str(x) for x in actual)))
    assert atoms == 640; checks += 1
    assert len(rows) == 4; checks += 1
    print(f"E033_EXACT_CHECKS={checks}; JOINT_ATOMS={atoms}; FAILURES=0")
    for row in rows:
        print(" | ".join(map(str, row)))


if __name__ == "__main__":
    main()
