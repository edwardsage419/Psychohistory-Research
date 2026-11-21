"""Sourced timing inputs and finite-horizon decision comparisons."""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .decision_registry import Context, Method
from .decision_scoring import _number as _exact
from .decision_state import InputModel, Key, Kind, Number, Text, TextLine

Nonnegative = Annotated[Number, Field(ge=0)]
Mass = Annotated[Number, Field(ge=0, le=1)]
_SUPPORTED_PROBABILITY = frozenset({"fact", "estimate", "synthetic"})
_STRATEGY_LABELS = {"act_now": "立即行动", "status_quo": "维持现状", "wait": "等待后行动"}
_FORECAST_LABELS = {"WITHIN": "在期限内", "AFTER": "越过期限", "STRADDLES": "预测区间跨过期限", "UNKNOWN": "待核对"}
_CHART_SCENARIO_LIMIT = 4

type Event = tuple[Fraction, str, str, Fraction]
type Affine = tuple[Fraction, Fraction]
type Branches = dict[tuple[Fraction, str], dict[str, Fraction]]


class TimeValue(InputModel):
    lower: Nonnegative | None = None
    upper: Nonnegative | None = None
    kind: Kind = "unknown"
    source: TextLine = ""

    @model_validator(mode="after")
    def check_bounds(self):
        if self.kind == "unknown" and (self.lower is not None or self.upper is not None):
            raise ValueError("未知数值应留空")
        if self.lower is not None and self.upper is not None and self.lower > self.upper:
            raise ValueError("下界不能大于上界")
        return self


class Cutoff(InputModel):
    at: Nonnegative
    inclusive: bool = Field(strict=True)
    kind: Kind
    source: TextLine = ""


class Reversibility(InputModel):
    description: Text
    kind: Kind
    source: TextLine = ""


class TimingAction(InputModel):
    cutoff: Cutoff | None = None
    switching_cost: TimeValue | None = None
    delay_losses: Annotated[dict[Key, TimeValue], Field(max_length=24)] = Field(default_factory=dict)
    reversibility: Reversibility | None = None


class CompletionMass(InputModel):
    duration: Nonnegative
    probability: Mass


class JointMass(CompletionMass):
    scenario_id: Key
    signal_id: Key


class Investigation(InputModel):
    mode: Literal["deterministic", "joint", "conditional"]
    cost: TimeValue | None = None
    duration: TimeValue | None = None
    kind: Kind = "unknown"
    source: TextLine = ""
    joint: list[JointMass] = Field(default_factory=list, max_length=384)
    completion_by_state: Annotated[
        dict[Key, Annotated[list[CompletionMass], Field(max_length=24)]], Field(max_length=24)
    ] = Field(default_factory=dict)


class TimingInput(InputModel):
    confirmed: bool = Field(default=False, strict=True)
    time_unit: Text | None = None
    time_origin: Text | None = None
    horizon: Cutoff | None = None
    decision_deadline: Cutoff | None = None
    desired_time: TimeValue | None = None
    predicted_completion: TimeValue | None = None
    wait_duration: TimeValue | None = None
    actions: Annotated[dict[Key, TimingAction], Field(max_length=24)] = Field(default_factory=dict)
    status_quo_option_id: Key | None = None
    fallback_option_id: Key | None = None
    investigation: Investigation | None = None


def _sourced(value) -> bool:
    return value is not None and value.kind != "unknown" and bool(value.source.strip())


def _point(value) -> Fraction | None:
    if _sourced(value) and value.lower is not None and value.lower == value.upper:
        return Fraction(value.lower)
    return None


def _by(time: Fraction, cutoff: Cutoff) -> bool:
    deadline = Fraction(cutoff.at)
    return time < deadline or (time == deadline and cutoff.inclusive)


def _availability(timing: TimingInput, option_id: str, time: Fraction) -> str:
    rule = timing.actions.get(option_id)
    bounds = (timing.horizon, timing.decision_deadline, rule.cutoff if rule else None)
    if any(_sourced(item) and not _by(time, item) for item in bounds if item is not None):
        return "EXPIRED"
    if rule is None or any(not _sourced(item) for item in bounds if item is not None):
        return "UNKNOWN"
    return "FEASIBLE"


def immediate_availability(timing: TimingInput | None, option_id: str) -> str:
    """Check the confirmed time basis and action availability at its origin."""
    if timing is None or not timing.confirmed:
        return "UNKNOWN"
    if not timing.time_origin or not timing.time_unit or not _sourced(timing.horizon):
        return "UNKNOWN"
    return _availability(timing, option_id, Fraction())


