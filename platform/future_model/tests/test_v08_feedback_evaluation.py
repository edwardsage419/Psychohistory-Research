from datetime import UTC, datetime, timedelta

import pytest

from psychohistory import decision_feedback as feedback


START = datetime(2026, 11, 26, tzinfo=UTC)
OUTCOME = START + timedelta(days=1)


def setup_lab(*, adjustment="2"):
    clock = [START]
    lab = feedback.FeedbackLab(clock=lambda: clock[0])
    plan = feedback.FeedbackFreezeInput.model_validate({
        "confirmed": True, "dataset_kind": "SYNTHETIC",
        "candidate_version": "candidate-1", "current_version": "current-1", "baseline_version": "baseline-1",
        "scope": "delivery-cost", "unit": "CNY", "adjustment": adjustment,
        "development_ids": ["old"],
        "cases": [
            {"id": "x", "current": "10", "baseline": "9", "not_before": OUTCOME},
            {"id": "y", "current": "10", "baseline": "9", "not_before": OUTCOME},
        ],
    })
    return lab, plan, clock


def observe(lab, token, case_id, value, *, upper=None, revision=1, kind="OBSERVED"):
    return lab.observe(token, feedback.FeedbackObservation.model_validate({
        "case_id": case_id, "kind": kind, "observed_at": OUTCOME, "revision": revision,
        "lower": value, "upper": value if upper is None else upper,
    }))


def test_feedback_compares_frozen_predictions_on_all_predeclared_cases():
    lab, plan, clock = setup_lab()
    token = lab.freeze(plan)["token"]
    clock[0] = OUTCOME
    observe(lab, token, "x", "14")
    assert lab.evaluate(token)["status"] == "UNKNOWN_INCOMPLETE_OUTCOMES"
    observe(lab, token, "y", "12", upper="15")
    result = lab.evaluate(token)
    assert result["status"] == "FINITE_GATE_MET"
    assert result["authority"] == "NONE"
    assert result["admission"] == "NOT_ADMITTED"
    assert result["absolute_gain_vs_current"] == ["4.00","4.00"]
    assert result["absolute_gain_vs_baseline"] == ["6.00","6.00"]


def test_evaluation_uses_underestimation_gate_and_keeps_old_tokens_inactive():
    lab, plan, clock = setup_lab(adjustment="-2")
    token = lab.freeze(plan)["token"]
    clock[0] = OUTCOME
    observe(lab, token, "x", "8")
    observe(lab, token, "y", "9")
    result = lab.evaluate(token)
    assert result["status"] == "FINITE_GATE_NOT_MET"
    assert result["underestimate_gain_vs_current"] == ["-1.00","-1.00"]
    assert lab.rollback(token)["status"] == "DISCARDED"
    with pytest.raises(PermissionError):
        lab.evaluate(token)


def test_feedback_refuses_future_data_revision_gaps_and_development_overlap():
    lab, plan, clock = setup_lab()
    with pytest.raises(ValueError):
        lab.freeze(plan.model_copy(update={"development_ids": ["x"]}))
    token = lab.freeze(plan)["token"]
    with pytest.raises(ValueError):
        observe(lab, token, "x", "12")
    clock[0] = OUTCOME
    with pytest.raises(ValueError):
        observe(lab, token, "x", "12", revision=2)
    observe(lab, token, "x", "12")
    assert observe(lab, token, "x", "12")["status"] == "UNCHANGED"
    observe(lab, token, "x", "11", revision=2)
    assert lab.evaluate(token)["missing_ids"] == ["y"]


def test_counterfactual_ever_remains_unobserved():
    lab, plan, clock = setup_lab()
    token = lab.freeze(plan)["token"]
    clock[0] = OUTCOME
    observe(lab, token, "x", "14")
    observe(lab, token, "y", None, kind="UNOBSERVED")
    result = lab.evaluate(token)
    assert result["status"] == "UNKNOWN_INCOMPLETE_OUTCOMES"
    assert result["missing_ids"] == ["y"]
    assert "absolute_gain_vs_current" not in result


def test_target_transfer_shrinks_only_under_declared_compatible_support():
    lab, plan, _ = setup_lab()
    token = lab.freeze(plan)["token"]
    request = feedback.FeedbackTransferInput.model_validate({
        "confirmed": True, "target_scope": "delivery-cost-local", "unit": "CNY",
        "support_version": "target-support-1", "reference_lower": "1", "reference_upper": "4",
        "offset_lower": "0", "offset_upper": "1", "scale": 1,
    })
    result = lab.transfer(token, request)
    assert result["authority"] == "NONE"
    assert result["status"] == "CONDITIONAL_RESEARCH_CANDIDATE"
    assert result["target_support"] == ["1.00", "5.00"]
    assert result["adjustment"] == "1.00"
    mismatch = lab.transfer(token, request.model_copy(update={"unit": "minutes"}))
    assert mismatch["status"] == "UNKNOWN_TRANSFER"
    assert "adjustment" not in mismatch
    cross_zero = lab.transfer(token, request.model_copy(update={"offset_lower": feedback.Decimal("-2")}))
    assert cross_zero["adjustment"] == "0.00"


def test_feedback_evaluation_is_local_and_rollback_revokes_old_token(tmp_path):
    from fastapi.testclient import TestClient
    from psychohistory.api import create_app

    _, plan, _ = setup_lab()
    next_day = datetime.now(UTC) + timedelta(days=1)
    for case in plan.cases:
        case.not_before = next_day
    local_token = "local-test-token"
    prefix = "/api/v8/decisions/feedback/"
    with TestClient(create_app(tmp_path, tmp_path, token=local_token)) as client:
        request = plan.model_dump(mode="json")
        assert client.post(prefix + "freeze", json=request).status_code == 401
        headers = {"Authorization": f"Bearer {local_token}"}
        frozen = client.post(prefix + "freeze", json=request, headers=headers)
        assert frozen.status_code == 200, frozen.text
        token = {"token": frozen.json()["token"]}
        current = client.post(prefix + "evaluate", json=token, headers=headers)
        assert current.status_code == 200, current.text
        assert current.json()["status"] == "UNKNOWN_INCOMPLETE_OUTCOMES"
        assert client.post(prefix + "rollback", json=token, headers=headers).status_code == 200
        assert client.post(prefix + "evaluate", json=token, headers=headers).status_code == 403
