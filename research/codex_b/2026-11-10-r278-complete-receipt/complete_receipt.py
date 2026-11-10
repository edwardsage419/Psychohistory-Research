"""R278 S74 complete artificial receipt gate, supplementing the archived B route.

Reuses its fifteen-risk/binomial and960-source checks. Conditional forecasts and
total-covariance certificate are newly derived here, without importing R Node.
All historical metadata claims remain bounded declarations, not new science.
"""
import argparse
import csv
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
from types import ModuleType

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE_PATH = ROOT/"research/evidence_audit/b_r278_s74_receipt_check_20261030.py"
BASE_BLOB = "f1ba4dcb2e80a612f14b3d7c10896c1d6fccfa62"
PS = ("1/4", "1/2", "3/4")
POLICIES = ("BMA_JOINT", "BMA_PRODUCT", "HARD_SELECT", "FIXED_HALF", "TRUTH_ORACLE")
LABELS = ("00", "01", "10", "11")
CSV_FIELDS = ("true_p", "policy", "full_sixbit", "train_fourbit", "future_twobit",
              "train_successes", "posterior_low", "source_probability", "joint_brier",
              "Q_00", "Q_01", "Q_10", "Q_11")


def require(condition, reason):
    if not condition: raise ValueError(reason)


def _load_base():
    source = BASE_PATH.read_bytes()
    blob = hashlib.sha1(b"blob "+str(len(source)).encode()+b"\0"+source).hexdigest()
    require(blob == BASE_BLOB, "ARCHIVED_B_CODE_CHANGED")
    module = ModuleType("codex_b_pinned_r278_s74")
    module.__file__ = str(BASE_PATH)
    # Compile precisely the bytes checked above; no second source-file read.
    exec(compile(source, str(BASE_PATH), "exec"), module.__dict__)
    return module


BASE = _load_base()


def loads_strict(raw):
    def pairs(entries):
        result = {}
        for key, value in entries:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def nonfinite(_):
        raise ValueError("NONFINITE_JSON_CONSTANT")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)


def expected_receipt():
    """Fixed schema plus existing B risks and new conditional covariance route."""
    risks = BASE.analytic()
    forecasts = {}
    low, high = F(1, 4), F(3, 4)
    for k in range(5):
        likelihood_low = low**k*(1-low)**(4-k)
        likelihood_high = high**k*(1-high)**(4-k)
        w = likelihood_low/(likelihood_low+likelihood_high)
        marginal = w*low+(1-w)*high
        joint = {z: w*low**z.count("1")*(1-low)**z.count("0")
                 +(1-w)*high**z.count("1")*(1-high)**z.count("0") for z in LABELS}
        product = {z: marginal**z.count("1")*(1-marginal)**z.count("0") for z in LABELS}
        # Conditional-on-model covariance0; covariance of model means is positive.
        covariance = w*(1-w)*(high-low)**2
        forecasts[k] = {"train_successes": k, "posterior_low": w, "marginal_q": marginal,
                        "joint_Q": joint, "product_Q": product, "joint_predictive_covariance": covariance}
    return {
        "research": "R278_S74", "evidence": "E1_ARTIFICIAL_NONBLIND_EXPLORATORY",
        "original_freeze": "eb1c8df38349c36ed10d7a2103969818b14d7500",
        "S74_freeze_commit": "56b00cf6d016242e4d35c800c9b4a3162d01ea1e",
        "true_p_values": list(PS), "policies": list(POLICIES), "primitive_rows": 960,
        "independent_true_bit_sources_per_p": 64, "same_source_reused_across_policies": True,
        "score": "joint_four_category_quadratic_Brier",
        "world_results": {(p, policy): {"true_p": p, "policy": policy, "expected_joint_brier": risks[(p, policy)]}
                          for p in PS for policy in POLICIES},
        "BMA_joint_minus_product": {p: {"true_p": p, "delta": risks[(p, "BMA_JOINT")]-risks[(p, "BMA_PRODUCT")]} for p in PS},
        "conditional_forecasts": forecasts,
        "two_exact_routes_equal": True, "original_R278_marginal_risk_unchanged": True,
        "mutation_cases_rejected": ["missing_source", "duplicate_source", "posterior_tamper",
                                    "future_label_tamper", "joint_probability_tamper", "missing_joint_class"],
        "new_E2_predictions": 0, "new_E3_predictions": 0,
        "external_team_replication": False, "R073": "FROZEN", "PESEN_v0_1": "FROZEN",
    }


