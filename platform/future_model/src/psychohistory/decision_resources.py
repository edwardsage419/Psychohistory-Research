"""Confirmed, local resource snapshots over a bounded cash and time contract."""

from datetime import UTC, date, datetime
from decimal import Decimal
from fractions import Fraction
from math import ceil
import re
from typing import Annotated, Literal

from pydantic import BeforeValidator, Field, PlainSerializer, StringConstraints, model_validator

from .decision_feasibility import OPERATORS
from .decision_state import InputModel, Key, Text


RESOURCE_SCHEMA_VERSION = "1.0.0"
RESOURCE_VERSION = "1.0.0"
MAX_SCHEDULE_DAYS = 366
ACTUAL = {"actual_income", "actual_expense", "actual_refund"}
SIGNS = {"actual_income": 1, "actual_expense": -1, "actual_refund": 1}


def _exact_decimal(value):
    if type(value) is int:
        return value
    if isinstance(value, Decimal) and value.is_finite():
        return value
    if isinstance(value, str) and re.fullmatch(r"-?[0-9]{1,13}(?:\.[0-9]{1,8})?", value):
        return value
    raise ValueError("请输入精确十进制金额，例如 12.34。")


def _civil_date(value):
    if type(value) is date or (isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value)):
        return value
    raise ValueError("请使用 YYYY-MM-DD 日期。")


Money = Annotated[Decimal, Field(ge=-10**12, le=10**12, allow_inf_nan=False, decimal_places=8),
                  BeforeValidator(_exact_decimal), PlainSerializer(lambda value: format(value, "f"), when_used="json")]
NonnegativeMoney = Annotated[Money, Field(ge=0)]
CivilDate = Annotated[date, BeforeValidator(_civil_date)]
Minutes = Annotated[int, Field(ge=0, le=366 * 1440, strict=True)]


class CashEvent(InputModel):
    id: Key
    kind: Literal["actual_income", "actual_expense", "actual_refund", "estimated_income", "estimated_refund"]
    amount: NonnegativeMoney
    date: CivilDate
    source: Text
    refund_of: Key | None = None


class CashState(InputModel):
    currency: Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]
    opening_balance: Money
    opening_date: CivilDate | None = None
    balance_includes_through: CivilDate | None = None
    covered_through: CivilDate | None = None
    source: Text | None = None
    events: list[CashEvent] = Field(default_factory=list, max_length=128)

    @model_validator(mode="after")
    def check_cash(self):
        if (self.opening_date is None) == (self.balance_includes_through is None):
            raise ValueError("请选用期初余额，或注明当前余额已包含的日期。")
        events = {event.id: event for event in self.events}
        if len(events) != len(self.events):
            raise ValueError("交易标识必须唯一，已确认交易只能更正其现有记录。")
        refunds = {}
        for event in self.events:
            if event.kind == "actual_refund" and event.refund_of is None:
                raise ValueError("实际到账退款须关联原已付款。")
            if event.refund_of is None:
                continue
            paid = events.get(event.refund_of)
            if (event.kind not in {"actual_refund", "estimated_refund"} or paid is None
                    or paid.kind != "actual_expense" or paid.date > event.date):
                raise ValueError("退款关联须指向同账本较早或同日的实际付款。")
            if event.kind == "actual_refund":
                refunds[paid.id] = refunds.get(paid.id, Decimal(0)) + event.amount
                if refunds[paid.id] > paid.amount:
                    raise ValueError("同一付款的实际退款累计不能超过原付款。")
        return self


class DayCapacity(InputModel):
    date: CivilDate
    minutes: int = Field(ge=0, le=1440, strict=True)


