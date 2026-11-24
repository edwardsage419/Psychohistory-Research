from __future__ import annotations
from fractions import Fraction
from itertools import combinations
# Research adapter: exact string representation; native scoring renderer omitted.
def _exact(v): return str(v)

def _sourced(value) -> bool:
    return value is not None and value.kind != "unknown" and bool(value.source.strip())


def _point(value) -> Fraction | None:
    if _sourced(value) and value.lower is not None and value.lower == value.upper:
        return Fraction(value.lower)
    return None


def _by(time: Fraction, cutoff: Cutoff) -> bool:
    deadline = Fraction(cutoff.at)
    return time < deadline or (time == deadline and cutoff.inclusive)


def _availability(timing: TimingInput, option_id: str, time: Fraction) -> str:
    rule = timing.actions.get(option_id)
    bounds = (timing.horizon, timing.decision_deadline, rule.cutoff if rule else None)
    if any(_sourced(item) and not _by(time, item) for item in bounds if item is not None):
        return "EXPIRED"
    if rule is None or any(not _sourced(item) for item in bounds if item is not None):
        return "UNKNOWN"
    return "FEASIBLE"


def immediate_availability(timing: TimingInput | None, option_id: str) -> str:
    """Check the confirmed time basis and action availability at its origin."""
    if timing is None or not timing.confirmed:
        return "UNKNOWN"
    if not timing.time_origin or not timing.time_unit or not _sourced(timing.horizon):
        return "UNKNOWN"
    return _availability(timing, option_id, Fraction())


def _relative(prediction: TimeValue | None, cutoff: Cutoff | None) -> str:
    if not _sourced(prediction) or prediction.lower is None or prediction.upper is None or not _sourced(cutoff):
        return "UNKNOWN"
    if not _by(Fraction(prediction.lower), cutoff):
        return "AFTER"
    if _by(Fraction(prediction.upper), cutoff):
        return "WITHIN"
    return "STRADDLES"


def _break_even(
    timing: TimingInput, lines: dict[str, dict[str, Affine]], baseline: Fraction, cost: Fraction,
) -> dict | None:
    horizon = Fraction(timing.horizon.at)
    split = {Fraction(), horizon}
    for cutoff in (timing.decision_deadline, *(r.cutoff for r in timing.actions.values())):
        if _sourced(cutoff) and Fraction(cutoff.at) < horizon:
            split.add(Fraction(cutoff.at))
    for choices in lines.values():
        for (a, da), (b, db) in combinations(choices.values(), 2):
            if da != db:
                cross = (a - b) / (da - db)
                if 0 < cross < horizon:
                    split.add(cross)

    def envelope(time):
        selected = []
        for choices in lines.values():
            eligible = [
                line for key, line in choices.items() if _availability(timing, key, time) == "FEASIBLE"
            ]
            if not eligible:
                return None
            selected.append(max(eligible, key=lambda line: line[0] - time * line[1]))
        return sum(line[0] for line in selected) - cost - baseline, sum(line[1] for line in selected)

    def profitable(time):
        line = envelope(time)
        return line is not None and line[0] > line[1] * time

    pieces = sorted(split)
    positive_through = [time for time in pieces if profitable(time)]
    for left, right in zip(pieces, pieces[1:]):
        line = envelope((left + right) / 2)
        if line is None:
            continue
        value, rate = line
        if value > left * rate:
            positive_through.append(min(right, value / rate) if rate else right)
    if not positive_through:
        return None
    latest = max(positive_through)
    return {"at": _exact(latest), "profitable_at_boundary": profitable(latest), "unit": timing.time_unit}


