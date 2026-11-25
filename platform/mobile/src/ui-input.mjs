const kinds = { unknown: '未知', fact: '事实（用户提供）', estimate: '估计', assumption: '假设', synthetic: '虚构示例' };
const MAX = { options: 24, constraints: 24, objectives: 16, scenarios: 24, evidence: 40, signals: 24 };
const unknown = () => ({ lower: null, upper: null, kind: 'unknown', source: '' });
const nextId = prefix => `${prefix}_${crypto.randomUUID().slice(0, 8)}`;
const getEntry = (record, id) => Object.hasOwn(record, id) ? record[id] : undefined;

function setEntry(record, id, value) {
  Object.defineProperty(record, id, { value, enumerable: true, configurable: true, writable: true });
}

export function element(parent, tag, content = '', className = '') {
  const node = document.createElement(tag);
  if (content) node.textContent = content;
  if (className) node.className = className;
  parent.append(node);
  return node;
}

export function button(parent, label, handle, kind = 'secondary') {
  const node = element(parent, 'button', label, kind);
  node.type = 'button';
  node.addEventListener('click', handle);
  return node;
}

export function input(parent, labelText, value, update, settings = {}) {
  const label = element(parent, 'label');
  element(label, 'span', labelText, 'label-text');
  const control = element(label, settings.rows ? 'textarea' : 'input');
  if (settings.rows) control.rows = settings.rows;
  control.autocomplete = 'off';
  control.spellcheck = false;
  control.maxLength = settings.numeric ? 40 : (settings.limit ?? 400);
  if (settings.numeric) control.inputMode = 'decimal';
  if (settings.placeholder) control.placeholder = settings.placeholder;
  control.value = value ?? '';
  control.addEventListener('input', () => update(control.value));
  return control;
}

export function select(parent, labelText, values, value, update) {
  const label = element(parent, 'label');
  element(label, 'span', labelText, 'label-text');
  const control = element(label, 'select');
  for (const [key, title, captionId] of Array.isArray(values) ? values : Object.entries(values)) {
    const option = element(control, 'option', title);
    option.value = key;
    if (captionId) option.dataset.optionCaption = captionId;
  }
  control.value = value ?? '';
  control.addEventListener('change', () => update(control.value));
  return control;
}

export function check(parent, labelText, value, update, captionId) {
  const label = element(parent, 'label', '', 'check');
  const control = element(label, 'input');
  control.type = 'checkbox';
  control.autocomplete = 'off';
  control.checked = value === true;
  const caption = element(label, 'span', labelText);
  if (captionId) caption.dataset.optionCaption = captionId;
  control.addEventListener('change', () => update(control.checked));
  return control;
}

function grid(root) {
  return element(root, 'div', '', 'editor-grid');
}

function field(parent, label, captionId) {
  const fieldset = element(parent, 'fieldset');
  const legend = element(fieldset, 'legend', label);
  if (captionId) {
    legend.dataset.optionCaption = captionId;
    fieldset.dataset.optionId = captionId;
  }
  return fieldset;
}

function textField(root, label, object, key, settings) {
  return input(root, label, object[key], value => { object[key] = value.trim(); }, settings);
}

function optionalField(root, label, object, key, settings) {
  return input(root, label, object[key], value => { object[key] = value.trim() || null; }, settings);
}

function numberField(root, label, object, key) {
  return optionalField(root, label, object, key, { numeric: true });
}

function selectField(root, label, object, key, values) {
  return select(root, label, values, object[key], value => { object[key] = value || null; });
}

function interval(root, object) {
  numberField(root, '下界', object, 'lower');
  numberField(root, '上界', object, 'upper');
}

function sourced(root, object, withUnit = false) {
  const values = grid(root);
  interval(values, object);
  if (withUnit) textField(values, '单位', object, 'unit');
  selectField(values, '数值类型', object, 'kind', kinds);
  textField(values, '来源或假设依据', object, 'source');
  if (withUnit) optionalField(values, '观察期限（选填）', object, 'horizon');
}

