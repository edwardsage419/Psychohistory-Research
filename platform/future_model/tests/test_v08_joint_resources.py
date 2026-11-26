from datetime import date, timedelta

from psychohistory import decision_resources as resources


TODAY = date(2026, 11, 26)


def snapshot(*, event_kind="actual_expense"):
    task = {"id":"setup","label":"Setup","total_minutes":40,"completed_minutes":0,
            "deadline":TODAY.isoformat(),"mode":"splittable","source":"confirmed setup"}
    return resources.ResourceState.model_validate({
        "as_of": TODAY, "reserve": "20", "capacity": [{"date": TODAY, "minutes": 60}],
        "cash": {"currency":"CNY","opening_balance":"120","opening_date":TODAY,"covered_through":TODAY,
                 "events":[{"id":"payment","kind":event_kind,"amount":"20","date":TODAY,"source":"checked ledger"},
                           {"id":"forecast","kind":"estimated_income","amount":"90","date":TODAY,"source":"forecast"}]},
        "options":[{"option_id":"first","future_cost":"60","tasks":[task]},
                   {"option_id":"second","future_cost":"60","tasks":[task]}],
    })


def query(*, same=True, paid=True, shared=True):
    first = [{"id":"common","amount":"60","due":TODAY}]
    second = [{"id":"common" if same else "independent","amount":"60","due":TODAY}]
    if paid:
        first.append({"id":"paid","amount":"20","due":TODAY,"reflected_payment_id":"payment"})
    return resources.JointResourceInput.model_validate({
        "option_ids":["first","second"],"confirmed":True,
        "shared_task_ids":["setup"] if shared else [],
        "cash_allocations":{"first":first,"second":second},
    })


def test_shared_confirmed_identity_is_charged_once_and_forecast_is_excluded():
    result = resources.evaluate_joint_resources(snapshot(), query(), current_date=TODAY)
    assert result["authority"] == "NONE"
    assert result["cash"]["balance"] == "100.00"
    assert result["cash"]["future_cost"] == "60.00"
    assert result["cash"]["margin"] == "20.00"
    assert result["status"] == "FEASIBLE"
    assert result["time"]["schedule"] == [{"date":TODAY.isoformat(),"task_id":"setup","minutes":40}]


def test_equal_amount_different_identity_uses_cash_twice():
    result = resources.evaluate_joint_resources(snapshot(), query(same=False), current_date=TODAY)
    assert result["status"] == "INFEASIBLE"
    assert result["cash"]["margin"] == "-40.00"


def test_estimated_cash_cannot_certify_a_reflected_payment():
    result = resources.evaluate_joint_resources(snapshot(event_kind="estimated_income"), query(), current_date=TODAY)
    assert result["cash"]["status"] == "UNKNOWN"
    assert result["cash"]["reason"] == "PAYMENT_RECONCILIATION_REQUIRED"


def test_uncorroborated_shared_task_identity_remains_unresolved():
    result = resources.evaluate_joint_resources(snapshot(), query(shared=False), current_date=TODAY)
    assert result["time"]["status"] == "UNKNOWN"
    assert result["status"] == "UNKNOWN"


def test_revision_conflict_cannot_fall_back_to_same_old_obligation():
    state = snapshot()
    state.options[1].future_cost = resources.Decimal("70")
    request = query()
    request.cash_allocations["second"][0].amount = resources.Decimal("70")
    result = resources.evaluate_joint_resources(state, request, current_date=TODAY)
    assert result["cash"]["status"] == "CONFLICT"
    assert result["status"] == "UNKNOWN"


def test_joint_cash_totals_must_match_each_individually_confirmed_plan():
    state = snapshot()
    state.options[1].future_cost = resources.Decimal("61")
    result = resources.evaluate_joint_resources(state, query(), current_date=TODAY)
    assert result["cash"]["reason"] == "ALLOCATION_COVERAGE_REQUIRED"
    assert result["status"] == "UNKNOWN"


def test_recurring_benefit_is_a_condition_and_starts_after_the_fixed_plan():
    request = resources.RecurringBenefitInput.model_validate({
        "confirmed": True, "horizon": 4, "fixed_period": 1, "fixed_cost": "20",
        "benefit_delay": 1, "base_income": "0", "quantum": "1",
        "goals": [{"id": "first", "cost": "40", "deadline": 2},
                  {"id": "second", "cost": "60", "deadline": 3}],
    })
    result = resources.evaluate_recurring_benefit(snapshot(), request, current_date=TODAY)
    assert result["authority"] == "NONE"
    assert result["status"] == "CONDITIONAL"
    assert result["minimum_per_period"] == "20.00"
    assert result["witness_dates"] == [{"first": "2026-11-28", "second": "2026-11-29"}]
    later = request.model_copy(update={"benefit_delay": 2})
    assert resources.evaluate_recurring_benefit(snapshot(), later, current_date=TODAY)["minimum_per_period"] == "40.00"
    too_late = request.model_copy(update={"benefit_delay": 3})
    assert resources.evaluate_recurring_benefit(snapshot(), too_late, current_date=TODAY)["status"] == "NO_FINITE_THRESHOLD"


