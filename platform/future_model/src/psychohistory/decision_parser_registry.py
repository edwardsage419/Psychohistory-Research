"""Reviewed local parsers can emit source-grounded alternatives for inspection."""

from collections.abc import Callable
from dataclasses import asdict, dataclass
from hashlib import sha256
import re
from threading import RLock


@dataclass(frozen=True)
class RawTurn:
    text: str
    session_instance: str
    revision: int
    turn_index: int
    authority_generation: int

    def describe(self):
        return {"contract": "1.0.0", "raw_sha256": sha256(self.text.encode("utf-8")).hexdigest(),
                "encoding": "unicode_code_points", "session_instance": self.session_instance,
                "turn_index": self.turn_index, "revision": self.revision,
                "authority_generation": self.authority_generation}


@dataclass(frozen=True)
class ParserSpec:
    name: str
    version: str
    source: str
    capabilities: tuple[str, ...]
    maximum_input_bytes: int = 12000

    @property
    def key(self):
        return f"{self.name}@{self.version}"


class ParserRegistry:
    """Accept only explicit, reviewed in-process registrations during assembly.

    Application callers cannot register modules. The host projects actionable
    claims using its own parser and shows these outputs as provisional candidates.
    """

    def __init__(self):
        self._lock = RLock()
        self._known: dict[str, tuple[ParserSpec, Callable]] = {}
        self._enabled: dict[str, None] = {}

    def register(self, spec: ParserSpec, parse: Callable[[RawTurn], list[dict]]):
        if (not re.fullmatch(r"[a-z][a-z0-9_]{1,63}@[0-9]+\.[0-9]+\.[0-9]+", spec.key)
                or not spec.source.strip() or not spec.capabilities or not callable(parse)
                or not 1 <= spec.maximum_input_bytes <= 16000):
            raise ValueError("Invalid local parser contract")
        with self._lock:
            if spec.key in self._known or len(self._known) >= 8:
                raise ValueError("Duplicate parser version or registry full")
            self._known[spec.key] = (spec, parse)

    def enable(self, key):
        with self._lock:
            if key not in self._known:
                raise ValueError("Unknown parser version")
            self._enabled[key] = None

    def disable(self, key):
        with self._lock:
            self._enabled.pop(key, None)

    def describe(self):
        with self._lock:
            return [{**asdict(spec), "key": key, "enabled": key in self._enabled,
                     "permission": "LOCAL_SOURCE_ONLY", "authority": "NONE"}
                    for key, (spec, _) in self._known.items()]

    def propose(self, raw: RawTurn):
        with self._lock:
            entries = [self._known[key] for key in self._enabled]
        output = []
        for spec, parse in entries:
            candidates = []
            status = "NEEDS_CONFIRMATION"
            if len(raw.text.encode("utf-8")) > spec.maximum_input_bytes:
                status = "INPUT_LIMIT"
            else:
                try:
                    candidates = _ground(raw.text, parse(raw))
                except ValueError:
                    status = "INVALID_OUTPUT"
                except Exception:
                    status = "PARSER_FAILED"
            output.append({"key": spec.key, "status": status, "authority": "NONE",
                           "candidates": candidates})
        return output


def _ground(text, items):
    if not isinstance(items, list) or len(items) > 96:
        raise ValueError("Invalid candidates")
    checked = []
    for item in items:
        if not isinstance(item, dict) or set(item) != {"source", "start", "end", "kind"}:
            raise ValueError("Invalid candidate fields")
        start, end = item["start"], item["end"]
        source, kind = item["source"], item["kind"]
        if (type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text)
                or not 1 <= end - start <= 400 or text[start:end] != source
                or not isinstance(kind, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,39}", kind)):
            raise ValueError("Invalid source anchor")
        checked.append({"source": source, "span": {"start": start, "end": end}, "kind": kind})
    return checked
