from datetime import date
from itertools import product

import pytest


DAY = date(2026, 11, 25)


def evaluate(payload, *, today=DAY):
    from psychohistory import decision_resources

    state = decision_resources.ResourceState.model_validate({"as_of": DAY.isoformat(), **payload})
    return decision_resources.evaluate_resources(state, current_date=today)


def entry(identity, kind, amount, day, **link):
    return {"id": identity, "kind": kind, "amount": amount, "date": day, "source": "Fictional self-report", **link}


def test_paid_amount_and_settled_refund_each_count_once():
    paid = entry("training", "actual_expense", "60.20", "2026-11-24")
    refund = entry("refund", "actual_refund", "10.10", "2026-11-25", refund_of="training")
    forecast = entry("salary", "estimated_income", "10000", "2026-11-26")
    options = [{"option_id": "a", "future_cost": "40.00"},
               {"option_id": "b", "future_cost": "40.01"}]
    result = evaluate({"cash": {"currency": "CNY", "opening_balance": "100.10", "opening_date": "2026-11-24",
        "covered_through": "2026-11-25", "events": [paid, refund, forecast]}, "reserve": "10.00", "options": options})
    assert result["cash"]["balance"] == "50.00"
    assert result["options"]["a"]["cash"]["margin"] == "0.00"
    assert result["options"]["a"]["status"] == "FEASIBLE"
    assert result["options"]["b"]["status"] == "INFEASIBLE"
    assert [event["id"] for event in result["cash"]["estimates"]] == ["salary"]
    same_cash = evaluate({"cash": {"currency": "CNY", "opening_balance": "50.00",
        "balance_includes_through": "2026-11-25", "events": [paid, refund]}, "reserve": "10.00", "options": options})
    assert same_cash["cash"]["balance"] == "50.00"
    assert same_cash["options"] == result["options"]


def test_missing_coverage_or_stale_balance_keeps_cash_unknown():
    cash = {"currency": "USD", "opening_balance": "30", "opening_date": "2026-11-24",
        "events": [entry("salary", "estimated_income", "50", "2026-11-25")]}
    options = [{"option_id": "a", "future_cost": "0"}]
    assert evaluate({"cash": cash, "options": options})["options"]["a"]["status"] == "UNKNOWN"
    assert evaluate({"cash": {**cash, "covered_through": "2026-11-25"}, "options": options},
                    today=date(2026, 11, 26))["options"]["a"]["status"] == "UNKNOWN"


@pytest.mark.parametrize("events", [
    [entry("x", "actual_income", "10", "2026-11-25"), entry("x", "actual_income", "20", "2026-11-25")],
    [entry("x", "actual_refund", "10", "2026-11-25", refund_of="missing")],
    [entry("x", "actual_expense", "4", "2026-11-25"), entry("y", "actual_refund", "5", "2026-11-25", refund_of="x")],
    [entry("x", "actual_income", "10", "2026-11-26")],
    [entry("x", "actual_income", 0.1, "2026-11-25")],
])
def test_inconsistent_actual_entries_cannot_change_spendable_cash(events):
    with pytest.raises(ValueError):
        evaluate({"cash": {"currency": "USD", "opening_balance": "30", "opening_date": "2026-11-24",
                           "covered_through": "2026-11-25", "events": events}})


def task(identity, *, total, progress, deadline, **rest):
    return {"id": identity, "label": identity, "total_minutes": total, "completed_minutes": progress,
            "deadline": deadline, "mode": "splittable", **rest}


def test_shared_deadline_and_progress_use_only_upcoming_capacity():
    capacity = [{"date": "2026-11-24", "minutes": 120}, {"date": "2026-11-25", "minutes": 60},
                {"date": "2026-11-26", "minutes": 60}]
    old = task("old", total=120, progress=60, deadline="2026-11-25", prior_plan_id="plan-old")
    new = task("new", total=60, progress=0, deadline="2026-11-25")
    base = {"capacity": capacity, "shared_tasks": [old], "options": [{"option_id": "a", "tasks": [new]},
                                                                    {"option_id": "b", "tasks": []}]}
    result = evaluate(base)
    assert result["options"]["a"]["status"] == "INFEASIBLE"
    assert result["options"]["b"]["status"] == "FEASIBLE"
    assert result["options"]["b"]["time"]["schedule"] == [{"date": "2026-11-25", "task_id": "old", "minutes": 60}]
    shifted = evaluate({**base, "shared_tasks": [{**old, "deadline": "2026-11-26"}]})
    assert shifted["options"]["a"]["status"] == "FEASIBLE"
    progressed = evaluate({**base, "shared_tasks": [{**old, "completed_minutes": 120}]})
    assert progressed["options"]["a"]["status"] == "FEASIBLE"
    late = evaluate(base, today=date(2026, 11, 26))
    assert late["options"]["b"]["status"] == "INFEASIBLE"


def test_unknown_time_and_fragmented_continuous_tasks_cannot_pass():
    new = task("new", total=120, progress=0, deadline="2026-11-26")
    capacity = [{"date": "2026-11-25", "minutes": 60}, {"date": "2026-11-26", "minutes": 60}]
    options = [{"option_id": "a", "tasks": [{**new, "mode": "continuous"}]},
               {"option_id": "b", "tasks": [{**new, "completed_minutes": None}]},
               {"option_id": "c"}]
    result = evaluate({"capacity": capacity, "options": options})
    assert [row["status"] for row in result["options"].values()] == ["UNKNOWN", "UNKNOWN", "UNKNOWN"]
    assert evaluate({"capacity": capacity[:1], "options": [{"option_id": "a", "tasks": [new]}]})[
        "options"]["a"]["status"] == "UNKNOWN"
    assert evaluate({"capacity": capacity[:1] + [{"date": "2026-11-26", "minutes": 0}],
                     "options": options})["options"]["a"]["status"] == "INFEASIBLE"


def test_splittable_schedule_matches_direct_unit_allocation():
    days = ["2026-11-25", "2026-11-26", "2026-11-27"]
    for counts in product((0, 1), repeat=3):
        capacity = [{"date": day, "minutes": count} for day, count in zip(days, counts)]
        available = [index for index, count in enumerate(counts) if count]
        for a_total, b_total, a_due, b_release in product((1, 2), (1, 2), (0, 1, 2), (0, 1, 2)):
            tasks = [task("a", total=a_total, progress=0, deadline=days[a_due]),
                     task("b", total=b_total, progress=0, deadline=days[2], release=days[b_release])]

            def works(allocation):
                a_days = [i for i, task_id in zip(available, allocation) if task_id == "a"]
                b_days = [i for i, task_id in zip(available, allocation) if task_id == "b"]
                return len(a_days) == a_total and len(b_days) == b_total and all(i <= a_due for i in a_days) and all(
                    i >= b_release for i in b_days)

            possible = any(works(allocation) for allocation in product(("a", "b", None), repeat=len(available)))
            result = evaluate({"capacity": capacity, "options": [{"option_id": "a", "tasks": tasks}]})
            assert result["options"]["a"]["status"] == ("FEASIBLE" if possible else "INFEASIBLE")


def test_unstructured_limits_cannot_silently_pass_resource_screening():
    options = [{"option_id": "a", "tasks": []}]
    result = evaluate({"options": options, "limits": ["Night work is prohibited"], "goals": ["Study more"]})
    assert result["options"]["a"]["status"] == "UNKNOWN"
    assert result["unapplied_limits"] == ["Night work is prohibited"]