function optionName(option) {
  return option.label || '未命名方案';
}

function optionChoices(options) {
  return [['', '未指定'], ...options.map(option => [option.id, optionName(option), option.id])];
}

function quantity(root, option, records, id, unit) {
  const value = getEntry(records, id) ?? { ...unknown(), unit, horizon: null };
  const section = field(root, optionName(option), option.id);
  sourced(section, value, true);
  section.addEventListener('input', () => setEntry(records, id, value));
}

function possibility(root, records, id, label) {
  const value = getEntry(records, id) ?? unknown();
  const section = field(root, label);
  sourced(section, value);
  section.addEventListener('input', () => setEntry(records, id, value));
}

function section(root, key, label, opened) {
  const details = element(root, 'details');
  details.dataset.editorSection = key;
  details.open = opened.has(key);
  element(details, 'summary', label);
  return details;
}

function addRow(root, label, rows, max, create, rebuild, focusSelector) {
  const add = button(root, label, () => {
    rows.push(create());
    rebuild();
    const controls = document.querySelectorAll(focusSelector);
    controls[controls.length - 1]?.focus();
  });
  add.disabled = rows.length >= max;
}

function removeRow(root, item, rows, detach, rebuild) {
  const sectionKey = root.closest('details')?.dataset.editorSection;
  const remove = button(root, '移除', () => {
    rows.splice(rows.indexOf(item), 1);
    detach(item.id);
    rebuild();
    const editor = document.getElementById('editor');
    const target = sectionKey ? `[data-editor-section="${sectionKey}"] summary` : '.option-list input, .option-list + button';
    editor.querySelector(target)?.focus();
  }, 'quiet');
  remove.setAttribute('aria-label', `移除 ${item.label || '这一项'}`);
  return remove;
}

function options(root, state, rebuild) {
  const block = element(root, 'div');
  element(block, 'h3', '候选方案');
  element(block, 'p', '逐项核对原文推测，也可以补充维持现状或暂缓行动。', 'help');
  const rows = element(block, 'div', '', 'option-list');
  for (const option of state.options) {
    const row = element(rows, 'div', '', 'option-row');
    input(row, `方案 ${state.options.indexOf(option) + 1}`, option.label, value => {
      option.label = value.trim();
      remove.setAttribute('aria-label', `移除 ${optionName(option)}`);
      for (const caption of root.querySelectorAll('[data-option-caption]')) {
        if (caption.dataset.optionCaption === option.id) caption.textContent = optionName(option);
      }
    });
    const remove = removeRow(row, option, state.options, id => {
      for (const scenario of state.scenarios) delete scenario.utilities[id];
      if (state.timing) {
        delete state.timing.actions[id];
        for (const name of ['status_quo_option_id', 'fallback_option_id']) {
          if (state.timing[name] === id) state.timing[name] = null;
        }
      }
      if (state.information) {
        for (const action of Object.values(state.information.actions_by_signal)) {
          action.option_ids = action.option_ids.filter(value => value !== id);
        }
        for (const [signal, optionId] of Object.entries(state.information.fixed_policy)) {
          if (optionId === id) delete state.information.fixed_policy[signal];
        }
      }
      if (state.intended_option_id === id) state.intended_option_id = null;
      if (state.reference_option_id === id) state.reference_option_id = null;
    }, rebuild);
  }
  addRow(block, '添加方案', state.options, MAX.options,
    () => ({ id: nextId('option'), label: '', measurements: {}, scores: {} }), rebuild, '#editor .option-list input');
  const base = grid(block);
  optionalField(base, '你要达成的目的（选填）', state, 'intent');
  optionalField(base, '最后决定时间（选填）', state, 'deadline');
  const choices = optionChoices(state.options);
  selectField(base, '比较基准（选填）', state, 'reference_option_id', choices);
  selectField(base, '目前打算选择（选填）', state, 'intended_option_id', choices);
  optionalField(base, '事前计划或预期（选填）', state, 'plan_note', { rows: 2 });
  if (state.preferences) {
    const preferences = field(block, '当前偏好记录');
    for (const item of state.preferences.values) element(preferences, 'p', `${item.label} · ${item.value}`);
    element(preferences, 'p', `${state.preferences.applicability} · ${state.preferences.provenance}`, 'help');
    button(preferences, '移除当前偏好记录', () => { state.preferences = null; rebuild(); }, 'quiet');
  }
}

