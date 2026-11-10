"""Independent synthetic-only R077 scoring oracle; no archived code imported.

History-bin sufficient statistics, exact rational squared loss and Decimal log
loss replace the original rowwise float scoring route. This new verification
algorithm is not claimed as the original authors' method or external replication.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import math

STATE_INDICES = {
    "M1_OWN_LAST": (0,), "M2_OPPONENT_LAST": (1,),
    "M3_JOINT_LAST": (0, 1), "M4_JOINT_TWO_LAGS": (0, 1, 2, 3),
}
MODELS = ("M0_TREATMENT_PREVALENCE", *STATE_INDICES, "M5_TFT_NOISY", "M6_WSLS_NOISY")
PAIRS = ((MODELS[3], MODELS[1]), (MODELS[4], MODELS[3]),
         (MODELS[1], MODELS[0]), (MODELS[2], MODELS[0]),
         (MODELS[5], MODELS[0]), (MODELS[6], MODELS[0]))
PUBLIC_FIELDS = {"models", "paired_differences", "original_session_count",
                 "scored_t3_human_events", "target_labels_used_in_training",
                 "all_raw_sessions_and_action_sequences_exported"}


def _require(condition, reason):
    if not condition:
        raise ValueError(reason)


def _validate_fit(fit):
    _require(type(fit) is dict and {"train_only_prevalence", "state_counts"} <= set(fit), "SOURCE_FIT_FIELDS")
    p0 = fit["train_only_prevalence"]
    _require(type(p0) is float and math.isfinite(p0) and 0 < p0 < 1, "SOURCE_PREVALENCE")
    tables = fit["state_counts"]
    _require(type(tables) is dict and set(tables) == set(STATE_INDICES), "SOURCE_MODEL_TABLES")
    for model, table in tables.items():
        _require(type(table) is dict, "SOURCE_STATE_TABLE")
        for state, counts in table.items():
            _require(type(state) is tuple and len(state) == len(STATE_INDICES[model])
                     and all(type(x) is int and x in (0, 1) for x in state), "SOURCE_STATE_KEY")
            _require(type(counts) is tuple and len(counts) == 2
                     and all(type(x) is int for x in counts)
                     and 0 <= counts[0] <= counts[1] and counts[1] > 0, "SOURCE_STATE_COUNTS")


def _probability(fit, model, event):
    p0 = Fraction(str(fit["train_only_prevalence"]))
    if model == MODELS[0]:
        return p0
    if model in STATE_INDICES:
        state = tuple(event[i] for i in STATE_INDICES[model])
        positive, count = fit["state_counts"][model].get(state, (0, 0))
        return (positive + 20*p0) / (count + 20)
    if model == MODELS[5]:
        return Fraction(19 if event[1] else 1, 20)
    if model == MODELS[6]:
        return Fraction(19 if event[0] == event[1] else 1, 20)
    raise ValueError("UNKNOWN_MODEL")


def source_probability(fit, model, event):
    _validate_fit(fit)
    _require(isinstance(event, (tuple, list)) and len(event) == 5
             and all(type(x) is int and x in (0, 1) for x in event), "INVALID_EVENT")
    return _probability(fit, model, event)


def expected_scores(fit, sessions):
    """Full public score tree. Synthetic histories are assumed already extracted.

