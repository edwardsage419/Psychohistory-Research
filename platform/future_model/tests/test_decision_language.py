from importlib import import_module

import pytest


def interpret(text, focus=None, **kwargs):
    return import_module("psychohistory.decision_language").interpret(text, focus, **kwargs)


def claims(text, focus=None, **kwargs):
    items = interpret(text, focus, **kwargs)["claims"]
    assert all(item["source"] and item["source"] in text for item in items)
    assert all(
        set(item) == {"kind", "field", "subject", "value", "unit", "source"}
        and all(isinstance(value, str) for value in item.values())
        for item in items
    )
    return [
        (item["kind"], item["field"], item["subject"], item["value"], item["unit"])
        for item in items
    ]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("最近在想要不要跳槽，但总觉得不太踏实。", "career"),
        ("我在犹豫续租还是去找别的房子。", "housing"),
        ("有点纠结要不要报名学数据分析的课程。", "learning"),
        ("最近花钱太多了，想重新规划一下开支。", "budget"),
        ("在想怎样让现在的生活有一点变化。", "life"),
        ("我该不该从成都搬去杭州？", "moving"),
        ("挺担心风险，不知道要不要赌一把。", "risk"),
        ("这件事想了好久，能帮我梳理一下吗？", "general"),
    ],
)
def test_vague_narratives_keep_plain_intent_and_broad_domain(text, expected):
    result = interpret(text)
    assert result["domain"] == expected
    assert result["intent"].strip()


def test_choice_phrase_yields_literal_options_and_scoped_evidence():
    user = (
        "我在纠结留在原岗位还是去新公司。"
        "我不能搬家，每周最多到岗两天。新公司需要搬家。原岗位每周到岗一天。"
    )
    result = interpret(user)
    assert result["options"] == ["留在原岗位", "去新公司"]
    assert all(option in user for option in result["options"])
    found = claims(user)
    assert ("constraint", "move_allowed", "", "no", "") in found
    assert ("constraint", "onsite_max", "", "2", "days/week") in found
    assert ("measurement", "move_required", "去新公司", "yes", "") in found
    assert ("measurement", "onsite", "留在原岗位", "1", "days/week") in found


def test_structured_labels_keep_measurements_apart_across_sentences():
    user = "方案甲：费用三千八百元，每周学习六小时；方案乙：费用4,200元，每周学习八个小时。"
    assert interpret(user)["options"] == ["方案甲", "方案乙"]
    found = claims(user)
    assert ("measurement", "cost", "方案甲", "3800", "yuan") in found
    assert ("measurement", "hours", "方案甲", "6", "hours/week") in found
    assert ("measurement", "cost", "方案乙", "4200", "yuan") in found
    assert ("measurement", "hours", "方案乙", "8", "hours/week") in found


def test_mentioned_hard_cap_is_separate_from_tentative_change():
    user = "预算原来上限四千元。如果能退费，预算就可以提高到五千元。现阶段最多花四千元。"
    found = claims(user)
    assert ("previous", "cost_max", "", "4000", "yuan") in found
    assert ("conditional", "cost_max", "", "5000", "yuan") in found
    assert ("constraint", "cost_max", "", "4000", "yuan") in found
    assert ("constraint", "cost_max", "", "5000", "yuan") not in found


def test_scoped_negation_distinguishes_relocation_constraints_from_preferences():
    user = "不是不能搬家，是不想搬得太远。B不需要搬家，C可能要搬家。"
    found = claims(user)
    assert all(field != "move_allowed" for _, field, *_ in found)
    assert ("measurement", "move_required", "B", "no", "") in found
    assert ("estimate", "move_required", "C", "yes", "") in found
    assert any(kind == "preference" and "不想搬得太远" in value for kind, _, _, value, _ in found)


def test_conditional_negation_keeps_exception_and_never_becomes_a_global_rule():
    user = "除非能远程，否则我不能搬家。若只是每周去一天，我可以搬家。"
    found = claims(user)
    assert ("conditional", "move_allowed", "", "no", "") in found
    assert ("conditional", "move_allowed", "", "yes", "") in found
    assert all(not (kind == "constraint" and field == "move_allowed") for kind, field, *_ in found)
    move = [item for item in interpret(user)["claims"] if item["field"] == "move_allowed"]
    assert "除非能远程" in move[0]["source"]


def test_correction_emits_only_the_new_candidate_as_revision():
    found = claims("我原来每周最多到岗两天，现在把上限从两天改为三天。", "onsite_max")
    assert ("previous", "onsite_max", "", "2", "days/week") in found
    assert ("revision", "onsite_max", "", "3", "days/week") in found
    assert not any(kind == "constraint" and field == "onsite_max" for kind, field, *_ in found)


def test_short_focused_answer_needs_context_for_implicit_units_or_subject():
    assert claims("两天。") == []
    assert claims("两天。", "onsite_max") == [("constraint", "onsite_max", "", "2", "days/week")]
    assert claims("三天", "onsite:岗位乙") == [("measurement", "onsite", "岗位乙", "3", "days/week")]
    assert claims("不需要。", "move_required:岗位乙") == [
        ("measurement", "move_required", "岗位乙", "no", ""),
    ]


def test_salary_and_rent_periods_remain_explicit():
    user = "每月收入至少一万二。A月薪１．５万，B月租三千五元，预算总额上限五万元。"
    found = claims(user)
    assert ("constraint", "income_min", "", "12000", "yuan/month") in found
    assert ("measurement", "income", "A", "15000", "yuan/month") in found
    assert ("measurement", "cost", "B", "3500", "yuan/month") in found
    assert ("constraint", "cost_max", "", "50000", "yuan") in found


