#!/usr/bin/env python3
"""Decode a fixed public human repeated-PD RDA and report schema only.

No participant-level rows are printed, stored in this repository or scored.
R073 frozen model and scoring rules are never loaded or modified.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import urllib.request
from pathlib import Path

import pyreadr

COMMIT = "a6373b23d80dc816a63f18f973d372c9e8421914"
URL = f"https://raw.githubusercontent.com/cran/stratEst/{COMMIT}/data/DF2011.rda"
BLOB_SHA = "52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0"
COLUMNS = ["treatment", "id", "game", "period", "choice", "other.choice"]


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check_blob(data: bytes, expected_sha: str) -> None:
    if len(data) != 3298 or not data.startswith(b"BZh"):
        raise AssertionError("DF2011_SIZE_OR_BZIP2_MAGIC_MISMATCH")
    if git_blob(data) != expected_sha:
        raise AssertionError("DF2011_GIT_BLOB_SHA_MISMATCH")


def negative_controls(data: bytes):
    rejected = 0
    for altered, expected in [
        (bytes([data[0] ^ 1]) + data[1:], BLOB_SHA),
        (data, "0" * 40),
    ]:
        try:
            check_blob(altered, expected)
        except AssertionError:
            rejected += 1
    if rejected != 2:
        raise AssertionError("DF2011_NEGATIVE_CONTROL_NOT_REJECTED")
    return rejected


def positive_integer_series(values):
    if values.isna().any():
        return False
    for value in values:
        try:
            if float(value) <= 0 or not float(value).is_integer():
                return False
        except (TypeError, ValueError, OverflowError):
            return False
    return True


def main():
    request = urllib.request.Request(URL, headers={"User-Agent": "Psychohistory-Research-Source-Audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
    check_blob(raw, BLOB_SHA)
    rejected = negative_controls(raw)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "DF2011.rda"
        path.write_bytes(raw)
        objects = pyreadr.read_r(str(path))
    if len(objects) != 1:
        raise AssertionError("DF2011_UNEXPECTED_RDA_OBJECT_COUNT")
    object_name, frame = next(iter(objects.items()))
    if list(frame.columns) != COLUMNS:
        raise AssertionError("DF2011_SCHEMA_DRIFT")
    if len(frame) != 7358:
        raise AssertionError("DF2011_ROW_COUNT_DRIFT")
    if not positive_integer_series(frame["game"]) or not positive_integer_series(frame["period"]):
        raise AssertionError("DF2011_GAME_PERIOD_NOT_POSITIVE_INTEGERS")
    if frame["id"].isna().any() or frame["treatment"].isna().any():
        raise AssertionError("DF2011_ID_OR_TREATMENT_MISSING")
    actions = {}
    for name in ("choice", "other.choice"):
        observed = sorted(set(str(x) for x in frame[name].dropna().unique()))
        actions[name] = observed
        if observed != ["c", "d"]:
            raise AssertionError("DF2011_ACTION_LABELS_UNEXPECTED_" + name)
    keys = ["treatment", "id", "game", "period"]
    duplicates = int(frame.duplicated(subset=keys).sum())
    distinct_participants_by_treatment = int(frame[["treatment", "id"]].drop_duplicates().shape[0])
    id_multiple_treatments = int((frame.groupby("id", observed=True)["treatment"].nunique() > 1).sum())
    nulls = {name: int(frame[name].isna().sum()) for name in COLUMNS}
    summary = {
        "source": "Dal Bo Frechette 2011 original DF2011 RDA via pinned CRAN mirror",
        "fixed_source_commit": COMMIT,
        "raw_blob_sha1": BLOB_SHA,
        "object_name": str(object_name),
        "rows": len(frame),
        "columns": COLUMNS,
        "missing_by_field": nulls,
        "action_categories": actions,
        "treatment_levels": sorted(str(x) for x in frame["treatment"].dropna().unique()),
        "distinct_treatment_id_pairs": distinct_participants_by_treatment,
        "id_reused_across_treatments_count": id_multiple_treatments,
        "duplicate_treatment_id_game_period_keys": duplicates,
        "distinct_supergame_labels": int(frame["game"].nunique()),
        "distinct_period_labels": int(frame["period"].nunique()),
        "max_period": int(frame["period"].max()),
        "negative_controls_rejected": rejected,
        "verified_session_identity": False,
        "verified_opponent_pair_identity": False,
        "R073_frozen_scoring_executed": False,
        "new_E2_predictions": 0,
        "new_E3_historical_evidence": 0,
        "status": "RAW_ROWS_DECODED_SCHEMA_CHECKED_SESSION_AND_IDENTITY_GATES_OPEN",
    }
    print(json.dumps(summary, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
