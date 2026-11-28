"""Structured public observations and host-owned parameter qualification."""
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from hashlib import sha256
import json
import re
from threading import RLock
from types import MappingProxyType
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4


VERSION = "public-fact-quarantine@1.0.0"
PARAMETER_CONTRACT = "qualified-public-parameter@1.0.0"
MAX_PAYLOAD_BYTES = 4096
MAX_SOURCES = 32
MAX_TICKETS = 256
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
DECIMAL_TEXT = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?")


@dataclass(frozen=True, slots=True)
class PublicFactSource:
    """Allowlist entry supplied by a trusted host, outside the imported payload."""

    id: str
    url: str
    publisher: str
    version: str
    licence: str
    unit: str
    max_age_days: int

    def __post_init__(self):
        if not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", self.id):
            raise ValueError("source id must be stable")
        if not all(isinstance(value, str) and 0 < len(value.strip()) <= 500
                   for value in (self.url, self.publisher, self.version, self.licence, self.unit)):
            raise ValueError("source requires publisher, version, licence and unit")
        origin = urlsplit(self.url)
        if (origin.scheme != "https" or not origin.hostname or origin.username is not None
                or origin.password is not None or origin.query or origin.fragment
                or any(char.isspace() or ord(char) < 32 or char in "\\?#" for char in self.url)):
            raise ValueError("source requires a fixed HTTPS URL with no credentials, query or fragment")
        if type(self.max_age_days) is not int or not 0 <= self.max_age_days <= 366:
            raise ValueError("source requires a fixed freshness window")


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON property")
        result[key] = value
    return result


def _parse(raw):
    if type(raw) is not bytes or len(raw) > MAX_PAYLOAD_BYTES:
        raise ValueError("payload needs bounded UTF-8 JSON bytes")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)
    if not isinstance(data, dict) or data.keys() != {"observed_on", "value"}:
        raise ValueError("payload fields outside schema")
    if not isinstance(data["observed_on"], str) or not ISO_DATE.fullmatch(data["observed_on"]):
        raise ValueError("invalid observation date")
    value = data["value"]
    if not isinstance(value, str) or len(value) > 40 or not DECIMAL_TEXT.fullmatch(value):
        raise ValueError("value must be a finite decimal string")
    return date.fromisoformat(data["observed_on"]), value


class ExternalFactQuarantine:
    """Parse an explicitly supplied public payload; no transport, storage or promotion."""

    def __init__(self, sources=()):
        allowlist = {}
        for source in sources:
            if not isinstance(source, PublicFactSource) or source.id in allowlist:
                raise ValueError("public source allowlist requires unique validated entries")
            allowlist[source.id] = source
        self._sources = MappingProxyType(allowlist)

    def stage(self, source_id, retrieved_from, raw_payload, *, as_of=None):
        source = self._sources.get(source_id) if isinstance(source_id, str) else None
        if source is None or retrieved_from != source.url:
            return {"status": "SOURCE_NOT_ALLOWED", "authority": "NONE"}
        if raw_payload is None:
            return {"status": "OFFLINE_UNAVAILABLE", "authority": "NONE"}
        as_of = as_of if as_of is not None else datetime.now(UTC).date()
        if type(as_of) is not date:
            raise ValueError("a trusted calendar date is required")
        try:
            observed_on, value = _parse(raw_payload)
        except (ValueError, RecursionError):
            return {"status": "REJECTED_PAYLOAD", "authority": "NONE"}
        age_days = (as_of - observed_on).days
        if age_days < 0:
            return {"status": "REJECTED_PAYLOAD", "authority": "NONE"}
        return {
            "status": "QUARANTINED", "version": VERSION, "authority": "NONE",
            "transport_identity": "UNVERIFIED_IMPORT", "payload_sha256": sha256(raw_payload).hexdigest(),
            "source": {
                "id": source.id, "url": source.url, "publisher": source.publisher,
                "version": source.version, "licence": source.licence,
            },
            "observation": {"observed_on": observed_on.isoformat(), "value": value, "unit": source.unit},
            "freshness": "FRESH_FOR_REVIEW" if age_days <= source.max_age_days else "STALE",
            "freshness_as_of": as_of.isoformat(), "max_age_days": source.max_age_days,
        }


@dataclass(frozen=True, slots=True)
class ParameterScope:
    subject: str
    metric: str
    unit: str
    horizon: str
    scenario: str
    purpose: str

    def __post_init__(self):
        fields = (self.subject, self.metric, self.unit, self.horizon, self.scenario, self.purpose)
        if any(not isinstance(field, str) or not field.strip() or len(field) > 400 for field in fields):
            raise ValueError("parameter scope requires bounded, explicit fields")


@dataclass(frozen=True, slots=True)
class QualifiedParameter:
    """A point-in-time resolution. The host re-resolves the ticket at publication."""

    value: Decimal
    scope: ParameterScope
    source_id: str
    source_url: str
    source_version: str
    payload_sha256: str
    observed_on: str
    freshness_as_of: str
    contract: str = PARAMETER_CONTRACT


@dataclass(frozen=True, slots=True)
class _SourceSnapshot:
    source: PublicFactSource
    raw: bytes | None = None
    transport: str = "UNVERIFIED_IMPORT"

    def stage(self, as_of):
        source = self.source
        result = ExternalFactQuarantine((source,)).stage(source.id, source.url, self.raw, as_of=as_of)
        if result["status"] == "QUARANTINED":
            result["transport_identity"] = self.transport
        return result


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _read_public_json(url):
    request = Request(url, headers={"Accept": "application/json"}, method="GET")
    with build_opener(_NoRedirects()).open(request, timeout=5) as response:
        if response.headers.get_content_type() != "application/json":
            return b""
        return response.read(MAX_PAYLOAD_BYTES + 1)


