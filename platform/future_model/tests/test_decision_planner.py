from psychohistory.decision_hub import DecisionHub
from psychohistory.decision_state import DecisionState


def quantity(lower, upper=None, unit="元"):
    return {"lower": lower, "upper": lower if upper is None else upper,
            "unit": unit, "kind": "synthetic", "source": "虚构数据"}


def decision():
    return {
        "decision_id": "0" * 32,
        "revision": 1,
        "question": "我该上现场课程，还是学习线上课程？",
        "confirmed": True,
        "deadline": "本周",
        "constraints_confirmed": True,
        "constraints": [{"id": "cost", "label": "费用", "unit": "元", "operator": "<=",
                         "threshold": 100, "source": "虚构上限"}],
        "objectives": [{"id": "access", "label": "易参与程度", "unit": "分", "direction": "max"}],
        "options": [
            {"id": "live", "label": "现场课程", "measurements": {"cost": quantity(75, 125)}},
            {"id": "online", "label": "线上课程", "measurements": {"cost": quantity(90)},
             "scores": {"access": quantity(8, unit="分")}},
        ],
    }


def analyze(state):
    return DecisionHub().analyze({key: value for key, value in state.items() if key in DecisionState.model_fields})


def planned(state, analysis=None):
    from psychohistory.decision_planner import plan

    return plan(state, analyze(state) if analysis is None else analysis)


def find(result, kind, **target):
    return [item for item in result["items"] if item["category"] == kind
            and all(item["target"].get(key) == value for key, value in target.items())]


def test_open_draft_targets_clarification_without_forcing_advanced_models():
    state = {"question": "我该调整短途出行方式吗？"}
    result = planned(state, {})
    assert find(result, "CLARIFICATION", field="options")
    assert not find(result, "EVIDENCE")
    assert not find(result, "MODEL_ASSUMPTIONS")
    assert result["can_run"] == []
    assert result["steps"][0] == {"stage": "UNDERSTAND", "status": "NEEDS_INPUT"}


def test_straddling_feasibility_fact_is_pivotal_before_comparison():
    result = planned(decision())
    first = result["items"][0]
    assert first["category"] == "FEASIBILITY"
    assert first["priority"] == "HIGH"
    assert first["target"] == {"field": "measurements", "option_id": "live", "constraint_id": "cost"}
    assert not find(result, "FEASIBILITY", option_id="online")
    assert not find(result, "COMPARABILITY", option_id="live")


def test_independent_failure_defers_unknown_for_same_option_even_if_inputs_change():
    state = decision()
    state["options"][0]["measurements"]["cost"] = quantity(101)
    state["constraints"].append({"id": "duration", "label": "完成时间", "unit": "小时", "operator": "<=",
                                 "threshold": 4, "source": "虚构时间上限"})
    state["options"][1]["measurements"]["duration"] = quantity(3, unit="小时")
    result = planned(state)
    gap, = find(result, "FEASIBILITY", option_id="live", constraint_id="duration")
    assert (gap["priority"], gap["action"], gap["evidence_status"]) == ("DEFERRED", "DEFER", "LOGICAL_INVARIANT")
    assert gap["proof"]["witness_constraint_id"] == "cost"
    assert gap["proof"]["scope"] == "CURRENT_FEASIBILITY_GATE"
    assert not find(result, "FEASIBILITY", option_id="online", constraint_id="duration")


def test_uncertain_fact_is_not_deferred_when_other_condition_is_also_uncertain():
    state = decision()
    state["constraints"].append({"id": "duration", "label": "完成时间", "unit": "小时", "operator": "<=",
                                 "threshold": 4, "source": "虚构时间上限"})
    state["options"][1]["measurements"]["duration"] = quantity(3, unit="小时")
    result = planned(state)
    gaps = find(result, "FEASIBILITY", option_id="live")
    assert {item["target"]["constraint_id"] for item in gaps} == {"cost", "duration"}
    assert not any(item["action"] == "DEFER" for item in gaps)


