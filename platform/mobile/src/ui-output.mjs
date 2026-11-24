import { button, element, input } from './ui-input.mjs';
import { actionable } from './decision-intake.mjs';

const labels = {
  ACCEPT: '通过', REJECT: '不通过', UNRESOLVED: '待核实',
  UNKNOWN: '未知', POSSIBLE: '区间跨过约束', CERTAIN_PASS: '确定通过', CERTAIN_FAIL: '确定不通过',
  FEASIBLE: '当前可用', EXPIRED: '已到期', EXECUTED: '已计算', INELIGIBLE: '条件不足', FAILED: '执行失败',
  UNSUPPORTED: '此版本未实现',
  ANALYZED: '已计算', CLARIFY: '待澄清', HIGH: '优先补齐', DEFERRED: '可暂缓', NOT_OBSERVED: '未观察',
};

export const display = value => Object.hasOwn(labels, value) ? labels[value] : (value || '—');

function details(parent, title) {
  const node = element(parent, 'details');
  element(node, 'summary', title);
  return node;
}

function list(parent, values = []) {
  if (!values?.length) return;
  const rows = element(parent, 'ul');
  for (const value of values) element(rows, 'li', String(value));
}

function strings(value) {
  if (value == null) return [];
  return Array.isArray(value) ? value.map(String) : [String(value)];
}

const targets = {
  measurements: 'constraints', scores: 'objectives', weights: 'objectives',
  score_dependence: 'objectives', precision_radius: 'objectives', scenario_basis: 'scenarios',
  evidence: 'evidence', scenarios: 'scenarios', information: 'information',
  signals: 'information', prior: 'information', likelihoods: 'information',
  cost: 'information', actions_by_signal: 'information', timing_basis: 'information',
  timing: 'timing', investigation: 'timing', actions: 'timing', constraints: 'constraints', objectives: 'objectives',
};

export function drawPlanning(root, plan, jump, { compact = false } = {}) {
  if (!plan) return;
  list(root, (plan.intent?.hints ?? []).map(hint => hint.prompt));
  let items = plan.items ?? [];
  if (compact) items = items.slice(0, 5);
  if (!items.length) return;
  const rows = element(root, 'ul');
  for (const item of items) {
    const entry = element(rows, 'li');
    const field = item.target?.field;
    const target = targets[field] || field;
    if (!jump || item.priority === 'DEFERRED') element(entry, 'p', item.prompt);
    else button(entry, item.prompt, () => jump(target, item.target), 'quiet plan-link');
    if (!compact && item.reason) element(entry, 'p', item.reason, 'help');
  }
}

export function drawClarifications(root, understanding, questions, plan, jump) {
  root.replaceChildren();
  if (understanding?.message) element(root, 'p', understanding.message);
  const suggestions = understanding?.suggestions ?? [];
  if (suggestions.length) {
    element(root, 'h3', '待确认的原文线索');
    list(root, suggestions.map(item => `${item.value} · ${item.source}`));
  }
  if (plan?.items?.length) drawPlanning(root, plan, jump, { compact: true });
  else list(root, questions?.map(item => item.prompt));
  root.hidden = !root.childElementCount;
}

const claimLabels = {
  option: '备选行动', goal: '目标', preference: '偏好', deadline: '期限', constraint: '硬约束',
  measurement: '方案资料', revision: '底线修订', previous: '以往条件', conditional: '条件说明', estimate: '未核实估计',
};

