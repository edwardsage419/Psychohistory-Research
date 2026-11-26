"""Backward evidence planning for the explicit decision goals in research round 67."""
from functools import lru_cache
import re
import unicodedata

from .decision_v05 import v05_registry


GOALS = {
    "判断方案是否违反底线": "c028_interval_feasibility@1.0.0",
    "比较各目标的优势": "pareto@1.0.0",
    "判断权重改变是否影响选择": "weight_sensitivity@1.0.0",
    "比较最坏情景的后悔值": "C029@1.0.0",
    "比较现在行动和等待": "timing_actions@1.0.0",
}

TASKS = {
    "scope": ("USER_CONFIRM", "确认分析目标和当前可采取的行动。", ()),
    "reviewSources": ("RESEARCH_REVIEW", "复审登记方法所用来源的版本和适用边界。", ()),
    "confirmConstraints": ("USER_CONFIRM", "确认每条底线、口径和阈值，或明确确认没有底线。", ("scope",)),
    "measurements": (
        "QUALIFIED_EVIDENCE", "按方案核对底线指标的实际值或可信区间、来源、主体、单位和周期。",
        ("confirmConstraints",),
    ),
    "gateReceipt": (
        "INTERNAL_NATIVE_GATE", "在当前版本计算硬约束，并保留未知和不合格方案。", ("measurements",),
    ),
    "objectives": ("USER_CONFIRM", "确认要比较的维度、方向、单位和时间口径。", ("scope",)),
    "scores": (
        "QUALIFIED_EVIDENCE", "核对通过底线的方案在各维度的可比较观测值或区间。", ("gateReceipt", "objectives"),
    ),
    "pointScores": ("QUALIFIED_EVIDENCE", "核对同一尺度上有依据的点值得分。", ("scores",)),
    "scale": ("USER_CONFIRM", "确认跨目标共同效用标尺及其可比性。", ("objectives",)),
    "weights": ("USER_CONFIRM", "由使用者提供各目标权重及拟考察的取值。", ("scale",)),
    "scenarios": ("SCENARIO_DEFINITION_AND_EVIDENCE", "定义待比较情景，注明各情景的证据或假设。", ("scope",)),
    "regretBasis": ("USER_CONFIRM", "确认跨方案、跨情景的共同效用与后悔值口径。", ("scope",)),
    "utilities": (
        "QUALIFIED_EVIDENCE", "核对每个合格方案在每种情景下的同量纲效用点值或明确的情景假设。",
        ("gateReceipt", "scenarios", "regretBasis"),
    ),
    "timing": (
        "QUALIFIED_EVIDENCE", "核对共同起点、截止和可执行窗口，以及实际换转成本和各情景的延迟损失。",
        ("scope", "reviewSources"),
    ),
}
REQUIREMENTS = {
    "c028_interval_feasibility@1.0.0": ("scope", "confirmConstraints", "measurements"),
    "pareto@1.0.0": ("scope", "confirmConstraints", "measurements", "gateReceipt", "objectives", "scores"),
    "weight_sensitivity@1.0.0": (
        "scope", "confirmConstraints", "measurements", "gateReceipt", "objectives", "scores",
        "pointScores", "scale", "weights",
    ),
    "C029@1.0.0": (
        "scope", "confirmConstraints", "measurements", "gateReceipt", "scenarios", "regretBasis", "utilities",
    ),
    "timing_actions@1.0.0": (
        "reviewSources", "scope", "confirmConstraints", "measurements", "gateReceipt", "scenarios",
        "regretBasis", "utilities", "timing",
    ),
}


@lru_cache(maxsize=1)
def _methods():
    return {method.key: method for method in v05_registry().methods()}


def _task(task_id):
    category, description, dependencies = TASKS[task_id]
    result = {"id": task_id, "category": category, "description": description, "after": list(dependencies)}
    if task_id == "measurements":
        result["condition"] = "仅在存在已确认底线时需要测量。"
    return result


def discover(goal, index, *, limit):
    search = index.search(goal, limit=limit)
    # Full-clause match keeps negations, quotations, and incidental mentions out of method selection.
    clauses = re.split(r"[。;!?\n]+", unicodedata.normalize("NFKC", goal))
    requested = dict.fromkeys(GOALS[clause.strip()] for clause in clauses if clause.strip() in GOALS)
    methods = []
    registry = _methods()
    for key in requested:
        method = registry.get(key)
        if method is None:
            methods.append({"method": key, "status": "NATIVE_UNAVAILABLE", "authority": "NONE"})
            continue
        source_status, sources = index.method_sources(method)
        review = source_status == "REVIEW_REQUIRED"
        requirements = list(REQUIREMENTS[key])
        if review and "reviewSources" not in requirements:
            requirements.insert(0, "reviewSources")
        methods.append({
            "method": key, "title": method.title, "registry": method.describe(),
            "status": "REVIEW_REQUIRED" if review else "NEEDS_SCOPE",
            "source_status": source_status, "sources": sources,
            "frontier": [_task("reviewSources" if review else "scope")],
            "requirements": [_task(task) for task in requirements], "authority": "NONE",
        })
    return {
        "status": "CANDIDATE" if methods else "NO_SUPPORTED_EXPLICIT_GOAL",
        "coverage": "BOUNDED_EXPLICIT_GOALS", "authority": "NONE", "methods": methods, "search": search,
    }