class PublicFactCache:
    """Opt-in, in-memory adapter. Source configuration and tickets belong to the trusted host."""

    def __init__(self, sources=()):
        self._lock = RLock()
        self._sources = {}
        self._tickets = {}
        for source in sources:
            if not isinstance(source, PublicFactSource) or source.id in self._sources:
                raise ValueError("public source allowlist requires unique validated entries")
            self.set_source(source)

    def _drop_tickets(self, source_id):
        self._tickets = {ticket: entry for ticket, entry in self._tickets.items() if entry[0] != source_id}

    def set_source(self, source):
        if not isinstance(source, PublicFactSource):
            raise ValueError("a validated public source is required")
        with self._lock:
            current = self._sources.get(source.id)
            if current is None and len(self._sources) >= MAX_SOURCES:
                raise ValueError("public fact source limit exceeded")
            if current is None or current.source != source:
                self._sources[source.id] = _SourceSnapshot(source)
                self._drop_tickets(source.id)

    def withdraw(self, source_id):
        with self._lock:
            self._sources.pop(source_id, None)
            self._drop_tickets(source_id)

    def _commit(self, current, raw, *, transport, as_of):
        candidate = _SourceSnapshot(current.source, raw, transport)
        result = candidate.stage(as_of)
        if result["status"] != "QUARANTINED" or candidate == current:
            return result
        if current.raw is not None:
            current_date, _ = _parse(current.raw)
            if result["observation"]["observed_on"] < current_date.isoformat():
                return {"status": "OLDER_OBSERVATION", "authority": "NONE"}
        self._sources[current.source.id] = candidate
        self._drop_tickets(current.source.id)
        return result

    def stage(self, source_id, retrieved_from, raw_payload, *, as_of=None):
        with self._lock:
            current = self._sources.get(source_id)
            if current is None or retrieved_from != current.source.url:
                return {"status": "SOURCE_NOT_ALLOWED", "authority": "NONE"}
            return self._commit(current, raw_payload, transport="UNVERIFIED_IMPORT", as_of=as_of)

    def cached(self, source_id, *, as_of=None):
        with self._lock:
            current = self._sources.get(source_id)
            if current is None:
                return {"status": "SOURCE_NOT_ALLOWED", "authority": "NONE"}
            return current.stage(as_of)

    def fetch(self, source_id, *, allow_network=False, as_of=None):
        with self._lock:
            current = self._sources.get(source_id)
            if current is None:
                return {"status": "SOURCE_NOT_ALLOWED", "authority": "NONE"}
            if allow_network is not True:
                return {"status": "NETWORK_DISABLED", "authority": "NONE"}
        try:
            raw = _read_public_json(current.source.url)
        except (OSError, ValueError):
            raw = None
        with self._lock:
            if self._sources.get(source_id) is not current:
                return {"status": "SOURCE_CHANGED", "authority": "NONE"}
            if raw is None:
                result = current.stage(as_of)
                if result["status"] == "QUARANTINED":
                    return {**result, "availability": "CACHED_OFFLINE"}
                return {"status": "NETWORK_UNAVAILABLE", "authority": "NONE"}
            return self._commit(current, raw, transport="HTTPS_RETRIEVED", as_of=as_of)

    def qualify(self, source_id, scope, *, epoch, verify, as_of=None):
        """An independently verified, fresh observation can earn one purpose-scoped ticket."""
        if not isinstance(scope, ParameterScope) or not isinstance(epoch, str) or not 0 < len(epoch) <= 256:
            raise ValueError("a qualified parameter scope and authorization epoch are required")
        with self._lock:
            current = self._sources.get(source_id)
            if current is None or current.source.unit != scope.unit:
                return None
            staged = current.stage(as_of)
        if staged.get("freshness") != "FRESH_FOR_REVIEW":
            return None
        try:
            accepted = verify(staged, scope) is True
        except Exception:
            return None
        with self._lock:
            if (not accepted or self._sources.get(source_id) is not current
                    or current.stage(as_of).get("freshness") != "FRESH_FOR_REVIEW"):
                return None
            if len(self._tickets) >= MAX_TICKETS:
                raise ValueError("public parameter ticket limit exceeded")
            ticket = uuid4().hex
            self._tickets[ticket] = (source_id, scope, epoch)
            return ticket

    def revoke(self, ticket):
        with self._lock:
            self._tickets.pop(ticket, None)

    def resolve(self, ticket, scope, *, epoch, as_of=None):
        if not isinstance(ticket, str) or not isinstance(scope, ParameterScope) or not isinstance(epoch, str):
            return None
        with self._lock:
            grant = self._tickets.get(ticket)
            if grant is None or grant[1:] != (scope, epoch):
                return None
            current = self._sources[grant[0]]
            result = current.stage(as_of)
            if result.get("freshness") != "FRESH_FOR_REVIEW":
                return None
            observation, source = result["observation"], current.source
            return QualifiedParameter(
                value=Decimal(observation["value"]), scope=scope, source_id=source.id,
                source_url=source.url, source_version=source.version, payload_sha256=result["payload_sha256"],
                observed_on=observation["observed_on"], freshness_as_of=result["freshness_as_of"],
            )


def knowledge_network_status():
    return {
        "version": VERSION, "status": "OFFLINE_ONLY", "authority": "NONE",
        "quarantine": "LOCAL_STRUCTURED_IMPORT_BOUNDARY", "active_source_count": 0,
        "network_connector_available": False, "egress_allowed": False, "remote_updates": "NOT_IMPLEMENTED",
        "host_adapter": PARAMETER_CONTRACT,
    }
