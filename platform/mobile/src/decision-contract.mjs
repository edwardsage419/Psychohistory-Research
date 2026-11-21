import { casefoldOverrides, stateSchema } from './platform-contract.generated.mjs';
import { cmp, decimal, rat, stripText } from './core.mjs';

const decimalPattern = /^([+-]?)(?:(\d+)(?:\.(\d*))?|\.(\d+))(?:[Ee]([+-]?\d+))?$/;
const own = Object.hasOwn;
const object = value => value !== null && typeof value === 'object' &&
  [null, Object.prototype].includes(Object.getPrototypeOf(value));

function invalid(path) {
  throw new Error(`输入不符合 v0.5 契约（${path}）。`);
}

function normalizeDecimal(value, rule, path) {
  if (typeof value === 'number' && Number.isFinite(value)) value = String(value);
  if (typeof value !== 'string' || value.length > 40) invalid(path);
  const parts = decimalPattern.exec(stripText(value).replaceAll('_', ''));
  if (!parts) invalid(path);
  const [, sign, integers = '', decimals, fraction, exponent = '0'] = parts;
  const after = decimals ?? fraction ?? '';
  const coefficient = (integers + after).replace(/^0+(?=\d)/, '');
  const shift = Number(exponent) - after.length;
  if (!Number.isSafeInteger(shift) || Math.abs(shift) > 10000) invalid(path);
  if (coefficient !== '0') {
    const whole = coefficient.length + shift;
    const trailing = coefficient.length - coefficient.replace(/0+$/, '').length;
    if (whole > 6 || -shift - trailing > 12) invalid(path);
  }
  const signed = sign === '-' ? '-' : '';
  const adjusted = coefficient.length + shift - 1;
  let normalized;
  if (shift > 0 || adjusted < -6) {
    const mantissa = coefficient.length === 1 ? coefficient : `${coefficient[0]}.${coefficient.slice(1)}`;
    normalized = `${signed}${mantissa}E${adjusted >= 0 ? '+' : ''}${adjusted}`;
  } else if (shift === 0) {
    normalized = signed + coefficient;
  } else {
    const point = coefficient.length + shift;
    normalized = point > 0 ? `${signed}${coefficient.slice(0, point)}.${coefficient.slice(point)}` :
      `${signed}0.${'0'.repeat(-point)}${coefficient}`;
  }
  const exact = coefficient === '0' ? rat(0) : decimal(normalized);
  if ((rule.ge != null && cmp(exact, decimal(rule.ge)) < 0) ||
      (rule.le != null && cmp(exact, decimal(rule.le)) > 0)) invalid(path);
  return normalized;
}

function read(rule, value, path) {
  if (rule.$ref) return read(stateSchema.$defs[rule.$ref.split('/').at(-1)], value, path);
  if (rule.anyOf) {
    const nonNull = rule.anyOf.filter(candidate => candidate.type !== 'null');
    if (nonNull.length === 1 && rule.anyOf.length === 2) {
      return value === null ? null : read(nonNull[0], value, path);
    }
    for (const candidate of rule.anyOf) {
      try { return read(candidate, value, path); } catch { /* try the next declared type */ }
    }
    return invalid(path);
  }
  if ((own(rule, 'const') && rule.const !== value) || (rule.enum && !rule.enum.includes(value))) invalid(path);
  switch (rule.type) {
    case 'decimal': return normalizeDecimal(value, rule, path);
    case 'null': if (value === null) return value; break;
    case 'boolean': if (typeof value === 'boolean') return value; break;
    case 'integer':
      if (Number.isSafeInteger(value) && !(value < rule.minimum || value > rule.maximum)) return value;
      break;
    case 'string': {
      if (typeof value !== 'string') break;
      const characters = [...value];
      const length = characters.length;
      if (length < rule.minLength || length > rule.maxLength || (rule.minLength && !stripText(value)) ||
          characters.some(char => char.length === 1 && /[\uD800-\uDFFF]/.test(char)) ||
          (rule.pattern && new RegExp(rule.pattern).exec(value)?.[0] !== value)) break;
      return value;
    }
    case 'array':
      if (Array.isArray(value) && !(value.length < rule.minItems || value.length > rule.maxItems)) {
        return value.map((item, i) => read(rule.items, item, `${path}[${i}]`));
      }
      break;
    case 'object': {
      if (!object(value)) break;
      const keys = Object.keys(value);
      if (keys.length > rule.maxProperties) break;
      if (rule.properties) {
        if (keys.some(key => !own(rule.properties, key))) invalid(`${path} 包含未知字段`);
        const result = Object.fromEntries(Object.entries(rule.properties).map(([key, field]) => {
          if (own(value, key)) return [key, read(field, value[key], `${path}.${key}`)];
          if (rule.required?.includes(key)) invalid(`${path}.${key}`);
          const fallback = own(field, 'default') ? field.default : field.type === 'array' ? [] : {};
          return [key, read(field, fallback, `${path}.${key}`)];
        }));
        if (own(rule.properties, 'lower') && own(rule.properties, 'upper')) verifyBounds(result);
        return result;
      }
      const [[pattern, field]] = Object.entries(rule.patternProperties ?? {});
      const matcher = new RegExp(pattern);
      if (keys.some(key => matcher.exec(key)?.[0] !== key)) invalid(`${path} 标识`);
      return Object.fromEntries(keys.map(key => [key, read(field, value[key], `${path}.*`)]));
    }
  }
  return invalid(path);
}

function verifyBounds({ lower, upper, kind }) {
  if (kind === 'unknown' && (lower != null || upper != null)) throw new Error('未知数值应留空。');
  if (lower != null && upper != null && cmp(decimal(lower), decimal(upper)) > 0) throw new Error('区间下界不能大于上界。');
}

function unique(ids) {
  const set = new Set(ids);
  if (set.size !== ids.length) throw new Error('同类字段的标识必须唯一。');
  return set;
}

function includes(set, keys) { return keys.every(key => set.has(key)); }

export function normalizeDecision(input) {
  const state = read(stateSchema, input, 'state');
  const objectives = unique(state.objectives.map(x => x.id));
  const options = unique(state.options.map(x => x.id));
  const constraints = unique(state.constraints.map(x => x.id));
  unique(state.scenarios.map(x => x.id));
  unique(state.evidence.map(x => x.id));
  if (!includes(objectives, [...Object.keys(state.weights), ...Object.keys(state.shared_offsets)])) {
    throw new Error('权重或误差引用了不存在的目标。');
  }
  for (const option of state.options) {
    if (!includes(constraints, Object.keys(option.measurements)) || !includes(objectives, Object.keys(option.scores))) {
      throw new Error('方案引用了不存在的硬约束或目标。');
    }
  }
  if (state.scenarios.some(x => !includes(options, Object.keys(x.utilities)))) throw new Error('情景引用了不存在的方案。');
  if (state.reference_option_id !== null && !options.has(state.reference_option_id)) throw new Error('基准方案不存在。');
  if (state.intended_option_id !== null && !options.has(state.intended_option_id)) throw new Error('计划方案不存在。');
  if (state.preferences) unique(state.preferences.values.map(({ label }) =>
    Array.from(stripText(label), char => casefoldOverrides[char] ?? char.toLowerCase()).join('')));
  if (state.information) {
    unique(state.information.signals.map(x => x.id));
    for (const row of Object.values(state.information.actions_by_signal)) unique(row.option_ids);
  }
  return state;
}

export function canonicalDecision(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalDecision).join(',')}]`;
  if (object(value)) {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalDecision(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}
