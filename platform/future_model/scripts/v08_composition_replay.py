"""Independent enumerations for the isolated composition contract, using synthetic data only."""

import json
import sys
from itertools import product
from pathlib import Path
from secrets import token_bytes

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from psychohistory.decision_composition import (  # noqa: E402
    CompositionScope, GroupedPort, Hypothesis, ModelResult, ValueGroup,
    advance_join, compare_hypotheses, prepare_join,
)

SIGNING_KEY = token_bytes(32)
MISSING = object()


def scope(worlds):
    return CompositionScope(
        session_instance="synthetic-replay", authorization_epoch="synthetic-only",
        evidence_epoch="synthetic-evidence-1",
        revision=1, domain_id="synthetic", domain_version="1",
        unit="integer units per period", horizon="synthetic period", exhaustive=True,
        worlds=worlds,
    )


def port(domain, kind, values):
    groups = {}
    for world, value in zip(domain.worlds, values, strict=True):
        if value is not MISSING:
            groups.setdefault(value, []).append(world)
    return GroupedPort(
        scope=domain, kind=kind, method_version=f"fixture-{kind}@1",
        source_versions=("synthetic-replay@1",),
        groups=tuple(ValueGroup(value=v, worlds=tuple(w)) for v, w in groups.items()),
    )


def require(condition, error):
    if not condition:
        raise AssertionError(error)


def replay_joint():
    domain = scope(("alpha", "beta", "gamma", "delta"))
    gains = [(1, 1, 3, 3), (3, MISSING, 0, 1), (MISSING, MISSING, 3, 1), (1, 1, 1, 1)]
    cases = 0
    for thresholds, values in product(product((0, 2, None, MISSING), repeat=4), gains):
        expected = {"pass": [], "fail": [], "missing_evidence": []}
        for world, threshold, value in zip(domain.worlds, thresholds, values, strict=True):
            if threshold is MISSING or value is MISSING:
                expected["missing_evidence"].append(world)
            elif threshold is None or value < threshold:
                expected["fail"].append(world)
            else:
                expected["pass"].append(world)

        threshold_port, gain_port = port(domain, "threshold", thresholds), port(domain, "gain", values)
        plan = prepare_join(domain, threshold_port, gain_port)
        progress = advance_join(plan, domain, 0, signing_key=SIGNING_KEY)
        pass_count, fail_count = len(expected["pass"]), len(expected["fail"])
        while progress["checkpoint"] is not None:
            require(progress["pass_count_bounds"][0] <= pass_count <= progress["pass_count_bounds"][1],
                    "Pass-count prefix bound differs from direct enumeration.")
            require(progress["fail_count_bounds"][0] <= fail_count <= progress["fail_count_bounds"][1],
                    "Fail-count prefix bound differs from direct enumeration.")
            checkpoint = json.loads(json.dumps(progress["checkpoint"]))
            rebuilt = prepare_join(domain, threshold_port, gain_port)
            progress = advance_join(rebuilt, domain, 1, signing_key=SIGNING_KEY, checkpoint=checkpoint)
        require(all(progress[key] == expected[key] for key in expected)
                and progress["not_calculated"] == [], "Resumed result differs from world-by-world oracle.")
        cases += 1
    return cases


def replay_hypotheses():
    actions = ("hold", "change")
    domain = scope(("near", "far"))
    assignments = tuple(item for item in product((None, actions[:1], actions[1:], actions), repeat=2)
                        if any(item))
    cases = 0
    for left, right in product(assignments, repeat=2):
        models = tuple(
            Hypothesis(scope=domain, method_version=f"fixture-{name}@1", source_versions=("synthetic-replay@1",),
                       results=tuple(ModelResult(world=w, winners=a)
                                     for w, a in zip(domain.worlds, rows, strict=True) if a is not None))
            for name, rows in zip(("left", "right"), (left, right), strict=True)
        )
        expected_rows = []
        for world, a, b in zip(domain.worlds, left, right, strict=True):
            alternatives = [row for row in (a, b) if row is not None]
            if alternatives:
                expected_rows.append((world, [x for x in actions if all(x in y for y in alternatives)],
                                      [x for x in actions if any(x in y for y in alternatives)]))
        result = compare_hypotheses(domain, actions, models)
        require([(r["world"], r["common"], r["possible"]) for r in result["rows"]] == expected_rows,
                "World winners differ from direct membership checks.")
        if len(expected_rows) == len(domain.worlds):
            choices = [row for row in (*left, *right) if row is not None]
            require(result["common"] == [a for a in actions if all(a in row for row in choices)]
                    and result["possible"] == [a for a in actions if any(a in row for row in choices)],
                    "Global winners differ from direct membership checks.")
        else:
            require(result["common"] is None and result["possible"] is None,
                    "A missing world received a global result.")
        cases += 1
    return cases


if __name__ == "__main__":
    print(json.dumps({"authority": "NONE", "joint_cases": replay_joint(),
                      "hypothesis_cases": replay_hypotheses()}, sort_keys=True))
