import { cmp, decimal, exact, minus, stripText, times } from './core.mjs';
import { ZERO, bounds, known, own, runScoring } from './scoring-shared.mjs';

const MODEL = 'timing_actions';
const STRATEGY_LABELS = { act_now: '立即行动', status_quo: '维持现状', wait: '等待后行动' };
const FORECAST_LABELS = { WITHIN: '在期限内', AFTER: '越过期限', STRADDLES: '预测区间跨过期限', UNKNOWN: '待核对' };
const STATUS_LABELS = { EXPIRED: '已截止', FEASIBLE: '可执行', UNKNOWN: '待核对' };
const TIME_FIELDS = {
  horizon: '分析时域', decision_deadline: '决定截止', desired_time: '希望完成时间',
  predicted_completion: '预测完成时间', wait_duration: '拟等待时长',
};
const CHART_LIMIT = 4;

function sourced(value) {
  return known(value) && Boolean(stripText(value.source));
}

function point(value) {
  const interval = bounds(value);
  return sourced(value) && interval && cmp(...interval) === 0 ? interval[0] : null;
}

function within(time, cutoff) {
  const difference = cmp(time, decimal(cutoff.at));
  return difference < 0 || (difference === 0 && cutoff.inclusive === true);
}

export function availability(timing, optionId, time) {
  const rule = own(timing.actions, optionId);
  const cutoffs = [timing.horizon, timing.decision_deadline, rule?.cutoff].filter(value => value != null);
  if (cutoffs.some(cutoff => sourced(cutoff) && !within(time, cutoff))) return 'EXPIRED';
  if (!rule || cutoffs.some(cutoff => !sourced(cutoff))) return 'UNKNOWN';
  return 'FEASIBLE';
}

export function immediateAvailability(timing, optionId) {
  if (timing?.confirmed !== true || !timing.time_origin || !timing.time_unit || !sourced(timing.horizon)) return 'UNKNOWN';
  try {
    return availability(timing, optionId, ZERO);
  } catch {
    return 'UNKNOWN';
  }
}

export function timingErrors(state, feasible) {
  const timing = state.timing;
  if (!timing) return ['需要设置行动时机。'];
  const errors = [];
  if (timing.confirmed !== true) errors.push('请确认行动时机及时间假设。');
  if (!timing.time_unit || !timing.time_origin || !sourced(timing.horizon)) {
    errors.push('需要共同的时间单位、起算时点与有来源的分析时域。');
  }
  if (!feasible.length) errors.push('需要至少一个通过硬约束的行动。');
  const scenarios = state.scenarios ?? [];
  if (!scenarios.length || !state.scenario_basis) errors.push('需要情景及已确认的共同基数效用口径。');
  const optionIds = new Set(state.options.map(option => option.id));
  const scenarioIds = new Set(scenarios.map(scenario => scenario.id));
  const references = [...Object.keys(timing.actions ?? {}), timing.status_quo_option_id, timing.fallback_option_id];
  if (references.some(id => id != null && !optionIds.has(id))) errors.push('行动时机引用了不存在的方案。');
  if (Object.values(timing.actions ?? {}).some(rule => Object.keys(rule.delay_losses ?? {}).some(id => !scenarioIds.has(id)))) {
    errors.push('延迟损失引用了不存在的情景。');
  }
  return errors;
}

export function timingUtilities(state, feasible, supportedStates) {
  const units = new Set();
  const horizons = new Set();
  const gaps = [];
  const options = feasible.filter(option => immediateAvailability(state.timing, option.id) === 'FEASIBLE');
  const utility = new Map();
  for (const scenario of state.scenarios) {
    if (supportedStates && !supportedStates.has(scenario.id)) continue;
    const row = new Map();
    for (const option of options) {
      const quantity = own(scenario.utilities, option.id);
      const value = point(quantity);
      const horizon = quantity ? quantity.horizon || state.deadline : null;
      if (!sourced(scenario) || value === null || horizon == null) {
        gaps.push(`「${option.label}」在「${scenario.label}」中的效用点值、来源或观察时域待核对。`);
      } else {
        units.add(stripText(quantity.unit));
        horizons.add(stripText(horizon));
        row.set(option.id, value);
      }
    }
    utility.set(scenario.id, row);
  }
  if (units.size > 1 || horizons.size > 1) {
    gaps.push('所有行动情景需要采用同一效用单位和观察时域。');
    return { utilities: new Map(), unit: null, gaps };
  }
  return { utilities: utility, unit: units.values().next().value ?? null, gaps };
}

