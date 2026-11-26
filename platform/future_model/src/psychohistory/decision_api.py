"""Personal decisions use the existing local bearer and origin boundary."""
from typing import Annotated

from fastapi import APIRouter
from pydantic import Field, StringConstraints

from .decision_service import DecisionService
from .decision_state import DecisionState, Identity, InputModel, Key, Original, Text

PREFIX = "/api/v4/decisions"
PREFIX_V05 = "/api/v5/decisions"
DECISION_ROUTES = (PREFIX + "/", PREFIX_V05 + "/", "/api/v6/decisions/", "/api/v7/decisions/", "/api/v8/decisions/")
MAX_DECISION_REQUEST = 256 * 1024
MAX_RESTORE_REQUEST = 32 * 1024 * 1024
EpochToken = Annotated[str, StringConstraints(min_length=1, max_length=128)]


class StartInput(InputModel):
    question: Original


class AnalysisInput(InputModel):
    state: DecisionState


class Epoch(InputModel):
    epoch: EpochToken


class SaveInput(Epoch):
    state: DecisionState


class RecordInput(Epoch):
    decision_id: Identity


class ActionInput(RecordInput):
    option_id: Key
    occurred_at: Text
    revision: int = Field(ge=1, le=1_000_000, strict=True)


class ReviewInput(RecordInput):
    observation: Original
    observed_at: Text
    kind: Text


class RestoreInput(Epoch):
    backup: dict
    confirm: bool = Field(default=False, strict=True)


class AdoptInput(RecordInput):
    review_index: int = Field(ge=1, strict=True)
    confirmed: bool = Field(default=False, strict=True)


def advanced_schemas():
    from .decision_preferences import Hindsight
    from .decision_v05 import DecisionStateV05

    class AdvancedAnalysis(InputModel):
        state: DecisionStateV05

    class AdvancedSave(Epoch):
        state: DecisionStateV05

    class AdvancedReview(ReviewInput):
        hindsight: Hindsight | None = None

    return AdvancedAnalysis, AdvancedSave, AdvancedReview


def router(root, *, advanced=False, invalidate=None, invalidate_record=None):
    routes = APIRouter(prefix=PREFIX_V05 if advanced else PREFIX)
    service = DecisionService(root, advanced=advanced)
    analysis_schema, save_schema, review_schema = advanced_schemas() if advanced else (AnalysisInput, SaveInput, ReviewInput)
    hub, records = service.hub, service.records

    @routes.get("/models")
    def models():
        return hub.registry.describe()

    @routes.post("/start")
    def start(data: StartInput):
        return hub.start(data.question)

    @routes.post("/analyze")
    def analyze(data: analysis_schema):
        return hub.analyze(data.state)

    @routes.get("/consent")
    def consent():
        return records.status()

    @routes.post("/consent")
    def grant(data: InputModel):
        return records.grant()

    @routes.post("/revoke")
    def revoke(data: Epoch):
        if invalidate is not None:
            return invalidate(records.revoke, data.epoch)
        return records.revoke(data.epoch)

    @routes.post("/save")
    def save(data: save_schema):
        return service.save(data.epoch, data.state)

    @routes.post("/history")
    def history(data: Epoch):
        return records.list(data.epoch)

    @routes.post("/record")
    def record(data: RecordInput):
        return records.get(data.epoch, data.decision_id)

    @routes.post("/action")
    def action(data: ActionInput):
        return service.action(data.epoch, data.decision_id, data.option_id, data.occurred_at, data.revision)

    @routes.post("/review")
    def review(data: review_schema):
        return service.review(data.epoch, data.decision_id, data.observation, data.observed_at,
                              data.kind, hindsight=getattr(data, "hindsight", None))

    @routes.post("/export")
    def export(data: Epoch):
        return records.export(data.epoch)

    @routes.post("/delete")
    def delete(data: RecordInput):
        if invalidate_record is not None:
            return invalidate_record(records.delete, data.epoch, data.decision_id, include_decision=True)
        return records.delete(data.epoch, data.decision_id)

    @routes.post("/restore")
    def restore(data: RestoreInput):
        return records.restore(data.epoch, data.backup, data.confirm)

    if advanced:
        @routes.post("/preferences")
        def preferences(data: Epoch):
            return records.preferences(data.epoch)

        @routes.post("/adopt-preferences")
        def adopt(data: AdoptInput):
            return records.adopt_preferences(data.epoch, data.decision_id, data.review_index, data.confirmed)

    return routes
