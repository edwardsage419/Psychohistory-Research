"""Isolated finite-model composition. Outputs have no decision authority."""

import hmac
from dataclasses import dataclass
from hashlib import sha256
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from .contracts import canonical

VERSION = "1.0.0"
MAX_WORLDS = 256
MAX_MODELS = 16
MAX_ACTIONS = 24
Identifier = Annotated[str, StringConstraints(min_length=1, max_length=128, strip_whitespace=True)]
Digest = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]
Mask = Annotated[str, StringConstraints(pattern=r"^(0|[1-9a-f][0-9a-f]{0,63})$")]
Worlds = Annotated[tuple[Identifier, ...], Field(max_length=MAX_WORLDS)]
SourceVersions = Annotated[tuple[Identifier, ...], Field(min_length=1, max_length=16)]
Quantity = Annotated[int, Field(ge=0, le=10**12)]
Actions = Annotated[tuple[Identifier, ...], Field(min_length=1, max_length=MAX_ACTIONS)]


class _Contract(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid", hide_input_in_errors=True)


class CompositionScope(_Contract):
    """The trusted host supplies the current scope and confirms joint coverage."""

    session_instance: Identifier
    authorization_epoch: Identifier
    evidence_epoch: Identifier
    revision: Annotated[int, Field(ge=1, le=2**53 - 1)]
    domain_id: Identifier
    domain_version: Identifier
    unit: Identifier
    horizon: Identifier
    exhaustive: bool
    worlds: Worlds
    purpose: Literal["isolated_research_replay"] = "isolated_research_replay"

    @model_validator(mode="after")
    def _unique_worlds(self):
        if len(set(self.worlds)) != len(self.worlds):
            raise ValueError("Joint world identifiers must be unique.")
        return self


class ValueGroup(_Contract):
    # Only a threshold may use null, meaning no finite qualifying value.
    # Missing evidence is represented by the absence of a world.
    value: Quantity | None
    worlds: Annotated[Worlds, Field(min_length=1)]


class GroupedPort(_Contract):
    scope: CompositionScope
    kind: Literal["threshold", "gain"]
    method_version: Identifier
    source_versions: SourceVersions
    groups: Annotated[tuple[ValueGroup, ...], Field(max_length=MAX_WORLDS)]


class ModelResult(_Contract):
    world: Identifier
    # No applicable model row excludes the hypothesis only in that world.
    # A row with null winners means the hypothesis remains viable but uncomputed.
    winners: Actions | None


class Hypothesis(_Contract):
    method_version: Identifier
    scope: CompositionScope
    source_versions: SourceVersions
    results: Annotated[tuple[ModelResult, ...], Field(max_length=MAX_WORLDS)]
    hypothesis_id: Identifier | None = None


@dataclass(frozen=True)
class _JoinJob:
    threshold: int | None
    gain: int
    support: int


@dataclass(frozen=True)
class _JoinPlan:
    scope: CompositionScope
    jobs: tuple[_JoinJob, ...]
    known: int
    digest: str
    dependencies: tuple[tuple[str, SourceVersions], ...]


class _Checkpoint(_Contract):
    cursor: Annotated[int, Field(ge=0, le=MAX_WORLDS)]
    passed: Mask
    failed: Mask
    mac: Digest


def _canonical(value) -> bytes:
    return canonical(value).encode("utf-8")


def _signature(key: bytes, digest: str, cursor: int, passed: int, failed: int) -> str:
    data = _canonical(["threshold_join", VERSION, digest, cursor, passed, failed])
    return hmac.new(key, data, sha256).hexdigest()


def _index(port: GroupedPort, domain: dict[str, int]) -> dict[str, int | None]:
    result = {}
    for group in port.groups:
        if port.kind == "gain" and group.value is None:
            raise ValueError("Gain port requires a numeric value.")
        for world in group.worlds:
            if world not in domain or world in result:
                raise ValueError("A grouped port has unknown or overlapping world support.")
            result[world] = group.value
    return result


def prepare_join(scope: CompositionScope, threshold: GroupedPort, gain: GroupedPort) -> _JoinPlan:
    """Compile a bounded joint support plan from two current host-qualified ports."""
    if threshold.kind != "threshold" or gain.kind != "gain" or threshold.scope != scope or gain.scope != scope:
        raise ValueError("Both ports must use the same current scope and the declared roles.")
    domain = {world: 1 << index for index, world in enumerate(scope.worlds)}
    thresholds, gains = _index(threshold, domain), _index(gain, domain)
    support_by_pair = {}
    known = 0
    for world, bit in domain.items():
        if world in thresholds and world in gains:
            values = (thresholds[world], gains[world])
            support_by_pair[values] = support_by_pair.get(values, 0) | bit
            known |= bit
    jobs = tuple(sorted(
        (_JoinJob(low, high, support) for (low, high), support in support_by_pair.items()),
        key=lambda job: (-job.support.bit_count(), job.support),
    ))
    digest = sha256(_canonical([
        VERSION, threshold.model_dump(mode="json"), gain.model_dump(mode="json"),
    ])).hexdigest()
    dependencies = tuple((port.method_version, port.source_versions) for port in (threshold, gain))
    return _JoinPlan(scope, jobs, known, digest, dependencies)


def _world_ids(scope: CompositionScope, mask: int) -> list[str]:
    worlds = []
    while mask:
        lowest_bit = mask & -mask
        worlds.append(scope.worlds[lowest_bit.bit_length() - 1])
        mask ^= lowest_bit
    return worlds


def advance_join(plan: _JoinPlan, current: CompositionScope, budget: int, *, signing_key: bytes,
                 checkpoint: dict | None = None, stop_on_mixed: bool = False) -> dict:
    """Advance at most budget joint comparisons. Plan preparation is separately bounded.

    Rebuild the trusted plan from current ports on restart. Only the checkpoint
    can come from a caller. The signing key stays in the local trusted host.
    """
    if current != plan.scope:
        raise ValueError("The joint calculation belongs to an earlier or different scope.")
    if type(budget) is not int or not 0 <= budget <= MAX_WORLDS:
        raise ValueError("The joint comparison budget is outside its integer bounds.")
    if type(signing_key) is not bytes or len(signing_key) < 32:
        raise ValueError("A trusted host signing key of at least 32 bytes is required.")
    result = {"version": VERSION, "authority": "NONE"}
    if not current.exhaustive:
        return {**result, "conclusion": "UNKNOWN_COVERAGE"}
    if not current.worlds:
        return {**result, "conclusion": "CONFLICT"}

    cursor = passed = failed = 0
    if checkpoint is not None:
        token = _Checkpoint.model_validate(checkpoint)
        cursor, passed, failed = token.cursor, int(token.passed, 16), int(token.failed, 16)
        signature = _signature(signing_key, plan.digest, cursor, passed, failed)
        if not hmac.compare_digest(token.mac, signature):
            raise ValueError("The joint calculation checkpoint is stale or invalid.")

    start = cursor
    for job in plan.jobs[cursor:cursor + budget]:
        if stop_on_mixed and passed and failed:
            break
        if job.threshold is not None and job.gain >= job.threshold:
            passed |= job.support
        else:
            failed |= job.support
        cursor += 1

    whole_domain = (1 << len(current.worlds)) - 1
    pending = plan.known & ~(passed | failed)
    missing = whole_domain & ~plan.known
    if passed and failed:
        conclusion = "CONDITIONAL_MIXED"
    elif pending or missing:
        conclusion = "UNKNOWN_GLOBAL"
    else:
        conclusion = "CONDITIONAL_ALL_PASS" if passed else "CONDITIONAL_ALL_FAIL"

    continuation = None
    if pending:
        continuation = {"cursor": cursor, "passed": format(passed, "x"), "failed": format(failed, "x"),
                        "mac": _signature(signing_key, plan.digest, cursor, passed, failed)}
    return {
        **result,
        "conclusion": conclusion,
        "dependency_sha256": plan.digest,
        "dependencies": [{"method_version": method, "sources": list(sources)}
                         for method, sources in plan.dependencies],
        "unit": current.unit,
        "horizon": current.horizon,
        "domain_id": current.domain_id,
        "domain_version": current.domain_version,
        "comparisons_used": cursor - start,
        "comparisons_remaining": len(plan.jobs) - cursor,
        "pass": _world_ids(current, passed),
        "fail": _world_ids(current, failed),
        "not_calculated": _world_ids(current, pending),
        "missing_evidence": _world_ids(current, missing),
        "pass_count_bounds": [passed.bit_count(), len(current.worlds) - failed.bit_count()],
        "fail_count_bounds": [failed.bit_count(), len(current.worlds) - passed.bit_count()],
        "witnesses": [
            {"threshold": job.threshold, "gain": job.gain, "worlds": _world_ids(current, job.support),
             "passes": bool(job.support & passed)}
            for job in plan.jobs[:cursor]
        ],
        "checkpoint": continuation,
    }


def compare_hypotheses(scope: CompositionScope, actions: Actions, hypotheses: tuple[Hypothesis, ...]) -> dict:
    """Preserve per-world competition and suppress global sets when coverage has gaps."""
    result = {"version": VERSION, "authority": "NONE"}
    if not scope.exhaustive:
        return {**result, "conclusion": "UNKNOWN_COVERAGE"}
    if not scope.worlds:
        return {**result, "conclusion": "CONFLICT"}
    if not actions or len(actions) > MAX_ACTIONS or len(set(actions)) != len(actions):
        raise ValueError("A bounded, nonempty, unique action set is required.")
    if len(hypotheses) > MAX_MODELS:
        raise ValueError("Too many competing hypotheses.")

    scoped_results = {world: {} for world in scope.worlds}
    model_names = set()
    for hypothesis in hypotheses:
        name = hypothesis.hypothesis_id or hypothesis.method_version
        if hypothesis.scope != scope or name in model_names:
            raise ValueError("A competing hypothesis has a stale scope or a duplicate identity.")
        model_names.add(name)
        for cell in hypothesis.results:
            if cell.world not in scoped_results or name in scoped_results[cell.world]:
                raise ValueError("A hypothesis must have one result per applicable world.")
            winners = None if cell.winners is None else set(cell.winners)
            if winners is not None and (not winners.issubset(actions) or len(winners) != len(cell.winners)):
                raise ValueError("Hypothesis winners must be unique and in the action set.")
            scoped_results[cell.world][name] = winners

    common = set(actions)
    possible = set()
    rows, missing = [], {}
    for world, world_results in scoped_results.items():
        unresolved = [name for name, winners in world_results.items() if winners is None]
        if not world_results or unresolved:
            missing[world] = unresolved
            continue
        world_common = set.intersection(*world_results.values())
        world_possible = set.union(*world_results.values())
        common &= world_common
        possible |= world_possible
        rows.append({"world": world, "models": list(world_results),
                     "common": [action for action in actions if action in world_common],
                     "possible": [action for action in actions if action in world_possible]})
    conclusion = ("PARTIAL_COVERAGE" if missing else
                  "CONDITIONAL_COMMON" if common else "CONDITIONAL_NO_COMMON")
    digest = sha256(_canonical([VERSION, scope.model_dump(mode="json"), actions,
                                [item.model_dump(mode="json") for item in hypotheses]])).hexdigest()
    return {**result, "conclusion": conclusion, "rows": rows, "missing": missing,
            "dependency_sha256": digest,
            "common": None if missing else [action for action in actions if action in common],
            "possible": None if missing else [action for action in actions if action in possible],
            "dependencies": [{"hypothesis": item.hypothesis_id or item.method_version,
                              "method_version": item.method_version, "sources": list(item.source_versions)}
                             for item in hypotheses]}