function relative(prediction, cutoff) {
  const interval = bounds(prediction);
  if (!sourced(prediction) || !interval || !sourced(cutoff)) return 'UNKNOWN';
  const [lower, upper] = interval;
  if (!within(lower, cutoff)) return 'AFTER';
  return within(upper, cutoff) ? 'WITHIN' : 'STRADDLES';
}

function renderTimeValue(value) {
  if (value == null) return null;
  const exactNumber = number => number == null ? null : exact(decimal(number));
  const kind = value.kind ?? 'unknown';
  const source = value.source ?? '';
  return Object.hasOwn(value, 'at')
    ? { at: exactNumber(value.at), inclusive: value.inclusive, kind, source }
    : { lower: exactNumber(value.lower), upper: exactNumber(value.upper), kind, source };
}

export function timeInputs(state, feasible) {
  const { timing } = state;
  const inputs = { time_unit: timing.time_unit, time_origin: timing.time_origin };
  for (const key of Object.keys(TIME_FIELDS)) inputs[key] = renderTimeValue(timing[key]);
  const prediction = timing.predicted_completion;
  inputs.prediction_vs_deadline = relative(prediction, timing.decision_deadline);
  inputs.prediction_vs_horizon = relative(prediction, timing.horizon);
  inputs.prediction_vs_action_cutoffs = Object.fromEntries(feasible.flatMap(option => {
    const cutoff = own(timing.actions, option.id)?.cutoff;
    return cutoff ? [[option.id, relative(prediction, cutoff)]] : [];
  }));
  return inputs;
}

function cutoffText(cutoff, number) {
  return `${cutoff.inclusive ? '≤' : '<'} ${number}`;
}

export function timingTables(state, feasible, times) {
  const { timing } = state;
  const rows = [];
  for (const [key, label] of Object.entries(TIME_FIELDS)) {
    const value = times[key];
    if (!value) continue;
    const interval = Object.hasOwn(value, 'at') ? cutoffText(value, value.at)
      : `[${value.lower ?? '?'}，${value.upper ?? '?'}]`;
    rows.push([label, interval, value.kind, value.source]);
  }
  const reversibility = [];
  const payoffInputs = [];
  for (const option of feasible) {
    const action = own(timing.actions, option.id);
    const cutoff = action?.cutoff;
    if (cutoff) rows.push([`「${option.label}」行动截止`, cutoffText(cutoff, exact(decimal(cutoff.at))), cutoff.kind, cutoff.source ?? '']);
    const detail = action?.reversibility;
    reversibility.push([option.label, sourced(detail) ? detail.description : 'UNKNOWN', detail ? detail.source ?? '' : null]);
    if (!action) continue;
    const entries = [[null, '换转成本', action.switching_cost], ...state.scenarios.map(scenario => [
      scenario.label, '单位时间延迟损失', own(action.delay_losses, scenario.id),
    ])];
    for (const [scenarioLabel, role, value] of entries) {
      const measurement = point(value);
      payoffInputs.push([
        option.label, scenarioLabel, role, measurement !== null ? exact(measurement) : null, value?.kind ?? 'unknown',
        value ? value.source ?? '' : null,
      ]);
    }
  }
  const tables = [
    { title: `时间口径（从「${timing.time_origin}」起算，${timing.time_unit}）`, columns: ['用途', '时间', '证据类型', '来源'], rows },
    { title: '撤销条件与影响', columns: ['方案', '可逆性说明', '来源'], rows: reversibility },
    { title: '换转成本及延迟损失依据', columns: ['方案', '情景', '用途', '数值', '证据类型', '来源'], rows: payoffInputs },
  ];
  if (timing.predicted_completion) {
    const checks = [['分析时域', FORECAST_LABELS[times.prediction_vs_horizon]]];
    if (timing.decision_deadline) checks.push(['决定截止', FORECAST_LABELS[times.prediction_vs_deadline]]);
    for (const option of feasible) {
      const relation = own(times.prediction_vs_action_cutoffs, option.id);
      if (relation) checks.push([`「${option.label}」行动截止`, FORECAST_LABELS[relation]]);
    }
    tables.push({ title: '完成预测与期限', columns: ['边界', '完成预测关系'], rows: checks });
  }
  return tables;
}

export function timingPayoff(state, option, duration, utilities) {
  const rule = own(state.timing.actions, option.id);
  const switching = point(rule.switching_cost);
  if (switching === null) {
    return { values: new Map(), gaps: [`需要「${option.label}」有来源的换转成本点值，已确认无成本时可填零。`] };
  }
  const payoffs = new Map();
  const gaps = [];
  for (const scenario of state.scenarios) {
    const value = utilities.get(scenario.id)?.get(option.id);
    const loss = cmp(duration, ZERO) === 0 ? ZERO : point(own(rule.delay_losses, scenario.id));
    if (value === undefined || loss === null) {
      gaps.push(`「${option.label}」在「${scenario.label}」中的效用或单位时间延迟损失为 UNKNOWN。`);
    } else {
      payoffs.set(scenario.id, minus(minus(value, switching), times(duration, loss)));
    }
  }
  return { values: payoffs, gaps };
}

