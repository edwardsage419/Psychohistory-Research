"""Decision methods for comparable scores and confirmed weight intervals."""

from fractions import Fraction
from itertools import combinations
from math import isfinite
from typing import NamedTuple

from .decision_registry import Context, Method
from .decision_state import DecisionState, Objective, Option, Quantity, Weight

_C004 = "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md"
_C034 = "research/decision_methods/C034_WEIGHT_SCORE_JOINT_ROBUSTNESS_CERTIFICATE_2026-11-20.md"
_SHARED = "research/decision_methods/C034_ADDENDUM_SHARED_SCORE_ERROR_CANCELLATION_2026-11-20.md"
_CLIPPING = "research/decision_methods/C034_ADDENDUM_CLIPPING_BREAKS_SHARED_ERROR_CANCELLATION_2026-11-20.md"

_RELATIONS = {
    "A_DOMINATES": "甲保证支配乙",
    "B_DOMINATES": "乙保证支配甲",
    "INCOMPARABLE": "各有更好的目标",
    "EQUAL": "各目标相等",
    "A_STRICT": "甲在所有允许情形下严格领先",
    "B_STRICT": "乙在所有允许情形下严格领先",
    "UNRESOLVED": "无法证明严格领先",
    "UNKNOWN": "证据不足",
}


