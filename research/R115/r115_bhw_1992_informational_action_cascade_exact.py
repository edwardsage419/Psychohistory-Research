#!/usr/bin/env python3
"""R115 exact Bayesian learning from *actions* in Bikhchandani et al. (1992).

Independent private Bernoulli signals conditional on a fixed binary state;
binary public actions selected by expected state value and fair random tie.
Exact fractions throughout. The observer must marginalize hidden signals and
tie coins: an observed action is NOT in general an independent private signal.

This is a bounded original-paper mathematical reconstruction, not a fitted
human psychology model or an empirical replication.
"""
from __future__ import annotations

from fractions import Fraction
import json


HALF = Fraction(1, 2)
ONE = Fraction(1)


class CascadeEvidenceError(ValueError):
    """Reject unsupported information sets, impossible action histories."""


def _fraction(x, name, lower=None, upper=None):
    if type(x) is not Fraction:
        raise CascadeEvidenceError("R115_EXACT_FRACTION_REQUIRED_" + name)
    if lower is not None and not lower < x:
        raise CascadeEvidenceError("R115_FRACTION_LOWER_BOUND_" + name)
    if upper is not None and not x < upper:
        raise CascadeEvidenceError("R115_FRACTION_UPPER_BOUND_" + name)
    return x


def _state_or_binary(value, name):
    if type(value) is not int or value not in (0, 1):
        raise CascadeEvidenceError("R115_BINARY_INT_REQUIRED_" + name)
    return value


def _parameters(public_prior, signal_reliability):
    q = _fraction(public_prior, "PUBLIC_PRIOR", Fraction(0), ONE)
    p = _fraction(signal_reliability, "SIGNAL_RELIABILITY", HALF, ONE)
    return q, p


def likelihood_private_signal(signal, hidden_state, reliability):
    """P(signal|V) for a conditionally independent private binary signal."""
    s = _state_or_binary(signal, "PRIVATE_SIGNAL")
    v = _state_or_binary(hidden_state, "HIDDEN_STATE")
    p = _fraction(reliability, "SIGNAL_RELIABILITY", HALF, ONE)
    return p if s == v else ONE - p


def posterior_after_private_signal(public_prior, signal, reliability):
    """Posterior given previous public *actions* and own new private signal."""
    prior, p = _parameters(public_prior, reliability)
    top = prior * likelihood_private_signal(signal, 1, p)
    bottom = (ONE - prior) * likelihood_private_signal(signal, 0, p)
    return top / (top + bottom)


def adopt_probability_given_signal(public_prior, signal, reliability):
    """Tie broken by an independent fair coin, as in original Sec II.A."""
    belief = posterior_after_private_signal(public_prior, signal, reliability)
    if belief > HALF:
        return ONE
    if belief < HALF:
        return Fraction(0)
    return HALF


def action_one_conditional_on_state(public_prior, hidden_state, reliability):
    """P(public action=1 | V, public history) integrates hidden signal AND coin."""
    prior, p = _parameters(public_prior, reliability)
    v = _state_or_binary(hidden_state, "HIDDEN_STATE")
    return sum(
        (likelihood_private_signal(s, v, p) *
         adopt_probability_given_signal(prior, s, p) for s in (0, 1)),
        Fraction(0)
    )


def action_likelihoods(public_prior, public_action, reliability):
    """(P(a|V=1, history), P(a|V=0, history))."""
    prior, p = _parameters(public_prior, reliability)
    a = _state_or_binary(public_action, "PUBLIC_ACTION")
    k1 = action_one_conditional_on_state(prior, 1, p)
    k0 = action_one_conditional_on_state(prior, 0, p)
    return (k1, k0) if a == 1 else (ONE - k1, ONE - k0)


def bayes_public_action_update(public_prior, public_action, reliability):
    """Return updated P(V=1|all actions) and action's mixture probability."""
    prior, p = _parameters(public_prior, reliability)
    l1, l0 = action_likelihoods(prior, public_action, p)
    numerator = prior * l1
    denominator = numerator + (ONE - prior) * l0
    if denominator == 0:
        raise CascadeEvidenceError("R115_ACTION_IMPOSSIBLE_AT_PUBLIC_HISTORY")
    return numerator / denominator, denominator


def trace_public_actions(actions, reliability, initial_prior=HALF):
    """Return exact posterior progression; only observed actions, no private IDs."""
    prior, p = _parameters(initial_prior, reliability)
    progression = [prior]
    likelihoods = []
    for action in actions:
        prior, mass = bayes_public_action_update(prior, action, p)
        progression.append(prior)
        likelihoods.append(mass)
    return tuple(progression), tuple(likelihoods)


def cascade_action(public_prior, reliability):
    """Return forced adopt 1 / reject 0, or None if private signal matters.

    A valid cascade is DETERMINISTIC under either possible private signal.
    """
    prior, p = _parameters(public_prior, reliability)
    low = adopt_probability_given_signal(prior, 0, p)
    high = adopt_probability_given_signal(prior, 1, p)
    if low == high == ONE:
        return 1
    if low == high == 0:
        return 0
    return None


