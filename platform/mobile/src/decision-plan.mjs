import { cmp, decimal, stripText } from './core.mjs';

const prompts = {
  options: '目前有哪些可以实际采取的行动？',
  objectives: '你想达成什么？哪些结果最能区分这些行动？',
  deadline: '何时必须作出决定？没有固定期限时可以明确说明。',
  constraints: '哪些条件一旦越界就必须放弃方案？也可以明确确认没有硬约束。',
  confirmed: '请核对问题、行动、目标、时限及底线。',
};
const domainHints = [
  ['CAREER', /工作|岗位|职业|跳槽|\b(?:jobs?|career|offers?)\b/i, '核对工作内容、合同条件和机会是否仍然可用。'],
  ['LEARNING', /学习|课程|培训|升学|\b(?:education|courses?|studying|training)\b/i, '核对参与条件、时间投入和预期学习成果。'],
  ['TRAVEL', /出行|旅行|交通|火车|航班|\b(?:travel|flights?|commute|trains?)\b/i, '核对总费用、门到门时间和可变更条件。'],
  ['HOUSEHOLD', /租房|搬家|住房|\b(?:rent|housing|apartment|relocat\w*)\b/i, '核对居住条件、完整支出和变更成本。'],
  ['HEALTH', /就医|健康|治疗|\b(?:health|treatment|medical)\b/i, '核对专业意见、适用人群和你在意的结果差异。'],
  ['FINANCE', /投资|理财|贷款|保险|\b(?:invest\w*|finance|loan|insurance)\b/i, '核对支付边界、费用和资金可用时点。'],
];
const waitCues = /等待|等.{0,12}再|延期|推迟|\b(?:wait\w*|delay\w*|postpon\w*)\b/i;
const timingCues = /等待|等.{0,12}再|延期|推迟|过期|截止|到期|失效|名额|只保留|\b(?:wait\w*|delay\w*|postpon\w*|deadlines?|expir\w*)\b/i;
const informationCues = /打听|调查|反馈|收集信息|获取信息|多了解|问清|核实后|\b(?:survey|feedback|research|investigat\w*|consult|verify)\b/i;
const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2, DEFERRED: 3 };
const documented = value => value && value.kind !== 'unknown' && stripText(value.source);
const bound = value => documented(value) && value.lower != null && value.upper != null;
const labels = list => new Map(list.map(row => [row.id, row.label]));

export function questionsFor(state) {
  const missing = { options: state.options.length < 2, objectives: !state.objectives.length,
    deadline: !state.deadline, constraints: !state.constraints_confirmed, confirmed: !state.confirmed };
  const questions = Object.keys(prompts).filter(field => missing[field]).map(field => ({ field, prompt: prompts[field] }));
  const groups = new Map();
  for (const constraint of state.constraints) {
    const key = JSON.stringify([stripText(constraint.label), stripText(constraint.unit), constraint.horizon || state.deadline]);
    const pair = groups.get(key) ?? { label: stripText(constraint.label), lower: null, upper: null };
    const side = constraint.operator.startsWith('>') ? 'lower' : 'upper';
    const candidate = { value: decimal(constraint.threshold), strict: constraint.operator.length === 1 };
    const existing = pair[side];
    const comparison = existing ? cmp(candidate.value, existing.value) * (side === 'lower' ? 1 : -1) : 1;
    if (comparison > 0 || (comparison === 0 && candidate.strict)) pair[side] = candidate;
    groups.set(key, pair);
  }
  for (const { label, lower, upper } of groups.values()) {
    if (lower && upper) {
      const comparison = cmp(lower.value, upper.value);
      if (comparison > 0 || (comparison === 0 && (lower.strict || upper.strict))) {
        questions.push({ field: 'constraints', prompt: `「${label}」的硬约束互相冲突，请复核阈值。` });
      }
    }
  }
  return questions;
}

function item(category, action, priority, prompt, reason, field, details = {}, evidence = 'UNKNOWN', proof) {
  return { id: [category.toLowerCase(), field, ...Object.values(details)].join(':'), category, stage: category,
    action, priority, prompt, reason, target: { field, ...details }, evidence_status: evidence, ...(proof ? { proof } : {}) };
}

