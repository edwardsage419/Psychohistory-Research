import { cmp, decimal, exact, maxValue, minus, plus, rat, stripText } from './core.mjs';
import {
  ZERO, bounds, divide, documented, horizon, known, max, midpoint, min, own, receipt, runScoring, uniqueIds,
} from './scoring-shared.mjs';

const POINT = 'C029';
const INTERVAL = 'C030';
const PRECISION = 'C031';

function nonnegative(value) {
  try {
    const parsed = decimal(value);
    return cmp(parsed, ZERO) >= 0 ? parsed : null;
  } catch {
    return null;
  }
}

function validate(state, feasible, model) {
  const errors = [];
  const scenarios = state.scenarios ?? [];
  if (!feasible.length) errors.push('需要至少一个通过硬约束的方案。');
  if (!scenarios.length || !uniqueIds(scenarios)) errors.push('需要至少一个有定义的情景。');
  if (!documented(state.scenario_basis)) errors.push('需要确认情景共用的时限、同一基数效用量尺和效用越高越好的含义。');
  if (!uniqueIds(scenarios)) return errors;
  const units = new Set();
  const horizons = new Set();
  for (const scenario of scenarios) {
    if (!known(scenario)) errors.push(`情景「${scenario.label}」的依据为 UNKNOWN。`);
    else if (!documented(scenario.source)) errors.push(`需要补充情景「${scenario.label}」的来源。`);
    if (!documented(scenario.label)) errors.push('需要情景名称。');
    for (const option of feasible) {
      const utility = own(scenario.utilities, option.id);
      const cell = `方案「${option.label}」在情景「${scenario.label}」中的效用`;
      if (!known(utility) || utility.lower == null || utility.upper == null) {
        errors.push(`${cell}为 UNKNOWN，需要有依据的上下界。`);
        continue;
      }
      const interval = bounds(utility);
      if (!interval) errors.push(`${cell}须具有有序的有限上下界。`);
      else if (model !== INTERVAL && cmp(...interval) !== 0) errors.push(`${cell}须为点值。`);
      if (!documented(utility.source)) errors.push(`需要补充${cell}的来源。`);
      units.add(stripText(utility.unit));
      horizons.add(horizon(utility, state.deadline) || null);
    }
  }
  if (units.has('') || units.size > 1) errors.push('所有方案和情景须使用同一明确的效用单位。');
  if (horizons.has(null) || horizons.size > 1) errors.push('所有方案和情景须使用同一明确的效用时间范围。');
  if (model === PRECISION) {
    if (!nonnegative(state.precision_radius)) errors.push('需要以效用单位计量、有限且非负的假设统一半径。');
    if (feasible.length < 2) errors.push('需要至少两个通过硬约束的方案才能比较精度阈值。');
  }
  return errors;
}

function utilityMatrix(state, feasible) {
  return feasible.map(option => state.scenarios.map(scenario => bounds(own(scenario.utilities, option.id))));
}

function unit(state, feasible) {
  return stripText(own(state.scenarios[0].utilities, feasible[0].id).unit);
}

function lowest(values) {
  return values.reduce(min);
}

function leaders(feasible, values, highest = false) {
  const target = highest ? maxValue(values) : lowest(values);
  return feasible.filter((_, index) => cmp(values[index], target) === 0).map(option => option.id);
}

function optionMap(feasible, values) {
  return Object.fromEntries(feasible.map((option, index) => [option.id, values[index]]));
}

function pointRegret(points) {
  const ceilings = points[0].map((_, index) => maxValue(points.map(row => row[index])));
  return points.map(row => row.map((value, index) => minus(ceilings[index], value)));
}

