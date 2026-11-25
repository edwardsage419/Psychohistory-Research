"""Personal terminal session. Protocol is one command per input line."""
import json
import sys

from .contracts import canonical
from .decision_conversation_api import OPERATIONS, create_conversation_root, invoke


def talk(data):
    hub = create_conversation_root(data)
    while raw := sys.stdin.buffer.readline(262145):
        try:
            if len(raw) > 262144:
                raise ValueError("Input too long")
            message = json.loads(raw)
            if not isinstance(message, dict) or set(message) != {"operation", "data"}:
                raise ValueError("Invalid message")
            operation = message["operation"]
            if operation == "status" and message["data"] == {}:
                result = hub.status()
            elif operation == "capabilities" and message["data"] == {}:
                result = hub.capabilities()
            elif isinstance(operation, str) and operation in OPERATIONS:
                result = invoke(hub, operation, message["data"])
            else:
                raise ValueError("Unknown operation")
        except (TypeError, ValueError, KeyError, PermissionError, RecursionError):
            result = {"status": "REJECTED", "reason": "请核对会话、修订及请求格式。"}
        print(canonical(result), flush=True)
        if len(raw) > 262144:
            return 1
    return 0