class ResourceTask(InputModel):
    id: Key
    label: Text
    total_minutes: Minutes | None = None
    completed_minutes: Minutes | None = None
    release: CivilDate | None = None
    deadline: CivilDate | None = None
    mode: Literal["splittable", "continuous", "unknown"] = "unknown"
    prior_plan_id: Key | None = None
    source: Text | None = None

    @model_validator(mode="after")
    def check_task(self):
        if self.total_minutes is not None and self.completed_minutes is not None:
            if self.completed_minutes > self.total_minutes:
                raise ValueError("已完成工时不能超过任务总工时。")
        if self.release is not None and self.deadline is not None and self.release > self.deadline:
            raise ValueError("任务的开始日期不能晚于截止日期。")
        return self

    @property
    def remaining(self):
        if self.total_minutes == 0:
            return 0
        if self.total_minutes is not None and self.completed_minutes is not None:
            return self.total_minutes - self.completed_minutes
        return None


class ResourceOption(InputModel):
    option_id: Key
    future_cost: NonnegativeMoney | None = None
    tasks: list[ResourceTask] | None = Field(default=None, max_length=24)


class ResourceState(InputModel):
    version: Literal["1.0.0"] = RESOURCE_SCHEMA_VERSION
    as_of: CivilDate
    cash: CashState | None = None
    reserve: NonnegativeMoney | None = None
    capacity: list[DayCapacity] | None = Field(default=None, max_length=MAX_SCHEDULE_DAYS)
    shared_tasks: list[ResourceTask] = Field(default_factory=list, max_length=24)
    options: list[ResourceOption] = Field(default_factory=list, max_length=24)
    goals: list[Text] = Field(default_factory=list, max_length=24)
    limits: list[Text] = Field(default_factory=list, max_length=24)
    preferences: list[Text] = Field(default_factory=list, max_length=24)

    @model_validator(mode="after")
    def check_resources(self):
        if self.cash is not None:
            cash = self.cash
            anchor = cash.opening_date or cash.balance_includes_through
            if anchor > self.as_of or (cash.covered_through is not None
                                      and not anchor <= cash.covered_through <= self.as_of):
                raise ValueError("现金余额日期和覆盖日期须在核对时点或之前。")
            if any(event.kind in ACTUAL and event.date > self.as_of for event in cash.events):
                raise ValueError("不能把未来现金流记作已实际发生。")
        if self.capacity and len({item.date for item in self.capacity}) != len(self.capacity):
            raise ValueError("同一天的可用时间只能声明一次。")
        if len({option.option_id for option in self.options}) != len(self.options):
            raise ValueError("各方案资源只能声明一次。")
        shared = {task.id for task in self.shared_tasks}
        if len(shared) != len(self.shared_tasks):
            raise ValueError("共用任务标识必须唯一。")
        for option in self.options:
            tasks = option.tasks or []
            identities = {task.id for task in tasks}
            if identities & shared or len(identities) != len(tasks):
                raise ValueError("每个方案的共用与追加任务不能重复。")
        return self


def _money(value):
    if value == 0:
        return "0.00"
    exact = format(value, "f")
    whole, _, fraction = exact.partition(".")
    return f"{whole}.{fraction.rstrip('0').ljust(2, '0')}"


def _cash_position(state, today):
    cash = state.cash
    if cash is None:
        return {"status": "UNKNOWN", "reason": "BALANCE_REQUIRED"}, None
    details = {"currency": cash.currency, "estimates": [
        event.model_dump(mode="json") for event in cash.events if event.kind not in ACTUAL
    ]}
    if today != state.as_of:
        return {**details, "status": "UNKNOWN", "reason": "STALE_OR_FUTURE_BALANCE"}, None
    if cash.balance_includes_through != state.as_of and cash.covered_through != state.as_of:
        return {**details, "status": "UNKNOWN", "reason": "CASH_COVERAGE_REQUIRED"}, None
    if cash.opening_date is not None:
        applied = [event for event in cash.events if event.kind in ACTUAL and event.date >= cash.opening_date]
    else:
        applied = [event for event in cash.events if event.kind in ACTUAL and event.date > cash.balance_includes_through]
    balance = cash.opening_balance + sum((SIGNS[event.kind] * event.amount for event in applied), Decimal(0))
    return {**details, "status": "KNOWN", "balance": _money(balance), "applied_event_ids": [event.id for event in applied]}, balance


