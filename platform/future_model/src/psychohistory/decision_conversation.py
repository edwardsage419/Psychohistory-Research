"""Temporary, revision-bound conversations over the v0.5 decision engine."""
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
import re
from threading import RLock
from time import monotonic
from uuid import uuid4
from unicodedata import normalize

from .decision_conversation_math import BOUNDS, build_state, evidence_number
from .decision_evidence import EvidenceLedger, PurposeConsent, confirm_claim, draft_claims
from .decision_language import interpret
from .decision_local_ai import ConversationOllama
from .decision_v05 import DecisionHubV05, DecisionStateV05

VERSION = "0.6.0"
MAX_SESSIONS = 48
SESSION_TTL = 45 * 60
MAX_TURNS = 20
COUPLED = re.compile(r"(?:共用|共享|合计|合在一起|加在一起).{0,12}(?:预算|上限|总额|容量)|(?:共同上限|联合约束)")
DEFAULT_OPTIONS = {
    "career": ("留在现有岗位", "考虑新的岗位"),
    "housing": ("继续租住", "考虑买房"),
    "learning": ("现在投入学习", "先保留时间和资金"),
    "budget": ("现在支出", "暂时保留预算"),
    "life": ("保留现有安排", "先做一个可撤回的小调整"),
    "moving": ("留在目前地点", "考虑搬到新地点"),
    "risk": ("现在决定", "先核实关键信息"),
}
FRAMING = {
    "career": ("先看两份安排是否都符合你的底线，再比较各自的长期取舍。",
               "到岗地点和时间会影响日常负担。", "收入、成长机会和失去现状后的代价可以分开看。",
               "当前选择里，有什么条件是你一定不能接受的？"),
    "housing": ("先用同一段居住时间比较，再决定该核对哪些真实费用。",
                "租住保留搬迁灵活性。", "买房还要考虑购入、持续持有和退出的成本。",
                "你大概需要在这个地方住多久？"),
    "learning": ("先看这次投入能否换来你实际想获得的能力。",
                 "现在学习能更早开始，但会占用时间和资金。", "等待可以保留资源，也可能错过机会。",
                 "这次投入最希望帮你实现什么？"),
    "budget": ("先分开必须保留的钱和可以调整的未来支出。",
               "立即投入会减少可用资金。", "保留预算有灵活性，等待也可能有代价。",
               "你最多愿意投入多少资金？"),
    "life": ("可以先比较维持现状和一个容易撤回的小调整。",
             "维持现状也会产生后果。", "小幅试行便于观察变化和回退。",
             "现在的生活中，你最想先改变哪一件事？"),
    "moving": ("先确认哪些地点和通勤安排实际能接受。",
               "留在原地可避免搬迁成本。", "搬迁可能带来新机会，也会改变可支配时间和生活条件。",
               "有哪些地点限制是必须遵守的？"),
    "risk": ("已有文字能帮助整理情景，现实发生概率仍需有依据。",
             "先比较不同情景发生时各方案的后果。", "进一步核实可能影响是否值得等待。",
             "哪一种结果最难接受？"),
}
GENERAL = ("先找出具体的选择和最不能接受的结果，再比较。",
           "维持现状有自己的成本和收益。", "改变前可以核对代价和是否容易回退。",
           "你现在实际在考虑哪一个选择？")
QUESTIONS = {
    "cost": "这个方案未来还要花多少钱？已经花掉且拿不回来的部分请单列。",
    "income": "这个方案每月能拿到多少收入？请用同一口径比较。",
    "hours": "这个方案每周需要工作多少小时？",
    "onsite": "这个方案每周实际需要到岗几天？",
    "move_required": "这个方案是否一定需要搬家？",
}


@dataclass
class Conversation:
    session_id: str
    base: DecisionStateV05
    domain: str
    ledger: EvidenceLedger = field(default_factory=EvidenceLedger)
    options: dict[str, dict] = field(default_factory=dict)
    dialogue: list[dict] = field(default_factory=list)
    dismissed: set[str] = field(default_factory=set)
    revision: int = 1
    saved_revision: int = 0
    context_confirmed: bool = False
    overrides: DecisionStateV05 | None = None
    state: DecisionStateV05 | None = None
    analysis: dict | None = None
    focus: str | None = None
    local_receipt: dict = field(default_factory=dict)
    selected_option_id: str | None = None
    selected_plan: dict | None = None
    changes: list[str] = field(default_factory=list)
    previous_gate: dict = field(default_factory=dict)
    touched: float = field(default_factory=monotonic)

    @property
    def coupled(self):
        messages = [item["text"] for item in self.dialogue if item["role"] == "user"]
        return any(COUPLED.search(text) for text in messages)


