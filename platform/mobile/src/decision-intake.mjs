import { stripText } from './core.mjs';
import { decisionWorkflowVersion, normalizeDecision } from './decision-contract.mjs';

const CHOICE_ZH = /(?:我该|应该选择|我应该|我在考虑|我在纠结|我在犹豫)([^，,。；;？?\n]{1,100}?)[，,]?\s*(?:还是|或者)([^。；;？?\n]{1,100})(?:[？?。]|$)/u;
const CHOICE_EN = /\b(?:should i|i am considering)\s+([^,.!?\n]{1,100}?),?\s+or\s+([^,.!?\n]{1,100})(?:[.?]|$)/iu;
const LABEL = /(?:^|[；;。\n])\s*(方案[\p{L}\d\-]{1,12})\s*[：:]/gu;
const DOMAINS = [
  ['moving', /搬(?:去|到)|搬家|迁居|relocat/i],
  ['career', /岗位|跳槽|薪资|月薪|offer|\bjob\b|career/i],
  ['housing', /租房|续租|合住|独住|住房|housing|\brent\b/i],
  ['learning', /课程|报名|学习|培训|进修|course|study/i],
  ['budget', /预算|开支|开销|费用|维修|budget|repair/i],
  ['risk', /风险|取消损失|不确定|\brisk\b/i],
  ['life', /生活|作息|日常|\blife\b/i],
];
const NUMBER = '[0-9０-９.,．，零〇一二两三四五六七八九十百千万]{1,24}';
const HEDGE = /大概|可能|估计|听说|预计|约|还没|不确定|未知|不知|\babout\b|\bmaybe\b/i;
const CONDITION = /如果|假如|只要|除非|否则|前提|即使|要是|^(?:若|如能)|\bif\b/i;
const PRIOR = /以前|原来|过去|先前|原本|^(?:之前|曾经)|\bused to\b/i;
const REVISION = /改(?:为|到|成)|修订为|调整(?:为|到)|更(?:正|改)为/u;
const RANGE = /(?:[\d０-９零一二两三四五六七八九十百千万]\s*[-–—~～至到]\s*[\d０-９零一二两三四五六七八九十百千万])/u;
const NON_CNY = /美元|美金|港元|港币|台币|日元|欧元|英镑|澳元|加元|[€$£]|\b(?:USD|HKD|JPY|EUR|GBP|AUD|CAD)\b/i;
const LIMITS = {
  income_min: { metric: 'income', label: '月收入', unit: 'yuan/month', operator: '>=' },
  hours_max: { metric: 'hours', label: '每周时长', unit: 'hours/week', operator: '<=' },
  onsite_max: { metric: 'onsite', label: '每周到岗天数', unit: 'days/week', operator: '<=' },
  cost_max: { metric: 'cost', label: '费用', unit: 'yuan', operator: '<=' },
  move_allowed: { metric: 'move_required', label: '需要搬家', unit: 'boolean', operator: '<=' },
};
const RULE = (field, unit, pattern) => ({ field, unit, re: new RegExp(pattern, 'u') });
const LIMIT_RULES = [
  RULE('income_min', 'yuan/month', `(?:每月收入|月收入|月薪|收入底线)[^。；，,]{0,10}?(?:至少|不低于|最低|改为|改到|调整为|底线是|底线为)\\s*(${NUMBER})`),
  RULE('onsite_max', 'days/week', `每周[^。；，,]{0,12}?(?:最多到岗|到岗最多|到岗上限(?:为|是)?|最多去).{0,3}?(\\s*${NUMBER})\\s*天`),
  RULE('hours_max', 'hours/week', `每周[^。；，,]{0,14}?(?:最多|不超过|上限(?:为|是)?)[^0-9０-９零一二两三四五六七八九十百千万。；，,]{0,8}(\\s*${NUMBER})\\s*(?:个)?小时`),
  RULE('cost_max', 'yuan', `(?:(?:总?预算)[^。；，,]{0,7}?(?:最多|不超过|上限|大概|估计|约)|最多(?:能动用|能花|花))[^0-9０-９零一二两三四五六七八九十百千万。；，,]{0,5}(\\s*${NUMBER})\\s*元`),
];
const MEASUREMENT_RULES = [
  RULE('income', 'yuan/month', `(?:每月收入|月收入|月薪)(?:是|为)?\\s*(${NUMBER})`),
  RULE('onsite', 'days/week', `每周(?:要|需要)?到岗\\s*(${NUMBER})\\s*天`),
  RULE('hours', 'hours/week', `每周[^0-9０-９零一二两三四五六七八九十百千万。；，,]{0,12}(\\s*${NUMBER})\\s*(?:个)?小时`),
  RULE('cost', 'yuan', `(?:费用|价格|花费|花费是|支出)(?:是|为)?\\s*(${NUMBER})\\s*元`),
];
export const offlineModelStatus = Object.freeze({
  status: 'RETIRED',
  enabled: false,
  model: null,
  bridge: 'UNAVAILABLE',
  message: `本机提供离线确定性引导及 v${decisionWorkflowVersion} 部分计算。v0.7 工作流可在桌面本地工作台运行。Mac 辅助连接未提供。`,
});

