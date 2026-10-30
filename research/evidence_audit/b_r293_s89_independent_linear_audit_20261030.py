#!/usr/bin/env python3
"""Independent R293 S89 E1 source and covariance audit; standard library only.

Does not import the R enumerator. The covariance oracle uses the latent
covariance matrix and the linear response-style transformation.
"""
from __future__ import annotations
import argparse
import copy
import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "validation"
SRC = BASE / "R293_S89_ALL_2112_ENDOGENOUS_STYLE_SOURCES.csv"
RESULT = BASE / "R293_S89_EXACT_RESULTS.json"
ORIGINAL = Path(__file__).resolve().parents[1] / "R293" / "R293_EXACT_VALUE_CENTERING_RESULTS.json"
FREEZE = "a0a862befbf99ad5e350cdd2ae83aec02df6c2c4"
MODES = ("INDEPENDENT", "OPPOSED_PAIRS")
STYLES = ("ANCHOR_PLUS", "ANCHOR_MINUS")
FIELDS = ("mode", "mechanism", "latent_bits", "source_probability", "shift",
          "latent_values", "raw_scores", "centered_scores")


def latent_cov(mode: str, i: int, j: int) -> Q:
    if mode == "INDEPENDENT":
        return Q(1, 4) if i == j else Q(0)
    if i % 5 != j % 5:
        return Q(0)
    return Q((1 if i < 5 else -1) * (1 if j < 5 else -1), 4)


def analytical(mode: str, style: str) -> dict:
    direction = 1 if style == "ANCHOR_PLUS" else -1
    raw = []
    centered = []
    for i in range(10):
        r, c = [], []
        for j in range(10):
            r.append(latent_cov(mode, i, j) + 2 * direction *
                     (latent_cov(mode, i, 0) + latent_cov(mode, j, 0)) + 1)
            if mode == "INDEPENDENT":
                c.append(Q(9, 40) if i == j else Q(-1, 40))
            else:
                c.append(latent_cov(mode, i, j))
        raw.append(r)
        centered.append(c)
    pair = raw[0][5] ** 2 / (raw[0][0] * raw[5][5])
    return {"raw_mean": ["3/2"] * 10, "centered_mean": ["0"] * 10,
            "raw_covariance": [[str(v) for v in r] for r in raw],
            "centered_covariance": [[str(v) for v in r] for r in centered],
            "pair_0_5_raw_correlation_squared": str(pair),
            "pair_0_5_raw_correlation_sign": "positive"}


def parse_vec(v: str) -> tuple[Q, ...]:
    out = tuple(Q(x) for x in v.split(";"))
    if len(out) != 10:
        raise ValueError("vector length")
    return out


