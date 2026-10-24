#!/usr/bin/env python3
"""R138 third-method independent finite mechanism audit, 2026-10-25.

No third-party packages. No original R138 algorithm imported.
Only synthetic integer types; not human data.
"""
import itertools
import json
from functools import lru_cache


def second_price(bids, true_values, i):
    winner = min(range(3), key=lambda k: (-bids[k], k))
    return (true_values[i] - max(bids[k] for k in range(3) if k != i)) if winner == i else 0


@lru_cache(None)
def assignment(bids):
    """Dynamic program on agent index and 2-bit used-item mask."""
    @lru_cache(None)
    def solve(agent, used):
        if agent == 3:
            return 0, ()
        best_value, tail = solve(agent + 1, used)
        best_alloc = (-1,) + tail
        for item in (0, 1):
            if not (used & (1 << item)):
                tail_value, tail_alloc = solve(agent + 1, used | (1 << item))
                candidate_value = bids[agent][item] + tail_value
                if candidate_value > best_value:
                    best_value = candidate_value
                    best_alloc = (item,) + tail_alloc
        return best_value, best_alloc
    return solve(0, 0)


def vcg(bids, actual, i):
    welfare, alloc = assignment(bids)
    without_i = tuple((0, 0) if j == i else bids[j] for j in range(3))
    others_optimal = assignment(without_i)[0]
    others_in_selected = sum(bids[j][alloc[j]] for j in range(3)
                             if j != i and alloc[j] != -1)
    tax = others_optimal - others_in_selected
    value = actual[i][alloc[i]] if alloc[i] != -1 else 0
    return value - tax, tax, welfare, alloc


def public_pivot(bids, true_values, i):
    others = sum(bids[j] for j in range(3) if j != i)
    built = sum(bids) >= 5
    tax = max(0, 5 - others) if built else 0
    externality = max(0, others - 5) - ((others - 5) if built else 0)
    assert tax == externality
    return (true_values[i] if built else 0) - tax, tax, built


def main():
    single = dict(profiles=0, deviations=0, violations=0, utility_ties=0)
    for true in itertools.product(range(5), repeat=3):
        single['profiles'] += 1
        for i in range(3):
            honest = second_price(true, true, i)
            for report in range(5):
                b = list(true)
                b[i] = report
                utility = second_price(tuple(b), true, i)
                single['deviations'] += 1
                single['violations'] += int(utility > honest)
                single['utility_ties'] += int(utility == honest and report != true[i])

    vcg_stats = dict(profiles=0, deviations=0, violations=0,
                     negative_tax=0, truthful_ir_fail=0, welfare_fail=0)
    types = tuple(itertools.product(range(3), repeat=2))
    for true in itertools.product(types, repeat=3):
        vcg_stats['profiles'] += 1
        honest_welfare, _ = assignment(true)
        for i in range(3):
            honest, tax, _, _ = vcg(true, true, i)
            vcg_stats['truthful_ir_fail'] += int(honest < 0)
            vcg_stats['negative_tax'] += int(tax < 0)
            for report in types:
                bids = list(true)
                bids[i] = report
                other_utility, _, _, _ = vcg(tuple(bids), true, i)
                vcg_stats['deviations'] += 1
                vcg_stats['violations'] += int(other_utility > honest)
        brute = 0
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    items = [v for v in (a, b, c) if v != -1]
                    if len(set(items)) != len(items):
                        continue
                    w = sum(true[j][x] for j, x in enumerate((a, b, c)) if x != -1)
                    brute = max(brute, w)
        vcg_stats['welfare_fail'] += int(brute != honest_welfare)

    public = dict(profiles=0, deviations=0, violations=0, built=0,
                  deficits=0, built_zero_tax=0, truthful_ir_fail=0,
                  welfare_fail=0)
    for true in itertools.product(range(6), repeat=3):
        public['profiles'] += 1
        is_built = sum(true) >= 5
        taxes = [public_pivot(true, true, i)[1] for i in range(3)]
        public['built'] += int(is_built)
        public['deficits'] += int(is_built and sum(taxes) < 5)
        public['built_zero_tax'] += int(is_built and sum(taxes) == 0)
        public['welfare_fail'] += int(is_built != (sum(true) >= 5))
        for i in range(3):
            honest = public_pivot(true, true, i)[0]
            public['truthful_ir_fail'] += int(honest < 0)
            for report in range(6):
                bids = list(true)
                bids[i] = report
                other = public_pivot(tuple(bids), true, i)[0]
                public['deviations'] += 1
                public['violations'] += int(other > honest)

    first_price = (4 - 4, 4 - 2)
    wrong_self_report_tax = (5 - 5, 5 - 0)
    wrong_free_tax = (0, 1)
    witness = ((0, 0), (0, 1), (1, 1))
    _, witness_tax, _, witness_alloc = vcg(witness, witness, 1)
    witness_single_item_price = max(witness[j][1] for j in range(3) if j != 1)
    negative = {
        'first_price_truth_vs_bid2': list(first_price),
        'own_report_tax_truth_vs_bid0': list(wrong_self_report_tax),
        'zero_tax_public_truth_vs_bid2': list(wrong_free_tax),
        'vcg_unit_demand_witness_allocation': list(witness_alloc),
        'vcg_witness_player1_tax': witness_tax,
        'incorrect_separate_second_price_B': witness_single_item_price,
        'all_controls_detected': first_price[1] > first_price[0]
            and wrong_self_report_tax[1] > wrong_self_report_tax[0]
            and wrong_free_tax[1] > wrong_free_tax[0]
            and witness_alloc[1] == 1 and witness_tax != witness_single_item_price,
    }
    result = {'method': 'critical_threshold_and_two_bit_assignment_DP',
              'evidence': 'internal_E1_only', 'single': single,
              'two_goods_vcg': vcg_stats, 'public': public, 'negative_controls': negative,
              'total_deviations': single['deviations'] + vcg_stats['deviations'] + public['deviations']}
    assert result['total_deviations'] == 25446, result
    assert single['profiles'] == 125 and single['violations'] == 0, result
    assert vcg_stats['profiles'] == 729 and vcg_stats['violations'] == 0, result
    assert vcg_stats['welfare_fail'] == 0 and vcg_stats['truthful_ir_fail'] == 0 and vcg_stats['negative_tax'] == 0, result
    assert public['profiles'] == 216 and public['violations'] == 0 and public['truthful_ir_fail'] == 0, result
    assert (public['built'], public['deficits'], public['built_zero_tax']) == (181, 160, 69), result
    assert negative['all_controls_detected'], result
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
