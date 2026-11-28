"""General decision coordination v0.5. Existing v0.4 state remains readable."""
from dataclasses import replace
from typing import Literal

from pydantic import Field, model_validator

from .decision_extensions import Capability, EvidenceItem, request_candidates
from .decision_feasibility import GATE_ID
from .decision_hub import DecisionHub
from .decision_planner import plan
from .decision_preferences import PreferenceSnapshot
from .decision_registry import default_registry
from .decision_state import DecisionState, Key, Text
from .decision_timing import TimingInput, immediate_availability
from .decision_voi import InformationInput

V05_VERSION = "0.5.0"
V05_SOURCE = "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a"
EXECUTION_STATUS = {"available": False, "authorization": "NOT_REQUESTED", "action_endpoint": "OBSERVATION_ONLY"}


class DecisionStateV05(DecisionState):
    workflow_version: Literal["0.5.0"] = V05_VERSION
    intent: Text | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list, max_length=40)
    information: InformationInput | None = None
    timing: TimingInput | None = None
    preferences: PreferenceSnapshot | None = None
    intended_option_id: Key | None = None
    plan_note: Text | None = None

    @model_validator(mode="after")
    def check_v05_references(self):
        if self.intended_option_id is not None and self.intended_option_id not in {item.id for item in self.options}:
            raise ValueError("计划选择必须引用现有方案")
        if len({item.id for item in self.evidence}) != len(self.evidence):
            raise ValueError("证据标识必须唯一")
        return self


def v05_registry():
    from .decision_timing import METHODS as timing_methods
    from .decision_voi import METHODS as voi_methods

    registry = default_registry()
    for method in (*voi_methods, *timing_methods):
        dependencies = (f"{GATE_ID}@1.0.0", *method.depends_on)
        scope = "structural" if method in timing_methods else method.candidate_scope
        registry.register(replace(method, source_baseline=V05_SOURCE, candidate_scope=scope,
                                  depends_on=tuple(dict.fromkeys(dependencies))))
    return registry.for_release(
        (method.model_id, method.version, method.source_baseline) for method in registry.methods()
    )


class DecisionHubV05(DecisionHub):
    state_model = DecisionStateV05
    hub_version = V05_VERSION

    def __init__(self, registry=None, *, adapters=None):
        super().__init__(registry=registry if registry is not None else v05_registry())
        self.adapters = dict(adapters or {})

    async def propose(self, capability: Capability, query: str, permit=None):
        return await request_candidates(self.adapters.get(capability), capability, query, permit)

    def start(self, original, *, allow_provider=False):
        result = super().start(original, allow_provider=allow_provider)
        analysis = self.analyze(result["state"])
        return {**result, "plan": analysis["plan"], "execution": dict(EXECUTION_STATUS)}

    def comparison_scope(self, state, feasible):
        if not state.timing or not state.timing.confirmed:
            return feasible, []
        statuses = {o.id: immediate_availability(state.timing, o.id) for o in feasible}
        risks = []
        if "EXPIRED" in statuses.values():
            risks.append("已确认到期的方案从当前比较中排除；时机表保留这些方案。")
        if "UNKNOWN" in statuses.values():
            risks.append("时间可用性未知的方案暂不进入当前比较；请核对其期限。")
        return tuple(o for o in feasible if statuses[o.id] == "FEASIBLE"), risks

    def analyze(self, state):
        state = self.state_model.model_validate(state)
        result = super().analyze(state)
        timed = state.timing
        temporal_scope = {}
        if timed and timed.confirmed:
            temporal_scope = {item["option_id"]: immediate_availability(timed, item["option_id"])
                              for item in result["feasibility"] if item["status"] == "ACCEPT"}
        if timed and timed.investigation and any(
            item["model_id"].startswith("voi_") and item["status"] == "EXECUTED" for item in result["methods"]
        ):
            result["risks"].append(
                "无延迟信息价值按准时获知且无需等待的反事实计算。有真实调查时长时，应按时机方法的期限及可行集解读。"
            )
        return {
            **result,
            "temporal_scope": temporal_scope,
            "plan": plan(state, {**result, "temporal_scope": temporal_scope}),
            "execution": dict(EXECUTION_STATUS),
            "evidence_retrieval": "USER_SOURCE_REQUIRED",
        }
