"""Same-origin, versioned conversation routes. No execution or provider authority."""
from fastapi import APIRouter
from pydantic import Field

from .decision_api import EpochToken
from .decision_candidates import default_candidate_registry
from .decision_knowledge import discover_knowledge, local_knowledge
from .decision_resources import ResourceState
from .decision_conversation import ConversationHub
from .decision_records import DecisionRecords
from .decision_service import personal_data_root
from .decision_state import Identity, InputModel, Key, Original, Text
from .decision_v05 import DecisionStateV05

PREFIX = "/api/v7/decisions"
LEGACY_PREFIX = "/api/v6/decisions"


class EndInput(InputModel):
    session_id: Identity


class SessionInput(EndInput):
    revision: int = Field(ge=1, le=1_000_000, strict=True)


class StartInput(InputModel):
    question: Original
    session_id: Identity | None = None
    use_local_model: bool = Field(default=False, strict=True)


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


def invoke(hub, operation, request):
    schema = OPERATIONS[operation]
    validated = schema.model_validate(request)
    return getattr(hub, operation)(**{key: getattr(validated, key) for key in schema.model_fields})


def create_conversation_root(root):
    return ConversationHub(records=DecisionRecords(personal_data_root(root)))


def router(hub, *, legacy=False):
    api = APIRouter(prefix=LEGACY_PREFIX if legacy else PREFIX)

    @api.get("/status")
    def status():
        return hub.status()

    @api.get("/capabilities")
    def capabilities():
        return hub.capabilities()

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

    def endpoint(operation, schema):
        def handle(data: schema):
            return invoke(hub, operation, data)
        return handle

    for operation, schema in OPERATIONS.items():
        api.add_api_route(f"/{operation}", endpoint(operation, schema), methods=["POST"], name=f"{'v6' if legacy else 'v7'}_{operation}")
    return api
