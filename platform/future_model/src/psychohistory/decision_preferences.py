"""User-authored preferences, hindsight, and explicit adoption for future use."""

from typing import Literal

from pydantic import Field, model_validator

from .decision_state import Identity, InputModel, Original, Text


class PreferenceValue(InputModel):
    label: Text
    value: Text


class PreferenceSnapshot(InputModel):
    values: list[PreferenceValue] = Field(min_length=1, max_length=16)
    applicability: Text
    provenance: Text
    adopted_version_id: Identity | None = None

    @model_validator(mode='after')
    def distinct_values(self):
        if len({entry.label.strip().casefold() for entry in self.values}) != len(self.values):
            raise ValueError('偏好事项名称必须唯一。')
        return self


class Hindsight(InputModel):
    evidence: Original | None = None
    current_preferences: PreferenceSnapshot | None = None
    process_quality: Original | None = None

    @model_validator(mode='after')
    def check_hindsight(self):
        if self.evidence is None and self.current_preferences is None and self.process_quality is None:
            raise ValueError('需要至少一项事后新证据、当前偏好或决策过程评价。')
        if self.current_preferences is not None and self.current_preferences.adopted_version_id is not None:
            raise ValueError('当前偏好是这次复盘的独立陈述。')
        return self


class AdoptedPreference(InputModel):
    version_id: Identity
    adopted_at: Text
    decision_id: Identity
    review_index: int = Field(ge=1, strict=True)
    source_kind: Literal['real', 'synthetic']
    preferences: PreferenceSnapshot