def _cash_feasibility(balance, reserve, option, applicable):
    if not applicable:
        return {"status": "NOT_APPLICABLE"}
    if balance is None:
        return {"status": "UNKNOWN", "reason": "SPENDABLE_BALANCE_REQUIRED"}
    if option.future_cost is None:
        if balance < reserve:
            return {"status": "INFEASIBLE", "reason": "BALANCE_BELOW_RESERVE", "reserve": _money(reserve)}
        return {"status": "UNKNOWN", "reason": "FUTURE_COST_REQUIRED"}
    return _cash_margin(balance, reserve, option.future_cost)


def _cash_margin(balance, reserve, future_cost):
    margin = balance - future_cost - reserve
    return {"status": "FEASIBLE" if OPERATORS[">="](margin, 0) else "INFEASIBLE",
            "future_cost": _money(future_cost), "reserve": _money(reserve), "margin": _money(margin)}


def _schedule(tasks, capacity, first):
    """EDF with known minute budgets over release/deadline windows."""
    last = min(max((task.deadline.toordinal() for task in tasks), default=first), first + MAX_SCHEDULE_DAYS - 1)
    ordered = sorted(tasks, key=lambda task: (task.deadline, task.id))
    remaining = {task.id: task.remaining for task in ordered}
    planned = []
    for day in range(first, last + 1):
        available = capacity.get(day, 0)
        for task in ordered:
            release = task.release.toordinal() if task.release else first
            if available == 0:
                break
            if day < release or day > task.deadline.toordinal() or remaining[task.id] == 0:
                continue
            minutes = min(available, remaining[task.id])
            available -= minutes
            remaining[task.id] -= minutes
            planned.append({"date": date.fromordinal(day).isoformat(), "task_id": task.id, "minutes": minutes})
        for task in ordered:
            if remaining[task.id] and day == task.deadline.toordinal():
                return False, task, planned
        if not any(remaining.values()):
            return True, None, planned
    return not any(remaining.values()), None, planned


def _time_feasibility(state, option, today, applicable):
    if not applicable:
        return {"status": "NOT_APPLICABLE"}
    if today < state.as_of:
        return {"status": "UNKNOWN", "reason": "FUTURE_SNAPSHOT"}
    tasks = [task for task in (*state.shared_tasks, *(option.tasks or [])) if task.remaining != 0]
    expired = [task.id for task in tasks if task.remaining is not None and task.deadline and task.deadline < today]
    if expired:
        return {"status": "INFEASIBLE", "reason": "DEADLINE_PASSED", "tasks": expired}
    first = today.toordinal()
    capacity = {item.date.toordinal(): item.minutes for item in (state.capacity or [])
                if item.date > today or (item.date == today == state.as_of)}
    numeric = [task for task in tasks if task.remaining is not None and task.deadline is not None]
    if numeric:
        feasible, missed, planned = _schedule(numeric, capacity, first)
        if not feasible:
            # Give unknown days a whole day's capacity before certifying impossibility.
            # This is a relaxation of both capacity and task divisibility.
            last = min(max(task.deadline.toordinal() for task in numeric), first + MAX_SCHEDULE_DAYS - 1)
            generous = {day: capacity.get(day, 1440) for day in range(first, last + 1)}
            _, obstruction, _ = _schedule(numeric, generous, first)
            if obstruction is not None:
                return {"status": "INFEASIBLE", "reason": "SHARED_CAPACITY_SHORTFALL", "task_id": obstruction.id,
                        "deadline": obstruction.deadline.isoformat()}
            return {"status": "UNKNOWN", "reason": "CAPACITY_OR_HORIZON_REQUIRED",
                    "task_id": missed.id if missed is not None else None}
    else:
        planned = []
    if option.tasks is None or len(numeric) != len(tasks):
        return {"status": "UNKNOWN", "reason": "TASK_SCOPE_PROGRESS_OR_DEADLINE_REQUIRED"}
    if any(task.mode != "splittable" for task in numeric):
        return {"status": "UNKNOWN", "reason": "TASK_DIVISIBILITY_UNSUPPORTED"}
    return {"status": "FEASIBLE", "schedule": planned}