def public_claims(row):
    trace = row.ledger.trace()
    statuses = {key: group["status"] for group in trace["groups"] for key in group["active_claim_ids"]}
    previous = {i: group["active_claim_ids"] for group in trace["groups"] for i in group["provisional_claim_ids"]}
    claims = []
    for entry in trace["entries"]:
        claim_id = entry["claim_id"]
        record = entry["claim"].copy()
        record["evidence_kind"] = record["kind"]
        record["kind"] = record.pop("role") or record["kind"]
        state = "DISMISSED" if claim_id in row.dismissed else entry["status"]
        if state == "USER_CONFIRMED" and statuses.get(claim_id) in {"CONFLICT", "INCOMPARABLE", "UNKNOWN"}:
            state = statuses[claim_id]
        claims.append({"id": claim_id, **record, "status": state, "prior_ids": previous.get(claim_id, []),
                       "supersedes": entry["supersedes"], "recorded_at": entry["recorded_at"],
                       "confirmed_at": entry["confirmed_at"]})
    return claims


def active_claims(claims):
    return [item for item in claims if item["status"] in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}
            and item["kind"] != "previous"
            and (item["kind"] != "conditional" or item["field"] == "move_if_onsite_max")]


def blocking_constraints(claims):
    """Unresolved hard obligations cannot disappear from the projection."""
    relevant = [c for c in claims if c["field"] in set(BOUNDS) | {"move_if_onsite_max"}
                and c["kind"] not in {"previous", "estimate"}
                and c["status"] not in {"DISMISSED", "SUPERSEDED"}]
    confirmed = {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}
    exceptions = [c for c in relevant if c["field"] == "move_if_onsite_max"]
    exception = exceptions[0] if len(exceptions) == 1 else None
    # Only the existing explicitly supported relocation exception is executable.
    def companion(c, field, value):
        return (exception is not None and c["kind"] == "conditional" and c["field"] == field
                and not c["subject"].strip() and c["confirmed_at"] is not None
                and c["status"] in confirmed | {"UNKNOWN"}
                and bool(exception["source"].strip()) and c["source"].endswith(exception["source"])
                and evidence_number(c) == value)
    valid_exception = bool(exception and exception["kind"] == "conditional"
                           and exception["status"] in confirmed and not exception["subject"].strip()
                           and evidence_number(exception) is not None
                           and any(c["field"] == "move_allowed" and c["kind"] != "conditional"
                                   and c["status"] in confirmed and not c["subject"].strip()
                                   and evidence_number(c) == 0 for c in relevant)
                           and any(companion(c, "onsite_max", evidence_number(exception)) for c in relevant)
                           and any(companion(c, "move_allowed", 1) for c in relevant))
    blocked = []
    for c in relevant:
        if c["field"] == "move_if_onsite_max":
            if not valid_exception:
                blocked.append(c)
        elif c["kind"] == "conditional":
            if not (valid_exception and (companion(c, "onsite_max", evidence_number(exception))
                                        or companion(c, "move_allowed", 1))):
                blocked.append(c)
        elif (c["status"] not in confirmed or c["subject"].strip() or evidence_number(c) is None):
            blocked.append(c)
    return blocked


def option_id(label):
    return "o-" + sha256(normalize("NFC", label.strip()).encode()).hexdigest()[:18]


