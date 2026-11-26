"""Same-origin, versioned conversation routes. No execution or provider authority."""
from fastapi import APIRouter
from pydantic import Field

from .decision_api import EpochToken
from .decision_candidates import default_candidate_registry
from .decision_knowledge import discover_knowledge, local_knowledge
from .decision_feedback import FeedbackFreezeInput, FeedbackObservation
from .decision_resources import GoalDeadlineInput, JointResourceInput, RecurringBenefitInput, ResourceState
from .decision_conversation import VERSION, ConversationHub
from .decision_records import DecisionRecords
from .decision_service import personal_data_root
from .decision_state import Identity, InputModel, Key, Original, Text
from .decision_v05 import DecisionStateV05

PREFIX = "/api/v7/decisions"
CURRENT_PREFIX = "/api/v8/decisions"
LEGACY_PREFIX = "/api/v6/decisions"


class EndInput(InputModel):
    session_id: Identity


class SessionInput(EndInput):
    session_instance: Identity | None = None
    revision: int = Field(ge=1, le=1_000_000, strict=True)


class StartInput(InputModel):
    question: Original
    session_id: Identity | None = None
    use_local_model: bool = Field(default=False, strict=True)


class CloseCurrentInput(SessionInput):
    session_instance: Identity


class StartCurrentInput(InputModel):
    question: Original
    cancel_nonce: Identity | None = None
    use_local_model: bool = Field(default=False, strict=True)


class CancelStartInput(InputModel):
    cancel_nonce: Identity


class TurnInput(SessionInput):
    text: Original
    use_local_model: bool = Field(default=False, strict=True)


class Correction(InputModel):
    claim_id: Identity
    supersedes: Identity


class ConfirmInput(SessionInput):
    claim_ids: list[Identity] = Field(default_factory=list, max_length=96)
    option_ids: list[Key] = Field(default_factory=list, max_length=24)
    accept_context: bool = Field(default=False, strict=True)
    corrections: list[Correction] = Field(default_factory=list, max_length=96)
    dismiss_claim_ids: list[Identity] = Field(default_factory=list, max_length=96)


class AnalyzeInput(SessionInput):
    state: DecisionStateV05 | None = None
    confirmed: bool = Field(default=False, strict=True)


class SelectInput(SessionInput):
    option_id: Key
    confirmed: bool = Field(default=False, strict=True)


class PlanInput(SelectInput):
    trigger: Text


class SaveInput(SessionInput):
    epoch: EpochToken
    save_confirmed: bool = Field(default=False, strict=True)


class KnowledgeInput(InputModel):
    query: Original
    limit: int = Field(default=5, ge=1, le=20, strict=True)


class ResourceUpdate(SessionInput):
    resources: ResourceState | None = None
    confirmed: bool = Field(default=False, strict=True)


class ReuseInput(SessionInput):
    epoch: EpochToken
    decision_id: Identity
    reuse_epoch: EpochToken


class FeedbackToken(InputModel):
    token: EpochToken


class FeedbackInput(FeedbackToken):
    observation: FeedbackObservation


class JointResourcesRequest(CloseCurrentInput):
    request: JointResourceInput


class RecurringBenefitRequest(CloseCurrentInput):
    request: RecurringBenefitInput


class GoalDeadlineRequest(CloseCurrentInput):
    request: GoalDeadlineInput


class ResourceRecord(InputModel):
    epoch: EpochToken
    decision_id: Identity


class ResourceReplay(ResourceRecord):
    revision: int | None = Field(default=None, ge=1, le=1_000_000, strict=True)


class ResourceGrant(ResourceRecord):
    confirmed: bool = Field(default=False, strict=True)


class ResourceRevoke(ResourceRecord):
    reuse_epoch: EpochToken


OPERATIONS = {
    "start": StartInput, "turn": TurnInput, "confirm": ConfirmInput, "analyze": AnalyzeInput,
    "select": SelectInput, "plan": PlanInput, "save": SaveInput, "end": EndInput,
    "update_resources": ResourceUpdate, "reuse_resources": ReuseInput,
}


CURRENT_OPERATIONS = {
    **OPERATIONS, "start": StartCurrentInput, "end": CloseCurrentInput, "discard": CloseCurrentInput,
    "cancel_start": CancelStartInput, "joint_resources": JointResourcesRequest,
    "recurring_benefit": RecurringBenefitRequest, "goal_deadline_frontier": GoalDeadlineRequest,
}