def validate(rows: list[dict], result: dict, original: dict | None = None) -> dict:
    if result.get("freeze_commit") != FREEZE or result.get("increment") != "S89":
        raise ValueError("freeze identity")
    if result.get("new_source_rows") != 2112 or len(rows) != 2112:
        raise ValueError("source universe length")
    if result.get("new_human_E2") != 0 or result.get("new_historical_E3") != 0:
        raise ValueError("evidence level")
    if result.get("empirical_circle_validated") is not False:
        raise ValueError("empirical claim")
    if result.get("R073") != "FROZEN" or result.get("PESEN_v0_1") != "FROZEN":
        raise ValueError("frozen project boundary")
    if result.get("original_R293_baseline") != "CLOSED_BOUNDED_E1_UNCHANGED":
        raise ValueError("baseline identity")
    seen = set()
    mass = defaultdict(Q)
    count = Counter()
    for row in rows:
        if tuple(row) != FIELDS:
            raise ValueError("CSV fields")
        mode, style, bits = row["mode"], row["mechanism"], row["latent_bits"]
        if mode not in MODES or style not in STYLES:
            raise ValueError("unfrozen world")
        n = 10 if mode == "INDEPENDENT" else 5
        if len(bits) != n or set(bits) - {"0", "1"}:
            raise ValueError("latent profile")
        key = (mode, style, bits)
        if key in seen:
            raise ValueError("duplicate source")
        seen.add(key)
        b = tuple(map(int, bits))
        latent = b if n == 10 else b + tuple(1 - x for x in b)
        shift = 2 * b[0] if style == "ANCHOR_PLUS" else 2 * (1 - b[0])
        if int(row["shift"]) != shift:
            raise ValueError("response-style dependence")
        p = Q(row["source_probability"])
        if p != Q(1, 2 ** n):
            raise ValueError("source probability")
        raw = tuple(x + shift for x in latent)
        centered = tuple(Q(x) - Q(sum(raw), 10) for x in raw)
        if parse_vec(row["latent_values"]) != latent:
            raise ValueError("latent values")
        if parse_vec(row["raw_scores"]) != raw:
            raise ValueError("raw score")
        if parse_vec(row["centered_scores"]) != centered:
            raise ValueError("centered score")
        if sum(centered) != 0 or raw[0] - raw[5] != centered[0] - centered[5]:
            raise ValueError("pathwise centering invariance")
        mass[(mode, style)] += p
        count[(mode, style)] += 1
    expected_keys = {(mode, style, format(i, f"0{10 if mode == 'INDEPENDENT' else 5}b"))
                     for mode in MODES for style in STYLES
                     for i in range(2 ** (10 if mode == "INDEPENDENT" else 5))}
    if seen != expected_keys:
        raise ValueError("missing or extra source")
    if len(result.get("worlds", [])) != 4:
        raise ValueError("world coverage")
    indexed = {}
    for w in result["worlds"]:
        key = (w.get("mode"), w.get("mechanism"))
        if key in indexed or key not in mass:
            raise ValueError("duplicate or extra result world")
        indexed[key] = w
    if set(indexed) != set(mass):
        raise ValueError("missing result world")
    for (mode, style), w in indexed.items():
        n = 2 ** (10 if mode == "INDEPENDENT" else 5)
        if count[(mode, style)] != n or mass[(mode, style)] != 1:
            raise ValueError("world probability mass")
        if w.get("source_rows") != n or w.get("source_mass") != "1":
            raise ValueError("result source count")
        for field, oracle in analytical(mode, style).items():
            if w.get(field) != oracle:
                raise ValueError(f"independent analytic mismatch: {mode}/{style}/{field}")
        if original is not None:
            baselines = {x["mode"]: x for x in original["worlds"]}
            if w["centered_covariance"] != baselines[mode]["centered_covariance"]:
                raise ValueError("original R293 centered baseline mismatch")
    return {"source_rows": len(rows), "worlds": len(indexed),
            "covariance_entries_checked": 800, "independent_oracle": "linear_latent_covariance"}


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--csv", type=Path, default=SRC)
    ap.add_argument("--json", type=Path, default=RESULT)
    ap.add_argument("--original", type=Path, default=ORIGINAL)
    args = ap.parse_args()
    if args.check == args.test:
        ap.error("select exactly one of --check or --test")
    rows = read_rows(args.csv)
    result = json.loads(args.json.read_text(encoding="utf-8"))
    original = json.loads(args.original.read_text(encoding="utf-8")) if args.original.exists() else None
    ok = validate(rows, result, original)
    if args.test:
        tests = []
        def run(name, mutator):
            r = copy.deepcopy(rows)
            j = copy.deepcopy(result)
            mutator(r, j)
            try:
                validate(r, j, original)
            except (ValueError, KeyError, TypeError, ZeroDivisionError):
                tests.append(name)
                return
            raise AssertionError(f"mutation accepted: {name}")
        run("duplicate_source", lambda r, j: r.__setitem__(1, copy.deepcopy(r[0])))
        run("missing_source", lambda r, j: r.pop())
        run("wrong_style", lambda r, j: r[0].__setitem__("shift", "2" if r[0]["shift"] == "0" else "0"))
        run("wrong_probability", lambda r, j: r[0].__setitem__("source_probability", "1/2"))
        run("wrong_raw", lambda r, j: r[0].__setitem__("raw_scores", "9;" + r[0]["raw_scores"].split(";", 1)[1]))
        run("wrong_centered", lambda r, j: r[0].__setitem__("centered_scores", "9;" + r[0]["centered_scores"].split(";", 1)[1]))
        run("wrong_covariance", lambda r, j: j["worlds"][0]["raw_covariance"][0].__setitem__(5, "999"))
        run("evidence_upgrade", lambda r, j: j.__setitem__("new_human_E2", 1))
        ok["mutations_rejected"] = tests
    print(json.dumps(ok, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