function feasibilityItems(state, analysis) {
  const constraints = labels(state.constraints);
  const items = [];
  for (const row of analysis.feasibility) {
    const failure = row.checks.find(check => check.status === 'CERTAIN_FAIL');
    for (const check of row.checks.filter(check => ['POSSIBLE', 'UNKNOWN'].includes(check.status))) {
      const details = { option_id: row.option_id, constraint_id: check.constraint_id };
      const label = `${row.label} · ${constraints.get(check.constraint_id)}`;
      if (row.status === 'REJECT' && failure) {
        items.push(item('FEASIBILITY', 'DEFER', 'DEFERRED', `暂缓核实 ${label}。`,
          `「${constraints.get(failure.constraint_id)}」已确定不通过。单独补齐该项不会使方案可行。`,
          'measurements', details, 'LOGICAL_INVARIANT', { scope: 'CURRENT_FEASIBILITY_GATE', witness_constraint_id: failure.constraint_id }));
      } else {
        items.push(item('FEASIBILITY', 'VERIFY', 'HIGH', `核实 ${label} 的区间、单位及依据。`,
          `${check.reason} 核实此项可能改变方案能否进入可行集。`, 'measurements', details));
      }
    }
  }
  return items;
}

function comparisonItems(state, executed) {
  const options = labels(state.options), objectives = labels(state.objectives);
  const items = [];
  for (const { model_id, result } of executed) {
    for (const gap of result.score_gaps ?? []) {
      items.push(item('COMPARABILITY', 'VERIFY', 'MEDIUM', `核对 ${options.get(gap.option)} · ${objectives.get(gap.objective)} 的可比测量。`,
        gap.reason, 'scores', { option_id: gap.option, objective_id: gap.objective }));
    }
    if (model_id === 'pareto' && !state.weights_confirmed && !state.preferences && result.pairs?.some(pair => pair.relation === 'INCOMPARABLE')) {
      items.push(item('SENSITIVITY', 'ASK', 'MEDIUM', '确认哪些结果更重要。',
        '可行方案各有优势。可以说明优先顺序或确认权重区间。', 'weights', { model_id }, 'CONDITIONAL'));
    }
    if (['weight_sensitivity', 'c034_joint_robustness'].includes(model_id)) {
      for (const pair of result.pairs ?? []) {
        const number = value => {
          const [numerator, denominator = '1'] = String(value).split('/');
          return Number(numerator) / Number(denominator);
        };
        if (number(pair.lower) < 0 && number(pair.upper) > 0) {
          items.push(item('SENSITIVITY', 'COMPARE', 'MEDIUM', `复核 ${options.get(pair.a)} 与 ${options.get(pair.b)} 的敏感条件。`,
            pair.bounds === 'exact' ? '可行边界包含两种排序。' : '外界跨过零，仍需核对是否存在排序反转。',
            model_id === 'weight_sensitivity' ? 'weights' : 'score_dependence',
            { model_id, option_id: pair.a, rival_option_id: pair.b }, 'CONDITIONAL',
            { scope: 'CURRENT_MODEL_AND_FEASIBLE_SET', bounds: pair.bounds, lower: pair.lower, upper: pair.upper }));
        }
      }
    }
    if (result.leaders?.length && result.maximin_leaders?.length &&
        String([...result.leaders].sort()) !== String([...result.maximin_leaders].sort())) {
      items.push(item('MODEL_ASSUMPTIONS', 'COMPARE', 'MEDIUM', '比较最坏后悔值与最坏效用的取舍。',
        '两条规则在同一情景表上给出不同结果。', 'scenarios', { model_id }, 'CONDITIONAL'));
    }
  }
  return items;
}

