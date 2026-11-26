"""Separate, offline staging boundary for structured public observations."""
from dataclasses import dataclass
from datetime import UTC, date, datetime
from hashlib import sha256
import json
import re
from types import MappingProxyType
from urllib.parse import urlsplit


VERSION = "public-fact-quarantine@1.0.0"
MAX_PAYLOAD_BYTES = 4096
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
        if (origin.scheme != "https" or not origin.hostname or origin.username or origin.password
                or origin.query or origin.fragment):
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


def knowledge_network_status():
    return {
        "version": VERSION, "status": "OFFLINE_ONLY", "authority": "NONE",
        "quarantine": "LOCAL_STRUCTURED_IMPORT_BOUNDARY", "active_source_count": 0,
        "network_connector_available": False, "egress_allowed": False, "remote_updates": "NOT_IMPLEMENTED",
    }
