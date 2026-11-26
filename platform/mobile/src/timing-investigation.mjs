import { cmp, decimal, exact, maxValue, minus, plus, times } from './core.mjs';
import { bounds, divide, documented, known, min, neg, ONE, own, runScoring, sum, ZERO } from './scoring-shared.mjs';
import { availability, immediateAvailability, timingErrors, timingPayoff, timingUtilities, timeInputs, timingTables } from './timing.mjs';

const modelId = 'timing_investigation';
const probabilityKinds = ['fact', 'estimate', 'synthetic'];
const sourced = value => known(value) && documented(value.source);
function point(value) {
  const range = bounds(value);
  return sourced(value) && range && cmp(...range) === 0 ? range[0] : null;
}
function probability(value) {
  const quantity = point(value);
  return quantity && probabilityKinds.includes(value.kind) && cmp(quantity, ZERO) >= 0 && cmp(quantity, ONE) <= 0 ? quantity : null;
}
const uniqueKeys = (record, keys) => Object.keys(record).length === keys.length && keys.every(key => Object.hasOwn(record, key));
const addsToOne = masses => masses.every(value => value !== null) && cmp(sum(masses), ONE) === 0;
const event = (time, scenario, signal, mass) => ({ time, scenario, signal, mass });
function jointEvents(state, model) {
  if (!model.joint.length || Object.keys(model.completion_by_state).length || model.duration !== null) {
    return { error: '联合模式需要单一的完成时间、情景与信号联合概率表。' };
  }
  const events = model.joint.map(row => event(decimal(row.duration), row.scenario_id, row.signal_id, decimal(row.probability)));
  const keys = events.map(e => `${exact(e.time)}:${e.scenario}:${e.signal}`);
  const scenarios = new Set(state.scenarios.map(row => row.id));
  if (new Set(keys).size !== keys.length || events.some(e => !scenarios.has(e.scenario))) {
    return { error: '联合概率表包含重复事件或未定义的情景。' };
  }
  if (!addsToOne(events.map(e => e.mass))) return { error: '联合概率之和须精确等于 1。' };
  const signals = new Set(state.information?.signals.map(row => row.id));
  if (signals.size && events.some(e => !signals.has(e.signal))) return { error: '联合概率表引用了未定义的信号。' };
  return { events: events.filter(e => e.mass.n) };
}
function factorizedEvents(state, model) {
  const info = state.information;
  if (!info?.signals.length) return { error: '请提供有来源的情景先验和条件信号概率，或填报直接联合概率。' };
  const scenarios = state.scenarios.map(row => row.id), signals = info.signals.map(row => row.id);
  const priors = Object.entries(info.prior).map(([id, value]) => [id, probability(value)]);
  if (!uniqueKeys(info.prior, scenarios) || !addsToOne(priors.map(([, value]) => value))) {
    return { error: '每个情景需要有来源的先验点概率，且总和须等于 1。' };
  }
  const deterministic = model.mode === 'deterministic';
  const time = point(model.duration);
  if (deterministic && (!time || Object.keys(model.completion_by_state).length)) {
    return { error: '确定时长模式需要一个有来源的完成时长点值。' };
  }
  if (!deterministic && (model.duration !== null || Object.keys(model.completion_by_state).some(id => !scenarios.includes(id)))) {
    return { error: '条件模式仅使用所列情景各自的完成时间分布。' };
  }
  if (model.joint.length) return { error: '需选择一个概率结构，保留对应的输入。' };
  const events = [];
  for (const [scenario, prior] of priors) {
    if (!prior.n) continue;
    const conditional = own(info.likelihoods, scenario) ?? {};
    const likelihood = Object.entries(conditional).map(([id, value]) => [id, probability(value)]);
    if (!uniqueKeys(conditional, signals) || !addsToOne(likelihood.map(([, value]) => value))) {
      return { error: `情景「${scenario}」下的信号点概率需有来源，且总和须等于 1。` };
    }
    const distribution = deterministic ? [[time, ONE]] : (own(model.completion_by_state, scenario) ?? [])
      .map(row => [decimal(row.duration), decimal(row.probability)]);
    if (new Set(distribution.map(([duration]) => exact(duration))).size !== distribution.length ||
        !addsToOne(distribution.map(([, mass]) => mass))) {
      return { error: `情景「${scenario}」需要唯一时长、总概率为 1 的条件完成分布。` };
    }
    for (const [duration, durationMass] of distribution) for (const [signal, signalMass] of likelihood) {
      if (durationMass.n && signalMass.n) events.push(event(duration, scenario, signal, times(times(prior, durationMass), signalMass)));
    }
  }
  return { events };
}
function observationScope(state, events) {
  const info = state.information;
  const scope = new Map(), errors = [];
  if (!info) return { scope, errors };
  if (info.unrestricted_actions) {
    if (Object.keys(info.actions_by_signal).length || !documented(info.action_source)) errors.push('调查后行动范围需要单一且有来源的确认。');
    return { scope, errors };
  }
  if (!Object.keys(info.actions_by_signal).length) {
    return { scope, errors: ['需要确认调查后按时仍可执行的动作范围，或提供各信号下的行动限制与来源。'] };
  }
  const options = new Set(state.options.map(x => x.id));
  for (const signal of [...new Set(events.map(e => e.signal))].sort()) {
    const rule = own(info.actions_by_signal, signal);
    if (!sourced(rule) || rule.option_ids.some(id => !options.has(id))) errors.push(`需要有来源的「${signal}」信号后行动范围。`);
    else scope.set(signal, new Set(rule.option_ids));
  }
  return { scope, errors };
}
function addMass(map, key, value) { map.set(key, plus(map.get(key) ?? ZERO, value)); }
function groupEvents(events) {
  const prior = new Map(), durations = new Map(), groups = new Map();
  for (const { time, scenario, signal, mass } of events) {
    const t = exact(time), key = `${t}:${signal}`;
    if (!groups.has(key)) groups.set(key, { time, signal, masses: new Map() });
    addMass(groups.get(key).masses, scenario, mass);
    addMass(prior, scenario, mass);
    addMass(durations, t, mass);
  }
  const observations = [...groups.values()].sort((a, b) => cmp(a.time, b.time) || (a.signal < b.signal ? -1 : a.signal > b.signal ? 1 : 0));
  return { prior, durations, observations };
}
function provenance(state, model, prior) {
  const info = state.information;
  const inputs = [model];
  if (model.mode !== 'joint') {
    inputs.push(...Object.values(info.prior));
    for (const scenario of [...prior.keys()].sort()) inputs.push(...Object.values(info.likelihoods[scenario]));
    if (model.mode === 'deterministic') inputs.push(model.duration);
  }
  const ranks = ['fact', 'estimate', 'assumption', 'synthetic'];
  const unique = new Map(inputs.map(({ kind, source }) => [JSON.stringify([kind, source]), { kind, source }]));
  return { kind: ranks[Math.max(...inputs.map(input => ranks.indexOf(input.kind)))], source: model.source, inputs: [...unique.values()] };
}
const valueOf = (values, key) => values instanceof Map ? values.get(key) : own(values, key);
function bestOptions(values) {
  const best = maxValue([...values.values()]);
  return best === null ? [] : [...values].filter(([, value]) => cmp(value, best) === 0).map(([id]) => id);
}
function branch(state, feasible, time, masses, utilities, allowed) {
  const values = new Map(), gaps = [], statuses = [], eligible = [];
  for (const option of feasible) {
    const status = allowed && !allowed.has(option.id) ? 'SIGNAL_EXCLUDED' : availability(state.timing, option.id, time);
    statuses.push([option.id, status]);
    if (status === 'UNKNOWN') gaps.push(`需要核对「${option.label}」的行动时间规则及期限来源。`);
    if (status !== 'FEASIBLE') continue;
    eligible.push(option.id);
    const payoff = timingPayoff(state, option, time, utilities);
    if ([...masses.keys()].some(id => valueOf(payoff.values, id) === undefined)) gaps.push(...payoff.gaps);
    else values.set(option.id, sum([...masses].map(([id, mass]) => times(mass, valueOf(payoff.values, id)))));
  }
  if (!eligible.length && !gaps.length) gaps.push(`在 ${exact(time)} ${state.timing.time_unit} 没有通过硬约束和期限检查的行动或兜底。`);
  const leaders = gaps.length ? [] : bestOptions(values);
  return { values, gaps, availability: Object.fromEntries(statuses), eligible, leaders, top: values.get(leaders[0]) ?? null };
}