function evidenceItems(state, analysis, text) {
  const items = [];
  for (const evidence of state.evidence) {
    if (evidence.verification === 'unverified' || evidence.kind === 'unknown' || !stripText(evidence.source) || !stripText(evidence.scope)) {
      items.push(item('EVIDENCE', 'VERIFY', 'MEDIUM', `核实「${evidence.label}」的来源和适用范围。`,
        '证据缺口会限制相应结论。', 'evidence', { evidence_id: evidence.id }));
    }
  }
  const accepted = analysis.feasibility.filter(row => row.status === 'ACCEPT' &&
    (!Object.hasOwn(analysis.temporal_scope, row.option_id) || analysis.temporal_scope[row.option_id] === 'FEASIBLE'));
  if (accepted.length > 1 && state.scenarios.length && !state.scenario_basis) {
    items.push(item('EVIDENCE', 'VERIFY', 'MEDIUM', '确认各情景的共同效用尺度和观察时段。',
      '后悔值比较需要可比的效用。', 'scenarios', { part: 'scenario_basis' }));
  }
  for (const scenario of accepted.length > 1 ? state.scenarios : []) {
    if (scenario.kind === 'unknown' || !stripText(scenario.source)) {
      items.push(item('EVIDENCE', 'VERIFY', 'MEDIUM', `核实「${scenario.label}」的来源和情景定义。`,
        '只有明确的情景才可以用作分析输入。', 'scenarios', { scenario_id: scenario.id }));
    }
    for (const option of accepted) {
      if (!bound(scenario.utilities[option.option_id])) items.push(item('EVIDENCE', 'VERIFY', 'MEDIUM',
        `核实「${option.label}」在「${scenario.label}」中的效用区间。`, '缺失的区间会影响可行方案之间的比较。',
        'scenarios', { scenario_id: scenario.id, option_id: option.option_id }));
    }
  }
  const info = state.information;
  const investigation = state.timing?.investigation;
  const timed = investigation && !info?.timing_basis;
  if ((!info && !informationCues.test(text)) || (timed && investigation.mode === 'joint') || analysis.methods.some(row =>
    (row.model_id === 'voi_point' || row.model_id === 'timing_investigation') && row.status === 'EXECUTED')) return items;
  const signals = info?.signals ?? [];
  const criteria = [
    ['signals', !signals.length, '明确准备查什么，以及调查可能给出哪些结果。'],
    ['scenarios', !state.scenarios.length, '列出调查涉及的不同状态及同尺度效用。'],
    ['prior', state.scenarios.some(s => !bound(info?.prior?.[s.id])), '核对各状态概率的来源和上下界。'],
    ['likelihoods', state.scenarios.some(s => signals.some(z => !bound(info?.likelihoods?.[s.id]?.[z.id]))), '核对各状态下得到每个信号的概率和来源。'],
    ['cost', !timed && !bound(info?.cost), '核对获取信息的成本及其效用单位。'],
    ['actions_by_signal', !timed && !(info?.unrestricted_actions && stripText(info.action_source)) &&
      signals.some(z => !documented(info?.actions_by_signal?.[z.id])), '核对看到调查结果后仍能采取哪些行动。'],
    ['timing_basis', !timed && !info?.timing_basis, '核对调查结果能否在行动机会关闭前到达。'],
  ];
  const next = criteria.find(([, missing]) => missing);
  if (next) items.push(item('EVIDENCE', 'VERIFY', 'MEDIUM', next[2], '这些信息决定能否比较调查与立即行动。', 'information', { part: next[0] }));
  else if (!timed) items.push(item('EVIDENCE', 'VERIFY', 'MEDIUM', '复核调查模型的准入条件。',
    '请查看模型审计中的适用性和证据理由。', 'information', { part: 'admission' }));
  return items;
}

