#!/usr/bin/env python3
"""R116: EXACT rational, researcher-defined status cost vs single social cue toy.

Not a replication of Bernheim (1994)'s ENDOGENOUS type-inference equilibrium.
No Asch/Deutsch-Gerard real human participants, actions, or fitted coefficients.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import json

ZERO, ONE, HALF = Fraction(0), Fraction(1), Fraction(1, 2)
SELF_RELIABILITY = Fraction(3, 5)
STRONG_GROUP_RELIABILITY = Fraction(3, 4)
WEAK_GROUP_RELIABILITY = Fraction(11, 20)
STATUS_COST = Fraction(1, 4)
CELLS = ("C0_ANON", "C0_PUBLIC", "C1_ANON", "C1_PUBLIC")

class NormativeDesignError(ValueError):
    """Invalid binary trial or unsupported numerical interpretation."""


def _exact_probability(p, label, *, informative=False):
    if type(p) is not Fraction:
        raise NormativeDesignError("R116_EXACT_FRACTION_REQUIRED_" + label)
    if not (HALF < p < ONE) if informative else not (ZERO <= p <= ONE):
        raise NormativeDesignError("R116_PROBABILITY_BOUNDARY_INVALID_" + label)
    return p


def _binary(value, name):
    if type(value) is not int or value not in (0, 1):
        raise NormativeDesignError("R116_BINARY_ACTION_REQUIRED_" + name)
    return value


def _bool(value, name):
    if type(value) is not bool:
        raise NormativeDesignError("R116_BOOLEAN_DESIGN_FLAG_REQUIRED_" + name)
    return value


def _cost(value):
    if type(value) is not Fraction or value < ZERO:
        raise NormativeDesignError("R116_NONNEGATIVE_EXACT_STATUS_COST_REQUIRED")
    return value


def binary_signal_posterior(signal, reliability):
    """P(V=1 | one private signal, equal state priors)."""
    s = _binary(signal, "PRIVATE_SIGNAL")
    p = _exact_probability(reliability, "PRIVATE_RELIABILITY", informative=True)
    return p if s == 1 else ONE-p


def single_independent_cue_update(prior, cue, reliability):
    """One cue conditional independent of private signal given the same V.

    A public group consensus is NOT automatically independent information.
    Never exponentiate this cue by the number of agreeing public agents.
    """
    if type(prior) is not Fraction or not ZERO < prior < ONE:
        raise NormativeDesignError("R116_INTERIOR_EXACT_POSTERIOR_REQUIRED")
    cue = _binary(cue, "ONE_GROUP_CUE")
    p = _exact_probability(reliability, "GROUP_RELIABILITY", informative=True)
    l1 = p if cue else ONE-p
    l0 = ONE-p if cue else p
    num = prior*l1
    denom = num + (ONE-prior)*l0
    if denom <= ZERO:
        raise NormativeDesignError("R116_ZERO_EVIDENCE_PROBABILITY")
    return num/denom


@dataclass(frozen=True)
class ToyMechanism:
    """Synthetic fixed-status-loss model, NOT Bernheim's signaling game."""
    group_cue_informative: bool
    public_dissent_cost: Fraction

    def __post_init__(self):
        _bool(self.group_cue_informative, "INFORMATIONAL_CHANNEL")
        _cost(self.public_dissent_cost)


MODELS = {
    "NO_INFLUENCE":ToyMechanism(False, ZERO),
    "NORMATIVE_ONLY":ToyMechanism(False, STATUS_COST),
    "INFORMATIONAL_ONLY":ToyMechanism(True, ZERO),
    "BOTH":ToyMechanism(True, STATUS_COST),
}