function constraints(root, state, rebuild, opened) {
  const block = section(root, 'constraints', '硬约束与测量', opened);
  element(block, 'p', '只有符合已确认底线的方案进入比较。同一项测量需要与底线使用相同的单位及观察期限。', 'help');
  check(block, '我已确认列出的硬约束，或确认没有硬约束', state.constraints_confirmed, checked => { state.constraints_confirmed = checked; });
  for (const constraint of state.constraints) {
    const row = field(block, constraint.label || '新增硬约束');
    row.dataset.itemId = constraint.id;
    const fields = grid(row);
    textField(fields, '约束名称', constraint, 'label');
    textField(fields, '单位', constraint, 'unit');
    selectField(fields, '比较规则', constraint, 'operator', [['<=', '不高于 ≤'], ['<', '低于 <'], ['>=', '不低于 ≥'], ['>', '高于 >']]);
    numberField(fields, '阈值', constraint, 'threshold');
    textField(fields, '来源或约束依据', constraint, 'source');
    optionalField(fields, '观察期限（选填）', constraint, 'horizon');
    for (const option of state.options) quantity(row, option, option.measurements, constraint.id, constraint.unit);
    removeRow(row, constraint, state.constraints, id => {
      for (const option of state.options) delete option.measurements[id];
    }, rebuild);
  }
  addRow(block, '添加硬约束', state.constraints, MAX.constraints,
    () => ({ id: nextId('constraint'), label: '', unit: '', operator: '<=', threshold: null, source: '', horizon: null }),
    rebuild, '#editor [data-editor-section="constraints"] > fieldset > .editor-grid > label:first-child input');
}

function criteria(root, state, rebuild, opened) {
  const block = section(root, 'objectives', '目标、评分与权重', opened);
  element(block, 'p', '为每项目标确认单位、优劣方向和权重区间。评分与权重取值范围为 0 至 1，权重需可合计为 1。', 'help');
  const basis = grid(block);
  optionalField(basis, '评分口径与比较基础', state, 'score_basis');
  selectField(basis, '评分区间依赖假设', state, 'score_dependence', { unknown: '未知', rectangle: '各区间端点可独立组合', shared_additive: '共享加性误差（详见 JSON）' });
  optionalField(basis, '依赖假设来源', state, 'score_dependence_source');
  selectField(basis, '评分变换', state, 'score_transform', { unknown: '未知', identity: '沿用原评分', clip_01: '截断至 0–1' });
  numberField(basis, '精度半径（选填）', state, 'precision_radius');
  check(block, '我确认下列权重代表当前偏好', state.weights_confirmed, checked => { state.weights_confirmed = checked; });
  for (const objective of state.objectives) {
    const row = field(block, objective.label || '新增目标');
    row.dataset.itemId = objective.id;
    const fields = grid(row);
    textField(fields, '目标名称', objective, 'label');
    textField(fields, '单位', objective, 'unit');
    selectField(fields, '偏好方向', objective, 'direction', { max: '越高越好', min: '越低越好' });
    const weight = getEntry(state.weights, objective.id) ?? { lower: null, upper: null };
    const weightGroup = field(row, '权重区间');
    interval(grid(weightGroup), weight);
    weightGroup.addEventListener('input', () => {
      if (weight.lower === null && weight.upper === null) delete state.weights[objective.id];
      else setEntry(state.weights, objective.id, weight);
    });
    for (const option of state.options) quantity(row, option, option.scores, objective.id, objective.unit);
    removeRow(row, objective, state.objectives, id => {
      delete state.weights[id];
      delete state.shared_offsets[id];
      for (const option of state.options) delete option.scores[id];
    }, rebuild);
  }
  addRow(block, '添加目标', state.objectives, MAX.objectives,
    () => ({ id: nextId('objective'), label: '', unit: '分', direction: 'max' }),
    rebuild, '#editor [data-editor-section="objectives"] > fieldset > .editor-grid > label:first-child input');
}

