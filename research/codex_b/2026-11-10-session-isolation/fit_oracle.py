"""Synthetic engineering gate, independent of all archived model implementations.

The expected fit uses a full-treatment contingency table MINUS the heldout table,
then marginalizes its 32 bins. No archived extraction, selection, counting,
state_for, smoothing, or scoring helper is imported. This is a new internal
verification algorithm, not a reproduction of the original authors' algorithm.
"""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import math

STATES = {
    "M1_OWN_LAST": (0,),
    "M2_OPPONENT_LAST": (1,),
    "M3_JOINT_LAST": (0, 1),
    "M4_JOINT_TWO_LAGS": (0, 1, 2, 3),
}
MODELS = ("M0_TREATMENT_PREVALENCE", *STATES, "M5_TFT_NOISY", "M6_WSLS_NOISY")
EVENTS = tuple(product((0, 1), repeat=5))


def expected_fit(sessions, heldout):
    """Return exact sufficient statistics; no probabilities fitted to heldout rows."""
    if not isinstance(sessions, dict) or heldout not in sessions:
        raise ValueError("ORACLE_MISSING_HELDOUT")
    histograms = {}
    treatment_bins = {}
    for name, info in sessions.items():
        if not isinstance(info, dict) or set(info) != {"treatment", "events"}:
            raise ValueError("ORACLE_SESSION_FIELDS")
        if not isinstance(info["events"], (list, tuple)) or not info["events"]:
            raise ValueError("ORACLE_EMPTY_EVENTS")
        bins = [0] * 32
        for event in info["events"]:
            if not isinstance(event, (tuple, list)) or len(event) != 5 or any(
                type(value) is not int or value not in (0, 1) for value in event
            ):
                raise ValueError("ORACLE_INVALID_BINARY_EVENT")
            index = sum(value << (4-i) for i, value in enumerate(event))
            bins[index] += 1
        histograms[name] = bins
        total = treatment_bins.setdefault(info["treatment"], [0] * 32)
        for index, count in enumerate(bins):
            total[index] += count
    treatment = sessions[heldout]["treatment"]
    bins = [a-b for a, b in zip(treatment_bins[treatment], histograms[heldout])]
    count = sum(bins)
    if not count:
        raise ValueError("ORACLE_NO_OTHER_TRAINING_EVENTS")
    prevalence = Fraction(sum(n for e, n in zip(EVENTS, bins) if e[4]), count)
    if not 0 < prevalence < 1:
        raise ValueError("ORACLE_DEGENERATE_TRAINING")
    tables = {}
    for model, indices in STATES.items():
        table = {}
        for state in product((0, 1), repeat=len(indices)):
            selected = [(event[4], n) for event, n in zip(EVENTS, bins)
                        if tuple(event[i] for i in indices) == state]
            total = sum(n for _, n in selected)
            if total:
                table[state] = (sum(y*n for y, n in selected), total)
        tables[model] = table
    return {
        "train_only_prevalence": prevalence,
        "train_target_count": count,
        "trained_from_other_sessions_same_treatment": sum(
            info["treatment"] == treatment for info in sessions.values()) - 1,
        "state_counts": tables,
    }


def probability(oracle, model, event):
    """Frozen alpha=20, reference error=1/20; exact rational arithmetic."""
    p0 = oracle["train_only_prevalence"]
    if model == "M0_TREATMENT_PREVALENCE":
        return p0
    if model in STATES:
        state = tuple(event[i] for i in STATES[model])
        successes, count = oracle["state_counts"][model].get(state, (0, 0))
        return (successes + 20*p0) / (count + 20)
    if model == "M5_TFT_NOISY":
        return Fraction(19 if event[1] else 1, 20)
    if model == "M6_WSLS_NOISY":
        return Fraction(19 if event[0] == event[1] else 1, 20)
    raise ValueError("ORACLE_UNKNOWN_MODEL")


def validate_fit(fitted, oracle):
    """Reject missing/extra fields, wrong types, and any sufficient-statistic error."""
    def require(condition):
        if not condition:
            raise ValueError("FIT_MISMATCH")

    require(type(fitted) is dict and set(fitted) == set(oracle))
    for field in ("train_target_count", "trained_from_other_sessions_same_treatment"):
        require(type(fitted[field]) is int and fitted[field] == oracle[field])
    prevalence = fitted["train_only_prevalence"]
    require(type(prevalence) is float and math.isfinite(prevalence)
            and prevalence == float(oracle["train_only_prevalence"]))
    tables = fitted["state_counts"]
    require(type(tables) is dict and set(tables) == set(STATES))
    for model, expected in oracle["state_counts"].items():
        table = tables[model]
        require(type(table) is dict and set(table) == set(expected))
        for state, counts in table.items():
            require(type(state) is tuple and all(type(x) is int for x in state))
            require(type(counts) is tuple and len(counts) == 2
                    and all(type(x) is int for x in counts) and counts == expected[state])


def check_trainer(trainer, predictor, sessions):
    """Fail-closed differential gate on supplied FICTIONAL sessions, never a scorer.

Every fold is checked before predictions. Flipping heldout and foreign-treatment
labels must leave its fit unchanged. All 32 events cover both current labels for
each feature state, so exact-oracle agreement also tests label independence.
"""
    comparisons = 0
    for heldout, info in sessions.items():
        oracle = expected_fit(sessions, heldout)
        fitted = trainer(sessions, heldout)
        validate_fit(fitted, oracle)
        changed = deepcopy(sessions)
        for name, other in changed.items():
            if name == heldout or other["treatment"] != info["treatment"]:
                other["events"] = [e[:4] + (1-e[4],) for e in other["events"]]
        validate_fit(trainer(changed, heldout), oracle)
        for model in MODELS:
            for event in EVENTS:
                actual = predictor(model, event, fitted)
                expected = probability(oracle, model, event)
                if (type(actual) is not float or not math.isfinite(actual)
                        or not 0 < actual < 1
                        or abs(actual - float(expected)) > 1e-15):
                    raise ValueError("PREDICTION_MISMATCH")
                comparisons += 1
    return {"folds": len(sessions), "prediction_comparisons": comparisons}