def _common_errors(ctx: Context) -> list[str]:
    timing = getattr(ctx.state, "timing", None)
    if timing is None:
        return ["需要设置行动时机。"]
    errors = []
    if not timing.confirmed:
        errors.append("请确认行动时机及时间假设。")
    if not timing.time_unit or not timing.time_origin or not _sourced(timing.horizon):
        errors.append("需要共同的时间单位、起算时点与有来源的分析时域。")
    if not ctx.feasible:
        errors.append("需要至少一个通过硬约束的行动。")
    if not ctx.state.scenarios or not ctx.state.scenario_basis:
        errors.append("需要情景及已确认的共同基数效用口径。")
    option_ids = {option.id for option in ctx.state.options}
    scenario_ids = {scenario.id for scenario in ctx.state.scenarios}
    if set(timing.actions) - option_ids or any(
        option_id is not None and option_id not in option_ids
        for option_id in (timing.status_quo_option_id, timing.fallback_option_id)
    ):
        errors.append("行动时机引用了不存在的方案。")
    if any(set(rule.delay_losses) - scenario_ids for rule in timing.actions.values()):
        errors.append("延迟损失引用了不存在的情景。")
    return errors


def _option_values(
    ctx: Context, supported_states: set[str] | None = None,
) -> tuple[dict[str, dict[str, Fraction]], str | None, list[str]]:
    """Read point utilities only from known, sourced, compatible cells."""
    values = {}
    units = set()
    horizons = set()
    gaps = []
    options = [
        option for option in ctx.feasible if immediate_availability(ctx.state.timing, option.id) == "FEASIBLE"
    ]
    for scenario in ctx.state.scenarios:
        if supported_states is not None and scenario.id not in supported_states:
            continue
        row = {}
        for option in options:
            utility = scenario.utilities.get(option.id)
            value = _point(utility)
            horizon = (utility.horizon or ctx.state.deadline) if utility is not None else None
            if not _sourced(scenario) or value is None or horizon is None:
                gaps.append(f"「{option.label}」在「{scenario.label}」中的效用点值、来源或观察时域待核对。")
                continue
            units.add(utility.unit.strip())
            horizons.add(horizon.strip())
            row[option.id] = value
        values[scenario.id] = row
    if len(units) > 1 or len(horizons) > 1:
        gaps.append("所有行动情景需要采用同一效用单位和观察时域。")
        return {}, None, gaps
    return values, next(iter(units), None), gaps


def _relative(prediction: TimeValue | None, cutoff: Cutoff | None) -> str:
    if not _sourced(prediction) or prediction.lower is None or prediction.upper is None or not _sourced(cutoff):
        return "UNKNOWN"
    if not _by(Fraction(prediction.lower), cutoff):
        return "AFTER"
    if _by(Fraction(prediction.upper), cutoff):
        return "WITHIN"
    return "STRADDLES"


def _time_inputs(ctx: Context) -> dict:
    timing = ctx.state.timing
    keys = ("horizon", "decision_deadline", "desired_time", "predicted_completion", "wait_duration")
    result = {"time_unit": timing.time_unit, "time_origin": timing.time_origin}
    for key in keys:
        value = getattr(timing, key)
        result[key] = value.model_dump(mode="json") if value is not None else None
        if isinstance(value, TimeValue):
            for bound in ("lower", "upper"):
                number = getattr(value, bound)
                result[key][bound] = _exact(Fraction(number)) if number is not None else None
        elif isinstance(value, Cutoff):
            result[key]["at"] = _exact(Fraction(value.at))
    result["prediction_vs_deadline"] = _relative(timing.predicted_completion, timing.decision_deadline)
    result["prediction_vs_horizon"] = _relative(timing.predicted_completion, timing.horizon)
    result["prediction_vs_action_cutoffs"] = {
        option.id: _relative(timing.predicted_completion, timing.actions[option.id].cutoff)
        for option in ctx.feasible if option.id in timing.actions and timing.actions[option.id].cutoff is not None
    }
    return result


