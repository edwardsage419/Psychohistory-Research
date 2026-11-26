"""Local synthetic evaluation of fixed, isolated continuous forecast candidates."""

from datetime import UTC, datetime
from decimal import Decimal
from hmac import compare_digest
from secrets import token_hex
from threading import RLock
from typing import Annotated, Callable, Literal

from pydantic import AwareDatetime, Field, StringConstraints, model_validator

from .decision_resources import Money, NonnegativeMoney, _money
from .decision_state import InputModel, Key


FEEDBACK_CONTRACT_VERSION = "1.0.0"
VersionName = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_.-]{1,64}$")]


class FeedbackForecast(InputModel):
    id: Key
    current: NonnegativeMoney
    baseline: NonnegativeMoney
    not_before: AwareDatetime


class FeedbackFreezeInput(InputModel):
    confirmed: bool = Field(strict=True)
    dataset_kind: Literal["SYNTHETIC", "PUBLIC_DEVELOPMENT"]
    candidate_version: VersionName
    current_version: VersionName
    baseline_version: VersionName
    scope: Key
    unit: Key
    adjustment: Money
    development_ids: list[Key] = Field(max_length=128)
    cases: list[FeedbackForecast] = Field(min_length=2, max_length=128)


class FeedbackObservation(InputModel):
    case_id: Key
    kind: Literal["OBSERVED", "MISSING", "CANCELLED", "UNOBSERVED"]
    observed_at: AwareDatetime
    revision: int = Field(strict=True, ge=1, le=2**31 - 1)
    lower: NonnegativeMoney | None = None
    upper: NonnegativeMoney | None = None

    @model_validator(mode="after")
    def check_interval(self):
        if self.kind == "OBSERVED":
            if self.lower is None or self.upper is None or self.lower > self.upper:
                raise ValueError("观测结果需要可信的上下界。")
        elif self.lower is not None or self.upper is not None:
            raise ValueError("未观察结果不接受数值。")
        return self



class FeedbackTransferInput(InputModel):
    confirmed: bool = Field(strict=True)
    target_scope: Key
    unit: Key
    support_version: VersionName
    reference_lower: Money
    reference_upper: Money
    offset_lower: Money
    offset_upper: Money
    scale: int = Field(strict=True, ge=1, le=2)

    @model_validator(mode="after")
    def check_support(self):
        if self.reference_lower > self.reference_upper or self.offset_lower > self.offset_upper:
            raise ValueError("支持范围须有序。")
        return self

def _gain_bounds(observation, old, candidate):
    points = [observation.lower, observation.upper]
    points.extend(value for value in (old, candidate) if observation.lower <= value <= observation.upper)
    absolute = [abs(value - old) - abs(value - candidate) for value in points]
    underestimate = [max(0, value - old) - max(0, value - candidate) for value in points]
    return min(absolute), max(absolute), min(underestimate), max(underestimate)


