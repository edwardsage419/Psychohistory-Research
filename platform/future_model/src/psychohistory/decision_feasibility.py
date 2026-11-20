"""C028 deterministic closed interval feasibility."""
from collections import defaultdict
import operator

from .decision_registry import Method

GATE_ID = "c028_interval_feasibility"
OPERATORS = {">=": operator.ge, ">": operator.gt, "<=": operator.le, "<": operator.lt}


def check_constraint(constraint, value, deadline):
    if not constraint.source.strip():
        return "UNKNOWN", "请补充硬约束阈值的依据。"
    if value is None or value.kind == "unknown" or value.lower is None or value.upper is None:
        return "UNKNOWN", "请补充有依据的上下界。"
    if not value.source.strip():
        return "UNKNOWN", "请补充区间来源。"
    if value.unit.strip() != constraint.unit.strip():
        return "UNKNOWN", "区间单位与硬约束单位冲突。"
    if (value.horizon or deadline) != (constraint.horizon or deadline):
        return "UNKNOWN", "区间与硬约束的时间范围冲突。"
    meets = OPERATORS[constraint.operator]
    worst, best = (value.lower, value.upper) if constraint.operator.startswith(">") else (value.upper, value.lower)
    if meets(worst, constraint.threshold):
        return "CERTAIN_PASS", "整个闭区间满足阈值。"
    if not meets(best, constraint.threshold):
        return "CERTAIN_FAIL", "整个闭区间违反阈值。"
    return "POSSIBLE", "区间同时包含满足与违反阈值的值。"


def metric_key(constraint, deadline):
    return (constraint.label.strip(), constraint.unit.strip(), constraint.horizon or deadline)


def inconsistent_measurements(state, option):
    metrics = defaultdict(list)
    for constraint in state.constraints:
        value = option.measurements.get(constraint.id)
        status, _ = check_constraint(constraint, value, state.deadline)
        if status != "UNKNOWN":
            metrics[metric_key(constraint, state.deadline)].append(value)
    return {
        key for key, values in metrics.items()
        if max(value.lower for value in values) > min(value.upper for value in values)
    }


def evaluate(context):
    state = context.state
    feasibility = []
    for option in state.options:
        checks = []
        inconsistent = inconsistent_measurements(state, option)
        for constraint in state.constraints:
            value = option.measurements.get(constraint.id)
            status, reason = check_constraint(constraint, value, state.deadline)
            if metric_key(constraint, state.deadline) in inconsistent:
                status, reason = "UNKNOWN", "同指标、同单位及时间范围的区间互相冲突。"
            checks.append(dict(constraint_id=constraint.id, status=status, reason=reason))
        if any(check["status"] == "CERTAIN_FAIL" for check in checks):
            status = "REJECT"
        elif all(check["status"] == "CERTAIN_PASS" for check in checks):
            status = "ACCEPT"
        else:
            status = "UNRESOLVED"
        feasibility.append(dict(option_id=option.id, label=option.label, status=status, checks=checks))
    return {
        "summary": "依据用户确认的底线逐项筛查。只对 ACCEPT 方案执行后续比较。",
        "tables": [{"title": "硬约束筛查", "columns": ["方案", "判定"],
                    "rows": [[item["label"], item["status"]] for item in feasibility]}],
        "charts": [],
        "feasibility": feasibility,
    }


METHOD = Method(
    model_id=GATE_ID,
    version="1.0.0",
    title="C028 区间硬约束",
    applicability="用户确认单调硬约束和有限候选行动。",
    inputs="候选方案、每项硬约束阈值与区间，或用户明确确认无硬约束。",
    outputs="每项 CERTAIN_PASS、CERTAIN_FAIL、POSSIBLE 或 UNKNOWN，及整体可行性。",
    units="阈值与上下界同单位、同时间范围。",
    assumptions="可信闭区间。阈值为单调不等式，多个条件使用逻辑与。",
    uncertainty="逻辑界限，无概率含义。",
    sources=("research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md",),
    failure_conditions="未知边界、单位或时间冲突、来源缺失、未确认底线。",
    replay="tests/test_decision_hub.py 的等号、单位、未知、合取与来源用例。",
    baseline="用区间中点比较阈值，可把跨阈值区间误标为确定可行。",
    validate=lambda context: [] if context.state.constraints_confirmed else ["请确认硬约束。"],
    execute=evaluate,
)
