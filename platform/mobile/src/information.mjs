import { cmp, exact, maxValue, minus, plus, stripText, times } from './core.mjs';
import { bounds, divide, documented, horizon, known, max, min, ONE, own, runScoring, sum, ZERO } from './scoring-shared.mjs';

const model = 'voi_point';
const sourced = value => known(value) && documented(value.source);
function point(value) {
  const range = bounds(value);
  return sourced(value) && range && cmp(...range) === 0 ? range[0] : null;
}
function distribution(keys, record, label, kinds, errors) {
  const intervals = [];
  for (const key of keys) {
    const item = own(record, key);
    const range = bounds(item);
    if (!sourced(item) || !range || cmp(range[0], ZERO) < 0 || cmp(range[1], ONE) > 0) {
      errors.push(`${label}中「${key}」缺少有来源的概率上下界。`);
    } else {
      intervals.push(range);
      kinds.add(item.kind);
    }
  }
  if (intervals.length !== keys.length) return null;
  const lower = sum(intervals.map(row => row[0])), upper = sum(intervals.map(row => row[1]));
  if (cmp(lower, ONE) > 0 || cmp(upper, ONE) < 0) {
    errors.push(`${label}的区间无法组成合计为 1 的概率。`);
    return null;
  }
  return intervals.map(([low, high]) => [max(low, minus(ONE, minus(upper, high))), min(high, minus(ONE, minus(lower, low)))]);
}

function prepare(state, feasible) {
  const info = state.information;
  if (!info) return { errors: ['需要填写调查信号、概率、成本及行动条件。'] };
  const errors = [];
  if (!state.scenarios.length || !documented(state.scenario_basis)) errors.push('需要确认状态集与可比较的基数效用量尺。');
  if (!feasible.length) errors.push('没有通过已确认硬约束的立即行动。');
  if (!info.signals.length) errors.push('需要列出有限且互斥、覆盖结果的调查信号。');
  if (!info.timing_basis) errors.push('需要说明调查在行动前完成且没有等待机会损失的依据。');
  if (info.unrestricted_actions && (!documented(info.action_source) || Object.keys(info.actions_by_signal).length)) {
    errors.push('需要一个明确的调查后行动集合及依据。');
  }
  if (errors.length) return { errors };
  const kinds = new Set();
  const stateIds = state.scenarios.map(x => x.id), signalIds = info.signals.map(x => x.id);
  const optionIds = new Set(state.options.map(x => x.id));
  const hasForeign = (record, ids) => Object.keys(record ?? {}).some(x => !ids.includes(x));
  if (hasForeign(info.prior, stateIds) || hasForeign(info.likelihoods, stateIds)) errors.push('概率输入指向不存在的状态。');
  if (hasForeign(info.actions_by_signal, signalIds) || Object.values(info.likelihoods).some(row => hasForeign(row, signalIds))) {
    errors.push('概率或行动输入指向不存在的信号。');
  }
  if (Object.values(info.actions_by_signal).some(row => row.option_ids.some(id => !optionIds.has(id)))) {
    errors.push('调查后的行动条件指向不存在的方案。');
  }
  const prior = distribution(stateIds, info.prior, '状态先验', kinds, errors);
  if (errors.length) return { errors };
  const units = new Set(), horizons = new Set();
  const active = [];
  for (const [index, scenario] of state.scenarios.entries()) {
    if (!prior[index][1].n) continue;
    if (!sourced(scenario)) errors.push(`状态「${scenario.label}」需要来源。`);
    kinds.add(scenario.kind);
    const likelihood = distribution(signalIds, own(info.likelihoods, scenario.id), `状态「${scenario.label}」的条件信号概率`, kinds, errors);
    const utility = feasible.map(option => {
      const value = own(scenario.utilities, option.id), numeric = point(value);
      if (!numeric) errors.push(`需要方案「${option.label}」在状态「${scenario.label}」中有来源的点效用。`);
      else {
        units.add(stripText(value.unit));
        horizons.add(horizon(value, state.deadline));
        kinds.add(value.kind);
      }
      return numeric;
    });
    active.push({ id: scenario.id, prior: prior[index], likelihood, utility });
  }
  const cost = point(info.cost);
  if (!cost || cmp(cost, ZERO) < 0) errors.push('需要有来源、非负且可比较的调查点成本。');
  else {
    units.add(stripText(info.cost.unit));
    if (info.cost.horizon) horizons.add(stripText(info.cost.horizon));
    kinds.add(info.cost.kind);
  }
  if (units.size !== 1 || units.has('')) errors.push('成本及各行动效用须共用同一明确单位。');
  if (horizons.size !== 1 || horizons.has(null)) errors.push('成本及各行动效用须基于同一明确时间范围。');
  if (errors.length) return { errors };
  const actions = info.signals.map((signal, z) => {
    if (!active.some(row => row.likelihood[z][1].n)) return [];
    if (info.unrestricted_actions) return feasible.map((_, index) => index);
    const allowed = own(info.actions_by_signal, signal.id);
    if (!sourced(allowed)) {
      errors.push(`信号「${signal.label}」的可行动作及来源为 UNKNOWN。`);
      return [];
    }
    kinds.add(allowed.kind);
    const indices = feasible.flatMap((option, index) => allowed.option_ids.includes(option.id) ? [index] : []);
    if (!indices.length) errors.push(`信号「${signal.label}」有正概率，需要已通过硬约束的行动或明确兜底行动。`);
    return indices;
  });
  if (errors.length) return { errors };
  if (active.some(row => [row.prior, ...row.likelihood].some(interval => cmp(...interval) !== 0))) {
    return { errors: ['点值计算需要唯一的先验和条件信号概率。'] };
  }
  const evidence = kinds.has('synthetic') ? 'SYNTHETIC' : documented(info.verification_source) &&
    [...kinds].every(kind => ['fact', 'estimate'].includes(kind)) ? 'USER_ATTESTED' : 'CONDITIONAL';
  return { errors, active, actions, cost, unit: stripText(info.cost.unit), evidence };
}

