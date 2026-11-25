import { cmp, exact, minus, plus, rat, stripText, times } from './core.mjs';
import {
  ONE, ZERO, bounds, divide, documented, max, midpoint, min, neg, own, pairs, receipt, runScoring, sum,
} from './scoring-shared.mjs';
import {
  RELATIONS, basicErrors, clip, difference, nominalBounds, objectiveHorizons, scoreGap, validObjectives,
} from './scoring-objectives.mjs';

const FIXED = 'weight_sensitivity';
const JOINT = 'c034_joint_robustness';

function weightErrors(state, feasible, joint) {
  const errors = basicErrors(state, feasible);
  const objectives = state.objectives ?? [];
  if (!validObjectives(objectives)) return errors;
  if (!documented(state.score_basis) || new Set(objectives.map(objective => stripText(objective.unit))).size !== 1) {
    errors.push('需要由用户确认共同的基数效用单位、目标间可补偿性与权重含义。');
  }
  if (state.weights_confirmed !== true) errors.push('需要用户确认每个目标的权重范围。');
  if (!covers(state.weights, objectives)) {
    errors.push('权重必须与列明的目标一一对应。');
  } else if (objectives.length) {
    const intervals = weightIntervals(state);
    if (intervals.some(interval => !interval || cmp(interval[0], ZERO) < 0 || cmp(interval[1], ONE) > 0)) {
      errors.push('权重上下界应有序且位于 0 到 1。');
    } else if (cmp(sum(intervals.map(([lower]) => lower)), ONE) > 0 || cmp(sum(intervals.map(([, upper]) => upper)), ONE) < 0) {
      errors.push('这些权重范围内没有总和等于 1 的组合。');
    }
  }
  for (const option of feasible) {
    for (const objective of objectives) {
      const gap = scoreGap(option, objective, state);
      if (gap) errors.push(`${option.label}的${objective.label}${gap}。`);
    }
  }
  const horizons = new Set(objectives.flatMap(objective => [...objectiveHorizons(feasible, objective, state)]));
  if (horizons.size > 1) errors.push('加权比较需要所有方案与目标采用共同的得分观察时域。');

  if (joint) {
    if (objectives.length !== 2 || objectives.some(objective => objective.direction !== 'max')) {
      errors.push('C034 需要两个越高越好的基数效用目标。');
    }
    if (!['rectangle', 'shared_additive'].includes(state.score_dependence) || !documented(state.score_dependence_source)) {
      errors.push('需要明确得分的联合误差结构及其依据。');
    }
    if (!['identity', 'clip_01'].includes(state.score_transform)) errors.push('需要确认得分使用恒等变换或截断至 0–1。');
    if (state.score_dependence === 'shared_additive') {
      if (!covers(state.shared_offsets, objectives) || objectives.some(objective => !bounds(own(state.shared_offsets, objective.id)))) {
        errors.push('每个目标需要有可核对的共同偏移区间。');
      }
      if (feasible.some(option => objectives.some(objective => containsInterval(own(option.scores, objective.id))))) {
        errors.push('共同偏移模型需要名义点值，方案特有误差需要另行指定联合模型。');
      }
    }
  } else {
    for (const option of feasible) {
      for (const objective of objectives) {
        if (containsInterval(own(option.scores, objective.id))) {
          errors.push(`${option.label}的${objective.label}含得分区间，权重单项分析需要点值。`);
        }
      }
    }
  }
  return errors;
}

function containsInterval(quantity) {
  const interval = bounds(quantity);
  if (interval) return cmp(...interval) !== 0;
  return quantity != null && (quantity.lower ?? null) !== (quantity.upper ?? null);
}

function covers(values, objectives) {
  return Object.keys(values ?? {}).length === objectives.length
    && objectives.every(objective => Object.hasOwn(values ?? {}, objective.id));
}

function weightIntervals(state) {
  return state.objectives.map(objective => bounds(own(state.weights, objective.id)));
}

function dot(coefficients, weights) {
  return sum(coefficients.map((coefficient, index) => times(coefficient, weights[index])));
}

function extreme(coefficients, intervals, maximum = false) {
  // Allocate the remaining mass in coefficient order, preserving objective order for ties.
  const weights = intervals.map(([lower]) => lower);
  let remaining = minus(ONE, sum(weights));
  const order = coefficients.map((_, i) => i).sort((i, j) => (maximum ? -1 : 1) * cmp(coefficients[i], coefficients[j]));
  for (const i of order) {
    const added = min(minus(intervals[i][1], weights[i]), remaining);
    weights[i] = plus(weights[i], added);
    remaining = minus(remaining, added);
  }
  return [dot(coefficients, weights), weights];
}