def evaluate_resources(state: ResourceState, *, current_date: date | None = None) -> dict:
    """Evaluate a confirmed structured snapshot without granting action authority."""
    today = current_date if current_date is not None else datetime.now(UTC).date()
    cash_applicable = state.cash is not None or state.reserve is not None or any(
        option.future_cost is not None for option in state.options)
    time_applicable = state.capacity is not None or bool(state.shared_tasks) or any(
        option.tasks is not None for option in state.options)
    cash, balance = _cash_position(state, today) if cash_applicable else ({"status": "NOT_APPLICABLE"}, None)
    reserve = state.reserve if state.reserve is not None else Decimal(0)
    options = {}
    for option in state.options:
        cash_check = _cash_feasibility(balance, reserve, option, cash_applicable)
        time_check = _time_feasibility(state, option, today, time_applicable)
        checks = {cash_check["status"], time_check["status"]}
        if "INFEASIBLE" in checks:
            status = "INFEASIBLE"
        elif "UNKNOWN" in checks or state.limits or not (cash_applicable or time_applicable):
            status = "UNKNOWN"
        else:
            status = "FEASIBLE"
        options[option.option_id] = {"status": status, "cash": cash_check, "time": time_check}
    return {"version": RESOURCE_VERSION, "as_of": state.as_of.isoformat(), "evaluated_on": today.isoformat(),
            "cash": cash, "options": options, "unapplied_limits": state.limits,
            "authority": "NONE", "qualification": "CONFIRMED_USER_INPUT_ONLY"}


JOINT_RESOURCE_VERSION = "1.0.0"
RECURRING_BENEFIT_VERSION = "1.0.0"
GOAL_DEADLINE_VERSION = "1.0.0"


class CashObligation(InputModel):
    """An explicitly reconciled canonical identity in the current cash account."""

    id: Key
    amount: NonnegativeMoney
    due: CivilDate
    reflected_payment_id: Key | None = None


class JointResourceInput(InputModel):
    version: Literal["1.0.0"] = JOINT_RESOURCE_VERSION
    confirmed: bool = Field(strict=True)
    option_ids: list[Key] = Field(min_length=2, max_length=24)
    cash_allocations: dict[Key, Annotated[list[CashObligation], Field(max_length=24)]] | None = Field(
        default=None, max_length=24
    )
    shared_task_ids: list[Key] = Field(default_factory=list, max_length=24)

    @model_validator(mode="after")
    def check_scope(self):
        if len(set(self.option_ids)) != len(self.option_ids):
            raise ValueError("同一计划只能选择一次。")
        if len(set(self.shared_task_ids)) != len(self.shared_task_ids):
            raise ValueError("共用任务标识必须唯一。")
        if self.cash_allocations is not None:
            if set(self.cash_allocations) != set(self.option_ids):
                raise ValueError("每项所选计划须具有明确的现金义务清单。")
            for obligations in self.cash_allocations.values():
                if len({row.id for row in obligations}) != len(obligations):
                    raise ValueError("同一计划不能重复列出同一现金义务。")
        return self


