/**
 * Mobile proof-of-concept deterministic core, independently implemented in JS.
 * Stage 0 only: finite decisions, point utilities, hard constraints and EVSI.
 * No claim of full parity with Platform v0.5 and no empirical predictions.
 */
export const ENGINE_VERSION = '0.1.0-dev';
const DECIMAL = /^([+-]?)(\d*)(?:\.(\d{1,12}))?$/;
function abs(n) { return n < 0n ? -n : n; }
function gcd(a, b) { a = abs(a); b = abs(b); while (b) [a, b] = [b, a % b]; return a || 1n; }
export function rat(n, d = 1n) {
  if (d === 0n) throw new Error('除数不能为零');
  n = BigInt(n); d = BigInt(d);
  if (d < 0n) { n = -n; d = -d; }
  const g = gcd(n, d); return { n: n / g, d: d / g };
}
export function decimal(value) {
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw new Error('仅支持有限数值');
    value = String(value);
  }
  if (typeof value !== 'string') throw new Error('数值需要十进制文字');
  const m = DECIMAL.exec(value.trim());
  if (!m || (!m[2] && !m[3]) || value.length > 42) throw new Error(`无效十进制数值：${String(value).slice(0, 35)}`);
  const digits = m[3] || '';
  const scale = 10n ** BigInt(digits.length);
  const numerator = BigInt((m[2] || '0') + digits) * (m[1] === '-' ? -1n : 1n);
  return rat(numerator, scale);
}
export function plus(a, b) { return rat(a.n * b.d + b.n * a.d, a.d * b.d); }
export function minus(a, b) { return rat(a.n * b.d - b.n * a.d, a.d * b.d); }
export function times(a, b) { return rat(a.n * b.n, a.d * b.d); }
export function cmp(a, b) { const x = a.n * b.d - b.n * a.d; return x > 0n ? 1 : x < 0n ? -1 : 0; }
export function exact(a) {
  if (a.d === 1n) return String(a.n);
  let t = a.d;
  while (t % 2n === 0n) t /= 2n;
  while (t % 5n === 0n) t /= 5n;
  if (t !== 1n) return `${a.n}/${a.d}`;
  // Simpler exact decimal conversion by long division using BigInt.
  let neg = a.n < 0n; let num = abs(a.n);
  let integer = String(num / a.d), remainder = num % a.d, fractions = '';
  while (remainder !== 0n && fractions.length < 80) {
    remainder *= 10n; fractions += String(remainder / a.d); remainder %= a.d;
  }
  return (neg ? '-' : '') + integer + (fractions ? '.' + fractions : '');
}
export function maxValue(values) { return values.reduce((best, x) => best === null || cmp(x, best) > 0 ? x : best, null); }
function point(q, label, unit) {
  if (!q || !['fact', 'estimate', 'assumption', 'synthetic'].includes(q.kind) || !q.source?.trim() || q.lower == null || q.upper == null) throw new Error(`${label}：缺少有来源的点值`);
  if (q.unit !== unit) throw new Error(`${label}：单位不一致`);
  const lo = decimal(q.lower), hi = decimal(q.upper);
  if (cmp(lo, hi) !== 0) throw new Error(`${label}：当前工程样机仅支持点效用`);
  return lo;
}
function checkOne(option, constraint) {
  const q = option.measurements?.[constraint.id];
  if (!q || !['fact', 'estimate', 'assumption', 'synthetic'].includes(q.kind) || !q.source?.trim() || q.lower == null || q.upper == null) return 'UNRESOLVED';
  if (q.unit !== constraint.unit) throw new Error(`约束「${constraint.id}」与「${option.id}」单位冲突`);
  const lower = decimal(q.lower), upper = decimal(q.upper), limit = decimal(constraint.threshold);
  if (cmp(lower, upper) > 0) throw new Error('无效区间');
  const l = cmp(lower, limit), u = cmp(upper, limit);
  const op = constraint.operator;
  if (op === '>=') return l >= 0 ? 'ACCEPT' : u < 0 ? 'REJECT' : 'UNRESOLVED';
  if (op === '>') return l > 0 ? 'ACCEPT' : u <= 0 ? 'REJECT' : 'UNRESOLVED';
  if (op === '<=') return u <= 0 ? 'ACCEPT' : l > 0 ? 'REJECT' : 'UNRESOLVED';
  if (op === '<') return u < 0 ? 'ACCEPT' : l >= 0 ? 'REJECT' : 'UNRESOLVED';
  throw new Error('未知的硬约束操作符');
}
export function feasibility(state) {
  if (!Array.isArray(state.options) || state.options.length === 0) throw new Error('需要候选方案');
  const ids = state.options.map(o => o.id);
  if (ids.some(x => !x || typeof x !== 'string') || new Set(ids).size !== ids.length) throw new Error('方案标识必须唯一');
  const constraints = state.constraints || [];
  return state.options.map(option => {
    const checks = constraints.map(c => ({ constraint_id: c.id, status: checkOne(option, c) }));
    const status = checks.some(c => c.status === 'REJECT') ? 'REJECT' : checks.some(c => c.status === 'UNRESOLVED') ? 'UNRESOLVED' : 'ACCEPT';
    return { option_id: option.id, label: option.label, status, checks };
  });
}
function payoffMatrix(state, accepted) {
  if (!Array.isArray(state.scenarios) || !state.scenarios.length) throw new Error('需要情景');
  const unit = state.utility_unit;
  if (typeof unit !== 'string' || !unit.trim()) throw new Error('需要共同效用单位');
  const matrix = {};
  for (const scenario of state.scenarios) {
    if (!scenario.id || Object.hasOwn(matrix, scenario.id)) throw new Error('情景标识必须唯一');
    matrix[scenario.id] = {};
    for (const option of accepted) matrix[scenario.id][option.id] = point(scenario.utilities?.[option.id], `情景 ${scenario.id} / 方案 ${option.id}`, unit);
  }
  return matrix;
}
export function minimaxRegret(state) {
  const checks = feasibility(state);
  const selected = state.options.filter(o => checks.find(c => c.option_id === o.id).status === 'ACCEPT');
  if (!selected.length) return { status: 'UNKNOWN', reason: '没有已确认可行的方案', checks };
  try {
    const mat = payoffMatrix(state, selected), worst = {};
    for (const o of selected) worst[o.id] = rat(0);
    for (const row of Object.values(mat)) {
      const leader = maxValue(Object.values(row));
      for (const o of selected) {
        const r = minus(leader, row[o.id]);
        if (cmp(r, worst[o.id]) > 0) worst[o.id] = r;
      }
    }
    const optimum = Object.values(worst).reduce((best, r) => cmp(r, best) < 0 ? r : best);
    const leaders = selected.filter(o => cmp(worst[o.id], optimum) === 0).map(o => o.id);
    return { status: 'CONDITIONAL', leaders, worst_regret: Object.fromEntries(Object.entries(worst).map(([key, value]) => [key, exact(value)])), checks, method: 'scenario_minimax_regret', unit: state.utility_unit };
  } catch (e) { return { status: 'UNKNOWN', reason: e.message, checks }; }
}
function prob(q, label) {
  if (!q || !['fact', 'estimate', 'assumption', 'synthetic'].includes(q.kind) || !q.source?.trim()) throw new Error(`${label} 缺少来源`);
  const p = point({ ...q, unit: 'probability' }, label, 'probability');
  if (cmp(p, rat(0)) < 0 || cmp(p, rat(1)) > 0) throw new Error(`${label} 超出 [0,1]`);
  return p;
}
function sum(values) { return values.reduce(plus, rat(0)); }
/** Finite point value of sample information. No inferred real-world probabilities. */
export function informationValue(state) {
  const checks = feasibility(state), info = state.information;
  if (!info) return { status: 'INELIGIBLE', reason: '未提供有来源的调查模型' };
  const accepted = state.options.filter(o => checks.find(c => c.option_id === o.id).status === 'ACCEPT');
  if (!accepted.length) return { status: 'UNKNOWN', reason: '无确认可行行动' };
  try {
    const mat = payoffMatrix(state, accepted);
    const states = state.scenarios.map(x => x.id), signals = info.signals?.map(x => x.id) || [];
    if (!signals.length || new Set(signals).size !== signals.length) throw new Error('必须确认不重复的信号');
    const priors = Object.fromEntries(states.map(s => [s, prob(info.prior?.[s], `先验 ${s}`)]));
    if (cmp(sum(Object.values(priors)), rat(1)) !== 0) throw new Error('先验概率之和必须严格等于 1');
    const likelihoods = {};
    const sources = [];
    for (const s of states) {
      likelihoods[s] = {};
      sources.push(info.prior[s].kind);
      for (const z of signals) {
        likelihoods[s][z] = prob(info.likelihoods?.[s]?.[z], `条件概率 ${s}/${z}`);
        sources.push(info.likelihoods[s][z].kind);
      }
      if (cmp(sum(Object.values(likelihoods[s])), rat(1)) !== 0) throw new Error(`条件信号概率之和必须严格等于 1：${s}`);
    }
    const cost = point(info.cost, '调查成本', state.utility_unit);
    if (cmp(cost, rat(0)) < 0) throw new Error('调查成本必须非负');
    sources.push(info.cost.kind);
    for (const s of state.scenarios) for (const o of accepted) sources.push(s.utilities[o.id].kind);
    const baselineByOption = {};
    for (const o of accepted) baselineByOption[o.id] = sum(states.map(s => times(priors[s], mat[s][o.id])));
    const baseline = maxValue(Object.values(baselineByOption));
    let informed = rat(0);
    const policies = [];
    for (const z of signals) {
      const mass = sum(states.map(s => times(priors[s], likelihoods[s][z])));
      if (cmp(mass, rat(0)) === 0) continue;
      const eligible = accepted.filter(o => !info.actions_by_signal || info.actions_by_signal[z]?.includes(o.id));
      if (!eligible.length) throw new Error(`正概率信号「${z}」没有确认可行行动，无法计算`);
      const each = eligible.map(o => ({ id: o.id, expected: sum(states.map(s => times(times(priors[s], likelihoods[s][z]), mat[s][o.id]))) }));
      const top = maxValue(each.map(x => x.expected));
      informed = plus(informed, top);
      policies.push({ signal_id: z, signal_mass: exact(mass), best_options: each.filter(x => cmp(x.expected, top) === 0).map(x => x.id) });
    }
    const gross = minus(informed, baseline), net = minus(gross, cost);
    const evidence_status = sources.includes('synthetic') ? 'SYNTHETIC' : 'CONDITIONAL';
    return {
      status: cmp(net, rat(0)) > 0 ? 'INVESTIGATE' : cmp(net, rat(0)) < 0 ? 'ACT_NOW' : 'TIE',
      baseline: exact(baseline), with_information: exact(informed), gross_information_value: exact(gross), net_value: exact(net),
      evidence_status, policy: policies, unit: state.utility_unit,
      summary: evidence_status === 'SYNTHETIC' ? '合成情景，仅作模型算例。' : '用户输入的条件性情景，系统未独立验证来源。'
    };
  } catch (e) { return { status: 'UNKNOWN', reason: e.message }; }
}
export function analyze(state) {
  const regret = minimaxRegret(state), voi = informationValue(state);
  return { engine_version: ENGINE_VERSION, scientific_effectiveness: 'UNVERIFIED', regret, information: voi, executed_real_world_action: false };
}
