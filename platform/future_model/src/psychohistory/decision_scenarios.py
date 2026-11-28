"""Ground explicitly stated, common-scale scenario scores for native C029."""

from hashlib import sha256
import re


PREFIX = "scenario-points:"
BASIS_FIELD = "scenario-basis"
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


def confirmed_scenarios(claims, options):
    """A partial or conflicting score set never becomes a scenario comparison."""
    groups = {}
    options = {option["label"]: option["id"] for option in options if option["status"] == "CONFIRMED"}
    for claim in claims:
        if not claim["field"].startswith(PREFIX) or claim["status"] == "SUPERSEDED":
            continue
        if claim["status"] not in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"} or claim["subject"] not in options:
            return None
        label = claim["field"].removeprefix(PREFIX)
        scores = groups.setdefault(label, {})
        option_id = options[claim["subject"]]
        if option_id in scores:
            return None
        scores[option_id] = {"lower": claim["value"], "upper": claim["value"],
                             "unit": "分", "kind": "assumption", "source": claim["source"]}
    if not groups:
        return None
    basis = [item for item in claims if item["field"] == BASIS_FIELD and item["status"] != "SUPERSEDED"]
    qualified = len(basis) == 1 and basis[0]["status"] in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}
    horizon = basis[0]["value"] if qualified else None
    if horizon:
        for scores in groups.values():
            for score in scores.values():
                score["horizon"] = horizon
    scenarios = [{"id": "talk-" + sha256(label.encode()).hexdigest()[:22],
                  "label": label, "utilities": scores, "kind": "assumption",
                  "source": "用户核对的情景评分，统一使用分，未提供概率。"}
                 for label, scores in groups.items()]
    return scenarios, basis[0]["source"] if qualified else None
