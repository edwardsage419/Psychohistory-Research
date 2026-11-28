"""Confirmed, local resource snapshots over a bounded cash and time contract."""

from datetime import UTC, date, datetime
from decimal import Decimal
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
    margin = balance - option.future_cost - reserve
    return {"status": "FEASIBLE" if OPERATORS[">="](margin, 0) else "INFEASIBLE",
            "future_cost": _money(option.future_cost), "reserve": _money(reserve), "margin": _money(margin)}


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