def test_missing_comparable_attribute_targets_only_the_gap_in_the_feasible_set():
    state = decision()
    state["options"][0]["measurements"]["cost"] = quantity(75)
    result = planned(state)
    gap, = find(result, "COMPARABILITY", option_id="live", objective_id="access")
    assert gap["action"] == "VERIFY"
    assert not find(result, "COMPARABILITY", option_id="online", objective_id="access")
    assert not find(result, "CLARIFICATION")
    assert "comparability" in {method["model_id"] for method in result["can_run"]}


def test_unknown_voi_evidence_is_requested_only_when_learning_is_relevant():
    state = decision()
    state["question"] = "我该先打听课程反馈再决定，还是本周直接报名？"
    state["intent"] = "在报名之前获取课程信息"
    result = planned(state)
    assert find(result, "EVIDENCE", field="information")
    assert not set(result) & {"evsi", "evpi", "information_value"}
    assert not find(planned(decision()), "EVIDENCE", field="information")


def test_timing_questions_target_action_opportunity_without_guessing_a_deadline():
    state = decision()
    state["question"] = "是否等课程反馈再报名？怕报名截止，名额可能过期。"
    result = planned(state)
    gap, = find(result, "TIMING", field="timing")
    assert gap["evidence_status"] == "UNKNOWN"
    assert not find(result, "CLARIFICATION", field="deadline")
    assert ("TIMING", "NEEDS_INPUT") in {(step["stage"], step["status"]) for step in result["steps"]}


def test_disagreeing_scenario_rules_keep_their_separate_scopes():
    state = decision()
    state["options"][0]["measurements"]["cost"] = quantity(75)
    state["scenario_basis"] = "相同效用单位和观察期"
    state["scenarios"] = [
        {"id": "ordinary", "label": "普通工作量", "kind": "synthetic", "source": "虚构情景",
         "utilities": {"live": quantity(12, unit="分"), "online": quantity(6, unit="分")}},
        {"id": "busy", "label": "工作量大", "kind": "synthetic", "source": "虚构情景",
         "utilities": {"live": quantity(0, unit="分"), "online": quantity(5, unit="分")}},
    ]
    result = planned(state)
    gap, = find(result, "MODEL_ASSUMPTIONS", field="scenarios")
    assert gap["action"] == "COMPARE"
    assert gap["evidence_status"] == "CONDITIONAL"


def test_exact_weight_reversal_prioritizes_preference_clarification():
    state = decision()
    state["options"][0]["measurements"]["cost"] = quantity(75)
    state["objectives"].append({"id": "quality", "label": "教学质量", "unit": "分", "direction": "max"})
    state["options"][0]["scores"] = {"access": quantity(6, unit="分"), "quality": quantity(8, unit="分")}
    state["options"][1]["scores"]["quality"] = quantity(6, unit="分")
    state["score_basis"] = "相同基数效用单位"
    state["weights_confirmed"] = True
    state["weights"] = {"access": {"lower": ".25", "upper": ".75"}, "quality": {"lower": ".25", "upper": ".75"}}
    result = planned(state)
    gap, = find(result, "SENSITIVITY", field="weights")
    assert gap["evidence_status"] == "CONDITIONAL"
    assert gap["proof"]["scope"] == "CURRENT_MODEL_AND_FEASIBLE_SET"
    assert (gap["proof"]["lower"], gap["proof"]["upper"]) == ("-1", "1")


