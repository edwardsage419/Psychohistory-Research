#!/usr/bin/env python3
"""R213 finite eight-unit assignment exact E1, using frozen R213 source generator.
Run from repository root: python research/validation/r213_eight_unit_assignment_exact_20261027.py
"""
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research' / 'R213'))
from r213_exact_instrumental_variables import WORLDS, build_population, z_probability, observed, complier_LATE, source_world  # noqa: E402


def summarize(world):
    persons = build_population(world)
    assert len(persons) == 8
    q = [z_probability(world, i) for i in range(8)]
    tally = {k: [0, F(0)] for k in ('empty_arm', 'zero_sample_first_stage', 'defined')}
    total = F(0)
    wald_weighted = F(0)
    tail_10 = F(0)
    gap_2 = F(0)
    max_abs_wald = F(0)
    late = complier_LATE(world)
    for z_vector in itertools.product((0, 1), repeat=8):
        probability = F(1)
        for i, z in enumerate(z_vector):
            probability *= q[i] if z else 1-q[i]
        total += probability
        n1 = sum(z_vector)
        n0 = 8-n1
        if n1 == 0 or n0 == 0:
            key = 'empty_arm'
        else:
            d1 = d0 = y1 = y0 = F(0)
            for i, z in enumerate(z_vector):
                d, y = observed(world, i, z)
                if z:
                    d1 += d; y1 += y
                else:
                    d0 += d; y0 += y
            fs = d1/n1 - d0/n0
            if fs == 0:
                key = 'zero_sample_first_stage'
            else:
                key = 'defined'
                ratio = (y1/n1-y0/n0)/fs
                wald_weighted += probability*ratio
                max_abs_wald = max(max_abs_wald, abs(ratio))
                if abs(ratio) >= 10:
                    tail_10 += probability
                if late is not None and abs(ratio-late) >= 2:
                    gap_2 += probability
        tally[key][0] += 1
        tally[key][1] += probability
    assert total == 1 and sum(x[0] for x in tally.values()) == 256
    assert sum((x[1] for x in tally.values()), F(0)) == 1
    assert all(x[1] >= 0 for x in tally.values())
    defined_mass = tally['defined'][1]
    old, _ = source_world(world)
    return {
        'world': world,
        'population_first_stage_exact': old['first_stage_exact'],
        'population_wald_exact': old['wald_ratio_exact'],
        'population_complier_LATE_exact': str(late) if late is not None else 'UNDEFINED_NO_COMPLIERS',
        'instrument_independent_of_type': world != 'Z_CONFOUNDING',
        'assignment_count': 256,
        'assignment_probability_sum_exact': str(total),
        'empty_arm_count': tally['empty_arm'][0],
        'empty_arm_probability_exact': str(tally['empty_arm'][1]),
        'zero_sample_first_stage_count': tally['zero_sample_first_stage'][0],
        'zero_sample_first_stage_probability_exact': str(tally['zero_sample_first_stage'][1]),
        'defined_count': tally['defined'][0],
        'defined_probability_exact': str(defined_mass),
        'wald_mean_conditional_defined_exact': str(wald_weighted/defined_mass) if defined_mass else 'UNDEFINED_NO_DEFINED_ASSIGNMENT',
        'max_absolute_defined_wald_exact': str(max_abs_wald) if defined_mass else 'UNDEFINED',
        'absolute_wald_at_least_10_unconditional_probability_exact': str(tail_10),
        'absolute_wald_at_least_10_conditional_defined_probability_exact': str(tail_10/defined_mass) if defined_mass else 'UNDEFINED',
        'absolute_wald_minus_late_at_least_2_unconditional_probability_exact': str(gap_2) if late is not None else 'NOT_APPLICABLE_NO_COMPLIERS',
        'absolute_wald_minus_late_at_least_2_conditional_defined_probability_exact': str(gap_2/defined_mass) if late is not None and defined_mass else 'NOT_APPLICABLE',
    }


def compute():
    worlds = [summarize(w) for w in WORLDS]
    assert len(worlds) == 8 and sum(w['assignment_count'] for w in worlds) == 2048
    return {'research_id': 'R213', 'date': '2026-10-27', 'evidence': 'E1_ARTIFICIAL_FINITE_ASSIGNMENT',
            'original_R213_acceptance_unchanged': True, 'R073_frozen': True, 'PESEN_v0_1_frozen': True,
            'real_human_E2': 0, 'historical_E3': 0, 'external_independent_replication': 0,
            'world_count': 8, 'assignment_vectors_total': 2048,
            'summary_worlds': worlds}


if __name__ == '__main__':
    print(json.dumps(compute(), ensure_ascii=False, indent=2, sort_keys=True))
