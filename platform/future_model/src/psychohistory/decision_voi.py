"""Validated and versioned finite value-of-information methods."""

from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .decision_registry import Context, Method
from .decision_state import InputModel, Key, Kind, Number, Quantity, Text, TextLine
from .decision_voi_math import (
    ONE, ZERO, Bounds, Payoffs, Policy, Problem, Q, ScopeLimit, Vector,
    adaptive, arrangement, fixed_search, fixed_worlds, net, payoffs, point_world, policies, policy_value, winners,
)


class Probability(InputModel):
    lower: Annotated[Number, Field(ge=0, le=1)] | None = None
    upper: Annotated[Number, Field(ge=0, le=1)] | None = None
    kind: Kind
    source: TextLine = ''

    @model_validator(mode='after')
    def check_bounds(self):
        if self.lower is not None and self.upper is not None and self.lower > self.upper:
            raise ValueError('概率区间下界不能大于上界')
        if self.kind == 'unknown' and (self.lower is not None or self.upper is not None):
            raise ValueError('未知概率应留空')
        return self


class Signal(InputModel):
    id: Key
    label: Text


class SignalActions(InputModel):
    option_ids: list[Key] = Field(default_factory=list, max_length=24)
    kind: Kind
    source: TextLine = ''

    @model_validator(mode='after')
    def check_options(self):
        if len(set(self.option_ids)) != len(self.option_ids):
            raise ValueError('同一信号的可行行动标识必须唯一')
        return self


type ProbabilityRow = Annotated[dict[Key, Probability], Field(max_length=24)]


class InformationInput(InputModel):
    signals: list[Signal] = Field(default_factory=list, max_length=24)
    prior: ProbabilityRow = Field(default_factory=dict)
    likelihoods: Annotated[dict[Key, ProbabilityRow], Field(max_length=24)] = Field(default_factory=dict)
    cost: Quantity | None = None
    actions_by_signal: Annotated[dict[Key, SignalActions], Field(max_length=24)] = Field(default_factory=dict)
    unrestricted_actions: bool = Field(default=False, strict=True)
    action_source: TextLine = ''
    parameter_domain: Literal['unknown', 'rectangle', 'constrained'] = 'unknown'
    parameter_domain_source: TextLine = ''
    timing_basis: Text | None = None
    fixed_policy: Annotated[dict[Key, Key], Field(max_length=24)] = Field(default_factory=dict)
    verification_source: Text | None = None

    @model_validator(mode='after')
    def check_signals(self):
        if len({signal.id for signal in self.signals}) != len(self.signals):
            raise ValueError('信号标识必须唯一')
        return self


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