def history_likelihood_given_state(actions, hidden_state, reliability):
    """P(ordered public action history | fixed V), with endogenous actions."""
    v = _state_or_binary(hidden_state, "HIDDEN_STATE")
    _, p = _parameters(HALF, reliability)
    prior = HALF
    conditional = ONE
    for action in actions:
        l1, l0 = action_likelihoods(prior, action, p)
        conditional *= l1 if v == 1 else l0
        prior, _ = bayes_public_action_update(prior, action, p)
    return conditional


def enumerate_public_histories(n, reliability):
    """Exact ex-ante joint masses over feasible public action histories length n."""
    if type(n) is not int or not 0 <= n <= 12:
        raise CascadeEvidenceError("R115_HISTORY_LENGTH_MUST_BE_INT_0_TO_12")
    _, p = _parameters(HALF, reliability)
    states = {(): (HALF, ONE)}
    for _ in range(n):
        nxt = {}
        for hist, (prior, joint_mass) in states.items():
            for action in (0, 1):
                try:
                    new_prior, mass = bayes_public_action_update(prior, action, p)
                except CascadeEvidenceError as e:
                    if str(e) == "R115_ACTION_IMPOSSIBLE_AT_PUBLIC_HISTORY":
                        continue
                    raise
                nxt[hist + (action,)] = (new_prior, joint_mass * mass)
        states = nxt
    if sum((weight for _,weight in states.values()),Fraction(0)) != ONE:
        raise CascadeEvidenceError("R115_EXACT_HISTORY_PROBABILITIES_NOT_NORMALIZED")
    return states


def ex_ante_cascade_masses_after_n(n, reliability):
    """Probability a cascade applies to agent n+1, by directional type."""
    states = enumerate_public_histories(n, reliability)
    p = _fraction(reliability, "SIGNAL_RELIABILITY", HALF, ONE)
    total = {0:Fraction(0), 1:Fraction(0), None:Fraction(0)}
    for prior, joint_prob in states.values():
        total[cascade_action(prior, p)] += joint_prob
    assert sum(total.values(), Fraction(0)) == ONE
    return {
        "up_cascade":total[1],
        "down_cascade":total[0],
        "no_cascade":total[None],
    }


def author_equation_1_even_n(n, reliability):
    """Original 1992 p.997 Eq (1) ex-ante cascade masses, even n only."""
    if type(n) is not int or not 2 <= n <= 12 or n % 2:
        raise CascadeEvidenceError("R115_ORIGINAL_EQ1_REQUIRES_EVEN_2_TO_12")
    p = _fraction(reliability, "SIGNAL_RELIABILITY", HALF, ONE)
    no = (p - p*p) ** (n // 2)
    return {
        "up_cascade":(ONE - no) / 2,
        "down_cascade":(ONE - no) / 2,
        "no_cascade":no,
    }


def first_two_identical_adoption_posterior(reliability):
    """Exact original source model with fair 2nd-person tie."""
    p = _fraction(reliability, "SIGNAL_RELIABILITY", HALF, ONE)
    numerator = p * (ONE + p)
    denominator = numerator + (ONE - p) * (2 - p)
    return numerator / denominator


def naive_two_actions_as_two_independent_high_signals(reliability):
    """PURPOSELY WRONG: counts a publicly observed action as private H signal."""
    p = _fraction(reliability, "SIGNAL_RELIABILITY", HALF, ONE)
    return p*p / (p*p + (ONE - p)**2)


def diagnostic_exact_receipt():
    p = Fraction(7, 10)
    history = (1, 1, 1)
    trace, masses = trace_public_actions(history, p)
    exact_after2 = first_two_identical_adoption_posterior(p)
    return {
        "research_id":"R115",
        "phase":"A",
        "model_source":"Bikhchandani Hirshleifer Welch (1992) JPE 100(5):992-1026 pp996-997",
        "source_DOI":"10.1086/261849",
        "signal_reliability":"7/10",
        "posterior_after_actions_1_1":str(trace[2]),
        "after_third_cascade_action_posterior":str(trace[3]),
        "correct_analytical_after_two":"119/158",
        "naive_double_count_two_observed_actions":str(naive_two_actions_as_two_independent_high_signals(p)),
        "third_action_new_information":False,
        "wrong_up_cascade_given_V0_after_two":str(history_likelihood_given_state((1,1),0,p)),
        "equation_1_n2":{k:str(v) for k,v in author_equation_1_even_n(2,p).items()},
        "equation_1_n4":{k:str(v) for k,v in author_equation_1_even_n(4,p).items()},
        "equation_1_n6":{k:str(v) for k,v in author_equation_1_even_n(6,p).items()},
        "original_human_E2_records":0,
        "synthetic_mathematical_replication_only":True,
        "PESEN_v0_1":"FROZEN",
        "R073":"FROZEN",
    }


if __name__ == "__main__":
    print(json.dumps(diagnostic_exact_receipt(), sort_keys=True, indent=2))
