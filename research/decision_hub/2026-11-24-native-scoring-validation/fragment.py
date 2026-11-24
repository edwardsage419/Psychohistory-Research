from fractions import Fraction
from typing import NamedTuple


def _documented(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _basic_errors(ctx: Context) -> list[str]:
    errors = []
    if len(ctx.feasible) < 2:
        errors.append("需要至少两个通过硬约束筛查的可执行方案。")
    if not ctx.state.objectives:
        errors.append("需要列明比较目标、方向与单位。")
    return errors


def _horizon(quantity: Quantity, deadline: str | None) -> str | None:
    value = quantity.horizon or deadline
    return value.strip() if value is not None else None


def _score_gap(option: Option, objective: Objective, state: DecisionState) -> str | None:
    quantity = option.scores.get(objective.id)
    if quantity is None or quantity.kind == "unknown" or quantity.lower is None or quantity.upper is None:
        return "缺少可核对的得分或完整区间"
    if quantity.unit.strip() != objective.unit.strip():
        return f"得分单位 {quantity.unit} 与目标要求的 {objective.unit} 不一致"
    if not _documented(quantity.source):
        return "缺少得分来源"
    if not _horizon(quantity, state.deadline):
        return "缺少得分观察时域"
    if state.score_dependence == "rectangle" and state.score_transform == "clip_01":
        if not 0 <= quantity.lower <= quantity.upper <= 1:
            return "需要提供截断后 0–1 内的效用区间"
    return None


def _objective_horizons(options: tuple[Option, ...], objective: Objective, state: DecisionState) -> set[str | None]:
    return {
        _horizon(option.scores[objective.id], state.deadline)
        for option in options
        if not _score_gap(option, objective, state)
    }


def _score_bounds(option: Option, objective: Objective) -> tuple[Fraction, Fraction]:
    quantity = option.scores[objective.id]
    return Fraction(quantity.lower), Fraction(quantity.upper)


def _clip(value: Fraction) -> Fraction:
    return min(Fraction(1), max(Fraction(), value))


def _nominal_bounds(option: Option, objective: Objective, state: DecisionState) -> tuple[Fraction, Fraction]:
    lower, upper = _score_bounds(option, objective)
    if state.score_dependence == "shared_additive" and state.score_transform == "clip_01":
        return _clip(lower), _clip(upper)
    return lower, upper


def _oriented(values: tuple[Fraction, Fraction], objective: Objective) -> tuple[Fraction, Fraction]:
    lower, upper = values
    return (lower, upper) if objective.direction == "max" else (-upper, -lower)


def _difference(a: Option, b: Option, objective: Objective, state: DecisionState) -> tuple[Fraction, Fraction]:
    a_lo, a_hi = _oriented(_nominal_bounds(a, objective, state), objective)
    b_lo, b_hi = _oriented(_nominal_bounds(b, objective, state), objective)
    return a_lo - b_hi, a_hi - b_lo


def _pareto_relation(a: Option, b: Option, state: DecisionState) -> str:
    objectives = state.objectives
    if any(_score_gap(option, objective, state) for option in (a, b) for objective in objectives):
        return "UNKNOWN"
    if any(len(_objective_horizons((a, b), objective, state)) > 1 for objective in objectives):
        return "UNKNOWN"
    differences = [_difference(a, b, objective, state) for objective in objectives]
    a_strict = any(lower > 0 for lower, _ in differences)
    b_strict = any(upper < 0 for _, upper in differences)
    if a_strict and all(lower >= 0 for lower, _ in differences):
        return "A_DOMINATES"
    if b_strict and all(upper <= 0 for _, upper in differences):
        return "B_DOMINATES"
    if a_strict and b_strict:
        return "INCOMPARABLE"
    if all(lower == upper == 0 for lower, upper in differences):
        return "EQUAL"
    return "UNRESOLVED"


def _weight_errors(ctx: Context) -> list[str]:
    state = ctx.state
    errors = _basic_errors(ctx)
    if not _documented(state.score_basis) or len({obj.unit.strip() for obj in state.objectives}) != 1:
        errors.append("需要由用户确认共同的基数效用单位、目标间可补偿性与权重含义。")
    if not state.weights_confirmed:
        errors.append("需要用户确认每个目标的权重范围。")
    ids = {obj.id for obj in state.objectives}
    weights = state.weights
    if set(weights) != ids:
        errors.append("权重必须与列明的目标一一对应。")
    elif ids:
        lower = [Fraction(weight.lower) for weight in weights.values()]
        upper = [Fraction(weight.upper) for weight in weights.values()]
        if any(not 0 <= lo <= hi <= 1 for lo, hi in zip(lower, upper, strict=True)):
            errors.append("权重上下界应有序且位于 0 到 1。")
        elif not sum(lower) <= 1 <= sum(upper):
            errors.append("这些权重范围内没有总和等于 1 的组合。")
    for option in ctx.feasible:
        for objective in state.objectives:
            gap = _score_gap(option, objective, state)
            if gap:
                errors.append(f"{option.label}的{objective.label}{gap}。")
    horizons = set().union(*(
        _objective_horizons(ctx.feasible, objective, state) for objective in state.objectives
    ))
    if len(horizons) > 1:
        errors.append("加权比较需要所有方案与目标采用共同的得分观察时域。")
    return errors


def _weight_sensitivity_errors(ctx: Context) -> list[str]:
    errors = _weight_errors(ctx)
    for option in ctx.feasible:
        for objective in ctx.state.objectives:
            quantity = option.scores.get(objective.id)
            if quantity is not None and quantity.lower != quantity.upper:
                errors.append(f"{option.label}的{objective.label}含得分区间，权重单项分析需要点值。")
    return errors


def _weight_intervals(state: DecisionState) -> list[tuple[Fraction, Fraction]]:
    return [
        (Fraction(state.weights[obj.id].lower), Fraction(state.weights[obj.id].upper))
        for obj in state.objectives
    ]


def _extreme(
    coefficients: list[Fraction], bounds: list[tuple[Fraction, Fraction]], *, maximum: bool
) -> tuple[Fraction, list[Fraction]]:
    # Move mass from the vector of lower bounds to the best available coefficient.
    weights = [lo for lo, _ in bounds]
    remaining = 1 - sum(weights)
    for i in sorted(range(len(weights)), key=coefficients.__getitem__, reverse=maximum):
        added = min(bounds[i][1] - weights[i], remaining)
        weights[i] += added
        remaining -= added
    return _dot(coefficients, weights), weights


def _dot(coefficients: list[Fraction], weights: list[Fraction]) -> Fraction:
    return sum((coefficient * weight for coefficient, weight in zip(coefficients, weights, strict=True)), Fraction())


def _values(objectives, values) -> dict[str, str]:
    return {objective.id: _number(value) for objective, value in zip(objectives, values, strict=True)}


def _c034_errors(ctx: Context) -> list[str]:
    state = ctx.state
    errors = _weight_errors(ctx)
    if len(state.objectives) != 2 or any(objective.direction != "max" for objective in state.objectives):
        errors.append("C034 需要两个越高越好的基数效用目标。")
    if state.score_dependence not in {"rectangle", "shared_additive"} or not _documented(state.score_dependence_source):
        errors.append("需要明确得分的联合误差结构及其依据。")
    if state.score_transform not in {"identity", "clip_01"}:
        errors.append("需要确认得分使用恒等变换或截断至 0–1。")
    if state.score_dependence == "shared_additive":
        if set(state.shared_offsets) != {objective.id for objective in state.objectives}:
            errors.append("每个目标需要有可核对的共同偏移区间。")
        if any(
            (quantity := option.scores.get(objective.id)) is not None
            and quantity.lower != quantity.upper
            for option in ctx.feasible for objective in state.objectives
        ):
            errors.append("共同偏移模型需要名义点值，方案特有误差需要另行指定联合模型。")
    return errors


class _Cell(NamedTuple):
    difference: Fraction
    a_score: Fraction
    b_score: Fraction
    offset: Fraction | None = None


def _clipping_cell(a: Fraction, b: Fraction, offsets: Weight) -> tuple[_Cell, _Cell]:
    lower, upper = Fraction(offsets.lower), Fraction(offsets.upper)
    breakpoints = {lower, upper, -a, 1 - a, -b, 1 - b}
    candidates = []
    for offset in sorted(breakpoints):
        if lower <= offset <= upper:
            a_score, b_score = _clip(a + offset), _clip(b + offset)
            candidates.append(_Cell(a_score - b_score, a_score, b_score, offset))
    return min(candidates, key=lambda cell: cell.difference), max(candidates, key=lambda cell: cell.difference)


def _joint_cells(a: Option, b: Option, state: DecisionState) -> tuple[list[_Cell], list[_Cell]]:
    minima = []
    maxima = []
    for objective in state.objectives:
        a_lo, a_hi = _score_bounds(a, objective)
        b_lo, b_hi = _score_bounds(b, objective)
        if state.score_dependence == "shared_additive" and state.score_transform == "clip_01":
            low, high = _clipping_cell(a_lo, b_lo, state.shared_offsets[objective.id])
        else:
            low, high = _Cell(a_lo - b_hi, a_lo, b_hi), _Cell(a_hi - b_lo, a_hi, b_lo)
        minima.append(low)
        maxima.append(high)
    return minima, maxima