class ConversationHub:
    def __init__(self, *, hub=None, provider=None, records=None):
        self.hub = hub or DecisionHubV05()
        self.provider = provider or ConversationOllama()
        self.records = records
        self._lock = RLock()
        self._sessions = OrderedDict()
        self._generation = 0

    def status(self):
        return {"conversation_version": VERSION, "engine_version": self.hub.hub_version,
                "local_model": self.provider.status(), "fallback": "GROUNDED_DETERMINISTIC",
                "purpose_consent": PurposeConsent().status(), "external_verification": "NOT_CONNECTED",
                "execution_available": False}

    def _expire(self):
        now = monotonic()
        for key in list(self._sessions):
            if now - self._sessions[key].touched >= SESSION_TTL:
                self._sessions.pop(key)

    def _read(self, sid, revision):
        self._expire()
        row = self._sessions.get(sid)
        if row is None:
            raise KeyError("Session expired")
        if row.revision != revision:
            raise ValueError("此会话已更新，请用当前版本继续。")
        return row

    def _update(self, row):
        row.touched = monotonic()
        result = self._view(row)
        self._sessions[row.session_id] = row
        self._sessions.move_to_end(row.session_id)
        while len(self._sessions) > MAX_SESSIONS:
            self._sessions.popitem(last=False)
        return deepcopy(result)

    def start(self, question, *, use_local_model=False):
        with self._lock:
            generation = self._generation
        base = DecisionStateV05.model_validate(self.hub.start(question)["state"])
        reading = interpret(question)
        row = Conversation(uuid4().hex, base, reading["domain"])
        self._ingest(row, question, reading, use_local_model)
        with self._lock:
            if generation != self._generation:
                raise KeyError("Session invalidated")
            self._expire()
            return self._update(row)

    def _ingest(self, row, text, reading, allow_local):
        grounded = self.provider.propose(text, self.hub.registry.methods(), allowed=allow_local)
        row.local_receipt = {key: value for key, value in grounded.items() if key != "options"}
        names = [*reading["options"], *grounded.get("options", [])]
        if not names and not row.options:
            names = DEFAULT_OPTIONS.get(row.domain, ())
        for label in names:
            if isinstance(label, str) and 0 < len(label.strip()) <= 100 and len(row.options) < 24:
                label = label.strip()
                for prefix in ("选「", "选择「", "选『", "选择『"):
                    if label.startswith(prefix):
                        label = label[len(prefix):]
                        break
                label = label.strip("「」『』“”")
                if not label:
                    continue
                key = option_id(label)
                row.options.setdefault(key, {"id": key, "label": label, "status": "PROVISIONAL"})
        raw = []
        for item in reading["claims"]:
            if item.get("source") and item["source"] in text and all(len(str(v)) <= 400 for v in item.values()):
                role = item["kind"]
                kind = "estimate" if role == "estimate" else "assumption" if role == "conditional" else "fact"
                raw.append({**item, "kind": kind, "role": role, "metadata": {"source_identity": "current_user", "channel": "user_self_report"}})
                subject = item["subject"].strip()
                if subject and len(subject) <= 100 and len(row.options) < 24:
                    key = option_id(subject)
                    row.options.setdefault(key, {"id": key, "label": subject, "status": "PROVISIONAL"})
        row.ledger = draft_claims(row.ledger, raw, origin="USER")
        row.dialogue.append({"role": "user", "text": text})

    def turn(self, session_id, revision, text, *, use_local_model=False):
        with self._lock:
            snapshot = deepcopy(self._read(session_id, revision))
        if sum(item["role"] == "user" for item in snapshot.dialogue) >= MAX_TURNS:
            raise ValueError("会话已达到轮次上限，请开始新会话。")
        focus = snapshot.focus
        target = focus.removeprefix("confirm_claim:") if focus and focus.startswith("confirm_claim:") else None
        short_yes = text.strip().strip("。！!") in {"对", "是", "正确", "没错", "对的"}
        reading = interpret(text, focus=None if target else focus,
                            known_options=(item["label"] for item in snapshot.options.values()))
        # New substantive input may contain a new obligation even when parsing misses it.
        # A short answer to the exact pending claim is the only narrow exception.
        if not (target and short_yes):
            snapshot.context_confirmed = False
        self._ingest(snapshot, text, reading, use_local_model)
        snapshot.revision += 1
        snapshot.analysis = None
        snapshot.selected_option_id = None
        snapshot.selected_plan = None
        snapshot.changes = []
        if target and short_yes:
            item = next(c for c in public_claims(snapshot) if c["id"] == target)
            if item["status"] == "PROVISIONAL" and not (item["kind"] == "revision" and item["prior_ids"]):
                snapshot.ledger = confirm_claim(snapshot.ledger, target)
                self._compute(snapshot)
        with self._lock:
            self._read(session_id, revision)
            return self._update(snapshot)

    def confirm(self, session_id, revision, claim_ids=(), option_ids=(), accept_context=False,
                corrections=(), dismiss_claim_ids=()):
        with self._lock:
            row = deepcopy(self._read(session_id, revision))
            claims = {item["id"]: item for item in public_claims(row)}
            corrections = {item.claim_id: item.supersedes for item in corrections}
            targets = set(claim_ids) | set(corrections) | set(dismiss_claim_ids)
            if not targets <= claims.keys() or not set(option_ids) <= row.options.keys():
                raise ValueError("仅可核对本会话中显示的项目。")
            accepted = list(dict.fromkeys((*claim_ids, *corrections)))
            if set(accepted) & set(dismiss_claim_ids):
                raise ValueError("同一项不能同时确认和略过。")
            for key in dismiss_claim_ids:
                if claims[key]["status"] != "PROVISIONAL":
                    raise ValueError("仅可略过待核对的项目。")
                row.dismissed.add(key)
            for key in accepted:
                item = claims[key]
                if item["status"] != "PROVISIONAL":
                    raise ValueError("仅可确认待核对的项目。")
                if item["kind"] == "revision" and item["prior_ids"] and key not in corrections:
                    raise ValueError("更改已确认的条件时，请选择要替换的原条件。")
                if key in corrections:
                    row.ledger = confirm_claim(row.ledger, key, mode="correct", supersedes=corrections[key])
                else:
                    row.ledger = confirm_claim(row.ledger, key)
            for key in option_ids:
                row.options[key]["status"] = "CONFIRMED"
            # Discarding a proposed interpretation is not itself withdrawal of a real limit.
            if any(claims[key]["field"] in set(BOUNDS) | {"move_if_onsite_max"}
                   for key in dismiss_claim_ids):
                row.context_confirmed = False
            row.context_confirmed = row.context_confirmed or accept_context
            row.revision += 1
            row.selected_option_id = None
            row.selected_plan = None
            self._compute(row)
            return self._update(row)

    def analyze(self, session_id, revision, *, state=None, confirmed=False):
        with self._lock:
            row = deepcopy(self._read(session_id, revision))
            if state is not None:
                if not confirmed:
                    raise ValueError("请确认高级输入的来源及含义。")
                if (state.question != row.base.question or state.decision_id != row.base.decision_id):
                    raise ValueError("高级输入须属于当前会话。")
                labels = {normalize("NFC", opt["label"]).strip(): key for key, opt in row.options.items()}
                for option in state.options:
                    name = normalize("NFC", option.label).strip()
                    existing = row.options.get(option.id)
                    if (name in labels and labels[name] != option.id) or (existing and existing["label"] != option.label):
                        raise ValueError("已有方案的名称和标识须保持一致。")
                    labels[name] = option.id
                    row.options.setdefault(option.id, {"id": option.id, "label": option.label, "status": "CONFIRMED"})
                    row.options[option.id]["status"] = "CONFIRMED"
                row.context_confirmed = True
                row.overrides = state
            row.revision += 1
            row.selected_option_id = None
            row.selected_plan = None
            self._compute(row)
            return self._update(row)

    def _project(self, row):
        claims = public_claims(row)
        blocking = blocking_constraints(claims)
        ready = row.context_confirmed and not row.coupled and not blocking and sum(
            opt["status"] == "CONFIRMED" for opt in row.options.values()) >= 2
        chosen = row.base.model_copy(update={"revision": row.saved_revision + 1})
        projected = build_state(chosen, row.options.values(), active_claims(claims), ready=ready,
                                overrides=row.overrides)
        if row.selected_plan:
            projected = projected.model_copy(update={"intended_option_id": row.selected_option_id,
                                                    "plan_note": row.selected_plan["trigger"]})
        return projected

    def _compute(self, row):
        row.state = self._project(row)
        row.analysis = None
        row.changes = []
        if not row.state.confirmed:
            return
        result = self.hub.analyze(row.state)
        if result["status"] == "CLARIFY":
            return
        current = {item["option_id"]: item["status"] for item in result["feasibility"]}
        names = {key: option["label"] for key, option in row.options.items()}
        names_of_status = {"ACCEPT": "通过底线", "REJECT": "不符合底线", "UNRESOLVED": "还待核对"}
        row.changes = [f"{names[key]}由{names_of_status[row.previous_gate[key]]}变为{names_of_status[value]}。"
                       for key, value in current.items() if key in row.previous_gate and row.previous_gate[key] != value]
        row.previous_gate = current
        row.analysis = result

    def select(self, session_id, revision, option_id, *, confirmed):
        with self._lock:
            row = deepcopy(self._read(session_id, revision))
            if (not confirmed or row.analysis is None or not any(
                item["option_id"] == option_id and item["status"] == "ACCEPT"
                and row.analysis.get("temporal_scope", {}).get(option_id, "FEASIBLE") == "FEASIBLE"
                for item in row.analysis["feasibility"]
            )):
                raise ValueError("只能明确选择当前已经通过筛查的方案。")
            row.selected_option_id = option_id
            row.selected_plan = None
            row.revision += 1
            return self._update(row)

    def plan(self, session_id, revision, option_id, trigger, *, confirmed):
        with self._lock:
            row = deepcopy(self._read(session_id, revision))
            if not confirmed or row.selected_option_id != option_id or row.analysis is None:
                raise ValueError("请先明确选择方案，再确认这条行动计划。")
            row.selected_plan = {"option_id": option_id, "trigger": trigger, "status": "USER_PLAN_ONLY"}
            row.revision += 1
            self._compute(row)
            return self._update(row)

    def save(self, session_id, revision, epoch, *, save_confirmed):
        with self._lock:
            row = self._read(session_id, revision)
            consent = PurposeConsent(save=save_confirmed)
            if not save_confirmed or self.records is None:
                raise PermissionError("请明确授权保存这条决策。")
            grant = self.records.status()
            if not consent.allows("save", active_save=grant["authorized"]) or grant["epoch"] != epoch:
                raise PermissionError("本地保存授权已失效。")
            if row.analysis is None or row.state is None:
                raise ValueError("请先核对并完成当前分析。")
            analysis = {**row.analysis, "conversation": {"version": VERSION, "revision": row.revision,
                         "confirmed_sources": active_claims(public_claims(row)),
                         "selection": row.selected_option_id, "plan": row.selected_plan}}
            saved = self.records.save(epoch, row.state.model_dump(mode="json"), analysis)
            row.saved_revision = row.state.revision
            return saved

    def end(self, session_id):
        with self._lock:
            self._sessions.pop(session_id, None)
        return {"status": "ENDED"}

    def clear(self):
        with self._lock:
            self._generation += 1
            self._sessions.clear()

    def _view(self, row):
        claims = public_claims(row)
        summary = summarize(row, claims)
        message = " ".join(filter(None, (summary["conclusion"], summary["question"])))
        if not row.dialogue or row.dialogue[-1] != {"role": "assistant", "text": message}:
            row.dialogue.append({"role": "assistant", "text": message})
        state = row.state if row.analysis is not None else self._project(row)
        return {
            "session_id": row.session_id, "revision": row.revision, "conversation_version": VERSION,
            "dialogue": row.dialogue, "summary": summary, "claims": claims, "options": list(row.options.values()),
            "state": state.model_dump(mode="json"), "analysis": row.analysis,
            "phase": "ANALYZED" if row.analysis is not None else "CLARIFY",
            "local_model_status": row.local_receipt["status"], "local_model_receipt": row.local_receipt,
            "selected_option_id": row.selected_option_id, "selected_plan": row.selected_plan,
            "purpose_consent": PurposeConsent().status(), "changes": row.changes,
        }


