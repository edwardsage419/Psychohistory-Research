#!/usr/bin/env python3
"""R112 Bayesian belief updates: finite hypotheses and beta-Bernoulli conjugacy.

Pure standard library, mathematics and synthetic fixtures only.
Observed-event likelihoods are discrete probabilities in [0,1].
They are conditional on the complete available previous evidence history.
"""
from __future__ import annotations
import math
from dataclasses import dataclass


class EvidenceError(ValueError):
    """Impossible or malformed evidence and prior support."""


def _simplex(prior):
    values = tuple(prior)
    if not values:
        raise EvidenceError("R112_EMPTY_HYPOTHESIS_SPACE")
    if any(type(v) not in (float, int) or not math.isfinite(v) or v < 0
           for v in values):
        raise EvidenceError("R112_PRIOR_MUST_BE_FINITE_NONNEGATIVE")
    total = math.fsum(values)
    if not math.isfinite(total) or total <= 0:
        raise EvidenceError("R112_PRIOR_ZERO_OR_NONFINITE_MASS")
    return tuple(v / total for v in values)


def _likelihoods(likelihoods, length):
    values = tuple(likelihoods)
    if len(values) != length:
        raise EvidenceError("R112_LIKELIHOOD_DIMENSIONS_DIFFER")
    if any(type(v) not in (float, int) or not math.isfinite(v) or v < 0 or v > 1
           for v in values):
        raise EvidenceError("R112_DISCRETE_LIKELIHOOD_OUTSIDE_0_1")
    return values


def posterior(prior, likelihoods):
    """P(H_i|e) proportional to P(H_i) P(e|H_i), stable for rare evidence.

    A zero prior hypothesis remains unsupported by finite likelihoods.
    Raises on evidence with exactly zero probability under every supported H.
    """
    weights = _simplex(prior)
    lik = _likelihoods(likelihoods, len(weights))
    logs = [math.log(p) + math.log(l) if p > 0 and l > 0 else -math.inf
            for p, l in zip(weights, lik)]
    pivot = max(logs)
    if pivot == -math.inf:
        raise EvidenceError("R112_OBSERVED_EVENT_IMPOSSIBLE_UNDER_PRIOR")
    exp_weights = [math.exp(v - pivot) if v != -math.inf else 0.
                   for v in logs]
    denom = math.fsum(exp_weights)
    answer = tuple(v / denom for v in exp_weights)
    if not all(math.isfinite(x) and 0 <= x <= 1 for x in answer):
        raise EvidenceError("R112_INVALID_POSTERIOR_PROBABILITIES")
    return answer


def sequential_posterior(prior, conditional_likelihood_rows):
    """Each row is P(E_t=e_t | H_i, E_1=e_1,...,E_{t-1}=e_{t-1}).

    Callers MUST condition on previous evidence. The function cannot determine
    independence from supplied numeric rows.
    """
    p = _simplex(prior)
    for likelihood_row in conditional_likelihood_rows:
        p = posterior(p, likelihood_row)
    return p


def binary_likelihood_ratio_prior(prior_h1, p_e_h1, p_e_h0):
    """Return P(H1|E) and its evidence Bayes factor, for supported priors.

    The factor is unavailable if denominator zero and numerator positive;
    infinity is a mathematically meaningful limit, not an estimator.
    """
    if type(prior_h1) not in (int, float) or not 0 < prior_h1 < 1:
        raise EvidenceError("R112_ODDS_PRIOR_MUST_BE_STRICTLY_INTERIOR")
    evidence = _likelihoods((p_e_h1, p_e_h0), 2)
    result = posterior((prior_h1, 1-prior_h1), evidence)[0]
    bayes_factor = (math.inf if evidence[1] == 0 and evidence[0] > 0
                    else evidence[0] / evidence[1] if evidence[1] > 0
                    else math.nan)
    # Both evidence probabilities zero was already denied by posterior.
    return {"posterior_H1": result, "Bayes_factor_e": bayes_factor}


@dataclass(frozen=True)
class BetaBernoulli:
    """Beta(a,b) prior for fixed theta and Bernoulli conditional i.i.d. data."""

    alpha: float
    beta: float

    def __post_init__(self):
        if (type(self.alpha) not in (float, int) or
                type(self.beta) not in (float, int) or
                not math.isfinite(self.alpha) or not math.isfinite(self.beta) or
                self.alpha <= 0 or self.beta <= 0):
            raise EvidenceError("R112_BETA_SHAPE_PARAMETERS_STRICTLY_POSITIVE")

    def update(self, observation):
        if type(observation) is not int or observation not in (0,1):
            raise EvidenceError("R112_BERNOULLI_OBSERVATION_MUST_BE_INT_0_1")
        return BetaBernoulli(self.alpha + observation,
                             self.beta + 1 - observation)

    def update_counts(self, successes, failures):
        if (type(successes) is not int or type(failures) is not int or
                successes < 0 or failures < 0):
            raise EvidenceError("R112_COUNTS_MUST_BE_NONNEGATIVE_INTEGERS")
        return BetaBernoulli(self.alpha + successes, self.beta + failures)

    def predictive_next_one(self):
        return self.alpha / (self.alpha + self.beta)

    def predictive_variance_theta(self):
        s = self.alpha + self.beta
        return self.alpha * self.beta / (s*s*(s+1))

    def log_sequence_marginal(self, observations):
        """P(ordered Bernoulli data), marginalized over one fixed theta.

        With beta-Bernoulli conditional i.i.d. observations, sequence marginal
        is B(a+s,b+f)/B(a,b), with no binomial combination factor.
        """
        n_success = n_failure = 0
        for z in observations:
            if type(z) is not int or z not in (0,1):
                raise EvidenceError("R112_BERNOULLI_OBSERVATION_MUST_BE_INT_0_1")
            if z == 1:
                n_success += 1
            else:
                n_failure += 1
        a,b = self.alpha,self.beta
        return (math.lgamma(a+n_success)+math.lgamma(b+n_failure)
                -math.lgamma(a+b+n_success+n_failure)
                -math.lgamma(a)-math.lgamma(b)+math.lgamma(a+b))


def duplicated_evidence_counterexample():
    """Second report is a deterministic copy of first: LR of second is one."""
    first = posterior((0.5,0.5),(0.9,0.1))
    correct = sequential_posterior((0.5,0.5),((0.9,0.1),(1.,1.)))
    naive = sequential_posterior((0.5,0.5),((0.9,0.1),(0.9,0.1)))
    return {
        "first_posterior_H1":first[0],
        "correct_duplicate_conditioned_H1":correct[0],
        "independence_assumed_duplicate_H1":naive[0],
        "assumption":"second evidence is perfectly copied, conditional likelihoods=(1,1)",
        "synthetic_only":True,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(duplicated_evidence_counterexample(), sort_keys=True))
