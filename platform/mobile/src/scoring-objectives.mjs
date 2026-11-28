import { cmp, minus, stripText } from './core.mjs';
import {
  ZERO, ONE, bounds, documented, horizon, known, max, min, own, pairs,
  runScoring, uniqueIds,
} from './scoring-shared.mjs';

export const RELATIONS = {
  A_DOMINATES: '甲保证支配乙',
  B_DOMINATES: '乙保证支配甲',
  INCOMPARABLE: '各有更好的目标',
  EQUAL: '各目标相等',
  A_STRICT: '甲在所有允许情形下严格领先',
  B_STRICT: '乙在所有允许情形下严格领先',
  UNRESOLVED: '无法证明严格领先',
  UNKNOWN: '证据不足',
};

export function validObjectives(objectives) {
  return uniqueIds(objectives) && objectives.every(objective =>
    documented(objective.label) && documented(objective.unit) && ['max', 'min'].includes(objective.direction));
}

export function basicErrors(state, feasible) {
  const errors = [];
  if (feasible.length < 2) errors.push('需要至少两个通过硬约束筛查的可执行方案。');
  const objectives = state.objectives ?? [];
  if (!objectives.length || !validObjectives(objectives)) {
    errors.push('需要列明比较目标、方向与单位。');
  }
  return errors;
}

export function scoreGap(option, objective, state) {
  const quantity = own(option.scores, objective.id);
  const interval = bounds(quantity);
  if (!known(quantity) || !interval) return '缺少可核对的得分或完整区间';
  if (!documented(quantity.unit) || stripText(quantity.unit) !== stripText(objective.unit)) {
    return `得分单位 ${quantity.unit ?? ''} 与目标要求的 ${objective.unit} 不一致`;
  }
  if (!documented(quantity.source)) return '缺少得分来源';
  if (!horizon(quantity, state.deadline)) return '缺少得分观察时域';
  if (state.score_dependence === 'rectangle' && state.score_transform === 'clip_01'
      && (cmp(interval[0], ZERO) < 0 || cmp(interval[1], ONE) > 0)) {
    return '需要提供截断后 0–1 内的效用区间';
  }
  return null;
}

export function objectiveHorizons(options, objective, state) {
  return new Set(options.filter(option => !scoreGap(option, objective, state))
    .map(option => horizon(own(option.scores, objective.id), state.deadline)));
}

function decimalText(value) {
  if (value == null) return null;
  return stripText(String(value)).replace(/^\+/, '').replace(/^(-?)\./, '$10.').replace(/^(-?)0+(?=\d)/, '$1');
}

function comparability(state, feasible) {
  const rows = [];
  const gaps = [];
  const score_gaps = [];
  for (const objective of state.objectives) {
    const horizons = objectiveHorizons(feasible, objective, state);
    for (const option of feasible) {
      const quantity = own(option.scores, objective.id);
      let gap = scoreGap(option, objective, state);
      if (!gap && horizons.size > 1) gap = '同一目标的方案采用了不同观察时域';
      if (gap) {
        gaps.push(`${option.label} · ${objective.label}：${gap}。`);
        score_gaps.push({ option: option.id, objective: objective.id, reason: gap });
      }
      rows.push([
        option.label, objective.label, objective.unit, objective.direction === 'max' ? '越高越好' : '越低越好',
        decimalText(quantity?.lower), decimalText(quantity?.upper), quantity ? horizon(quantity, state.deadline) : null,
        quantity?.kind ?? 'unknown', quantity?.source ?? (quantity ? '' : null), gap ?? '可按该目标比较',
      ]);
    }
  }
  let summary = gaps.length
    ? '有些目标的方案得分仍需核对单位、观察时域、来源或上下界。'
    : '可逐目标比较通过硬约束的方案。';
  summary += documented(state.score_basis)
    ? `已记录跨目标的效用刻度依据。${state.score_basis}`
    : '跨目标加权需要确认共同的基数效用刻度与可补偿性。';
  return {
    summary, status: gaps.length ? 'UNKNOWN' : 'COMPARABLE_BY_OBJECTIVE', gaps, score_gaps,
    tables: [{
      title: '得分可比性检查',
      columns: ['方案', '目标', '要求单位', '比较方向', '填报下界', '填报上界', '观察时域', '证据类型', '来源', '结论'],
      rows,
    }],
  };
}

export const clip = value => min(ONE, max(ZERO, value));

export function nominalBounds(option, objective, state) {
  const interval = bounds(own(option.scores, objective.id));
  return state.score_dependence === 'shared_additive' && state.score_transform === 'clip_01'
    ? interval.map(clip) : interval;
}

export function difference(a, b, objective, state) {
  const [aLo, aHi] = nominalBounds(a, objective, state);
  const [bLo, bHi] = nominalBounds(b, objective, state);
  return objective.direction === 'max' ? [minus(aLo, bHi), minus(aHi, bLo)]
    : [minus(bLo, aHi), minus(bHi, aLo)];
}

function paretoRelation(a, b, state) {
  if (state.objectives.some(objective => scoreGap(a, objective, state) || scoreGap(b, objective, state)
    || objectiveHorizons([a, b], objective, state).size > 1)) return 'UNKNOWN';
  const differences = state.objectives.map(objective => difference(a, b, objective, state));
  const aStrict = differences.some(([lower]) => cmp(lower, ZERO) > 0);
  const bStrict = differences.some(([, upper]) => cmp(upper, ZERO) < 0);
  if (aStrict && differences.every(([lower]) => cmp(lower, ZERO) >= 0)) return 'A_DOMINATES';
  if (bStrict && differences.every(([, upper]) => cmp(upper, ZERO) <= 0)) return 'B_DOMINATES';
  if (aStrict && bStrict) return 'INCOMPARABLE';
  if (differences.every(([lower, upper]) => cmp(lower, ZERO) === 0 && cmp(upper, ZERO) === 0)) return 'EQUAL';
  return 'UNRESOLVED';
}

function pareto(state, feasible) {
  const dominated = new Set();
  const comparisons = [];
  const rows = [];
  for (const [a, b] of pairs(feasible)) {
    const relation = paretoRelation(a, b, state);
    if (relation === 'A_DOMINATES') dominated.add(b.id);
    if (relation === 'B_DOMINATES') dominated.add(a.id);
    comparisons.push({ a: a.id, b: b.id, relation });
    rows.push([a.label, b.label, RELATIONS[relation]]);
  }
  const frontier = feasible.filter(option => !dominated.has(option.id));
  const unknown = comparisons.some(({ relation }) => ['UNKNOWN', 'UNRESOLVED'].includes(relation));
  const shared = state.score_dependence === 'shared_additive';
  const scope = shared ? '名义得分' : '已列明的得分或区间';
  let summary = `依据${scope}，当前未被证明支配的方案有${frontier.map(option => option.label).join('、')}。`;
  if (unknown) summary += '存在区间重叠或证据缺口，部分比较待定。';
  if (shared) summary += '共同校准误差及其变换由联合稳健性方法评估。';
  return {
    summary, status: unknown ? 'UNKNOWN' : 'PARETO_FRONTIER', frontier: frontier.map(option => option.id),
    pairs: comparisons, tables: [{ title: '逐目标支配关系', columns: ['甲', '乙', '关系'], rows }],
  };
}

export function score(state, options = {}) {
  return runScoring('comparability', state, options, basicErrors, comparability);
}

export function dominance(state, options = {}) {
  return runScoring('pareto', state, options, basicErrors, pareto);
}
