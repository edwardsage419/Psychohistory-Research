"""Deterministic next questions over the current decision and method audit."""

from collections.abc import Mapping
from fractions import Fraction
import re


_CLARIFY = {
    "options": "目前有哪些可实际采取的行动？",
    "objectives": "你想达成什么？哪些结果最能区分这些行动？",
    "deadline": "何时必须作出决定？没有固定期限时可以明确说明。",
    "constraints": "哪些条件一旦越界就必须放弃行动？也可以明确确认没有硬约束。",
    "confirmed": "请核对问题、行动、目标、时限和底线。",
}
_DOMAIN_HINTS = (
    ("CAREER", r"工作|岗位|职业|跳槽|工作邀请|\b(?:jobs?|career|offers?)\b",
     "核对工作内容、合同条件和机会是否仍然可用。"),
    ("LEARNING", r"学习|课程|培训|升学|\b(?:education|courses?|studying|training)\b",
     "可以核对参与条件、时间投入和预期学习成果。"),
    ("TRAVEL", r"出行|旅行|交通|火车|航班|\b(?:travel|flights?|commute|trains?)\b",
     "可以核对总费用、门到门时间和可变更条件。"),
    ("HOUSEHOLD", r"租房|搬家|住房|\b(?:rent|housing|apartment|relocat\w*)\b",
     "可以核对居住条件、完整支出和变更成本。"),
    ("HEALTH", r"就医|健康|治疗|\b(?:health|treatment|medical)\b",
     "可以核对专业意见、适用人群和你在意的结果差异。"),
    ("FINANCE", r"投资|理财|贷款|保险|\b(?:invest\w*|finance|loan|insurance)\b",
     "可以核对支付边界、费用和资金可用时点。"),
)
_INFORMATION_CUES = r"打听|调查|反馈|收集信息|获取信息|多了解|问清|核实后|\b(?:survey|feedback|research|investigat\w*|consult|verify)\b"
_WAIT_CUES = r"等待|等.{0,12}再|延期|推迟|\b(?:wait\w*|delay\w*|postpon\w*)\b"
_TIMING_CUES = _WAIT_CUES + r"|过期|截止|到期|失效|名额|只保留|\b(?:deadlines?|expir\w*)\b"
_PRIORITY = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "DEFERRED": 3}
_SENSITIVITY_FIELDS = {
    "weight_sensitivity": "weights",
    "c034_joint_robustness": "score_dependence",
}


def _item(category, action, priority, prompt, reason, field, *,
          evidence_status="UNKNOWN", proof=None, **target):
    identity = ":".join((category.lower(), field, *target.values()))
    item = {
        "id": identity,
        "category": category,
        "action": action,
        "priority": priority,
        "prompt": prompt,
        "reason": reason,
        "target": {"field": field, **target},
        "evidence_status": evidence_status,
    }
    if proof is not None:
        item["proof"] = proof
    return item


def _clarification(state, analysis):
    missing = {
        "options": len(state.get("options", ())) < 2,
        "objectives": not state.get("objectives"),
        "deadline": not state.get("deadline"),
        "constraints": not state.get("constraints_confirmed"),
        "confirmed": not state.get("confirmed"),
    }
    explicit = {question["field"]: question["prompt"] for question in analysis.get("questions", ())}
    for field, default in _CLARIFY.items():
        if missing[field] or (field == "constraints" and field in explicit):
            yield _item("CLARIFICATION", "ASK", "HIGH", explicit.get(field, default),
                        "此回答用于确认本次选择的比较范围。", field)


def _labels(state, field):
    return {entry["id"]: entry.get("label", entry["id"]) for entry in state.get(field, ())}


def _feasibility(state, analysis):
    constraints = _labels(state, "constraints")
    for row in analysis.get("feasibility", ()):
        option_id = row["option_id"]
        witness = next((check["constraint_id"] for check in row["checks"]
                        if check["status"] == "CERTAIN_FAIL"), None)
        for check in row["checks"]:
            if check["status"] not in {"UNKNOWN", "POSSIBLE"}:
                continue
            constraint_id = check["constraint_id"]
            label = f'{row["label"]} · {constraints.get(constraint_id, constraint_id)}'
            target = {"option_id": option_id, "constraint_id": constraint_id}
            if row["status"] == "REJECT" and witness is not None:
                proof = {"scope": "CURRENT_FEASIBILITY_GATE", "witness_constraint_id": witness}
                reason = f"在当前底线和证据下，「{constraints.get(witness, witness)}」已确定不通过。仅补齐此项仍会排除该方案。"
                yield _item("FEASIBILITY", "DEFER", "DEFERRED", f"暂缓核实 {label}。",
                            reason, "measurements", evidence_status="LOGICAL_INVARIANT", proof=proof, **target)
            else:
                reason = f'{check["reason"]} 核实此项可能改变方案能否进入可行集。'
                yield _item("FEASIBILITY", "VERIFY", "HIGH", f"核实 {label} 的区间、单位及依据。",
                            reason, "measurements", **target)