function fixedDurationLines(state, feasible, observations, utilities, scope) {
  const lines = new Map();
  for (const { signal, masses } of observations) {
    const choices = new Map();
    for (const option of feasible) {
      if ((scope.has(signal) && !scope.get(signal).has(option.id)) || immediateAvailability(state.timing, option.id) === 'EXPIRED') continue;
      const action = own(state.timing.actions, option.id);
      const switching = point(action?.switching_cost);
      if (!action || (action.cutoff && !sourced(action.cutoff)) || switching === null) return null;
      let base = ZERO, slope = ZERO;
      for (const [id, mass] of masses) {
        const utility = valueOf(valueOf(utilities, id), option.id), loss = point(own(action.delay_losses, id));
        if (utility === undefined || loss === null) return null;
        base = plus(base, times(mass, minus(utility, switching)));
        slope = plus(slope, times(mass, loss));
      }
      choices.set(option.id, { base, slope });
    }
    lines.set(signal, choices);
  }
  return lines;
}
const affine = ({ base, slope }, time) => minus(base, times(time, slope));
function breakEven(timing, lines, baseline, cost) {
  const horizon = decimal(timing.horizon.at);
  const split = new Map([['0', ZERO], [exact(horizon), horizon]]);
  for (const cutoff of [timing.decision_deadline, ...Object.values(timing.actions).map(rule => rule.cutoff)]) {
    if (!sourced(cutoff)) continue;
    const at = decimal(cutoff.at);
    if (cmp(at, horizon) < 0) split.set(exact(at), at);
  }
  for (const choices of lines.values()) {
    const alternatives = [...choices.values()];
    for (const [index, a] of alternatives.entries()) for (const b of alternatives.slice(index + 1)) {
      const slope = minus(a.slope, b.slope);
      if (!slope.n) continue;
      const crossing = divide(minus(a.base, b.base), slope);
      if (cmp(crossing, ZERO) > 0 && cmp(crossing, horizon) < 0) split.set(exact(crossing), crossing);
    }
  }
  function envelope(time) {
    const selected = [];
    for (const choices of lines.values()) {
      let best = null;
      for (const [id, line] of choices) if (availability(timing, id, time) === 'FEASIBLE' &&
          (best === null || cmp(affine(line, time), affine(best, time)) > 0)) best = line;
      if (!best) return null;
      selected.push(best);
    }
    return { base: minus(minus(sum(selected.map(line => line.base)), cost), baseline), slope: sum(selected.map(line => line.slope)) };
  }
  function profitable(time) {
    const line = envelope(time);
    return line !== null && cmp(affine(line, time), ZERO) > 0;
  }
  const boundaries = [...split.values()].sort(cmp), positive = boundaries.filter(profitable);
  for (const [index, right] of boundaries.slice(1).entries()) {
    const left = boundaries[index];
    const midpoint = divide(plus(left, right), plus(ONE, ONE));
    const line = envelope(midpoint);
    if (line && cmp(affine(line, left), ZERO) > 0) positive.push(line.slope.n ? min(right, divide(line.base, line.slope)) : right);
  }
  const latest = maxValue(positive);
  return latest === null ? null : { at: exact(latest), profitable_at_boundary: profitable(latest), unit: timing.time_unit };
}
function lateMassRange(state, feasible, observations, durations, gross, utilities, cost) {
  if (durations.size !== 2) return null;
  const [early, late] = [...durations.keys()].sort((a, b) => cmp(decimal(a), decimal(b)));
  const conditional = [early, late].map(time => {
    const priors = new Map();
    for (const entry of observations.filter(row => exact(row.time) === time)) {
      for (const [id, value] of entry.masses) addMass(priors, id, divide(value, durations.get(time)));
    }
    return branch(state, feasible, ZERO, priors, utilities, undefined);
  });
  if (conditional.some(row => row.gaps.length)) return null;
  const [earlyValue, lateValue] = [early, late].map(time => minus(divide(gross.get(time), durations.get(time)), cost));
  let lower = ZERO, upper = ONE, lowerInclusive = true, upperInclusive = true, possible = true;
  for (const [id, first] of conditional[0].values) {
    const offset = minus(earlyValue, first), slope = minus(minus(lateValue, conditional[1].values.get(id)), offset);
    if (!slope.n) { possible &&= cmp(offset, ZERO) > 0; continue; }
    const root = divide(neg(offset), slope);
    if (slope.n > 0n && cmp(root, lower) >= 0) { lower = root; lowerInclusive = false; }
    else if (slope.n < 0n && cmp(root, upper) <= 0) { upper = root; upperInclusive = false; }
  }
  const range = possible && (cmp(lower, upper) < 0 || (cmp(lower, upper) === 0 && lowerInclusive && upperInclusive)) ? {
    lower: exact(lower), upper: exact(upper), lower_inclusive: lowerInclusive, upper_inclusive: upperInclusive,
  } : null;
  return { early_duration: early, late_duration: late, profitable_range: range };
}