def test_known_information_inputs_do_not_reprompt_for_confirmed_fields():
    state = decision()
    state["question"] = "该不该先收集反馈再决定？"
    state["information"] = {
        "signals": [{"id": "positive"}, {"id": "negative"}],
        "prior": {"good": quantity(".5", unit="1"), "bad": quantity(".5", unit="1")},
        "likelihoods": {"good": {"positive": quantity(".9", unit="1"), "negative": quantity(".1", unit="1")},
                        "bad": {"positive": quantity(".1", unit="1"), "negative": quantity(".9", unit="1")}},
        "cost": quantity(0, unit="分"),
        "unrestricted_actions": True,
        "action_source": "虚构复选条件",
        "timing_basis": "在期限内到达，可保留两项选择",
    }
    state["scenarios"] = [{"id": "good"}, {"id": "bad"}]
    summary = {"feasibility": [], "methods": [{
        "model_id": "voi_point", "title": "样本信息价值", "status": "EXECUTED",
        "result": {"decision": "POSITIVE", "evsi": ".15"},
    }]}
    result = planned(state, summary)
    assert not find(result, "EVIDENCE", field="information")
    assert result["can_run"] == [{"model_id": "voi_point", "title": "样本信息价值"}]


def test_explicit_unverified_evidence_is_qualified_and_confirmed_evidence_is_skipped():
    state = decision()
    state["evidence"] = [
        {"id": "dates", "label": "课程日期", "kind": "estimate", "source": "内部公告",
         "verification": "unverified", "scope": "本次开班"},
        {"id": "fees", "label": "报名费用", "kind": "fact", "source": "已查阅的费用说明",
         "verification": "user_confirmed", "scope": "本次开班"},
    ]
    result = planned(state)
    assert find(result, "EVIDENCE", evidence_id="dates")
    assert not find(result, "EVIDENCE", evidence_id="fees")


def test_scenario_question_targets_missing_utility_only_for_a_feasible_option():
    state = decision()
    state["options"][0]["measurements"]["cost"] = quantity(75)
    state["options"].append({"id": "private", "label": "私人辅导", "measurements": {"cost": quantity(150)}})
    state["scenario_basis"] = "相同效用单位和观察期"
    state["scenarios"] = [
        {"id": "busy", "label": "工作量大", "kind": "synthetic", "source": "虚构情景",
         "utilities": {"online": quantity(6, unit="分")}},
    ]
    result = planned(state)
    gap, = find(result, "EVIDENCE", field="scenarios", option_id="live", scenario_id="busy")
    assert gap["action"] == "VERIFY"
    assert not find(result, "EVIDENCE", field="scenarios", option_id="private")
    assert not find(result, "EVIDENCE", field="scenarios", option_id="online")


def test_timing_asks_for_wait_duration_after_confirming_comparison_horizon():
    state = decision()
    state["question"] = "是否先等课程反馈再报名？"
    state["timing"] = {
        "confirmed": True,
        "time_unit": "天",
        "time_origin": "当前日期",
        "horizon": {"at": 7, "inclusive": True, "kind": "synthetic", "source": "虚构周末观察期限"},
        "decision_deadline": {"at": 3, "inclusive": False, "kind": "synthetic", "source": "虚构报名期限"},
    }
    result = planned(state)
    assert find(result, "TIMING", field="timing", part="wait_duration")
    assert not find(result, "TIMING", field="timing", part="horizon")
    assert not find(result, "TIMING", field="timing", part="decision_deadline")


def test_expired_wait_strategy_prompts_comparison_without_reasking_confirmed_times():
    state = decision()
    state["timing"] = {
        "confirmed": True,
        "time_unit": "天",
        "time_origin": "当前日期",
        "horizon": {"at": 7, "inclusive": True, "kind": "synthetic", "source": "虚构周末观察期限"},
        "wait_duration": quantity(4, unit="天"),
    }
    result = planned(state, {
        "methods": [{"model_id": "timing_actions", "title": "时机", "status": "EXECUTED",
                     "result": {"strategies": [{"type": "wait", "status": "EXPIRED", "option_id": "live"}]}}],
    })
    gap, = find(result, "TIMING", field="timing")
    assert gap["action"] == "COMPARE"
    assert {"stage": "TIMING", "status": "READY"} in result["steps"]