function evidence(root, state, rebuild, opened) {
  const block = section(root, 'evidence', '证据与来源', opened);
  element(block, 'p', '记录使用的事实、估计或假设的来源与适用范围。模型使用各数值旁边标注的来源。', 'help');
  for (const item of state.evidence) {
    const row = field(block, item.label || '新增证据');
    row.dataset.itemId = item.id;
    const fields = grid(row);
    textField(fields, '证据名称', item, 'label');
    selectField(fields, '证据类型', item, 'kind', kinds);
    textField(fields, '来源', item, 'source');
    textField(fields, '适用范围', item, 'scope');
    selectField(fields, '核对状态', item, 'verification', { unverified: '未核对', user_supplied: '用户提供', user_confirmed: '用户核对' });
    removeRow(row, item, state.evidence, () => {}, rebuild);
  }
  addRow(block, '添加证据', state.evidence, MAX.evidence,
    () => ({ id: nextId('evidence'), label: '', kind: 'unknown', source: '', scope: '', verification: 'unverified' }),
    rebuild, '#editor [data-editor-section="evidence"] > fieldset > .editor-grid > label:first-child input');
}

function scenarios(root, state, rebuild, opened) {
  const block = section(root, 'scenarios', '情景与效用', opened);
  element(block, 'p', '按每种可能情景填写各方案的效用区间。情景须使用相同的效用单位和观察期限。', 'help');
  const basis = grid(block);
  optionalField(basis, '共同效用口径', state, 'scenario_basis');
  selectField(basis, '效用区间依赖假设', state, 'scenario_dependence', { unknown: '未知', rectangle: '各区间端点可独立组合', constrained: '受约束' });
  optionalField(basis, '依赖假设来源', state, 'scenario_dependence_source');
  for (const scenario of state.scenarios) {
    const row = field(block, scenario.label || '新增情景');
    row.dataset.itemId = scenario.id;
    const fields = grid(row);
    textField(fields, '情景名称', scenario, 'label');
    selectField(fields, '情景类型', scenario, 'kind', kinds);
    textField(fields, '来源或假设依据', scenario, 'source');
    for (const option of state.options) quantity(row, option, scenario.utilities, option.id, '效用');
    removeRow(row, scenario, state.scenarios, id => {
      if (state.information) {
        delete state.information.prior[id];
        delete state.information.likelihoods[id];
      }
      if (state.timing) {
        for (const rule of Object.values(state.timing.actions)) delete rule.delay_losses[id];
        const investigation = state.timing.investigation;
        if (investigation) {
          delete investigation.completion_by_state[id];
          investigation.joint = investigation.joint.filter(event => event.scenario_id !== id);
        }
      }
    }, rebuild);
  }
  addRow(block, '添加情景', state.scenarios, MAX.scenarios,
    () => ({ id: nextId('scenario'), label: '', kind: 'unknown', source: '', utilities: {}, probability: null }),
    rebuild, '#editor [data-editor-section="scenarios"] > fieldset > .editor-grid > label:first-child input');
}

function toggleSection(root, title, state, key, blank, rebuild) {
  check(root, title, Boolean(state[key]), value => {
    state[key] = value ? blank() : null;
    rebuild();
    rootFocus(root.dataset.editorSection);
  });
}