def trial(model, *, private_signal=0, group_cue=1,
          cue_exposed=True, response_public=True,
          private_accuracy=SELF_RELIABILITY,
          group_accuracy=STRONG_GROUP_RELIABILITY):
    """Return private posterior, chosen public/private action and utilities.

    The inferred hidden fact and the agent's emitted action are different
    objects. The same visible choice can arise under dissimilar posteriors.
    """
    if type(model) is not ToyMechanism:
        raise NormativeDesignError("R116_TOY_MODEL_REQUIRED")
    s = _binary(private_signal, "PRIVATE_SIGNAL")
    cue = _binary(group_cue, "GROUP_CUE")
    seen = _bool(cue_exposed, "GROUP_CUE_EXPOSED")
    public = _bool(response_public, "RESPONSE_PUBLIC")
    private_accuracy = _exact_probability(private_accuracy, "PRIVATE_RELIABILITY", informative=True)
    group_accuracy = _exact_probability(group_accuracy, "GROUP_RELIABILITY", informative=True)
    prior = binary_signal_posterior(s, private_accuracy)
    q = single_independent_cue_update(prior,cue,group_accuracy) if (
        seen and model.group_cue_informative) else prior
    cost = model.public_dissent_cost if seen and public else ZERO
    u0 = (ONE-q) - (cost if cue == 1 else ZERO)
    u1 = q - (cost if cue == 0 else ZERO)
    action = 1 if u1 > u0 else 0  # deterministic tie policy, pre-frozen
    return {
        "private_signal":s,
        "group_cue_seen":seen,
        "response_public":public,
        "belief_V1":q,
        "payoff_action0":u0,
        "payoff_action1":u1,
        "choice":action,
    }


def factorial_choices(model, *, group_accuracy=STRONG_GROUP_RELIABILITY):
    """C0_ANON, C0_PUBLIC, C1_ANON, C1_PUBLIC, only choices."""
    if type(model) is not ToyMechanism:
        raise NormativeDesignError("R116_TOY_MODEL_REQUIRED")
    return {
        "C0_ANON":trial(model,cue_exposed=False,response_public=False,group_accuracy=group_accuracy)["choice"],
        "C0_PUBLIC":trial(model,cue_exposed=False,response_public=True,group_accuracy=group_accuracy)["choice"],
        "C1_ANON":trial(model,cue_exposed=True,response_public=False,group_accuracy=group_accuracy)["choice"],
        "C1_PUBLIC":trial(model,cue_exposed=True,response_public=True,group_accuracy=group_accuracy)["choice"],
    }


def public_conformity_threshold():
    """Own signal0 has q=2/5; status cost > 1/5 strictly flips to action1."""
    prior=binary_signal_posterior(0,SELF_RELIABILITY)
    return (ONE-prior)-prior


def study_receipt():
    strong={name:factorial_choices(model) for name,model in MODELS.items()}
    weak={name:factorial_choices(model,group_accuracy=WEAK_GROUP_RELIABILITY)
          for name,model in MODELS.items()}
    normative=trial(MODELS["NORMATIVE_ONLY"])
    informational=trial(MODELS["INFORMATIONAL_ONLY"])
    both=trial(MODELS["BOTH"])
    return {
        "research_id":"R116",
        "phase":"A",
        "catalogue_id":"03-005",
        "sources":{"Asch_1955":"10.1038/scientificamerican1155-31",
                   "Deutsch_Gerard_1955":"10.1037/h0046408",
                   "Bernheim_1994":"10.1086/261957"},
        "model_status":"RESEARCHER_DESIGNED_STATUS_COST_TOY_NOT_BERNHEIM_ORIGINAL_EQUILIBRIUM",
        "strong_single_cue_choice_grid":strong,
        "weak_single_cue_choice_grid":weak,
        "strong_cue_normative_private_belief_V1":str(normative["belief_V1"]),
        "strong_cue_informational_private_belief_V1":str(informational["belief_V1"]),
        "strong_cue_combined_private_belief_V1":str(both["belief_V1"]),
        "strong_cue_public_actions_identical_for_normative_and_information":(
            normative["choice"]==informational["choice"]==both["choice"]==1),
        "strong_cue_both_vs_informational_grid_indistinguishable":(
            strong["BOTH"]==strong["INFORMATIONAL_ONLY"]),
        "weak_cue_public_actions_identify_extra_status_only_under_frozen_toy_assumptions":(
            weak["BOTH"]["C1_PUBLIC"]==1 and
            weak["INFORMATIONAL_ONLY"]["C1_PUBLIC"]==0),
        "unobserved_private_state_and_social_motive_not_identified_from_single_public_choice":True,
        "private_posterior_equal_public_and_anonymous_for_fixed_information":True,
        "original_human_E2_evaluations":0,
        "original_1955_individual_observations_reanalyzed":False,
        "fitted_Bernheim_1994_game_equilibrium":False,
        "PESEN_v0_1":"FROZEN",
        "R073":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(study_receipt(),sort_keys=True,indent=2))
