from fractions import Fraction

type Points = dict[str, tuple[Fraction, ...]]
type Bound = tuple[Fraction, Fraction]
type Intervals = dict[str, tuple[Bound, ...]]


def _validate(ctx: 'Context', *, point: bool = False) -> list[str]:
    state = ctx.state
    errors = []
    if not ctx.feasible:
        errors.append('需要至少一个通过硬约束的方案。')
    if not state.scenarios:
        errors.append('需要至少一个有定义的情景。')
    if not state.scenario_basis or not state.scenario_basis.strip():
        errors.append('需要确认情景共用的时限、同一基数效用量尺和效用越高越好的含义。')
    units, horizons = set(), set()
    for scenario in state.scenarios:
        if scenario.kind == 'unknown':
            errors.append(f'情景「{scenario.label}」的依据为 UNKNOWN。')
        elif not scenario.source.strip():
            errors.append(f'需要补充情景「{scenario.label}」的来源。')
        for option in ctx.feasible:
            utility = scenario.utilities.get(option.id)
            cell = f'方案「{option.label}」在情景「{scenario.label}」中的效用'
            if utility is None or utility.kind == 'unknown' or utility.lower is None or utility.upper is None:
                errors.append(f'{cell}为 UNKNOWN，需要有依据的上下界。')
                continue
            if not utility.lower.is_finite() or not utility.upper.is_finite() or utility.lower > utility.upper:
                errors.append(f'{cell}须具有有序的有限上下界。')
            elif point and utility.lower != utility.upper:
                errors.append(f'{cell}须为点值。')
            if not utility.source.strip():
                errors.append(f'需要补充{cell}的来源。')
            units.add(utility.unit.strip())
            horizon = utility.horizon or state.deadline
            horizons.add(horizon.strip() if horizon is not None else None)
    if '' in units or len(units) > 1:
        errors.append('所有方案和情景须使用同一明确的效用单位。')
    if None in horizons or len(horizons) > 1:
        errors.append('所有方案和情景须使用同一明确的效用时间范围。')
    return errors


def _validate_points(ctx: 'Context') -> list[str]:
    return _validate(ctx, point=True)


def _validate_precision(ctx: 'Context') -> list[str]:
    errors = _validate_points(ctx)
    radius = ctx.state.precision_radius
    if radius is None or not radius.is_finite() or radius < 0:
        errors.append('需要以效用单位计量、有限且非负的假设统一半径。')
    if len(ctx.feasible) < 2:
        errors.append('需要至少两个通过硬约束的方案才能比较精度阈值。')
    return errors


def _point_regret(utilities: Points) -> Points:
    maxima = [max(column) for column in zip(*utilities.values(), strict=True)]
    return {
        key: tuple(ceiling - value for ceiling, value in zip(maxima, row, strict=True))
        for key, row in utilities.items()
    }


def _regret_bounds(utilities: Intervals) -> Intervals:
    regret = {}
    for key, cells in utilities.items():
        row = []
        for index, (lower, upper) in enumerate(cells):
            competitors = [other[index] for rival, other in utilities.items() if rival != key]
            lower_regret = max(Fraction(0), max((low - upper for low, _ in competitors), default=Fraction(0)))
            upper_regret = max(Fraction(0), max((high - lower for _, high in competitors), default=Fraction(0)))
            row.append((lower_regret, upper_regret))
        regret[key] = tuple(row)
    return regret


def _rectangle(ctx: 'Context') -> bool:
    return bool(
        ctx.state.scenario_dependence == 'rectangle'
        and ctx.state.scenario_dependence_source
        and ctx.state.scenario_dependence_source.strip()
    )


def _precision_threshold(points: Points, leader: str) -> Fraction:
    # Before clipping at zero, the worst regret bounds are g(a) ± 2e.
    # For a strict comparison the rival's lower bound must also be positive.
    gaps = {
        key: max(rival - own for competitor, other in points.items() if competitor != key
                 for own, rival in zip(row, other, strict=True))
        for key, row in points.items()
    }
    return min(min(gap / 2, (gap - gaps[leader]) / 4) for key, gap in gaps.items() if key != leader)