function writtenNumber(raw) {
  const spelling = stripText(raw).normalize('NFKC').replace(/,$/, '');
  if (!spelling || (spelling.includes(',') && !/^\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(spelling))) return null;
  const token = spelling.replaceAll(',', '');
  if (/^\d+(?:\.\d+)?$/.test(token)) return token;
  const digit = new Map(Array.from('零一二三四五六七八九', (letter, number) => [letter, number]));
  digit.set('〇', 0);
  digit.set('两', 2);
  if (Array.from(token).every(letter => digit.has(letter))) {
    return String(Number(Array.from(token, letter => digit.get(letter)).join('')));
  }
  if (!/^[零〇一二两三四五六七八九十百千万]+$/u.test(token)) return null;
  let total = 0, group = 0, pending = null, previousUnit = 10000;
  for (const letter of token) {
    if (digit.has(letter)) {
      pending = digit.get(letter);
      continue;
    }
    const unit = { 十: 10, 百: 100, 千: 1000, 万: 10000 }[letter];
    if (unit === 10000) {
      if (total) return null;
      total = (group + (pending ?? 0)) * unit;
      group = 0;
      previousUnit = 10000;
    } else if (unit < previousUnit) {
      group += (pending ?? 1) * unit;
      previousUnit = unit;
    } else return null;
    pending = null;
  }
  if (total && previousUnit === 10000 && /万[一二两三四五六七八九]$/u.test(token)) return String(total + pending * 1000);
  return String(total + group + (pending ?? 0));
}

function candidate(kind, field, value, source, { subject = '', unit = '' } = {}) {
  return { kind, field, subject, value, unit, source };
}

function alternatives(text) {
  const choice = CHOICE_ZH.exec(text) ?? CHOICE_EN.exec(text);
  return [...new Set([...(choice?.slice(1).map(stripText) ?? []),
    ...Array.from(text.matchAll(LABEL), match => match[1])].filter(Boolean))];
}

