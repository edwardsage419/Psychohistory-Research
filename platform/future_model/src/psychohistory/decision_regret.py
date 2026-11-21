"""Scenario regret methods, evaluated on the hard-constraint ACCEPT set."""

from fractions import Fraction
from typing import TYPE_CHECKING

from .decision_registry import Method

if TYPE_CHECKING:
    from .decision_registry import Context


POINT_SOURCE = 'research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md'
INTERVAL_SOURCE = 'research/decision_methods/C030_INTERVAL_BOUNDED_SCENARIO_REGRET_2026-11-20.md'
PRECISION_SOURCE = 'research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md'
WITNESS_SOURCE = 'research/decision_methods/C031_ADDENDUM_SHARP_THRESHOLD_COUNTEREXAMPLE_2026-11-20.md'

type Points = dict[str, tuple[Fraction, ...]]
type Bound = tuple[Fraction, Fraction]
type Intervals = dict[str, tuple[Bound, ...]]


def _decimal(value: Fraction) -> str:
    """Render exact finite decimals, including results beyond Decimal's default precision."""
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        raise ValueError('Regret requires a finite decimal representation')
    places = max(twos, fives)
    digits = str(abs(value.numerator) * 2 ** (places - twos) * 5 ** (places - fives))
    if places:
        digits = digits.zfill(places + 1)
        digits = f'{digits[:-places]}.{digits[-places:]}'
    return f'-{digits}' if value < 0 else digits


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


def _utilities(ctx: 'Context') -> Intervals:
    return {
        option.id: tuple(
            (Fraction(scenario.utilities[option.id].lower), Fraction(scenario.utilities[option.id].upper))
            for scenario in ctx.state.scenarios
        )
        for option in ctx.feasible
    }


def _labels(ctx: 'Context') -> dict[str, str]:
    return {option.id: option.label for option in ctx.feasible}


def _unit(ctx: 'Context') -> str:
    return ctx.state.scenarios[0].utilities[ctx.feasible[0].id].unit.strip()


def _leaders(values: dict[str, Fraction], *, highest: bool = False) -> list[str]:
    target = (max if highest else min)(values.values())
    return [key for key, value in values.items() if value == target]


def _point_regret(utilities: Points) -> Points:
    maxima = [max(column) for column in zip(*utilities.values(), strict=True)]
    return {
        key: tuple(ceiling - value for ceiling, value in zip(maxima, row, strict=True))
        for key, row in utilities.items()
    }


