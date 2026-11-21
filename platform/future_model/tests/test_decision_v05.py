from dataclasses import replace

import pytest

from psychohistory.decision_feasibility import METHOD
from psychohistory.decision_registry import DecisionRegistry
from psychohistory.decision_v05 import DecisionHubV05, DecisionStateV05


def test_open_question_has_plan_without_invented_probability():
    hub = DecisionHubV05()
    original = "我该留在目前岗位，还是换工作？新机会可能只保留几天。"
    started = hub.start(original)
    state = started["state"]
    assert state["question"] == original
    assert state["workflow_version"] == "0.5.0"
    assert state["information"] is None
    assert not state["confirmed"]
    assert started["plan"]["items"]
    result = hub.analyze(state)
    assert result["hub_version"] == "0.5.0"
    assert result["status"] == "CLARIFY"


def test_v04_input_is_accepted_in_v05_with_original_identity():
    from psychohistory.decision_hub import DecisionHub

    v4 = DecisionHub().start("This is a fictional decision.")["state"]
    v5 = DecisionStateV05.model_validate(v4)
    assert v5.decision_id == v4["decision_id"]
    assert v5.workflow_version == "0.5.0"
    assert v5.understanding_receipt.mode == v4["understanding_receipt"]["mode"]


def test_method_dependency_needs_an_executed_version():
    registry = DecisionRegistry()
    registry.register(METHOD)
    registry.register(replace(METHOD, model_id="disabled", validate=lambda ctx: ["无适用证据"]))
    registry.register(replace(METHOD, model_id="dependent", depends_on=("disabled@1.0.0",),
                              execute=lambda ctx: {"summary": "不应执行"}))
    hub = DecisionHubV05(registry=registry)
    state = hub.start("Synthetic dependency test")["state"]
    state.update(confirmed=True, constraints_confirmed=True, deadline="一个期限",
                 objectives=[dict(id="objective", label="目标", unit="效用", direction="max")],
                 options=[dict(id="a", label="甲"), dict(id="b", label="乙")])
    result = hub.analyze(state)
    methods = {m["model_id"]: m for m in result["methods"]}
    assert methods["dependent"]["status"] == "INELIGIBLE"
    assert "disabled@1.0.0" in methods["dependent"]["reasons"][0]


def test_workflow_intent_is_not_an_execution_authorization():
    hub = DecisionHubV05()
    raw = hub.start("Synthetic alternatives")["state"]
    with pytest.raises(ValueError):
        DecisionStateV05.model_validate({**raw, "execute": True})
    with pytest.raises(ValueError):
        DecisionStateV05.model_validate({**raw, "intended_option_id": "missing"})


def test_confirmed_expired_option_cannot_be_ranked_as_available_now():
    hub = DecisionHubV05()
    state = hub.start("虚构的安排和今天的截止时点")["state"]
    state.update(confirmed=True, constraints_confirmed=True, deadline="今天",
                 objectives=[{"id": "quality", "label": "分数", "unit": "分", "direction": "max"}],
                 options=[{"id": "a", "label": "已到期的行动"},
                          {"id": "b", "label": "可用的行动"},
                          {"id": "c", "label": "可用的备选"}])
    def value(score):
        return {"lower": score, "upper": score, "unit": "分", "kind": "synthetic", "source": "合成样例"}
    def cutoff(at, inclusive=True):
        return {"at": at, "inclusive": inclusive, "kind": "synthetic", "source": "合成期限"}
    state["scenario_basis"] = "同尺度效用"
    state["scenarios"] = [{"id": "one", "label": "情景", "kind": "synthetic", "source": "合成样例",
                           "utilities": {"a": value(10), "b": value(5), "c": value(4)}}]
    state["timing"] = dict(confirmed=True, time_unit="日", time_origin="现在", horizon=cutoff(1),
                          actions={"a": {"cutoff": cutoff(0, False)}, "b": {}, "c": {}})
    analysis = hub.analyze(state)
    assert not any("已到期的行动" in advice for advice in analysis["advice"])
    assert analysis["temporal_scope"]["a"] == "EXPIRED"
    regret = next(method for method in analysis["methods"] if method["model_id"] == "C029")
    assert regret["result"]["leaders"] == ["b"]
    timing = next(method for method in analysis["methods"] if method["model_id"] == "timing_actions")
    assert any(item["status"] == "EXPIRED" for item in timing["result"]["strategies"] if item["option_id"] == "a")