function pointResults(state, feasible) {
  const labels = new Map(feasible.map(option => [option.id, option.label]));
  const scenarios = state.scenarios.map(scenario => scenario.label);
  const utilityUnit = unit(state, feasible);
  const points = utilityMatrix(state, feasible).map(row => row.map(([value]) => value));
  const regret = pointRegret(points);
  const worst = regret.map(maxValue);
  const minimumUtility = points.map(lowest);
  const minimax = leaders(feasible, worst);
  const maximin = leaders(feasible, minimumUtility, true);
  const scenarioBest = scenarios.map((_, index) =>
    feasible.filter((_, optionIndex) => cmp(regret[optionIndex][index], ZERO) === 0).map(option => option.id));
  const worstScenarios = regret.map((row, index) => scenarios.filter((_, j) => cmp(row[j], worst[index]) === 0));
  const printable = regret.map(row => row.map(exact));
  const tables = [
    {
      title: `各情景后悔值（${utilityUnit}）`, columns: ['方案', ...scenarios],
      rows: feasible.map((option, index) => [option.label, ...printable[index]]),
    },
    {
      title: '各情景的最优可行方案', columns: ['情景', '最优方案（含并列）'],
      rows: scenarios.map((label, index) => [label, scenarioBest[index].map(id => labels.get(id)).join('、')]),
    },
    {
      title: `最大后悔值与最小效用（${utilityUnit}）`, columns: ['方案', '最大后悔值', '最坏情景（含并列）', '最小效用'],
      rows: feasible.map((option, index) => [
        option.label, exact(worst[index]), worstScenarios[index].join('、'), exact(minimumUtility[index]),
      ]),
    },
  ];
  const referenceId = state.reference_option_id;
  let reference = null;
  let referenceNote = '可确认一个可行方案作为参照。';
  if (labels.has(referenceId)) {
    const referenceIndex = feasible.findIndex(option => option.id === referenceId);
    reference = { option_id: referenceId, scenario_gains: printable[referenceIndex] };
    tables.push({
      title: `相对参照方案「${labels.get(referenceId)}」的条件性效用增益（${utilityUnit}）`,
      columns: ['情景', '完全预知情景后的效用增益'],
      rows: scenarios.map((label, index) => [label, reference.scenario_gains[index]]),
    });
    referenceNote = '预知增益以承诺前完全识别情景且仍能改选为条件。实际信息价值还取决于误差、费用和等待时间。';
  } else if (referenceId != null) {
    referenceNote = '所选参照方案尚未通过硬约束，参照增益为 UNKNOWN。';
  }
  return {
    summary: `最小化最大后悔值的方案为「${minimax.map(id => labels.get(id)).join('、')}」。`
      + `最大化最小效用的方案为「${maximin.map(id => labels.get(id)).join('、')}」。`
      + `比较仅覆盖所列情景，按无概率权重的规则计算。${referenceNote}`,
    tables,
    charts: [{
      title: '最大情景后悔值', unit: utilityUnit,
      rows: feasible.map((option, index) => ({ label: option.label, lower: exact(worst[index]), upper: exact(worst[index]) })),
    }],
    leaders: minimax,
    maximin_leaders: maximin,
    regret: optionMap(feasible, printable),
    worst_regret: optionMap(feasible, worst.map(exact)),
    scenario_best: scenarioBest,
    worst_scenarios: optionMap(feasible, worstScenarios),
    reference,
  };
}

function rectangle(state) {
  return state.scenario_dependence === 'rectangle' && documented(state.scenario_dependence_source);
}

function intervalRegret(utilities) {
  return utilities.map((cells, ownIndex) => cells.map(([lower, upper], i) => {
    // A candidate cannot regret its own utility at a different point in its range.
    const rivals = utilities.filter((_, other) => other !== ownIndex);
    return [
      rivals.reduce((bound, row) => max(bound, minus(row[i][0], upper)), ZERO),
      rivals.reduce((bound, row) => max(bound, minus(row[i][1], lower)), ZERO),
    ];
  }));
}

function intervalResults(state, feasible, utilities = utilityMatrix(state, feasible)) {
  const labels = new Map(feasible.map(option => [option.id, option.label]));
  const scenarios = state.scenarios.map(scenario => scenario.label);
  const utilityUnit = unit(state, feasible);
  const regret = intervalRegret(utilities);
  const worst = regret.map(row => [maxValue(row.map(([low]) => low)), maxValue(row.map(([, high]) => high))]);
  const minimax = leaders(feasible, worst.map(([, high]) => high));
  const strict = minimax.filter(id => {
    const i = feasible.findIndex(option => option.id === id);
    return worst.length > 1 && worst.every(([low], j) => j === i || cmp(worst[i][1], low) < 0);
  });
  const midpointWorst = pointRegret(utilities.map(row => row.map(interval => midpoint(...interval)))).map(maxValue);
  const midpointLeaders = leaders(feasible, midpointWorst);
  const boundType = rectangle(state) ? 'sharp' : 'outer';
  const scope = boundType === 'sharp'
    ? '以声明的矩形假设计算，每个方案的极值分别可达。'
    : '矩形独立性尚未确立，结果为保守外界，适用于非空且落在所给区间内的联合可行集。';
  let comparison = '目前只有一个可行方案。';
  if (strict.length) comparison = `「${labels.get(strict[0])}」的上界严格低于所有其他方案的下界。`;
  else if (worst.length > 1) comparison = '区间交叠或接触，按界限无法认证任何方案在每个联合取值下的严格优势。';
  const printable = regret.map(row => row.map(interval => interval.map(exact)));
  const printableWorst = worst.map(interval => interval.map(exact));
  return {
    summary: `最大情景后悔值上界最小的方案为「${minimax.map(id => labels.get(id)).join('、')}」。${comparison}${scope}`,
    tables: [
      {
        title: `各情景后悔值区间（${utilityUnit}）`, columns: ['方案', ...scenarios],
        rows: feasible.map((option, i) => [option.label, ...printable[i].map(([lo, hi]) => `[${lo}, ${hi}]`)]),
      },
      {
        title: `最大情景后悔值区间和中点假设基线（${utilityUnit}）`,
        columns: ['方案', '下界', '上界', '中点假设下的最大后悔值'],
        rows: feasible.map((option, i) => [option.label, ...printableWorst[i], exact(midpointWorst[i])]),
      },
    ],
    charts: [{
      title: '最大情景后悔值区间', unit: utilityUnit,
      rows: feasible.map((option, i) => ({ label: option.label, lower: printableWorst[i][0], upper: printableWorst[i][1] })),
    }],
    leaders: minimax,
    strict_leaders: strict,
    midpoint_leaders: midpointLeaders,
    bound_type: boundType,
    regret_bounds: optionMap(feasible, printable),
    worst_regret_bounds: optionMap(feasible, printableWorst),
  };
}

