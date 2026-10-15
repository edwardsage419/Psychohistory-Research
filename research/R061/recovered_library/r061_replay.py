#!/usr/bin/env python3
"""R061: fail-closed Najar 2020 raw-data verification and leave-one-person-out replay.

Requires original, unmodified author's task1.csv/task2.csv from
https://github.com/hrl-team/mfree_imitation/tree/master/data
No source file is bundled with this research package.
"""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

SOURCE = {
    1: {"sha": "6f90784a49c26c92806b4876cb0ce4b446f810b1", "rows": 9600, "people": 24, "sessions": 4, "private": 5760, "demo": 3840, "correct": 4308},
    2: {"sha": "5239155f233d42e4dbbe3f986865d5459a3e9cee", "rows": 13200, "people": 44, "sessions": 3, "private": 7920, "demo": 5280, "correct": 4916},
}
ALPHA_PRIVATE = (.05, .1, .3, .6)
BETA = (.5, 1.0, 2.0, 4.0)
PERSEVERATION = (0.0, .15, .4)
ALPHA_SOCIAL = (0.0, .03, .1, .3)
GRID = [(ap, beta, kappa, social) for ap in ALPHA_PRIVATE for beta in BETA for kappa in PERSEVERATION for social in ALPHA_SOCIAL]
CATEGORIES = ("private", "skilled", "unskilled")


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def parse_data(data, task, check_provenance=True):
    """Use only observed choices and own reward; never use cgb as a predictive feature."""
    import io
    if task not in SOURCE:
        raise ValueError("Unrecognized task")
    spec = SOURCE[task]
    if check_provenance and git_blob_sha(data) != spec["sha"]:
        raise ValueError("FAIL CLOSED: author Git blob SHA1 mismatch")
    rows = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
    if check_provenance and len(rows) != spec["rows"]:
        raise ValueError("FAIL CLOSED: row count does not match author's file")
    people = defaultdict(lambda: defaultdict(list))
    ids, statuses = set(), Counter()
    unique_trials = set()
    for row in rows:
        subject = row["expid"]
        session, trial = int(row["session"]), int(row["trial"])
        identity = (subject, session, trial)
        if identity in unique_trials:
            raise ValueError("Duplicate subject-session-trial")
        unique_trials.add(identity)
        if not 1 <= session <= spec["sessions"] or not 1 <= trial <= 100:
            raise ValueError("Out-of-range session or trial")
        cond = row["condition.obs"]
        if cond not in ("Private", "Choice"):
            raise ValueError("Unexpected observation condition")
        chosen = int(row["cgb"])
        if chosen not in (0, 1):
            raise ValueError("Unexpected stimulus-choice code")
        state = int(row["state"])
        if state < 1:
            raise ValueError("Invalid state")
        demo = row["id"] == "dem"
        out = None if row["out"] == "NA" else int(row["out"])
        if demo and (out is not None or cond != "Choice"):
            raise ValueError("Demonstrator should have an unobserved reward")
        if not demo and out not in (-1, 1):
            raise ValueError("Missing or invalid own reward")
        skill = row["condition.demskill"] if task == 1 else row["group.demskill"]
        if skill not in ("private", "skilled.dem", "unskilled.dem") and task == 1:
            raise ValueError("Invalid task1 condition")
        if skill not in ("skilled.dem", "unskilled.dem") and task == 2:
            raise ValueError("Invalid task2 condition")
        if cond == "Choice" and not demo and skill == "private":
            raise ValueError("Private demonstrator condition conflict")
        ids.add(subject)
        statuses["dem" if demo else "private"] += 1
        statuses["correct"] += (chosen if not demo else 0)
        people[subject][session].append({
            "trial": trial, "state": state, "choice": chosen, "demo": demo,
            "out": out, "condition": cond, "skill": skill,
        })
    for subject in people:
        if len(people[subject]) != spec["sessions"]:
            raise ValueError("Subject missing sessions")
        for session, events in people[subject].items():
            events.sort(key=lambda x: x["trial"])
            if [e["trial"] for e in events] != list(range(1, 101)):
                raise ValueError("Missing/duplicate trial in session")
    if check_provenance and (
        len(ids) != spec["people"] or statuses["private"] != spec["private"]
        or statuses["dem"] != spec["demo"] or statuses["correct"] != spec["correct"]
    ):
        raise ValueError("FAIL CLOSED: dataset structure inconsistent with registered source")
    return people, dict(statuses)


def softplus(z):
    if z > 0:
        return z + math.log1p(math.exp(-z))
    return math.log1p(math.exp(z))


