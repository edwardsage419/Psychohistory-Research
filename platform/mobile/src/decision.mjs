import { normalizeDecision, canonicalDecision, decisionWorkflowVersion } from './decision-contract.mjs';
import { buildPlan, questionsFor } from './decision-plan.mjs';
import { stripText } from './core.mjs';
import { beginIntake } from './decision-intake.mjs';
import { modelCards, platformCapabilities } from './platform-contract.generated.mjs';
import * as scoring from './scoring.mjs';
import * as information from './information.mjs';
import { immediateAvailability, timingActions } from './timing.mjs';
import { timingInvestigation } from './timing-investigation.mjs';

export { normalizeDecision };
export const HUB_VERSION = decisionWorkflowVersion;
export const MOBILE_VERSION = platformCapabilities.mobile.package_version;
const gateId = 'c028_interval_feasibility';
const execution = Object.freeze({ available: false, authorization: 'NOT_REQUESTED', action_endpoint: 'OBSERVATION_ONLY' });
const optionPattern = /(?:我该|应该选择|我应该|我在考虑)([^，,。；;？?\n]{1,100}?)[，,]?\s*(?:还是|或者)([^。；;？?\n]{1,100})(?:[？?。]|$)/;
const englishOptions = /\b(?:should i|i am considering)\s+([^,.!?\n]{1,100}?),?\s+or\s+([^,.!?\n]{1,100})(?:[.?]|$)/i;

const handlers = new Map([
  [gateId, scoring.feasibility],
  ['comparability', scoring.score],
  ['pareto', scoring.dominance],
  ['weight_sensitivity', scoring.sensitivity],
  ['c034_joint_robustness', scoring.sensitivity],
  ['C029', scoring.regret], ['C030', scoring.regret], ['C031', scoring.regret],
  ['voi_point', information.informationValue],
  ['timing_actions', timingActions],
  ['timing_investigation', timingInvestigation],
]);
const unsupported = '此 v0.5 方法仍为桌面候选，移动端未实现其区间或策略证书。';
export const registry = Object.freeze(modelCards.map(card => Object.freeze({ ...card,
  mobile_support: handlers.has(card.model_id) ? 'SUPPORTED_SUBSET' : 'UNSUPPORTED',
})));
const methodIdentity = ({ model_id, version }) => `${model_id}@${version}`;
const implemented = registry.filter(card => card.mobile_support === 'SUPPORTED_SUBSET');
if (platformCapabilities.exchange.decision_state.workflow_version !== HUB_VERSION ||
    implemented.length !== handlers.size ||
    implemented.map(methodIdentity).join() !== platformCapabilities.shared_methods.map(methodIdentity).join()) {
  throw new Error('Cross-end capability manifest does not match the mobile workflow or method registry.');
}
const capabilityContract = Object.freeze({
  schema: platformCapabilities.schema, platform_version: platformCapabilities.platform_version,
  runtime: platformCapabilities.mobile.runtime,
});

export function start(question) {
  const match = typeof question === 'string' ? (optionPattern.exec(question) ?? englishOptions.exec(question)) : null;
  const suggestions = (match?.slice(1) ?? []).map(stripText).filter(Boolean).map(value => ({ field: 'options',
    value, source: '原文片段' }));
  const mode = 'GUIDED_CONFIRMATION';
  const decision_id = Array.from(crypto.getRandomValues(new Uint8Array(16)), byte => byte.toString(16).padStart(2, '0')).join('');
  const state = normalizeDecision({ decision_id, revision: 1, question, understanding_receipt: { mode, suggestions } });
  const questions = questionsFor(state);
  const intake = beginIntake(state);
  return { state, questions, intake, understanding: { mode, suggestions,
    message: '本机按原文措辞和当前证据提出澄清。请确认候选片段与结构化资料。' },
  plan: buildPlan(state, { questions, methods: [], feasibility: [], temporal_scope: {} }), execution };
}

function entry(card, status, reasons, result = null) { return { ...card, status, reasons, result }; }

function execute(card, state, feasible) {
  try {
    const method = handlers.get(card.model_id);
    const receipt = method(state, { feasible, model_id: card.model_id });
    if (receipt.model_id !== card.model_id || receipt.version !== card.version ||
        !['EXECUTED', 'INELIGIBLE', 'FAILED'].includes(receipt.status) || !Array.isArray(receipt.reasons) ||
        receipt.reasons.some(reason => typeof reason !== 'string')) throw new Error('invalid model receipt');
    if (receipt.status === 'EXECUTED') {
      if (typeof receipt.result?.summary !== 'string' || (receipt.result.leaders ?? []).some(id =>
        !feasible.some(option => option.id === id))) throw new Error('invalid model result');
      return entry(card, receipt.status, receipt.reasons, receipt.result);
    }
    return entry(card, receipt.status, receipt.reasons);
  } catch {
    return entry(card, 'FAILED', ['方法执行或输出校验失败；已隔离本次结果。']);
  }
}

function recognizeEvidence(evidence) {
  return evidence.map(row => ({ ...row, evidence_status: row.kind === 'synthetic' ? 'SYNTHETIC' :
    row.kind === 'unknown' || row.verification === 'unverified' || !stripText(row.source) || !stripText(row.scope) ? 'UNKNOWN' : 'USER_ATTESTED' }));
}

