from decimal import Decimal
from fractions import Fraction
from importlib import import_module

import pytest

from psychohistory.decision_hub import valid_result
from psychohistory.decision_registry import Context
from psychohistory.decision_state import Option, Quantity, Scenario
from psychohistory.decision_v05 import DecisionStateV05, v05_registry
from psychohistory.decision_voi import InformationInput


def timed(value, upper=None):
    return {"lower": value, "upper": value if upper is None else upper, "kind": "synthetic", "source": "合成边界"}


def cutoff(at, inclusive=True):
    return {"at": at, "inclusive": inclusive, "kind": "synthetic", "source": "合成期限"}


def ctx(timing=None, *, investigate=None, information=None, accepted=("a", "b"), rules=None):
    options = [Option(id="a", label="方案甲"), Option(id="b", label="方案乙")]
    scenarios = [
        Scenario(
            id=scenario, label=scenario, kind="synthetic", source="合成效用",
            utilities={key: Quantity(**timed(value), unit="效用") for key, value in utility.items()},
        )
        for scenario, utility in (("good", {"a": 6, "b": 10}), ("bad", {"a": 6, "b": 0}))
    ]
    actions = {
        key: {"switching_cost": timed(0), "delay_losses": {"good": timed(rate), "bad": timed(0)}}
        for key, rate in (("a", 0), ("b", 2))
    }
    for key, rule in (rules or {}).items():
        actions[key].update(rule)
    time = {
        "confirmed": True, "time_unit": "天", "time_origin": "确认时刻",
        "horizon": cutoff(2), "actions": actions,
        "investigation": investigate,
    }
    state = DecisionStateV05(
        decision_id="0" * 32, revision=1, question="选择", deadline="两天内",
        scenario_basis="共用时间范围和效用量尺，越大越好",
        options=options, scenarios=scenarios, timing=time | (timing or {}),
        information=information, confirmed=True, constraints_confirmed=True,
    )
    return Context(state, tuple(option for option in options if option.id in accepted))


def info():
    return InformationInput(
        signals=[{"id": key, "label": key} for key in ("plus", "minus")],
        prior={"good": timed(".5"), "bad": timed(".5")},
        likelihoods={
            "good": {"plus": timed(".9"), "minus": timed(".1")},
            "bad": {"plus": timed(".3"), "minus": timed(".7")},
        },
        actions_by_signal={},
        unrestricted_actions=True,
        action_source="合成例可从仍在期限内的行动中选择",
    )


def investigation(mode, **changes):
    return {
        "mode": mode, "kind": "synthetic", "source": "有限合成分布及依赖机制",
        "cost": timed(".5"), **changes,
    }


def run(context, method_id):
    method = v05_registry().get(method_id, "1.0.0")
    assert method.validate(context) == []
    return valid_result(method.execute(context), context)


def direct_rows(*durations):
    rows = []
    for time, share in durations:
        for scenario, signal, probability in (
            ("good", "plus", ".45"), ("bad", "plus", ".15"),
            ("good", "minus", ".05"), ("bad", "minus", ".35"),
        ):
            rows.append({
                "scenario_id": scenario, "signal_id": signal, "duration": time,
                "probability": str(Decimal(probability) * Decimal(share)),
            })
    return rows


def test_action_and_wait_compare_scenarios_without_inventing_probabilities():
    result = run(ctx({"wait_duration": timed(".5"), "status_quo_option_id": "a"}), "timing_actions")
    strategies = {(r["type"], r["option_id"]): r for r in result["strategies"]}
    assert strategies["status_quo", "a"]["utilities"] == {"good": "6", "bad": "6"}
    assert strategies["wait", "b"]["utilities"] == {"good": "9", "bad": "0"}
    assert result["probabilities_used"] is False
    first_chart, second_chart = result["charts"]
    assert first_chart["unit"] == second_chart["unit"] == "效用"
    assert [row["lower"] for row in first_chart["rows"]] == ["6", "6", "10", "9"]
    assert [row["lower"] for row in second_chart["rows"]] == ["6", "6", "0", "0"]
    assert all(row["lower"] == row["upper"] for chart in result["charts"] for row in chart["rows"])


