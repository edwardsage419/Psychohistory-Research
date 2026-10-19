#!/usr/bin/env python3
"""R118: Granovetter (1978) global binary participation thresholds, finite version.

First-party original text: AJS 83(6):1420-1443, pp1422,1424-1426,
doi:10.1086/226707. This is a mathematical reconstruction with no real
human actions, and NO network adjacency, withdrawals, inference of motives,
multi-equilibrium selection, or prospective historical forecast.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json


SOURCE_DOI = "10.1086/226707"


class ThresholdModelError(ValueError):
    """Fail closed on inadmissible or inconsistent finite crowd input."""


def _thresholds(values):
    """Accept only explicit finite anonymous threshold vectors, 1<=n<=2000."""
    if type(values) not in (tuple, list):
        raise ThresholdModelError("R118_EXPLICIT_TUPLE_OR_LIST_REQUIRED")
    size = len(values)
    if not 1 <= size <= 2000:
        raise ThresholdModelError("R118_GROUP_SIZE_MUST_BE_1_TO_2000")
    if any(type(k) is not int or not 0 <= k <= size for k in values):
        raise ThresholdModelError("R118_INTEGER_THRESHOLD_MUST_BE_0_TO_N")
    return tuple(values)


@dataclass(frozen=True)
class ParticipationResult:
    """From zero participants, monotone and no removals."""
    size: int
    final_participants: int
    counts_from_initial_zero: tuple[int, ...]
    activation_rounds: int
    source_model: str = "global_observable_one_time_no_withdrawal"

    @property
    def participation_fraction(self):
        return Fraction(self.final_participants, self.size)


def threshold_cdf_count(thresholds, currently_active):
    """Granovetter r(t+1)=F[r(t)] represented in exact finite counts."""
    values = _thresholds(thresholds)
    if type(currently_active) is not int or not 0 <= currently_active <= len(values):
        raise ThresholdModelError("R118_CDF_INPUT_COUNT_INVALID")
    return sum(k <= currently_active for k in values)


def synchronous_participation(thresholds):
    """Parallel entry, original participation threshold model, no exits.

    Each nonparticipant joins if at least theta OTHER actors have already
    joined. Existing participants remain. Starts without arbitrary seeds;
    theta=0 actors autonomously act. Counts include the initial zero stage.
    """
    values = _thresholds(thresholds)
    n = len(values)
    active = set()
    trajectory = [0]
    while True:
        k = len(active)
        newcomers = {i for i,theta in enumerate(values)
                     if i not in active and theta <= k}
        if not newcomers:
            break
        active.update(newcomers)
        if len(active) <= k or len(active) > n:
            raise ThresholdModelError("R118_MONOTONE_BOUND_INVARIANT_BROKEN")
        trajectory.append(len(active))
        if len(trajectory) > n + 1:
            raise ThresholdModelError("R118_NONTERMINATING_CASCADE")
    if trajectory[-1] != len(active):
        raise ThresholdModelError("R118_PARTICIPATION_COUNT_MISMATCH")
    return ParticipationResult(
        size=n,
        final_participants=len(active),
        counts_from_initial_zero=tuple(trajectory),
        activation_rounds=len(trajectory)-1,
    )


def independently_sorted_minimal_closure(thresholds):
    """Independent sorted-threshold bootstrap, does NOT call synchronous solver.

    Given sorted theta(0)..theta(n-1), exactly k participants can be reached
    from zero iff all theta(j)<=j for j<k. First failure stops activation.
    """
    values = _thresholds(thresholds)
    ordered = sorted(values)
    k = 0
    for value in ordered:
        if value > k:
            break
        k += 1
    return k


def verify_both_solvers(thresholds):
    """Independent implementations must yield the same minimal reachable size."""
    values = _thresholds(thresholds)
    primary = synchronous_participation(values)
    independent = independently_sorted_minimal_closure(values)
    if primary.final_participants != independent:
        raise ThresholdModelError("R118_INDEPENDENT_ALGORITHMS_DISAGREE")
    if primary.final_participants != threshold_cdf_count(values, primary.final_participants):
        raise ThresholdModelError("R118_FIXED_POINT_CONDITION_NOT_SATISFIED")
    return primary


def original_author_one_threshold_counterexample():
    """1978 pp1424-25: 100 agents, change ONLY theta 1 -> theta 2."""
    chain = tuple(range(100))
    broken = tuple(2 if k == 1 else k for k in chain)
    x = verify_both_solvers(chain)
    y = verify_both_solvers(broken)
    return {
        "original_paper_source_DOI": SOURCE_DOI,
        "group_size": 100,
        "chain_final": x.final_participants,
        "broken_chain_final": y.final_participants,
        "modified_people_count": sum(a!=b for a,b in zip(chain,broken)),
        "original_threshold_sum":sum(chain),
        "broken_threshold_sum":sum(broken),
        "original_initial_to_terminal_count_trajectory": list(x.counts_from_initial_zero),
        "broken_initial_to_terminal_count_trajectory": list(y.counts_from_initial_zero),
        "mathematical_reconstruction_not_observed_human_behavior":True,
    }


def same_mean_different_collective_outcome():
    """Own NEW analytic counterexample, not source-author's 1978 example.

    Compared with 0..99, replace theta1 by2 AND theta99 by98. Both groups
    have same EXACT mean49.5 but chain 100 vs broken 1 participants.
    """
    original = tuple(range(100))
    compensated = tuple(2 if k==1 else 98 if k==99 else k for k in original)
    a = verify_both_solvers(original)
    b = verify_both_solvers(compensated)
    mean_a = Fraction(sum(original),100)
    mean_b = Fraction(sum(compensated),100)
    if mean_a != mean_b or a.final_participants != 100 or b.final_participants != 1:
        raise ThresholdModelError("R118_PREDEFINED_SAME_MEAN_EXAMPLE_INVALID")
    return {
        "original_mean_exact":str(mean_a),
        "compensated_mean_exact":str(mean_b),
        "original_threshold_sum":sum(original),
        "compensated_threshold_sum":sum(compensated),
        "modified_people_count":sum(x!=y for x,y in zip(original,compensated)),
        "original_final_participants":a.final_participants,
        "compensated_final_participants":b.final_participants,
        "constructed_by_project_not_source_author":True,
        "individual_threshold_reasons_or_real_human_data_inferred":False,
    }


def exhaustive_small_groups(max_n=5):
    """All ordered integer threshold vectors for every n=1..max_n.

    Strict tiny limits prevent combinatorial accidental resource abuse.
    Each n has (n+1)^n vectors. Test counts are not empirical observations.
    """
    if type(max_n) is not int or not 1 <= max_n <= 5:
        raise ThresholdModelError("R118_EXHAUSTIVE_SIZE_MUST_BE_1_TO_5")
    counts = {}
    for n in range(1,max_n+1):
        verified = 0
        for values in product(range(n+1),repeat=n):
            result = verify_both_solvers(values)
            trace = result.counts_from_initial_zero
            if trace[0] != 0 or trace[-1] != result.final_participants:
                raise ThresholdModelError("R118_EXHAUSTIVE_TRACE_ENDPOINT_INVALID")
            if any(y<=x for x,y in zip(trace, trace[1:])):
                raise ThresholdModelError("R118_EXHAUSTIVE_NOT_STRICTLY_GROWING")
            verified += 1
        assert verified == (n+1)**n
        counts[str(n)] = verified
    return counts


def study_receipt():
    classic = original_author_one_threshold_counterexample()
    mean = same_mean_different_collective_outcome()
    return {
        "research_id":"R118","phase":"A",
        "source_DOI":SOURCE_DOI,
        "first_party_printed_pages":[1422,1424,1425,1426],
        "original_author_100person_counterexample":classic,
        "new_project_same_mean_counterexample":mean,
        "source_1978_threshold_definition":"integer number of other participants required",
        "full_history_exhaustive_deterministic_counts_up_to_n5":exhaustive_small_groups(),
        "original_human_E2_score_observations":0,
        "source_mathematical_mechanism_not_empirical_fit":True,
        "no_network_or_dropout_assumed":True,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(study_receipt(),indent=2,sort_keys=True))
