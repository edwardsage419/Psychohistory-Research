"""Personal decisions use the existing local bearer and origin boundary."""
from typing import Annotated

from fastapi import APIRouter
from pydantic import Field, StringConstraints

from .decision_service import DecisionService
from .decision_state import DecisionState, Identity, InputModel, Key, Original, Text

PREFIX = "/api/v4/decisions"
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


def router(root):
    routes = APIRouter(prefix=PREFIX)
    service = DecisionService(root)
    hub, records = service.hub, service.records

    @routes.get("/models")
    def models():
        return hub.registry.describe()

    @routes.post("/start")
    def start(data: StartInput):
        return hub.start(data.question)

    @routes.post("/analyze")
    def analyze(data: AnalysisInput):
        return hub.analyze(data.state)

    @routes.get("/consent")
    def consent():
        return records.status()

    @routes.post("/consent")
    def grant(data: InputModel):
        return records.grant()

    @routes.post("/revoke")
    def revoke(data: Epoch):
        return records.revoke(data.epoch)

    @routes.post("/save")
    def save(data: SaveInput):
        return service.save(data.epoch, data.state)

    @routes.post("/history")
    def history(data: Epoch):
        return records.list(data.epoch)

    @routes.post("/record")
    def record(data: RecordInput):
        return records.get(data.epoch, data.decision_id)

    @routes.post("/action")
    def action(data: ActionInput):
        return records.action(data.epoch, data.decision_id, data.option_id, data.occurred_at, data.revision)

    @routes.post("/review")
    def review(data: ReviewInput):
        return records.review(data.epoch, data.decision_id, data.observation, data.observed_at, data.kind)

    @routes.post("/export")
    def export(data: Epoch):
        return records.export(data.epoch)

    @routes.post("/delete")
    def delete(data: RecordInput):
        return records.delete(data.epoch, data.decision_id)

    @routes.post("/restore")
    def restore(data: RestoreInput):
        return records.restore(data.epoch, data.backup, data.confirm)

    return routes
