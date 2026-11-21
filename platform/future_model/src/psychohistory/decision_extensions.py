"""Permissioned extension interface for future understanding and evidence adapters."""
import asyncio
from dataclasses import dataclass
from typing import Literal, Protocol

from pydantic import Field, TypeAdapter, ValidationError

from .decision_state import InputModel, Key, Kind, Text, TextLine

Capability = Literal["understanding", "evidence"]


class EvidenceItem(InputModel):
    id: Key
    label: Text
    kind: Kind
    source: TextLine = ""
    verification: Literal["user_supplied", "user_confirmed", "unverified"] = "unverified"
    scope: TextLine = ""


class AdapterSpec(InputModel):
    identity: Key
    version: Text
    capability: Capability
    mode: Literal["local", "external"]
    privacy_scope: Text
    free_confirmed: bool = Field(strict=True)
    maximum_input_bytes: int = Field(ge=1, le=32000, strict=True)
    timeout_ms: int = Field(ge=10, le=15000, strict=True)


class Candidate(InputModel):
    field: Literal["option", "objective", "constraint", "deadline", "preference", "evidence"]
    value: Text
    source: Text
    scope: TextLine = ""


@dataclass(frozen=True)
class AdapterPermit:
    capability: Capability
    identity: str
    allow_external: bool = False
    # Consent applies to the exact minimal query approved by the operator.
    approved_query: str = ""
    version: str = ""


class DecisionAdapter(Protocol):
    spec: AdapterSpec

    async def propose(self, query: str) -> list[dict]:
        """Return bounded, provisional suggestions. Implementations must honor cancellation."""


CandidateList = TypeAdapter(list[Candidate])


async def request_candidates(adapter: DecisionAdapter | None, capability: Capability,
                             query: str, permit: AdapterPermit | None = None):
    """The calculation layer receives no adapter output until the user confirms it."""
    if adapter is None:
        return {"status": "USER_SOURCE_REQUIRED", "proposals": []}
    try:
        spec = AdapterSpec.model_validate(adapter.spec)
        if (permit is None or permit.capability != capability or spec.capability != capability
                or permit.identity != spec.identity or permit.version != spec.version or permit.approved_query != query
                or not spec.free_confirmed or (spec.mode == "external" and not permit.allow_external)):
            return {"status": "PERMISSION_REQUIRED", "proposals": []}
        if not query.strip() or len(query.encode()) > spec.maximum_input_bytes:
            return {"status": "INVALID_QUERY", "proposals": []}
        async with asyncio.timeout(spec.timeout_ms / 1000):
            proposals = await adapter.propose(query)
        if not isinstance(proposals, list) or len(proposals) > 20:
            return {"status": "INVALID_RESULT", "proposals": []}
        checked = CandidateList.validate_python(proposals)
        if capability == "evidence" and any(item.field != "evidence" for item in checked):
            return {"status": "INVALID_RESULT", "proposals": []}
        return {"status": "NEEDS_CONFIRMATION", "provider_id": spec.identity, "provider_version": spec.version,
                "proposals": [item.model_dump(mode="json") for item in checked]}
    except TimeoutError:
        return {"status": "TIMEOUT", "proposals": []}
    except ValidationError:
        return {"status": "INVALID_RESULT", "proposals": []}
    except Exception:
        return {"status": "FAILED", "proposals": []}
