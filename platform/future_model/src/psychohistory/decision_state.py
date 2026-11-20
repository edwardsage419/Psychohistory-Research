"""v0.4 decision input. No persistence and no inferred user preference."""
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, StringConstraints, model_validator

SCHEMA_VERSION = "1.0.0"
HUB_VERSION = "0.4.0"


def nonblank(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("需要非空文字")
    return value


def decimal_input(value):
    if type(value) not in (str, int, float, Decimal):
        raise ValueError("需要有限十进制数")
    if isinstance(value, str) and len(value) > 40:
        raise ValueError("数值长度超过限制")
    return value


Text = Annotated[str, StringConstraints(min_length=1, max_length=400), BeforeValidator(nonblank)]
TextLine = Annotated[str, StringConstraints(max_length=400)]
Original = Annotated[str, StringConstraints(max_length=6000), BeforeValidator(nonblank)]
Identity = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{32}$")]
Key = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_-]{1,48}$")]
Number = Annotated[
    Decimal,
    Field(allow_inf_nan=False, max_digits=18, decimal_places=12, ge=-10**12, le=10**12),
    BeforeValidator(decimal_input),
]
Kind = Literal["fact", "estimate", "assumption", "synthetic", "unknown"]


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)


class Quantity(InputModel):
    lower: Number | None = None
    upper: Number | None = None
    unit: Text
    kind: Kind
    source: TextLine = ""
    horizon: Text | None = None

    @model_validator(mode="after")
    def check_bounds(self):
        if self.lower is not None and self.upper is not None and self.lower > self.upper:
            raise ValueError("区间下界不能大于上界")
        if self.kind == "unknown" and (self.lower is not None or self.upper is not None):
            raise ValueError("未知数值应留空")
        return self


class Weight(InputModel):
    lower: Number
    upper: Number

    @model_validator(mode="after")
    def check_bounds(self):
        if self.lower > self.upper:
            raise ValueError("区间下界不能大于上界")
        return self


class Objective(InputModel):
    id: Key
    label: Text
    unit: Text
    direction: Literal["max", "min"]


class Constraint(InputModel):
    id: Key
    label: Text
    unit: Text
    operator: Literal[">=", ">", "<=", "<"]
    threshold: Number
    source: TextLine = ""
    horizon: Text | None = None


class Option(InputModel):
    id: Key
    label: Text
    measurements: Annotated[dict[Key, Quantity], Field(max_length=24)] = Field(default_factory=dict)
    scores: Annotated[dict[Key, Quantity], Field(max_length=16)] = Field(default_factory=dict)


class Scenario(InputModel):
    id: Key
    label: Text
    utilities: Annotated[dict[Key, Quantity], Field(max_length=24)] = Field(default_factory=dict)
    kind: Kind
    source: TextLine = ""
    probability: Annotated[Number, Field(ge=0, le=1)] | None = None


class Proposal(InputModel):
    field: Literal["objectives", "options", "deadline", "constraints", "preferences"]
    value: Text
    source: Text


class UnderstandingReceipt(InputModel):
    mode: Literal["GUIDED_CONFIRMATION", "PROVISIONAL_PROVIDER", "PROVIDER_FAILED"]
    provider_id: Text | None = None
    provider_version: Text | None = None
    suggestions: list[Proposal] = Field(default_factory=list, max_length=22)


class DecisionState(InputModel):
    schema_version: Literal["1.0.0"] = SCHEMA_VERSION
    decision_id: Identity
    revision: int = Field(ge=1, le=1_000_000, strict=True)
    question: Original
    understanding_receipt: UnderstandingReceipt | None = None
    confirmed: bool = Field(default=False, strict=True)
    deadline: Text | None = None
    constraints_confirmed: bool = Field(default=False, strict=True)
    objectives: list[Objective] = Field(default_factory=list, max_length=16)
    constraints: list[Constraint] = Field(default_factory=list, max_length=24)
    options: list[Option] = Field(default_factory=list, max_length=24)
    weights_confirmed: bool = Field(default=False, strict=True)
    weights: Annotated[dict[Key, Weight], Field(max_length=16)] = Field(default_factory=dict)
    score_basis: Text | None = None
    score_dependence: Literal["unknown", "rectangle", "shared_additive"] = "unknown"
    score_dependence_source: Text | None = None
    score_transform: Literal["unknown", "identity", "clip_01"] = "unknown"
    shared_offset_dependence: Literal["unknown", "rectangle"] = "unknown"
    shared_offsets: Annotated[dict[Key, Weight], Field(max_length=16)] = Field(default_factory=dict)
    scenarios: list[Scenario] = Field(default_factory=list, max_length=24)
    scenario_basis: Text | None = None
    scenario_dependence: Literal["unknown", "rectangle", "constrained"] = "unknown"
    scenario_dependence_source: Text | None = None
    precision_radius: Annotated[Number, Field(ge=0)] | None = None
    reference_option_id: Key | None = None

    @model_validator(mode="after")
    def check_references(self):
        for items in (self.objectives, self.constraints, self.options, self.scenarios):
            if len({item.id for item in items}) != len(items):
                raise ValueError("同类字段的标识必须唯一")
        objectives = {item.id for item in self.objectives}
        constraints = {item.id for item in self.constraints}
        options = {item.id for item in self.options}
        if (self.weights.keys() | self.shared_offsets.keys()) - objectives:
            raise ValueError("权重或误差引用了不存在的目标")
        for option in self.options:
            if option.measurements.keys() - constraints or option.scores.keys() - objectives:
                raise ValueError("方案引用了不存在的硬约束或目标")
        if any(scenario.utilities.keys() - options for scenario in self.scenarios):
            raise ValueError("情景引用了不存在的方案")
        if self.reference_option_id is not None and self.reference_option_id not in options:
            raise ValueError("基准方案不存在")
        return self