def score_subject(sessions, params):
    """Predict THEN update within each session and stimulus state; no current outcome leakage."""
    ap, beta, kappa, social = params
    loss, n = 0.0, 0
    subscores = {k: [0.0, 0] for k in CATEGORIES}
    for _, events in sorted(sessions.items()):
        Q, prev = {}, {}
        for e in events:
            state = e["state"]
            if state not in Q:
                Q[state] = [0.0, 0.0]
            q = Q[state]
            chosen = e["choice"]
            other = 1 - chosen
            if e["demo"]:
                q[chosen] += social * (1 - q[chosen])
                q[other] += social * (-1 - q[other])
            else:
                history = prev.get(state)
                signed = 0 if history is None else (1 if history == 1 else -1)
                logit = beta * (q[1] - q[0] + kappa * signed)
                obs_loss = softplus(-logit if chosen == 1 else logit)
                loss += obs_loss
                n += 1
                category = ("private" if e["condition"] == "Private" else
                            "skilled" if e["skill"] == "skilled.dem" else "unskilled")
                subscores[category][0] += obs_loss
                subscores[category][1] += 1
                own = e["out"]
                q[chosen] += ap * (own - q[chosen])
                q[other] += ap * (-own - q[other])
                prev[state] = chosen
    if n < 1:
        raise ValueError("No private outcomes")
    return {"loss": loss / n, "n": n, "strata": subscores}


def accuracy_subject(sessions):
    tally = {k: [0, 0] for k in CATEGORIES}
    for events in sessions.values():
        for e in events:
            if e["demo"]:
                continue
            category = ("private" if e["condition"] == "Private" else
                        "skilled" if e["skill"] == "skilled.dem" else "unskilled")
            tally[category][0] += e["choice"]
            tally[category][1] += 1
    return {k: (a / n if n else None) for k, (a, n) in tally.items()}


def cross_validate(people):
    """For each held-out participant, choose grid params using other people only."""
    ids = sorted(people, key=lambda v: int(v))
    allscores = {subject: [score_subject(people[subject], g) for g in GRID] for subject in ids}
    results = []
    for subject in ids:
        selected = {}
        for family in ("RW", "VS"):
            options = (i for i, params in enumerate(GRID) if family != "RW" or params[3] == 0)
            idx = min(options, key=lambda i: sum(allscores[other][i]["loss"] for other in ids if other != subject))
            selected[family] = {**allscores[subject][idx], "params": GRID[idx]}
        results.append({
            "id": subject, "n": selected["RW"]["n"],
            "rw_loss": selected["RW"]["loss"], "vs_loss": selected["VS"]["loss"],
            "delta": selected["VS"]["loss"] - selected["RW"]["loss"],
            "rw_params": selected["RW"]["params"], "vs_params": selected["VS"]["params"],
            "strata": {k: {
                "n": selected["RW"]["strata"][k][1],
                "rw_loss_sum": selected["RW"]["strata"][k][0],
                "vs_loss_sum": selected["VS"]["strata"][k][0],
            } for k in CATEGORIES},
        })
    return results


def summarize(task, people, checks, cv):
    def avg(col):
        return sum(z[col] for z in cv) / len(cv)
    a = {"task": task, "sha": SOURCE[task]["sha"], "participants": len(people),
         "records": SOURCE[task]["rows"], "data_checks": checks,
         "rw_loss": avg("rw_loss"), "vs_loss": avg("vs_loss"), "delta": avg("delta"),
         "improved_people": sum(z["delta"] < -1e-12 for z in cv)}
    for cat in CATEGORIES:
        n = sum(z["strata"][cat]["n"] for z in cv)
        a[cat] = {"n": n, "rw_loss": (sum(z["strata"][cat]["rw_loss_sum"] for z in cv) / n) if n else None,
                  "vs_loss": (sum(z["strata"][cat]["vs_loss_sum"] for z in cv) / n) if n else None}
    return a


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task1", type=Path, required=True)
    parser.add_argument("--task2", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    outcomes = []
    for task, path in ((1, args.task1), (2, args.task2)):
        data = path.read_bytes()
        people, checks = parse_data(data, task, check_provenance=True)
        cv = cross_validate(people)
        outcomes.append({"summary": summarize(task, people, checks, cv), "participants": cv,
                         "accuracy": {id: accuracy_subject(sessions) for id, sessions in people.items()}})
    args.out.write_text(json.dumps({"provenance": "AUTHOR_RAW_LOCAL_VERIFIED", "results": outcomes},
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "summaries": [r["summary"] for r in outcomes]}, ensure_ascii=False))


if __name__ == "__main__":
    main()