def _comparison(state, executed):
    options = _labels(state, "options")
    objectives = _labels(state, "objectives")
    for method in executed:
        model_id = method["model_id"]
        result = method.get("result") or {}
        if model_id == "comparability":
            for gap in result.get("score_gaps", ()):
                option, objective = gap["option"], gap["objective"]
                label = f"{options.get(option, option)} · {objectives.get(objective, objective)}"
                yield _item("COMPARABILITY", "VERIFY", "MEDIUM", f"核对 {label} 的可比测量。",
                            f'{gap["reason"]}；该差异可能影响当前可行方案的比较。',
                            "scores", option_id=option, objective_id=objective)
        if model_id == "pareto" and not (state.get("weights_confirmed") or state.get("preferences")) and any(
            pair["relation"] == "INCOMPARABLE" for pair in result.get("pairs", ())
        ):
            yield _item("SENSITIVITY", "ASK", "MEDIUM", "确认面对此取舍时，哪些结果更重要。",
                        "可行方案各有明确优势。可以说明优先顺序，也可以确认用于比较的权重范围。",
                        "weights", evidence_status="CONDITIONAL", model_id=model_id)
        field = _SENSITIVITY_FIELDS.get(model_id)
        if field is None:
            continue
        for pair in result.get("pairs", ()):
            lower, upper = str(pair["lower"]), str(pair["upper"])
            if not Fraction(lower) < 0 < Fraction(upper):
                continue
            option, rival = pair["a"], pair["b"]
            exact = pair.get("bounds") == "exact"
            proof = {
                "scope": "CURRENT_MODEL_AND_FEASIBLE_SET", "bounds": pair["bounds"],
                "lower": lower, "upper": upper,
            }
            variability = "可行边界包含两种排序。" if exact else "外界跨过零，现有边界无法判定是否存在排序反转。"
            prompt = f"复核 {options.get(option, option)} 与 {options.get(rival, rival)} 的敏感条件。"
            yield _item("SENSITIVITY", "COMPARE", "MEDIUM", prompt, variability, field,
                        evidence_status="CONDITIONAL", proof=proof, model_id=model_id,
                        option_id=option, rival_option_id=rival)


def _model_disagreements(executed):
    leaders_by_model = {}
    information_decisions = {}
    for method in executed:
        result = method.get("result") or {}
        model_id = method["model_id"]
        leaders = result.get("leaders", ())
        maximin = result.get("maximin_leaders", ())
        if leaders:
            leaders_by_model[model_id] = frozenset(leaders)
        if model_id.startswith("voi_") and "decision" in result:
            information_decisions[model_id] = result["decision"]
        if leaders and maximin and frozenset(maximin) != frozenset(leaders):
            yield _item("MODEL_ASSUMPTIONS", "COMPARE", "MEDIUM", "比较最坏后悔值与最坏效用的取舍。",
                        "这两条规则在当前同一情景表上给出不同结果；规则选择取决于你希望防范什么。",
                        "scenarios", evidence_status="CONDITIONAL", model_id=model_id)
    if len(set(leaders_by_model.values())) > 1:
        yield _item("MODEL_ASSUMPTIONS", "COMPARE", "MEDIUM", "核对不同方法的优选条件与假设。",
                    "各自的优选集合不同。确认比较范围、效用含义和决策规则后再作取舍。",
                    "methods", evidence_status="CONDITIONAL",
                    proof={"scope": "CURRENT_MODELS_AND_FEASIBLE_SET", "model_ids": list(leaders_by_model)})
    if len(set(information_decisions.values())) > 1:
        yield _item("MODEL_ASSUMPTIONS", "COMPARE", "MEDIUM", "核对在什么条件下能根据调查结果改选。",
                    "不同信息规则得到的调查结论有分歧。请区分可以重新优化、必须预先承诺和侧重保护最坏结果的定义。",
                    "information", evidence_status="CONDITIONAL",
                    proof={"scope": "CURRENT_MODELS_AND_FEASIBLE_SET", "model_ids": list(information_decisions)})


def _documented(value):
    return bool(value and value.get("kind") not in {None, "unknown"}
                and str(value.get("source") or "").strip())


def _bounded(value):
    return _documented(value) and value.get("lower") is not None and value.get("upper") is not None