function validate(state, feasible) {
  const errors = timingErrors(state, feasible);
  if (errors.length) return { errors };
  const model = state.timing.investigation;
  if (!model) return { errors: ['尚未指定调查及信息到达方式。可改用无概率的行动时机比较。'] };
  if (!probabilityKinds.includes(model.kind) || !documented(model.source)) return { errors: ['需要完成与信号概率的证据，或注明合成数据来源。'] };
  const cost = point(model.cost);
  if (!cost) return { errors: ['需要有来源、与效用同单位的调查固定成本。'] };
  const data = model.mode === 'joint' ? jointEvents(state, model) : factorizedEvents(state, model);
  if (data.error) return { errors: [data.error] };
  const scope = observationScope(state, data.events);
  return { ...scope, ...groupEvents(data.events), model, cost };
}

const nullable = value => value === null ? null : exact(value);
function evaluate(state, feasible, { model, cost, scope, observations, prior, durations }) {
  const { utilities, unit, gaps } = timingUtilities(state, feasible, new Set(prior.keys()));
  const immediate = branch(state, feasible, ZERO, prior, utilities, undefined);
  const labels = new Map(feasible.map(option => [option.id, option.label]));
  const signals = new Map((state.information?.signals ?? []).map(signal => [signal.id, signal.label]));
  const labelsFor = ids => ids.map(id => labels.get(id)).join('、') || null;
  const inputProvenance = provenance(state, model, prior);
  const grossByTime = new Map(), branchGaps = [];
  const policy = observations.map(({ time, signal, masses }) => {
    const outcome = branch(state, feasible, time, masses, utilities, scope.get(signal));
    const duration = exact(time);
    if (outcome.top !== null) addMass(grossByTime, duration, outcome.top);
    branchGaps.push(...outcome.gaps);
    return { duration, signal_id: signal, probability: exact(sum([...masses.values()])), eligible_option_ids: outcome.eligible,
      option_ids: outcome.leaders, availability: outcome.availability,
      fallback_selected: outcome.leaders.includes(state.timing.fallback_option_id), expected_contribution: nullable(outcome.top) };
  });
  const informed = branchGaps.length ? null : minus(sum([...grossByTime.values()]), cost);
  const net = informed !== null && immediate.top !== null ? minus(informed, immediate.top) : null;
  const status = net === null ? 'UNKNOWN' : net.n > 0n ? 'INVESTIGATE' : net.n < 0n ? 'ACT_NOW' : 'TIE';
  const allGaps = [...immediate.gaps, ...gaps, ...branchGaps];
  let threshold = null, lateMass = null;
  if (model.mode === 'deterministic' && immediate.top !== null) {
    const lines = fixedDurationLines(state, feasible, observations, utilities, scope);
    if (lines) threshold = breakEven(state.timing, lines, immediate.top, cost);
    else allGaps.push('需要各相关情景的完整损失率与时间规则才能复算确定时长的优势边界。');
  } else if (net !== null) lateMass = lateMassRange(state, feasible, observations, durations, grossByTime, utilities, cost);
  const probabilityBasis = { joint: '直接使用完成时间、情景和信号的联合概率。',
    conditional: '按有来源的条件独立假设，在给定情景后分解完成时间和信号。',
    deterministic: '完成时间固定，使用有来源的情景概率和情景内信号概率。' }[model.mode];
  let summary = `按事前风险中性期望效用比较。调查完成后观察到达时刻和信号，再从仍可执行的行动中选择。${probabilityBasis}`;
  if (inputProvenance.kind === 'synthetic') summary += '概率或时长包含合成输入，数值用于复算示例。';
  else if (['estimate', 'assumption'].includes(inputProvenance.kind)) summary += '概率或时长使用了所列估计或假设。';
  summary += net === null ? '缺少可行的结束行动或收益依据，净价值为 UNKNOWN。' : `相对立即行动的调查净增益为 ${exact(net)} ${unit}。`;
  if (threshold) summary += `在所列确定时长模型内，调查严格占优要求完成时间 ${threshold.profitable_at_boundary ? '≤' : '<'} ${threshold.at} ${threshold.unit}。`;
  if (lateMass) {
    const range = lateMass.profitable_range;
    summary += '晚到概率的敏感性比较保持各时点内的情景与信号分布，并重新计算立即行动基线。';
    if (range) summary += `调查严格占优的晚到概率范围为 ${range.lower_inclusive ? '[' : '('}${range.lower}，${range.upper}${range.upper_inclusive ? ']' : ')'}。`;
    else summary += '这一混合下没有使调查严格占优的晚到概率。';
  }
  const times = timeInputs(state, feasible);
  return { summary, status, probabilities_used: true, probability_basis: model.mode, probability_provenance: inputProvenance,
    immediate_value: nullable(immediate.top), investigation_value: nullable(informed), net_value: nullable(net),
    immediate_leaders: immediate.leaders, immediate_availability: immediate.availability, leaders: status === 'ACT_NOW' ? immediate.leaders : [],
    policy, threshold, time_inputs: times, gaps: [...new Set(allGaps)], late_mass_sensitivity: lateMass,
    duration_probabilities: Object.fromEntries([...durations].map(([time, value]) => [time, exact(value)])),
    scenario_probabilities: Object.fromEntries([...prior].map(([id, value]) => [id, exact(value)])),
    tables: [
      ...timingTables(state, feasible, times),
      { title: `立即行动与调查（${unit ?? '单位待核对'}）`, columns: ['立即可行方案', '立即行动优选', '立即行动效用', '调查成本', '调查净效用', '相对净增益'],
        rows: [[labelsFor(immediate.eligible), labelsFor(immediate.leaders), nullable(immediate.top), exact(cost), nullable(informed), nullable(net)]] },
      { title: '观察完成时刻及信号后选择', columns: [`时刻（${state.timing.time_unit}）`, '信号', '联合概率', '仍可行动作', '最优动作（含并列）', '入选的指定兜底', '效用贡献'],
        rows: policy.map(row => [row.duration, signals.get(row.signal_id) ?? row.signal_id, row.probability, labelsFor(row.eligible_option_ids),
          labelsFor(row.option_ids), row.fallback_selected ? labels.get(state.timing.fallback_option_id) : null, row.expected_contribution]) },
      { title: '调查输入的概率依据', columns: ['计算口径', '证据类型', '来源'], rows: inputProvenance.inputs.map(row => [probabilityBasis, row.kind, row.source]) },
    ],
    charts: informed === null || immediate.top === null ? [] : [{ title: '立即行动与调查的期望效用比较', unit,
      rows: [['立即行动', immediate.top], ['先调查', informed]].map(([label, value]) => ({ label, lower: exact(value), upper: exact(value) })) }],
  };
}

export function timingInvestigation(state, options = {}) {
  let prepared;
  return runScoring(modelId, state, options,
    (state, feasible) => { prepared = validate(state, feasible); return prepared.errors; },
    (state, feasible) => evaluate(state, feasible, prepared));
}
