"""Reviewable natural-language clarification and deterministic decision dispatch."""
from collections import defaultdict
from collections.abc import Sequence
from copy import deepcopy
from hashlib import sha256
import math
import re
from typing import Protocol
from uuid import uuid4

from .contracts import canonical
from .decision_feasibility import GATE_ID, metric_key
from .decision_registry import Context, DecisionRegistry, default_registry
from .decision_state import DecisionState, HUB_VERSION, UnderstandingReceipt


class UnderstandingProvider(Protocol):
    """Trusted in-process adapter. Implementation owns timeout and data handling."""

    provider_id: str
    version: str

    def propose(self, original: str) -> Sequence[dict[str, str]]:
        """Return provisional field/value/source suggestions only."""


PROMPTS = {
    "objectives": "你希望这个选择达成什么？每项目标应改善哪个方向，用什么单位比较？",
    "options": "有哪些可实际采取的行动？请确认方案名称。",
    "deadline": "需要在什么时候决定？没有固定期限时可明确填「无固定期限」。",
    "constraints": "哪些条件一旦越界就必须放弃方案？请确认底线，或明确确认没有硬约束。",
    "confirmed": "请核对原文、方案、目标、期限和底线后确认本版理解。",
}
PROVIDER_FIELDS = frozenset((*PROMPTS, "preferences")) - {"confirmed"}
OPTION_PHRASE = re.compile(r"(?:我该|应该选择|我应该)([^，,。；;？?\n]{1,100})[，,]\s*还是([^。；;？?\n]{1,100})[？?]")


def question_list(state):
    questions = []
    missing = {
        "objectives": not state.objectives,
        "options": len(state.options) < 2,
        "deadline": state.deadline is None,
        "constraints": not state.constraints_confirmed,
        "confirmed": not state.confirmed,
    }
    for field, prompt in PROMPTS.items():
        if missing[field]:
            if field == "options" and any(word in state.question for word in ("岗位", "工作", "职业", "offer")):
                prompt = "目前可选的岗位或行动有哪些？请确认当前选择和可接受的替代方案。"
            questions.append({"field": field, "prompt": prompt})
    return questions


def conflict_questions(state):
    groups = defaultdict(list)
    for constraint in state.constraints:
        groups[metric_key(constraint, state.deadline)].append(constraint)
    problems = []
    for (label, _, _), constraints in groups.items():
        lowers = [(x.threshold, x.operator == ">") for x in constraints if x.operator in (">", ">=")]
        uppers = [(x.threshold, x.operator == "<") for x in constraints if x.operator in ("<", "<=")]
        if lowers and uppers:
            low, low_strict = max(lowers)
            high, high_strict = min(uppers, key=lambda item: (item[0], not item[1]))
            if low > high or (low == high and (low_strict or high_strict)):
                problems.append({"field": "constraints", "prompt": f"「{label}」的硬约束互相冲突，请修订阈值或指标名称。"})
    return problems


def provider_suggestions(provider, original):
    proposals = provider.propose(original)
    if not isinstance(proposals, (list, tuple)) or len(proposals) > 20:
        raise ValueError("Invalid provider proposal")
    for proposal in proposals:
        if not isinstance(proposal, dict) or set(proposal) != {"field", "value", "source"}:
            raise ValueError("Invalid provider proposal")
        if not all(isinstance(value, str) and 0 < len(value.strip()) <= 400 for value in proposal.values()):
            raise ValueError("Invalid provider proposal")
        if proposal["field"] not in PROVIDER_FIELDS:
            raise ValueError("Invalid provider proposal")
    return list(proposals)


def entry(method, status, reasons, result=None):
    return {**method.describe(), "status": status, "reasons": reasons, "result": result}