function interpret(text, state, previousOptions = [], focus = null) {
  const options = alternatives(text);
  const named = [...new Set([...options, ...previousOptions, ...state.options.map(option => option.label)])];
  const claims = options.map(value => candidate('option', 'option', value, value));
  for (const match of text.matchAll(/[^。！？!?；;\n]+/gu)) {
    const source = stripText(match[0]);
    if (!source) continue;
    const certainty = CONDITION.test(source) ? 'conditional' : HEDGE.test(source) || RANGE.test(source) ? 'estimate' :
      REVISION.test(source) ? 'revision' : PRIOR.test(source) ? 'previous' : null;
    const direct = source.split(/，|,(?![0-9]{3}(?:[^\d]|$))/u);
    const revisionText = certainty === 'revision' ? direct.find(part => REVISION.test(part)) : null;
    const revisionFields = revisionText ? Object.entries({
      onsite_max: /到岗/u, hours_max: /工时|时长|小时/u,
      income_min: /月收入|收入底线|月薪/u, cost_max: /预算|费用/u,
    }).filter(([, pattern]) => pattern.test(revisionText)).map(([field]) => field) : [];
    for (const { field, unit, re } of LIMIT_RULES) {
      if (unit.startsWith('yuan') && NON_CNY.test(source)) continue;
      let number = re.exec(source)?.[1];
      if (revisionText) {
        if (revisionFields.length !== 1 || revisionFields[0] !== field) continue;
        const revision = new RegExp(`(?:改(?:为|到|成)|修订为|调整(?:为|到)|更(?:正|改)为)\\s*(${NUMBER})`, 'u');
        number = revision.exec(revisionText)?.[1];
      }
      const value = number ? writtenNumber(number) : null;
      const applicableUnit = field === 'cost_max' && /每月|月预算|这个月|本月/u.test(revisionText ?? source) ? 'yuan/month' : unit;
      if (value !== null) claims.push(candidate(certainty ?? 'constraint', field, value, source, { unit: applicableUnit }));
    }
    if (/(?:^|[，,：:\s]|我)(?:不能|不得|不可以)搬家/u.test(source) && !/不是|并非/u.test(source)) {
      claims.push(candidate(certainty ?? 'constraint', 'move_allowed', 'no', source));
    }
    for (const label of named) {
      // Only an explicitly named option at the start of a statement can own its numbers.
      if (!source.startsWith(label) || !/^[：:\s每月费价花支要需不无]/u.test(source.slice(label.length))) continue;
      const body = source.slice(label.length);
      for (const { field, unit, re } of MEASUREMENT_RULES) {
        if (unit.startsWith('yuan') && NON_CNY.test(body)) continue;
        const number = re.exec(body)?.[1];
        const value = number ? writtenNumber(number) : null;
        if (value !== null) claims.push(candidate(certainty ?? 'measurement', field, value, source, { subject: label, unit }));
      }
      const moves = /^(?:[：:\s]*)(不需要|无需|需要|必须)搬家/u.exec(body);
      if (moves) claims.push(candidate(certainty ?? 'measurement', 'move_required',
        /不|无/u.test(moves[1]) ? 'no' : 'yes', source, { subject: label }));
    }
    for (const sentence of direct) {
      const line = stripText(sentence);
      for (const [kind, re] of [
        ['goal', /^(?:我的目标是|目标是|我希望达成|我想实现)(.{1,100})$/u],
        ['preference', /^(?:我最看重|我更看重|我更在意)(.{1,100})$/u],
        ['deadline', /^(?:我希望)?(.{1,45}?(?:前|内|之前))(?:必须|需要|要|想)?决定$/u],
      ]) {
        const value = re.exec(line)?.[1];
        if (value && !certainty) claims.push(candidate(kind, kind, stripText(value), line));
      }
    }
    if (/^(?:没有|无)(?:其他)?硬约束$/u.test(source)) {
      claims.push(candidate('constraint', 'constraints_confirmed', 'yes', source));
    }
  }
  if (!claims.length && focus) {
    const separator = focus.indexOf(':');
    const field = focus.slice(0, separator);
    const subject = focus.slice(separator + 1);
    const source = stripText(text);
    const metric = Object.values(LIMITS).find(item => item.metric === field);
    const matching = state.constraints.find(limit => metric?.label === limit.label);
    const unitPattern = { 'yuan': '元', 'yuan/month': '元', 'days/week': '天', 'hours/week': '(?:个)?小时' }[matching?.unit];
    const amount = unitPattern && new RegExp('^(' + NUMBER + ')\\s*' + unitPattern + '[。!！]?$', 'u').exec(source);
    const negative = field === 'move_required' && /^(?:不用|无需|不需要)(?:搬家)?[。!！]?$/u.test(source);
    const affirmative = field === 'move_required' && /^(?:需要|必须)(?:搬家)?[。!！]?$/u.test(source);
    const value = amount ? writtenNumber(amount[1]) : negative ? 'no' : affirmative ? 'yes' : null;
    if (matching && value !== null && state.options.some(option => option.label === subject)) {
      claims.push(candidate('measurement', field, value, source,
        { subject, unit: matching.unit === 'boolean' ? '' : matching.unit }));
    }
  }
  const relevant = new Map(claims.map(item => [JSON.stringify(item), item]));
  return { options, claims: [...relevant.values()] };
}

