"""Independent R141 audit: exact binomial threshold equilibria and KKT.

No repository source import, third party dependencies, or external data.
"""
import json
from fractions import Fraction as F
from math import comb

NS_BINARY = (3, 4, 5, 6, 8, 10, 12, 16)
RS_BINARY = (F(0), F(1, 2), F(2))
NS_CONTINUOUS = (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24)
RS_CONTINUOUS = (F(0), F(1, 2))


def binomial_audit():
    rows = []
    total_profiles = 0
    total_flips = 0
    total_equilibria = 0
    for n in NS_BINARY:
        for reward in RS_BINARY:
            counts = {}
            for m in range(n + 1):
                # Analyze a contributor's withdrawal and a noncontributor's entry.
                # Payoffs are exact fractions; no direct use of the JS algorithm.
                benefit = lambda k: F(12, n) if k >= 3 else F(0)
                withdraw_gain = (benefit(m - 1) - benefit(m) + 1 - reward) if m else F(0)
                enter_gain = (benefit(m + 1) - benefit(m) - 1 + reward) if m < n else F(0)
                if withdraw_gain <= 0 and enter_gain <= 0:
                    counts[m] = comb(n, m)
            number = sum(counts.values())
            rows.append({'n': n, 'reward': str(reward), 'ne_count': number, 'by_m': counts})
            total_equilibria += number
            total_profiles += 2 ** n
            total_flips += n * 2 ** n
    lookup = {(row['n'], row['reward']): row['ne_count'] for row in rows}
    assert lookup[8, '0'] == 57
    assert lookup[16, '0'] == 1
    assert lookup[16, '1/2'] == 561
    assert lookup[16, '2'] == 1
    assert total_profiles == 213096
    assert total_flips == 3331944
    assert total_equilibria == 1446
    return {'scenarios': len(rows), 'profiles': total_profiles, 'possible_flips': total_flips,
            'equilibria': total_equilibria, 'rows': rows}


def continuous_audit():
    rows = []
    for n in NS_CONTINUOUS:
        for reward in RS_CONTINUOUS:
            t = max(F(0), (F(12) - n * (1 - reward)) / 3)
            x = t / n
            gradient = (12 - t) / n - (1 - reward) - 2 * x
            assert (gradient == 0 if x > 0 else gradient <= 0)
            social_t = F(11 * n, n + 2)
            assert social_t > 0
            rows.append({'n': n, 'reward': str(reward), 't': str(t),
                         'social_optimum': str(social_t), 'external_fiscal': str(reward * t)})
    shares = [F(1, 2)] + [F(1, 30)] * 15
    efforts = [F(2)] + [F(0)] * 15
    t = sum(efforts)
    assert sum(shares) == 1 and t == 2
    gradients = [shares[i] * (12 - t) - 1 - 2 * efforts[i] for i in range(16)]
    assert gradients[0] == 0 and all(g == F(-2, 3) for g in gradients[1:])
    assert next(row for row in rows if row['n'] == 16 and row['reward'] == '0')['t'] == '0'
    return {'scenarios': len(rows), 'rows': rows, 'privileged_t': str(t),
            'privileged_inactive_gradients': str(gradients[1])}


def main():
    binary = binomial_audit()
    continuous = continuous_audit()
    result = {'status': 'PASS_INDEPENDENT_LOCAL_FRACTION_COMB_E1',
              'binary': binary, 'continuous': continuous,
              'nc1_wrong_n16_r0_three_contributor_profiles': comb(16, 3),
              'nc2_n16_r2_real_resource_welfare': 12 - 16,
              'nc2_n16_r2_external_fiscal': 2 * 16,
              'new_E2': 0, 'new_E3': 0, 'external_independent_replication': 0}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