function evaluate(state, options, { active, actions, cost, unit, evidence }) {
  const baseline = options.map((_, a) => sum(active.map(row => times(row.prior[0], row.utility[a]))));
  const baselineValue = maxValue(baseline);
  const baselineActions = options.filter((_, i) => cmp(baseline[i], baselineValue) === 0).map(option => option.id);
  const evpi = minus(sum(active.map(row => times(row.prior[0], maxValue(row.utility)))), baselineValue);
  let informed = ZERO;
  const signals = Object.fromEntries(state.information.signals.map((signal, z) => {
    const weights = active.map(row => times(row.prior[0], row.likelihood[z][0]));
    const probability = sum(weights);
    if (!probability.n) return [signal.id, { probability: '0', actions: [], posterior: null, joint_value: '0' }];
    const values = actions[z].map(a => sum(active.map((row, i) => times(weights[i], row.utility[a]))));
    const top = maxValue(values);
    informed = plus(informed, top);
    return [signal.id, {
      probability: exact(probability), actions: actions[z].filter((_, i) => cmp(top, values[i]) === 0).map(i => options[i].id),
      posterior: Object.fromEntries(active.map((row, i) => [row.id, exact(divide(weights[i], probability))])), joint_value: exact(top),
    }];
  }));
  const gross = minus(informed, baselineValue), net = minus(gross, cost);
  const unrestricted = actions.every(row => !row.length || row.length === options.length);
  const decision = net.n > 0n ? 'POSITIVE' : net.n < 0n ? 'NEGATIVE' : 'TIE';
  const result = {
    summary: `先比较免调查的立即行动，再按各信号选择可执行行动。${unrestricted ? '点值 EVSI' : '有行动限制的调查收益差'}。` +
      `在声明的范围与假设下，调查净优势${{ POSITIVE: '严格为正', NEGATIVE: '严格为负', TIE: '等于零' }[decision]}。` +
      { SYNTHETIC: '含合成输入，输出用于数学演示。', CONDITIONAL: '结果为给定假设和来源的条件计算。',
        USER_ATTESTED: '用户声明已核对所填点值。系统没有独立核实来源、准确性或现实适用性。' }[evidence],
    evidence_status: evidence, decision, net_bounds: { lower: exact(net), upper: exact(net) }, range_kind: 'EXACT',
    cost: exact(cost), break_even_cost: { lower: exact(gross), upper: exact(gross), unit },
    baseline_value: exact(baselineValue), baseline_actions: baselineActions, information_value: exact(informed),
    evpi: exact(evpi), evsi: unrestricted ? exact(gross) : null, gross_advantage: exact(gross), net_value: exact(net), signals,
    tables: [
      { title: '立即行动和调查条件比较', columns: ['免调查基线', '调查后期望效用', '调查收益差', '调查成本', '净优势'],
        rows: [[baselineValue, informed, gross, cost, net].map(exact)] },
      { title: '信号后的行动及加权贡献', columns: ['信号', '发生概率', '最优可行行动（含并列）', '联合收益'],
        rows: state.information.signals.map(z => { const row = signals[z.id];
          return [z.label, row.probability, row.actions.map(id => options.find(option => option.id === id).label).join('、') || '不发生', row.joint_value]; }) },
    ],
    charts: [{ title: '调查净优势与无差异边界', unit,
      rows: [{ label: '调查净优势', lower: exact(net), upper: exact(net) }, { label: '无差异', lower: '0', upper: '0' }] }],
  };
  return result;
}

export function informationValue(state, options = {}) {
  let prepared;
  return runScoring(model, state, options,
    (state, feasible) => { prepared = prepare(state, feasible); return prepared.errors; },
    (state, feasible) => evaluate(state, feasible, prepared));
}
