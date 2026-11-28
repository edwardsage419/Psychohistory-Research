"""Reproduce the fixed 15-contract inventory through the live registry."""

from fractions import Fraction as Q
from hashlib import sha1
from itertools import product
import json
from pathlib import Path

import pytest

from psychohistory.decision_feasibility import GATE_ID
from psychohistory.decision_hub import run_method
from psychohistory.decision_registry import Context, default_registry
from psychohistory.decision_v05 import DecisionHubV05, DecisionStateV05


REPO = Path(__file__).resolve().parents[3]
INDEX = REPO / "research/decision_hub/2026-11-24-native-method-contract-index/method_contracts.json"
CONTRACTS = json.loads(INDEX.read_text(encoding="utf-8"))
METHOD_IDS = [row["key"].split("@")[0] for row in CONTRACTS]
SOURCE = "合成工程验收"
SCORING = {"comparability", "pareto", "weight_sensitivity", "c034_joint_robustness"}
REGRET = {"C029", "C030", "C031"}


def sourced(lower, upper=None):
    return {"lower": lower, "upper": lower if upper is None else upper, "kind": "synthetic", "source": SOURCE}


def quantity(lower, upper=None, *, unit="效用"):
    return {**sourced(lower, upper), "unit": unit}


def cutoff(at, inclusive=True):
    return {"at": at, "inclusive": inclusive, "kind": "synthetic", "source": SOURCE}


def fixture(method_id):
    values = {"a": (6, 6), "b": (10, 0)}
    if method_id == "C030":
        values = {"a": ((5, 7), (5, 7)), "b": ((9, 11), (-1, 1))}
    elif method_id == "C031":
        values = {"a": (8, 2), "b": ("5.5", "5.5"), "c": ("2.5", 8)}

    options = [{"id": key, "label": key.upper(), "measurements": {"cap": quantity(10, unit="元")}}
               for key in values]
    options[0]["scores"] = {"x": quantity(".8"), "y": quantity(".3")}
    options[1]["scores"] = {"x": quantity(".6"), "y": quantity(".6")}
    if method_id == "c034_joint_robustness":
        options[0]["scores"]["x"] = quantity(".7", ".8")

    scenarios = [{"id": key, "label": key, "kind": "synthetic", "source": SOURCE,
                  "utilities": {option: quantity(*(row[i] if isinstance(row[i], tuple) else (row[i],)))
                                for option, row in values.items()}}
                 for i, key in enumerate(("good", "bad"))]
    prior = sourced(".5") if method_id in {"voi_point", "timing_investigation"} else sourced(".4", ".6")
    return {
        "decision_id": "1" * 32, "revision": 1, "question": "合成比较", "deadline": "未来两天",
        "confirmed": True, "constraints_confirmed": True,
        "constraints": [{"id": "cap", "label": "预算", "operator": "<=", "threshold": 10,
                         "source": SOURCE, "unit": "元"}],
        "options": options,
        "objectives": [{"id": key, "label": key, "unit": "效用", "direction": "max"} for key in ("x", "y")],
        "weights_confirmed": True,
        "weights": {key: {"lower": ".2", "upper": ".8"} for key in ("x", "y")},
        "score_basis": SOURCE, "score_dependence": "rectangle", "score_dependence_source": SOURCE,
        "score_transform": "identity", "scenarios": scenarios, "scenario_basis": SOURCE,
        "scenario_dependence": "rectangle", "scenario_dependence_source": SOURCE, "precision_radius": ".5",
        "information": {
            "signals": [{"id": key, "label": key} for key in ("yes", "no")],
            "prior": {"good": prior.copy(), "bad": prior.copy()},
            "likelihoods": {"good": {"yes": sourced(".9"), "no": sourced(".1")},
                            "bad": {"yes": sourced(".3"), "no": sourced(".7")}},
            "cost": quantity(".5"), "unrestricted_actions": True, "action_source": SOURCE,
            "parameter_domain": "rectangle", "parameter_domain_source": SOURCE,
            "timing_basis": SOURCE, "fixed_policy": {"yes": "b", "no": "a"},
        },
        "timing": {
            "confirmed": True, "time_unit": "天", "time_origin": "确认时点", "horizon": cutoff(2),
            "wait_duration": sourced(".25"),
            "actions": {key: {"switching_cost": sourced(0),
                              "delay_losses": {"good": sourced(rate), "bad": sourced(0)}}
                        for key, rate in (("a", 0), ("b", 2))},
            "investigation": {"mode": "deterministic", "kind": "synthetic", "source": SOURCE,
                              "cost": sourced(".5"), "duration": sourced(".25")},
        },
    }