def _joint_cash(state, request, selected, today):
    details, balance = _cash_position(state, today)
    if balance is None:
        return details
    if state.reserve is None:
        return {**details, "status": "UNKNOWN", "reason": "RESERVE_REQUIRED"}
    if request.cash_allocations is None:
        return {**details, "status": "UNKNOWN", "reason": "CASH_ALLOCATIONS_REQUIRED"}
    obligations = {}
    payments = {event.id: event for event in state.cash.events if event.kind == "actual_expense"}
    refunded_payments = {event.refund_of for event in state.cash.events
                         if event.kind == "actual_refund" and event.amount > 0}
    linked_payments = {}
    for option in selected:
        allocated = Decimal(0)
        for row in request.cash_allocations[option.option_id]:
            old = obligations.setdefault(row.id, row)
            if old != row:
                return {**details, "status": "CONFLICT", "reason": "CASH_OBLIGATION_CONFLICT",
                        "obligation_id": row.id}
            if row.reflected_payment_id is None:
                allocated += row.amount
                continue
            payment = payments.get(row.reflected_payment_id)
            if (payment is None or payment.amount != row.amount or payment.date > today
                    or payment.id in refunded_payments):
                return {**details, "status": "UNKNOWN", "reason": "PAYMENT_RECONCILIATION_REQUIRED",
                        "obligation_id": row.id}
            if linked_payments.setdefault(payment.id, row.id) != row.id:
                return {**details, "status": "CONFLICT", "reason": "PAYMENT_LINKED_TWICE"}
        if option.future_cost is None or option.future_cost != allocated:
            return {**details, "status": "UNKNOWN", "reason": "ALLOCATION_COVERAGE_REQUIRED",
                    "option_id": option.option_id}

    outstanding = [row for row in obligations.values() if row.reflected_payment_id is None]
    total = sum((row.amount for row in outstanding), Decimal(0))
    return {
        **details,
        **_cash_margin(balance, state.reserve, total),
        "outstanding_ids": sorted(row.id for row in outstanding),
        "reflected_payment_ids": sorted(linked_payments),
    }


def _joint_time(state, request, selected, today):
    if state.capacity is None and not state.shared_tasks and all(option.tasks is None for option in selected):
        return {"status": "NOT_APPLICABLE"}
    if today != state.as_of:
        return {"status": "UNKNOWN", "reason": "CURRENT_TIME_SNAPSHOT_REQUIRED"}
    if any(option.tasks is None for option in selected):
        return {"status": "UNKNOWN", "reason": "TASK_SCOPE_PROGRESS_OR_DEADLINE_REQUIRED"}
    shared_ids = set(request.shared_task_ids)
    tasks = {}
    used_shared_ids = set()
    for option in selected:
        for task in option.tasks:
            if task.id not in tasks:
                tasks[task.id] = task
            elif task.id not in shared_ids:
                return {"status": "UNKNOWN", "reason": "TASK_IDENTITY_REQUIRED", "task_id": task.id}
            elif tasks[task.id] != task:
                return {"status": "CONFLICT", "reason": "TASK_REVISION_CONFLICT", "task_id": task.id}
            else:
                used_shared_ids.add(task.id)
    if shared_ids != used_shared_ids:
        return {"status": "UNKNOWN", "reason": "SHARED_TASK_SCOPE_MISMATCH"}
    # Both lists were already validated by the archive-compatible snapshot contract.
    # Keep all merged tasks, including when the joint list exceeds one option's cap.
    combined = ResourceOption(option_id="joint", tasks=[]).model_copy(update={"tasks": list(tasks.values())})
    return _time_feasibility(state, combined, today, True)


def evaluate_joint_resources(state: ResourceState, request: JointResourceInput, *, current_date: date | None = None) -> dict:
    """Compare simultaneous plans under a confirmed, bounded shared snapshot."""
    today = current_date if current_date is not None else datetime.now(UTC).date()
    result = {"version": JOINT_RESOURCE_VERSION, "authority": "NONE", "as_of": state.as_of.isoformat(),
              "evaluated_on": today.isoformat(), "option_ids": request.option_ids}
    options = {option.option_id: option for option in state.options}
    if not request.confirmed:
        return {**result, "status": "UNKNOWN", "reason": "JOINT_SCOPE_CONFIRMATION_REQUIRED"}
    if not set(request.option_ids) <= options.keys():
        return {**result, "status": "UNKNOWN", "reason": "CONFIRMED_PLAN_REQUIRED"}
    selected = [options[key] for key in request.option_ids]
    cash_applicable = (
        request.cash_allocations is not None or state.cash is not None or state.reserve is not None
        or any(option.future_cost is not None for option in selected)
    )
    cash = _joint_cash(state, request, selected, today) if cash_applicable else {"status": "NOT_APPLICABLE"}
    time = _joint_time(state, request, selected, today)
    statuses = {cash["status"], time["status"]}
    if "INFEASIBLE" in statuses:
        status = "INFEASIBLE"
    elif statuses <= {"FEASIBLE", "NOT_APPLICABLE"} and "FEASIBLE" in statuses and not state.limits:
        status = "FEASIBLE"
    else:
        status = "UNKNOWN"
    return {**result, "status": status, "cash": cash, "time": time, "unapplied_limits": state.limits}


