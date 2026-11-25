"""Same-origin v0.6 conversation routes. No execution or provider authority."""
from fastapi import APIRouter
from pydantic import Field

from .decision_api import EpochToken
from .decision_conversation import ConversationHub
from .decision_records import DecisionRecords
from .decision_service import personal_data_root
from .decision_state import Identity, InputModel, Key, Original, Text
from .decision_v05 import DecisionStateV05

PREFIX = "/api/v6/decisions"


class EndInput(InputModel):
    session_id: Identity


class SessionInput(EndInput):
    revision: int = Field(ge=1, le=1_000_000, strict=True)


class StartInput(InputModel):
    question: Original
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


OPERATIONS = {
    "start": StartInput, "turn": TurnInput, "confirm": ConfirmInput, "analyze": AnalyzeInput,
    "select": SelectInput, "plan": PlanInput, "save": SaveInput, "end": EndInput,
}


def invoke(hub, operation, request):
    schema = OPERATIONS[operation]
    validated = schema.model_validate(request)
    return getattr(hub, operation)(**{key: getattr(validated, key) for key in schema.model_fields})


def create_conversation_root(root):
    return ConversationHub(records=DecisionRecords(personal_data_root(root)))


def router(hub):
    api = APIRouter(prefix=PREFIX)

    @api.get("/status")
    def status():
        return hub.status()

    @api.get("/models")
    def models():
        return hub.hub.registry.describe()

    def endpoint(operation, schema):
        def handle(data: schema):
            return invoke(hub, operation, data)
        return handle

    for operation, schema in OPERATIONS.items():
        api.add_api_route(f"/{operation}", endpoint(operation, schema), methods=["POST"], name=f"v06_{operation}")
    return api