function dominates(other, candidate) {
  const comparisons = [...candidate.payoffs].map(([id, value]) => cmp(other.payoffs.get(id), value));
  return comparisons.every(relation => relation >= 0) && comparisons.some(relation => relation > 0);
}

function actionComparison(state, feasible) {
  const { timing, scenarios } = state;
  const { utilities, unit, gaps } = timingUtilities(state, feasible);
  const wait = point(timing.wait_duration);
  const unknownWait = timing.wait_duration != null && wait === null;
  if (unknownWait) gaps.push('拟等待时长需要一个有来源的点值才能比较固定等待方案。');
  if (timing.status_quo_option_id != null && !feasible.some(option => option.id === timing.status_quo_option_id)) {
    gaps.push('用户标注的现状方案尚未通过硬约束。');
  }
  const rows = [];
  const strategies = [];
  const values = [];
  for (const option of feasible) {
    const type = option.id === timing.status_quo_option_id ? 'status_quo' : 'act_now';
    const plans = [[type, ZERO]];
    if (wait !== null) plans.push(['wait', wait]);
    for (const [strategy, time] of plans) {
      let status = availability(timing, option.id, time);
      const duration = exact(time);
      let payoffs = new Map();
      if (status === 'EXPIRED') gaps.push(`「${option.label}」在 ${duration} ${timing.time_unit} 已越过所列截止或分析时域。`);
      else if (status === 'UNKNOWN') gaps.push(`需要核对「${option.label}」的行动时间规则及期限来源。`);
      else {
        let missing;
        ({ values: payoffs, gaps: missing } = timingPayoff(state, option, time, utilities));
        if (missing.length) {
          status = 'UNKNOWN';
          gaps.push(...missing);
        } else {
          values.push({ strategy, option, payoffs });
        }
      }
      strategies.push({
        type: strategy, option_id: option.id, status, duration,
        utilities: Object.fromEntries([...payoffs].map(([key, value]) => [key, exact(value)])),
      });
      rows.push([option.label, STRATEGY_LABELS[strategy], duration, STATUS_LABELS[status],
        ...scenarios.map(scenario => payoffs.has(scenario.id) ? exact(payoffs.get(scenario.id)) : null)]);
    }
  }

  const undominated = values.filter(candidate => !values.some(other => dominates(other, candidate)));
  const frontier = undominated.map(({ strategy, option }) => ({ type: strategy, option_id: option.id }));
  const incomplete = !values.length || strategies.some(row => row.status === 'UNKNOWN') || unknownWait;
  let summary = '逐情景比较立即行动、现状与已填报的固定等待。每种策略预先固定行动，比较未使用任何概率。';
  let leaders = [];
  if (incomplete) summary += '部分结果待核对，完整行动排序为 UNKNOWN。';
  else if (undominated.length) {
    const options = new Map(undominated.map(({ option }) => [option.id, option.label]));
    if (options.size === 1) leaders = [...options.keys()];
    summary += `在当前情景中，${[...options.values()].join('、')}对应未被其他可执行策略支配的结果。`;
  }
  const times = timeInputs(state, feasible);
  const tables = timingTables(state, feasible, times);
  tables.push({
    title: `可行时机与逐情景效用（${unit || '效用单位待核对'}）`,
    columns: ['中性方案名', '用户标明的角色', `行动时刻（${timing.time_unit}）`, '时间可行性', ...scenarios.map(scenario => scenario.label)],
    rows,
  });
  const charts = unit && values.length ? scenarios.slice(0, CHART_LIMIT).map(scenario => ({
    title: `「${scenario.label}」的行动时机效用`, unit,
    rows: values.map(({ strategy, option, payoffs }) => {
      const value = exact(payoffs.get(scenario.id));
      return { label: `${option.label}（${STRATEGY_LABELS[strategy]}）`, lower: value, upper: value };
    }),
  })) : [];
  if (charts.length && scenarios.length > CHART_LIMIT) summary += `图中显示前 ${CHART_LIMIT} 个情景，表中保留所有情景。`;
  return {
    summary, status: incomplete ? 'UNKNOWN' : 'SCENARIO_COMPARISON', probabilities_used: false,
    strategies, undominated_strategies: frontier, leaders, time_inputs: times, tables, charts, gaps: [...new Set(gaps)],
  };
}

export function timingActions(state, options = {}) {
  return runScoring(MODEL, state, options, timingErrors, actionComparison);
}
