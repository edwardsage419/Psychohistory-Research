from copy import deepcopy

from psychohistory.decision_hub import DecisionHub


def decision(hub=None):
    started = (hub or DecisionHub()).start("在两份职业邀请中，三个月内如何选择？")
    state = started["state"]
    state.update(
        confirmed=True,
        constraints_confirmed=True,
        deadline="三个月内",
        objectives=[dict(id="growth", label="成长", unit="效用", direction="max")],
        constraints=[dict(id="salary", label="月收入", unit="千元/月",
                          operator=">=", threshold="10", source="虚构个人底线")],
        options=[
            dict(id="a", label="甲邀请", measurements={"salary": quantity("10", "12", "千元/月")}),
            dict(id="b", label="乙邀请", measurements={"salary": quantity("7", "9", "千元/月")}),
            dict(id="c", label="丙邀请", measurements={"salary": quantity("10", "13", "元/月")}),
        ],
    )
    return state


def quantity(lower, upper, unit, source="虚构测量"):
    return dict(lower=lower, upper=upper, unit=unit, kind="synthetic", source=source)


def test_open_question_keeps_original_and_requests_confirmation():
    hub = DecisionHub()
    original = "  要不要换工作？\n"
    started = hub.start(original)
    assert started["state"]["question"] == original
    assert started["understanding"]["mode"] == "GUIDED_CONFIRMATION"
    assert {"objectives", "options", "deadline", "constraints", "confirmed"} <= {
        q["field"] for q in started["questions"]
    }
    result = hub.analyze(started["state"])
    assert result["status"] == "CLARIFY"
    assert result["feasibility"] == []
    assert all(x["status"] != "EXECUTED" for x in result["methods"])


def test_exact_gate_unit_refusal_and_reanalysis():
    hub = DecisionHub()
    state = decision(hub)
    result = hub.analyze(state)
    assert [x["status"] for x in result["feasibility"]] == ["ACCEPT", "REJECT", "UNRESOLVED"]
    assert result["conditional_scope"]
    edit = deepcopy(state)
    edit["revision"] += 1
    edit["constraints"][0]["operator"] = ">"
    changed = hub.analyze(edit)
    assert [x["status"] for x in changed["feasibility"]] == ["UNRESOLVED", "REJECT", "UNRESOLVED"]
    assert result["input_hash"] != changed["input_hash"]
    assert changed["status"] == "UNRESOLVED"


def test_unknown_without_source_and_known_failure_are_both_recorded():
    state = decision()
    state["constraints"].append(dict(id="hours", label="每周工时", operator="<=",
                                     threshold="44", unit="小时/周", source="虚构底线"))
    state["options"][0]["measurements"]["salary"]["source"] = ""
    result = DecisionHub().analyze(state)
    a, b, _ = result["feasibility"]
    assert a["status"] == "UNRESOLVED"
    assert b["status"] == "REJECT"
    assert [c["status"] for c in b["checks"]] == ["CERTAIN_FAIL", "UNKNOWN"]


def test_unreviewed_provider_is_never_called_without_permission():
    class Provider:
        provider_id = "fictional-local"
        version = "1.0.0"

        def propose(self, original):
            raise RuntimeError("sensitive details")

    hub = DecisionHub(provider=Provider())
    assert hub.start("虚构选择")["understanding"]["mode"] == "GUIDED_CONFIRMATION"
    failed = hub.start("虚构选择", allow_provider=True)
    assert failed["understanding"]["mode"] == "PROVIDER_FAILED"
    assert "sensitive details" not in str(failed)
    assert not failed["state"]["confirmed"]