def _timing_tables(ctx: Context, times: dict) -> list[dict]:
    timing = ctx.state.timing
    rows = []
    for key, label in (
        ("horizon", "分析时域"),
        ("decision_deadline", "决定截止"),
        ("desired_time", "希望完成时间"),
        ("predicted_completion", "预测完成时间"),
        ("wait_duration", "拟等待时长"),
    ):
        value = times[key]
        if value is None:
            continue
        if "at" in value:
            interval = ("≤ " if value["inclusive"] else "< ") + value["at"]
        else:
            bounds = value["lower"], value["upper"]
            interval = f"[{bounds[0] or '?'}，{bounds[1] or '?'}]"
        rows.append([label, interval, value["kind"], value["source"]])
    for option in ctx.feasible:
        action = timing.actions.get(option.id)
        if action is not None and action.cutoff is not None:
            cutoff = action.cutoff
            boundary = ("≤ " if cutoff.inclusive else "< ") + _exact(Fraction(cutoff.at))
            rows.append([f"「{option.label}」行动截止", boundary, cutoff.kind, cutoff.source])
    reversibility = []
    payoff_inputs = []
    for option in ctx.feasible:
        action = timing.actions.get(option.id)
        detail = action.reversibility if action is not None else None
        reversibility.append([
            option.label, detail.description if _sourced(detail) else "UNKNOWN",
            detail.source if detail is not None else None,
        ])
        if action is None:
            continue
        entries = [(None, "换转成本", action.switching_cost)]
        entries.extend((scenario.label, "单位时间延迟损失", action.delay_losses.get(scenario.id))
                       for scenario in ctx.state.scenarios)
        for scenario_label, role, value in entries:
            point = _point(value)
            payoff_inputs.append([
                option.label, scenario_label, role, _exact(point) if point is not None else None,
                value.kind if value is not None else "unknown", value.source if value is not None else None,
            ])
    tables = [
        {
            "title": f"时间口径（从「{timing.time_origin}」起算，{timing.time_unit}）",
            "columns": ["用途", "时间", "证据类型", "来源"], "rows": rows,
        },
        {"title": "撤销条件与影响", "columns": ["方案", "可逆性说明", "来源"], "rows": reversibility},
        {
            "title": "换转成本及延迟损失依据",
            "columns": ["方案", "情景", "用途", "数值", "证据类型", "来源"],
            "rows": payoff_inputs,
        },
    ]
    if timing.predicted_completion is not None:
        checks = [["分析时域", _FORECAST_LABELS[times["prediction_vs_horizon"]]]]
        if timing.decision_deadline is not None:
            checks.append(["决定截止", _FORECAST_LABELS[times["prediction_vs_deadline"]]])
        checks.extend(
            [f"「{option.label}」行动截止", _FORECAST_LABELS[times["prediction_vs_action_cutoffs"][option.id]]]
            for option in ctx.feasible if option.id in times["prediction_vs_action_cutoffs"]
        )
        tables.append({"title": "完成预测与期限", "columns": ["边界", "完成预测关系"], "rows": checks})
    return tables


def _payoffs(
    ctx: Context, option_id: str, duration: Fraction, utilities: dict[str, dict[str, Fraction]],
) -> tuple[dict[str, Fraction], list[str]]:
    option = next(option for option in ctx.feasible if option.id == option_id)
    rule = ctx.state.timing.actions[option_id]
    switching = _point(rule.switching_cost)
    if switching is None:
        return {}, [f"需要「{option.label}」有来源的换转成本点值，已确认无成本时可填零。"]
    result = {}
    gaps = []
    for scenario in ctx.state.scenarios:
        value = utilities.get(scenario.id, {}).get(option_id)
        loss = _point(rule.delay_losses.get(scenario.id)) if duration else Fraction()
        if value is None or loss is None:
            gaps.append(f"「{option.label}」在「{scenario.label}」中的效用或单位时间延迟损失为 UNKNOWN。")
        else:
            result[scenario.id] = value - switching - duration * loss
    return result, gaps


def _unavailable(ctx: Context, status: str, option_label: str, time: Fraction) -> str | None:
    if status == "EXPIRED":
        return f"「{option_label}」在 {_exact(time)} {ctx.state.timing.time_unit} 已越过所列截止或分析时域。"
    if status == "UNKNOWN":
        return f"需要核对「{option_label}」的行动时间规则及期限来源。"
    return None