def valid_result(result, context):
    if not isinstance(result, dict) or not isinstance(result.get("summary"), str):
        raise ValueError("方法结果缺少摘要")
    ids = {option.id for option in context.feasible}
    leaders = result.get("leaders", [])
    if not isinstance(leaders, (list, tuple)) or any(x not in ids for x in leaders):
        raise ValueError("结果包含未通过硬约束的推荐方案")
    gaps = result.get("gaps", [])
    if not isinstance(gaps, (list, tuple)) or any(not isinstance(gap, str) for gap in gaps):
        raise ValueError("方法结果的信息缺口格式无效")
    if not isinstance(result.get("tables", []), (list, tuple)):
        raise ValueError("方法结果表格式不符")
    for table in result.get("tables", []):
        if not isinstance(table["title"], str) or not all(isinstance(x, str) for x in table["columns"]):
            raise ValueError("方法结果表格式不符")
        for row in table["rows"]:
            if len(row) != len(table["columns"]) or any(
                type(item) not in (str, int, float, bool, type(None)) for item in row
            ):
                raise ValueError("方法结果表格列数或值有误")
    if not isinstance(result.get("charts", []), (list, tuple)):
        raise ValueError("方法图表格式不符")
    for chart in result.get("charts", []):
        if not isinstance(chart["title"], str) or not isinstance(chart["unit"], str):
            raise ValueError("方法图表格式不符")
        for row in chart["rows"]:
            lower, upper = float(row["lower"]), float(row["upper"])
            if not isinstance(row["label"], str) or not all(map(math.isfinite, (lower, upper))) or lower > upper:
                raise ValueError("方法结果图表范围无效")
    canonical(result)
    return result


def validate_gate(result, state):
    options = {item.id: item.label for item in state.options}
    constraints = {item.id for item in state.constraints}
    rows = result["feasibility"]
    if not isinstance(rows, list) or len(rows) != len(options):
        raise ValueError("硬约束结果未覆盖所有方案")
    for row in rows:
        if options.pop(row["option_id"]) != row["label"]:
            raise ValueError("硬约束方案身份不一致")
        checks = row["checks"]
        if len(checks) != len(constraints) or {c["constraint_id"] for c in checks} != constraints:
            raise ValueError("硬约束结果未覆盖所有条件")
        statuses = {c["status"] for c in checks}
        if statuses - {"CERTAIN_FAIL", "CERTAIN_PASS", "POSSIBLE", "UNKNOWN"}:
            raise ValueError("无效的单项硬约束状态")
        if any(not isinstance(c["reason"], str) or not c["reason"].strip() for c in checks):
            raise ValueError("硬约束结果缺少理由")
        if "CERTAIN_FAIL" in statuses:
            expected = "REJECT"
        elif statuses <= {"CERTAIN_PASS"}:
            expected = "ACCEPT"
        else:
            expected = "UNRESOLVED"
        if row["status"] != expected:
            raise ValueError("硬约束结果与逐项状态冲突")


def run_method(method, context):
    try:
        reasons = method.validate(deepcopy(context))
        if not isinstance(reasons, list) or any(not isinstance(reason, str) for reason in reasons):
            raise ValueError("无效的方法适用条件结果")
        if reasons:
            return entry(method, "INELIGIBLE", reasons)
        result = valid_result(method.execute(deepcopy(context)), context)
        if method.model_id == GATE_ID:
            validate_gate(result, context.state)
        return entry(method, "EXECUTED", ["本次输入满足方法声明的适用条件。"], result)
    except Exception:
        return entry(method, "FAILED", ["方法执行或输出校验失败。此方法的结果已隔离。"])


