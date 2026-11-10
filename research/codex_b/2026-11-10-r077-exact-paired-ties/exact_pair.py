"""Exact paired Brier arithmetic, with no model fitting or tolerance tie rule.

Caller supplies exact source-derived probabilities for the SAME binary target.
This module cannot authenticate their origin or infer whether they leak a label.
No archived implementation imported; no rows/IDs are included in the summary.
"""
from fractions import Fraction
import math

PAIR_FIELDS = {"Brier_delta_all_original_sessions_equal", "sessions_better", "sessions_equal",
               "sessions_worse", "sessions", "per_treatment"}
GROUP_FIELDS = {"sessions", "Brier_delta", "better", "equal", "worse"}


def _require(condition, reason):
    if not condition:
        raise ValueError(reason)


def session_risks(records):
    """Fraction means and sign for records (y,p_candidate,p_reference)."""
    _require(isinstance(records, (list, tuple)) and bool(records), "EMPTY_OR_INVALID_RECORDS")
    candidate = reference = Fraction(0)
    for record in records:
        _require(isinstance(record, (tuple, list)) and len(record) == 3, "INVALID_RECORD_WIDTH")
        y, pc, pr = record
        _require(type(y) is int and y in (0, 1), "INVALID_BINARY_OUTCOME")
        _require(type(pc) is Fraction and type(pr) is Fraction and 0 < pc < 1 and 0 < pr < 1,
                 "EXACT_INTERIOR_PROBABILITIES_REQUIRED")
        candidate += (pc-y)**2
        reference += (pr-y)**2
    candidate /= len(records)
    reference /= len(records)
    delta = candidate-reference
    return {"candidate_Brier": candidate, "reference_Brier": reference, "delta": delta,
            "direction": "better" if delta < 0 else "worse" if delta > 0 else "equal"}


def summarize(sessions):
    """Average sessions equally, retaining R077's two-treatment comparison shape."""
    _require(type(sessions) is dict and bool(sessions), "EMPTY_OR_INVALID_SESSIONS")
    risks = []
    groups = {0: [], 1: []}
    for info in sessions.values():
        _require(type(info) is dict and set(info) == {"treatment", "records"}, "INVALID_SESSION_FIELDS")
        treatment = info["treatment"]
        _require(type(treatment) is int and treatment in (0, 1), "INVALID_TREATMENT")
        risk = session_risks(info["records"])
        risks.append(risk)
        groups[treatment].append(risk)
    _require(all(groups.values()), "BOTH_TREATMENTS_REQUIRED")

    def mean(values):
        return sum(values, Fraction(0))/len(values)

    def group_summary(entries):
        return {"sessions": len(entries), "Brier_delta": mean([r["delta"] for r in entries]),
                "better": sum(r["delta"] < 0 for r in entries),
                "equal": sum(r["delta"] == 0 for r in entries),
                "worse": sum(r["delta"] > 0 for r in entries)}

    overall = group_summary(risks)
    return {
        "candidate_macro_Brier": mean([r["candidate_Brier"] for r in risks]),
        "reference_macro_Brier": mean([r["reference_Brier"] for r in risks]),
        "paired": {
            "Brier_delta_all_original_sessions_equal": overall["Brier_delta"],
            "sessions_better": overall["better"], "sessions_equal": overall["equal"],
            "sessions_worse": overall["worse"], "sessions": overall["sessions"],
            "per_treatment": {str(tr): group_summary(entries) for tr, entries in groups.items()},
        },
    }


def as_float_pair(pair):
    """Representation adapter for tests/legacy JSON comparison, not a classifier."""
    if type(pair) is dict:
        return {key: as_float_pair(value) for key, value in pair.items()}
    return float(pair) if type(pair) is Fraction else pair


def validate_legacy_pair(actual, exact):
    """Compare an original pair to a trusted paired tree from summarize().

    2e-12 only bounds float DELTA representation error. All vote counts/types must
    match exact rational signs; no epsilon ever classifies a pair as tied.
    This does not authenticate externally supplied expected numerical values.
    """
    reason = "PAIRED_DIRECTION_MISMATCH"
    _require(type(exact) is dict and set(exact) == PAIR_FIELDS, reason)
    _require(type(exact["sessions"]) is int and exact["sessions"] > 0, reason)
    groups = exact["per_treatment"]
    _require(type(groups) is dict and set(groups) == {"0", "1"}, reason)
    for group in groups.values():
        _require(type(group) is dict and set(group) == GROUP_FIELDS, reason)
        _require(type(group["sessions"]) is int and group["sessions"] > 0, reason)

    def compare(found, wanted):
        if type(wanted) is dict:
            _require(type(found) is dict and set(found) == set(wanted), reason)
            for key, value in wanted.items(): compare(found[key], value)
        elif type(wanted) is Fraction:
            _require(type(found) is float and math.isfinite(found) and abs(found-float(wanted)) <= 2e-12, reason)
        else:
            _require(type(wanted) is int and type(found) is int and found == wanted, reason)

    compare(actual, exact)