def _prepare(ctx: Context) -> tuple[list[str], Problem | None, str]:
    state = ctx.state
    info = getattr(state, 'information', None)
    if info is None:
        return ['需要填写调查信号、概率、成本及行动条件。'], None, 'CONDITIONAL'
    errors = []
    if not state.scenarios or not state.scenario_basis or not state.scenario_basis.strip():
        errors.append('需要确认状态集与可比较的基数效用量尺。')
    if not ctx.feasible:
        errors.append('没有通过已确认硬约束的立即行动。')
    if not info.signals:
        errors.append('需要列出有限且互斥、覆盖结果的调查信号。')
    if not info.timing_basis:
        errors.append('需要说明调查在行动前完成且没有等待机会损失的依据。')
    if info.unrestricted_actions and (not info.action_source.strip() or info.actions_by_signal):
        errors.append('需要一个明确的调查后行动集合及依据。')
    if errors:
        return errors, None, 'CONDITIONAL'

    kinds = set()
    state_ids = tuple(scenario.id for scenario in state.scenarios)
    signal_ids = tuple(signal.id for signal in info.signals)
    option_ids = tuple(option.id for option in ctx.feasible)
    declared_options = {option.id for option in state.options}
    if (info.prior.keys() | info.likelihoods.keys()) - set(state_ids):
        errors.append('概率输入指向不存在的状态。')
    if (info.actions_by_signal.keys() - set(signal_ids)
            or any(row.keys() - set(signal_ids) for row in info.likelihoods.values())):
        errors.append('概率或行动输入指向不存在的信号。')
    if any(set(row.option_ids) - declared_options for row in info.actions_by_signal.values()):
        errors.append('调查后的行动条件指向不存在的方案。')
    prior = _probability_row(state_ids, info.prior, '状态先验', errors, kinds)
    if errors:
        return errors, None, 'CONDITIONAL'

    # Conditional distributions and utilities on impossible states have no contribution.
    active = [(scenario, bound) for scenario, bound in zip(state.scenarios, prior, strict=True) if bound[1]]
    likelihoods = []
    utility = []
    units, horizons = set(), set()
    for scenario, _ in active:
        if scenario.kind == 'unknown' or not scenario.source.strip():
            errors.append(f'状态「{scenario.label}」需要来源。')
        kinds.add(scenario.kind)
        likelihoods.append(_probability_row(signal_ids, info.likelihoods.get(scenario.id, {}),
                                             f'状态「{scenario.label}」的条件信号概率', errors, kinds))
        row = []
        for option in ctx.feasible:
            value = scenario.utilities.get(option.id)
            if not _known(value) or value.lower != value.upper:
                errors.append(f'需要方案「{option.label}」在状态「{scenario.label}」中有来源的点效用。')
                continue
            units.add(value.unit.strip())
            horizon = value.horizon or state.deadline
            horizons.add(horizon.strip() if horizon else None)
            kinds.add(value.kind)
            row.append(Fraction(value.lower))
        utility.append(tuple(row))

    cost = info.cost
    if not _known(cost) or cost.lower != cost.upper or cost.lower < 0:
        errors.append('需要有来源、非负且可比较的调查点成本。')
    else:
        units.add(cost.unit.strip())
        if cost.horizon:
            horizons.add(cost.horizon.strip())
        kinds.add(cost.kind)
    if len(units) != 1 or '' in units:
        errors.append('成本及各行动效用须共用同一明确单位。')
    if len(horizons) != 1 or None in horizons:
        errors.append('成本及各行动效用须基于同一明确时间范围。')
    if errors:
        return errors, None, 'CONDITIONAL'

    actions = []
    for index, signal in enumerate(info.signals):
        reachable = any(row[index][1] > 0 for row in likelihoods)
        if not reachable:
            actions.append(())
            continue
        if info.unrestricted_actions:
            actions.append(tuple(range(len(option_ids))))
            continue
        allowed = info.actions_by_signal.get(signal.id)
        if allowed is None or allowed.kind == 'unknown' or not allowed.source.strip():
            errors.append(f'信号「{signal.label}」的可行动作及来源为 UNKNOWN。')
            actions.append(())
            continue
        kinds.add(allowed.kind)
        eligible = tuple(a for a, option in enumerate(option_ids) if option in allowed.option_ids)
        if not eligible:
            errors.append(f'信号「{signal.label}」有正概率，需要已通过硬约束的行动或明确兜底行动。')
        actions.append(eligible)
    if errors:
        return errors, None, 'CONDITIONAL'

    problem = Problem(tuple(scenario.id for scenario, _ in active), signal_ids, option_ids,
                      tuple(bound for _, bound in active), tuple(likelihoods), tuple(utility), tuple(actions),
                      Fraction(cost.lower))
    evidence = 'CONDITIONAL'
    if 'synthetic' in kinds:
        evidence = 'SYNTHETIC'
    elif (info.verification_source and info.verification_source.strip()
          and kinds <= {'fact', 'estimate'} and problem.point):
        # A user-supplied receipt is an assertion, never independent source verification.
        evidence = 'USER_ATTESTED'
    return [], problem, evidence


def _declared_policy(ctx: Context, problem: Problem) -> Policy | None:
    declared = ctx.state.information.fixed_policy
    if not declared or declared.keys() - set(problem.signals):
        return None
    policy = []
    for signal, choices in zip(problem.signals, problem.actions, strict=True):
        if not choices:
            policy.append(-1)
        elif declared.get(signal) in {problem.options[index] for index in choices}:
            policy.append(problem.options.index(declared[signal]))
        else:
            return None
    return tuple(policy)