Period = Annotated[int, Field(ge=1, le=30, strict=True)]


class BenefitGoal(InputModel):
    id: Key
    cost: NonnegativeMoney
    earliest: Period = 1
    deadline: Period
    hard_deadline: bool = Field(default=True, strict=True)


class _SingleSlotScenario(InputModel):
    confirmed: bool = Field(strict=True)
    horizon: Period
    fixed_period: Period
    fixed_cost: NonnegativeMoney
    base_income: NonnegativeMoney
    goals: tuple[BenefitGoal, BenefitGoal]

    @model_validator(mode="after")
    def check_periods(self):
        first, second = self.goals
        if self.fixed_period > self.horizon or any(
            not goal.earliest <= goal.deadline <= self.horizon for goal in self.goals
        ):
            raise ValueError("计划时点与硬期限必须在给定时域内。")
        if first.id == second.id:
            raise ValueError("需要两项不同的既有目标。")
        return self


class GoalDeadlineInput(_SingleSlotScenario):
    version: Literal["1.0.0"] = GOAL_DEADLINE_VERSION


class RecurringBenefitInput(_SingleSlotScenario):
    version: Literal["1.0.0"] = RECURRING_BENEFIT_VERSION
    benefit_delay: Period
    quantum: Annotated[Money, Field(gt=0)]

    @model_validator(mode="after")
    def check_hard_deadlines(self):
        if any(not goal.hard_deadline for goal in self.goals):
            raise ValueError("持续收益门槛需要固定的目标硬期限。")
        return self


def _goal_pairs(request, include_plan):
    left, right = request.goals
    left_limit = left.deadline if left.hard_deadline else request.horizon
    right_limit = right.deadline if right.hard_deadline else request.horizon
    for a in range(left.earliest, left_limit + 1):
        for b in range(right.earliest, right_limit + 1):
            if a != b and (not include_plan or request.fixed_period not in (a, b)):
                yield a, b


def _balance_path(balance, request, first, second, include_plan):
    left, right = request.goals
    for period in range(1, request.horizon + 1):
        balance += request.base_income
        if include_plan and period == request.fixed_period:
            balance -= request.fixed_cost
        if period == first:
            balance -= left.cost
        if period == second:
            balance -= right.cost
        yield period, balance


def _benefit_units(balance, reserve, request, first, second):
    minimum_units = 0
    for period, balance in _balance_path(balance, request, first, second, include_plan=True):
        gap = reserve - balance
        if gap <= 0:
            continue
        payouts = max(0, period - request.fixed_period - request.benefit_delay + 1)
        if payouts == 0:
            return None
        # Fraction prevents rounding before taking the required integer ceiling.
        units = Fraction(gap) / (payouts * Fraction(request.quantum))
        minimum_units = max(minimum_units, ceil(units))
    return minimum_units