def plain_measure_differences(row, checked):
    feasible = {item["option_id"] for item in checked if item["status"] == "ACCEPT"
                and row.analysis.get("temporal_scope", {}).get(item["option_id"], "FEASIBLE") == "FEASIBLE"}
    options = [option for option in row.state.options if option.id in feasible]
    if len(options) != 2:
        return []
    left, right = options
    differences = []
    for objective in row.state.objectives:
        if not objective.id.startswith("talk-"):
            continue
        a, b = left.scores.get(objective.id), right.scores.get(objective.id)
        if not a or not b or a.lower is None or b.lower is None or a.lower == b.lower:
            continue
        higher, lower = (left, right) if a.lower > b.lower else (right, left)
        condition = "按你核对的估计" if "estimate" in {a.kind, b.kind} else "按你核对的资料"
        differences.append(f"{objective.label}方面，{higher.label}高于{lower.label}（{condition}）。")
    return differences[:2]


def summarize(row, claims):
    initial, first, second, default_question = FRAMING.get(row.domain, GENERAL)
    warning = None
    question, focus = default_question, "cost_max" if row.domain == "budget" else None
    differences = [first, second]
    unknowns = ["目前缺少足以核对所有方案的资料。"]
    active = active_claims(claims)
    conflicts = [c for c in claims if c["status"] in {"CONFLICT", "INCOMPARABLE"}]
    pending = [c for c in claims if c["status"] == "PROVISIONAL" and c["kind"] != "previous"]
    hard = [c for c in active if c["field"] in BOUNDS and evidence_number(c) is not None and c["kind"] != "estimate"]
    if hard:
        terms = [c["source"] for c in hard[:3]]
        warning = "已核对的底线：" + "；".join(terms)
    if conflicts:
        subject = conflicts[0]["subject"] or "这项条件"
        warning = "有互相冲突或口径不同的说法，先保留未知。"
        question = f"关于「{subject}」的不同说法，能先核对来源和口径吗？"
        focus = None
    elif pending:
        item = next((c for c in pending if c["field"] in BOUNDS), pending[0])
        question = f"我把「{item['source']}」列为待核对，这样理解对吗？"
        focus = f"confirm_claim:{item['id']}"
        if item["field"] in BOUNDS and not warning:
            warning = "这项可能是你的底线，核对后才会用来筛查。"
        if item["kind"] == "conditional" and item["field"] == "onsite_max":
            question = "每周到岗上限是新增条件，还是签约或搬家的明确例外？"
            focus = None
    elif row.analysis is not None:
        result = row.analysis
        checked = result["feasibility"]
        names = {item["option_id"]: item["label"] for item in checked}
        differences = []
        for item in checked:
            if item["status"] == "REJECT":
                differences.append(f"{item['label']}不符合已核对的底线。")
            elif item["status"] == "ACCEPT":
                differences.append(f"{item['label']}通过当前底线。")
            else:
                differences.append(f"{item['label']}仍有条件需要核实。")
        differences = plain_measure_differences(row, checked) + differences
        differences = (differences or [first, second])[:3]
        unknowns = ["部分方案的底线还待核实。"] if any(x["status"] == "UNRESOLVED" for x in checked) else []
        if not any(method["status"] == "EXECUTED" and method["result"].get("leaders") for method in result["methods"]):
            unknowns.append("还需要核对最关心的收益、成本或风险，才能可靠比较。")
        leader_sets = {tuple(sorted(method["result"].get("leaders") or [])) for method in result["methods"]
                       if method["status"] == "EXECUTED" and method["result"].get("leaders")}
        if len(leader_sets) > 1:
            initial = "不同比较方式给出不同结果。先看你更在意的取舍。"
        elif len(leader_sets) == 1 and len(next(iter(leader_sets))) == 1 and not result["conditional_scope"]:
            label = names[next(iter(leader_sets))[0]]
            initial = f"按当前已核对的比较指标，{label}在该计算范围内占优。是否符合整体目标仍需核对。"
        else:
            initial = "目前可以判断部分取舍，现有资料还不足以给出唯一选择。"
        question, focus = None, None
        for item in checked:
            if item["status"] != "UNRESOLVED":
                continue
            for check in item["checks"]:
                key = check["constraint_id"].removeprefix("talk-")
                if key in BOUNDS and check["status"] in {"UNKNOWN", "POSSIBLE"}:
                    field = BOUNDS[key][0]
                    if field == "move_required" and any(c["field"] == "move_if_onsite_max" for c in active):
                        field = "onsite" if any(c["field"] == "move_required" and c["subject"] == item["label"]
                                                for c in active) else field
                    focus = f"{field}:{item['label']}"
                    question = f"关于「{item['label']}」，{QUESTIONS[field]}"
                    break
            if question:
                break
        if not question and not leader_sets:
            question = "哪一项收益、代价或风险最会改变你的选择？"
    elif row.options and not row.context_confirmed:
        unknowns = ["你可以直接核对下方选项和条件，也可以用一句话补充。"]
    if not pending and not conflicts and row.analysis is None and row.context_confirmed:
        question = "还要比较哪些实际可以采取的方案？"
        focus = None
    unresolved = blocking_constraints(claims)
    if unresolved and not pending and not conflicts:
        initial = "目前只能保留条件性分析，尚不能完成全部底线筛查。"
        warning = "有已记录但尚无法完整计算的底线：" + "；".join(c["source"] for c in unresolved[:3])
        unknowns = ["条件的适用范围、单位或计算表达仍待核实。"]
        question = "能否明确这项底线何时适用，以及用什么单位比较？"
        focus = None
    if row.coupled:
        initial = "各项分别符合条件，还不能证明同时采用时也可行。"
        warning = "涉及共用上限，当前尚无针对该联合条件的已准入计算。"
        unknowns = ["需要核对哪些项目共用资源，什么时候可以调整，以及调整是否有损失。"]
        question = "哪些方案会同时占用这笔共同预算或资源？"
        focus = None
    row.focus = focus
    return {"conclusion": initial, "differences": differences, "unknowns": unknowns, "question": question,
            "warning": warning, "focus": focus}
