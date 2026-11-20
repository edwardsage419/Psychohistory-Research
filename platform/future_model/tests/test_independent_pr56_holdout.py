"""Independent held-out acceptance examples, authored before the v0.4 PR repair pass.

Original standalone review fixture: pr56_independent_holdout.py (2026-11-20).
One-time independent evaluation on the original candidate must be reported
separately from subsequent regression runs after any fixes.
All data are fictitious. No private user data or empirical claims.
"""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from uuid import uuid4
import pytest

from psychohistory.decision_hub import DecisionHub
from psychohistory.decision_records import DecisionRecords

HORIZON = "独立验收虚构时间段"
SOURCE = "审查专用虚构区间，非真实世界估计"

def q(low, high=None, unit="utility"):
    return {"lower": str(low), "upper": str(low if high is None else high),
            "unit": unit, "kind": "synthetic", "source": SOURCE, "horizon": HORIZON}

def baseline(options=("a", "b")):
    return {"schema_version": "1.0.0", "decision_id": uuid4().hex, "revision": 1,
            "question": "请比较虚构方案，供独立软件验收。",
            "confirmed": True, "deadline": HORIZON, "constraints_confirmed": True,
            "objectives": [{"id": "u", "label": "效用", "unit": "utility", "direction": "max"}],
            "options": [{"id": key, "label": f"方案{key.upper()}"} for key in options]}

def result_of(report, model_id):
    found = [item for item in report["methods"] if item["model_id"] == model_id]
    assert len(found) == 1, (model_id, found)
    assert found[0]["status"] == "EXECUTED", found[0]
    return found[0]["result"]

def scenarios(state, scores, *, intervals=False):
    count = len(next(iter(scores.values())))
    state["scenario_basis"] = "所有虚构情景共用同一基数效用尺度与时限。"
    state["scenario_dependence"] = "rectangle"
    state["scenario_dependence_source"] = SOURCE
    state["scenarios"] = [
        {"id": f"s{i}", "label": f"情景{i}", "kind": "synthetic", "source": SOURCE,
         "utilities": {key: (q(*values[i]) if intervals else q(values[i]))
                       for key, values in scores.items()}}
        for i in range(count)]

def test_holdout_strict_constraint_equality_and_crossing():
    state = baseline(("a", "b", "c"))
    state["constraints"] = [{"id": "floor", "label": "虚构最低值",
                             "unit": "unit", "operator": ">", "threshold": "10",
                             "source": SOURCE, "horizon": HORIZON}]
    for option, pair in zip(state["options"], [(10, 10), (10, 12), (11, 13)], strict=True):
        option["measurements"] = {"floor": q(*pair, unit="unit")}
    rows = result_of(DecisionHub().analyze(state), "c028_interval_feasibility")["feasibility"]
    assert [row["status"] for row in rows] == ["REJECT", "UNRESOLVED", "ACCEPT"]

def test_holdout_incompatible_units_cannot_be_silently_converted():
    state = baseline()
    state["constraints"] = [{"id": "time", "label": "最大时间", "unit": "小时",
                             "operator": "<=", "threshold": "6", "source": SOURCE}]
    state["options"][0]["measurements"] = {"time": q(1, 2, "天")}
    state["options"][1]["measurements"] = {"time": q(7, 8, "小时")}
    rows = result_of(DecisionHub().analyze(state), "c028_interval_feasibility")["feasibility"]
    assert [row["status"] for row in rows] == ["UNRESOLVED", "REJECT"]
    assert rows[0]["checks"][0]["status"] == "UNKNOWN"

def test_holdout_minimax_regret_and_maximin_disagree():
    state = baseline()
    scenarios(state, {"a": [100, 0], "b": [55, 40]})
    result = result_of(DecisionHub().analyze(state), "C029")
    assert result["leaders"] == ["a"]
    assert result["maximin_leaders"] == ["b"]
    assert {key: Fraction(value) for key, value in result["worst_regret"].items()} == {
        "a": Fraction(40), "b": Fraction(45)}

