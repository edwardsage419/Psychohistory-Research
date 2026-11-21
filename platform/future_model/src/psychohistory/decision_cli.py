"""Read personal input from stdin or an explicit file, never command arguments."""
import json
from pathlib import Path
import sys

from pydantic import ValidationError

from .decision_api import (
    MAX_DECISION_REQUEST, MAX_RESTORE_REQUEST, ActionInput, AdoptInput, AnalysisInput, Epoch,
    RecordInput, RestoreInput, ReviewInput, SaveInput, StartInput, advanced_schemas,
)
from .decision_service import DecisionService

def add_parser(subparsers, *, advanced=False):
    name, version = ("decision-v05", "v0.5") if advanced else ("decision", "v0.4")
    decision = subparsers.add_parser(name, help=f"{version} personal decision analysis and private records")
    actions = decision.add_subparsers(dest="action", required=True)
    for name in ("models", "status", "grant"):
        actions.add_parser(name)
    operations = ("start", "analyze", "save", "history", "record", "action", "review", "export",
                  "revoke", "delete", "restore")
    if advanced:
        operations += ("preferences", "adopt-preferences")
    for name in operations:
        action = actions.add_parser(name)
        action.add_argument("--input", type=Path, help="Read JSON from this private file (default: stdin)")


def input_data(path, action):
    limit = MAX_RESTORE_REQUEST if action == "restore" else MAX_DECISION_REQUEST
    if action == "restore" and path is not None:
        # The local operator explicitly names a file. This path can read exports
        # larger than the HTTP transport limit.
        try:
            with path.open("rb") as stream:
                return json.load(stream)
        except (ValueError, RecursionError) as exc:
            raise ValueError("需要有效的 JSON 请求。") from exc
    if path is None:
        data = sys.stdin.buffer.read(limit + 1)
    else:
        with path.open("rb") as stream:
            data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("个人决策请求过大。")
    try:
        value = json.loads(data)
    except (ValueError, RecursionError) as exc:
        raise ValueError("需要有效的 JSON 请求。") from exc
    return value


def run(args):
    advanced = args.command == "decision-v05"
    service = DecisionService(args.data, advanced=advanced)
    records = service.records
    if args.action == "models":
        return service.hub.registry.describe()
    if args.action == "status":
        return records.status()
    if args.action == "grant":
        return records.grant()
    analysis_schema, save_schema, review_schema = advanced_schemas() if advanced else (AnalysisInput, SaveInput, ReviewInput)
    handlers = {
        "start": (StartInput, lambda question: service.hub.start(question)),
        "analyze": (analysis_schema, service.hub.analyze),
        "save": (save_schema, service.save),
        "history": (Epoch, records.list),
        "record": (RecordInput, records.get),
        "action": (ActionInput, service.action),
        "review": (review_schema, service.review),
        "export": (Epoch, records.export),
        "revoke": (Epoch, records.revoke),
        "delete": (RecordInput, records.delete),
        "restore": (RestoreInput, records.restore),
    }
    if advanced:
        handlers.update({
            "preferences": (Epoch, records.preferences),
            "adopt-preferences": (AdoptInput, records.adopt_preferences),
        })
    schema, handler = handlers[args.action]
    try:
        data = schema.model_validate(input_data(args.input, args.action))
    except ValidationError:
        raise ValueError("个人决策请求字段缺失或格式无效。") from None
    return handler(**{key: getattr(data, key) for key in type(data).model_fields})
