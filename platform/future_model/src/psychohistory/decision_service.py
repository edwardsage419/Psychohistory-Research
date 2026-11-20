"""Shared v0.4 entry points for the authenticated API and the local CLI."""
from pathlib import Path

from .decision_hub import DecisionHub
from .decision_records import DecisionRecords
from .decision_state import DecisionState
from .storage import checked_path


def personal_data_root(research_root):
    root = checked_path(Path(research_root))
    return root.with_name(f"{root.name}-personal-v04")


class DecisionService:
    def __init__(self, research_root):
        self.records = DecisionRecords(personal_data_root(research_root))
        self.hub = DecisionHub()

    def save(self, epoch, state):
        state = DecisionState.model_validate(state)
        analysis = self.hub.analyze(state)
        if analysis["status"] == "CLARIFY":
            raise ValueError("请完成本版澄清和确认后再保存。")
        return self.records.save(epoch, state.model_dump(mode="json"), analysis)
