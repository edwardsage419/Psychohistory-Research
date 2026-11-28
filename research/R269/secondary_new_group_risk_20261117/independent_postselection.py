#!/usr/bin/env python3
"""R269: post-selection risk on an independent future GROUP, not a row.

Independent finite rational replay of the archived 6-group, 12-duplicated-row
artificial experiment. Original freeze, fitted models and original score
artifacts remain immutable. The additional selection rule is retrospective
and exploratory. This file does not import the original R269 implementation.

Run from anywhere:
  python -B research/R269/secondary_new_group_risk_20261117/independent_postselection.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "R269_ALL_576_ORIGINAL_CLUSTERED_CV_SOURCE_TYPES.csv"
RESULT = ROOT / "R269_EXACT_RESULTS.json"
SOURCE_SHA256 = "6bc98c0c07c2a6d48184e6a8643dbd515dfa470ba626a10928d90614ce75155d"
RESULT_SHA256 = "d7dda54fdd07148713cd8acbaaafb06bc1282a005b48b09f570211e1a7d4193e"
MODELS = ("GROUP_ID_MEMORIZER", "GLOBAL_LAPLACE", "CONSTANT_HALF")
PS = (F(1, 4), F(1, 2), F(3, 4))
HALF = F(1, 2)
# Fixed exploratory tie-break: Laplace, constant, memorizer. It affects
# neither LOOR choice (unique) nor unseen-risk at LOGO's constant/memo tie.
ORDER = ("GLOBAL_LAPLACE", "CONSTANT_HALF", "GROUP_ID_MEMORIZER")
FIELDS = (
    "world", "predictor", "true_p",
    "original_six_independent_group_latents",
    "original_complete_source_probability", "original_twelve_row_groups",
    "original_twelve_row_outcomes", "loor_row_predictions",
    "loor_row_squared_losses", "loor_average_brier",
    "logo_row_predictions", "logo_row_squared_losses", "logo_average_brier",
)


class IntegrityError(ValueError):
    pass


def require(ok: bool, tag: str) -> None:
    if ok is not True:
        raise IntegrityError(tag)


def canonical_fraction(s: str) -> F:
    x = F(s)
    require(str(x) == s, "NONCANONICAL_FRACTION")
    return x


def brier(p: F, q: F) -> F:
    return p * (1 - q) ** 2 + (1 - p) * q ** 2


def predict(bits: str, model: str, protocol: str) -> tuple[F, ...]:
    k = bits.count("1")
    result = []
    for g, char in enumerate(bits):
        z = int(char)
        if model == "GROUP_ID_MEMORIZER":
            q = F(z) if protocol == "LOOR" else HALF
        elif model == "CONSTANT_HALF":
            q = HALF
        elif model == "GLOBAL_LAPLACE":
            q = F(2 * k - z + 1, 13) if protocol == "LOOR" else F(2 * (k - z) + 1, 12)
        else:
            raise IntegrityError("UNKNOWN_MODEL")
        result.extend((q, q))
    return tuple(result)


def validate_row(row: dict[str, str]) -> tuple[F, str, str, F, F, F]:
    require(set(row) == set(FIELDS), "CSV_SCHEMA")
    p = canonical_fraction(row["true_p"])
    require(p in PS, "FROZEN_P")
    bits = row["original_six_independent_group_latents"]
    require(len(bits) == 6 and set(bits) <= {"0", "1"}, "SOURCE_BITS")
    model = row["predictor"]
    require(model in MODELS, "MODEL_UNIVERSE")
    want_world = "P" + str(p).replace("/", "OF") + "_" + model
    require(row["world"] == want_world, "FROZEN_WORLD")
    require(row["original_twelve_row_groups"] == ";".join(str(i // 2) for i in range(12)),
            "REPEATED_GROUP_IDENTITIES")
    y = tuple(int(bits[i // 2]) for i in range(12))
    require(row["original_twelve_row_outcomes"] == ";".join(map(str, y)),
            "REPEATED_LABELS")
    weight = canonical_fraction(row["original_complete_source_probability"])
    require(weight == p ** bits.count("1") * (1 - p) ** (6 - bits.count("1")),
            "SOURCE_WEIGHT_MISMATCH")
    scores = {}
    for protocol in ("LOOR", "LOGO"):
        q = predict(bits, model, protocol)
        saved_q = tuple(canonical_fraction(s) for s in row[protocol.lower() + "_row_predictions"].split(";"))
        saved_losses = tuple(canonical_fraction(s) for s in row[protocol.lower() + "_row_squared_losses"].split(";"))
        want_losses = tuple((F(z) - v) ** 2 for z, v in zip(y, q))
        require(len(saved_q) == 12 and saved_q == q, "FOLD_PREDICTIONS_" + protocol)
        require(len(saved_losses) == 12 and saved_losses == want_losses,
                "FOLD_BRIER_LOSSES_" + protocol)
        saved_avg = canonical_fraction(row[protocol.lower() + "_average_brier"])
        require(saved_avg == sum(want_losses, F(0)) / 12, "FOLD_MEAN_" + protocol)
        scores[protocol] = saved_avg
    return p, bits, model, weight, scores["LOOR"], scores["LOGO"]


def newly_unseen_group_risk(p: F, bits: str, model: str) -> F:
    """Fit on all six groups, then average over an independent new Bernoulli(p)."""
    require(model in MODELS, "NEW_GROUP_MODEL")
    q = F(2 * bits.count("1") + 1, 14) if model == "GLOBAL_LAPLACE" else HALF
    return brier(p, q)


def choose_model(scores: dict[str, F]) -> str:
    require(set(scores) == set(MODELS), "SELECTOR_MODEL_SET")
    return min(ORDER, key=lambda m: (scores[m], ORDER.index(m)))


def analytic_full_training_laplace(p: F) -> F:
    """Fresh risk identity independent of 64-source enumeration."""
    return F(55, 49) * p * (1 - p) + (HALF - p) ** 2 / 49


def analytic_binomial_selection(p: F) -> tuple[F, F]:
    """Independent K~Bin(6,p) path; does not read source rows or CV scores."""
    chosen_global_mass = F(0)
    future_risk = F(0)
    for k in range(7):
        mass = F(comb(6, k)) * p ** k * (1 - p) ** (6 - k)
        loss_logo_laplace = F(k * (13 - 2 * k) ** 2 +
                              (6 - k) * (2 * k + 1) ** 2, 864)
        chosen = "GLOBAL_LAPLACE" if loss_logo_laplace < F(1, 4) else "CONSTANT_HALF"
        if chosen == "GLOBAL_LAPLACE":
            chosen_global_mass += mass
        q = F(2 * k + 1, 14) if chosen == "GLOBAL_LAPLACE" else HALF
        future_risk += mass * brier(p, q)
    return future_risk, chosen_global_mass


def evaluate(csv_bytes: bytes, json_bytes: bytes, negative_controls: bool = True) -> dict:
    rows_str = csv_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(rows_str))
    require(tuple(reader.fieldnames or ()) == FIELDS, "CSV_COLUMNS")
    grouped: dict[tuple[F, str], dict[str, tuple[F, F, F]]] = {}
    recorded = list(reader)
    require(len(recorded) == 576, "ARCHIVED_SOURCE_ROW_COUNT")
    for row in recorded:
        p, bits, model, mass, loor, logo = validate_row(row)
        key = (p, bits)
        group = grouped.setdefault(key, {})
        require(model not in group, "DUPLICATE_MODEL_SOURCE")
        group[model] = (mass, loor, logo)
    require(len(grouped) == 192, "ARCHIVED_SIX_BIT_SEQUENCES")
    orig = json.loads(json_bytes)
    require(orig.get("world_count") == 9 and orig.get("source_types") == 576,
            "ARCHIVED_RESULT_UNIVERSE")
    worlds = {(F(w["true_p"]), w["predictor"]): w for w in orig["world_results"]}
    require(len(worlds) == 9, "ARCHIVED_RESULT_WORLDS")

    results = []
    for p in PS:
        mass_total = F(0)
        all_score_means = {m: {"LOOR": F(0), "LOGO": F(0)} for m in MODELS}
        selector_masses = {"LOOR": Counter(), "LOGO": Counter()}
        selector_counts = {"LOOR": Counter(), "LOGO": Counter()}
        future = {"LOOR": F(0), "LOGO": F(0), "GLOBAL_LAPLACE": F(0)}
        for bits in map("".join, itertools.product("01", repeat=6)):
            group = grouped.get((p, bits))
            require(group is not None and set(group) == set(MODELS), "GROUP_SOURCE_COMPLETENESS")
            weights = {item[0] for item in group.values()}
            require(len(weights) == 1, "SHARED_SIX_LATENTS_SOURCE_MASS")
            mass = weights.pop()
            mass_total += mass
            scores = {protocol: {m: group[m][1 if protocol == "LOOR" else 2]
                                 for m in MODELS} for protocol in ("LOOR", "LOGO")}
            for m in MODELS:
                all_score_means[m]["LOOR"] += mass * group[m][1]
                all_score_means[m]["LOGO"] += mass * group[m][2]
            for protocol in ("LOOR", "LOGO"):
                chosen = choose_model(scores[protocol])
                selector_masses[protocol][chosen] += mass
                selector_counts[protocol][chosen] += 1
                future[protocol] += mass * newly_unseen_group_risk(p, bits, chosen)
            future["GLOBAL_LAPLACE"] += mass * newly_unseen_group_risk(p, bits, "GLOBAL_LAPLACE")
        require(mass_total == 1, "TOTAL_EXACT_SOURCE_MASS")
        for m in MODELS:
            old = worlds[(p, m)]
            require(all_score_means[m]["LOOR"] == F(old["expected_LOOR_Brier"]) and
                    all_score_means[m]["LOGO"] == F(old["expected_LOGO_Brier"]),
                    "HISTORICAL_FROZEN_SCORE_RECOMPUTATION")
        require(selector_masses["LOOR"]["GROUP_ID_MEMORIZER"] == 1,
                "FROZEN_SOURCE_LOOR_CHOICE")
        require(future["LOOR"] == F(1, 4), "LOOR_NEW_GROUP_RISK")
        analytic_glob = analytic_full_training_laplace(p)
        require(future["GLOBAL_LAPLACE"] == analytic_glob,
                "FULL_FIT_RISK_INDEPENDENT_MOMENT_PATH")
        analytic_selected, analytic_mass = analytic_binomial_selection(p)
        require(future["LOGO"] == analytic_selected and
                selector_masses["LOGO"]["GLOBAL_LAPLACE"] == analytic_mass,
                "LOGO_SELECTION_INDEPENDENT_BINOMIAL_PATH")
        oracle = min(F(1, 4), analytic_glob)
        require(future["LOOR"] >= oracle and future["LOGO"] >= oracle,
                "RISK_BENCHMARK_ORDER")

        results.append({
            "p": str(p),
            "unique_six_group_sequences": 64,
            "LOOR_selected_models_by_source": dict(selector_counts["LOOR"]),
            "LOGO_selected_models_by_source": dict(selector_counts["LOGO"]),
            "LOGO_global_selection_probability": str(analytic_mass),
            "new_group_expected_Brier_after_LOOR_model_choice": str(future["LOOR"]),
            "new_group_expected_Brier_after_LOGO_model_choice": str(future["LOGO"]),
            "new_group_expected_Brier_full_train_Laplace": str(analytic_glob),
            "oracle_minimum_expected_Brier_among_three_candidates": str(oracle),
            "LOOR_selection_regret_vs_oracle": str(future["LOOR"] - oracle),
            "LOGO_selection_regret_vs_oracle": str(future["LOGO"] - oracle),
        })
    if negative_controls:
        tamper = dict(recorded[0])
        tamper["loor_average_brier"] = "1/2"
        try:
            validate_row(tamper)
        except IntegrityError as error:
            require(str(error) == "FOLD_MEAN_LOOR", "SCORE_MUTANT_REJECTION_CAUSE")
        else:
            raise IntegrityError("SCORE_MUTANT_ACCEPTED")
        tamper2 = dict(recorded[0])
        tamper2["original_complete_source_probability"] = "1/2"
        try:
            validate_row(tamper2)
        except IntegrityError as error:
            require(str(error) == "SOURCE_WEIGHT_MISMATCH", "WEIGHT_MUTANT_REJECTION_CAUSE")
        else:
            raise IntegrityError("SOURCE_WEIGHT_MUTANT_ACCEPTED")
    return {
        "status": "PASS_R269_SECONDARY_EXACT_NEW_GROUP_POST_SELECTION_RISK",
        "scope": "ARTIFICIAL_E1_EXPLORATORY_AFTER_ORIGINAL_FREEZE",
        "published_source_rows": len(recorded),
        "distinct_six_group_sequences_per_probability": 64,
        "weighted_configurations_per_probability": 64,
        "independent_future_group_outcome_integrated": True,
        "selection_policy": "per_source_empirical_CV_minimum_fixed_tiebreak",
        "full_training_after_selection": "all_six_groups_twelve_rows",
        "estimation_target": "one_new_independent_Bernoulli_p_group",
        "oracle_is_ex_ante_known_true_p_reference_only": True,
        "mutation_controls": ["source_score_REJECTED", "source_probability_REJECTED"],
        "results": results,
        "new_real_human_E2": 0, "new_historical_E3": 0,
        "original_R269_frozen_protocol_changed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--results", type=Path, default=RESULT)
    args = parser.parse_args()
    source = args.source.read_bytes()
    old_result = args.results.read_bytes()
    require(hashlib.sha256(source).hexdigest() == SOURCE_SHA256, "ARCHIVED_SOURCE_SHA256")
    require(hashlib.sha256(old_result).hexdigest() == RESULT_SHA256, "ARCHIVED_RESULT_SHA256")
    receipt = evaluate(source, old_result)
    receipt["original_csv_sha256"] = SOURCE_SHA256
    receipt["original_result_json_sha256"] = RESULT_SHA256
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