class FeedbackLab:
    """One bounded evaluation per local process. No storage or production writes."""

    def __init__(self, *, clock: Callable[[], datetime] | None = None):
        self._clock = clock if clock is not None else lambda: datetime.now(UTC)
        self._lock = RLock()
        self._plan: FeedbackFreezeInput | None = None
        self._token: str | None = None
        self._frozen_at: datetime | None = None
        self._observations: dict[str, FeedbackObservation] = {}
        self._revision = 0

    def _require_current(self, token: str) -> FeedbackFreezeInput:
        if (self._plan is None or self._token is None or not isinstance(token, str)
                or not token.isascii() or not compare_digest(token, self._token)):
            raise PermissionError("候选评价已结束或当前凭据无效。")
        return self._plan

    def freeze(self, plan: FeedbackFreezeInput) -> dict:
        """Freeze candidate adjustment, references and complete evaluation roster."""
        with self._lock:
            if self._plan is not None:
                raise ValueError("请先结束当前候选评价。")
            now = self._clock()
            plan = plan.model_copy(deep=True)
            ids = {case.id for case in plan.cases}
            if not plan.confirmed:
                raise PermissionError("候选评价必须明确确认。")
            if len(ids) != len(plan.cases) or ids.intersection(plan.development_ids):
                raise ValueError("开发与评价案例必须分离，每个评价案例只接受一次。")
            if any(case.not_before <= now or case.current + plan.adjustment < 0 for case in plan.cases):
                raise ValueError("候选预测须在观察前冻结，且不能产生负值。")
            self._plan = plan
            self._token = token_hex(24)
            self._frozen_at = now
            self._revision = 1
            return {**self._metadata(plan), "status": "FROZEN", "token": self._token}

    def _metadata(self, plan):
        return {
            "version": FEEDBACK_CONTRACT_VERSION, "revision": self._revision,
            "authority": "NONE", "admission": "NOT_ADMITTED",
            "candidate_version": plan.candidate_version, "current_version": plan.current_version,
            "baseline_version": plan.baseline_version, "frozen_at": self._frozen_at.isoformat(),
            "scope": plan.scope, "unit": plan.unit, "dataset_kind": plan.dataset_kind,
            "case_count": len(plan.cases),
        }

    def observe(self, token: str, observation: FeedbackObservation) -> dict:
        with self._lock:
            plan = self._require_current(token)
            observation = observation.model_copy(deep=True)
            case = next((case for case in plan.cases if case.id == observation.case_id), None)
            if case is None or not case.not_before <= observation.observed_at <= self._clock():
                raise ValueError("结果必须属于冻结案例并在规定的观察时点之后。")
            previous = self._observations.get(case.id)
            if observation == previous:
                return {**self._metadata(plan), "status": "UNCHANGED"}
            if observation.revision != (previous.revision + 1 if previous is not None else 1):
                raise ValueError("必须按顺序更新当前观察版本。")
            if previous is not None:
                if previous.kind == "UNOBSERVED" and observation.kind != "UNOBSERVED":
                    raise ValueError("未执行行动的反事实不能改记为观察。")
                if previous.kind == "OBSERVED" and observation.observed_at != previous.observed_at:
                    raise ValueError("更正结果不能改写原观察时点。")
            self._observations[case.id] = observation
            self._revision += 1
            return {**self._metadata(plan), "status": "RECORDED"}

    def evaluate(self, token: str) -> dict:
        with self._lock:
            plan = self._require_current(token)
            metadata = self._metadata(plan)
            missing = [case.id for case in plan.cases if case.id not in self._observations
                       or self._observations[case.id].kind != "OBSERVED"]
            if missing:
                return {**metadata, "status": "UNKNOWN_INCOMPLETE_OUTCOMES", "missing_ids": missing}

            comparison = {}
            passes = True
            for reference in ("current", "baseline"):
                gains = [_gain_bounds(self._observations[case.id], getattr(case, reference),
                                      case.current + plan.adjustment) for case in plan.cases]
                absolute_min, absolute_max, low_min, low_max = (
                    sum(column, Decimal(0)) for column in zip(*gains, strict=True)
                )
                comparison[f"absolute_gain_vs_{reference}"] = [_money(absolute_min), _money(absolute_max)]
                comparison[f"underestimate_gain_vs_{reference}"] = [_money(low_min), _money(low_max)]
                passes = passes and absolute_min > 0 and low_min >= 0
            return {**metadata, **comparison, "status": "FINITE_GATE_MET" if passes else "FINITE_GATE_NOT_MET"}

    def transfer(self, token: str, request: FeedbackTransferInput) -> dict:
        """Compare shrinkage under separately declared target support assumptions."""
        with self._lock:
            plan = self._require_current(token)
            metadata = self._metadata(plan)
            if not request.confirmed or request.unit != plan.unit or request.target_scope == plan.scope:
                return {**metadata, "status": "UNKNOWN_TRANSFER"}
            lower = request.scale * request.reference_lower + request.offset_lower
            upper = request.scale * request.reference_upper + request.offset_upper
            raw = request.scale * plan.adjustment
            adjustment = Decimal(0)
            if raw > 0 and lower > 0:
                adjustment = min(raw, lower)
            elif raw < 0 and upper < 0:
                adjustment = max(raw, upper)
            return {
                **metadata, "status": "CONDITIONAL_RESEARCH_CANDIDATE", "target_scope": request.target_scope,
                "support_version": request.support_version, "target_support": [_money(lower), _money(upper)],
                "raw_adjustment": _money(raw), "adjustment": _money(adjustment),
                "worst_case_absolute_gain": _money(abs(adjustment)),
            }

    def rollback(self, token: str) -> dict:
        with self._lock:
            plan = self._require_current(token)
            metadata = self._metadata(plan)
            self._plan = None
            self._token = None
            self._frozen_at = None
            self._observations.clear()
            self._revision = 0
            return {**metadata, "status": "DISCARDED"}