def change_case(method_id, case, raw):
    if case == "missing":
        if method_id == GATE_ID:
            raw["options"][0]["measurements"].clear()
        elif method_id in SCORING:
            raw["options"][0]["scores"].pop("x")
        elif method_id in REGRET:
            raw["scenarios"][0]["utilities"].pop("b")
        elif method_id.startswith("voi_"):
            raw["information"]["prior"].pop("good")
        elif method_id == "timing_actions":
            raw["timing"] = None
        else:
            raw["timing"]["investigation"] = None
    elif case == "invalid":
        if method_id == GATE_ID:
            raw["options"][0]["measurements"]["cap"]["unit"] = "小时"
        elif method_id in SCORING:
            raw["options"][0]["scores"]["x"]["unit"] = "小时"
        elif method_id in REGRET:
            raw["scenarios"][0]["utilities"]["b"]["unit"] = "小时"
        elif method_id.startswith("voi_"):
            raw["information"]["prior"] = {key: sourced(".2") for key in ("good", "bad")}
        else:
            raw["timing"]["actions"]["b"]["delay_losses"]["unknown"] = sourced(3)
    elif case == "edge":
        if method_id == GATE_ID:
            raw["constraints"][0]["operator"] = "<"
        elif method_id in SCORING:
            raw["options"][0]["scores"] = raw["options"][1]["scores"].copy()
        elif method_id in {"C029", "C030"}:
            raw["scenarios"] = [{**row, "utilities": {"a": row["utilities"]["a"], "b": row["utilities"]["a"]}}
                                for row in raw["scenarios"]]
        elif method_id == "C031":
            raw["precision_radius"] = ".75"
        elif method_id.startswith("voi_"):
            info = raw["information"]
            info["prior"] = {key: sourced(".5") for key in ("good", "bad")}
            info["cost"] = quantity(".9")
        elif method_id == "timing_actions":
            raw["timing"]["actions"]["b"]["cutoff"] = cutoff(".25", False)
        else:
            raw["timing"]["investigation"]["cost"] = sourced(".675")


def fraction_bounds(bounds):
    return tuple(Q(bounds[key]) for key in ("lower", "upper"))


def git_blob(path):
    content = path.read_bytes()
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()


def reference_regret(matrix):
    best = [max(column) for column in zip(*matrix.values(), strict=True)]
    return {key: max(upper - value for upper, value in zip(best, row, strict=True)) for key, row in matrix.items()}


def information_reference(prior, cost):
    """Enumerate all four policy mappings without the registry's VOI implementation."""
    values = {"a": (Q(6), Q(6)), "b": (Q(10), Q(0))}
    weights = ((prior * Q(".9"), (1 - prior) * Q(".3")),
               (prior * Q(".1"), (1 - prior) * Q(".7")))
    baseline = max(prior * good + (1 - prior) * bad for good, bad in values.values())
    return {policy: sum(sum(weight * value for weight, value in zip(row, values[action], strict=True))
                        for row, action in zip(weights, policy, strict=True)) - baseline - cost
            for policy in product(values, repeat=2)}


