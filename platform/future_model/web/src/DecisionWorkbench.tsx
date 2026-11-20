import { useEffect, useRef, useState } from 'react';
import { DecisionEditor } from './DecisionEditor';
import { DecisionHistory } from './DecisionHistory';
import { DecisionResults } from './DecisionResults';
import { decisionPath, demoQuestion, demoState } from './decisionTypes';
import type { Analysis, Api, DecisionState, Quantity, Question, StartResponse, Understanding } from './decisionTypes';
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

function draftIssue(state: DecisionState): string {
  if (!state.question.trim()) return '请填写决策问题。';
  if (!state.deadline?.trim()) return '请填写决策时限。没有固定期限时可填「无固定期限」。';
  if (!state.constraints_confirmed) return '请核对并确认硬约束清单。';
  if (state.options.length < 2 || state.options.some(option => !option.label.trim())) return '请填写至少两个方案的名称。';
  if (!state.objectives.length || state.objectives.some(objective => !objective.label.trim() || !objective.unit.trim())) return '请填写至少一个目标及其单位。';
  if (state.constraints.some(constraint => !constraint.label.trim() || !constraint.unit.trim() || !decimal(constraint.threshold))) return '请填写各项硬约束的名称、单位和数值阈值。';
  if (state.scenarios.some(scenario => !scenario.label.trim())) return '请填写已添加情景的名称。';
  if (state.precision_radius !== null && (!decimal(state.precision_radius) || Number(state.precision_radius) < 0)) return '反转检验半径需为非负数。';
  for (const [name, entries] of [['权重', state.weights], ['共享误差', state.shared_offsets]] as const) {
    if (Object.values(entries).some(entry => !decimal(entry.lower) || !decimal(entry.upper) || Number(entry.lower) > Number(entry.upper))) return `请填写有效的${name}区间，或清除该区间。`;
  }
  const quantities: Quantity[] = [
    ...state.options.flatMap(option => [...Object.values(option.measurements), ...Object.values(option.scores)]),
    ...state.scenarios.flatMap(scenario => Object.values(scenario.utilities)),
  ];
  if (quantities.some(quantity => !quantity.unit.trim() || [quantity.lower, quantity.upper].some(value => value !== null && !decimal(value)) || (quantity.lower !== null && quantity.upper !== null && Number(quantity.lower) > Number(quantity.upper)))) return '请核对已填写数值的单位、下界和上界。';
  return '';
}

export function DecisionWorkbench({ api }: { api: Api }) {
  const [question, setQuestion] = useState('');
  const [draft, setDraft] = useState<Draft | null>(null);
  const [understanding, setUnderstanding] = useState<Understanding | null>(null);
  const [initialQuestions, setInitialQuestions] = useState<Question[]>([]);
  const [response, setResponse] = useState<{ state: DecisionState; analysis: Analysis } | null>(null);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState('');
  const [attemptedConfirmation, setAttemptedConfirmation] = useState(false);
  const [retry, setRetry] = useState(0);
  const startSequence = useRef(0);
  const state = draft?.state ?? null;
  const currentDecisionId = useRef<string | undefined>(undefined);
  useEffect(() => { currentDecisionId.current = state?.decision_id; }, [state?.decision_id]);
  const analysis = response && response.state === state ? response.analysis : null;
  const issue = state ? draftIssue(state) : '';
  const questions = state ? analysis?.questions ?? initialQuestions.filter(question => missingFields(state)[question.field] !== false) : [];

  function clear(onlyDecisionId?: string) {
    if (onlyDecisionId && currentDecisionId.current !== onlyDecisionId) return;
    startSequence.current += 1;
    setStarting(false);
    setDraft(null);
    setQuestion('');
    setUnderstanding(null);
    setInitialQuestions([]);
    setResponse(null);
    setAttemptedConfirmation(false);
    setError('');
  }

  async function start(original: string, demo: boolean) {
    const sequence = ++startSequence.current;
    setStarting(true);
    setError('');
    try {
      const result = await api<StartResponse>(`${decisionPath}/start`, { question: original }, 'v4');
      if (sequence !== startSequence.current) return;
      setDraft({ state: demo ? demoState(result.state) : result.state, savedRevision: 0, preview: false });
      setUnderstanding(result.understanding);
      setInitialQuestions(result.questions);
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
    setDraft({ state: savedState, savedRevision: savedState.revision, preview: false });
  }

  useEffect(() => {
    if (!state?.confirmed || issue) return;
    let current = true;
    const delay = window.setTimeout(() => {
      api<Analysis>(`${decisionPath}/analyze`, { state }, 'v4').then(result => {
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
  }, [api, state, issue, retry]);

  return <div className="decision-workbench">
    {!state && <section className="card decision-entry" aria-labelledby="decision-entry-title">
      <h2 id="decision-entry-title">你正在考虑什么？</h2>
      <p>用自己的话描述要做的选择。我们会逐步核对方案、目标、时限和底线。</p>
      <form onSubmit={event => { event.preventDefault(); if (question.trim()) void start(question, false); }}>
        <label>你的决策问题<textarea autoComplete="off" value={question} required maxLength={6000} placeholder="例如，我该留在当前岗位，还是接受新的工作机会？" onChange={event => setQuestion(event.target.value)}/></label>
        <div className="decision-actions"><button type="submit" disabled={starting || !question.trim()}>开始澄清</button><button type="button" className="quiet" disabled={starting} onClick={() => void start(demoQuestion, true)}>载入虚构示例</button></div>
      </form>
      {starting && <p role="status" className="decision-notice">正在准备澄清问题…</p>}
    </section>}
    {state && <DecisionEditor key={state.decision_id} state={state} understanding={understanding} questions={questions} update={update} confirm={confirm} reset={() => clear()}/>}
    {state && (state.confirmed || attemptedConfirmation) && issue && <p className="error" role="alert">{issue}</p>}
    {error && <div className="error" role="alert"><p>{error}</p>{state?.confirmed && !issue && <button type="button" className="quiet" onClick={() => { setError(''); setRetry(value => value + 1); }}>重新计算</button>}</div>}
    {state?.confirmed && !analysis && !issue && !error && <p role="status" className="decision-notice">正在计算当前修订…</p>}
    {state && analysis && <DecisionResults state={state} analysis={analysis} preview={draft?.preview ?? false}/>}
    <DecisionHistory api={api} state={state} analysis={analysis} savedRevision={draft?.savedRevision ?? 0} onSave={saved} onLoad={load} onClear={clear}/>
  </div>;
}