function rootFocus(key) {
  document.querySelector(`#editor [data-editor-section="${key}"] > label input`)?.focus();
}

function cutoff(root, label, parent, key) {
  const row = field(root, label);
  row.dataset.targetPart = key;
  const model = parent[key] ?? { at: null, inclusive: true, kind: 'unknown', source: '' };
  const fields = grid(row);
  numberField(fields, '距离起点的时间', model, 'at');
  selectField(fields, '数值类型', model, 'kind', kinds);
  textField(fields, '来源或依据', model, 'source');
  check(row, '截止时点仍可行动', model.inclusive, checked => { model.inclusive = checked; });
  row.addEventListener('input', () => { parent[key] = model.at === null ? null : model; });
}

function optionalRange(root, label, object, key, unit) {
  const value = object[key] ?? (unit ? { ...unknown(), unit, horizon: null } : unknown());
  const row = field(root, label);
  row.dataset.targetPart = key;
  sourced(row, value, Boolean(unit));
  row.addEventListener('input', () => {
    object[key] = value.lower === null && value.upper === null && !value.source ? null : value;
  });
}

function timing(root, state, rebuild, opened) {
  const block = section(root, 'timing', '行动时机与期限', opened);
  element(block, 'p', '确认起算时点和观察期限后，才将时间可用性纳入当前比较。完成分布及依赖等高级输入可用 JSON 编辑。', 'help');
  toggleSection(block, '纳入行动时机条件', state, 'timing', () => ({
    confirmed: false, time_unit: null, time_origin: null, horizon: null, decision_deadline: null, desired_time: null,
    predicted_completion: null, wait_duration: null, actions: {}, status_quo_option_id: null, fallback_option_id: null, investigation: null,
  }), rebuild);
  const t = state.timing;
  if (!t) return;
  const info = grid(block);
  optionalField(info, '时间单位', t, 'time_unit', { placeholder: '小时或天' });
  optionalField(info, '共同起算时点', t, 'time_origin');
  cutoff(block, '共同分析时域', t, 'horizon');
  cutoff(block, '决策期限', t, 'decision_deadline');
  optionalRange(block, '期望完成时段', t, 'desired_time');
  optionalRange(block, '预计完成时段', t, 'predicted_completion');
  optionalRange(block, '等待时长', t, 'wait_duration');
  const items = optionChoices(state.options);
  selectField(info, '现状方案', t, 'status_quo_option_id', items);
  selectField(info, '备用方案', t, 'fallback_option_id', items);
  for (const option of state.options) {
    const row = field(block, optionName(option), option.id);
    const rule = getEntry(t.actions, option.id) ?? { cutoff: null, switching_cost: null, delay_losses: {}, reversibility: null };
    check(row, '确认此方案的可用性规则', Object.hasOwn(t.actions, option.id), enabled => {
      if (enabled) setEntry(t.actions, option.id, rule);
      else delete t.actions[option.id];
    });
    cutoff(row, '方案截止时点（无单独截止可留空）', rule, 'cutoff');
    optionalRange(row, '转换成本', rule, 'switching_cost');
    for (const scenario of state.scenarios) possibility(row, rule.delay_losses, scenario.id, `${scenario.label || '未命名情景'}等待损失`);
    const reverse = rule.reversibility ?? { description: '', kind: 'unknown', source: '' };
    const reverseFields = grid(field(row, '可逆性'));
    textField(reverseFields, '撤回或调整行动的条件', reverse, 'description');
    selectField(reverseFields, '条件类型', reverse, 'kind', kinds);
    textField(reverseFields, '可逆性依据', reverse, 'source');
    reverseFields.addEventListener('input', () => { rule.reversibility = reverse.description ? reverse : null; });
  }
  toggleSection(block, '纳入有完成时长的调查', t, 'investigation', () => ({
    mode: 'deterministic', cost: null, duration: null, kind: 'unknown', source: '', joint: [], completion_by_state: {},
  }), rebuild);
  const investigation = t.investigation;
  if (investigation) {
    if (investigation.mode === 'deterministic') {
      const row = field(block, '调查时长及成本');
      optionalRange(row, '完成时长（确定时长的上下界相同）', investigation, 'duration');
      optionalRange(row, '调查成本', investigation, 'cost');
      const description = grid(row);
      selectField(description, '调查条件类型', investigation, 'kind', kinds);
      textField(description, '调查条件来源', investigation, 'source');
    } else {
      element(block, 'p', '当前调查有联合或条件完成分布，请在高级 JSON 中修改。', 'help');
    }
  }
  check(block, '我确认已填写的时机与时间假设', t.confirmed, checked => { t.confirmed = checked; });
}

