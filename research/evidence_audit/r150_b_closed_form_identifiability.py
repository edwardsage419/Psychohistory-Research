"""R150 independent B audit: closed-form factor intervals, no JS/source import.
Only synthetic E1. Run: python r150_b_closed_form_identifiability.py
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json

SHOCKS = ("NONE", "PANDEMIC_YEAR4", "INMIGRATION_YEAR4")

def closed_form(td: int, tb: int, t: int, shock: str) -> Q:
    if not (0 <= td <= 8 and 0 <= tb <= 8 and 0 <= t <= 12 and shock in SHOCKS):
        raise ValueError("outside frozen domain")
    positive = max(0, min(t, tb) - td) if td < tb else 0
    negative = max(0, min(t, td) - tb) if tb < td else 0
    population = Q(1000) * Q(23, 20)**positive * Q(17, 20)**negative
    if t > 4 and shock != "NONE":
        if td <= 4 < tb:
            original_year4_factor = Q(23, 20)
        elif tb <= 4 < td:
            original_year4_factor = Q(17, 20)
        else:
            original_year4_factor = Q(1)
        delta = Q(-1, 10) if shock == "PANDEMIC_YEAR4" else Q(1, 10)
        population *= (original_year4_factor + delta) / original_year4_factor
    return population

def run():
    output = {"method": "independent_interval_exponents_with_year4_factor_ratio",
              "evidence": "E1 artificial", "results": {}, "checks": 0}
    for shock in SHOCKS:
        terminal, trajectories = defaultdict(list), defaultdict(list)
        for td in range(9):
            for tb in range(9):
                history = tuple(closed_form(td, tb, t, shock) for t in range(13))
                assert history[0] == 1000
                terminal[history[-1]].append((td, tb))
                trajectories[history].append((td, tb))
                output["checks"] += 13
        terminal_hist = dict(sorted(Counter(map(len, terminal.values())).items()))
        trajectory_hist = dict(sorted(Counter(map(len, trajectories.values())).items()))
        output["results"][shock] = {
            "terminal_distinct": len(terminal),
            "trajectory_distinct": len(trajectories),
            "terminal_class_size_histogram": terminal_hist,
            "trajectory_class_size_histogram": trajectory_hist,
            "example_td2_tb6": str(closed_form(2, 6, 12, shock)),
        }
        assert len(trajectories) == 73
        assert trajectory_hist == {1: 72, 9: 1}
        assert len(terminal) == (17 if shock == "NONE" else 25)
        assert all(closed_form(k, k, 12, shock) == closed_form(0, 0, 12, shock)
                   for k in range(9))
        output["checks"] += 4
    ratios = set()
    for td in range(9):
        for tb in range(9):
            ratios.add(closed_form(td, tb, 12, "PANDEMIC_YEAR4") /
                       closed_form(td, tb, 12, "NONE"))
    assert ratios == {Q(15, 17), Q(21, 23), Q(9, 10)}
    output["mortality_shock_multipliers"] = sorted(map(str, ratios))
    output["checks"] += 1
    return output

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