def _action_comparison(ctx: Context) -> dict:
    timing = ctx.state.timing
    utility, unit, gaps = _option_values(ctx)
    wait = _point(timing.wait_duration)
    if timing.wait_duration is not None and wait is None:
        gaps.append("拟等待时长需要一个有来源的点值才能比较固定等待方案。")
    if timing.status_quo_option_id is not None and timing.status_quo_option_id not in {o.id for o in ctx.feasible}:
        gaps.append("用户标注的现状方案尚未通过硬约束。")
    rows = []
    comparison = []
    values = {}
    for option in ctx.feasible:
        immediate = "status_quo" if option.id == timing.status_quo_option_id else "act_now"
        plans = [(immediate, Fraction())]
        if wait is not None:
            plans.append(("wait", wait))
        for strategy, time in plans:
            status = _availability(timing, option.id, time)
            reason = _unavailable(ctx, status, option.label, time)
            if reason:
                gaps.append(reason)
            payoffs = {}
            if status == "FEASIBLE":
                payoffs, payoff_gaps = _payoffs(ctx, option.id, time, utility)
                if payoff_gaps:
                    status = "UNKNOWN"
                    gaps.extend(payoff_gaps)
                else:
                    values[(strategy, option.id)] = payoffs
            comparison.append({
                "type": strategy, "option_id": option.id, "status": status, "duration": _exact(time),
                "utilities": {key: _exact(value) for key, value in payoffs.items()},
            })
            description = _STRATEGY_LABELS[strategy]
            rows.append([
                option.label, description, _exact(time), {"EXPIRED": "已截止", "FEASIBLE": "可执行", "UNKNOWN": "待核对"}[status],
                *(_exact(payoffs[s.id]) if s.id in payoffs else None for s in ctx.state.scenarios),
            ])
    frontier = [
        {"type": key[0], "option_id": key[1]}
        for key, payoffs in values.items()
        if not any(
            all(other[s] >= value for s, value in payoffs.items())
            and any(other[s] > value for s, value in payoffs.items())
            for other in values.values()
        )
    ]
    incomplete = not values or any(row["status"] == "UNKNOWN" for row in comparison) or (
        timing.wait_duration is not None and wait is None
    )
    times = _time_inputs(ctx)
    labels = {option.id: option.label for option in ctx.feasible}
    summary = "逐情景比较立即行动、现状与已填报的固定等待。每种策略预先固定行动，比较未使用任何概率。"
    leaders = []
    if incomplete:
        summary += "部分结果待核对，完整行动排序为 UNKNOWN。"
    elif frontier:
        frontier_options = list(dict.fromkeys(row["option_id"] for row in frontier))
        names = "、".join(labels[key] for key in frontier_options)
        if len(frontier_options) == 1:
            leaders = frontier_options
        summary += f"在当前情景中，{names}对应未被其他可执行策略支配的结果。"
    tables = _timing_tables(ctx, times)
    tables.append({
        "title": f"可行时机与逐情景效用（{unit or '效用单位待核对'}）",
        "columns": ["中性方案名", "用户标明的角色", f"行动时刻（{timing.time_unit}）", "时间可行性",
                    *(s.label for s in ctx.state.scenarios)], "rows": rows,
    })
    charts = []
    if unit:
        for scenario in ctx.state.scenarios[:_CHART_SCENARIO_LIMIT]:
            points = [
                {"label": f"{labels[key]}（{_STRATEGY_LABELS[role]}）", "lower": _exact(payoff[scenario.id]),
                 "upper": _exact(payoff[scenario.id])}
                for (role, key), payoff in values.items()
            ]
            if points:
                charts.append({"title": f"「{scenario.label}」的行动时机效用", "unit": unit, "rows": points})
        if charts and len(ctx.state.scenarios) > _CHART_SCENARIO_LIMIT:
            summary += f"图中显示前 {_CHART_SCENARIO_LIMIT} 个情景，表中保留所有情景。"
    return {
        "summary": summary, "status": "UNKNOWN" if incomplete else "SCENARIO_COMPARISON",
        "probabilities_used": False, "strategies": comparison, "undominated_strategies": frontier,
        "leaders": leaders, "time_inputs": times, "tables": tables, "charts": charts, "gaps": list(dict.fromkeys(gaps)),
    }


def _mass_point(value) -> Fraction | None:
    point = _point(value)
    if point is not None and 0 <= point <= 1 and value.kind in _SUPPORTED_PROBABILITY:
        return point
    return None


def _positive_branch_scope(ctx: Context, signals: set[str]) -> tuple[dict[str, set[str]], list[str]]:
    information = getattr(ctx.state, "information", None)
    if information is None:
        # Direct joint input stands on the explicitly confirmed timing rules.
        return {}, []
    restrictions = information.actions_by_signal
    if information.unrestricted_actions:
        if restrictions or not information.action_source.strip():
            return {}, ["调查后行动范围需要单一且有来源的确认。"]
        return {}, []
    if not restrictions:
        return {}, ["需要确认调查后按时仍可执行的动作范围，或提供各信号下的行动限制与来源。"]
    all_options = {option.id for option in ctx.state.options}
    scope = {}
    errors = []
    for signal in sorted(signals):
        rule = restrictions.get(signal)
        if not _sourced(rule) or set(rule.option_ids) - all_options:
            errors.append(f"需要有来源的「{signal}」信号后行动范围。")
        else:
            scope[signal] = set(rule.option_ids)
    return scope, errors


def _joint_events(ctx: Context, model: Investigation) -> tuple[list[Event], list[str]]:
    if not model.joint or model.completion_by_state or model.duration is not None:
        return [], ["联合模式需要单一的完成时间、情景与信号联合概率表。"]
    scenario_ids = {scenario.id for scenario in ctx.state.scenarios}
    cells = {
        (Fraction(row.duration), row.scenario_id, row.signal_id): Fraction(row.probability)
        for row in model.joint
    }
    if len(cells) != len(model.joint) or {scenario for _, scenario, _ in cells} - scenario_ids:
        return [], ["联合概率表包含重复事件或未定义的情景。"]
    if sum(cells.values()) != 1:
        return [], ["联合概率之和须精确等于 1。"]
    info = getattr(ctx.state, "information", None)
    if info is not None and info.signals:
        if {signal for _, _, signal in cells} - {signal.id for signal in info.signals}:
            return [], ["联合概率表引用了未定义的信号。"]
    return [(*event, p) for event, p in cells.items() if p], []