def invoke(hub, operation, request, *, current=False):
    schema = (CURRENT_OPERATIONS if current else OPERATIONS)[operation]
    validated = schema.model_validate(request)
    arguments = {
        key: getattr(validated, key) for key in schema.model_fields
    }
    if isinstance(validated, SessionInput) and current != (validated.session_instance is not None):
        raise ValueError("请求必须使用对应版本的会话身份。")
    if isinstance(validated, StartCurrentInput):
        arguments["current"] = True
    return getattr(hub, operation)(**arguments)


def current_capabilities(hub):
    return {**hub.capabilities(), "platform_version": VERSION,
            "conversation_contract": {"protocol": VERSION, "session_instance": "REQUIRED",
                                      "first_request": "CANCELLATION_NONCE_ONLY",
                                      "result_authority": ["FULL_ANALYSIS", "DESCRIPTIVE_ONLY"],
                                      "joint_resources": "DESCRIPTIVE_ONLY",
                                      "recurring_benefit": "NOT_ADMITTED",
                                      "goal_deadline_frontier": "NOT_ADMITTED",
                                      "feedback": "ISOLATED_DEVELOPMENT_ONLY"},
            "active_method_manifest": {
                "contract": "1.0.0",
                "methods": [{"id": method.model_id, "version": method.version, "source": method.source_baseline}
                            for method in hub.hub.registry.methods()],
            },
            "language_adapters": hub.candidate_parsers.describe()}


def create_conversation_root(root):
    return ConversationHub(records=DecisionRecords(personal_data_root(root)))


def router(hub, *, legacy=False, current=False):
    api = APIRouter(prefix=CURRENT_PREFIX if current else LEGACY_PREFIX if legacy else PREFIX)
    version_label = "v8" if current else "v6" if legacy else "v7"

    @api.get("/status")
    def status():
        return hub.status(current=current)

    @api.get("/capabilities")
    def capabilities():
        return current_capabilities(hub) if current else hub.capabilities()

    @api.get("/models")
    def models():
        return hub.hub.registry.describe()

    if not legacy:
        @api.post("/knowledge")
        def knowledge(data: KnowledgeInput):
            return local_knowledge().search(data.query, data.limit)

        @api.post("/knowledge/discover")
        def knowledge_discovery(data: KnowledgeInput):
            return discover_knowledge(data.query, limit=data.limit)

        @api.get("/knowledge/report")
        def knowledge_report():
            return local_knowledge().report()

        @api.get("/research-candidates")
        def research_candidates():
            return {"authority": "NONE", "candidates": default_candidate_registry().describe()}

        @api.post("/resource-grant")
        def grant(data: ResourceGrant):
            return hub.invalidate_record(hub.records.grant_resource_reuse, data.epoch, data.decision_id,
                                         confirmed=data.confirmed)

        @api.post("/resource-revoke")
        def revoke(data: ResourceRevoke):
            return hub.invalidate_record(hub.records.revoke_resource_reuse, data.epoch, data.decision_id,
                                         data.reuse_epoch)

        @api.post("/resource-replay")
        def replay(data: ResourceReplay):
            return hub.records.resource_replay(data.epoch, data.decision_id, revision=data.revision)

    if current:
        @api.post("/feedback/freeze")
        def feedback_freeze(data: FeedbackFreezeInput):
            return hub.feedback.freeze(data)

        @api.post("/feedback/observe")
        def feedback_observe(data: FeedbackInput):
            return hub.feedback.observe(data.token, data.observation)

        @api.post("/feedback/evaluate")
        def feedback_evaluate(data: FeedbackToken):
            return hub.feedback.evaluate(data.token)

        @api.post("/feedback/rollback")
        def feedback_rollback(data: FeedbackToken):
            return hub.feedback.rollback(data.token)

    def endpoint(operation, schema):
        def handle(data: schema):
            return invoke(hub, operation, data, current=current)
        return handle

    for operation, schema in (CURRENT_OPERATIONS if current else OPERATIONS).items():
        path = "cancel-start" if operation == "cancel_start" else operation
        api.add_api_route(f"/{path}", endpoint(operation, schema), methods=["POST"],
                          name=f"{version_label}_{operation}")
    return api