def test_provisional_domain_hint_does_not_fill_user_intent_or_ask_for_confirmed_fields():
    result = planned({"question": "How do I choose an evening course?", "intent": "study with friends"}, {})
    assert result["intent"]["description"] is None
    assert {"LEARNING"} == {hint["domain"] for hint in result["intent"]["hints"]}
    assert all(hint["evidence_status"] == "PROVISIONAL_HINT" for hint in result["intent"]["hints"])
    state = decision()
    state["intent"] = "以先修需求为条件选择课程"
    also = planned(DecisionState.model_validate({key: value for key, value in state.items() if key != "intent"}), analyze(state))
    assert not find(also, "CLARIFICATION", field="intent")
    assert planned(state)["intent"]["description"] == state["intent"]


def test_information_opened_explicitly_gets_a_next_step_without_lexical_cues():
    state = decision()
    state["information"] = {"signals": [], "prior": {}, "likelihoods": {}}
    assert find(planned(state), "EVIDENCE", field="information", part="signals")


def test_timed_joint_evidence_does_not_require_separate_prior_or_likelihood():
    state = decision()
    state["question"] = "是否先调查课程反馈再决定何时报名？"
    state["information"] = {"signals": [{"id": "positive"}, {"id": "negative"}]}
    state["timing"] = {"investigation": {"mode": "joint"}}
    assert not find(planned(state), "EVIDENCE", field="information")


def test_information_policy_disagreement_is_preserved_without_selecting_one():
    state = decision()
    result = planned(state, {"methods": [
        {"model_id": "voi_oracle_bounds", "title": "可重优化", "status": "EXECUTED",
         "result": {"decision": "POSITIVE"}},
        {"model_id": "voi_fixed_policy", "title": "预先承诺", "status": "EXECUTED",
         "result": {"decision": "NEGATIVE"}},
    ]})
    gap, = find(result, "MODEL_ASSUMPTIONS", field="information")
    assert gap["action"] == "COMPARE"
    assert gap["proof"]["model_ids"] == ["voi_oracle_bounds", "voi_fixed_policy"]
    assert "decision" not in result


def test_pareto_tradeoff_asks_about_priorities_without_imputing_weights():
    state = decision()
    state["options"][0]["measurements"]["cost"] = quantity(75)
    state["objectives"].append({"id": "quality", "label": "教学质量", "unit": "分", "direction": "max"})
    state["options"][0]["scores"] = {"access": quantity(6, unit="分"), "quality": quantity(8, unit="分")}
    state["options"][1]["scores"]["quality"] = quantity(6, unit="分")
    result = planned(state)
    gap, = find(result, "SENSITIVITY", field="weights")
    assert gap["action"] == "ASK"
    assert state.get("weights") is None


def test_hard_deadline_alone_does_not_seem_to_be_a_wait_request():
    state = decision()
    state["question"] = "报名星期五截止，我该选现场课程还是线上课？"
    state["timing"] = {
        "confirmed": True,
        "time_unit": "天",
        "time_origin": "星期一",
        "horizon": {"at": 7, "inclusive": True, "kind": "synthetic", "source": "虚构观察期限"},
        "decision_deadline": {"at": 4, "inclusive": False, "kind": "synthetic", "source": "虚构报名截止"},
    }
    assert not find(planned(state), "TIMING", field="timing", part="wait_duration")


def test_prediction_that_straddles_action_cutoff_is_prioritized_as_uncertain():
    state = decision()
    state["timing"] = {
        "confirmed": True,
        "time_unit": "天",
        "time_origin": "星期一",
        "horizon": {"at": 7, "inclusive": True, "kind": "synthetic", "source": "虚构观察期限"},
    }
    result = planned(state, {
        "methods": [{"model_id": "timing_actions", "title": "时机", "status": "EXECUTED",
                     "result": {"strategies": [], "time_inputs": {"prediction_vs_action_cutoffs": {"live": "STRADDLES"}}}}],
    })
    gap, = find(result, "TIMING", field="timing", part="predicted_completion", option_id="live")
    assert (gap["priority"], gap["action"]) == ("HIGH", "VERIFY")
    assert gap["proof"]["relation"] == "STRADDLES"