function values(objectives, entries) {
  return Object.fromEntries(objectives.map((objective, i) => [objective.id, exact(entries[i])]));
}

function strictRelation(lower, upper, sharp = true) {
  if (cmp(lower, ZERO) > 0) return 'A_STRICT';
  if (cmp(upper, ZERO) < 0) return 'B_STRICT';
  return sharp ? 'UNRESOLVED' : 'UNKNOWN';
}

function possibleOutcomes(lower, upper) {
  const outcomes = [];
  if (cmp(lower, ZERO) < 0) outcomes.push('B_LEADS');
  if (cmp(lower, ZERO) <= 0 && cmp(upper, ZERO) >= 0) outcomes.push('TIE');
  if (cmp(upper, ZERO) > 0) outcomes.push('A_LEADS');
  return outcomes;
}

function nominalCondition(objectives, coefficients, greater) {
  if (objectives.length === 2) {
    const slope = minus(coefficients[0], coefficients[1]);
    const direction = cmp(slope, ZERO);
    if (direction !== 0) {
      const threshold = divide(neg(coefficients[1]), slope);
      if (cmp(threshold, ZERO) >= 0 && cmp(threshold, ONE) <= 0) {
        const symbol = greater === (direction > 0) ? '>' : '<';
        return [`${objectives[0].label}权重 ${symbol} ${exact(threshold)}`, { objective: objectives[0].id, value: exact(threshold) }];
      }
    }
  }
  const expression = objectives.map((objective, i) => `(${exact(coefficients[i])}) × ${objective.label}权重`).join(' + ');
  return [`${expression} ${greater ? '>' : '<'} 0`, null];
}

function aggregate(state, feasible, comparisons, table, summary) {
  const wins = new Map(feasible.map(option => [option.id, 0]));
  const labels = new Map(feasible.map(option => [option.id, option.label]));
  const rows = [];
  for (const pair of comparisons) {
    if (pair.relation === 'A_STRICT') wins.set(pair.a, wins.get(pair.a) + 1);
    if (pair.relation === 'B_STRICT') wins.set(pair.b, wins.get(pair.b) + 1);
    const qualifier = pair.bounds === 'outer' ? '（保守界）' : '';
    rows.push({ label: `${labels.get(pair.a)} − ${labels.get(pair.b)}${qualifier}`, lower: Number(pair.lower), upper: Number(pair.upper) });
  }
  const leaders = feasible.filter(option => wins.get(option.id) === feasible.length - 1).map(option => option.id);
  if (leaders.length) summary += `在这些条件下，${labels.get(leaders[0])}对所有其他可行方案严格领先。`;
  else summary += '当前条件下，没有得到对所有可行替代方案都严格领先的选项。';
  const status = leaders.length ? 'STRICT_LEADER' : comparisons.some(pair => pair.relation === 'UNKNOWN') ? 'UNKNOWN' : 'UNRESOLVED';
  return {
    summary, status, pairs: comparisons, leaders, tables: [table],
    charts: rows.length ? [{ title: '加权效用差区间（甲减乙）', unit: state.objectives[0].unit, rows }] : [],
  };
}

function fixedSensitivity(state, feasible) {
  const { objectives } = state;
  const intervals = weightIntervals(state);
  const comparisons = [];
  const rows = [];
  for (const [a, b] of pairs(feasible)) {
    const differences = objectives.map(objective => difference(a, b, objective, state)[0]);
    const [lower, minWeights] = extreme(differences, intervals);
    const [upper, maxWeights] = extreme(differences, intervals, true);
    const relation = strictRelation(lower, upper);
    const [aCondition, threshold] = nominalCondition(objectives, differences, true);
    const [bCondition] = nominalCondition(objectives, differences, false);
    const pair = {
      a: a.id, b: b.id, lower: exact(lower), upper: exact(upper), relation, bounds: 'exact',
      possible_outcomes: possibleOutcomes(lower, upper),
      minimum: { weights: values(objectives, minWeights) },
      maximum: { weights: values(objectives, maxWeights) },
      a_condition: aCondition, b_condition: bCondition,
    };
    if (threshold) pair.threshold = threshold;
    comparisons.push(pair);
    rows.push([a.label, b.label, pair.lower, pair.upper, RELATIONS[relation], aCondition, bCondition]);
  }
  let summary = '使用固定的名义得分和用户确认的权重范围。权重和为 1，效用差等于零时为并列。';
  if (state.score_dependence === 'shared_additive') summary += '名义情形将共同偏移设为零。共同误差下的结论见联合稳健性比较。';
  return aggregate(state, feasible, comparisons, {
    title: '固定得分下的权重敏感性',
    columns: ['甲', '乙', '效用差下界', '效用差上界', '关系', '甲严格领先条件', '乙严格领先条件'], rows,
  }, summary);
}