def test_status_quo_labels_leave_switching_cost_and_numeric_utilities_intact():
    rules = {"b": {"switching_cost": timed(5)}}
    first = run(ctx({"status_quo_option_id": "a"}, rules=rules), "timing_actions")
    second = run(ctx({"status_quo_option_id": "b"}, rules=rules), "timing_actions")
    assert {row["option_id"]: row["utilities"] for row in first["strategies"]} == {
        row["option_id"]: row["utilities"] for row in second["strategies"]
    } == {"a": {"good": "6", "bad": "6"}, "b": {"good": "5", "bad": "-5"}}
    assert first["leaders"] == second["leaders"] == ["a"]


def test_time_prediction_goal_and_deadline_stay_separate():
    result = run(ctx({
        "desired_time": timed(".2"),
        "predicted_completion": timed(".3", ".8"),
        "decision_deadline": cutoff(".5"),
    }), "timing_actions")
    times = result["time_inputs"]
    assert times["desired_time"]["lower"] == "0.2"
    assert times["predicted_completion"]["upper"] == "0.8"
    assert times["decision_deadline"]["at"] == "0.5"
    assert times["prediction_vs_deadline"] == "STRADDLES"
    assert "actual_completion" not in times


@pytest.mark.parametrize(("inclusive", "expected"), [(True, "FEASIBLE"), (False, "EXPIRED")])
def test_action_cutoff_is_checked_on_exact_equality(inclusive, expected):
    result = run(
        ctx({"wait_duration": timed(".5")}, rules={"b": {"cutoff": cutoff(".5", inclusive)}}),
        "timing_actions",
    )
    assert next(row for row in result["strategies"] if row["type"] == "wait" and row["option_id"] == "b")[
        "status"
    ] == expected


def test_global_analysis_horizon_checks_exact_equality_independently_of_action_cutoffs():
    result = run(ctx({"horizon": cutoff(".5", False), "wait_duration": timed(".5")}), "timing_actions")
    assert {row["status"] for row in result["strategies"] if row["type"] == "wait"} == {"EXPIRED"}


def test_immediate_availability_requires_confirmed_time_basis_and_obeys_zero_cutoff():
    check = import_module("psychohistory.decision_timing").immediate_availability
    timing = ctx(rules={"b": {"cutoff": cutoff(0, False)}}).state.timing
    assert check(timing, "b") == "EXPIRED"
    assert check(timing, "a") == "FEASIBLE"
    assert check(timing.model_copy(update={"confirmed": False}), "a") == "UNKNOWN"
    assert check(timing.model_copy(update={"time_origin": None}), "a") == "UNKNOWN"
    assert check(None, "a") == "UNKNOWN"


def test_deterministic_opportunity_loss_has_exact_break_even():
    result = run(
        ctx(investigate=investigation("deterministic", duration=timed(".25")), information=info()),
        "timing_investigation",
    )
    assert result["immediate_value"] == "6"
    assert result["net_value"] == "0.175"
    assert result["status"] == "INVESTIGATE"
    assert result["threshold"] == {"at": "4/9", "profitable_at_boundary": False, "unit": "天"}
    assert {row["signal_id"]: row["option_ids"] for row in result["policy"]} == {
        "plus": ["b"], "minus": ["a"],
    }


def test_exact_value_tie_is_not_promoted_to_strict_investigation():
    payload = investigation("deterministic", duration=timed(".5")) | {"cost": timed(".45")}
    result = run(ctx(investigate=payload, information=info()), "timing_investigation")
    assert result["net_value"] == "0"
    assert result["status"] == "TIE"
    assert result["leaders"] == []
    assert result["threshold"] == {"at": "0.5", "profitable_at_boundary": False, "unit": "天"}