def _validate(mode, ctx: Context) -> list[str]:
    errors, problem, _ = _prepare(ctx)
    if errors:
        return errors
    info = ctx.state.information
    if mode == 'point':
        return [] if problem.point else ['点值计算需要唯一的先验和条件信号概率。']
    if not problem.point and (info.parameter_domain != 'rectangle' or not info.parameter_domain_source.strip()):
        return ['需要有来源的联合区间约束。当前精确方法支持各概率行可独立组合，行内仍须合计为 1。']
    if mode == 'fixed' and _declared_policy(ctx, problem) is None:
        return ['需要事前为每个可出现的信号指定同一可执行行动。']
    try:
        if mode in {'oracle', 'fixed'}:
            if not problem.point:
                arrangement(problem, adaptive_policy=(mode == 'oracle'))
        else:
            fixed_search(problem)
    except ScopeLimit as exc:
        return [str(exc)]
    return []


def _decimal(value: Q, *, exact: bool = False) -> str:
    with localcontext() as context:
        context.prec = max(24, len(str(abs(value.numerator))) + len(str(value.denominator)))
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
    if exact and Fraction(decimal) != value:
        return str(value)
    return format(decimal, 'f')


def _exact(value: Q) -> str:
    return _decimal(value, exact=True)


def _decision(lower: Q, upper: Q) -> str:
    if lower > 0:
        return 'POSITIVE'
    if upper < 0:
        return 'NEGATIVE'
    if lower == upper == 0:
        return 'TIE'
    return 'CONDITIONAL'


def _decision_text(lower: Q, upper: Q) -> str:
    return {
        'POSITIVE': '在声明的范围与假设下，调查净优势严格为正。',
        'NEGATIVE': '在声明的范围与假设下，调查净优势严格为负。',
        'TIE': '在声明的范围与假设下，调查净优势等于零。',
        'CONDITIONAL': '调查净优势的范围包含零，结论取决于条件或停在等号边界。',
    }[_decision(lower, upper)]


def _evidence_text(status: str) -> str:
    return {
        'SYNTHETIC': '含合成输入，输出用于数学演示。',
        'CONDITIONAL': '结果为给定假设和来源的条件计算。',
        'USER_ATTESTED': '用户声明已核对所填点值。系统没有独立核实来源、准确性或现实适用性。',
    }[status]


def _labels(ctx: Context) -> tuple[dict, dict]:
    return ({option.id: option.label for option in ctx.feasible},
            {signal.id: signal.label for signal in ctx.state.information.signals})


def _policy(problem: Problem, policy: Policy) -> dict[str, str]:
    return {signal: problem.options[index] for signal, index in zip(problem.signals, policy, strict=True) if index >= 0}


def _describe_policy(ctx: Context, policy: dict[str, str]) -> str:
    options, signals = _labels(ctx)
    return '、'.join(f'{signals[z]} → {options[a]}' for z, a in policy.items())


def _world(problem: Problem, mass: Vector) -> dict:
    width = len(problem.signals)
    rows = tuple(mass[i:i + width] for i in range(0, len(mass), width))
    return {
        'prior': {state: _exact(sum(row, ZERO)) for state, row in zip(problem.states, rows, strict=True)},
        'likelihoods': {
            state: ({signal: _exact(weight / total) for signal, weight in zip(problem.signals, row, strict=True)}
                    if (total := sum(row, ZERO)) else None)
            for state, row in zip(problem.states, rows, strict=True)
        },
        'joint_mass': {
            state: {signal: _exact(value) for signal, value in zip(problem.signals, row, strict=True)}
            for state, row in zip(problem.states, rows, strict=True)
        },
    }


def _base_result(ctx: Context, lower: Q, upper: Q, evidence: str, summary: str) -> dict:
    cost_quantity = ctx.state.information.cost
    cost = Fraction(cost_quantity.lower)
    unit = cost_quantity.unit.strip()
    gross_lower, gross_upper = lower + cost, upper + cost
    return {
        'summary': summary + _decision_text(lower, upper) + _evidence_text(evidence),
        'evidence_status': evidence,
        'decision': _decision(lower, upper),
        'net_bounds': {'lower': _exact(lower), 'upper': _exact(upper)},
        'range_kind': 'EXACT',
        'cost': _exact(cost),
        'break_even_cost': {'lower': _exact(gross_lower), 'upper': _exact(gross_upper), 'unit': unit},
        'tables': [
            {'title': f'净优势与等号边界（{unit}）', 'columns': ['下界', '上界', '无差异'],
             'rows': [[_exact(lower), _exact(upper), '0']]},
            {'title': f'实际输入成本和净优势归零的临界成本（{unit}）', 'columns': ['输入成本', '临界下界', '临界上界'],
             'rows': [[_exact(cost), _exact(gross_lower), _exact(gross_upper)]]},
        ],
        'charts': [{
            'title': '调查净优势与无差异边界', 'unit': unit,
            'rows': [{'label': '调查净优势', 'lower': _decimal(lower), 'upper': _decimal(upper)},
                     {'label': '无差异', 'lower': '0', 'upper': '0'}],
        }],
    }


