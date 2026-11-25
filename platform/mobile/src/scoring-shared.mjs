import { cmp, decimal, minus, plus, rat, stripText } from './core.mjs';

export const ZERO = rat(0);
export const ONE = rat(1);
export const min = (a, b) => cmp(a, b) <= 0 ? a : b;
export const max = (a, b) => cmp(a, b) >= 0 ? a : b;
export const sum = values => values.reduce(plus, ZERO);
export const neg = value => minus(ZERO, value);
export const divide = (a, b) => rat(a.n * b.d, a.d * b.n);
export const midpoint = (a, b) => divide(plus(a, b), rat(2));
export const documented = value => Boolean(stripText(value));
export const known = value => ['fact', 'estimate', 'assumption', 'synthetic'].includes(value?.kind);
export const own = (object, key) => object != null && Object.hasOwn(object, key) ? object[key] : undefined;
export function horizon(value, deadline) {
  const effective = value?.horizon || deadline;
  return effective == null ? null : stripText(effective);
}

export function bounds(value) {
  if (value?.lower == null || value?.upper == null) return null;
  try {
    const lower = decimal(value.lower);
    const upper = decimal(value.upper);
    return cmp(lower, upper) <= 0 ? [lower, upper] : null;
  } catch {
    return null;
  }
}

export function uniqueIds(collection) {
  return Array.isArray(collection)
    && collection.every(item => /^[a-zA-Z0-9_-]{1,48}$/.test(item?.id ?? '') && typeof item.id === 'string')
    && new Set(collection.map(item => item.id)).size === collection.length;
}

export function* pairs(items) {
  for (let i = 0; i < items.length; i++) {
    for (const other of items.slice(i + 1)) yield [items[i], other];
  }
}

export function receipt(model_id, status, reasons, result = null) {
  return { model_id, version: '1.0.0', status, reasons, result };
}

export function executed(modelId, result) {
  return receipt(modelId, 'EXECUTED', ['本次输入满足方法声明的适用条件。'], result);
}

const OPERATORS = {
  '>=': relation => relation >= 0,
  '>': relation => relation > 0,
  '<=': relation => relation <= 0,
  '<': relation => relation < 0,
};

function constraintCheck(constraint, value, deadline) {
  if (!documented(constraint.source)) return ['UNKNOWN', '请补充硬约束阈值的依据。'];
  if (!known(value) || value.lower == null || value.upper == null) return ['UNKNOWN', '请补充有依据的上下界。'];
  if (!documented(value.source)) return ['UNKNOWN', '请补充区间来源。'];
  if (!documented(value.unit) || stripText(value.unit) !== stripText(constraint.unit)) return ['UNKNOWN', '区间单位与硬约束单位冲突。'];
  if ((value.horizon || deadline) !== (constraint.horizon || deadline)) return ['UNKNOWN', '区间与硬约束的时间范围冲突。'];
  const range = bounds(value);
  if (!range) return ['UNKNOWN', '区间须有有限且有序的上下界。'];
  const [lower, upper] = range;
  const threshold = decimal(constraint.threshold);
  const meets = OPERATORS[constraint.operator];
  const isLower = constraint.operator.startsWith('>');
  const worst = isLower ? lower : upper;
  const best = isLower ? upper : lower;
  if (meets(cmp(worst, threshold))) return ['CERTAIN_PASS', '整个闭区间满足阈值。'];
  if (!meets(cmp(best, threshold))) return ['CERTAIN_FAIL', '整个闭区间违反阈值。'];
  return ['POSSIBLE', '区间同时包含满足与违反阈值的值。'];
}

function evaluateOption(option, constraints, deadline) {
  const intersection = new Map();
  const rows = constraints.map(constraint => {
    const key = JSON.stringify([stripText(constraint.label), stripText(constraint.unit), constraint.horizon || deadline || null]);
    const value = own(option.measurements, constraint.id);
    const [status, reason] = constraintCheck(constraint, value, deadline);
    if (status !== 'UNKNOWN') {
      const interval = bounds(value);
      const previous = intersection.get(key);
      intersection.set(key, previous ? [max(previous[0], interval[0]), min(previous[1], interval[1])] : interval);
    }
    return { key, check: { constraint_id: constraint.id, status, reason } };
  });
  const checks = rows.map(({ key, check }) => {
    const interval = intersection.get(key);
    if (interval && cmp(...interval) > 0) {
      return { ...check, status: 'UNKNOWN', reason: '同指标、同单位及时间范围的区间互相冲突。' };
    }
    return check;
  });
  let status = 'UNRESOLVED';
  if (checks.some(check => check.status === 'CERTAIN_FAIL')) status = 'REJECT';
  else if (checks.every(check => check.status === 'CERTAIN_PASS')) status = 'ACCEPT';
  return { option_id: option.id, label: option.label, status, checks };
}

const GATE_ID = 'c028_interval_feasibility';
export function feasibility(state) {
  if (state?.constraints_confirmed !== true) return receipt(GATE_ID, 'INELIGIBLE', ['请确认硬约束。']);
  const constraints = state.constraints ?? [];
  const options = state.options ?? [];
  if (!uniqueIds(constraints) || !uniqueIds(options)) return receipt(GATE_ID, 'INELIGIBLE', ['硬约束和方案的标识必须有效且唯一。']);
  if (constraints.some(item => !documented(item.label) || !documented(item.unit)
    || !Object.hasOwn(OPERATORS, item.operator) || !bounds({ lower: item.threshold, upper: item.threshold }))
    || options.some(item => !documented(item.label))) {
    return receipt(GATE_ID, 'INELIGIBLE', ['需要有效的方案名称、硬约束单位和单调阈值。']);
  }
  const feasibility = options.map(option => evaluateOption(option, constraints, state.deadline));
  return executed(GATE_ID, {
    summary: '依据用户确认的底线逐项筛查。只对 ACCEPT 方案执行后续比较。',
    tables: [{ title: '硬约束筛查', columns: ['方案', '判定'], rows: feasibility.map(item => [item.label, item.status]) }],
    charts: [],
    feasibility,
  });
}

export function runScoring(modelId, state, options, validate, run) {
  try {
    const gate = feasibility(state);
    if (gate.status !== 'EXECUTED') return receipt(modelId, 'INELIGIBLE', gate.reasons);

    let accepted = new Set(gate.result.feasibility.filter(row => row.status === 'ACCEPT').map(row => row.option_id));
    if (options.feasible !== undefined) {
      if (!uniqueIds(options.feasible) || options.feasible.some(option => !accepted.has(option.id))) {
        return receipt(modelId, 'INELIGIBLE', ['参与比较的方案必须通过硬约束筛查。']);
      }
      accepted = new Set(options.feasible.map(option => option.id));
    }
    const feasible = (state.options ?? []).filter(option => accepted.has(option.id));
    const reasons = validate(state, feasible);
    return reasons.length ? receipt(modelId, 'INELIGIBLE', reasons) : executed(modelId, run(state, feasible));
  } catch {
    return receipt(modelId, 'FAILED', ['方法执行或输出校验失败。此方法的结果已隔离。']);
  }
}