def _number(value: Fraction) -> str:
    """Render terminating decimals exactly and preserve other values as ratios."""
    numerator, denominator = value.as_integer_ratio()
    rest = denominator
    twos = fives = 0
    while rest % 2 == 0:
        rest //= 2
        twos += 1
    while rest % 5 == 0:
        rest //= 5
        fives += 1
    if rest != 1:
        return str(value)
    places = max(twos, fives)
    if places == 0:
        return str(numerator)
    digits = str(abs(numerator) * (10 ** places // denominator)).zfill(places + 1)
    sign = "-" if numerator < 0 else ""
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


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


def _comparability(ctx: Context) -> dict:
    rows = []
    gaps = []
    details = []
    state = ctx.state
    for objective in ctx.state.objectives:
        horizons = _objective_horizons(ctx.feasible, objective, state)
        for option in ctx.feasible:
            quantity = option.scores.get(objective.id)
            gap = _score_gap(option, objective, state)
            if not gap and len(horizons) > 1:
                gap = "同一目标的方案采用了不同观察时域"
            if gap:
                gaps.append(f"{option.label} · {objective.label}：{gap}。")
                details.append({"option": option.id, "objective": objective.id, "reason": gap})
            rows.append([
                option.label, objective.label, objective.unit,
                "越高越好" if objective.direction == "max" else "越低越好",
                str(quantity.lower) if quantity and quantity.lower is not None else None,
                str(quantity.upper) if quantity and quantity.upper is not None else None,
                _horizon(quantity, state.deadline) if quantity else None,
                quantity.kind if quantity else "unknown", quantity.source if quantity else None,
                gap or "可按该目标比较",
            ])
    summary = ("有些目标的方案得分仍需核对单位、观察时域、来源或上下界。"
               if gaps else "可逐目标比较通过硬约束的方案。")
    if _documented(ctx.state.score_basis):
        summary += f"已记录跨目标的效用刻度依据。{ctx.state.score_basis}"
    else:
        summary += "跨目标加权需要确认共同的基数效用刻度与可补偿性。"
    return {
        "summary": summary,
        "status": "UNKNOWN" if gaps else "COMPARABLE_BY_OBJECTIVE",
        "gaps": gaps,
        "score_gaps": details,
        "tables": [{
            "title": "得分可比性检查",
            "columns": ["方案", "目标", "要求单位", "比较方向", "填报下界", "填报上界",
                        "观察时域", "证据类型", "来源", "结论"],
            "rows": rows,
        }],
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


def _pareto(ctx: Context) -> dict:
    dominated = set()
    comparisons = []
    rows = []
    for a, b in combinations(ctx.feasible, 2):
        relation = _pareto_relation(a, b, ctx.state)
        if relation == "A_DOMINATES":
            dominated.add(b.id)
        elif relation == "B_DOMINATES":
            dominated.add(a.id)
        comparisons.append({"a": a.id, "b": b.id, "relation": relation})
        rows.append([a.label, b.label, _RELATIONS[relation]])
    frontier = [option for option in ctx.feasible if option.id not in dominated]
    unknown = any(pair["relation"] in {"UNKNOWN", "UNRESOLVED"} for pair in comparisons)
    scope = "名义得分" if ctx.state.score_dependence == "shared_additive" else "已列明的得分或区间"
    summary = f"依据{scope}，当前未被证明支配的方案有{'、'.join(option.label for option in frontier)}。"
    if unknown:
        summary += "存在区间重叠或证据缺口，部分比较待定。"
    if ctx.state.score_dependence == "shared_additive":
        summary += "共同校准误差及其变换由联合稳健性方法评估。"
    return {
        "summary": summary,
        "status": "UNKNOWN" if unknown else "PARETO_FRONTIER",
        "frontier": [option.id for option in frontier],
        "pairs": comparisons,
        "tables": [{"title": "逐目标支配关系", "columns": ["甲", "乙", "关系"], "rows": rows}],
    }


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


def _strict_relation(lower: Fraction, upper: Fraction, *, exact: bool = True) -> str:
    if lower > 0:
        return "A_STRICT"
    if upper < 0:
        return "B_STRICT"
    return "UNRESOLVED" if exact else "UNKNOWN"


def _possible_outcomes(lower: Fraction, upper: Fraction) -> list[str]:
    outcomes = []
    if lower < 0:
        outcomes.append("B_LEADS")
    if lower <= 0 <= upper:
        outcomes.append("TIE")
    if upper > 0:
        outcomes.append("A_LEADS")
    return outcomes


def _nominal_condition(objectives, coefficients, *, superior: str) -> tuple[str, dict | None]:
    """Show the sign condition for an affine score difference in the weight simplex."""
    greater = superior == "A"
    if len(objectives) == 2:
        slope = coefficients[0] - coefficients[1]
        if slope != 0:
            threshold = -coefficients[1] / slope
            if 0 <= threshold <= 1:
                symbol = ">" if greater == (slope > 0) else "<"
                return (
                    f"{objectives[0].label}权重 {symbol} {_number(threshold)}",
                    {"objective": objectives[0].id, "value": _number(threshold)},
                )
    symbol = ">" if greater else "<"
    expression = " + ".join(
        f"({_number(coefficient)}) × {objective.label}权重"
        for objective, coefficient in zip(objectives, coefficients, strict=True)
    )
    return f"{expression} {symbol} 0", None


def _aggregate_pairs(
    ctx: Context, comparisons: list[dict], rows: list[list], title: str, columns: list[str], summary: str,
) -> dict:
    wins = {option.id: 0 for option in ctx.feasible}
    charts = []
    labels = {option.id: option.label for option in ctx.feasible}
    for pair in comparisons:
        if pair["relation"] == "A_STRICT":
            wins[pair["a"]] += 1
        elif pair["relation"] == "B_STRICT":
            wins[pair["b"]] += 1
        try:
            lower = float(Fraction(pair["lower"]))
            upper = float(Fraction(pair["upper"]))
        except OverflowError:
            continue
        if isfinite(lower) and isfinite(upper):
            qualifier = "（保守界）" if pair["bounds"] == "outer" else ""
            charts.append({
                "label": f"{labels[pair['a']]} − {labels[pair['b']]}{qualifier}",
                "lower": lower, "upper": upper,
            })
    leaders = [key for key, count in wins.items() if count == len(ctx.feasible) - 1]
    if leaders:
        summary += f"在这些条件下，{labels[leaders[0]]}对所有其他可行方案严格领先。"
    else:
        summary += "当前条件下，没有得到对所有可行替代方案都严格领先的选项。"
    status = "STRICT_LEADER" if leaders else "UNRESOLVED"
    if not leaders and any(pair["relation"] == "UNKNOWN" for pair in comparisons):
        status = "UNKNOWN"
    return {
        "summary": summary,
        "status": status,
        "pairs": comparisons,
        "leaders": leaders,
        "tables": [{"title": title, "columns": columns, "rows": rows}],
        "charts": [{"title": "加权效用差区间（甲减乙）", "unit": ctx.state.objectives[0].unit, "rows": charts}]
        if charts else [],
    }


def _weight_sensitivity(ctx: Context) -> dict:
    objectives = ctx.state.objectives
    bounds = _weight_intervals(ctx.state)
    comparisons = []
    rows = []
    for a, b in combinations(ctx.feasible, 2):
        differences = [_difference(a, b, objective, ctx.state)[0] for objective in objectives]
        lower, min_weights = _extreme(differences, bounds, maximum=False)
        upper, max_weights = _extreme(differences, bounds, maximum=True)
        relation = _strict_relation(lower, upper)
        a_condition, threshold = _nominal_condition(objectives, differences, superior="A")
        b_condition, _ = _nominal_condition(objectives, differences, superior="B")
        pair = {
            "a": a.id, "b": b.id, "lower": _number(lower), "upper": _number(upper),
            "relation": relation, "bounds": "exact",
            "possible_outcomes": _possible_outcomes(lower, upper),
            "minimum": {"weights": _values(objectives, min_weights)},
            "maximum": {"weights": _values(objectives, max_weights)},
            "a_condition": a_condition, "b_condition": b_condition,
        }
        if threshold is not None:
            pair["threshold"] = threshold
        comparisons.append(pair)
        rows.append([
            a.label, b.label, _number(lower), _number(upper), _RELATIONS[relation], a_condition, b_condition,
        ])
    summary = "使用固定的名义得分和用户确认的权重范围。权重和为 1，效用差等于零时为并列。"
    if ctx.state.score_dependence == "shared_additive":
        summary += "名义情形将共同偏移设为零。共同误差下的结论见联合稳健性比较。"
    return _aggregate_pairs(
        ctx, comparisons, rows, "固定得分下的权重敏感性",
        ["甲", "乙", "效用差下界", "效用差上界", "关系", "甲严格领先条件", "乙严格领先条件"],
        summary,
    )


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


def _joint_witness(state: DecisionState, weights: list[Fraction], cells: list[_Cell]) -> dict:
    objectives = state.objectives
    witness = {"weights": _values(objectives, weights)}
    if state.score_dependence == "rectangle" or state.score_transform == "clip_01":
        witness["a_scores"] = _values(objectives, [cell.a_score for cell in cells])
        witness["b_scores"] = _values(objectives, [cell.b_score for cell in cells])
    if state.score_dependence == "shared_additive" and state.score_transform == "clip_01":
        witness["offsets"] = _values(objectives, [cell.offset for cell in cells])
    return witness


def _rectangle_information(a: Option, b: Option, state: DecisionState, bounds, centers, pair: dict) -> str:
    lower, _ = _extreme(centers, bounds, maximum=False)
    upper, _ = _extreme(centers, bounds, maximum=True)
    if lower <= 0 <= upper:
        if lower < 0 < upper:
            pair["information_gap"] = "WEIGHT_CAN_REVERSE_AT_CENTER_SCORES"
            return "即使各得分取区间中点，确认的权重范围仍允许排序反转。"
        pair["information_gap"] = "WEIGHT_PERMITS_TIE_AT_CENTER_SCORES"
        return "即使各得分取区间中点，确认的权重范围仍允许并列。"
    widths = set()
    for option in (a, b):
        for objective in state.objectives:
            lo, hi = _score_bounds(option, objective)
            widths.add(hi - lo)
    if len(widths) == 1 and state.score_transform == "identity":
        ceiling = lower / 2 if lower > 0 else -upper / 2
        label = a.label if lower > 0 else b.label
        pair["score_radius_threshold"] = {
            "preferred": a.id if lower > 0 else b.id,
            "strict_upper": _number(ceiling),
        }
        return f"若各分数仍以区间中点为中心且误差半径相同，半径小于 {_number(ceiling)} 可证明{label}严格领先。"
    return "现有权重范围下，分数区间的端点决定保证领先的条件。"


def _c034(ctx: Context) -> dict:
    state = ctx.state
    bounds = _weight_intervals(state)
    first_lower = max(bounds[0][0], 1 - bounds[1][1])
    first_upper = min(bounds[0][1], 1 - bounds[1][0])
    midpoint = (first_lower + first_upper) / 2
    midpoint_weights = [midpoint, 1 - midpoint]
    rectangle = state.score_dependence == "rectangle"
    clipping = not rectangle and state.score_transform == "clip_01"
    exact = not clipping or state.shared_offset_dependence == "rectangle"
    if rectangle:
        scope = "采用声明可共同实现的矩形得分区间。"
    elif not clipping:
        scope = "相同的未截断加性偏移在每个目标的效用差中抵消。"
    elif exact:
        scope = "在声明可共同实现的偏移区间内检查截断转折点。"
    else:
        scope = "偏移间的联合范围未知，使用边际区间的保守界。保守界与零相交时，排序待定。"

    comparisons = []
    rows = []
    witnesses = []
    gaps = []
    baselines = []
    for a, b in combinations(ctx.feasible, 2):
        minima, maxima = _joint_cells(a, b, state)
        low_coeffs = [cell.difference for cell in minima]
        high_coeffs = [cell.difference for cell in maxima]
        lower, min_weights = _extreme(low_coeffs, bounds, maximum=False)
        upper, max_weights = _extreme(high_coeffs, bounds, maximum=True)
        relation = _strict_relation(lower, upper, exact=exact)
        a_condition, _ = _nominal_condition(state.objectives, low_coeffs, superior="A")
        b_condition, _ = _nominal_condition(state.objectives, high_coeffs, superior="B")
        pair = {
            "a": a.id, "b": b.id, "lower": _number(lower), "upper": _number(upper),
            "relation": relation, "bounds": "exact" if exact else "outer",
            "a_condition": a_condition, "b_condition": b_condition,
        }
        centers = [
            (sum(_nominal_bounds(a, objective, state)) - sum(_nominal_bounds(b, objective, state))) / 2
            for objective in state.objectives
        ]
        baseline_difference = _dot(centers, midpoint_weights)
        pair["nominal_baseline"] = {
            "weights": _values(state.objectives, midpoint_weights),
            "difference": _number(baseline_difference),
        }
        baselines.append([
            a.label, b.label, *(_number(weight) for weight in midpoint_weights), _number(baseline_difference),
        ])
        if exact:
            pair["possible_outcomes"] = _possible_outcomes(lower, upper)
            for key, label, margin, weights, cells in (
                ("minimum", "最小", lower, min_weights, minima),
                ("maximum", "最大", upper, max_weights, maxima),
            ):
                witness = _joint_witness(state, weights, cells)
                pair[key] = witness
                values = [
                    "、".join(f"{obj.label} {witness[field][obj.id]}" for obj in state.objectives)
                    if field in witness else None
                    for field in ("weights", "a_scores", "b_scores", "offsets")
                ]
                witnesses.append([a.label, b.label, label, _number(margin), *values])
        if rectangle:
            info = _rectangle_information(a, b, state, bounds, centers, pair)
        elif clipping and not exact:
            info = "若需判定实际可实现的反转或并列，请核对共同偏移可联合达到的范围。"
        elif clipping:
            info = "严格领先取决于声明的共同偏移范围及权重范围。"
        else:
            info = "缩小共同偏移区间不会改变比较结果。请核对得分差和权重范围。"
        if relation in {"UNKNOWN", "UNRESOLVED"}:
            gaps.append(f"{a.label}与{b.label}的联合稳健性。{info}")
        comparisons.append(pair)
        rows.append([
            a.label, b.label, _number(lower), _number(upper), _RELATIONS[relation],
            a_condition, b_condition, info,
        ])
    heading = "给定权重下的严格领先条件" if exact else "给定权重下严格领先的充分条件"
    result = _aggregate_pairs(
        ctx, comparisons, rows, "权重与得分联合稳健性",
        ["甲", "乙", "效用差下界", "效用差上界", "关系", f"甲{heading}", f"乙{heading}", "条件与信息缺口"],
        f"{scope}效用差等于零时为并列。计算允许权重范围与得分误差集合中的情形任意组合。"
        f"联合误差依据为{state.score_dependence_source}。",
    )
    result["tables"].append({
        "title": "参考比较（可行权重中点与分数中点）" if rectangle
        else "参考比较（可行权重中点与零共同偏移）",
        "columns": ["甲", "乙", *(f"{objective.label}权重" for objective in state.objectives), "效用差"],
        "rows": baselines,
    })
    if witnesses:
        result["tables"].append({
            "title": "达到效用差边界的情形",
            "columns": ["甲", "乙", "边界", "效用差", "权重", "甲得分", "乙得分", "共同偏移"],
            "rows": witnesses,
        })
    if gaps:
        result["gaps"] = gaps
    return result


METHODS = (
    Method(
        model_id="comparability", version="1.0.0", title="目标得分可比性",
        applicability="至少两个通过硬约束筛查的方案，已列明目标方向与单位。",
        inputs=("通过筛查的方案", "目标与单位", "得分区间、证据类型和来源"),
        outputs=("逐方案逐目标的可比性检查", "数据缺口"),
        units="沿用各目标的单位。",
        assumptions="同一目标采用同一观察口径。跨目标加权需额外确认效用刻度。",
        uncertainty="缺失、未知证据或单位不一致均显示待核对。",
        sources=(_C004,),
        failure_conditions="缺少可行方案或目标时无法比较。",
        replay="按目标逐项复核得分区间、单位和来源。",
        baseline="逐一并列查看各目标原始记录。",
        validate=_basic_errors, execute=_comparability,
    ),
    Method(
        model_id="pareto", version="1.0.0", title="Pareto 支配比较",
        applicability="通过硬约束的方案可按各目标独立比较。",
        inputs=("目标方向", "可核对的得分或区间"),
        outputs=("保证支配关系", "未被证明支配的方案集合"),
        units="每个目标沿用自身单位。",
        assumptions="若所有目标均保证不差且至少一个目标保证更好，则形成支配。共同误差使用名义点值进行这一层的比较。",
        uncertainty="得分区间端点用于保守支配判断。重叠或证据缺口可使比较待定。",
        sources=(_C004,),
        failure_conditions="指标口径或单位不一致时，相应比较待定。",
        replay="按目标方向核对两方案的最差和最好得分。",
        baseline="列出各目标上的优劣。",
        validate=_basic_errors, execute=_pareto,
    ),
    Method(
        model_id="weight_sensitivity", version="1.0.0", title="已确认权重的敏感性",
        applicability="用户确认共同基数刻度、补偿和权重含义，比较固定名义分数。",
        inputs=("目标方向和点得分", "用户确认的权重上下界", "共同效用刻度依据"),
        outputs=("精确效用差区间", "严格领先条件", "边界权重组合"),
        units="共同效用单位。",
        assumptions="加权可加，权重非负且和为 1。",
        uncertainty="权重以可行集合表达，得分固定为名义值。",
        sources=(_C004,),
        failure_conditions="未确认权重或共同刻度，权重区间不可行，或得分未知或为区间。",
        replay="按效用差系数顺序将剩余权重分配到上界，复算极值。",
        baseline="在任一确认的单组权重下比较固定得分。",
        validate=_weight_sensitivity_errors, execute=_weight_sensitivity,
    ),
    Method(
        model_id="c034_joint_robustness", version="1.0.0", title="C034 权重与得分联合稳健性",
        applicability="两个越高越好的共同基数效用目标，已确认权重和联合误差结构及变换。",
        inputs=("点得分或矩形区间", "用户确认的权重范围", "误差结构和依据", "得分变换", "共同偏移区间"),
        outputs=("效用差界与严格偏好条件", "可证实的边界情形", "条件性信息缺口"),
        units="共同效用单位。",
        assumptions="权重范围与得分误差集合可任意组合。共同偏移后的得分若截断至 0–1，则检查转折点。"
        "矩形区间使用变换后的效用。",
        uncertainty="外界包含零时，相关信息不足。精确区间包含零时，无法证明任一方严格领先。",
        sources=(_C034, _SHARED, _CLIPPING, _C004),
        failure_conditions="依据不足、变换未知、量尺不可比、权重不可行或误差超出所列模型时，联合证据待定。",
        replay="矩形误差比较对立端点，恒等变换抵消共同偏移，截断检查端点和转折点并对权重取极值。",
        baseline="固定名义得分的权重比较，以及逐目标的 Pareto 比较。",
        validate=_c034_errors, execute=_c034,
    ),
)