def _point_run(ctx: Context) -> dict:
    _, problem, evidence = _prepare(ctx)
    values = payoffs(problem, point_world(problem))
    baseline = max(values.baseline)
    with_information = adaptive(problem, values)
    gross = with_information - baseline
    perfect = sum(p * max(row) for (p, _), row in zip(problem.prior, problem.utility, strict=True)) - baseline
    value = gross - problem.cost
    options, signal_labels = _labels(ctx)
    immediate = [problem.options[a] for a in winners(values.baseline, tuple(range(len(problem.options))))]
    signals = {}
    for z, signal in enumerate(problem.signals):
        probability = values.probability[z]
        increment = max((values.signals[z][a] for a in problem.actions[z]), default=ZERO)
        posterior = ({state: _exact(values.mass[s * len(problem.signals) + z] / probability)
                      for s, state in enumerate(problem.states)} if probability else None)
        signals[signal] = {
            'probability': _exact(probability),
            'actions': [problem.options[a] for a in winners(values.signals[z], problem.actions[z])] if probability else [],
            'posterior': posterior,
            'joint_value': _exact(increment),
        }
    label = '点值 EVSI' if problem.unrestricted else '有行动限制的调查收益差'
    result = _base_result(ctx, value, value, evidence, f'先比较免调查的立即行动，再按各信号选择可执行行动。{label}。')
    result.update(baseline_value=_exact(baseline), baseline_actions=immediate, information_value=_exact(with_information),
                  evpi=_exact(perfect), evsi=_exact(gross) if problem.unrestricted else None,
                  gross_advantage=_exact(gross), net_value=_exact(value), signals=signals)
    result['tables'].extend([
        {'title': '立即行动和调查条件比较', 'columns': ['免调查基线', '调查后期望效用', label, '调查成本', '净优势'],
         'rows': [[_exact(baseline), _exact(with_information), _exact(gross), _exact(problem.cost), _exact(value)]]},
        {'title': '信号后的行动及加权贡献', 'columns': ['信号', '发生概率', '最优可行行动（含并列）', '联合收益'],
         'rows': [[signal_labels[key], entry['probability'], '、'.join(options[a] for a in entry['actions']) or '不发生',
                   entry['joint_value']] for key, entry in signals.items()]},
    ])
    return result


def _bounds_run(ctx: Context, *, fixed: bool) -> dict:
    _, problem, evidence = _prepare(ctx)
    policy = _declared_policy(ctx, problem) if fixed else None
    worlds = (point_world(problem),) if problem.point else arrangement(problem, adaptive_policy=not fixed).vertices()
    payoffs_by_world = [payoffs(problem, world) for world in worlds]
    outcomes = [(net(problem, values, policy), values.mass) for values in payoffs_by_world]
    lower, low_world = min(outcomes)
    upper, high_world = max(outcomes)
    description = ('同一个预先声明的信号策略与每个参数点的最佳免费行动相比。'
                   if fixed else '各参数点按其自身最优信号策略与同一点的最佳免费行动比较。执行该适应策略需要先知道参数。')
    result = _base_result(ctx, lower, upper, evidence, description)
    result['extrema'] = {'lower': _world(problem, low_world), 'upper': _world(problem, high_world)}
    result['scope'] = 'FIXED_POLICY' if fixed else 'ORACLE_ADAPTATION'
    if fixed:
        result['policy'] = _policy(problem, policy)
        minima = {}
        for values in payoffs_by_world:
            fixed_value = policy_value(values, policy) - problem.cost
            for key, baseline in zip(problem.options, values.baseline, strict=True):
                difference = fixed_value - baseline
                minima[key] = min(minima.get(key, difference), difference)
        result['worst_against_baseline'] = {key: _exact(value) for key, value in minima.items()}
        labels, _ = _labels(ctx)
        result['tables'].append({
            'title': '事前固定规则的逐行动优势', 'columns': ['固定规则', '免费行动', '最小净优势'],
            'rows': [[_describe_policy(ctx, result['policy']), labels[key], _exact(value)] for key, value in minima.items()],
        })
    states = {scenario.id: scenario.label for scenario in ctx.state.scenarios}
    result['tables'].append({
        'title': '达到净优势界限的参数见证', 'columns': ['界限', '先验', '状态—信号联合概率'],
        'rows': [[label, '、'.join(f'{states[key]}={value}' for key, value in evidence['prior'].items()),
                  '、'.join(f'{states[key]}: ' + ' / '.join(row.values()) for key, row in evidence['joint_mass'].items())]
                 for label, evidence in [('下界', result['extrema']['lower']), ('上界', result['extrema']['upper'])]],
    })
    return result


