import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { DecisionEditor } from './DecisionEditor';
import { DecisionHistory } from './DecisionHistory';
import { DecisionResults, type ResultScope } from './DecisionResults';
import { completePreference } from './DecisionWorkflowInputs';
import { decisionPath, demoQuestion, demoState } from './decisionTypes';
import type { Analysis, Api, DecisionState, DecisionVersion, PreferenceVersion, Quantity, Question, SourcedRange, StartResponse, Understanding, WorkflowPlan } from './decisionTypes';
import './decision.css';

type Draft = { state: DecisionState; savedRevision: number; preview: boolean };
const decimal = (value: unknown) => typeof value === 'number' || (typeof value === 'string' && /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(value.trim()));
const missingFields = (state: DecisionState): Record<string, boolean> => ({
  objectives: !state.objectives.length,
  options: state.options.length < 2,
  deadline: !state.deadline?.trim(),
  constraints: !state.constraints_confirmed,
  confirmed: !state.confirmed,
});

function clarificationIssue(state: DecisionState, guided: boolean): string {
  if (!state.question.trim()) return '请填写决策问题。';
  if (guided && !state.intent?.trim()) return '请在「决策意图与证据」填写并确认本次决策意图。';
  if (!state.deadline?.trim()) return '请填写决策时限。没有固定期限时可填「无固定期限」。';
  if (!state.constraints_confirmed) return '请核对并确认硬约束清单。';
  if (state.options.length < 2) return '请填写至少两个可实际采取的方案。';
  if (!state.objectives.length) return '请填写至少一个目标及其单位。';
  return '';
}

function invalidRange(quantity: SourcedRange) {
  return [quantity.lower, quantity.upper].some(value => value !== null && !decimal(value)) || (quantity.lower !== null && quantity.upper !== null && Number(quantity.lower) > Number(quantity.upper));
}

function structuredIssue(state: DecisionState): string {
  if (state.options.some(option => !option.label.trim())) return '请填写已添加方案的名称。';
  if (state.objectives.some(objective => !objective.label.trim() || !objective.unit.trim())) return '请填写已添加目标的名称和单位。';
  if (state.constraints.some(constraint => !constraint.label.trim() || !constraint.unit.trim() || !decimal(constraint.threshold))) return '请填写各项硬约束的名称、单位和数值阈值。';
  if (state.scenarios.some(scenario => !scenario.label.trim())) return '请填写已添加情景的名称。';
  if (state.precision_radius !== null && (!decimal(state.precision_radius) || Number(state.precision_radius) < 0)) return '反转检验半径需为非负数。';
  for (const [name, entries] of [['权重', state.weights], ['共享误差', state.shared_offsets]] as const) {
    if (Object.values(entries).some(entry => !decimal(entry.lower) || !decimal(entry.upper) || Number(entry.lower) > Number(entry.upper))) return `请填写有效的${name}区间，或清除该区间。`;
  }
  const quantities: Quantity[] = [
    ...state.options.flatMap(option => [...Object.values(option.measurements), ...Object.values(option.scores)]),
    ...state.scenarios.flatMap(scenario => Object.values(scenario.utilities)),
    ...(state.information?.cost ? [state.information.cost] : []),
  ];
  if (quantities.some(quantity => !quantity.unit.trim() || invalidRange(quantity))) return '请核对已填写数值的单位、下界和上界。';
  if (state.evidence?.some(item => !item.label.trim())) return '请填写已添加证据的名称。';
  if (state.preferences && !completePreference(state.preferences)) return '请填写已添加偏好的名称、内容、适用范围和来源。';
  if (state.information) {
    const information = state.information;
    if (information.signals.some(item => !item.label.trim())) return '请填写已添加信号的名称。';
    const probabilities = [...Object.values(information.prior), ...Object.values(information.likelihoods).flatMap(Object.values)];
    if (probabilities.some(value => invalidRange(value) || [value.lower, value.upper].some(bound => bound != null && (Number(bound) < 0 || Number(bound) > 1)))) return '概率区间须在 0 至 1 之间，下界不得大于上界。';
  }
  if (state.timing) {
    const timing = state.timing;
    const actions = Object.values(timing.actions);
    if ([timing.horizon, timing.decision_deadline, ...actions.map(action => action.cutoff)].some(cutoff => cutoff && (!decimal(cutoff.at) || Number(cutoff.at) < 0))) return '请填写已添加的截止或期限时点。';
    if ([timing.desired_time, timing.predicted_completion, timing.wait_duration, timing.investigation?.cost, timing.investigation?.duration, ...actions.flatMap(action => [action.switching_cost, ...Object.values(action.delay_losses)])].some(value => value && (invalidRange(value) || [value.lower, value.upper].some(bound => bound !== null && Number(bound) < 0)))) return '时机分析的数值区间须为非负数。';
    if (actions.some(action => action.reversibility && !action.reversibility.description.trim())) return '请填写已添加的可逆性说明。';
    if (timing.investigation?.joint.some(row => !row.scenario_id || !row.signal_id || !decimal(row.duration) || !decimal(row.probability)) || Object.values(timing.investigation?.completion_by_state ?? {}).flat().some(row => !decimal(row.duration) || !decimal(row.probability))) return '请完成已添加的调查时长与概率资料。';
  }
  return '';
}