Only source p0 and source counts enter probability; current outcomes enter the
loss bins. This does not authenticate a source dataset or reconstruct timelines.
"""
    _validate_fit(fit)
    _require(type(sessions) is dict and bool(sessions), "EMPTY_SESSIONS")
    groups = {0: [], 1: []}
    histograms = {}
    total_events = 0
    for session, info in sessions.items():
        _require(type(info) is dict and set(info) == {"treatment", "events"}, "SESSION_FIELDS")
        treatment = info["treatment"]
        _require(type(treatment) is int and treatment in (0, 1), "SESSION_TREATMENT")
        events = info["events"]
        _require(isinstance(events, (list, tuple)) and bool(events), "EMPTY_EVENTS")
        bins = Counter()
        for event in events:
            _require(isinstance(event, (tuple, list)) and len(event) == 5
                     and all(type(x) is int and x in (0, 1) for x in event), "INVALID_EVENT")
            bins[tuple(event)] += 1
        histograms[session] = bins
        groups[treatment].append(session)
        total_events += len(events)
    _require(all(groups.values()), "BOTH_TREATMENTS_REQUIRED")

    def mean(values):
        return sum(values) / len(values)

    with localcontext() as context:
        context.prec = 70
        scores = {}
        for session, bins in histograms.items():
            scores[session] = {}
            n = sum(bins.values())
            for model in MODELS:
                squared = Fraction(0)
                logarithmic = Decimal(0)
                for event, mass in bins.items():
                    p = _probability(fit, model, event)
                    observed_probability = p if event[4] else 1-p
                    squared += mass * (1-observed_probability)**2
                    logarithmic -= mass * (Decimal(observed_probability.numerator)
                                            / observed_probability.denominator).ln()
                scores[session][model] = (squared/n, logarithmic/n)
        models = {}
        names = list(sessions)
        for model in MODELS:
            models[model] = {
                "all_original_sessions_equal_Brier": mean([scores[s][model][0] for s in names]),
                "all_original_sessions_equal_log_loss": mean([scores[s][model][1] for s in names]),
                "per_treatment_original_session_equal": {
                    str(tr): {
                        "original_sessions": len(ids),
                        "Brier": mean([scores[s][model][0] for s in ids]),
                        "log_loss": mean([scores[s][model][1] for s in ids]),
                    } for tr, ids in groups.items()
                },
            }
        pairs = {}
        for model, reference in PAIRS:
            differences = {s: scores[s][model][0]-scores[s][reference][0] for s in names}
            values = list(differences.values())
            pairs[model+"_VS_"+reference] = {
                "Brier_delta_all_original_sessions_equal": mean(values),
                "sessions_better": sum(d < 0 for d in values),
                "sessions_equal": sum(d == 0 for d in values),
                "sessions_worse": sum(d > 0 for d in values), "sessions": len(names),
                "per_treatment": {
                    str(tr): {
                        "sessions": len(ids), "Brier_delta": mean([differences[s] for s in ids]),
                        "better": sum(differences[s] < 0 for s in ids),
                        "equal": sum(differences[s] == 0 for s in ids),
                        "worse": sum(differences[s] > 0 for s in ids),
                    } for tr, ids in groups.items()
                },
            }
    return {
        "models": models, "paired_differences": pairs,
        "original_session_count": len(names), "scored_t3_human_events": total_events,
        "target_labels_used_in_training": 0, "all_raw_sessions_and_action_sequences_exported": False,
    }


def validate_scores(actual, expected):
    """Exact keys/counts/types, absolute numeric tolerance 2e-12, never NaN PASS."""
    _require(type(expected) is dict and set(expected) == PUBLIC_FIELDS
             and expected["original_session_count"] > 0, "EMPTY_OR_INVALID_EXPECTATION")

    def compare(found, wanted, path):
        reason = "SCORE_MISMATCH:"+path
        if type(wanted) is dict:
            _require(type(found) is dict and set(found) == set(wanted), reason)
            return sum(compare(found[k], value, path+"."+str(k)) for k, value in wanted.items())
        if type(wanted) in (bool, int):
            _require(type(found) is type(wanted) and found == wanted, reason)
        else:
            _require(isinstance(wanted, (Fraction, Decimal)), "UNSUPPORTED_EXPECTATION")
            _require(type(found) is float and math.isfinite(found)
                     and abs(found-float(wanted)) <= 2e-12, reason)
        return 1

    return compare(actual, expected, "root")


def check_scorer(scorer, fit, sessions):
    expected = expected_scores(fit, sessions)
    actual = scorer(fit, sessions)
    return validate_scores(actual, expected)
