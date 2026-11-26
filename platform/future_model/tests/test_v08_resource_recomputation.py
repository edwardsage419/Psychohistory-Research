"""Independent action-string oracle for the pinned public development domains."""

from datetime import date
from itertools import product

from psychohistory.decision_resources import (
    GoalDeadlineInput, RecurringBenefitInput, ResourceState,
    evaluate_goal_deadlines, evaluate_recurring_benefit,
)

TODAY = date(2026, 11, 26)
PATHS = [
    (actions, tuple(actions.index(goal) + 1 for goal in (1, 2)))
    for actions in product(range(3), repeat=4)
    if actions.count(1) == actions.count(2) == 1
]


def snapshot(balance, reserve):
    return ResourceState.model_validate({
        'as_of': TODAY, 'reserve': reserve,
        'cash': {'opening_balance': balance, 'balance_includes_through': TODAY, 'currency': 'USD'},
    })


def direct_paths(balance, reserve, income, a, b, fee, busy, delay, gain):
    results = set()
    if balance < reserve:
        return results
    for actions, dates in PATHS:
        cash = balance
        for day, action in enumerate(actions, 1):
            if busy == day and action:
                break
            cash += income
            if busy == day:
                cash -= fee
            if day >= busy + delay:
                cash += gain
            cash -= (0, a, b)[action]
            if cash < reserve:
                break
        else:
            results.add(dates)
    return results


def request_values(income, a, b, fee, busy, da, db, hard):
    return {'confirmed': True, 'horizon': 4, 'base_income': income, 'fixed_period': busy, 'fixed_cost': fee,
            'goals': [{'id': 'a', 'deadline': da, 'cost': a, 'hard_deadline': hard},
                      {'id': 'b', 'deadline': db, 'cost': b, 'hard_deadline': hard}]}


def test_all_5184_public_recurring_threshold_cases_against_action_sequences():
    threshold_scenarios = 0
    for balance, reserve, income, a, b, fee, busy, da, db, delay in product(
        (0, 2, 4), (0, 1), (0, 1, 2), (1, 3), (1, 3), (0, 2, 3), (1, 2), (2, 4), (3, 4), (1, 2, 3)
    ):
        request = RecurringBenefitInput.model_validate({
            **request_values(income, a, b, fee, busy, da, db, True), 'quantum': 1, 'benefit_delay': delay,
        })
        actual = evaluate_recurring_benefit(snapshot(balance, reserve), request, current_date=TODAY)
        expected = next((gain for gain in range(11) if any(
            left <= da and right <= db
            for left, right in direct_paths(balance, reserve, income, a, b, fee, busy, delay, gain)
        )), None)
        assert actual['authority'] == 'NONE'
        assert actual['status'] == ('NO_FINITE_THRESHOLD' if expected is None else 'CONDITIONAL')
        if expected is not None:
            assert actual['minimum_per_period'] == f'{expected}.00'
        threshold_scenarios += 1
    assert threshold_scenarios == 5184


def test_all_3888_public_deadline_frontier_cases_against_action_sequences():
    deadline_scenarios = 0
    for balance, reserve, income, a, b, fee, busy, da, db in product(
        (0, 2, 4), (0, 1), (0, 1, 2), (1, 3), (1, 3), (0, 1, 3), (1, 2), (2, 3, 4), (2, 3, 4)
    ):
        request = GoalDeadlineInput.model_validate(request_values(income, a, b, fee, busy, da, db, False))
        result = evaluate_goal_deadlines(snapshot(balance, reserve), request, current_date=TODAY)
        for period, key in [(0, 'without_fixed_plan'), (busy, 'with_fixed_plan')]:
            paths = direct_paths(balance, reserve, income, a, b, fee, period, 1, 0)
            actual = result[key]
            if not paths:
                assert actual['status'] == 'NO_JOINT_COMPLETION_WITHIN_HORIZON'
                continue
            assert actual['joint_completion_count'] == len(paths)
            extensions = {(row['a'], row['b']) for row in actual['extensions']}
            for left, right in product(range(5), repeat=2):
                assert any(a <= left and b <= right for a, b in extensions) == any(
                    a <= da + left and b <= db + right for a, b in paths
                )
        deadline_scenarios += 1
    assert deadline_scenarios == 3888