export function DecisionWorkbench({ api: appApi, version }: { api: Api; version: DecisionVersion }) {
  const guided = version === 'v5';
  const view = useRef<AbortController | null>(null);
  useLayoutEffect(() => {
    const controller = new AbortController();
    view.current = controller;
    return () => controller.abort();
  }, []);
  const api: Api = useCallback(<T,>(path: string, body?: unknown, requestVersion?: DecisionVersion) => appApi<T>(path, body, requestVersion, view.current?.signal), [appApi]);
  const [question, setQuestion] = useState('');
  const [draft, setDraft] = useState<Draft | null>(null);
  const [understanding, setUnderstanding] = useState<Understanding | null>(null);
  const [initialQuestions, setInitialQuestions] = useState<Question[]>([]);
  const [initialPlan, setInitialPlan] = useState<WorkflowPlan>();
  const [response, setResponse] = useState<{ state: DecisionState; analysis: Analysis } | null>(null);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState('');
  const [attemptedConfirmation, setAttemptedConfirmation] = useState(false);
  const [retry, setRetry] = useState(0);
  const [scope, setScope] = useState<ResultScope>({ options: 'all', methods: 'all' });
  const startSequence = useRef(0);
  const state = draft?.state ?? null;
  const currentDecisionId = useRef<string | undefined>(undefined);
  useEffect(() => { currentDecisionId.current = state?.decision_id; }, [state?.decision_id]);
  const currentAnalysis = response && response.state === state ? response.analysis : null;
  const analysis = state?.confirmed ? currentAnalysis : null;
  const plan = currentAnalysis?.plan ?? (!state?.confirmed ? initialPlan : undefined);
  const schemaIssue = state ? structuredIssue(state) : '';
  const issue = state ? clarificationIssue(state, guided) || schemaIssue : '';
  const questions = state ? currentAnalysis?.questions ?? initialQuestions.filter(question => missingFields(state)[question.field] !== false) : [];

  function clear(onlyDecisionId?: string) {
    if (onlyDecisionId && currentDecisionId.current !== onlyDecisionId) return;
    startSequence.current += 1;
    setStarting(false);
    setDraft(null);
    setQuestion('');
    setUnderstanding(null);
    setInitialQuestions([]);
    setInitialPlan(undefined);
    setScope({ options: 'all', methods: 'all' });
    setResponse(null);
    setAttemptedConfirmation(false);
    setError('');
  }

  async function start(original: string, demo: boolean) {
    const sequence = ++startSequence.current;
    setStarting(true);
    setError('');
    try {
      const result = await api<StartResponse>(`${decisionPath}/start`, { question: original }, version);
      if (sequence !== startSequence.current) return;
      const incoming = demo ? demoState(result.state) : result.state;
      setDraft({ state: { ...incoming, ...(guided && demo ? { intent: '比较周六出行方案，同时遵守预算上限并权衡时间和舒适度。' } : {}) }, savedRevision: 0, preview: false });
      setUnderstanding(result.understanding);
      setInitialQuestions(result.questions);
      setInitialPlan(result.plan);
    } catch (failure) {
      if (sequence === startSequence.current) setError(failure instanceof Error ? failure.message : '未能开始澄清。');
    } finally {
      if (sequence === startSequence.current) setStarting(false);
    }
  }

  function update(patch: Partial<Omit<DecisionState, 'question' | 'decision_id' | 'revision'>>) {
    setResponse(null);
    setError('');
    setDraft(current => current && ({ ...current, preview: current.state.confirmed, state: { ...current.state, ...patch, revision: Math.max(current.state.revision, current.savedRevision + 1) } }));
  }

  function confirm() {
    setAttemptedConfirmation(true);
    if (!issue) update({ confirmed: true });
  }

  function saved(savedState: DecisionState) {
    setDraft(current => {
      if (!current || current.state.decision_id !== savedState.decision_id) return current;
      const savedRevision = Math.max(current.savedRevision, savedState.revision);
      const latest = current.state === savedState || current.state.revision > savedRevision ? current.state : { ...current.state, revision: savedRevision + 1 };
      return { state: latest, savedRevision, preview: latest !== savedState };
    });
  }

  function load(savedState: DecisionState) {
    clear();
    const state = guided && !savedState.workflow_version ? { ...savedState, workflow_version: '0.5.0' as const, confirmed: false } : savedState;
    setDraft({ state, savedRevision: savedState.revision, preview: false });
  }

  function applyPreference(version: PreferenceVersion) {
    update({ preferences: { ...version.preferences, adopted_version_id: version.version_id } });
  }

  useEffect(() => {
    if (!state || schemaIssue || (!guided && (!state.confirmed || issue))) return;
    let current = true;
    const delay = window.setTimeout(() => {
      api<Analysis>(`${decisionPath}/analyze`, { state }, version).then(result => {
        if (!current) return;
        if (result.decision_id !== state.decision_id || result.revision !== state.revision) {
          setError('返回的分析与当前修订不一致，请重新计算。');
          return;
        }
        setResponse({ state, analysis: result });
      }).catch(failure => {
        if (current) setError(failure instanceof Error ? failure.message : '当前修订分析失败。');
      });
    }, 300);
    return () => { current = false; window.clearTimeout(delay); };
  }, [api, state, issue, schemaIssue, retry, version, guided]);

  return <div className="decision-workbench">
    {guided && <section className="decision-session-note" aria-label="个人会话与本地资料"><p>离开个人工作台会清除本页未保存内容。使用共享设备时，请在离开前结束本地会话。已授权保存的本地记录和下载的备份为明文。</p><a href="?workflow=v04">打开 v0.4 工作台</a></section>}
    {!state && <section className="card decision-entry" aria-labelledby="decision-entry-title">
      <h2 id="decision-entry-title">你正在考虑什么？</h2>
      <p>用自己的话描述要做的选择。我们会逐步核对方案、目标、时限和底线。</p>
      <form onSubmit={event => { event.preventDefault(); if (question.trim()) void start(question, false); }}>
        <label>你的决策问题<textarea autoComplete="off" value={question} required maxLength={6000} placeholder="例如，我该留在当前岗位，还是接受新的工作机会？" onChange={event => setQuestion(event.target.value)}/></label>
        <div className="decision-actions"><button type="submit" disabled={starting || !question.trim()}>开始澄清</button><button type="button" className="quiet" disabled={starting} onClick={() => void start(demoQuestion, true)}>载入虚构示例</button></div>
      </form>
      {starting && <p role="status" className="decision-notice">正在准备澄清问题…</p>}
    </section>}
    {state && <DecisionEditor key={state.decision_id} state={state} understanding={understanding} questions={questions} plan={plan} guided={guided} update={update} confirm={confirm} reset={() => clear()}/>}
    {state && (state.confirmed || attemptedConfirmation) && issue && <p className="error" role="alert">{issue}</p>}
    {error && <div className="error" role="alert"><p>{error}</p>{state?.confirmed && !issue && <button type="button" className="quiet" onClick={() => { setError(''); setRetry(value => value + 1); }}>重新计算</button>}</div>}
    {state?.confirmed && !analysis && !issue && !error && <p role="status" className="decision-notice">正在计算当前修订…</p>}
    {state && analysis && <DecisionResults state={state} analysis={analysis} preview={draft?.preview ?? false} guided={guided} scope={scope} onScope={setScope}/>}
    <DecisionHistory api={api} version={version} state={state} analysis={analysis} savedRevision={draft?.savedRevision ?? 0} onSave={saved} onLoad={load} onClear={clear} onApplyPreference={applyPreference}/>
  </div>;
}
