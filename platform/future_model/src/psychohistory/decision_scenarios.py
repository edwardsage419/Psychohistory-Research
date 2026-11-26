"""Ground explicitly stated, common-scale scenario scores for native C029."""

from hashlib import sha256
import re
from unicodedata import normalize


PREFIX = "scenario-points:"
BASIS_FIELD = "scenario-basis"
_BASIS_SCOPE = BASIS_FIELD + ":"
_BASIS = re.compile(r"都比较([^，,。；;]{1,40})[，,]分差可比较[，,]分数越高越好")
_HEADER = re.compile(r"情景([^：:，,。；;\n]{1,40})[:：]\s*(.+)")
_SCORE = re.compile(r"([^，,。；;\n]{1,80}?)\s*得\s*(-?[0-9]{1,10}(?:\.[0-9]{1,6})?)\s*分")


def scenario_candidates(text, labels):
    """Accept only complete explicitly labelled score statements."""
    labels = set(labels)
    for clause in re.split(r"[。；;\n！？?]", text):
        basis = _BASIS.fullmatch(clause.strip())
        if basis:
            yield {"kind": "scenario_score", "field": BASIS_FIELD, "subject": "", "value": basis[1],
                   "unit": "", "source": clause.strip()}
            continue
        header = _HEADER.fullmatch(clause.strip())
        if not header:
            continue
        scores = [_SCORE.fullmatch(item.strip()) for item in re.split(r"[，,]", header[2])]
        if len(scores) < 2 or any(item is None for item in scores):
            continue
        subjects = [item[1].strip(" 「」『』") for item in scores]
        if len(set(subjects)) != len(subjects) or not set(subjects) <= labels:
            continue
        for score, subject in zip(scores, subjects, strict=True):
            yield {
                "kind": "scenario_score", "field": PREFIX + header[1].strip(),
                "subject": subject, "value": score[2], "unit": "分", "source": clause.strip(),
            }


def draft_scenario_claims(ledger, text, labels, *, metadata, dismissed=()):
    """Bind new score proposals to the exact basis offered with them."""
    from .decision_evidence import draft_claims

    candidates = [
        {**claim, "kind": "assumption", "role": "scenario_score", "metadata": metadata}
        for claim in scenario_candidates(text, labels) if len(claim["source"]) <= 400
    ]
    offered_bases = [claim for claim in candidates if claim["field"] == BASIS_FIELD]
    ledger = draft_claims(ledger, offered_bases, dismissed=dismissed)
    inactive = set(dismissed) | {entry.supersedes for entry in ledger.entries}
    active = [entry for entry in ledger.entries
              if entry.claim.field == BASIS_FIELD and entry.claim_id not in inactive]
    if offered_bases:
        # An explicitly supplied basis belongs to this turn's score statements,
        # even while the user still has to link it as a correction.
        sources = {item["source"] for item in offered_bases}
        active = [entry for entry in active if entry.claim.source in sources]
    scope = (_BASIS_SCOPE + active[0].claim_id) if len(active) == 1 else None
    scores = ({**claim, "metadata": {**metadata, "scope": scope}}
              for claim in candidates if claim["field"].startswith(PREFIX))
    return draft_claims(ledger, scores, dismissed=dismissed)


def confirmed_scenarios(claims, options):
    """Keep unknown coverage when a confirmed basis invalidates old scores."""
    history = [item for item in claims if item["field"] == BASIS_FIELD]
    active = [item for item in history if item["status"] not in {"DISMISSED", "SUPERSEDED"}]
    if len(active) != 1 or active[0]["status"] not in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}:
        return None
    basis = active[0]
    basis_metadata = basis["metadata"] or {}
    scope = _BASIS_SCOPE + basis["id"]
    # Before the first basis there is no older scale to reinterpret. The
    # user's first explicit common-scale declaration may cover those scores.
    initial_basis = len(history) == 1
    groups = {}
    seen = {}
    options = {option["label"]: option["id"] for option in options if option["status"] == "CONFIRMED"}
    for claim in claims:
        if not claim["field"].startswith(PREFIX) or claim["status"] in {"SUPERSEDED", "DISMISSED"}:
            continue
        label = normalize("NFC", claim["field"].removeprefix(PREFIX))
        scores = groups.setdefault(label, {})
        metadata = claim["metadata"] or {}
        if metadata.get("scope") != scope and not (initial_basis and not metadata.get("scope")):
            continue
        if claim["status"] not in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"} or claim["subject"] not in options:
            return None
        if (metadata.get("channel"), metadata.get("source_identity")) != (
            basis_metadata.get("channel"), basis_metadata.get("source_identity")
        ):
            return None
        option_id = options[claim["subject"]]
        key = (label, option_id)
        signature = (claim["value"], claim["unit"], {**metadata, "scope": scope})
        if key in seen:
            if seen[key] != signature:
                return None
            continue
        seen[key] = signature
        scores[option_id] = {"lower": claim["value"], "upper": claim["value"],
                             "unit": "分", "kind": "assumption", "source": claim["source"],
                             "horizon": basis["value"]}
    scenarios = [{"id": "talk-" + sha256(label.encode()).hexdigest()[:22],
                  "label": label, "utilities": scores, "kind": "assumption",
                  "source": "用户核对的情景评分，统一使用分，未提供概率。"}
                 for label, scores in groups.items()]
    return (scenarios, basis["source"]) if scenarios else None
