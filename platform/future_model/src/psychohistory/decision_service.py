"""Versioned entry points for the authenticated API and the local CLI."""
from pathlib import Path

from .decision_hub import DecisionHub
from .decision_records import DecisionRecords
from .storage import checked_path


def personal_data_root(research_root):
    root = checked_path(Path(research_root))
    return root.with_name(f"{root.name}-personal-v04")


class DecisionService:
    def __init__(self, research_root, *, advanced=False):
        self.records = DecisionRecords(personal_data_root(research_root))
        if advanced:
            from .decision_v05 import DecisionHubV05

            self.hub = DecisionHubV05()
        else:
            self.hub = DecisionHub()
        self.advanced = advanced

    def save(self, epoch, state):
        state = self.hub.state_model.model_validate(state)
        analysis = self.hub.analyze(state)
        if analysis["status"] == "CLARIFY":
            raise ValueError("请完成本版澄清和确认后再保存。")
        return self.records.save(epoch, state.model_dump(mode="json"), analysis)

    def action(self, epoch, decision_id, option_id, occurred_at, revision):
        return self.records.action(epoch, decision_id, option_id, occurred_at, revision, allow_v05=self.advanced)

    def review(self, epoch, decision_id, observation, observed_at, kind, *, hindsight=None):
        return self.records.review(epoch, decision_id, observation, observed_at, kind,
                                   hindsight=hindsight, allow_v05=self.advanced)
