import pytest

from psychohistory.decision_language import interpret


def test_quantity_and_date_candidates_preserve_separate_exact_spans():
    text = "  12月1日前确认，收入一亿零三万，成功率七成，费用三千五，成本20%。"
    semantic = interpret(text)["semantic"]
    candidates = semantic["candidates"]
    assert all(text[item["span"]["start"]:item["span"]["end"]] == item["source"] for item in candidates)
    assert any(item["kind"] == "date" and item["source"] == "12月1日前" for item in candidates)
    quantities = {item["source"]: item for item in candidates if item["kind"] == "quantity"}
    assert "12" not in quantities and "1" not in quantities
    assert quantities["一亿零三万"]["value"] == "100030000"
    assert quantities["三千五"]["reading"] == "COLLOQUIAL_ELLIPSIS"
    assert quantities["三千五"]["unit"] is None
    assert quantities["七成"]["ratio"] == "0.7"
    assert quantities["20%"]["ratio"] == "0.2"


@pytest.mark.parametrize("text, reason", [
    ("预算最多3000韩元", "VERIFY_CURRENCY"),
    ("预算最多3000KRW", "VERIFY_CURRENCY"),
    ("预算最多3000", "VERIFY_CURRENCY"),
    ("每天预算最多3000元", "VERIFY_PERIOD"),
    ("朋友说预算最多3000元", "VERIFY_SUBJECT"),
    ("‘预算最多3000元’是同事的要求", "VERIFY_SUBJECT"),
])
def test_unsupported_scopes_keep_hard_obligation(text, reason):
    result = interpret(text)
    assert any(item["reason"] == reason and item["hard"] for item in result["semantic"]["unknowns"])
    if reason != "VERIFY_CURRENCY" or not text.endswith("3000"):
        assert not any(item["field"] == "cost_max" for item in result["claims"])


@pytest.mark.parametrize(("text", "field", "operator"), [
    ("每周工时不能少于40小时", "hours_min", ">="),
    ("每月工资不能多于3000元", "income_max", "<="),
    ("预算不少于3000元", "cost_min", ">="),
    ("每周工时超过40小时", "hours_min", ">"),
])
def test_full_negation_projects_the_intended_direction(text, field, operator):
    result = interpret(text)
    assert [item["field"] for item in result["claims"]] == [field]
    assert result["semantic"]["obligations"][0]["operator"] == operator


def test_option_narrative_does_not_become_personal_goal():
    result = interpret("方案A：目标是提高收入。", known_options=["方案A", "方案B"])
    assert not any(item["field"] == "goal" and not item["subject"] for item in result["claims"])


def test_dismissed_constraint_cannot_discharge_independent_obligation():
    from psychohistory.decision_language import blocking_obligations

    result = interpret("预算最多3000元")
    claim = result["claims"][0]
    assert blocking_obligations([result["semantic"]], [{**claim, "status": "DISMISSED"}], [])
    assert not blocking_obligations([result["semantic"]], [{**claim, "status": "USER_CONFIRMED"}], [])


def test_joint_budget_uses_exact_sum_in_native_gate():
    from psychohistory.decision_conversation_math import build_state
    from psychohistory.decision_feasibility import check_constraint
    from psychohistory.decision_v05 import DecisionHubV05, DecisionStateV05

    text = (
        "房租和停车费合计每月最多3000元。"
        "A：每月房租2600元，停车费每月500元。"
        "B：每月房租2600元，停车费每月300元。"
        "C：每月房租2600元，停车费300。"
    )
    result = interpret(text)
    assert [item["field"] for item in result["claims"]].count("rent_parking_max") == 1
    assert any(item["subject"] == "C" and item["reason"] == "VERIFY_CURRENCY"
               for item in result["semantic"]["unknowns"])
    base = DecisionStateV05.model_validate(DecisionHubV05().start(text)["state"])
    options = [{"id": label, "label": label, "status": "CONFIRMED"} for label in "ABC"]
    claims = [{**item, "id": str(i)} for i, item in enumerate(result["claims"])]
    state = build_state(base, options, claims, ready=True)
    cap = next(item for item in state.constraints if item.id == "talk-rent_parking_max")
    statuses = [check_constraint(cap, option.measurements.get(cap.id), state.deadline)[0] for option in state.options]
    assert statuses == ["CERTAIN_FAIL", "CERTAIN_PASS", "UNKNOWN"]
    assert "2600元" in state.options[0].measurements[cap.id].source
    assert "500元" in state.options[0].measurements[cap.id].source