function finish(state, values) {
  const gaps = [...new Set(values.gaps)];
  const report = { ...values, gaps, priority_gap: gaps[0] ?? null,
    mobile_version: MOBILE_VERSION, hub_version: HUB_VERSION, capability_contract: capabilityContract,
    execution, evidence_retrieval: 'USER_SOURCE_REQUIRED',
    evidence: recognizeEvidence(state.evidence), scientific_effectiveness: 'UNVERIFIED',
    trace: [{ phase: 'CONFIRMATION', status: values.status === 'CLARIFY' ? 'PENDING' : 'CONFIRMED' },
      ...values.methods.map(({ model_id, version, status, reasons }) => ({ phase: 'METHOD', model_id, version, status, reasons }))] };
  return { ...report, plan: buildPlan(state, report) };
}

export async function analyze(input) {
  const state = normalizeDecision(input);
  const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(canonicalDecision(state)));
  const input_hash = Array.from(new Uint8Array(hash), byte => byte.toString(16).padStart(2, '0')).join('');
  const questions = questionsFor(state);
  const base = { decision_id: state.decision_id, revision: state.revision, input_hash, questions };
  if (questions.length) {
    const methods = registry.map(card => card.mobile_support === 'UNSUPPORTED' ? entry(card, 'UNSUPPORTED', [unsupported]) :
      entry(card, 'INELIGIBLE', ['先完成问题澄清并确认输入。']));
    return finish(state, { ...base, status: 'CLARIFY', feasibility: [], methods, temporal_scope: {}, conditional_scope: false,
      advice: ['请先完成澄清。'], risks: [], gaps: questions.map(question => question.prompt) });
  }

  const gate = execute(registry[0], state, state.options);
  const feasibility = gate.result?.feasibility ?? [];
  const accept = new Set(feasibility.filter(row => row.status === 'ACCEPT').map(row => row.option_id));
  const feasible = state.options.filter(option => accept.has(option.id));
  const timed = state.timing?.confirmed;
  const temporal = new Map(timed ? feasible.map(option => [option.id, immediateAvailability(state.timing, option.id)]) : []);
  const current = timed ? feasible.filter(option => temporal.get(option.id) === 'FEASIBLE') : feasible;
  const executed = new Set(gate.status === 'EXECUTED' ? [`${gateId}@${gate.version}`] : []);
  const methods = [gate];
  for (const card of registry.slice(1)) {
    const candidates = card.candidate_scope === 'structural' ? feasible : current;
    const missing = (card.depends_on ?? []).filter(key => !executed.has(key));
    let outcome;
    if (card.mobile_support === 'UNSUPPORTED') outcome = entry(card, 'UNSUPPORTED', [unsupported]);
    else if (!feasible.length) outcome = entry(card, 'INELIGIBLE', ['当前没有已确认通过硬约束的方案。']);
    else if (!candidates.length) outcome = entry(card, 'INELIGIBLE', ['当前时点没有已确认可用的方案。']);
    else if (missing.length) outcome = entry(card, 'INELIGIBLE', missing.map(key => `前置方法尚未成功执行：${key}`));
    else outcome = execute(card, state, candidates);
    methods.push(outcome);
    if (outcome.status === 'EXECUTED') executed.add(`${card.model_id}@${card.version}`);
  }

  const advice = [], risks = [], gaps = [], leaderSets = new Set();
  const conditional_scope = feasibility.some(row => row.status === 'UNRESOLVED');
  if (conditional_scope) risks.push('可行性未决的方案暂不排名。比较仅适用于当前已通过底线的方案。');
  if ([...temporal.values()].includes('EXPIRED')) risks.push('已到期的方案从当前比较中排除，时机分析保留其机会窗口。');
  if ([...temporal.values()].includes('UNKNOWN')) risks.push('时间可用性待核实的方案暂不进入当前比较。');
  if (state.scenarios.length) risks.push('结论随所列情景与效用尺度变化。');
  if (state.timing?.investigation && methods.some(x => x.model_id === 'voi_point' && x.status === 'EXECUTED')) {
    risks.push('点值信息比较假设信号及时到达；有调查时长时同时查看行动时机。');
  }
  const constraintLabels = new Map(state.constraints.map(x => [x.id, x.label]));
  for (const row of feasibility) for (const check of row.checks) {
    if (['UNKNOWN', 'POSSIBLE'].includes(check.status)) gaps.push(`${row.label} · ${constraintLabels.get(check.constraint_id)}：${check.reason}`);
  }
  const labels = new Map(feasible.map(x => [x.id, x.label]));
  for (const method of methods) {
    if (method.status !== 'EXECUTED') {
      if (method.status !== 'UNSUPPORTED') gaps.push(...method.reasons);
      continue;
    }
    gaps.push(...(method.result.gaps ?? []));
    if (method.result.leaders?.length) {
      const names = method.result.leaders.map(id => labels.get(id));
      leaderSets.add([...method.result.leaders].sort().join(','));
      advice.push(`${method.title}的条件性结果：${names.join('、')}。${method.result.summary}`);
    }
  }
  if (leaderSets.size > 1) risks.push('适用方法给出不同的优选集合。请检查各方法的假设与取舍。');
  if (!advice.length) advice.push(!feasible.length ? '请核实底线及其来源。' : !current.length ? '请核对期限或补充替代方案。' :
    '请参照各方法的条件性比较与待补信息。');
  const status = methods.some(method => ![gateId, 'comparability'].includes(method.model_id) && method.status === 'EXECUTED') ? 'ANALYZED' : 'UNRESOLVED';
  return finish(state, { ...base, status, feasibility, methods, temporal_scope: Object.fromEntries(temporal), conditional_scope, advice, risks, gaps });
}