def _evidence(state):
    for evidence in state.get("evidence", ()):
        if (evidence.get("verification") == "unverified" or evidence.get("kind") == "unknown"
                or not (evidence.get("source") or "").strip() or not (evidence.get("scope") or "").strip()):
            yield _item("EVIDENCE", "VERIFY", "MEDIUM", f'核实「{evidence["label"]}」的来源和适用范围。',
                        "记录仍有证据缺口。补齐后才能把它用于相应的事实或模型输入。",
                        "evidence", evidence_id=evidence["id"])


def _scenario_evidence(state, analysis):
    scenarios = state.get("scenarios", ())
    temporal = analysis.get("temporal_scope", {})
    accepted = [row for row in analysis.get("feasibility", ())
                if row["status"] == "ACCEPT" and temporal.get(row["option_id"], "FEASIBLE") == "FEASIBLE"]
    if not scenarios or len(accepted) < 2:
        return
    if not state.get("scenario_basis"):
        yield _item("EVIDENCE", "VERIFY", "MEDIUM", "确认各情景的效用尺度和观察时段。",
                    "只有可比的效用才能用于情景后悔值比较。", "scenarios", part="scenario_basis")
    for scenario in scenarios:
        scenario_id = scenario["id"]
        label = scenario.get("label", scenario_id)
        if not _documented(scenario):
            yield _item("EVIDENCE", "VERIFY", "MEDIUM", f"核实「{label}」的来源和情景定义。",
                        "只有明确的情景才可以用作分析输入。", "scenarios", scenario_id=scenario_id)
        utilities = scenario.get("utilities", {})
        for option in accepted:
            option_id = option["option_id"]
            if not _bounded(utilities.get(option_id)):
                yield _item("EVIDENCE", "VERIFY", "MEDIUM", f'核实「{option["label"]}」在「{label}」中的效用区间。',
                            "这项缺口会影响已通过底线的方案在该情景中的比较。",
                            "scenarios", scenario_id=scenario_id, option_id=option_id)


def _information(state, text, methods):
    info = state.get("information") or {}
    signals = _labels(info, "signals")
    requested = state.get("information") is not None or re.search(_INFORMATION_CUES, text, re.I)
    if not requested or any(method["model_id"].startswith("voi_") and method["status"] == "EXECUTED"
                            for method in methods):
        return
    investigation = (state.get("timing") or {}).get("investigation")
    timed = investigation and not info.get("timing_basis")
    if timed and investigation.get("mode") == "joint":
        return
    scenarios = _labels(state, "scenarios")
    prior, likelihoods = info.get("prior") or {}, info.get("likelihoods") or {}
    action_sets = info.get("actions_by_signal") or {}
    missing = [
        ("signals", not signals, "明确准备查什么，以及不同调查结果可能是什么。"),
        ("scenarios", not scenarios, "列出信号所指向的不同情景及相同尺度的效用。"),
        ("prior", any(not _bounded(prior.get(key)) for key in scenarios), "核对各情景概率的来源和上下界。"),
        ("likelihoods", any(not _bounded((likelihoods.get(key) or {}).get(signal))
                            for key in scenarios for signal in signals), "核对各情景下调查结果的可靠性与来源。"),
        ("cost", not timed and not _bounded(info.get("cost")), "核对获取信息的成本及其效用单位。"),
        ("actions_by_signal", not timed and not (info.get("unrestricted_actions") and info.get("action_source"))
         and any(not _documented(action_sets.get(signal)) for signal in signals),
         "核对得到各项结果后仍能采取哪些行动。"),
        ("timing_basis", not timed and not info.get("timing_basis"),
         "核对结果能否在行动机会关闭前到达。"),
    ]
    for part, required, prompt in missing:
        if required:
            yield _item("EVIDENCE", "VERIFY", "MEDIUM", prompt,
                        "这些信息用于判断是否具备比较调查与立即行动的条件。当前仅提供补证次序。",
                        "information", part=part)
            return
    if not timed and any(method["model_id"].startswith("voi_") for method in methods):
        yield _item("EVIDENCE", "VERIFY", "MEDIUM", "复核信息模型的概率、行动和证据条件。",
                    "已有输入尚未通过信息价值方法的适用性检查。请查看该方法的审计理由。",
                    "information", part="admission")


