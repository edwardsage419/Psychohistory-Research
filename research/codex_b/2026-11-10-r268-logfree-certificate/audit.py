"""R268 scoped exact decision/probability/S64 audit; no archived code imported.

Floating scalar log/AIC/BIC VALUE errors are not independently certified here.
Their finite representation is checked; native byte replay is a separate record.
This is not a new full scientific-acceptance or historical-provenance certificate.
"""
import argparse
import csv
from fractions import Fraction as F
import hashlib
import io
import json
import math
from pathlib import Path
import re

from certificate import PS, SIZES, METHODS, certify, world_metrics, require

FIELDS = ("world", "true_p", "n", "original_ordered_binary_sequence", "original_success_count",
          "exact_source_probability", "maximum_likelihood_qhat", "log_likelihood_M0",
          "log_likelihood_M1", "deviance_gain", "AIC_M0", "AIC_M1", "BIC_M0", "BIC_M1",
          "AIC_selected", "BIC_selected", "criteria_disagree")
FLOAT_FIELDS = FIELDS[7:14]
CORE_META = {
    "research_id": "R268", "original_catalogue_id": "11-028",
    "prescore_freeze_commit": "6ab880be304cebf916948aa9877e6d233b6a5e69",
    "scope": "E1_ARTIFICIAL_COMPLETE_ORDERED_BERNOULLI_AIC_BIC", "complete_source_types": 3312,
    "all_nine_independent_binomial_decision_probabilities_verified": True,
    "numerical_logs_used_while_source_probabilities_are_exact_Fraction": True,
    "frozen_M0_parameter_count": 0, "frozen_M1_parameter_count": 1, "frozen_M0_q": "1/5",
    "all_parameter_border_cases_handled": True, "no_out_of_sample_predictive_superiority_claim": True,
    "new_real_human_E2": 0, "new_real_historical_E3": 0, "R073": "FROZEN", "PESEN_v0_1": "FROZEN",
}
S64_META = {
    "research_id": "R268_S64", "frozen_protocol_commit": "a61edfe2f3f479c2309cbc3e5f1e6757730ed7d4",
    "scope": "E1_ARTIFICIAL_NONBLIND_PROSPECTIVE_ENDPOINT",
    "source_csv_git_blob": "6296528507012dd1d8d11e3556fcdeb7b6aeb2b5",
    "original_selection_json_git_blob": "3d407ddcf524bfc55c0a076d57383c6655a36441",
    "ordered_source_count": 3312, "independent_future_event_types": 6624, "world_count": 9,
    "exact_risk_comparisons": 36, "paired_AIC_BIC_comparisons": 9,
    "source_route": "full_ordered_sequence_and_two_future_outcomes_Fraction_V8",
    "independent_route": "analytic_binomial_and_conditional_Brier_Fraction_V8",
    "native_python_independent_replay": "9_worlds_36_risks_9_differences_equal_V8",
    "new_human_E2": 0, "new_historical_E3": 0, "external_team_replications": 0, "ci": "NOT_RUN",
    "R073": "FROZEN", "PESEN_v0_1": "FROZEN", "strict_receipt_negative_controls_rejected": 5,
}