def _fixed_evaluation(problem: Problem) -> tuple[tuple[Payoffs, ...], list[tuple[Q, Policy, int]]]:
    values = tuple(payoffs(problem, world) for world in fixed_worlds(problem))
    ranked = []
    for policy in policies(problem):
        minimum, witness = min((net(problem, value, policy), i) for i, value in enumerate(values))
        ranked.append((minimum, policy, witness))
    return values, ranked


def _maximin_run(ctx: Context) -> dict:
    _, problem, evidence = _prepare(ctx)
    values, ranked = _fixed_evaluation(problem)
    best = max(minimum for minimum, _, _ in ranked)
    result = _base_result(ctx, best, best, evidence, '在完整确定性映射集合中最大化最小逐参数净优势。')
    result['scope'] = 'DETERMINISTIC_MAXIMIN_ADVANTAGE'
    result['optimal_policies'] = [_policy(problem, policy) for minimum, policy, _ in ranked if minimum == best]
    result['policies'] = [{'policy': _policy(problem, policy), 'minimum_advantage': _exact(minimum),
                           'witness': _world(problem, values[index].mass)} for minimum, policy, index in ranked]
    result['tables'].append({
        'title': '完整确定性规则的最坏净优势', 'columns': ['规则', '最坏净优势'],
        'rows': [[_describe_policy(ctx, item['policy']), item['minimum_advantage']] for item in result['policies']],
    })
    return result


def _randomized_run(ctx: Context) -> dict:
    _, problem, evidence = _prepare(ctx)
    values, ranked = _fixed_evaluation(problem)
    lower = max(minimum for minimum, _, _ in ranked)
    upper, index = min((net(problem, value), i) for i, value in enumerate(values))
    certified = lower == upper
    witness = values[index]
    lower_policies = [_policy(problem, policy) for value, policy, _ in ranked if value == lower]
    unique = None
    if certified:
        if len(lower_policies) > 1:
            unique = False
        elif all(len(row) <= 1 or (probability and len(winners(joint, row)) == 1)
                 for row, probability, joint in zip(problem.actions, witness.probability, witness.signals, strict=True)):
            unique = True
    description = ('固定确定性规则给出下界，同一参数见证点的逐信号最优响应给出随机规则的上界。'
                   + ('上下界相等，已认证所述随机规则类的最大最小值。' if certified else
                      '上下界未合，随机规则的精确最优值及最优规则为 UNKNOWN。'))
    result = _base_result(ctx, lower, upper, evidence, description)
    result.update(scope='PRECOMMITTED_SIGNAL_RANDOMIZATION', certificate_status='CERTIFIED' if certified else 'UNKNOWN',
                  range_kind='EXACT' if certified else 'OUTER',
                  unique_policy=unique, witness=_world(problem, witness.mass), deterministic_lower_policies=lower_policies)
    result['tables'].append({
        'title': '随机化上界见证', 'columns': ['信号', '各可行动作的联合期望贡献'],
        'rows': [[label, '、'.join(f'{problem.options[action]}={_exact(row[action])}' for action in choices)]
                 for label, row, choices in zip(problem.signals, witness.signals, problem.actions, strict=True)],
    })
    return result