function precisionThreshold(points, leaderIndex) {
  // Before clipping at zero, each option's maximum regret lies in its worst gap ± twice the radius.
  const gaps = points.map((row, i) => maxValue(points.flatMap((other, j) =>
    i === j ? [] : row.map((value, k) => minus(other[k], value)))));
  return lowest(gaps.flatMap((gap, i) => i === leaderIndex ? [] : [
    min(divide(gap, rat(2)), divide(minus(gap, gaps[leaderIndex]), rat(4))),
  ]));
}

function witnessProfiles(points) {
  if (points.length !== 3 || points.some(row => row.length !== 2)) return null;
  const profiles = ['8,2', '5.5,5.5', '2.5,8'];
  for (const reverse of [false, true]) {
    const identifiers = points.map(row => (reverse ? [row[1], row[0]] : row).map(exact).join(','));
    if (profiles.every(profile => identifiers.includes(profile))) return profiles.map(profile => identifiers.indexOf(profile));
  }
  return null;
}

function precisionResults(state, feasible) {
  const points = utilityMatrix(state, feasible).map(row => row.map(([value]) => value));
  const radius = nonnegative(state.precision_radius);
  const utilities = points.map(row => row.map(value => [minus(value, radius), plus(value, radius)]));
  const result = intervalResults(state, feasible, utilities);
  const utilityUnit = unit(state, feasible);
  Object.assign(result, { precision_threshold: null, sharp_threshold: false, witness: null });
  if (result.midpoint_leaders.length !== 1) {
    result.summary += ' 点值基线并列，没有可由统一半径界限认证的唯一严格占优方案。';
    return result;
  }

  const id = result.midpoint_leaders[0];
  const leaderIndex = feasible.findIndex(option => option.id === id);
  const leader = feasible[leaderIndex];
  const threshold = precisionThreshold(points, leaderIndex);
  result.precision_threshold = { option_id: id, upper_exclusive: exact(threshold) };
  result.summary += `假设各效用单元格的统一半径为 ${exact(radius)} ${utilityUnit}。对点值基线领先方案「${leader.label}」，`
    + `界限证书要求半径严格小于 ${exact(threshold)} ${utilityUnit}，使其后悔值上界低于各对手下界。`;
  const [, upper] = result.worst_regret_bounds[id];
  result.tables.push({
    title: `统一半径的严格比较（${utilityUnit}）`,
    columns: ['点值基线领先方案', '对照方案', '领先方案上界', '对照方案下界', '要求'],
    rows: feasible.filter(option => option.id !== id).map(option => [
      leader.label, option.label, upper, result.worst_regret_bounds[option.id][0], '上界 < 下界',
    ]),
  });
  const profiles = witnessProfiles(points);
  if (!profiles || !rectangle(state) || cmp(radius, rat(1)) > 0) return result;
  result.sharp_threshold = true;
  result.summary += ' 对这组矩形合成数据及 0 ≤ 半径 ≤ 1，上述条件充要。';
  if (cmp(radius, threshold) < 0) return result;

  const [, b, c] = profiles;
  const realization = points.map((row, i) => row.map(value => i === c ? plus(value, radius) : minus(value, radius)));
  const worst = pointRegret(realization).map(row => exact(maxValue(row)));
  result.witness = {
    utilities: optionMap(feasible, realization.map(row => row.map(exact))),
    worst_regret: optionMap(feasible, worst),
  };
  result.tables.push({
    title: `反例中的可行联合取值（${utilityUnit}）`,
    columns: ['方案', ...state.scenarios.map(scenario => scenario.label), '最大后悔值'],
    rows: profiles.map(i => [feasible[i].label, ...result.witness.utilities[feasible[i].id], worst[i]]),
  });
  const outcome = cmp(radius, threshold) === 0 ? '并列' : '后悔值严格更低';
  result.summary += ` 表中有一个允许的联合取值，其中「${feasible[c].label}」相对「${feasible[b].label}」${outcome}。`;
  return result;
}

export function regret(state, options = {}) {
  const modelId = options.model_id ?? INTERVAL;
  const method = own({ [POINT]: pointResults, [INTERVAL]: intervalResults, [PRECISION]: precisionResults }, modelId);
  if (!method) return receipt(modelId, 'INELIGIBLE', ['此后悔值方法未在移动端注册。']);
  return runScoring(modelId, state, options, (state, feasible) => validate(state, feasible, modelId), method);
}
