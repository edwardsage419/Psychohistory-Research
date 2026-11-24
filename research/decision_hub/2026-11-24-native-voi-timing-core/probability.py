from __future__ import annotations
from fractions import Fraction
ONE = Fraction(1)

def _known(value: Probability | Quantity | None) -> bool:
    return bool(value and value.kind != 'unknown' and value.source.strip() and value.lower is not None
                and value.upper is not None and value.lower.is_finite() and value.upper.is_finite()
                and value.lower <= value.upper)


def _probability_row(keys, raw, description, errors, kinds) -> tuple[Bounds, ...] | None:
    bounds = []
    for key in keys:
        item = raw.get(key)
        if not _known(item) or not 0 <= item.lower <= item.upper <= 1:
            errors.append(f'{description}中「{key}」缺少有来源的概率上下界。')
            continue
        bounds.append((Fraction(item.lower), Fraction(item.upper)))
        kinds.add(item.kind)
    if len(bounds) != len(keys):
        return None
    lower, upper = map(sum, zip(*bounds, strict=True))
    if lower > 1 or upper < 1:
        errors.append(f'{description}的区间无法组成合计为 1 的概率。')
        return None
    return tuple((max(low, ONE - (upper - high)), min(high, ONE - (lower - low))) for low, high in bounds)