def _cash_scenario(state, request, today, version):
    result = {"version": version, "authority": "NONE",
              "admission": "NOT_ADMITTED", "scope": "TWO_SINGLE_SLOT_GOALS",
              "as_of": state.as_of.isoformat(), "evaluated_on": today.isoformat(), "horizon": request.horizon}
    if not request.confirmed:
        return {**result, "status": "UNKNOWN", "reason": "SCENARIO_CONFIRMATION_REQUIRED"}, None
    if today.toordinal() + request.horizon > date.max.toordinal() or state.limits:
        return {**result, "status": "UNKNOWN", "reason": "SCENARIO_SCOPE_UNRESOLVED"}, None
    cash, balance = _cash_position(state, today)
    if balance is None or state.reserve is None:
        return {**result, "status": "UNKNOWN", "reason": cash.get("reason", "RESERVE_REQUIRED")}, None
    return {**result, "currency": cash["currency"], "starting_balance": _money(balance),
            "reserve": _money(state.reserve), "assumed_base_income_per_period": _money(request.base_income)}, balance


def _witness_dates(request, today, pair):
    return {goal.id: date.fromordinal(today.toordinal() + period).isoformat()
            for goal, period in zip(request.goals, pair, strict=True)}


def evaluate_recurring_benefit(state: ResourceState, request: RecurringBenefitInput, *,
                               current_date: date | None = None) -> dict:
    """Conditional one-slot scenario using only the verified current cash balance."""
    today = current_date if current_date is not None else datetime.now(UTC).date()
    result, balance = _cash_scenario(state, request, today, RECURRING_BENEFIT_VERSION)
    if balance is None:
        return result

    result["benefit_from_period"] = request.fixed_period + request.benefit_delay
    best = None
    witness_dates = []
    if balance >= state.reserve:
        for first, second in _goal_pairs(request, include_plan=True):
            units = _benefit_units(balance, state.reserve, request, first, second)
            if units is None or (best is not None and units > best):
                continue
            if best is None or units < best:
                best = units
                witness_dates = []
            witness_dates.append(_witness_dates(request, today, (first, second)))
    if best is None:
        return {**result, "status": "NO_FINITE_THRESHOLD"}
    return {**result, "status": "CONDITIONAL", "minimum_per_period": _money(best * request.quantum),
            "witness_dates": witness_dates}


def _deadline_frontier(balance, reserve, request, today, include_plan):
    pairs = []
    if balance >= reserve:
        for first, second in _goal_pairs(request, include_plan=include_plan):
            path = _balance_path(balance, request, first, second, include_plan=include_plan)
            if all(remaining >= reserve for _, remaining in path):
                pairs.append((first, second))
    if not pairs:
        return {"status": "NO_JOINT_COMPLETION_WITHIN_HORIZON"}

    left, right = request.goals
    by_extension = {}
    for first, second in pairs:
        extension = (max(0, first - left.deadline), max(0, second - right.deadline))
        by_extension.setdefault(extension, _witness_dates(request, today, (first, second)))
    frontier = {}
    best_right = request.horizon + 1
    for delay_left, delay_right in sorted(by_extension):
        if delay_right < best_right:
            frontier[delay_left, delay_right] = by_extension[delay_left, delay_right]
            best_right = delay_right
    earliest = (min(pair[0] for pair in pairs), min(pair[1] for pair in pairs))
    return {
        "status": "CONDITIONAL", "on_time": (0, 0) in frontier,
        "marginal_earliest": _witness_dates(request, today, earliest),
        "marginal_earliest_joint": earliest in pairs,
        "extensions": [{left.id: a, right.id: b} for a, b in frontier],
        "witness_dates": list(frontier.values()),
        "joint_completion_count": len(pairs),
    }


def evaluate_goal_deadlines(state: ResourceState, request: GoalDeadlineInput, *,
                            current_date: date | None = None) -> dict:
    """Compare conditionally attainable deadline extensions without changing goals."""
    today = current_date if current_date is not None else datetime.now(UTC).date()
    result, balance = _cash_scenario(state, request, today, GOAL_DEADLINE_VERSION)
    if balance is None:
        return result
    return {
        **result, "status": "CONDITIONAL",
        "without_fixed_plan": _deadline_frontier(balance, state.reserve, request, today, include_plan=False),
        "with_fixed_plan": _deadline_frontier(balance, state.reserve, request, today, include_plan=True),
    }