function nextQuestion(state, claims) {
  const ask = (question, focus = null) => ({ question, focus });
  const pending = claims.filter(item => item.status === 'PROVISIONAL');
  const constraint = [...pending].reverse().find(item => ['constraint', 'revision'].includes(item.role) && Object.hasOwn(LIMITS, item.field));
  if (constraint) {
    const label = LIMITS[constraint.field].label;
    return ask(constraint.field === 'income_min'
      ? '月收入底线会排除不达标的岗位。两个岗位各自有依据的月收入是多少？'
      : `${label}底线会影响哪些方案可行。各方案在这项条件上的数值或范围是什么？`);
  }
  const measurement = pending.find(item => item.role === 'measurement' && state.options.some(option => option.label === item.subject));
  if (measurement) return ask(`请核对「${measurement.subject}」的这条资料及其来源。`, `confirm_claim:${measurement.id}`);
  for (const limit of state.constraints) {
    const unknown = state.options.find(option => !option.measurements[limit.id]?.source);
    if (!unknown) continue;
    const measure = Object.values(LIMITS).find(item => item.label === limit.label);
    const focus = measure ? `${measure.metric}:${unknown.label}` : null;
    return ask(`「${unknown.label}」的${limit.label}有什么可核对的资料？`, focus);
  }
  if (state.options.length < 2) return ask(pending.some(item => item.field === 'option')
    ? '原文列出的哪些行动确实可选？请逐条核对。' : '你目前实际可以采取哪些行动？');
  if (!state.constraints_confirmed) return ask('哪些底线会直接排除方案？没有其他底线时也可以明确说明。');
  if (!state.objectives.length) return ask('这些可行方案之间，你最重要的比较目标是什么？');
  if (!state.deadline) return ask('最晚什么时候要决定？');
  return ask(null);
}

function summarize(state, domain, claims) {
  const labels = [...new Set([...state.options.map(option => option.label),
    ...claims.filter(item => item.field === 'option' && item.status === 'PROVISIONAL').map(item => item.value)])];
  const differences = labels.map(label => state.options.some(option => option.label === label) ? label : `${label}（待确认）`);
  const unknowns = [];
  if (!state.constraints_confirmed) unknowns.push('哪些底线最终适用');
  if (!state.options.length || state.options.some(option => state.constraints.some(limit => !option.measurements[limit.id]?.source))) {
    unknowns.push('各方案的适用条件和可核对证据');
  }
  if (!state.objectives.length) unknowns.push('目标、单位和比较方向');
  if (!state.deadline) unknowns.push('最晚决定时间');
  return {
    phase: 'CLARIFY',
    conversation_version: '0.6.0',
    domain,
    claims,
    options: claims.filter(item => item.role === 'option' && item.status !== 'DISMISSED')
      .map(({ id, value: label, status }) => ({ id, label, status })),
    summary: {
      conclusion: labels.length > 1
        ? '先核对哪些行动可选、各自是否满足底线，再比较可能的取舍。'
        : '先把你要决定的事情、可选行动和限制说清楚。',
      differences,
      unknowns,
      ...nextQuestion(state, claims),
      warning: '目前按原文提取线索。请确认候选和资料后再计算，缺失项保留未知。',
    },
    local_model_status: offlineModelStatus.status,
    local_model_receipt: offlineModelStatus,
  };
}

function append(state, previous, text) {
  const earlier = previous?.claims ?? [];
  const options = earlier.filter(item => item.field === 'option' && item.status !== 'DISMISSED').map(item => item.value);
  const parsed = interpret(text, state, options, previous?.summary.focus);
  const unique = new Set(earlier.map(({ field, subject, value, role }) => JSON.stringify([field, subject, value, role])));
  const added = parsed.claims.filter(({ field, subject, value, kind }) => {
    const key = JSON.stringify([field, subject, value, kind]);
    if (unique.has(key)) return false;
    unique.add(key);
    return true;
  }).slice(0, Math.max(0, 64 - earlier.length));
  const proposals = added.map(({ kind: role, ...item }, index) => ({
    ...item, kind: role === 'estimate' ? 'estimate' : role === 'conditional' ? 'assumption' : 'fact',
    role, id: `claim_${earlier.length + index + 1}`, status: 'PROVISIONAL',
  }));
  return summarize(state, previous?.domain ?? DOMAINS.find(([, pattern]) => pattern.test(text))?.[0] ?? 'general',
    [...earlier, ...proposals]);
}

export const beginIntake = state => append(state, null, state.question);
export const refreshIntake = (state, intake) => summarize(state, intake.domain, intake.claims);