def _card(name: str, date='2026-11-21') -> str:
    return f'research/decision_methods/VOI_{name}_{date}.md'


POINT_SOURCES = (
    _card('IMPERFECT_BINARY_SIGNAL_METHOD_CARD', '2026-11-20'),
    _card('ASYMMETRIC_BINARY_SIGNAL_EXTENSION', '2026-11-20'),
    _card('REVERSED_BINARY_SIGNAL_LABEL_INVARIANCE', '2026-11-20'),
    _card('ASYMMETRIC_SIGNAL_PRIOR_SWITCH_INTERVAL', '2026-11-20'),
    'research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md',
)


def _method(model_id, title, mode, execute, outputs, assumptions, sources, replay):
    return Method(
        model_id=model_id, version='1.0.0', title=title,
        applicability='有限互斥状态和调查信号，有明确来源的概率、行动集合、可比较的点效用和调查成本。',
        inputs=('先验和条件信号概率', '通过硬约束的立即行动和调查后行动', '效用、时限和成本的证据'),
        outputs=outputs, units='概率为比例，效用和调查成本采用确认的同一量纲。',
        assumptions=assumptions,
        uncertainty='仅比较当前问题的期望效用。不为区间参数补造分布。用户提交的核对声明不等于系统独立核验，条件计算与合成演示分别标明。',
        sources=sources,
        failure_conditions='缺少来源或行动，归一化冲突，效用或成本不可比较，时序未确认，或超出声明的参数范围。',
        replay=replay, baseline='同一参数点下，从全部通过硬约束的立即行动中选取期望效用最大的免费行动。',
        validate=lambda ctx: _validate(mode, ctx), execute=execute,
    )


METHODS = (
    _method('voi_point', '点值调查信息价值', 'point', _point_run,
            ('立即行动', '信号后行动及概率', 'EVSI、完全信息上界与调查净优势'),
            '调查在行动前完成，无等待损失。行动受限时显示相对免费基线的调查收益差。',
            POINT_SOURCES, '根据先验和条件信号概率计算联合概率，逐信号最大化联合效用。'),
    _method('voi_oracle_bounds', '按参数各自最优的调查优势区间', 'oracle', lambda ctx: _bounds_run(ctx, fixed=False),
            ('精确净优势上下界', '可复算的极值见证'),
            '有据的概率行间直积与行内归一化。每个参数点允许选不同调查策略。',
            (_card('PRIOR_INTERVAL_ROBUST_COST'), *POINT_SOURCES),
            '将参数区间写成联合概率的线性约束，按立即行动和信号行动的切换面分段求界。'),
    _method('voi_fixed_policy', '固定调查规则的逐参数优势', 'fixed', lambda ctx: _bounds_run(ctx, fixed=True),
            ('固定规则', '精确净优势上下界', '对各免费行动的最小优势'),
            '事前确认同一可执行映射，参数变化时规则保持固定。',
            (_card('FIXED_POLICY_UNIFORM_DOMINANCE'), _card('JOINT_SIGNAL_QUALITY_ROBUST_FIXED_POLICY')),
            '按立即行动的切换面分段，以同一调查规则计算各参数点的净优势。'),
    _method('voi_maximin', '确定性规则的最大最小调查优势', 'maximin', _maximin_run,
            ('完整确定性映射集合', '每项规则最坏净优势', '含并列的最优规则'),
            '事前承诺确定性映射，目标为最大化最小逐参数优势。',
            (_card('FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE'), _card('JOINT_SIGNAL_QUALITY_ROBUST_FIXED_POLICY')),
            '枚举可执行确定性策略和概率行端点，用多重仿射比较精确求各规则最坏优势。'),
    _method('voi_randomized_certificate', '固定随机规则的上下界证书', 'randomized', _randomized_run,
            ('确定性下界', '随机规则上界见证', '覆盖的策略范围和证书状态'),
            '随机化只依赖所见信号，所有概率在事前固定，期望效用对混合行动线性。',
            (_card('RANDOMIZED_SIGNAL_POLICY_MINIMAX_BOUND'), _card('FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE')),
            '比较确定性最大最小值与单点最优响应上界。仅在上下界相等时认证精确值。'),
)
