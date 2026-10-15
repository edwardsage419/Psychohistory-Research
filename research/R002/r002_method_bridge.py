#!/usr/bin/env python3
"""R002 retrospective methodological bridge, created 2026-10-15.

Synthetic controlled exposures only. This is neither the historical missing R002
file nor a reconstruction of the original R003 parameterization, and it is NOT
human-subject or network-contagion evidence. Standard library only.
"""
import argparse
import json
import math
import random
from pathlib import Path

PARAMS = {
    "b0": (-0.7, -0.3, 0.1),
    "bx": (0.0, 0.9),
    "g": (0.0, 0.7, 1.4, 2.1),
    "rho": (0.2, 0.65, 0.85),
}


def expit(v):
    if v >= 0:
        q = math.exp(-v)
        return 1.0 / (1.0 + q)
    q = math.exp(v)
    return q / (1.0 + q)


def neglogprob(y, p):
    return -math.log(p if y else 1.0 - p)


def make_panel(family, seed, persons=180, rounds=28):
    """Exogenous, Bernoulli random signal; delayed state uses PREVIOUS exposure.

    Exposures are toy experiment assignments; z != measured social interaction.
    Every individual has its own independently initialized lag history.
    """
    if family not in ("M0", "M1", "M2"):
        raise ValueError("invalid family")
    rng = random.Random(seed)
    result = []
    for person in range(persons):
        x = 1 if rng.random() < 0.5 else -1
        previous_z, history = None, 0.5
        for t in range(rounds):
            if t and previous_z is not None:
                history = 0.65 * history + 0.35 * previous_z
            z = int(rng.random() < 0.5)
            feature = {"M0": 0.0, "M1": z - 0.5,
                       "M2": history - 0.5}[family]
            eta = -0.7 + 0.9 * x + (0.0 if family == "M0" else 2.1 * feature)
            y = int(rng.random() < expit(eta))
            result.append({"person": f"{seed}:{person}", "t": t, "x": x, "z": z,
                           "h_02": None, "h_065": None, "h_085": None, "y": y})
            previous_z = z
    add_history_features(result)
    return result


def add_history_features(rows):
    """Compute h_t from z_{t-1}, grouping by participant and sorted time.

    Reject duplicate person-time rows and noncontiguous time histories. Does
    not inspect outcomes, allowing the same features for held-out subjects.
    """
    groups = {}
    for row in rows:
        groups.setdefault(row["person"], []).append(row)
    for person, events in groups.items():
        events.sort(key=lambda r: r["t"])
        assert [r["t"] for r in events] == list(range(len(events)))
        histories = {0.2: 0.5, 0.65: 0.5, 0.85: 0.5}
        prev_z = None
        for row in events:
            if prev_z is not None:
                for rho in histories:
                    histories[rho] = rho * histories[rho] + (1-rho) * prev_z
            for rho, key in [(0.2,"h_02"),(0.65,"h_065"),(0.85,"h_085")]:
                row[key] = histories[rho]
            prev_z = row["z"]
    return rows


def predict(row, family, b0, bx, gamma=0.0, rho=None):
    if family == "M0":
        signal = 0
    elif family == "M1":
        signal = row["z"] - 0.5
    elif family == "M2":
        key = {0.2: "h_02", 0.65: "h_065", 0.85: "h_085"}.get(rho)
        if key is None and gamma != 0:
            raise ValueError("Nonzero delayed effect requires rho")
        signal = 0 if gamma == 0 else row[key] - 0.5
    else:
        raise ValueError("Unknown model")
    return expit(b0 + bx * row["x"] + gamma * signal)


def candidates(family):
    for b0 in PARAMS["b0"]:
        for bx in PARAMS["bx"]:
            gs = (0.0,) if family == "M0" else PARAMS["g"]
            for gamma in gs:
                rhos = PARAMS["rho"] if family == "M2" and gamma != 0 else (None,)
                for rho in rhos:
                    yield {"b0": b0,"bx": bx,"gamma": gamma,"rho": rho}


def mean_logloss(rows, fam, params):
    return sum(neglogprob(r["y"], predict(r, fam, **params)) for r in rows)/len(rows)


def mean_brier(rows, fam, params):
    return sum((r["y"]-predict(r,fam, **params))**2 for r in rows)/len(rows)


def fit(rows, fam):
    return min(candidates(fam), key=lambda p: mean_logloss(rows, fam, p))


def one_run(family, train_seed=425, test_seed=984, train_people=180, test_people=80, rounds=28):
    train = make_panel(family, train_seed, train_people, rounds)
    test = make_panel(family, test_seed, test_people, rounds)
    out = {"synthetic_truth": family, "train_people": train_people,
           "test_people": test_people, "train_observations": len(train),
           "test_observations": len(test), "train_seed": train_seed,
           "test_seed": test_seed, "model_results": {}}
    for fam in ("M0", "M1", "M2"):
        p = fit(train, fam)
        out["model_results"][fam] = {"parameters_train_only": p,
           "test_logloss": mean_logloss(test,fam,p),
           "test_brier": mean_brier(test,fam,p)}
    out["best_test_logloss"] = min(out["model_results"], key=lambda k:out["model_results"][k]["test_logloss"])
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("R002_SYNTHETIC_RESULTS.json"))
    args=parser.parse_args()
    result = {"research_round":"R002 RETROSPECTIVE GAPFILL",
              "evidence_type":"SYNTHETIC_METHOD_VALIDATION_ONLY",
              "creation_date":"2026-10-15",
              "warning":"Not historical recovered R002; not evidence on real human social influence.",
              "runs":[one_run(f) for f in ("M0","M1","M2")],
              "nonidentification_cases":[
                "M1 with gamma=0 equals M0 on every observed event",
                "M2 with gamma=0 equals M0 on every observed event",
                "If exposure does not vary, an immediate effect can become indistinguishable from the intercept",
                "Without exogenous exposure assignment, common-shock/confounding remains possible"]}
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps({"wrote":str(args.output),"synthetic_best_models":[z["best_test_logloss"] for z in result["runs"]]}))

if __name__=="__main__":
    main()