export function drawIntake(root, intake, reply, resolve) {
  root.replaceChildren();
  root.hidden = !intake;
  if (!intake) return;
  const { summary, claims } = intake;
  element(root, 'h3', '本机初步判断');
  element(root, 'p', summary.conclusion);
  if (summary.differences.length || summary.unknowns.length) {
    const sources = details(root, '查看备选行动和未知项');
    if (summary.differences.length) {
      element(sources, 'h4', '备选行动');
      list(sources, summary.differences);
    }
    if (summary.unknowns.length) {
      element(sources, 'h4', '当前未知');
      list(sources, summary.unknowns);
    }
  }
  if (summary.question) {
    const next = element(root, 'div', '', 'intake-next');
    element(next, 'h4', '下一问');
    element(next, 'p', summary.question);
  }
  if (summary.warning) element(root, 'p', summary.warning, 'help');
  const followup = element(root, 'form');
  followup.autocomplete = 'off';
  const answer = input(followup, '补充回应', '', () => {}, { rows: 2, limit: 6000 });
  answer.required = true;
  const send = element(followup, 'button', '补充并检查线索', 'secondary');
  send.type = 'submit';
  followup.addEventListener('submit', event => {
    event.preventDefault();
    reply(answer.value);
  });
  const status = element(root, 'p', '', 'message');
  status.id = 'intake-message';
  status.tabIndex = -1;
  status.setAttribute('role', 'status');
  const pending = claims.filter(item => item.status === 'PROVISIONAL');
  if (!pending.length) return;
  element(root, 'h4', '逐项核对');
  const proposals = element(root, 'ul', '', 'intake-claims');
  for (const claim of pending) {
    const row = element(proposals, 'li');
    row.dataset.claimField = claim.field;
    const { id, role, subject, unit, value, source } = claim;
    element(row, 'strong', `${claimLabels[role]} · ${[subject, value, unit].filter(Boolean).join(' ')}`);
    element(row, 'p', `原文 · ${source}`, 'help');
    const controls = element(row, 'div', '', 'controls');
    if (actionable(claim)) button(controls, '确认采用', () => resolve(id, 'accept'));
    button(controls, '略过线索', () => resolve(id, 'reject'), 'quiet');
    if (!actionable(claim)) continue;
    const correction = details(row, '更正候选内容');
    const corrected = input(correction, '正确的内容', value, () => {});
    button(correction, '确认更正', () => resolve(id, 'correct', corrected.value));
  }
}

function drawTable(root, { title, columns, rows }) {
  if (!Array.isArray(rows) || !Array.isArray(columns)) return;
  const wrapper = element(root, 'div', '', 'table-wrap');
  wrapper.tabIndex = 0;
  wrapper.setAttribute('role', 'region');
  wrapper.setAttribute('aria-label', title);
  const table = element(wrapper, 'table');
  element(table, 'caption', title);
  const header = element(element(table, 'thead'), 'tr');
  for (const name of columns) element(header, 'th', String(name)).scope = 'col';
  const body = element(table, 'tbody');
  for (const values of rows) {
    if (!Array.isArray(values)) continue;
    const row = element(body, 'tr');
    for (const value of values) element(row, 'td', value == null ? '—' : String(value));
  }
}

function chartNumber(value) {
  const [numerator, denominator = '1'] = String(value).split('/');
  return Number(numerator) / Number(denominator);
}

function drawChart(root, { title, unit, rows }) {
  const bounds = rows.map(row => [chartNumber(row.lower), chartNumber(row.upper)]);
  if (!bounds.length || bounds.some(pair => pair.some(value => !Number.isFinite(value)))) return;
  const minimum = Math.min(...bounds.map(pair => pair[0]));
  const maximum = Math.max(...bounds.map(pair => pair[1]));
  const width = maximum - minimum;
  const fraction = number => width ? 100 * (number - minimum) / width : 50;
  const chart = element(root, 'figure', '', 'interval-chart');
  element(chart, 'figcaption', title);
  element(chart, 'p', `单位：${unit}。点击各行查看精确区间。`, 'help');
  const summary = element(chart, 'p', '', 'interval-selection');
  summary.setAttribute('aria-live', 'polite');
  let selected;
  for (const [index, row] of rows.entries()) {
    const [lower, upper] = bounds[index];
    const description = `${row.label}：${row.lower} 至 ${row.upper} ${unit}`;
    const control = button(chart, row.label, () => {
      selected?.setAttribute('aria-pressed', 'false');
      control.setAttribute('aria-pressed', 'true');
      selected = control;
      summary.textContent = description;
    });
    control.setAttribute('aria-label', description);
    control.setAttribute('aria-pressed', 'false');
    const track = element(control, 'span', '', 'interval-track');
    track.setAttribute('aria-hidden', 'true');
    const bar = element(track, 'span', '', 'interval-bar');
    bar.style.setProperty('--start', `${Math.min(98, fraction(lower))}%`);
    bar.style.setProperty('--width', `${width ? fraction(upper) - fraction(lower) : 0}%`);
  }
  drawTable(details(chart, '查看区间数值表'), {
    title, columns: ['比较项', `下界（${unit}）`, `上界（${unit}）`], rows: rows.map(row => [row.label, row.lower, row.upper]),
  });
}