def assert_math(method_id, result, *, edge):
    if method_id == GATE_ID:
        assert [row["status"] for row in result["feasibility"]] == ["REJECT" if edge else "ACCEPT"] * 2
    elif method_id == "comparability":
        assert result["status"] == "COMPARABLE_BY_OBJECTIVE"
        assert len(result["tables"][0]["rows"]) == 4
    elif method_id == "pareto":
        assert result["pairs"][0]["relation"] == ("EQUAL" if edge else "INCOMPARABLE")
        assert result["frontier"] == ["a", "b"]
    elif method_id in {"weight_sensitivity", "c034_joint_robustness"}:
        pair = result["pairs"][0]
        first = [Q(".2")] if method_id == "weight_sensitivity" else [Q(".1"), Q(".2")]
        values = [coef * weight - Q(".3") * (1 - weight) for coef, weight in product(first, [Q(".2"), Q(".8")])]
        assert fraction_bounds(pair) == ((0, 0) if edge else (min(values), max(values)))
    elif method_id == "C029":
        expected = reference_regret({"a": (6, 6), "b": (6, 6) if edge else (10, 0)})
        assert {key: Q(value) for key, value in result["worst_regret"].items()} == expected
    elif method_id == "C030":
        b_ranges = ((5, 7), (5, 7)) if edge else ((9, 11), (-1, 1))
        corners = product((5, 7), (5, 7), *b_ranges)
        worlds = [reference_regret({"a": (ag, ab), "b": (bg, bb)}) for ag, ab, bg, bb in corners]
        assert result["worst_regret_bounds"] == {
            key: [str(min(world[key] for world in worlds)), str(max(world[key] for world in worlds))]
            for key in ("a", "b")
        }
    elif method_id == "C031":
        assert Q(result["precision_threshold"]["upper_exclusive"]) == Q(3, 4)
        assert result["strict_leaders"] == ([] if edge else ["b"])
        if edge:
            radius = Q(3, 4)
            example = {"a": (8 - radius, 2 - radius), "b": (Q("5.5") - radius,) * 2,
                       "c": (Q("2.5") + radius, 8 + radius)}
            assert {key: Q(value) for key, value in result["witness"]["worst_regret"].items()} == reference_regret(example)
    elif method_id.startswith("voi_"):
        priors = [Q(1, 2)] if edge or method_id == "voi_point" else [Q(2, 5), Q(3, 5)]
        by_prior = [information_reference(p, Q(".9") if edge else Q(".5")) for p in priors]
        if method_id == "voi_fixed_policy":
            gains = [x["b", "a"] for x in by_prior]
        elif method_id in {"voi_maximin", "voi_randomized_certificate"}:
            gains = [max(min(world[policy] for world in by_prior) for policy in by_prior[0])]
            if method_id == "voi_randomized_certificate":
                assert result["certificate_status"] == "CERTIFIED"
        else:
            gains = [max(x.values()) for x in by_prior]
        assert fraction_bounds(result["net_bounds"]) == (min(gains), max(gains))
    elif method_id == "timing_actions":
        row = next(item for item in result["strategies"] if item["type"] == "wait" and item["option_id"] == "b")
        if edge:
            assert row["status"] == "EXPIRED"
        else:
            assert Q(row["utilities"]["good"]) == 10 - Q(".25") * 2
            assert Q(row["utilities"]["bad"]) == 0
        assert result["probabilities_used"] is False
    else:
        gross = Q(".45") * (10 - Q(".25") * 2) + Q(".4") * 6 - 6
        assert Q(result["net_value"]) == gross - (Q(".675") if edge else Q(".5"))


@pytest.mark.parametrize("contract", CONTRACTS, ids=METHOD_IDS)
def test_history_resolves_to_live_descriptions_and_pinned_dependencies(contract):
    registry = DecisionHubV05().registry
    key = contract["key"]
    method = registry.get(*key.split("@"))
    description = method.describe()
    assert description in registry.describe()
    assert set(description["sources"]) == {row["path"] for row in contract["sources"]}
    assert description["source_baseline"] == contract["sourceBaseline"]
    assert method.candidate_scope == contract["scope"]
    assert list(method.depends_on) == contract["dependencies"]
    ordered = [item.key for item in registry.execution_order()]
    assert all(ordered.index(dependency) < ordered.index(key) for dependency in method.depends_on)
    for field in ("applicability", "inputs", "outputs", "units", "assumptions", "uncertainty",
                  "sources", "failure_conditions", "replay", "baseline"):
        assert description[field]


def test_live_registry_inventory_distinguishes_base_from_v05_extended():
    assert {item.key for item in DecisionHubV05().registry.methods()} == {row["key"] for row in CONTRACTS}
    assert {item.key for item in default_registry().methods()} == {row["key"] for row in CONTRACTS[:8]}