def _factorized_events(ctx: Context, model: Investigation) -> tuple[list[Event], list[str]]:
    info = getattr(ctx.state, "information", None)
    if info is None or not info.signals:
        return [], ["请提供有来源的情景先验和条件信号概率，或填报直接联合概率。"]
    ids = {scenario.id for scenario in ctx.state.scenarios}
    signals = {signal.id for signal in info.signals}
    prior = {key: _mass_point(value) for key, value in info.prior.items()}
    if prior.keys() != ids or None in prior.values() or sum(prior.values()) != 1:
        return [], ["每个情景需要有来源的先验点概率，且总和须等于 1。"]
    duration = _point(model.duration)
    if model.mode == "deterministic":
        if duration is None or model.completion_by_state:
            return [], ["确定时长模式需要一个有来源的完成时长点值。"]
    elif set(model.completion_by_state) - ids or model.duration is not None:
        return [], ["条件模式仅使用所列情景各自的完成时间分布。"]
    if model.joint:
        return [], ["需选择一个概率结构，保留对应的输入。"]
    result = []
    for scenario, p in prior.items():
        if not p:
            continue
        conditional = {
            key: _mass_point(value) for key, value in info.likelihoods.get(scenario, {}).items()
        }
        if conditional.keys() != signals or None in conditional.values() or sum(conditional.values()) != 1:
            return [], [f"情景「{scenario}」下的信号点概率需有来源，且总和须等于 1。"]
        distribution = {duration: Fraction(1)}
        if model.mode == "conditional":
            rows = model.completion_by_state.get(scenario, [])
            distribution = {Fraction(row.duration): Fraction(row.probability) for row in rows}
            if len(distribution) != len(rows) or sum(distribution.values()) != 1:
                return [], [f"情景「{scenario}」需要唯一时长、总概率为 1 的条件完成分布。"]
        result.extend(
            (time, scenario, signal, p * d_mass * s_mass)
            for time, d_mass in distribution.items() if d_mass
            for signal, s_mass in conditional.items() if s_mass
        )
    return result, []


def _investigation_errors(ctx: Context) -> list[str]:
    errors = _common_errors(ctx)
    if errors:
        return errors
    model = ctx.state.timing.investigation
    if model is None:
        return ["尚未指定调查及信息到达方式。可改用无概率的行动时机比较。"]
    if model.kind not in _SUPPORTED_PROBABILITY or not model.source.strip():
        return ["需要完成与信号概率的证据，或注明合成数据来源。"]
    if _point(model.cost) is None:
        return ["需要有来源、与效用同单位的调查固定成本。"]
    events, errors = (_joint_events if model.mode == "joint" else _factorized_events)(ctx, model)
    if not errors:
        _, errors = _positive_branch_scope(ctx, {signal for _, _, signal, _ in events})
    return errors


def _mass_by_observation(events: list[Event]) -> tuple[Branches, dict[str, Fraction], dict[Fraction, Fraction]]:
    observations = defaultdict(dict)
    prior = defaultdict(Fraction)
    durations = defaultdict(Fraction)
    for time, state, signal, mass in events:
        observations[time, signal][state] = mass
        prior[state] += mass
        durations[time] += mass
    return observations, prior, durations


def _probability_provenance(ctx: Context, model: Investigation, supported_states: set[str]) -> dict:
    inputs = [(model.kind, model.source)]
    if model.mode != "joint":
        information = ctx.state.information
        inputs.extend((row.kind, row.source) for row in information.prior.values())
        inputs.extend(
            (row.kind, row.source)
            for scenario_id in sorted(supported_states)
            for row in information.likelihoods[scenario_id].values()
        )
        if model.mode == "deterministic":
            inputs.append((model.duration.kind, model.duration.source))
    limits = {"fact": 0, "estimate": 1, "assumption": 2, "synthetic": 3}
    kinds = {kind for kind, _ in inputs}
    return {
        "kind": max(kinds, key=limits.__getitem__),
        "source": model.source,
        "inputs": [{"kind": kind, "source": source} for kind, source in dict.fromkeys(inputs)],
    }


def _maximizers(values: dict[str, Fraction]) -> list[str]:
    if not values:
        return []
    best = max(values.values())
    return [key for key, value in values.items() if value == best]


def _branch(
    ctx: Context, time: Fraction, masses: dict[str, Fraction], utility: dict[str, dict[str, Fraction]],
    allowed: set[str] | None,
) -> tuple[list[str], dict[str, Fraction], list[str], dict[str, str]]:
    timing = ctx.state.timing
    values = {}
    eligible = []
    gaps = []
    availability = {}
    for option in ctx.feasible:
        option_id = option.id
        if allowed is not None and option_id not in allowed:
            availability[option_id] = "SIGNAL_EXCLUDED"
            continue
        status = _availability(timing, option_id, time)
        availability[option_id] = status
        if status == "UNKNOWN":
            gaps.append(_unavailable(ctx, status, option.label, time))
        if status != "FEASIBLE":
            continue
        eligible.append(option_id)
        payoff, utility_gaps = _payoffs(ctx, option_id, time, utility)
        if not set(masses) <= payoff.keys():
            gaps.extend(utility_gaps)
            continue
        values[option_id] = sum(mass * payoff[scenario] for scenario, mass in masses.items())
    if not eligible and not gaps:
        gaps.append(f"在 {_exact(time)} {timing.time_unit} 没有通过硬约束和期限检查的行动或兜底。")
    return eligible, values, gaps, availability