def _timing(state, text, executed):
    timing = state.get("timing") or {}
    active = state.get("timing") is not None
    if not active and not re.search(_TIMING_CUES, text, re.I):
        return
    if not timing.get("confirmed"):
        yield _item("TIMING", "VERIFY", "MEDIUM", "核对决定、等待和实际行动的时间界限。",
                    "等待可能改变可采取的行动。应先确认截止时间、信息到达或已有行动的到期条件。", "timing")
        return
    if not timing.get("time_unit") or not timing.get("time_origin"):
        yield _item("TIMING", "VERIFY", "MEDIUM", "核对比较时机所用的时间单位和起点。",
                    "统一参照后才能检查行动截止和信息到达的先后。", "timing", part="time_origin")
        return
    if not _documented(timing.get("horizon")):
        yield _item("TIMING", "VERIFY", "MEDIUM", "核对时间模型评估到何时，并记录来源。",
                    "当前缺少比较立即行动和等待结果的共同时间边界。", "timing", part="horizon")
        return
    if re.search(_WAIT_CUES, text, re.I) and not (
        _bounded(timing.get("wait_duration")) or timing.get("investigation")
    ):
        yield _item("TIMING", "VERIFY", "MEDIUM", "核对预计要等多久，以及等待后仍可行动的机会。",
                    "同一个截止日下，信息到达或等待结束的时间会改变可行的行动。", "timing",
                    part="wait_duration")
    action_result = next((method["result"] for method in executed if method["model_id"] == "timing_actions"), {})
    strategies = action_result.get("strategies", ())
    if any(row["status"] == "EXPIRED" for row in strategies):
        yield _item("TIMING", "COMPARE", "HIGH", "比较等待后仍可采取的行动与到期的机会。",
                    "部分策略在所列时间条件下越过了行动边界。", "timing",
                    evidence_status="CONDITIONAL", part="actions")
    if any(row["status"] == "UNKNOWN" for row in strategies):
        yield _item("TIMING", "VERIFY", "HIGH", "核实受影响策略的行动窗口和实际成本。",
                    "时间规则、效用或成本的依据尚未确定，详细原因见时机审计。", "timing", part="availability")
    times = action_result.get("time_inputs") or {}
    relations = [
        (times.get("prediction_vs_deadline"), "决策截止点", {"boundary": "decision_deadline"}),
        (times.get("prediction_vs_horizon"), "观察期限", {"boundary": "horizon"}),
    ]
    labels = _labels(state, "options")
    relations.extend((relation, f"「{labels.get(option, option)}」的截止点", {"option_id": option})
                     for option, relation in times.get("prediction_vs_action_cutoffs", {}).items())
    for relation, cutoff, target in relations:
        if relation not in {"AFTER", "STRADDLES"}:
            continue
        crosses = relation == "STRADDLES"
        reason = f"预测区间跨过{cutoff}，赶上截止的情形仍未确定。" if crosses else f"当前预测区间已越过{cutoff}。"
        yield _item("TIMING", "VERIFY" if crosses else "COMPARE", "HIGH", f"核对预测完成时间和{cutoff}。",
                    reason, "timing", evidence_status="CONDITIONAL", part="predicted_completion",
                    proof={"scope": "CURRENT_TIMING_ASSUMPTIONS", "relation": relation}, **target)


def _stage(items, ready):
    if any(item["action"] in {"ASK", "VERIFY"} for item in items):
        return "NEEDS_INPUT"
    return "READY" if ready else "PENDING"


def plan(state, analysis):
    """Suggest the next prerequisite or comparison without imputing any input."""
    if not isinstance(state, Mapping):
        state = state.model_dump(mode="json")
    confirmed_intent = state.get("intent") if state.get("confirmed") else None
    text = " ".join(filter(None, (state.get("question"), state.get("intent"))))
    hints = [{"domain": domain, "prompt": prompt, "evidence_status": "PROVISIONAL_HINT"}
             for domain, pattern, prompt in _DOMAIN_HINTS if re.search(pattern, text, re.I)]
    methods = analysis.get("methods", ())
    executed = [method for method in methods if method["status"] == "EXECUTED"]
    clarification = list(_clarification(state, analysis))
    feasibility = list(_feasibility(state, analysis))
    comparison = [*_comparison(state, executed), *_model_disagreements(executed)]
    evidence = [*_evidence(state), *_scenario_evidence(state, analysis), *_information(state, text, methods)]
    timing = list(_timing(state, text, executed))
    items = sorted([*clarification, *feasibility, *comparison, *evidence, *timing],
                   key=lambda item: _PRIORITY[item["priority"]])
    steps = [
        ("UNDERSTAND", "NEEDS_INPUT" if clarification else "READY"),
        ("FEASIBILITY", _stage(feasibility, analysis.get("feasibility"))),
        ("COMPARE", _stage([*comparison, *evidence], any(
            not method["model_id"].startswith(("c028_", "timing_")) for method in executed))),
        ("TIMING", _stage(timing, any(method["model_id"].startswith("timing_") for method in executed))),
        ("REVIEW", "PENDING"),
    ]
    return {
        "steps": [{"stage": stage, "status": status} for stage, status in steps],
        "items": items,
        "can_run": [{"model_id": method["model_id"], "title": method["title"]} for method in executed],
        "intent": {"description": confirmed_intent, "hints": hints},
    }