def test_holdout_rejected_high_utility_option_stays_excluded():
    state = baseline(("a", "b", "c"))
    state["constraints"] = [{"id": "cap", "label": "成本上限", "unit": "cost",
                             "operator": "<=", "threshold": "10", "source": SOURCE}]
    for option, amount in zip(state["options"], [2, 4, 100], strict=True):
        option["measurements"] = {"cap": q(amount, unit="cost")}
    scenarios(state, {"a": [10, 10], "b": [9, 9], "c": [100000, 100000]})
    report = DecisionHub().analyze(state)
    assert result_of(report, "c028_interval_feasibility")["feasibility"][2]["status"] == "REJECT"
    result = result_of(report, "C029")
    assert set(result["regret"]) == {"a", "b"} and result["leaders"] == ["a"]

def test_holdout_interval_regret_touching_boundary_is_not_strict():
    state = baseline()
    scenarios(state, {"a": [(0, 2), (6, 7)], "b": [(5, 7), (4, 5)]}, intervals=True)
    result = result_of(DecisionHub().analyze(state), "C030")
    assert {key: tuple(map(Fraction, value))
            for key, value in result["worst_regret_bounds"].items()} == {
                "a": (Fraction(3), Fraction(7)), "b": (Fraction(1), Fraction(3))}
    assert result["leaders"] == ["b"]
    assert result["strict_leaders"] == []

def weighted_state(radius):
    state = baseline()
    state["objectives"] = [
        {"id": "x", "label": "指标X", "unit": "utility", "direction": "max"},
        {"id": "y", "label": "指标Y", "unit": "utility", "direction": "max"}]
    state["weights_confirmed"] = True
    state["weights"] = {"x": {"lower": "0.55", "upper": "0.65"},
                        "y": {"lower": "0.35", "upper": "0.45"}}
    state["score_basis"] = "虚构可补偿的共同基数效用量尺"
    state["score_dependence"] = "rectangle"
    state["score_dependence_source"] = SOURCE
    state["score_transform"] = "identity"
    centers = ((Decimal("0.9"), Decimal("0.1")), (Decimal("0.2"), Decimal("0.8")))
    r = Decimal(radius)
    for option, values in zip(state["options"], centers, strict=True):
        option["scores"] = {
            "x": q(values[0] - r, values[0] + r),
            "y": q(values[1] - r, values[1] + r)}
    return state

def test_holdout_joint_weight_and_score_error_exact_boundary():
    first = result_of(DecisionHub().analyze(weighted_state("0.02")), "c034_joint_robustness")["pairs"][0]
    assert first["relation"] == "A_STRICT"
    assert Fraction(first["lower"]) == Fraction(3, 100)
    assert Fraction(first["upper"]) == Fraction(25, 100)
    equal = result_of(DecisionHub().analyze(weighted_state("0.035")), "c034_joint_robustness")["pairs"][0]
    assert equal["relation"] == "UNRESOLVED" and Fraction(equal["lower"]) == 0

def test_holdout_revocation_rejects_original_and_regenerated_authorization(tmp_path):
    store = DecisionRecords(tmp_path / "private_personal")
    assert not (tmp_path / "private_personal").exists()
    old = store.grant()["epoch"]
    state = baseline()
    # Use the public service input contract: normalize schema defaults before saving.
    # DecisionRecords is a lower-level store, and its snapshot hash binds canonical state.
    from psychohistory.decision_state import DecisionState
    normalized = DecisionState.model_validate(state).model_dump(mode="json")
    store.save(old, normalized, DecisionHub().analyze(normalized))
    exported = store.export(old)
    assert exported["signature"]
    assert store.revoke(old)["authorized"] is False
    with pytest.raises(PermissionError):
        store.restore(old, exported, confirm=True)
    new = store.grant()["epoch"]
    assert new != old
    preview = store.restore(new, exported, confirm=False)
    assert preview["mode"] == "preview" and preview["eligible"] is False
    with pytest.raises(ValueError):
        store.restore(new, exported, confirm=True)

def test_holdout_raw_question_requires_explicit_confirmation():
    raw = "需要在两年内选择照顾家人或去外地发展，我最在意的条件还没整理好。"
    start = DecisionHub().start(raw)
    assert start["state"]["question"] == raw
    assert start["state"]["confirmed"] is False
    assert start["understanding"]["mode"] == "GUIDED_CONFIRMATION"
    assert DecisionHub().analyze(start["state"])["status"] == "CLARIFY"