def test_investigation_respects_confirmed_signal_scopes():
    information = info().model_copy(update={"unrestricted_actions": False})
    information.actions_by_signal = InformationInput(
        actions_by_signal={
            key: {"option_ids": ["a"], "kind": "synthetic", "source": "信号后仅甲"}
            for key in ("plus", "minus")
        }
    ).actions_by_signal
    result = run(
        ctx(investigate=investigation("deterministic", duration=timed("0")), information=information),
        "timing_investigation",
    )
    assert result["net_value"] == "-0.5"
    assert all(row["availability"]["b"] == "SIGNAL_EXCLUDED" for row in result["policy"])


@pytest.mark.parametrize("patch", [{"unrestricted_actions": False}, {"action_source": ""}])
def test_investigation_cannot_infer_unrestricted_action_scope_from_blank_controls(patch):
    information = info().model_copy(update=patch)
    context = ctx(investigate=investigation("deterministic", duration=timed("0")), information=information)
    method = v05_registry().get("timing_investigation", "1.0.0")
    assert method.validate(context)


def test_fact_label_does_not_override_synthetic_probability_inputs():
    payload = investigation("deterministic", duration=timed(".25")) | {
        "kind": "fact", "source": "已核对调查存在",
    }
    result = run(ctx(investigate=payload, information=info()), "timing_investigation")
    assert result["probability_provenance"]["kind"] == "synthetic"
    assert {row["kind"] for row in result["probability_provenance"]["inputs"]} == {"fact", "synthetic"}


def test_strict_opportunity_window_can_reverse_the_card_at_the_cutoff():
    result = run(
        ctx(investigate=investigation("deterministic", duration=timed(".3")), information=info(),
            rules={"b": {"cutoff": cutoff(".3", False)}}),
        "timing_investigation",
    )
    assert result["net_value"] == "-0.5"
    assert result["threshold"] == {"at": "0.3", "profitable_at_boundary": False, "unit": "天"}
    assert all(row["eligible_option_ids"] == ["a"] for row in result["policy"])


@pytest.mark.parametrize(("has_deadline", "net", "bound"), [(False, "0.175", "8/9"), (True, "-0.05", "4/9")])
def test_random_completion_does_not_replace_times_with_their_mean(has_deadline, net, bound):
    result = run(
        ctx(investigate=investigation("joint", joint=direct_rows(("0", ".5"), (".5", ".5"))),
            rules={"b": {"cutoff": cutoff(".3", False)}} if has_deadline else {}),
        "timing_investigation",
    )
    assert result["net_value"] == net
    assert len(result["policy"]) == 4
    assert result["late_mass_sensitivity"] == {
        "early_duration": "0", "late_duration": "0.5",
        "profitable_range": {"lower": "0", "upper": bound, "lower_inclusive": True, "upper_inclusive": False},
    }


@pytest.mark.parametrize(
    ("early_good", "early_bad", "net"),
    [(".8", ".2", "0.76"), (".2", ".8", "-0.5"), (".5", ".5", "-0.05")],
)
def test_same_completion_marginals_can_reverse_when_time_depends_on_state(early_good, early_bad, net):
    distribution = {
        scenario: [{"duration": "0", "probability": share}, {
            "duration": ".5", "probability": str(1 - Decimal(share)),
        }]
        for scenario, share in (("good", early_good), ("bad", early_bad))
    }
    result = run(
        ctx(investigate=investigation("conditional", completion_by_state=distribution),
            information=info(), rules={"b": {"cutoff": cutoff(".3", False)}}),
        "timing_investigation",
    )
    assert result["duration_probabilities"] == {"0": "0.5", "0.5": "0.5"}
    assert result["net_value"] == net


def test_positive_mass_without_an_explicit_accepted_exit_keeps_net_value_unknown():
    result = run(
        ctx(
            {"fallback_option_id": "a"}, accepted=("b",),
            investigate=investigation("joint", joint=direct_rows((".5", "1"))),
            rules={"b": {"cutoff": cutoff(".5", False)}},
        ),
        "timing_investigation",
    )
    assert result["status"] == "UNKNOWN"
    assert result["net_value"] is None
    assert all(not row["eligible_option_ids"] for row in result["policy"])
    assert "a" not in result.get("leaders", [])