class DecisionHub:
    def __init__(self, registry: DecisionRegistry | None = None, provider: UnderstandingProvider | None = None):
        self.registry = registry if registry is not None else default_registry()
        self.gate = self.registry.get(GATE_ID, "1.0.0")
        self.provider = provider

    def start(self, original: str, *, allow_provider: bool = False):
        state = DecisionState(decision_id=uuid4().hex, revision=1, question=original)
        mode = "GUIDED_CONFIRMATION"
        message = "使用有针对性的澄清问题和明确措辞的原文片段。所有理解均需用户确认。"
        match = OPTION_PHRASE.search(original)
        suggestions = [{"field": "options", "value": x.strip(), "source": "原文片段"}
                       for x in match.groups() if x.strip()] if match else []
        provider_id = provider_version = None
        if allow_provider and self.provider is not None:
            try:
                proposals = provider_suggestions(self.provider, original)
                provider_id = self.provider.provider_id
                provider_version = self.provider.version
                if not all(isinstance(x, str) and 0 < len(x.strip()) <= 400
                           for x in (provider_id, provider_version)):
                    raise ValueError("Invalid provider identity")
                suggestions.extend(proposals)
                mode = "PROVISIONAL_PROVIDER"
                message = "已返回待确认的适配器建议。"
            except Exception:
                provider_id = provider_version = None
                mode = "PROVIDER_FAILED"
                message = "理解适配器失败，已继续使用确定性澄清。"
        state.understanding_receipt = UnderstandingReceipt(
            mode=mode, provider_id=provider_id, provider_version=provider_version, suggestions=suggestions,
        )
        return {
            "state": state.model_dump(mode="json"),
            "questions": question_list(state),
            "understanding": {"mode": mode, "message": message, "suggestions": suggestions},
        }

    def analyze(self, state: DecisionState | dict):
        state = DecisionState.model_validate(state)
        input_hash = sha256(canonical(state.model_dump(mode="json")).encode()).hexdigest()
        questions = [*question_list(state), *conflict_questions(state)]
        base = dict(decision_id=state.decision_id, revision=state.revision, input_hash=input_hash,
                    hub_version=HUB_VERSION, questions=questions)
        methods = self.registry.methods()
        if questions:
            attempted = [entry(method, "INELIGIBLE", ["先完成问题理解确认及输入修订。"])
                         for method in methods]
            return self._response(base, "CLARIFY", [], attempted, ["请先完成澄清。"], [],
                                  [q["prompt"] for q in questions])

        gate = run_method(self.gate, Context(state))
        feasibility = gate["result"]["feasibility"] if gate["status"] == "EXECUTED" else []
        accepted = {item["option_id"] for item in feasibility if item["status"] == "ACCEPT"}
        context = Context(state, tuple(o for o in state.options if o.id in accepted))
        attempted = [gate]
        for method in methods:
            if method.model_id == GATE_ID:
                continue
            attempted.append(
                run_method(method, context) if context.feasible else
                entry(method, "INELIGIBLE", ["当前没有经硬约束证实可行的方案。"])
            )

        gaps, risks, advice = [], [], []
        conditional_scope = any(item["status"] == "UNRESOLVED" for item in feasibility)
        if conditional_scope:
            risks.append("仍有可行性未决的方案。任何比较仅适用于当前 ACCEPT 集。")
        labels = {item.id: item.label for item in context.feasible}
        constraints = {item.id: item.label for item in state.constraints}
        for item in feasibility:
            for check in item["checks"]:
                if check["status"] in {"POSSIBLE", "UNKNOWN"}:
                    gaps.append(f'{item["label"]} · {constraints[check["constraint_id"]]}：{check["reason"]}')
        outcomes = []
        leaders_by_method = []
        for method in attempted:
            if method["status"] != "EXECUTED":
                gaps.extend(method["reasons"])
                continue
            result = method["result"]
            if method["model_id"] not in {GATE_ID, "comparability"}:
                outcomes.append(result)
            for gap in result.get("gaps", []):
                gaps.append(str(gap))
            leaders = result.get("leaders", [])
            if leaders:
                leaders_by_method.append(frozenset(leaders))
                names = "、".join(labels[key] for key in leaders)
                advice.append(f'{method["title"]} 的条件性结果：{names}。{result["summary"]}')
        if len(set(leaders_by_method)) > 1:
            risks.append("适用方法给出不同的优选集合。请检查各规则的适用条件和取舍。")
        if not advice:
            if not context.feasible:
                advice.append("当前没有可证实的可行方案。请优先核实上述底线及其来源。")
            elif len(context.feasible) == 1:
                advice.append("当前仅一个方案通过底线；可在核实未决条件后再比较。")
            else:
                advice.append("当前信息不足以确定严格排序。请参照各方法的比较范围及待补信息。")
        if state.scenarios:
            risks.append("情景结论依赖所列情景和效用尺度；情景集合可能仍有遗漏。")
        status = "ANALYZED" if outcomes else "UNRESOLVED"
        return self._response(base, status, feasibility, attempted, advice, risks, gaps, conditional_scope)

    @staticmethod
    def _response(base, status, feasibility, methods, advice, risks, gaps, conditional_scope=False):
        trace = [{"phase": "CONFIRMATION", "status": "PENDING" if status == "CLARIFY" else "CONFIRMED"}]
        trace.extend({"phase": "METHOD", "model_id": item["model_id"], "version": item["version"],
                      "status": item["status"], "reasons": item["reasons"]} for item in methods)
        ordered_gaps = list(dict.fromkeys(gaps))
        return dict(base, status=status, feasibility=feasibility, methods=methods, advice=advice,
                    risks=risks, gaps=ordered_gaps, priority_gap=ordered_gaps[0] if ordered_gaps else None,
                    conditional_scope=conditional_scope, trace=trace)
