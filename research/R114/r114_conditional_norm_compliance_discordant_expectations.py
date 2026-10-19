#!/usr/bin/env python3
"""R114 source-bounded study: synthetic social expectation conflict identification.

IMPORTANT: these parameterized logit surfaces are researcher's counterexamples.
They are NOT Bicchieri & Xiao (2009) author-estimated equations, nor human data.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math


class NormMechanismError(ValueError):
    """Invalid belief factorial design or numerical model inputs."""


CELLS = ("E0N0", "E1N0", "E0N1", "E1N1")


def _finite_real(x, name):
    if type(x) not in (float, int) or not math.isfinite(x):
        raise NormMechanismError("R114_FINITE_REAL_REQUIRED_" + name)
    return float(x)


def _belief_level(x, name):
    if type(x) is not int or x not in (0, 1):
        raise NormMechanismError("R114_BINARY_BELIEF_REQUIRED_" + name)
    return x


def logistic(x):
    """Stable inverse logit at extreme, finite log-odds."""
    z = _finite_real(x, "LOG_ODDS")
    if z >= 0:
        v = math.exp(-z)
        return 1.0 / (1.0 + v)
    v = math.exp(z)
    return v / (1.0 + v)


def logit(p):
    """Finite log-odds for strictly interior mathematical probabilities only."""
    z = _finite_real(p, "PROBABILITY")
    if not 0 < z < 1:
        raise NormMechanismError("R114_LOGIT_REQUIRES_STRICT_INTERIOR_PROBABILITY")
    return math.log(z) - math.log1p(-z)


@dataclass(frozen=True)
class SyntheticBeliefModel:
    """Educational 2x2 factorial, not a behavioral theory fitted to an experiment."""

    intercept: float
    empirical_effect: float
    normative_effect: float
    interaction_effect: float

    def __post_init__(self):
        for field in ("intercept", "empirical_effect", "normative_effect",
                      "interaction_effect"):
            _finite_real(getattr(self, field), field.upper())

    def linear_predictor(self, empirical, normative):
        e = _belief_level(empirical, "EMPIRICAL")
        n = _belief_level(normative, "NORMATIVE")
        return (self.intercept + self.empirical_effect * e
                + self.normative_effect * n
                + self.interaction_effect * e * n)

    def probability(self, empirical, normative):
        return logistic(self.linear_predictor(empirical, normative))

    def grid(self):
        return {
            "E0N0": self.probability(0, 0),
            "E1N0": self.probability(1, 0),
            "E0N1": self.probability(0, 1),
            "E1N1": self.probability(1, 1),
        }


MODELS = {
    "DESCRIPTIVE": SyntheticBeliefModel(-1, 2, 0, 0),
    "NORMATIVE_ONLY": SyntheticBeliefModel(-1, 0, 2, 0),
    "BOTH_ADDITIVE": SyntheticBeliefModel(-1, 1, 1, 0),
    "INTERACTION": SyntheticBeliefModel(-1, 1, 1, 1),
}


def exact_factorial_logit_coefficients(cell_probs):
    """Identify FOUR saturated logistic coefficients from complete 2x2 cells.

    Recovered parameters are mathematical cell contrasts. They are not causal
    without a legitimate randomized experiment and measurement assumptions.
    """
    if type(cell_probs) is not dict or set(cell_probs) != set(CELLS):
        raise NormMechanismError("R114_ALL_FOUR_UNIQUE_FACTORIAL_CELLS_REQUIRED")
    z = {key: logit(cell_probs[key]) for key in CELLS}
    base = z["E0N0"]
    effect_e = z["E1N0"] - base
    effect_n = z["E0N1"] - base
    effect_en = z["E1N1"] - z["E1N0"] - z["E0N1"] + base
    return SyntheticBeliefModel(base, effect_e, effect_n, effect_en)


def log_odds_interaction_contrast(cell_probs):
    return exact_factorial_logit_coefficients(cell_probs).interaction_effect


def aligned_conditions_counterexample():
    """Aligned-only cells cannot distinguish descriptive from normative effects."""
    desc = MODELS["DESCRIPTIVE"].grid()
    norm = MODELS["NORMATIVE_ONLY"].grid()
    return {
        "aligned_E0N0_identical": desc["E0N0"] == norm["E0N0"],
        "aligned_E1N1_identical": desc["E1N1"] == norm["E1N1"],
        "discordant_E1N0_descriptive": desc["E1N0"],
        "discordant_E1N0_normative": norm["E1N0"],
        "discordant_E0N1_descriptive": desc["E0N1"],
        "discordant_E0N1_normative": norm["E0N1"],
        "same_aligned_observations_do_not_identify_expectation_type": True,
        "synthetic_only": True,
    }


def factorial_math_receipt():
    """No empirical regression, no source human observations."""
    return {
        "research_id": "R114",
        "phase": "A",
        "source_primary_2009_DOI": "10.1002/bdm.621",
        "source_primary_2014_DOI": "10.3389/fpsyg.2014.01418",
        "toy_model_is_authored_here_not_in_primary_paper": True,
        "all_models_four_exact_factorial_probabilities": {
            name: model.grid() for name, model in MODELS.items()
        },
        "all_models_exact_2x2_log_odds_interaction": {
            name: log_odds_interaction_contrast(model.grid())
            for name, model in MODELS.items()
        },
        "aligned_observation_nonidentification": aligned_conditions_counterexample(),
        "observed_real_human_choices": 0,
        "estimated_human_psychological_coefficients": 0,
        "causal_norm_effect_demonstrated": False,
        "PESEN_v0_1": "FROZEN",
    }


if __name__ == "__main__":
    print(json.dumps(factorial_math_receipt(), sort_keys=True, indent=2))