def _conditional_lines(
    ctx: Context, observations: Branches, utility: dict[str, dict[str, Fraction]], scope: dict[str, set[str]],
) -> dict[str, dict[str, Affine]] | None:
    lines = {}
    for (_, signal), masses in observations.items():
        choices = {}
        for option in ctx.feasible:
            if signal in scope and option.id not in scope[signal]:
                continue
            if immediate_availability(ctx.state.timing, option.id) == "EXPIRED":
                continue
            action = ctx.state.timing.actions.get(option.id)
            if action is None or (action.cutoff is not None and not _sourced(action.cutoff)):
                return None
            switching = _point(action.switching_cost)
            losses = {key: _point(action.delay_losses.get(key)) for key in masses}
            if switching is None or None in losses.values() or any(option.id not in utility.get(key, {}) for key in masses):
                return None
            intercept = sum(mass * (utility[key][option.id] - switching) for key, mass in masses.items())
            slope = sum(mass * losses[key] for key, mass in masses.items())
            choices[option.id] = (intercept, slope)
        lines[signal] = choices
    return lines


def _break_even(
    timing: TimingInput, lines: dict[str, dict[str, Affine]], baseline: Fraction, cost: Fraction,
) -> dict | None:
    horizon = Fraction(timing.horizon.at)
    split = {Fraction(), horizon}
    for cutoff in (timing.decision_deadline, *(r.cutoff for r in timing.actions.values())):
        if _sourced(cutoff) and Fraction(cutoff.at) < horizon:
            split.add(Fraction(cutoff.at))
    for choices in lines.values():
        for (a, da), (b, db) in combinations(choices.values(), 2):
            if da != db:
                cross = (a - b) / (da - db)
                if 0 < cross < horizon:
                    split.add(cross)

    def envelope(time):
        selected = []
        for choices in lines.values():
            eligible = [
                line for key, line in choices.items() if _availability(timing, key, time) == "FEASIBLE"
            ]
            if not eligible:
                return None
            selected.append(max(eligible, key=lambda line: line[0] - time * line[1]))
        return sum(line[0] for line in selected) - cost - baseline, sum(line[1] for line in selected)

    def profitable(time):
        line = envelope(time)
        return line is not None and line[0] > line[1] * time

    pieces = sorted(split)
    positive_through = [time for time in pieces if profitable(time)]
    for left, right in zip(pieces, pieces[1:]):
        line = envelope((left + right) / 2)
        if line is None:
            continue
        value, rate = line
        if value > left * rate:
            positive_through.append(min(right, value / rate) if rate else right)
    if not positive_through:
        return None
    latest = max(positive_through)
    return {"at": _exact(latest), "profitable_at_boundary": profitable(latest), "unit": timing.time_unit}


def _late_mass_range(
    ctx: Context,
    observations: Branches,
    durations: dict[Fraction, Fraction],
    gross: dict[Fraction, Fraction],
    utility: dict[str, dict[str, Fraction]],
    cost: Fraction,
) -> dict | None:
    """Vary the late mass while holding the state/signal law within each time fixed."""
    if len(durations) != 2:
        return None
    early, late = sorted(durations)
    utilities_by_time = []
    for time in (early, late):
        conditional_prior = defaultdict(Fraction)
        for (observed_time, _), masses in observations.items():
            if observed_time == time:
                for scenario, mass in masses.items():
                    conditional_prior[scenario] += mass / durations[time]
        _, immediate, gaps, _ = _branch(ctx, Fraction(), conditional_prior, utility, None)
        if gaps:
            return None
        utilities_by_time.append(immediate)
    early_value, late_value = (gross[time] / durations[time] - cost for time in (early, late))
    early_immediate, late_immediate = utilities_by_time

    lower, upper = Fraction(), Fraction(1)
    lower_inclusive = upper_inclusive = True
    possible = True
    # Beat every immediate action, since the best immediate action can depend on
    # the mixture even when the within-time investigation policy is unchanged.
    for option_id, first in early_immediate.items():
        offset = early_value - first
        slope = late_value - late_immediate[option_id] - offset
        if not slope:
            possible &= offset > 0
            continue
        root = -offset / slope
        if slope > 0 and root >= lower:
            lower, lower_inclusive = root, False
        elif slope < 0 and root <= upper:
            upper, upper_inclusive = root, False
    interval = None
    if possible and (lower < upper or (lower == upper and lower_inclusive and upper_inclusive)):
        interval = {
            "lower": _exact(lower), "upper": _exact(upper),
            "lower_inclusive": lower_inclusive, "upper_inclusive": upper_inclusive,
        }
    return {"early_duration": _exact(early), "late_duration": _exact(late), "profitable_range": interval}