def test_ranges_and_hedges_are_never_promoted_to_a_precise_endpoint():
    user = "A每周到岗三到五天。预算大概三千元。可能每周最多花十小时。"
    found = claims(user)
    assert not any(kind in {"constraint", "measurement"} for kind, *_ in found)
    assert any(kind == "estimate" and field == "cost_max" for kind, field, *_ in found)


def test_narrative_goals_preferences_and_deadlines_do_not_create_probabilities_or_weights():
    user = "我的目标是积累管理经验，我最看重稳定性，周五之前必须决定。听说有80%成功率，我可能给它七成权重。"
    found = claims(user)
    assert ("goal", "goal", "", "积累管理经验", "") in found
    assert ("preference", "preference", "", "稳定性", "") in found
    assert any(kind == "deadline" and value == "周五之前" for kind, _, _, value, _ in found)
    assert all(field not in {"weight", "probability"} for _, field, *_ in found)


def test_no_unsupported_move_fact_from_remote_work_or_double_negation():
    found = claims("A是远程岗位。我也不是不可以搬家。目前还不知道B是否必须搬家。")
    assert not any(kind in {"constraint", "measurement"} for kind, *_ in found)


def test_explicit_compare_joins_full_literal_options_with_and():
    user = "我想比较留在本城和去外地。去外地需要搬家，留在本城不需要搬家。"
    assert interpret(user)["options"] == ["留在本城", "去外地"]
    assert ("measurement", "move_required", "去外地", "yes", "") in claims(user)
    assert ("measurement", "move_required", "留在本城", "no", "") in claims(user)


def test_period_units_follow_subject_bound_evidence():
    user = "甲的工资是每月8000元。房源A每月2600元。"
    assert ("measurement", "income", "甲", "8000", "yuan/month") in claims(user)
    assert ("measurement", "cost", "房源A", "2600", "yuan/month") in claims(user)


def test_explicit_conditional_relocation_keeps_prior_constraint_and_requires_sufficient_rule():
    text = "我不能搬家，如果每周到岗不超过三天，我就可以搬家。"
    found = claims(text)
    assert ("constraint", "move_allowed", "", "no", "") in found
    assert ("conditional", "move_if_onsite_max", "", "3", "days/week") in found

    text = "如果每周不超过三天到岗，我可以考虑搬家。"
    assert not any(field == "move_if_onsite_max" for _, field, *_ in claims(text))

    text = "每周到岗低于三天才可以搬家。"
    assert not any(field == "move_if_onsite_max" for _, field, *_ in claims(text))


def test_strict_comparator_keeps_direction_and_currency_scope():
    assert ("strict_constraint", "onsite_max", "", "3", "days/week") in claims("每周到岗少于三天")
    assert not any(field == "cost_max" for _, field, *_ in claims("预算不能低于五千元。"))
    assert not any(field == "cost_max" for _, field, *_ in claims("预算不能超过五千美元。"))


def test_incomplete_preceding_statement_becomes_evidence_of_a_revision_not_an_active_limit():
    found = claims("不是说预算上限三千，是四千。")
    assert ("previous", "cost_max", "", "3000", "yuan") in found
    assert ("revision", "cost_max", "", "4000", "yuan") in found
    assert ("revision", "onsite_max", "", "3", "days/week") in claims("改成三天。", "onsite_max")


def test_open_comparison_and_explicit_lettered_alternatives():
    text = "A是本地岗位，B是异地岗位。"
    assert interpret(text)["options"] == ["A", "B"]
    assert interpret("房租和预算都要核对。")["options"] == []


def test_existing_option_context_resolves_literal_unambiguous_aliases_without_creating_options():
    options = ["报名周末夜课", "继续自主练习"]
    user = "夜课每周需要七小时。"
    result = interpret(user, known_options=options)
    assert not result["options"]
    assert ("measurement", "hours", "报名周末夜课", "7", "hours/week") in claims(
        user, known_options=options,
    )
    assert not any(field == "hours" for _, field, *_ in claims(
        user, known_options=[*options, "报名另一个夜课"],
    ))


def test_amounts_stated_inside_choice_keep_option_scope_and_current_month_budget():
    text = "我该现在花七百元更换物品，还是先花一百元维修？本月最多能动用五百元。"
    found = claims(text)
    assert ("measurement", "cost", "现在花七百元更换物品", "700", "yuan") in found
    assert ("measurement", "cost", "先花一百元维修", "100", "yuan") in found
    assert ("constraint", "cost_max", "", "500", "yuan") in found


def test_hoped_for_date_stays_distinct_from_an_explicit_weekend_deadline():
    assert not any(field == "deadline" for _, field, *_ in claims("希望三周内决定。"))
    assert ("deadline", "deadline", "", "周末前", "") in claims("我周末前决定。")


def test_casual_explicit_residential_movement_is_gated_without_treating_items_as_homes():
    found = claims("A不用搬，B需要搬。我的办公桌不能搬到门口。")
    assert ("measurement", "move_required", "A", "no", "") in found
    assert ("measurement", "move_required", "B", "yes", "") in found
    assert not any(field == "move_allowed" for _, field, *_ in found)


def test_hedged_or_negated_willingness_never_becomes_positive_relocation_permission():
    found = claims("我不太能搬家，也不愿意搬家。如果到岗每周最多三天，我就可能搬家。")
    assert not any(kind in {"constraint", "conditional"} and field.startswith("move_") for kind, field, *_ in found)
    assert any(kind == "preference" and "不愿意搬家" in value for kind, _, _, value, _ in found)