function information(root, state, rebuild, opened) {
  const block = section(root, 'information', '调查信号与信息价值', opened);
  element(block, 'p', '概率需要可追溯的出处。每一行概率区间应允许合计为 1。调查后行动需要明确确认。', 'help');
  toggleSection(block, '纳入有限信号调查', state, 'information', () => ({
    signals: [], prior: {}, likelihoods: {}, cost: null, actions_by_signal: {}, unrestricted_actions: false,
    action_source: '', parameter_domain: 'unknown', parameter_domain_source: '', timing_basis: null, fixed_policy: {}, verification_source: null,
  }), rebuild);
  const info = state.information;
  if (!info) return;
  const basics = grid(block);
  optionalField(basics, '调查先于行动且不造成等待损失的依据', info, 'timing_basis');
  selectField(basics, '参数区间依赖', info, 'parameter_domain', { unknown: '未知', rectangle: '矩形范围', constrained: '受约束' });
  textField(basics, '参数依赖依据', info, 'parameter_domain_source');
  optionalField(basics, '固定策略核验来源（选填）', info, 'verification_source');
  optionalRange(block, '调查成本（使用共同效用单位）', info, 'cost', '效用');
  check(block, '我确认调查后仍可选择所有通过底线的方案', info.unrestricted_actions, enabled => {
    info.unrestricted_actions = enabled;
    if (enabled) info.actions_by_signal = {};
    rebuild();
    rootFocus('information');
  });
  textField(block, '调查后行动依据', info, 'action_source');
  for (const signal of info.signals) {
    const row = field(block, signal.label || '新增信号');
    const fields = grid(row);
    textField(fields, '信号名称', signal, 'label');
    select(fields, '固定策略选项（选填）', optionChoices(state.options),
      getEntry(info.fixed_policy, signal.id), value => {
        if (value) setEntry(info.fixed_policy, signal.id, value);
        else delete info.fixed_policy[signal.id];
      });
    if (!info.unrestricted_actions) {
      const action = getEntry(info.actions_by_signal, signal.id) ?? { option_ids: [], kind: 'unknown', source: '' };
      const choices = field(row, '获知该信号后仍可选的方案');
      for (const option of state.options) check(choices, optionName(option), action.option_ids.includes(option.id), enabled => {
        action.option_ids = enabled ? [...action.option_ids, option.id] : action.option_ids.filter(id => id !== option.id);
      }, option.id);
      selectField(choices, '行动依据类型', action, 'kind', kinds);
      textField(choices, '行动限制来源', action, 'source');
      choices.addEventListener('input', () => setEntry(info.actions_by_signal, signal.id, action));
    }
    removeRow(row, signal, info.signals, id => {
      delete info.actions_by_signal[id];
      delete info.fixed_policy[id];
      for (const row of Object.values(info.likelihoods)) delete row[id];
      const timed = state.timing?.investigation;
      if (timed) timed.joint = timed.joint.filter(event => event.signal_id !== id);
    }, rebuild);
  }
  addRow(block, '添加调查信号', info.signals, MAX.signals, () => ({ id: nextId('signal'), label: '' }),
    rebuild, '#editor [data-editor-section="information"] > fieldset > .editor-grid > label:first-child input:not([inputmode])');
  for (const scenario of state.scenarios) {
    const row = field(block, `${scenario.label || '未命名情景'}的概率`);
    possibility(row, info.prior, scenario.id, '先验概率');
    const likelihood = getEntry(info.likelihoods, scenario.id) ?? {};
    for (const signal of info.signals) possibility(row, likelihood, signal.id, `${signal.label || '未命名信号'}的条件概率`);
    row.addEventListener('input', () => {
      if (Object.keys(likelihood).length) setEntry(info.likelihoods, scenario.id, likelihood);
    });
  }
}