def _investigation_comparison(ctx: Context) -> dict:
    timing = ctx.state.timing
    model = timing.investigation
    info = getattr(ctx.state, "information", None)
    signals = {signal.id: signal.label for signal in info.signals} if info is not None else {}
    labels = {option.id: option.label for option in ctx.feasible}
    events, _ = (_joint_events if model.mode == "joint" else _factorized_events)(ctx, model)
    observations, prior, durations = _mass_by_observation(events)
    utility, unit, payoff_gaps = _option_values(ctx, set(prior))
    provenance = _probability_provenance(ctx, model, set(prior))
    scope, _ = _positive_branch_scope(ctx, {signal for _, signal in observations})
    immediate_eligible, immediate, gaps, immediate_availability = _branch(ctx, Fraction(), prior, utility, None)
    immediate_leaders = _maximizers(immediate) if not gaps else []
    immediate_value = immediate[immediate_leaders[0]] if immediate_leaders else None
    gaps.extend(payoff_gaps)
    cost = _point(model.cost)
    policy = []
    rows = []
    branch_gaps = []
    gross_by_time = defaultdict(Fraction)
    for (time, signal), masses in sorted(observations.items()):
        eligible, values, unknown, availability = _branch(ctx, time, masses, utility, scope.get(signal))
        best = _maximizers(values) if not unknown else []
        if best:
            gross_by_time[time] += values[best[0]]
        branch_gaps.extend(unknown)
        policy.append({
            "duration": _exact(time), "signal_id": signal, "probability": _exact(sum(masses.values())),
            "eligible_option_ids": eligible, "option_ids": best, "availability": availability,
            "fallback_selected": timing.fallback_option_id in best,
            "expected_contribution": _exact(values[best[0]]) if best else None,
        })
        rows.append([
            _exact(time), signals.get(signal, signal), _exact(sum(masses.values())),
            "、".join(labels[key] for key in eligible) or None,
            "、".join(labels[key] for key in best) or None,
            labels[timing.fallback_option_id] if timing.fallback_option_id in best else None,
            _exact(values[best[0]]) if best else None,
        ])
    gaps.extend(branch_gaps)
    after_cost = sum(gross_by_time.values()) - cost if not branch_gaps else None
    net = after_cost - immediate_value if after_cost is not None and immediate_value is not None else None
    status = "UNKNOWN" if net is None else "INVESTIGATE" if net > 0 else "ACT_NOW" if net < 0 else "TIE"
    threshold = None
    late_mass_sensitivity = None
    if model.mode == "deterministic" and immediate_value is not None:
        lines = _conditional_lines(ctx, observations, utility, scope)
        if lines is not None:
            threshold = _break_even(timing, lines, immediate_value, cost)
        else:
            gaps.append("需要各相关情景的完整损失率与时间规则才能复算确定时长的优势边界。")
    elif net is not None:
        late_mass_sensitivity = _late_mass_range(ctx, observations, durations, gross_by_time, utility, cost)
    if model.mode == "conditional":
        probability_basis = "按有来源的条件独立假设，在给定情景后分解完成时间和信号。"
    elif model.mode == "joint":
        probability_basis = "直接使用完成时间、情景和信号的联合概率。"
    else:
        probability_basis = "完成时间固定，使用有来源的情景概率和情景内信号概率。"
    summary = (
        "按事前风险中性期望效用比较。调查完成后观察到达时刻和信号，再从仍可执行的行动中选择。"
        + probability_basis
    )
    if provenance["kind"] == "synthetic":
        summary += "概率或时长包含合成输入，数值用于复算示例。"
    elif provenance["kind"] in {"estimate", "assumption"}:
        summary += "概率或时长使用了所列估计或假设。"
    if status == "UNKNOWN":
        summary += "缺少可行的结束行动或收益依据，净价值为 UNKNOWN。"
    else:
        summary += f"相对立即行动的调查净增益为 {_exact(net)} {unit}。"
    if threshold is not None:
        symbol = "≤" if threshold["profitable_at_boundary"] else "<"
        summary += f"在所列确定时长模型内，调查严格占优要求完成时间 {symbol} {threshold['at']} {timing.time_unit}。"
    if late_mass_sensitivity is not None:
        interval = late_mass_sensitivity["profitable_range"]
        summary += "晚到概率的敏感性比较固定各时点内的情景与信号分布，并重新计算立即行动基线。"
        if interval is None:
            summary += "这种混合下没有使调查严格占优的晚到概率。"
        else:
            left = "[" if interval["lower_inclusive"] else "("
            right = "]" if interval["upper_inclusive"] else ")"
            summary += f"调查严格占优的晚到概率范围为 {left}{interval['lower']}，{interval['upper']}{right}。"
    times = _time_inputs(ctx)
    tables = _timing_tables(ctx, times)
    tables.extend([
        {
            "title": f"基线与调查净价值（{unit or '效用单位待核对'}）",
            "columns": ["立即可行方案", "立即行动最优方案", "立即行动效用", "调查直接成本", "调查净效用", "调查相对净增益"],
            "rows": [[
                "、".join(labels[key] for key in immediate_eligible) or None,
                "、".join(labels[key] for key in immediate_leaders) or None,
                _exact(immediate_value) if immediate_value is not None else None,
                _exact(cost), _exact(after_cost) if after_cost is not None else None,
                _exact(net) if net is not None else None,
            ]],
        },
        {
            "title": "观察完成时刻及信号后选择",
            "columns": [f"时刻（{timing.time_unit}）", "信号", "联合概率", "仍可行动作", "最优动作（含并列）",
                        "入选的指定兜底", "效用贡献"],
            "rows": rows,
        },
        {
            "title": "调查输入的概率依据",
            "columns": ["计算口径", "证据类型", "来源"],
            "rows": [[probability_basis, entry["kind"], entry["source"]] for entry in provenance["inputs"]],
        },
    ])
    charts = []
    if after_cost is not None and immediate_value is not None:
        charts.append({
            "title": "立即行动与调查的期望效用比较", "unit": unit,
            "rows": [{"label": label, "lower": _exact(value), "upper": _exact(value)}
                     for label, value in (("立即行动", immediate_value), ("先调查", after_cost))],
        })
    return {
        "summary": summary, "status": status, "tables": tables, "charts": charts,
        "probabilities_used": True, "probability_basis": model.mode,
        "probability_provenance": provenance,
        "immediate_value": _exact(immediate_value) if immediate_value is not None else None,
        "investigation_value": _exact(after_cost) if after_cost is not None else None,
        "net_value": _exact(net) if net is not None else None,
        "immediate_leaders": immediate_leaders, "immediate_availability": immediate_availability,
        "leaders": immediate_leaders if status == "ACT_NOW" else [],
        "policy": policy, "threshold": threshold, "time_inputs": times, "gaps": list(dict.fromkeys(gaps)),
        "late_mass_sensitivity": late_mass_sensitivity,
        "duration_probabilities": {_exact(time): _exact(mass) for time, mass in sorted(durations.items())},
        "scenario_probabilities": {key: _exact(mass) for key, mass in prior.items()},
    }


