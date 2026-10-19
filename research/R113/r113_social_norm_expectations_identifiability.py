#!/usr/bin/env python3
"""R113 first-party published-table arithmetic and synthetic mechanism nonidentification.

The published table is Bicchieri, Lindemans, Jiang (2014), Front. Psychol.
5:1418, Table 2. It summarizes previous Bicchieri & Chavez (2013) studies.
No original person-level source records were obtained or fitted.

The counterfactual utility toy function is OUR OWN falsification construction,
NOT Bicchieri's original behavioral model or any fitted psychology.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import math

SOURCE_DOI = "10.3389/fpsyg.2014.01418"
SOURCE_TABLE = "Table 2"
CATEGORIES = ("equal_split_5_5", "unequal_split_8_2", "coin_flip")
ACTUAL_BEHAVIOR_PERCENT = (44, 12, 44)
RESPONDER_EMPIRICAL_EXPECTATION_PERCENT = (44, 28, 28)
RESPONDER_PERSONAL_NORMATIVE_BELIEF_PERCENT = (100, 22, 52)
PROPOSER_NORMATIVE_EXPECTATION_PERCENT = (100, 10, 79)


class R113MeasurementError(ValueError):
    pass


def _percentage(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 100:
        raise R113MeasurementError("R113_PERCENT_OUTSIDE_CLOSED_0_TO_100")
    return float(value)


def _validate_three(values, *, mutually_exclusive):
    seq = tuple(values)
    if len(seq) != 3:
        raise R113MeasurementError("R113_EXPECT_THREE_PUBLISHED_OPTIONS")
    numbers = tuple(_percentage(v) for v in seq)
    if mutually_exclusive and not math.isclose(math.fsum(numbers), 100, abs_tol=1e-10):
        raise R113MeasurementError("R113_EXCLUSIVE_OPTIONS_NOT_SUM_TO_100_PERCENT")
    return numbers


def measure_kind(*, social, normative):
    """Paper Table 1 cross-classification; descriptive names, not latent inference."""
    if type(social) is not bool or type(normative) is not bool:
        raise R113MeasurementError("R113_SOCIAL_AND_NORMATIVE_FLAGS_MUST_BE_BOOL")
    return {
        (False, False): "factual_belief",
        (True, False): "empirical_expectation_about_others_actions",
        (False, True): "personal_normative_belief_about_ought",
        (True, True): "normative_expectation_about_others_ought_beliefs",
    }[(social, normative)]


def published_table_2_arithmetic():
    """Published 2014 Table 2 rounded aggregate values, NOT person-level reanalysis."""
    actual = _validate_three(ACTUAL_BEHAVIOR_PERCENT, mutually_exclusive=True)
    empirical = _validate_three(RESPONDER_EMPIRICAL_EXPECTATION_PERCENT, mutually_exclusive=True)
    personal = _validate_three(RESPONDER_PERSONAL_NORMATIVE_BELIEF_PERCENT, mutually_exclusive=False)
    normative = _validate_three(PROPOSER_NORMATIVE_EXPECTATION_PERCENT, mutually_exclusive=False)
    return {
        "source": SOURCE_DOI,
        "source_table": SOURCE_TABLE,
        "categories": list(CATEGORIES),
        "published_actor_behavior_percent": list(ACTUAL_BEHAVIOR_PERCENT),
        "published_responder_empirical_expectation_percent": list(RESPONDER_EMPIRICAL_EXPECTATION_PERCENT),
        "published_responder_personal_normative_belief_percent": list(RESPONDER_PERSONAL_NORMATIVE_BELIEF_PERCENT),
        "published_proposer_normative_expectation_percent": list(PROPOSER_NORMATIVE_EXPECTATION_PERCENT),
        "empirical_minus_behavior_percentage_points": [int(round(x-y)) for x,y in zip(empirical, actual)],
        "normative_minus_personal_ought_percentage_points": [int(round(x-y)) for x,y in zip(normative,personal)],
        "sum_actual_behavior_percent": int(round(math.fsum(actual))),
        "sum_empirical_expectation_percent": int(round(math.fsum(empirical))),
        "sum_personal_normative_judgment_percent": int(round(math.fsum(personal))),
        "sum_normative_expectation_judgment_percent": int(round(math.fsum(normative))),
        "fairness_judgments_allow_multiple_options": True,
        "source_values_rounded_published_percentages_not_individual_rows": True,
        "original_individual_human_experiment_data_read": False,
        "causal_effect_or_uncertainty_identified_from_aggregate_table": False,
    }


@dataclass(frozen=True)
class SyntheticChoiceMechanism:
    """Researcher-defined educational illustration, not an author-estimated model."""
    baseline: float
    empirical_weight: float
    normative_weight: float

    def __post_init__(self):
        for x in (self.baseline, self.empirical_weight, self.normative_weight):
            if type(x) not in (int, float) or not math.isfinite(x):
                raise R113MeasurementError("R113_SYNTHETIC_COEFFICIENT_NOT_FINITE")

    def margin(self, empirical_expectation, normative_expectation):
        e = _percentage(empirical_expectation * 100) / 100 if type(empirical_expectation) in (float, int) else None
        n = _percentage(normative_expectation * 100) / 100 if type(normative_expectation) in (float, int) else None
        if e is None or n is None:
            raise R113MeasurementError("R113_SYNTHETIC_EXPECTATION_MUST_BE_NUMERIC_0_1")
        return self.baseline + self.empirical_weight*(e-0.5) + self.normative_weight*(n-0.5)

    def choice(self, empirical_expectation, normative_expectation):
        return int(self.margin(empirical_expectation, normative_expectation) >= 0)


def observational_equivalence_counterexample():
    """Same baseline actions, distinct counterfactual mechanisms.

    Both worlds see EE=NE=0.8, and both choose A. Only the conditional world
    switches its action when beliefs move to 0.2. The problem is identification.
    """
    unconditional = SyntheticChoiceMechanism(0.1, 0, 0)
    conditional = SyntheticChoiceMechanism(-0.2, 0.5, 0.5)
    base = (0.8, 0.8)
    counterfactual = (0.2, 0.2)
    results = {
        "baseline_empirical": base[0],
        "baseline_normative": base[1],
        "unconditional_world": {"parameters": asdict(unconditional),
            "observed_action": unconditional.choice(*base),
            "intervened_action": unconditional.choice(*counterfactual)},
        "conditional_world": {"parameters": asdict(conditional),
            "observed_action": conditional.choice(*base),
            "intervened_action": conditional.choice(*counterfactual)},
        "counterfactual_empirical": counterfactual[0],
        "counterfactual_normative": counterfactual[1],
        "models_are_synthetic_not_fitted": True,
        "same_observed_choices_cannot_identify_social_norm_mechanism": True,
    }
    assert results["unconditional_world"]["observed_action"] == results["conditional_world"]["observed_action"] == 1
    assert results["unconditional_world"]["intervened_action"] != results["conditional_world"]["intervened_action"]
    return results


def isolated_expectation_manipulation():
    """Synthetic selective contrasts: EE-only and NE-only effects differ."""
    empirical_only = SyntheticChoiceMechanism(-0.1, 1.0, 0.0)
    normative_only = SyntheticChoiceMechanism(-0.1, 0.0, 1.0)
    low, high = 0.2, 0.8
    return {
        "empirical_only": {
            "original": empirical_only.choice(high, high),
            "switch_empirical_only": empirical_only.choice(low, high),
            "switch_normative_only": empirical_only.choice(high, low),
        },
        "normative_only": {
            "original": normative_only.choice(high, high),
            "switch_empirical_only": normative_only.choice(low, high),
            "switch_normative_only": normative_only.choice(high, low),
        },
        "synthetic_only": True,
    }


if __name__ == "__main__":
    print(json.dumps({"table_2": published_table_2_arithmetic(),
                      "identifiability": observational_equivalence_counterexample(),
                      "selective_contrasts": isolated_expectation_manipulation()},
                     sort_keys=True, indent=2))