function timingItems(state, analysis, text) {
  const timing = state.timing;
  if (!timing && !timingCues.test(text)) return [];
  const items = [];
  const ask = (prompt, part) => item('TIMING', 'VERIFY', 'MEDIUM', prompt,
    '等待会改变可采取的行动，统一时间起点和边界后才能比较。', 'timing', { part });
  if (!timing?.confirmed) return [ask('核对决定、等待和实际行动的时间界限。', 'confirmed')];
  if (!timing.time_unit || !timing.time_origin) return [ask('核对比较时机所用的时间单位和起点。', 'time_origin')];
  if (!stripText(timing.horizon?.source) || timing.horizon.kind === 'unknown') return [ask('核对共同评估期限及其来源。', 'horizon')];
  if (waitCues.test(text) && !bound(timing.wait_duration) && !timing.investigation) {
    items.push(ask('核对预计要等多久，以及等待后仍能采取哪些行动。', 'wait_duration'));
  }
  const result = analysis.methods.find(row => row.model_id === 'timing_actions')?.result;
  for (const row of result?.strategies ?? []) {
    if (row.status === 'EXPIRED' || row.status === 'UNKNOWN') {
      items.push(ask('核实受影响策略的截止点、到期后果和实际成本。', 'availability'));
      break;
    }
  }
  const times = result?.time_inputs;
  if (times) {
    const relations = [['决策截止点', times.prediction_vs_deadline, { boundary: 'decision_deadline' }],
      ['观察期限', times.prediction_vs_horizon, { boundary: 'horizon' }]];
    for (const [optionId, relation] of Object.entries(times.prediction_vs_action_cutoffs ?? {})) {
      relations.push([`「${labels(state.options).get(optionId)}」的截止点`, relation, { option_id: optionId }]);
    }
    for (const [label, relation, details] of relations) if (['AFTER', 'STRADDLES'].includes(relation)) {
      const crossing = relation === 'STRADDLES';
      items.push(item('TIMING', crossing ? 'VERIFY' : 'COMPARE', 'HIGH', `核对预测完成时间与${label}。`,
        crossing ? '预测区间跨过该边界。' : '当前预测区间越过了该边界。', 'timing',
        { part: 'predicted_completion', ...details }, 'CONDITIONAL', { scope: 'CURRENT_TIMING_ASSUMPTIONS', relation }));
    }
  }
  return items;
}

export function buildPlan(state, analysis) {
  const text = `${state.question} ${state.intent ?? ''}`;
  const executed = analysis.methods.filter(model => model.status === 'EXECUTED');
  const clarification = analysis.questions.map(({ field, prompt }) => item('CLARIFICATION', 'ASK', 'HIGH', prompt,
    '此回答用于确认本次选择的比较范围。', field));
  const feasibility = feasibilityItems(state, analysis);
  const comparison = comparisonItems(state, executed);
  const leaders = executed.filter(model => model.result.leaders?.length);
  if (new Set(leaders.map(model => [...model.result.leaders].sort().join(','))).size > 1) {
    comparison.push(item('MODEL_ASSUMPTIONS', 'COMPARE', 'MEDIUM', '核对各方法给出不同优选结果的条件。',
      '确认各自的可行集、效用含义和取舍规则。', 'methods', {}, 'CONDITIONAL',
      { scope: 'CURRENT_MODELS_AND_FEASIBLE_SET', model_ids: leaders.map(model => model.model_id) }));
  }
  const evidence = evidenceItems(state, analysis, text);
  const timing = timingItems(state, analysis, text);
  const items = [...clarification, ...feasibility, ...comparison, ...evidence, ...timing]
    .sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
  const hasModels = predicate => executed.some(model => predicate(model.model_id));
  const stage = (name, list, ready) => ({ stage: name,
    status: list.some(step => ['ASK', 'VERIFY'].includes(step.action)) ? 'NEEDS_INPUT' : ready ? 'READY' : 'PENDING' });
  return { items, steps: [stage('UNDERSTAND', clarification, true), stage('FEASIBILITY', feasibility, analysis.feasibility.length > 0),
    stage('COMPARE', [...comparison, ...evidence], hasModels(id => !id.startsWith('c028_') && !id.startsWith('timing_'))),
    stage('TIMING', timing, hasModels(id => id.startsWith('timing_'))), stage('REVIEW', [], false)],
    can_run: executed.map(({ model_id, title }) => ({ model_id, title })), intent: {
      description: state.confirmed ? state.intent : null,
      hints: domainHints.filter(([, rule]) => rule.test(text)).map(([domain, , prompt]) => ({ domain, prompt, evidence_status: 'PROVISIONAL_HINT' })),
    } };
}