export function drawEditor(root, state, changed, initiallyOpen = []) {
  function rebuild(invalidate = true) {
    const opened = new Set([
      ...initiallyOpen,
      ...Array.from(root.querySelectorAll('details[open]'), node => node.dataset.editorSection),
    ]);
    initiallyOpen = [];
    root.replaceChildren();
    options(root, state, rebuild);
    constraints(root, state, rebuild, opened);
    criteria(root, state, rebuild, opened);
    scenarios(root, state, rebuild, opened);
    evidence(root, state, rebuild, opened);
    timing(root, state, rebuild, opened);
    information(root, state, rebuild, opened);
    if (invalidate) changed();
  }
  root.oninput = changed;
  rebuild(false);
}

const source = '完全虚构的周末出行算例';
const quantityOf = (lower, upper, unit) => ({ lower, upper, kind: 'synthetic', source, unit, horizon: '同一次出行' });
export const sampleQuestion = '虚构出行：我该选择短途火车还是长途巴士？预算不超过 160 元，还想兼顾节省时间与行程舒适度。';

export function sampleState(base) {
  return {
    ...base, intent: '在预算内选择周末出行方式', deadline: '同一次出行',
    constraints_confirmed: true,
    constraints: [{ id: 'budget', label: '预算', unit: '元', operator: '<=', threshold: 160, source, horizon: '同一次出行' }],
    objectives: [
      { id: 'time', label: '节省时间', unit: '分', direction: 'max' },
      { id: 'comfort', label: '舒适度', unit: '分', direction: 'max' },
    ],
    options: [
      { id: 'train', label: '短途火车', measurements: { budget: quantityOf(130, 150, '元') }, scores: { time: quantityOf(0.8, 0.9, '分'), comfort: quantityOf(0.5, 0.6, '分') } },
      { id: 'bus', label: '长途巴士', measurements: { budget: quantityOf(80, 95, '元') }, scores: { time: quantityOf(0.4, 0.5, '分'), comfort: quantityOf(0.7, 0.8, '分') } },
    ],
    weights_confirmed: true,
    weights: { time: { lower: 0.55, upper: 0.75 }, comfort: { lower: 0.25, upper: 0.45 } },
    score_basis: '两项目标分别使用共同的 0 至 1 量表。', score_dependence: 'rectangle',
    score_dependence_source: '虚构示例假设评分区间端点可独立组合。', score_transform: 'identity',
    scenarios: [
      { id: 'normal', label: '正常运行', utilities: { train: quantityOf(0.8, 0.9, '效用'), bus: quantityOf(0.7, 0.8, '效用') }, kind: 'synthetic', source, probability: null },
      { id: 'delay', label: '火车晚点', utilities: { train: quantityOf(0.35, 0.5, '效用'), bus: quantityOf(0.65, 0.75, '效用') }, kind: 'synthetic', source, probability: null },
    ],
    scenario_basis: '效用 0 最差，1 最好，同一次出行。', scenario_dependence: 'rectangle',
    scenario_dependence_source: '虚构情景的效用端点允许独立组合。', precision_radius: 0.05, reference_option_id: 'bus',
    evidence: [{ id: 'sample', label: '合成车费、时间与舒适度', kind: 'synthetic', source, verification: 'unverified', scope: '只用于演示' }],
  };
}