def test_method_competition_and_output_admission_are_explicit():
    from dataclasses import replace
    from psychohistory.decision_feasibility import METHOD
    from psychohistory.decision_registry import DecisionRegistry

    def candidate(name, leaders, validate=lambda ctx: []):
        return replace(METHOD, model_id=name, title=name, validate=validate,
                       execute=lambda ctx: {"summary": "虚构测试规则", "leaders": leaders})

    registry = DecisionRegistry()
    registry.register(METHOD)
    registry.register(candidate("rule-one", ["a"]))
    registry.register(candidate("rule-two", ["b"]))
    registry.register(candidate("rule-invalid", ["c"]))
    registry.register(candidate("rule-inapplicable", [], lambda ctx: ["本规则缺少来源。"]))
    registry.register(replace(METHOD, model_id="bad-gaps",
                              execute=lambda ctx: {"summary": "测试无效输出", "gaps": None}))
    state = decision()
    state["options"][1]["measurements"]["salary"] = quantity("11", "11", "千元/月")
    result = DecisionHub(registry=registry).analyze(state)
    methods = {m["model_id"]: m for m in result["methods"]}
    assert methods["rule-one"]["result"]["leaders"] == ["a"]
    assert methods["rule-two"]["result"]["leaders"] == ["b"]
    assert methods["rule-invalid"]["status"] == "FAILED"
    assert methods["rule-invalid"]["result"] is None
    assert methods["rule-inapplicable"]["status"] == "INELIGIBLE"
    assert methods["bad-gaps"]["status"] == "FAILED"
    assert "本规则缺少来源。" in result["gaps"]
    assert any("不同的优选集合" in risk for risk in result["risks"])


def test_conflicting_thresholds_cannot_be_confirmed():
    state = decision()
    state["constraints"].append(dict(id="cap", label="月收入", operator="<",
                                     threshold="10", unit="千元/月", source="虚构底线"))
    result = DecisionHub().analyze(state)
    assert result["status"] == "CLARIFY"
    assert any("互相冲突" in q["prompt"] for q in result["questions"])


def test_pending_literal_options_do_not_enter_draft_state():
    raw = "我该留在现有岗位，还是接受新岗位？预算仍待核实。"
    result = DecisionHub().start(raw)
    assert result["state"]["question"] == raw
    assert result["state"]["options"] == []
    assert [item["value"] for item in result["understanding"]["suggestions"]] == ["留在现有岗位", "接受新岗位"]


def test_incompatible_intervals_for_same_metric_block_false_accept():
    state = decision()
    state["constraints"].append(dict(id="cap", label="月收入", operator="<=",
                                     threshold="12", unit="千元/月", source="虚构底线"))
    state["options"][0]["measurements"]["cap"] = quantity("2", "3", "千元/月")
    result = DecisionHub().analyze(state)
    option = result["feasibility"][0]
    assert option["status"] == "UNRESOLVED"
    assert [check["status"] for check in option["checks"]] == ["UNKNOWN", "UNKNOWN"]
    assert "冲突" in option["checks"][0]["reason"]


def test_mutating_method_cannot_change_other_methods_or_hash():
    from dataclasses import replace
    from psychohistory.decision_feasibility import METHOD
    from psychohistory.decision_registry import DecisionRegistry

    def mutate(ctx):
        ctx.state.options[0].label = "INCORRECT"
        ctx.feasible[0].label = "INCORRECT"
        return {"summary": "虚构方法"}

    registry = DecisionRegistry()
    registry.register(METHOD)
    registry.register(replace(METHOD, model_id="mutating", execute=mutate))
    registry.register(replace(METHOD, model_id="reader",
                              execute=lambda ctx: {"summary": ctx.feasible[0].label}))
    state = decision()
    result = DecisionHub(registry=registry).analyze(state)
    assert result["methods"][-1]["result"]["summary"] == "甲邀请"
    assert result["input_hash"] == DecisionHub().analyze(state)["input_hash"]


def test_invalid_gate_output_fails_closed():
    from dataclasses import replace
    from psychohistory.decision_feasibility import METHOD
    from psychohistory.decision_registry import DecisionRegistry

    registry = DecisionRegistry()
    registry.register(replace(METHOD, execute=lambda ctx: {"summary": "缺少结构化方案判定"}))
    registry.register(replace(METHOD, model_id="unused", execute=lambda ctx: {"summary": "不应运行"}))
    result = DecisionHub(registry=registry).analyze(decision())
    assert result["status"] == "UNRESOLVED"
    assert result["feasibility"] == []
    assert [method["status"] for method in result["methods"]] == ["FAILED", "INELIGIBLE"]