def loads_strict(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def invalid(_): raise ValueError("NONFINITE_JSON_CONSTANT")
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def fraction(text):
    require(type(text) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", text) is not None, "RATIONAL_FIELD_TYPE")
    return F(text)


def finite_scalar(text):
    require(type(text) is str, "FLOAT_SCALAR_TYPE")
    try: value = float(text)
    except ValueError as exc: raise ValueError("FLOAT_SCALAR_SYNTAX") from exc
    require(math.isfinite(value), "NONFINITE_FLOAT_SCALAR")


def world_id(p, n): return "TRUE_P"+str(p).replace("/", "OF")+"_N"+str(n)


def metadata(document, expected, records):
    require(type(document) is dict and set(document) == set(expected)|{records}, "ROOT_SCHEMA")
    for key, value in expected.items():
        require(type(document[key]) is type(value) and document[key] == value, "FROZEN_METADATA")
    require(type(document[records]) is list and len(document[records]) == 9, "WORLD_COVERAGE")


def key_of(row):
    require(type(row) is dict and {"world", "true_p", "n"} <= set(row), "WORLD_ID_FIELDS")
    require(type(row["n"]) is int and row["n"] in SIZES and type(row["true_p"]) is str and
            row["true_p"] in tuple(map(str, PS)), "UNFROZEN_WORLD")
    p, n = F(row["true_p"]), row["n"]
    require(row["world"] == world_id(p, n), "WORLD_NAME")
    return p, n


def audit(csv_path, core_path, s64_path):
    captured = {"csv": Path(csv_path).read_bytes(), "core": Path(core_path).read_bytes(), "s64": Path(s64_path).read_bytes()}
    core, s64 = loads_strict(captured["core"]), loads_strict(captured["s64"])
    metadata(core, CORE_META, "worlds"); metadata(s64, S64_META, "results")
    proofs = {(n, k): certify(n, k) for n in SIZES for k in range(n+1)}
    metrics = {(p, n): world_metrics(p, n) for p in PS for n in SIZES}
    table = list(csv.reader(io.StringIO(captured["csv"].decode("utf-8"), newline=""), strict=True))
    require(bool(table) and tuple(table[0]) == FIELDS and len(table) == 3313, "CSV_HEADER_OR_COUNT")
    seen = set(); totals = {(p, n): F(0) for p in PS for n in SIZES}; per_world = {key: 0 for key in totals}
    for cells in table[1:]:
        require(len(cells) == len(FIELDS), "CSV_ROW_WIDTH")
        row = dict(zip(FIELDS, cells))
        require(row["n"] in ("4", "6", "10") and row["true_p"] in tuple(map(str, PS)), "CSV_WORLD")
        p, n = F(row["true_p"]), int(row["n"])
        require(row["world"] == world_id(p, n), "CSV_WORLD_NAME")
        bits = row["original_ordered_binary_sequence"]
        require(len(bits) == n and set(bits) <= {"0", "1"}, "CSV_BITS")
        identity = (p, n, bits)
        require(identity not in seen, "DUPLICATE_SOURCE")
        seen.add(identity); k = bits.count("1")
        require(row["original_success_count"] == str(k), "CSV_COUNT")
        mass = p**k*(1-p)**(n-k)
        require(fraction(row["exact_source_probability"]) == mass and fraction(row["maximum_likelihood_qhat"]) == F(k, n), "CSV_MASS_OR_MLE")
        decision = proofs[(n, k)]
        require(row["AIC_selected"] == decision["AIC"] and row["BIC_selected"] == decision["BIC"] and
                row["criteria_disagree"] == str(int(decision["AIC"] != decision["BIC"])), "CSV_DECISION_CERTIFICATE")
        for field in FLOAT_FIELDS: finite_scalar(row[field])
        totals[(p, n)] += mass; per_world[(p, n)] += 1
    require(len(seen) == 3312 and all(totals[key] == 1 and per_world[key] == 2**key[1] for key in totals), "SOURCE_UNIVERSE")
    core_seen = set(); decisions_checked = probability_checks = 0
    world_fields = {"world", "true_p", "n", "full_ordered_original_source_types",
                    "source_weighted_probability_AIC_selects_M1", "source_weighted_probability_BIC_selects_M1",
                    "source_weighted_probability_AIC_BIC_disagree", "independent_binomial_exact_aggregate_verified", "frozen_per_K_decisions"}
    for row in core["worlds"]:
        key = key_of(row); p, n = key
        require(set(row) == world_fields and key not in core_seen, "CORE_WORLD_SCHEMA_OR_DUPLICATE")
        core_seen.add(key)
        require(type(row["full_ordered_original_source_types"]) is int and row["full_ordered_original_source_types"] == 2**n and
                row["independent_binomial_exact_aggregate_verified"] is True, "CORE_COUNT_OR_FLAG")
        for criterion, field in (("AIC", "source_weighted_probability_AIC_selects_M1"), ("BIC", "source_weighted_probability_BIC_selects_M1"), ("disagree", "source_weighted_probability_AIC_BIC_disagree")):
            require(fraction(row[field]) == metrics[key]["selection"][criterion], "CORE_SELECTION_PROBABILITY")
            probability_checks += 1
        decisions = row["frozen_per_K_decisions"]
        require(type(decisions) is dict and set(decisions) == set(map(str, range(n+1))), "CORE_K_COVERAGE")
        for k in range(n+1):
            item = decisions[str(k)]
            require(type(item) is dict and set(item) == {"AIC", "BIC", "deviance_gain"} and
                    item["AIC"] == proofs[(n, k)]["AIC"] and item["BIC"] == proofs[(n, k)]["BIC"], "CORE_DECISION_CERTIFICATE")
            finite_scalar(item["deviance_gain"]); decisions_checked += 1
    require(core_seen == set(metrics), "CORE_WORLD_COVERAGE")
    future_seen = set(); risk_checks = 0
    for row in s64["results"]:
        key = key_of(row); p, n = key
        require(key not in future_seen and set(row) == {"world", "true_p", "n", "ordered_sources", "risk", "excess", "AIC_minus_BIC"}, "S64_WORLD_SCHEMA_OR_DUPLICATE")
        future_seen.add(key)
        require(type(row["ordered_sources"]) is int and row["ordered_sources"] == 2**n, "S64_SOURCE_COUNT")
        for field in ("risk", "excess"):
            require(type(row[field]) is dict and set(row[field]) == set(METHODS), "S64_METHOD_COVERAGE")
            for method in METHODS:
                require(fraction(row[field][method]) == metrics[key][field][method], "S64_RISK_CERTIFICATE")
                risk_checks += 1
        require(fraction(row["AIC_minus_BIC"]) == metrics[key]["AIC_minus_BIC"], "S64_DIFFERENCE_CERTIFICATE")
        risk_checks += 1
    require(future_seen == set(metrics), "S64_WORLD_COVERAGE")
    return {"status": "PASS_EXACT_SELECTION_AND_S64_RISK_CERTIFICATE", "states": len(proofs),
            "source_rows": len(seen), "core_decision_records": decisions_checked,
            "selection_probabilities": probability_checks, "S64_fraction_checks": risk_checks,
            "e2_interval": [str(next(iter(proofs.values()))[field]) for field in ("e2_lower", "e2_upper")],
            "minimum_AIC_margin_lower_bound": str(min(item["AIC_margin_lower_bound"] for item in proofs.values())),
            "minimum_BIC_margin_lower_bound": str(min(item["BIC_margin_lower_bound"] for item in proofs.values())),
            "certificate": list(proofs.values()), "world_metrics": {world_id(*key): value for key, value in metrics.items()},
            "input_snapshot_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in captured.items()},
            "scalar_log_value_error_certification": "NOT_RUN_FINITE_REPRESENTATION_ONLY",
            "historical_flags": "MATCHED_NOT_NEW_SCIENTIFIC_CERTIFICATION", "new_E2_E3": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv"); parser.add_argument("core"); parser.add_argument("s64")
    args = parser.parse_args()
    try: result = audit(args.csv, args.core, args.s64)
    except (OSError, ValueError, UnicodeError, csv.Error, TypeError, KeyError, ZeroDivisionError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)[:120] if isinstance(exc, ValueError) else type(exc).__name__}))
        raise SystemExit(2)
    print(json.dumps(result, default=str, indent=2))