export function respond(state, intake, text) {
  if (typeof text !== 'string' || !stripText(text) || [...text].length > 6000) {
    throw new Error('请输入非空的跟进内容，最多 6000 字。');
  }
  return append(state, intake, text);
}

export const actionable = item => ['option', 'deadline', 'goal', 'constraint', 'revision', 'measurement'].includes(item.role);

function adopt(state, proposal, value, source) {
  if (proposal.field === 'option') {
    if (!state.options.some(option => option.label === value)) {
      state.options.push({ id: `option_${proposal.id}`, label: value, measurements: {}, scores: {} });
    }
  } else if (proposal.field === 'goal') {
    state.intent = value;
  } else if (proposal.field === 'deadline') {
    state.deadline = value;
  } else if (proposal.field === 'constraints_confirmed' && value === 'yes') {
    state.constraints_confirmed = true;
  } else if (Object.hasOwn(LIMITS, proposal.field)) {
    const { label, unit: defaultUnit, operator } = LIMITS[proposal.field];
    const unit = proposal.unit || defaultUnit;
    const threshold = value === 'no' && unit === 'boolean' ? '0' : value;
    const matching = state.constraints.find(limit =>
      limit.label === label && limit.unit === unit && limit.operator === operator);
    if (proposal.role === 'revision' && !matching) throw new Error('先核对要修改的是哪条现有底线。');
    if (matching && matching.threshold !== threshold && proposal.role !== 'revision') {
      throw new Error('已有不同的底线。请明确提出修改，或在结构化条件里核对冲突。');
    }
    if (matching) Object.assign(matching, { threshold, source });
    else state.constraints.push({ id: `limit_${proposal.field}`, label, unit, operator, threshold, source });
    state.constraints_confirmed = false;
  } else if (proposal.role === 'measurement') {
    const option = state.options.find(item => item.label === proposal.subject);
    const metric = Object.values(LIMITS).find(entry => entry.metric === proposal.field);
    const unit = proposal.unit || metric?.unit;
    const limits = metric ? state.constraints.filter(limit => limit.label === metric.label && limit.unit === unit) : [];
    if (!option || limits.length !== 1) throw new Error('请先确认这条测量对应的方案和底线。');
    const point = unit === 'boolean' && ['yes', 'no'].includes(value) ? (value === 'yes' ? '1' : '0') : value;
    const previous = option.measurements[limits[0].id];
    if (previous?.source && (previous.lower !== point || previous.upper !== point)) {
      throw new Error('已记录不同的测量。请在结构化条件中核对两个来源后修改。');
    }
    option.measurements[limits[0].id] = { lower: point, upper: point, unit, kind: 'fact', source };
  } else {
    throw new Error('此线索需要在结构化条件中确认。');
  }
}

export function resolveClaim(state, intake, id, action, correction) {
  const proposal = intake.claims.find(item => item.id === id);
  if (!proposal || proposal.status !== 'PROVISIONAL') throw new Error('该候选已处理或不在本次草稿中。');
  if (!['accept', 'correct', 'reject'].includes(action)) throw new Error('需要明确核对候选。');
  let updated = state;
  let value = proposal.value;
  if (action !== 'reject') {
    if (!actionable(proposal)) throw new Error('这条内容只能保留为待核对线索。');
    if (action === 'correct') {
      value = typeof correction === 'string' ? stripText(correction) : '';
      if (!value || [...value].length > 400) throw new Error('请填写明确的更正内容。');
    }
    updated = { ...structuredClone(state), confirmed: false };
    const prefix = action === 'correct' ? `用户确认更正：${value}；原文：` : '用户确认原文：';
    const source = [...(prefix + proposal.source)].slice(0, 400).join('');
    adopt(updated, proposal, value, source);
    updated = normalizeDecision(updated);
  }
  const claims = intake.claims.map(item => {
    if (item.id === id) return { ...item, ...(action === 'correct' ? { original_value: item.value, value } : {}),
      status: action === 'reject' ? 'DISMISSED' : 'USER_CONFIRMED' };
    if (action !== 'reject' && proposal.role === 'revision' && item.status === 'USER_CONFIRMED' &&
        item.field === proposal.field && item.unit === proposal.unit) return { ...item, status: 'SUPERSEDED' };
    return item;
  });
  return { state: updated, intake: summarize(updated, intake.domain, claims) };
}