function clippingCell(a, b, [lower, upper]) {
  // The difference is piecewise affine, so only endpoints and clipping breakpoints matter.
  const breakpoints = [lower, upper, neg(a), minus(ONE, a), neg(b), minus(ONE, b)].sort(cmp);
  const candidates = breakpoints.filter(offset => cmp(lower, offset) <= 0 && cmp(offset, upper) <= 0).map(offset => {
    const aScore = clip(plus(a, offset));
    const bScore = clip(plus(b, offset));
    return { difference: minus(aScore, bScore), aScore, bScore, offset };
  });
  return [
    candidates.reduce((chosen, cell) => cmp(cell.difference, chosen.difference) < 0 ? cell : chosen),
    candidates.reduce((chosen, cell) => cmp(cell.difference, chosen.difference) > 0 ? cell : chosen),
  ];
}

function jointCells(a, b, state, clipping) {
  const minima = [];
  const maxima = [];
  for (const objective of state.objectives) {
    const [aLo, aHi] = bounds(own(a.scores, objective.id));
    const [bLo, bHi] = bounds(own(b.scores, objective.id));
    if (clipping) {
      const [low, high] = clippingCell(aLo, bLo, bounds(own(state.shared_offsets, objective.id)));
      minima.push(low);
      maxima.push(high);
    } else {
      minima.push({ difference: minus(aLo, bHi), aScore: aLo, bScore: bHi });
      maxima.push({ difference: minus(aHi, bLo), aScore: aHi, bScore: bLo });
    }
  }
  return [minima, maxima];
}

function jointWitness(objectives, rectangle, clipping, weights, cells) {
  const witness = { weights: values(objectives, weights) };
  if (rectangle || clipping) {
    witness.a_scores = values(objectives, cells.map(cell => cell.aScore));
    witness.b_scores = values(objectives, cells.map(cell => cell.bScore));
  }
  if (clipping) witness.offsets = values(objectives, cells.map(cell => cell.offset));
  return witness;
}

function rectangleInformation(a, b, state, intervals, centers, pair) {
  const [lower] = extreme(centers, intervals);
  const [upper] = extreme(centers, intervals, true);
  const loSign = cmp(lower, ZERO);
  const hiSign = cmp(upper, ZERO);
  if (loSign < 0 && hiSign > 0) {
    pair.information_gap = 'WEIGHT_CAN_REVERSE_AT_CENTER_SCORES';
    return '即使各得分取区间中点，确认的权重范围仍允许排序反转。';
  }
  if (loSign <= 0 && hiSign >= 0) {
    pair.information_gap = 'WEIGHT_PERMITS_TIE_AT_CENTER_SCORES';
    return '即使各得分取区间中点，确认的权重范围仍允许并列。';
  }
  const widths = new Set([a, b].flatMap(option => state.objectives.map(objective => {
    const [lo, hi] = bounds(own(option.scores, objective.id));
    return exact(minus(hi, lo));
  })));
  if (widths.size === 1 && state.score_transform === 'identity') {
    const ceiling = exact(divide(loSign > 0 ? lower : neg(upper), rat(2)));
    const preferred = loSign > 0 ? a : b;
    pair.score_radius_threshold = { preferred: preferred.id, strict_upper: ceiling };
    return `若各分数仍以区间中点为中心且误差半径相同，半径小于 ${ceiling} 可证明${preferred.label}严格领先。`;
  }
  return '现有权重范围下，分数区间的端点决定保证领先的条件。';
}

