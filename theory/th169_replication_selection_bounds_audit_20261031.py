#!/usr/bin/env python3
"""TH169 exact synthetic selection and published-count audit.

No real participant data, original code imports, or network access.
Nonblind artificial audit only; no scientific E1/E2/E3 upgrade.
"""
from fractions import Fraction as F
import json


def audit():
    # Original paper vintages and published 2016 replication counts.
    n2014 = (113, 195, 45)
    n2016 = (112, 139, 45)
    assert sum(n2014) == 353
    assert sum(n2016) == 296
    assert n2014[0] + n2014[2] == 158
    assert n2016[0] + n2016[2] == 157
    assert sum(n2014) - sum(n2016) == 57
    assert 35 + 2 == 37  # 3ie report and openICPSR code directory.
    assert 880 - 818 == 62  # NREGS GP official versus survey.
    assert 880 - 878 == 2   # SSP GP official versus survey.

    # Synthetic nonrandom adoption, equal sized observed adopter/nonadopter.
    observed_adopter = F(9, 10)
    observed_nonadopter = F(1, 2)
    observed_gap = observed_adopter - observed_nonadopter
    assert observed_gap == F(2, 5)

    # Two missing potential outcomes are each unconstrained in [0, 1].
    def ate(adopter_y0, nonadopter_y1):
        assert F(0) <= adopter_y0 <= F(1)
        assert F(0) <= nonadopter_y1 <= F(1)
        return ((observed_adopter - adopter_y0)
                + (nonadopter_y1 - observed_nonadopter)) / 2

    worlds = {
        "A": ate(F(4, 5), F(3, 5)),
        "B": ate(F(0), F(1)),
        "C": ate(F(1), F(0)),
    }
    assert worlds == {"A": F(1, 10), "B": F(7, 10), "C": F(-3, 10)}
    lower = ate(F(1), F(0))
    upper = ate(F(0), F(1))
    assert lower == F(-3, 10)
    assert upper == F(7, 10)
    assert lower < observed_gap < upper
    return {
        "status": "PASS_SYNTHETIC_NONBLIND",
        "original_2014_randomized": sum(n2014),
        "original_2016_randomized": sum(n2016),
        "vintage_difference": 57,
        "observed_adoption_gap": str(observed_gap),
        "synthetic_ate_worlds": {k: str(v) for k, v in worlds.items()},
        "sharp_ate_bounds": [str(lower), str(upper)],
        "real_data_replay": "NOT_RUN",
        "new_E1_E2_E3": 0,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True))