def test_current_source_bytes_keep_the_known_timing_review_visible():
    assert git_blob(INDEX) == "4ff1666907c362066dcef697d955bc6fb689b75c"
    changed = []
    for contract in CONTRACTS:
        assert git_blob(REPO / contract["module"]) == contract["moduleBlob"]
        for source in contract["sources"]:
            assert git_blob(REPO / source["path"]) == source["currentBlob"]
            if source["baselineBlob"] != source["currentBlob"]:
                changed.append((contract["key"], source["baselineBlob"], source["currentBlob"]))
                assert source["status"] == "CHANGED"
                assert contract["sourceReview"] == "REVIEW_REQUIRED"
    assert changed == [("timing_actions@1.0.0", "b611c66afbdeb862353dbad7330916afc57ac45e",
                        "e7e1002f00aab5bf782a5f2845fbfac2cb80969b")]


@pytest.mark.parametrize("method_id", METHOD_IDS)
@pytest.mark.parametrize("case", ["positive", "missing", "out_of_scope", "invalid", "edge"])
def test_native_validate_execute_and_boundary_contracts(method_id, case):
    raw = fixture(method_id)
    change_case(method_id, case, raw)
    if case == "out_of_scope" and method_id == GATE_ID:
        raw["constraints_confirmed"] = False
    state = DecisionStateV05.model_validate(raw)
    feasible = () if case == "out_of_scope" else tuple(state.options)
    hub = DecisionHubV05()
    method = hub.registry.get(method_id, "1.0.0")
    context = Context(state, feasible)
    reasons = method.validate(context)
    outcome = run_method(method, context)
    if case in {"positive", "edge"}:
        assert reasons == [] and outcome["status"] == "EXECUTED"
        assert method.execute(context) == outcome["result"]
        assert_math(method_id, outcome["result"], edge=case == "edge")
    elif case != "out_of_scope" and method_id in {GATE_ID, "comparability", "pareto"}:
        assert reasons == [] and outcome["status"] == "EXECUTED"
        result = outcome["result"]
        if method_id == GATE_ID:
            assert result["feasibility"][0]["status"] == "UNRESOLVED"
            assert result["feasibility"][0]["checks"][0]["status"] == "UNKNOWN"
        else:
            assert result["status"] == "UNKNOWN"
    else:
        assert reasons and outcome["status"] == "INELIGIBLE" and outcome["result"] is None


@pytest.mark.parametrize("method_id", METHOD_IDS)
def test_native_hub_dispatch_matches_the_arithmetic_reference(method_id):
    raw = fixture(method_id)
    if method_id == "C031":
        raw["timing"] = None
    result = DecisionHubV05().analyze(raw)
    assert result["status"] == "ANALYZED"
    assert result["methods"][0]["model_id"] == GATE_ID
    assert {option["status"] for option in result["feasibility"]} == {"ACCEPT"}
    outcome = next(method for method in result["methods"] if method["model_id"] == method_id)
    assert outcome["status"] == "EXECUTED"
    assert_math(method_id, outcome["result"], edge=False)


def test_confirmed_time_scope_recomputes_the_precision_threshold_for_current_options():
    result = DecisionHubV05().analyze(fixture("C031"))
    assert result["temporal_scope"] == {"a": "FEASIBLE", "b": "FEASIBLE", "c": "UNKNOWN"}
    outcome = next(method for method in result["methods"] if method["model_id"] == "C031")
    assert outcome["status"] == "EXECUTED"
    assert outcome["result"]["precision_threshold"] == {"option_id": "b", "upper_exclusive": "0.25"}
    assert outcome["result"]["strict_leaders"] == []


def test_violating_a_hard_limit_removes_every_other_native_method_from_dispatch():
    raw = fixture("voi_point")
    raw["constraints"][0]["operator"] = "<"
    result = DecisionHubV05().analyze(raw)
    gate, *subsequent = result["methods"]
    assert gate["model_id"] == GATE_ID and gate["status"] == "EXECUTED"
    assert {option["status"] for option in result["feasibility"]} == {"REJECT"}
    assert len(subsequent) == 14
    assert all(method["status"] == "INELIGIBLE" and method["result"] is None for method in subsequent)