def test_soft_deadline_extension_keeps_marginal_dates_separate_from_joint_feasibility():
    request = resources.GoalDeadlineInput.model_validate({
        "confirmed": True, "horizon": 4, "fixed_period": 1, "fixed_cost": "20",
        "base_income": "0",
        "goals": [{"id": "first", "cost": "20", "deadline": 2, "hard_deadline": False},
                  {"id": "second", "cost": "20", "deadline": 2, "hard_deadline": False}],
    })
    result = resources.evaluate_goal_deadlines(snapshot(), request, current_date=TODAY)
    assert result["authority"] == "NONE"
    assert result["without_fixed_plan"]["on_time"] is True
    assert result["with_fixed_plan"]["on_time"] is False
    assert result["with_fixed_plan"]["marginal_earliest"] == {"first": "2026-11-28", "second": "2026-11-28"}
    assert result["with_fixed_plan"]["marginal_earliest_joint"] is False
    assert result["with_fixed_plan"]["extensions"] == [
        {"first": 0, "second": 1}, {"first": 1, "second": 0},
    ]
    hard_goals = tuple(goal.model_copy(update={"hard_deadline": True}) for goal in request.goals)
    hard = request.model_copy(update={"goals": hard_goals})
    assert resources.evaluate_goal_deadlines(snapshot(), hard, current_date=TODAY)["with_fixed_plan"] == {
        "status": "NO_JOINT_COMPLETION_WITHIN_HORIZON",
    }


def test_shifted_resource_snapshot_does_not_certify_joint_time():
    state = snapshot()
    state.cash = None
    state.reserve = None
    for option in state.options:
        option.future_cost = None
        option.tasks[0].deadline = TODAY + timedelta(days=2)
    state.capacity[0].date = TODAY + timedelta(days=2)
    request = query(paid=False).model_copy(update={"cash_allocations": None})
    result = resources.evaluate_joint_resources(state, request, current_date=TODAY + timedelta(days=1))
    assert result["status"] == "UNKNOWN"
    assert result["time"]["reason"] == "CURRENT_TIME_SNAPSHOT_REQUIRED"


def test_a_payment_with_a_refund_needs_obligation_reconciliation():
    state = snapshot()
    state.cash.events.append(resources.CashEvent.model_validate({
        "id": "refund", "kind": "actual_refund", "amount": "20", "date": TODAY,
        "refund_of": "payment", "source": "actual refund",
    }))
    result = resources.evaluate_joint_resources(state, query(), current_date=TODAY)
    assert result["cash"]["reason"] == "PAYMENT_RECONCILIATION_REQUIRED"
    assert result["status"] == "UNKNOWN"


def test_joint_analysis_actual_api_binds_current_instance_and_revision(tmp_path):
    from datetime import UTC, datetime

    from fastapi.testclient import TestClient
    from psychohistory.api import create_app

    today = datetime.now(UTC).date().isoformat()
    token = "local-test-token"
    prefix = "/api/v8/decisions/"
    headers = {"Authorization": f"Bearer {token}"}
    with TestClient(create_app(tmp_path, tmp_path, token=token), headers=headers) as client:
        response = client.post(prefix + "start", json={"question": "我该选『方案甲』，还是『方案乙』？"})
        assert response.status_code == 200
        started = response.json()
        ids = [option["id"] for option in started["options"]]
        assert len(ids) == 2
        session = {key: started[key] for key in ("session_id", "session_instance", "revision")}
        payload = {
            **session, "confirmed": True, "resources": {
                "as_of": today, "reserve": "10", "cash": {
                    "currency": "CNY", "opening_balance": "80", "balance_includes_through": today,
                    "events": [{"id": "forecast", "kind": "estimated_income",
                                "amount": "100", "date": today, "source": "forecast"}],
                },
                "options": [{"option_id": key, "future_cost": "40"} for key in ids],
            },
        }
        updated = client.post(prefix + "update_resources", json=payload)
        assert updated.status_code == 200, updated.text
        request = {
            "confirmed": True, "option_ids": ids,
            "cash_allocations": {key: [{"id": "shared", "amount": "40", "due": today}] for key in ids},
        }
        stale = client.post(prefix + "joint_resources", json={**session, "request": request})
        assert stale.status_code == 422
        session["revision"] = updated.json()["revision"]
        assessed = client.post(prefix + "joint_resources", json={**session, "request": request})
        assert assessed.status_code == 200, assessed.text
        actual = assessed.json()
        assert actual["authority"] == "NONE"
        assert actual["session_instance"] == session["session_instance"]
        assert actual["revision"] == session["revision"]
        assert len(actual["dependency_sha256"]) == 64
        assert actual["analysis"]["cash"]["margin"] == "30.00"
        assert actual["analysis"]["cash"]["balance"] == "80.00"