const auditLabels = {
  applicability: '适用范围', inputs: '输入', outputs: '输出', units: '单位', assumptions: '假设',
  uncertainty: '不确定性', sources: '来源', failure_conditions: '退出条件', replay: '复算',
  baseline: '对比基线', evidence: '证据等级', depends_on: '前置方法', source_baseline: '来源提交',
};

function drawMethod(root, method) {
  const group = element(root, 'article', '', 'result-group');
  element(group, 'h4', method.title || method.model_id);
  element(group, 'p', `${display(method.status)} · ${method.model_id}@${method.version}`, 'help');
  const result = method.result;
  if (result?.summary) element(group, 'p', result.summary);
  if (result?.evidence_status) element(group, 'p', `证据状态：${display(result.evidence_status)}`, 'help');
  for (const chart of result?.charts ?? []) drawChart(group, chart);
  for (const table of result?.tables ?? []) drawTable(group, table);
  const audit = details(group, '适用条件、版本与来源');
  list(audit, strings(method.reasons));
  for (const [field, name] of Object.entries(auditLabels)) {
    if (method[field]) {
      element(audit, 'h4', name);
      list(audit, strings(method[field]));
    }
  }
}

export function drawResult(root, state, report, jump) {
  root.replaceChildren();
  const summary = element(root, 'div', '', 'result-summary');
  element(summary, 'h3', display(report.status));
  list(summary, strings(report.advice));
  if (report.priority_gap) element(summary, 'p', `优先核实：${report.priority_gap}`);
  list(summary, strings(report.risks));
  const rows = report.feasibility ?? [];
  if (rows.length) {
    drawTable(root, {
      title: '硬约束与时间可用性',
      columns: ['方案', '硬约束', '当前时间', '逐项理由'],
      rows: rows.map(row => [
        row.label, display(row.status), display(report.temporal_scope?.[row.option_id]),
        row.checks?.map(item => {
          const name = state.constraints.find(constraint => constraint.id === item.constraint_id)?.label ?? item.constraint_id;
          return `${name} · ${display(item.status)} · ${item.reason}`;
        }).join('；') || '—',
      ]),
    });
  }
  const next = report.plan;
  if (next?.items?.length) {
    const planning = details(root, '下一步可以核实什么');
    drawPlanning(planning, next, jump);
  } else if (report.questions?.length) {
    drawClarifications(root, null, report.questions, null, jump);
  }
  if (report.gaps?.length) list(details(root, '全部待核实信息'), strings(report.gaps));
  const executed = (report.methods ?? []).filter(method => method.status === 'EXECUTED');
  const other = (report.methods ?? []).filter(method => method.status !== 'EXECUTED');
  if (executed.length) {
    const title = element(root, 'h3', '方法结果');
    if (root.id === 'result-content') {
      title.id = 'method-results';
      title.tabIndex = -1;
    }
    for (const method of executed) drawMethod(root, method);
  }
  if (other.length) {
    const skipped = details(root, '未执行的方法与原因');
    for (const method of other) drawMethod(skipped, method);
  }
  const trace = details(root, '复算凭据');
  element(trace, 'p', `Platform ${report.hub_version} · 修订 ${report.revision}`);
  if (report.input_hash) element(trace, 'p', `输入 SHA-256：${report.input_hash}`);
  if (report.trace) element(trace, 'pre', JSON.stringify(report.trace, null, 2));
}