function jointSensitivity(state, feasible) {
  const { objectives } = state;
  const intervals = weightIntervals(state);
  const firstLower = max(intervals[0][0], minus(ONE, intervals[1][1]));
  const firstUpper = min(intervals[0][1], minus(ONE, intervals[1][0]));
  const firstMidpoint = midpoint(firstLower, firstUpper);
  const midpointWeights = [firstMidpoint, minus(ONE, firstMidpoint)];
  const rectangle = state.score_dependence === 'rectangle';
  const clipping = !rectangle && state.score_transform === 'clip_01';
  const sharp = !clipping || state.shared_offset_dependence === 'rectangle';
  let scope;
  if (rectangle) scope = '采用声明可共同实现的矩形得分区间。';
  else if (!clipping) scope = '相同的未截断加性偏移在每个目标的效用差中抵消。';
  else if (sharp) scope = '在声明可共同实现的偏移区间内检查截断转折点。';
  else scope = '偏移间的联合范围未知，使用边际区间的保守界。保守界与零相交时，排序待定。';

  const comparisons = [];
  const rows = [];
  const witnesses = [];
  const gaps = [];
  const baselines = [];
  for (const [a, b] of pairs(feasible)) {
    const [minima, maxima] = jointCells(a, b, state, clipping);
    const lowCoefficients = minima.map(cell => cell.difference);
    const highCoefficients = maxima.map(cell => cell.difference);
    const [lower, minWeights] = extreme(lowCoefficients, intervals);
    const [upper, maxWeights] = extreme(highCoefficients, intervals, true);
    const relation = strictRelation(lower, upper, sharp);
    const [aCondition] = nominalCondition(objectives, lowCoefficients, true);
    const [bCondition] = nominalCondition(objectives, highCoefficients, false);
    const centers = objectives.map(objective => minus(
      midpoint(...nominalBounds(a, objective, state)), midpoint(...nominalBounds(b, objective, state)),
    ));
    const baseline = exact(dot(centers, midpointWeights));
    const pair = {
      a: a.id, b: b.id, lower: exact(lower), upper: exact(upper), relation, bounds: sharp ? 'exact' : 'outer',
      a_condition: aCondition, b_condition: bCondition,
      nominal_baseline: { weights: values(objectives, midpointWeights), difference: baseline },
    };
    baselines.push([a.label, b.label, ...midpointWeights.map(exact), baseline]);
    if (sharp) {
      pair.possible_outcomes = possibleOutcomes(lower, upper);
      for (const [field, label, margin, weights, cells] of [
        ['minimum', '最小', pair.lower, minWeights, minima],
        ['maximum', '最大', pair.upper, maxWeights, maxima],
      ]) {
        const witness = jointWitness(objectives, rectangle, clipping, weights, cells);
        pair[field] = witness;
        const displayed = ['weights', 'a_scores', 'b_scores', 'offsets'].map(key =>
          witness[key] ? objectives.map(objective => `${objective.label} ${witness[key][objective.id]}`).join('、') : null);
        witnesses.push([a.label, b.label, label, margin, ...displayed]);
      }
    }
    let information;
    if (rectangle) information = rectangleInformation(a, b, state, intervals, centers, pair);
    else if (clipping && !sharp) information = '若需判定实际可实现的反转或并列，请核对共同偏移可联合达到的范围。';
    else if (clipping) information = '严格领先取决于声明的共同偏移范围及权重范围。';
    else information = '缩小共同偏移区间不会改变比较结果。请核对得分差和权重范围。';
    if (relation === 'UNKNOWN' || relation === 'UNRESOLVED') gaps.push(`${a.label}与${b.label}的联合稳健性。${information}`);
    comparisons.push(pair);
    rows.push([a.label, b.label, pair.lower, pair.upper, RELATIONS[relation], aCondition, bCondition, information]);
  }
  const heading = sharp ? '给定权重下的严格领先条件' : '给定权重下严格领先的充分条件';
  const result = aggregate(state, feasible, comparisons, {
    title: '权重与得分联合稳健性',
    columns: ['甲', '乙', '效用差下界', '效用差上界', '关系', `甲${heading}`, `乙${heading}`, '条件与信息缺口'], rows,
  }, `${scope}效用差等于零时为并列。计算允许权重范围与得分误差集合中的情形任意组合。联合误差依据为${state.score_dependence_source}。`);
  result.tables.push({
    title: rectangle ? '参考比较（可行权重中点与分数中点）' : '参考比较（可行权重中点与零共同偏移）',
    columns: ['甲', '乙', ...objectives.map(objective => `${objective.label}权重`), '效用差'], rows: baselines,
  });
  if (witnesses.length) result.tables.push({
    title: '达到效用差边界的情形',
    columns: ['甲', '乙', '边界', '效用差', '权重', '甲得分', '乙得分', '共同偏移'], rows: witnesses,
  });
  if (gaps.length) result.gaps = gaps;
  return result;
}

export function sensitivity(state, options = {}) {
  const modelId = options.model_id ?? JOINT;
  if (![FIXED, JOINT].includes(modelId)) return receipt(modelId, 'INELIGIBLE', ['此加权方法未在移动端注册。']);
  const joint = modelId === JOINT;
  return runScoring(modelId, state, options, (state, feasible) => weightErrors(state, feasible, joint),
    joint ? jointSensitivity : fixedSensitivity);
}