def _index(records, identity):
    require(type(records) is list, "RECEIPT_COLLECTION_TYPE")
    indexed = {}
    for row in records:
        require(type(row) is dict and set(identity) <= set(row), "RECEIPT_IDENTITY_FIELDS")
        for field in identity:
            require(type(row[field]) is (int if field == "train_successes" else str), "RECEIPT_IDENTITY_TYPE")
        key = tuple(row[field] for field in identity)
        if len(key) == 1: key = key[0]
        require(key not in indexed, "RECEIPT_DUPLICATE_IDENTITY")
        indexed[key] = row
    return indexed


def validate_receipt(data):
    expected = expected_receipt()
    require(type(data) is dict and set(data) == set(expected), "RECEIPT_ROOT_FIELDS")
    actual = dict(data)
    actual["world_results"] = _index(data["world_results"], ("true_p", "policy"))
    actual["BMA_joint_minus_product"] = _index(data["BMA_joint_minus_product"], ("true_p",))
    actual["conditional_forecasts"] = _index(data["conditional_forecasts"], ("train_successes",))

    def compare(found, wanted):
        reason = "RECEIPT_MISMATCH"
        if type(wanted) is dict:
            require(type(found) is dict and set(found) == set(wanted), reason)
            return sum(compare(found[key], value) for key, value in wanted.items())
        if type(wanted) is list:
            require(type(found) is list and len(found) == len(wanted), reason)
            return sum(compare(a, b) for a, b in zip(found, wanted))
        if type(wanted) is F:
            require(type(found) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", found) is not None, reason)
            require(F(found) == wanted, reason)
        else:
            require(type(found) is type(wanted) and found == wanted, reason)
        return 1

    leaves = compare(actual, expected)
    require(leaves == 140, "RECEIPT_INCOMPLETE_EXPECTATION")
    return leaves


def check(csv_path, json_path):
    """Read inputs once; both mathematical routes see the same temporary bytes."""
    csv_bytes, json_bytes = Path(csv_path).read_bytes(), Path(json_path).read_bytes()
    data = loads_strict(json_bytes)
    leaves = validate_receipt(data)
    # DictReader silently folds duplicate names and stores surplus cells under
    # None. Check the wire shape before delegating numeric source verification.
    try:
        rows = list(csv.reader(io.StringIO(csv_bytes.decode("utf-8"), newline=""), strict=True))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError("CSV_PARSE_INVALID") from exc
    require(bool(rows) and tuple(rows[0]) == CSV_FIELDS, "CSV_HEADER_SCHEMA")
    require(len(rows) == 961 and all(len(row) == len(CSV_FIELDS) for row in rows[1:]), "CSV_ROW_SCHEMA")
    with tempfile.TemporaryDirectory(prefix="codex-b-s74-snapshot-") as tmp:
        snapshot_csv, snapshot_json = Path(tmp)/"source.csv", Path(tmp)/"receipt.json"
        snapshot_csv.write_bytes(csv_bytes); snapshot_json.write_bytes(json_bytes)
        source = BASE.check(snapshot_csv, snapshot_json)
    require(source == {"status": "PASS", "worlds": 15, "rows": 960,
                       "independent_route": "binomial K + four-class expected quadratic risk",
                       "scope": "E1 internal nonblind"}, "ARCHIVED_B_RESULT_CHANGED")
    return {"status": "PASS_BOUNDED_FULL_RECEIPT", "receipt_leaves": leaves,
            "source_rows": 960, "worlds": 15,
            "input_snapshot_sha256": {"csv": hashlib.sha256(csv_bytes).hexdigest(),
                                      "json": hashlib.sha256(json_bytes).hexdigest()},
            "scope": "E1_ARTIFICIAL_NONBLIND_INTERNAL", "scientific_acceptance": "UNCHANGED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv"); parser.add_argument("json")
    args = parser.parse_args()
    try:
        result = check(args.csv, args.json)
    except (OSError, ValueError, UnicodeError, TypeError, KeyError, ZeroDivisionError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)[:120] if isinstance(exc, ValueError) else type(exc).__name__}))
        raise SystemExit(2)
    print(json.dumps(result, indent=2))