def _point_results(ctx: 'Context') -> dict:
    labels = _labels(ctx)
    scenarios = [scenario.label for scenario in ctx.state.scenarios]
    unit = _unit(ctx)
    points = {key: tuple(low for low, _ in row) for key, row in _utilities(ctx).items()}
    regret = _point_regret(points)
    worst = {key: max(row) for key, row in regret.items()}
    minimum_utility = {key: min(row) for key, row in points.items()}
    leaders = _leaders(worst)
    maximin = _leaders(minimum_utility, highest=True)
    scenario_best = [
        [key for key, row in regret.items() if row[index] == 0]
        for index in range(len(scenarios))
    ]
    worst_scenarios = {
        key: [label for label, value in zip(scenarios, row, strict=True) if value == worst[key]]
        for key, row in regret.items()
    }
    printable = {key: [_decimal(value) for value in row] for key, row in regret.items()}
    tables = [
        {
            'title': f'各情景后悔值（{unit}）', 'columns': ['方案', *scenarios],
            'rows': [[label, *printable[key]] for key, label in labels.items()],
        },
        {
            'title': '各情景的最优可行方案', 'columns': ['情景', '最优方案（含并列）'],
            'rows': [[scenario, '、'.join(labels[key] for key in best)]
                     for scenario, best in zip(scenarios, scenario_best, strict=True)],
        },
        {
            'title': f'最大后悔值与最小效用（{unit}）',
            'columns': ['方案', '最大后悔值', '最坏情景（含并列）', '最小效用'],
            'rows': [[label, _decimal(worst[key]), '、'.join(worst_scenarios[key]), _decimal(minimum_utility[key])]
                     for key, label in labels.items()],
        },
    ]
    reference_id = ctx.state.reference_option_id
    reference = None
    reference_note = '可确认一个可行方案作为参照。'
    if reference_id in points:
        reference = {'option_id': reference_id, 'scenario_gains': printable[reference_id]}
        tables.append({
            'title': f'相对参照方案「{labels[reference_id]}」的条件性效用增益（{unit}）',
            'columns': ['情景', '完全预知情景后的效用增益'],
            'rows': [[scenario, gain] for scenario, gain in zip(scenarios, printable[reference_id], strict=True)],
        })
        reference_note = '预知增益以承诺前完全识别情景且仍能改选为条件。实际信息价值还取决于误差、费用和等待时间。'
    elif reference_id is not None:
        reference_note = '所选参照方案尚未通过硬约束，参照增益为 UNKNOWN。'
    return {
        'summary': (
            f'最小化最大后悔值的方案为「{"、".join(labels[key] for key in leaders)}」。'
            f'最大化最小效用的方案为「{"、".join(labels[key] for key in maximin)}」。'
            f'比较仅覆盖所列情景，按无概率权重的规则计算。{reference_note}'
        ),
        'tables': tables,
        'charts': [{
            'title': '最大情景后悔值', 'unit': unit,
            'rows': [{'label': label, 'lower': _decimal(worst[key]), 'upper': _decimal(worst[key])}
                     for key, label in labels.items()],
        }],
        'leaders': leaders,
        'maximin_leaders': maximin,
        'regret': printable,
        'worst_regret': {key: _decimal(value) for key, value in worst.items()},
        'scenario_best': scenario_best,
        'worst_scenarios': worst_scenarios,
        'reference': reference,
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


def _interval_results(ctx: 'Context', utilities: Intervals) -> dict:
    labels = _labels(ctx)
    scenarios = [scenario.label for scenario in ctx.state.scenarios]
    unit = _unit(ctx)
    regret = _regret_bounds(utilities)
    worst = {
        key: (max(low for low, _ in row), max(high for _, high in row))
        for key, row in regret.items()
    }
    leaders = _leaders({key: high for key, (_, high) in worst.items()})
    strict = [key for key in leaders if len(worst) > 1
              and all(worst[key][1] < low for rival, (low, _) in worst.items() if rival != key)]
    midpoint = _point_regret({key: tuple((low + high) / 2 for low, high in row) for key, row in utilities.items()})
    midpoint_worst = {key: max(row) for key, row in midpoint.items()}
    midpoint_leaders = _leaders(midpoint_worst)
    bound_type = 'sharp' if _rectangle(ctx) else 'outer'
    if bound_type == 'sharp':
        scope = '以声明的矩形假设计算，每个方案的极值分别可达。'
    else:
        scope = '矩形独立性尚未确立，结果为保守外界，适用于非空且落在所给区间内的联合可行集。'
    if strict:
        comparison = f'「{labels[strict[0]]}」的上界严格低于所有其他方案的下界。'
    elif len(worst) > 1:
        comparison = '区间交叠或接触，按界限无法认证任何方案在每个联合取值下的严格优势。'
    else:
        comparison = '目前只有一个可行方案。'
    return {
        'summary': f'最大情景后悔值上界最小的方案为「{"、".join(labels[key] for key in leaders)}」。{comparison}{scope}',
        'tables': [
            {
                'title': f'各情景后悔值区间（{unit}）',
                'columns': ['方案', *scenarios],
                'rows': [[label, *(f'[{_decimal(low)}, {_decimal(high)}]' for low, high in regret[key])]
                         for key, label in labels.items()],
            },
            {
                'title': f'最大情景后悔值区间和中点假设基线（{unit}）',
                'columns': ['方案', '下界', '上界', '中点假设下的最大后悔值'],
                'rows': [[label, _decimal(worst[key][0]), _decimal(worst[key][1]), _decimal(midpoint_worst[key])]
                         for key, label in labels.items()],
            },
        ],
        'charts': [{
            'title': '最大情景后悔值区间', 'unit': unit,
            'rows': [{'label': label, 'lower': _decimal(worst[key][0]), 'upper': _decimal(worst[key][1])}
                     for key, label in labels.items()],
        }],
        'leaders': leaders,
        'strict_leaders': strict,
        'midpoint_leaders': midpoint_leaders,
        'bound_type': bound_type,
        'regret_bounds': {key: [[_decimal(low), _decimal(high)] for low, high in row] for key, row in regret.items()},
        'worst_regret_bounds': {key: [_decimal(low), _decimal(high)] for key, (low, high) in worst.items()},
    }


def _interval_run(ctx: 'Context') -> dict:
    return _interval_results(ctx, _utilities(ctx))


def _precision_threshold(points: Points, leader: str) -> Fraction:
    # Before clipping at zero, the worst regret bounds are g(a) ± 2e.
    # For a strict comparison the rival's lower bound must also be positive.
    gaps = {
        key: max(rival - own for competitor, other in points.items() if competitor != key
                 for own, rival in zip(row, other, strict=True))
        for key, row in points.items()
    }
    return min(min(gap / 2, (gap - gaps[leader]) / 4) for key, gap in gaps.items() if key != leader)


def _witness_options(points: Points) -> tuple[str, str, str] | None:
    if len(points) != 3 or any(len(row) != 2 for row in points.values()):
        return None
    profiles = ((Fraction(8), Fraction(2)), (Fraction(11, 2), Fraction(11, 2)), (Fraction(5, 2), Fraction(8)))
    for reverse in (False, True):
        options = {(row[::-1] if reverse else row): key for key, row in points.items()}
        if all(profile in options for profile in profiles):
            return options[profiles[0]], options[profiles[1]], options[profiles[2]]
    return None


def _precision_run(ctx: 'Context') -> dict:
    points = {key: tuple(low for low, _ in row) for key, row in _utilities(ctx).items()}
    radius = Fraction(ctx.state.precision_radius)
    utilities = {key: tuple((value - radius, value + radius) for value in row) for key, row in points.items()}
    result = _interval_results(ctx, utilities)
    labels = _labels(ctx)
    unit = _unit(ctx)
    center_leaders = result['midpoint_leaders']
    result.update(precision_threshold=None, sharp_threshold=False, witness=None)
    if len(center_leaders) != 1:
        result['summary'] += ' 点值基线并列，没有可由统一半径界限认证的唯一严格占优方案。'
        return result

    leader = center_leaders[0]
    threshold = _precision_threshold(points, leader)
    result['precision_threshold'] = {'option_id': leader, 'upper_exclusive': _decimal(threshold)}
    result['summary'] += (
        f'假设各效用单元格的统一半径为 {_decimal(radius)} {unit}。对点值基线领先方案「{labels[leader]}」，'
        f'界限证书要求半径严格小于 {_decimal(threshold)} {unit}，使其后悔值上界低于各对手下界。'
    )
    _, upper = result['worst_regret_bounds'][leader]
    result['tables'].append({
        'title': f'统一半径的严格比较（{unit}）',
        'columns': ['点值基线领先方案', '对照方案', '领先方案上界', '对照方案下界', '要求'],
        'rows': [[labels[leader], label, upper, result['worst_regret_bounds'][key][0], '上界 < 下界']
                 for key, label in labels.items() if key != leader],
    })
    profiles = _witness_options(points)
    if profiles is None or not _rectangle(ctx) or radius > 1:
        return result

    result['sharp_threshold'] = True
    result['summary'] += ' 对这组矩形合成数据及 0 ≤ 半径 ≤ 1，上述条件充要。'
    if radius < threshold:
        return result

    a, b, c = profiles
    realization = {key: tuple(value + radius if key == c else value - radius for value in row)
                   for key, row in points.items()}
    regret = _point_regret(realization)
    worst = {key: _decimal(max(row)) for key, row in regret.items()}
    result['witness'] = {
        'utilities': {key: [_decimal(value) for value in row] for key, row in realization.items()},
        'worst_regret': worst,
    }
    result['tables'].append({
        'title': f'反例中的可行联合取值（{unit}）',
        'columns': ['方案', *(scenario.label for scenario in ctx.state.scenarios), '最大后悔值'],
        'rows': [[labels[key], *result['witness']['utilities'][key], worst[key]] for key in (a, b, c)],
    })
    outcome = '并列' if radius == threshold else '后悔值严格更低'
    result['summary'] += f' 表中有一个允许的联合取值，其中「{labels[c]}」相对「{labels[b]}」{outcome}。'
    return result


METHODS = (
    Method(
        model_id='C029', version='1.0.0', title='情景最小最大后悔值',
        applicability='通过硬约束且已确认同一时限、效用量尺及完整点值的有限情景比较。',
        inputs=('可行方案', '情景', '各情景的点值效用', '用户选择的参照方案（可选）'),
        outputs=('后悔值矩阵', '最小最大后悔方案', '各情景最优方案', '最大最小效用基线', '参照方案的条件性预知增益'),
        units='用户确认的共用效用单位。',
        assumptions=('效用越高越好。', '比较基于所列固定情景，结论取决于情景覆盖。'),
        uncertainty='不需要情景概率。只在承诺前完全预知情景、且允许改选的假设下显示逐情景效用增益。',
        sources=(POINT_SOURCE,),
        failure_conditions=('缺失点值、来源或共同单位', '情景、时限或效用尺度未确认', '依硬约束通过的方案为空'),
        replay='逐情景计算可行方案的最大效用，再减去各方案效用，对每个方案取情景最大值。',
        baseline='比较各方案最小效用，并在指定参照时计算对该方案的逐情景增益。',
        validate=_validate_points, execute=_point_results,
    ),
    Method(
        model_id='C030', version='1.0.0', title='区间情景后悔值',
        applicability='效用可表示为共用标尺上的闭区间，且区间内至少存在一个联合可行取值。',
        inputs=('可行方案', '情景', '闭区间效用', '区间依赖关系及来源'),
        outputs=('后悔值区间矩阵', '最大后悔值区间', '最小上界方案', '严格分离的比较'),
        units='用户确认的共用效用单位。',
        assumptions=('效用越高越好。', '矩形独立性决定各极值能否分别达到。'),
        uncertainty='仅在声明有来源的矩形独立性下报告可达极值。其他情况为保守外界，区间接触时严格排序仍为 UNKNOWN。',
        sources=(INTERVAL_SOURCE, POINT_SOURCE),
        failure_conditions=('缺失、倒置或不可比的效用区间', '情景、来源、时限或效用尺度未确认', '不存在一致的联合取值'),
        replay='排除自身，分别比较对手下界与自身上界、对手上界与自身下界，再以零截断并跨情景取最大值。',
        baseline='假设每个效用取区间中点，计算 C029 作为比较。',
        validate=_validate, execute=_interval_run,
    ),
    Method(
        model_id='C031', version='1.0.0', title='后悔值排序的效用精度阈值',
        applicability='两个及以上可行方案有可比较的情景效用中心，并给出假设统一半径。',
        inputs=('效用点数据作为中心', '假设统一半径', '区间依赖关系及来源'),
        outputs=('最大后悔值区间', '最小上界方案', '严格分离阈值', '适用时的合成反例'),
        units='统一半径与后悔值采用共用效用单位。',
        assumptions=('所有情景的效用单元格按同一个非负半径展开。', '充要结论仅适用于来源卡的原始矩形合成几何与半径范围。'),
        uncertainty='按区间外界给出严格比较的充分条件。阈值衡量假设效用精度，合成反例依赖声明的矩形联合取值。',
        sources=(PRECISION_SOURCE, WITNESS_SOURCE, INTERVAL_SOURCE),
        failure_conditions=('缺失或不可比的点值中心', '负或缺失半径', '通过硬约束的方案少于两个'),
        replay='由中心加减统一半径得到区间。按 C030 计算，再求领先方案上界严格低于各对手下界的半径范围。',
        baseline='以点值中心计算 C029，留存所有并列候选。',
        validate=_validate_precision, execute=_precision_run,
    ),
)