def test_an_explicit_accepted_fallback_uses_its_actual_negative_payoff():
    result = run(
        ctx(
            {"fallback_option_id": "a"}, investigate=investigation("joint", joint=direct_rows((".5", "1"))),
            rules={"a": {"switching_cost": timed("7")}, "b": {"cutoff": cutoff(".5", False)}},
        ),
        "timing_investigation",
    )
    assert result["immediate_value"] == "5"
    assert result["investigation_value"] == "-1.5"
    assert result["net_value"] == "-6.5"
    assert all(row["fallback_selected"] for row in result["policy"])


def test_unsupported_joint_probability_renders_ineligible():
    known = ctx(investigate=investigation("joint", joint=direct_rows(("0", "1"))))
    model = known.state.timing.investigation
    for kind, source in (("assumption", model.source), ("synthetic", "")):
        model.kind, model.source = kind, source
        method = import_module("psychohistory.decision_timing").METHODS[1]
        assert method.validate(known)


def test_zero_mass_late_outcome_does_not_require_a_fallback():
    result = run(
        ctx(
            {"decision_deadline": cutoff(".4")},
            investigate=investigation("joint", joint=direct_rows(("0", "1"), (".5", "0"))),
        ),
        "timing_investigation",
    )
    assert result["net_value"] == "0.4"
    assert {row["duration"] for row in result["policy"]} == {"0"}


def test_expired_actions_do_not_set_the_payoff_unit_for_remaining_actions():
    context = ctx(
        investigate=investigation("joint", joint=direct_rows((".5", "1"))),
        rules={"a": {"cutoff": cutoff(0, False)}},
    )
    for scenario in context.state.scenarios:
        scenario.utilities["a"].unit = "不可比单位"
    actions = run(context, "timing_actions")
    assert actions["leaders"] == ["b"]
    investigation_result = run(context, "timing_investigation")
    assert investigation_result["net_value"] == "-1"
    assert investigation_result["immediate_availability"]["a"] == "EXPIRED"


def test_impossible_state_utility_is_not_required_for_probability_weighted_plan():
    context = ctx(investigate=investigation("joint", joint=[
        {"scenario_id": "good", "signal_id": "plus", "duration": ".5", "probability": 1},
    ]))
    bad = next(scenario for scenario in context.state.scenarios if scenario.id == "bad")
    bad.utilities["a"].unit = "不可比单位"
    result = run(context, "timing_investigation")
    assert result["net_value"] == "-1.5"
    assert result["scenario_probabilities"] == {"good": "1"}


def test_missing_joint_evidence_keeps_investigation_unknown_even_if_durations_are_known():
    context = ctx(
        investigate=investigation("conditional", completion_by_state={"good": [{"duration": 0, "probability": 1}]}),
        information=info(),
    )
    method = import_module("psychohistory.decision_timing").METHODS[1]
    assert method.validate(context)


def test_random_joint_reference_enumerates_fixed_observation_policies():
    rows = [
        {"scenario_id": "good", "signal_id": "plus", "duration": ".2", "probability": ".38"},
        {"scenario_id": "bad", "signal_id": "plus", "duration": ".2", "probability": ".1"},
        {"scenario_id": "good", "signal_id": "minus", "duration": ".8", "probability": ".07"},
        {"scenario_id": "bad", "signal_id": "minus", "duration": ".8", "probability": ".45"},
    ]
    result = run(
        ctx(rules={"b": {"cutoff": cutoff(".8", False)}},
            investigate=investigation("joint", joint=rows)),
        "timing_investigation",
    )
    # There are only two feasible deterministic policies: choose A or B on the
    # first observation and A on the second. Their gross values use raw event rows.
    baseline = max(Fraction(6), Fraction(".45") * 10)
    payoffs = [Fraction(6), Fraction(".38") * Fraction("9.6") + Fraction(".52") * 6]
    assert Fraction(result["net_value"]) == max(payoffs) - Fraction(".5") - baseline