def test_night_shift_policy_is_separate_from_actual_schedule_evidence():
    text = (
        "我不接受夜班。A：老板说没有夜班。B：当前实际排班有夜班。"
        "C：当前实际排班没有夜班。D：承诺不安排夜班。"
    )
    result = interpret(text)
    observed = {item["subject"]: item["value"] for item in result["claims"]
                if item["field"] == "night_shift_required"}
    assert observed == {"B": "yes", "C": "no"}
    assert any(item["field"] == "night_shift_max" and item["value"] == "0" for item in result["claims"])
    assert {"A", "D"} <= {item["subject"] for item in result["semantic"]["unknowns"]}


def test_unparsed_conditional_refusal_retains_hard_source_obligation():
    result = interpret("只要夜班我就不去。")
    [obligation] = result["semantic"]["obligations"]
    assert obligation["source"] == "只要夜班我就不去"
    assert obligation["condition"]
    assert obligation["reason"] == "VERIFY_CONDITION"
    assert result["semantic"]["candidates"] == []


def test_missing_evidence_is_visible_without_an_inferred_policy():
    result = interpret("车位得问房东。")
    assert not result["semantic"]["obligations"]
    [unknown] = result["semantic"]["unknowns"]
    assert unknown["source"] == "车位得问房东"
    assert unknown["field"] == "parking_monthly"
    assert unknown["reason"] == "VERIFY_PARKING"


def test_duration_number_is_not_a_civil_calendar_day():
    result = interpret("12月1日签约，七天内能退。")["semantic"]
    assert [item["source"] for item in result["candidates"] if item["kind"] == "date"] == ["12月1日"]
    assert any(item["value"] == "7" and item["unit"] == "day" and item["reading"] == "DURATION"
               for item in result["candidates"])


def test_confirmed_explicit_restatement_repairs_only_matching_missing_unit():
    from psychohistory.decision_language import blocking_obligations

    before = interpret("房租和停车费合计每月最多3000")
    after = interpret("房租和停车费合计每月最多3000元")
    later = {**after["claims"][0], "status": "USER_CONFIRMED"}
    assert not blocking_obligations([before["semantic"], after["semantic"]], [later], [])
    assert blocking_obligations([after["semantic"], before["semantic"]], [later], [])
    assert blocking_obligations([before["semantic"], after["semantic"]],
                                [{**later, "status": "DISMISSED"}], [])


def test_supersession_chain_keeps_older_bounds_resolved():
    from psychohistory.decision_language import blocking_obligations

    first = interpret("每周最多到岗两天")
    next_turn = interpret("改成每周最多到岗三天")
    last = interpret("改成每周最多到岗四天")
    turns = [first, next_turn, last]
    claims = []
    for i, turn in enumerate(turns):
        claims.append({**turn["claims"][0], "id": str(i),
                       "status": "USER_CONFIRMED" if i == 2 else "SUPERSEDED",
                       "supersedes": str(i - 1) if i else None})
    assert not blocking_obligations([turn["semantic"] for turn in turns], claims, [])


def test_recognized_decision_deadline_does_not_sink_confirmed_attendance_gate():
    from psychohistory.decision_conversation import ConversationHub

    question = (
        "我在比较两个工作岗位。方案甲：每周到岗一天，不需要搬家；"
        "方案乙：每周到岗三天，不需要搬家。每周最多到岗两天。"
        "我的目标是积累管理经验，周五之前必须决定。"
    )
    hub = ConversationHub()
    started = hub.start(question)
    checked = hub.confirm(started["session_id"], started["revision"], accept_context=True,
                          claim_ids=[item["id"] for item in started["claims"]],
                          option_ids=[item["id"] for item in started["options"]])
    assert not checked["semantic"]["blocking_obligations"]
    assert {item["label"]: item["status"] for item in checked["analysis"]["feasibility"]} == {
        "方案甲": "ACCEPT", "方案乙": "REJECT",
    }
    assert checked["state"]["deadline"] == "周五之前"


def test_unrelated_budget_does_not_resolve_implicit_currency():
    from psychohistory.decision_language import blocking_obligations

    rent = interpret("租房预算最多3000")
    car = interpret("买车预算最多3000元")
    assert car["claims"]
    claims = [{**item, "status": "USER_CONFIRMED"} for item in car["claims"]]
    assert blocking_obligations([rent["semantic"], car["semantic"]], claims, [])


def test_claim_candidates_retain_exact_source_role_and_negated_comparison():
    text = " 🧾每周工时不能少于40小时。"
    result = interpret(text)
    [candidate] = result["semantic"]["claim_candidates"]
    assert candidate["role"] == "constraint"
    assert candidate["operator"] == ">="
    assert candidate["negation"]
    assert candidate["source_identity"] == "current_user"
    assert text[candidate["span"]["start"]:candidate["span"]["end"]] == candidate["source"]


def test_unresolved_retraction_preserves_original_hard_obligation():
    result = interpret("我撤回上一条底线。")
    [obligation] = result["semantic"]["obligations"]
    assert obligation["revision"] == "retract"
    assert obligation["reason"] == "VERIFY_REVISION"