_RESEARCH = "research/decision_methods/"

METHODS = (
    Method(
        model_id="timing_actions", version="1.0.0", title="立即行动、等待与维持现状",
        applicability="时机已确认、使用共同起点和分析时域，按所列情景对比可执行方案。",
        inputs=("有来源的期限与时间变量", "可行方案的情景效用", "实际换转成本", "情景内延迟损失"),
        outputs=("情景效用与未被支配的策略", "时间可行性", "现状标签与可逆性依据"),
        units="输入指定的时间单位及共同效用量尺。",
        assumptions=(
            "延迟损失按情景与动作单独计量，固定等待期间无新信息。",
            "明确填有时机规则的方案沿用共同时域与共同截止，并应用已填报的单独截止。",
        ),
        uncertainty="没有概率时逐情景比较，列出 UNKNOWN 并保留实际换转费用。",
        sources=(
            _RESEARCH + "C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md",
            _RESEARCH + "BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md",
            _RESEARCH + "SAMUELSON_ZECKHAUSER_1988_STATUS_QUO_FRAMING_AUDIT_2026-11-20.md",
            _RESEARCH + "TVERSKY_SHAFIR_1992_CONFLICT_DEFERRAL_OPTION_SET_BOUNDARY_2026-11-21.md",
        ),
        failure_conditions="硬约束可行性、效用、行动时机或来源不明时，对应策略待核对。",
        replay="在共享时间轴上检查每个动作的期限，逐情景从效用扣除换转成本及随时间增加的延迟损失。",
        baseline="以相同标签和真实成本逐情景比较立即采取的行动。",
        validate=_common_errors, execute=_action_comparison,
    ),
    Method(
        model_id="timing_investigation", version="1.0.0", title="有截止期限的调查信息价值",
        applicability="调查完成才观察到时长与信号，有限概率已注明来源，给定可执行范围与共用效用标尺。",
        inputs=("固定调查费", "确定时长、联合概率或基于证据的条件因式分解", "行动窗口与情景延迟损失"),
        outputs=("立即行动基线", "观察后最优行动", "净调查价值", "确定时长的优势边界"),
        units="输入指定的时间单位及共同效用量尺。",
        assumptions=(
            "调查前承诺，调查中途不可取消。固定成本与每个动作的线性机会损失分开计量。",
            "条件模式明确使用给定情景后的完成时间与信号条件独立。依赖关系未知时需直接联合证据。",
            "调查完成后先观察完成时刻与信号。默认考虑通过硬约束与期限检查的所有行动，并应用已填报的信号后限制。",
        ),
        uncertainty="保留合成与有来源的证据类型。正概率分支没有可执行行动时，净值为 UNKNOWN。",
        sources=(
            _RESEARCH + "VOI_DELAY_DEADLINE_OPPORTUNITY_COST_2026-11-21.md",
            _RESEARCH + "VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
            _RESEARCH + "VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md",
        ),
        failure_conditions="概率、时间口径或效用来源缺失，或决策者不能在行动前观察到完成时刻和信号。",
        replay="按观察到的时间与信号分组枚举联合事件，逐组筛除到期行动，比较后验加权效用并扣除调查费。",
        baseline="在同一情景边际概率下，比较不调查且立即执行的最优行动。",
        validate=_investigation_errors, execute=_investigation_comparison,
    ),
)
