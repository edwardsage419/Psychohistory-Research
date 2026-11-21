import { useState } from 'react';
import { emptyQuantity, kindLabels, newId } from './decisionTypes';
import type { DecisionState, PlanItem, Quantity, Question, Understanding, ValueKind, WorkflowPlan } from './decisionTypes';
import { DecisionPlan } from './DecisionPlan';
import { InformationFields, IntentFields, PreferenceInput, TimingFields } from './DecisionWorkflowInputs';

const legacySteps = ['问题与时限', '底线与方案', '目标与权重', '评分与误差', '情景与参考'] as const;
const steps = ['决策意图与证据', ...legacySteps, '信息价值', '时机与行动', '决策偏好'] as const;
type Step = typeof steps[number];
type Update = (patch: Partial<Omit<DecisionState, 'question' | 'decision_id' | 'revision' | 'confirmed'>>) => void;
const nullable = (value: string) => value.trim() === '' ? null : value;
const omit = <T,>(entries: Record<string, T>, key: string) => Object.fromEntries(Object.entries(entries).filter(([name]) => name !== key));
const operatorLabels = { '>=': '≥', '>': '>', '<=': '≤', '<': '<' };

function questionStep(field: string): Step {
  if (/^intent$|evidence/i.test(field)) return '决策意图与证据';
  if (/information|probability/i.test(field)) return '信息价值';
  if (/timing|plan_note|intended_option/i.test(field)) return '时机与行动';
  if (/preference/i.test(field)) return '决策偏好';
  if (/scenario|precision|reference/i.test(field)) return '情景与参考';
  if (/score|offset|dependence/i.test(field)) return '评分与误差';
  if (/objective|weight/i.test(field)) return '目标与权重';
  if (/constraint|option|measurement/i.test(field)) return '底线与方案';
  return '问题与时限';
}

function QuantityEditor({ label, value, unit, onChange }: { label: string; value?: Quantity; unit: string; onChange: (value: Quantity) => void }) {
  const quantity = value ?? emptyQuantity(unit);
  const set = (patch: Partial<Quantity>) => onChange({ ...quantity, ...patch });
  return <fieldset className="decision-quantity" data-quantity-label={label}>
    <legend>{label}</legend>
    <div className="decision-fields">
      <label>数据性质<select aria-label={`${label}数据性质`} value={quantity.kind} onChange={event => {
        const kind = event.target.value as ValueKind;
        set(kind === 'unknown' ? { kind, lower: null, upper: null } : { kind });
      }}>{Object.entries(kindLabels).map(([kind, text]) => <option key={kind} value={kind}>{text}</option>)}</select></label>
      <label>下界<input aria-label={`${label}下界`} inputMode="decimal" disabled={quantity.kind === 'unknown'} value={quantity.lower ?? ''} onChange={event => set({ lower: nullable(event.target.value) })}/></label>
      <label>上界<input aria-label={`${label}上界`} inputMode="decimal" disabled={quantity.kind === 'unknown'} value={quantity.upper ?? ''} onChange={event => set({ upper: nullable(event.target.value) })}/></label>
      <label>单位<input aria-label={`${label}单位`} value={quantity.unit} onChange={event => set({ unit: event.target.value })}/></label>
    </div>
    <div className="decision-grid">
      <label>来源或依据<input aria-label={`${label}来源`} value={quantity.source} onChange={event => set({ source: event.target.value })}/></label>
      <label>数据适用时段（可选）<input aria-label={`${label}时段`} value={quantity.horizon ?? ''} onChange={event => set({ horizon: nullable(event.target.value) })}/></label>
    </div>
  </fieldset>;
}

function Dependence({ label, value, source, additional, onChange }: { label: string; value: string; source: string | null; additional: { key: string; label: string }; onChange: (value: string, source: string | null) => void }) {
  return <div className="decision-grid">
    <label>{label}<select value={value} onChange={event => onChange(event.target.value, source)}><option value="unknown">未知</option><option value="rectangle">各区间端点可独立组合（矩形集合）</option><option value={additional.key}>{additional.label}</option></select></label>
    <label>{label}依据<input value={source ?? ''} onChange={event => onChange(value, nullable(event.target.value))}/></label>
  </div>;
}

export function DecisionEditor({ state, questions, understanding, plan, guided, update, confirm, reset }: {
  state: DecisionState; questions: Question[]; understanding: Understanding | null; plan?: WorkflowPlan; guided: boolean; update: Update; confirm: () => void; reset: () => void;
}) {
  const [selection, setStep] = useState<Step>(guided ? '决策意图与证据' : '底线与方案');
  const [showAll, setShowAll] = useState(false);
  const relevant = new Set<Step>(['决策意图与证据', '问题与时限', '底线与方案', '目标与权重']);
  if (state.objectives.length && state.options.length >= 2) relevant.add('评分与误差');
  if (state.scenarios.length || state.information || state.timing) relevant.add('情景与参考');
  if (state.information) relevant.add('信息价值');
  if (state.timing || state.confirmed || state.intended_option_id || state.plan_note) relevant.add('时机与行动');
  if (state.preferences || state.confirmed) relevant.add('决策偏好');
  for (const item of plan?.items ?? []) if (item.priority !== 'DEFERRED') relevant.add(questionStep(item.target.field));
  const visibleSteps = guided ? steps.filter(name => showAll || relevant.has(name)) : legacySteps;
  const step = visibleSteps.some(name => name === selection) ? selection : visibleSteps[0];
  function goTo(next: Step, quantity?: string) {
    if (guided && !relevant.has(next)) setShowAll(true);
    setStep(next);
    requestAnimationFrame(() => {
      const heading = document.getElementById('decision-editor-step');
      const target = quantity && Array.from(document.querySelectorAll<HTMLElement>('[data-quantity-label]')).find(node => node.dataset.quantityLabel === quantity);
      (target ? target.querySelector('select,input') as HTMLElement | null : heading)?.focus();
    });
  }
  function navigate(item: PlanItem) {
    if (item.target.field === 'methods') {
      document.getElementById('decision-methods-title')?.focus();
      return;
    }
    const option = state.options.find(candidate => candidate.id === item.target.option_id);
    const criterion = item.target.field === 'measurements' ? state.constraints.find(entry => entry.id === item.target.constraint_id) : state.objectives.find(entry => entry.id === item.target.objective_id);
    goTo(questionStep(item.target.field), option && criterion ? `${option.label} · ${criterion.label}` : undefined);
  }
  const constraintStep = <>
    <label className="decision-check"><input type="checkbox" checked={state.constraints_confirmed} onChange={event => update({ constraints_confirmed: event.target.checked })}/>我确认底线清单完整（也可确认没有硬约束）</label>
    <h4>硬约束</h4>
    {state.constraints.map((constraint, index) => {
      const set = (patch: Partial<typeof constraint>) => update({ constraints: state.constraints.map(item => item.id === constraint.id ? { ...item, ...patch } : item) });
      return <fieldset className="decision-quantity" key={constraint.id}><legend>{constraint.label || `底线 ${index + 1}`}</legend>
        <div className="decision-fields">
          <label>底线名称<input value={constraint.label} onChange={event => set({ label: event.target.value })}/></label>
          <label>比较符号<select value={constraint.operator} onChange={event => set({ operator: event.target.value as typeof constraint.operator })}>{Object.entries(operatorLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
          <label>阈值<input inputMode="decimal" value={constraint.threshold} onChange={event => set({ threshold: event.target.value })}/></label>
          <label>底线单位<input value={constraint.unit} onChange={event => set({ unit: event.target.value })}/></label>
        </div>
        <div className="decision-grid">
          <label>底线依据<input value={constraint.source} onChange={event => set({ source: event.target.value })}/></label>
          <label>底线适用时段（可选）<input value={constraint.horizon ?? ''} onChange={event => set({ horizon: nullable(event.target.value) })}/></label>
        </div>
        <button type="button" className="quiet" onClick={() => update({
          constraints: state.constraints.filter(item => item.id !== constraint.id),
          options: state.options.map(option => ({ ...option, measurements: omit(option.measurements, constraint.id) })),
        })}>移除底线 {index + 1}</button>
      </fieldset>;
    })}
    <button type="button" className="quiet" onClick={() => update({ constraints: [...state.constraints, { id: newId(), label: '', unit: '', operator: '<=', threshold: '', source: '' }] })}>添加硬约束</button>
    <h4>候选方案</h4>
    {state.options.map((option, index) => {
      const set = (patch: Partial<typeof option>) => update({ options: state.options.map(item => item.id === option.id ? { ...item, ...patch } : item) });
      return <fieldset className="decision-quantity" key={option.id}><legend>{option.label || `方案 ${index + 1}`}</legend>
        <label>方案名称<input value={option.label} onChange={event => set({ label: event.target.value })}/></label>
        {state.constraints.map(constraint => <QuantityEditor key={constraint.id} label={`${option.label || '方案'} · ${constraint.label || '底线'}`} unit={constraint.unit} value={option.measurements[constraint.id]} onChange={value => set({ measurements: { ...option.measurements, [constraint.id]: value } })}/>)}
        <button type="button" className="quiet" onClick={() => update({
          options: state.options.filter(item => item.id !== option.id),
          scenarios: state.scenarios.map(scenario => ({ ...scenario, utilities: omit(scenario.utilities, option.id) })),
          reference_option_id: state.reference_option_id === option.id ? null : state.reference_option_id,
          ...(state.intended_option_id === option.id ? { intended_option_id: null, plan_note: null } : {}),
          ...(state.information ? { information: { ...state.information,
            actions_by_signal: Object.fromEntries(Object.entries(state.information.actions_by_signal).map(([key, values]) => [key, { ...values, option_ids: values.option_ids.filter(id => id !== option.id) }])),
            fixed_policy: Object.fromEntries(Object.entries(state.information.fixed_policy ?? {}).filter(([, id]) => id !== option.id)),
          } } : {}),
          ...(state.timing ? { timing: { ...state.timing, actions: omit(state.timing.actions, option.id),
            status_quo_option_id: state.timing.status_quo_option_id === option.id ? null : state.timing.status_quo_option_id,
            fallback_option_id: state.timing.fallback_option_id === option.id ? null : state.timing.fallback_option_id,
          } } : {}),
        })}>移除方案 {index + 1}</button>
      </fieldset>;
    })}
    <button type="button" className="quiet" onClick={() => update({ options: [...state.options, { id: newId(), label: '', measurements: {}, scores: {} }] })}>添加候选方案</button>
  </>;
  const objectiveStep = <>
    <p className="muted">权重区间采用 0 至 1。可留下未知权重，让方法按自己的适用条件判断。</p>
    <label className="decision-check"><input type="checkbox" checked={state.weights_confirmed} onChange={event => update({ weights_confirmed: event.target.checked })}/>我确认使用下列权重区间</label>
    {state.objectives.map((objective, index) => {
      const set = (patch: Partial<typeof objective>) => update({ objectives: state.objectives.map(item => item.id === objective.id ? { ...item, ...patch } : item) });
      const weight = state.weights[objective.id] ?? { lower: '', upper: '' };
      return <fieldset className="decision-quantity" key={objective.id}><legend>{objective.label || `目标 ${index + 1}`}</legend>
        <div className="decision-grid">
          <label>目标名称<input value={objective.label} onChange={event => set({ label: event.target.value })}/></label>
          <label>目标单位<input value={objective.unit} onChange={event => set({ unit: event.target.value })}/></label>
          <label>目标方向<select value={objective.direction} onChange={event => set({ direction: event.target.value as typeof objective.direction })}><option value="max">越大越好</option><option value="min">越小越好</option></select></label>
          <div className="decision-grid">
            <label>{objective.label || `目标 ${index + 1}`}权重下界<input inputMode="decimal" value={weight.lower} onChange={event => update({ weights: { ...state.weights, [objective.id]: { ...weight, lower: event.target.value } } })}/></label>
            <label>{objective.label || `目标 ${index + 1}`}权重上界<input inputMode="decimal" value={weight.upper} onChange={event => update({ weights: { ...state.weights, [objective.id]: { ...weight, upper: event.target.value } } })}/></label>
          </div>
        </div>
        <div className="decision-actions">
          {state.weights[objective.id] && <button type="button" className="quiet" onClick={() => update({ weights: omit(state.weights, objective.id), weights_confirmed: false })}>清除 {objective.label} 权重</button>}
          <button type="button" className="quiet" onClick={() => update({
            objectives: state.objectives.filter(item => item.id !== objective.id), weights: omit(state.weights, objective.id), shared_offsets: omit(state.shared_offsets, objective.id),
            options: state.options.map(option => ({ ...option, scores: omit(option.scores, objective.id) })),
          })}>移除目标 {index + 1}</button>
        </div>
      </fieldset>;
    })}
    <button type="button" className="quiet" onClick={() => update({ objectives: [...state.objectives, { id: newId(), label: '', unit: '', direction: 'max' }] })}>添加目标</button>
  </>;
  const scoreStep = <>
    <label>评分量表与比较依据<input value={state.score_basis ?? ''} onChange={event => update({ score_basis: nullable(event.target.value) })}/></label>
    <Dependence label="评分误差依赖" additional={{ key: 'shared_additive', label: '同一目标的误差为共享加性偏移' }} value={state.score_dependence} source={state.score_dependence_source} onChange={(score_dependence, score_dependence_source) => update({ score_dependence, score_dependence_source })}/>
    {!state.options.length || !state.objectives.length ? <p className="muted">添加方案和目标后可填写评分区间。</p> : state.options.map(option => <fieldset className="decision-quantity" key={option.id}>
      <legend>{option.label || '未命名方案'}</legend>
      {state.objectives.map(objective => <QuantityEditor key={objective.id} label={`${option.label || '方案'} · ${objective.label || '目标'}`} unit={objective.unit} value={option.scores[objective.id]} onChange={value => update({ options: state.options.map(item => item.id === option.id ? { ...item, scores: { ...item.scores, [objective.id]: value } } : item) })}/>)}
    </fieldset>)}
    <details className="decision-disclosure"><summary>共享误差与评分变换</summary>
      <div className="decision-grid">
        <label>评分变换<select value={state.score_transform} onChange={event => update({ score_transform: event.target.value })}><option value="unknown">未知</option><option value="identity">保留原评分</option><option value="clip_01">截断到 0 至 1</option></select></label>
        <label>共享误差跨目标依赖<select value={state.shared_offset_dependence} onChange={event => update({ shared_offset_dependence: event.target.value })}><option value="unknown">未知</option><option value="rectangle">矩形集合</option></select></label>
      </div>
      {state.objectives.map((objective, index) => {
        const label = objective.label || `目标 ${index + 1}`;
        const bounds = state.shared_offsets[objective.id] ?? { lower: '', upper: '' };
        const set = (patch: Partial<typeof bounds>) => update({ shared_offsets: { ...state.shared_offsets, [objective.id]: { ...bounds, ...patch } } });
        return <fieldset className="decision-quantity" key={objective.id}>
          <legend>{label} · 共享误差</legend>
          <div className="decision-grid">
            <label>{label}共享误差下界<input inputMode="decimal" value={bounds.lower} onChange={event => set({ lower: event.target.value })}/></label>
            <label>{label}共享误差上界<input inputMode="decimal" value={bounds.upper} onChange={event => set({ upper: event.target.value })}/></label>
          </div>
          {state.shared_offsets[objective.id] && <button type="button" className="quiet" onClick={() => update({ shared_offsets: omit(state.shared_offsets, objective.id) })}>清除 {label} 共享误差</button>}
        </fieldset>;
      })}
    </details>
  </>;
  const scenarioStep = <>
    <label>情景效用的共同量表<input value={state.scenario_basis ?? ''} onChange={event => update({ scenario_basis: nullable(event.target.value) })}/></label>
    <Dependence label="情景效用依赖" additional={{ key: 'constrained', label: '区间端点受共同条件限制' }} value={state.scenario_dependence} source={state.scenario_dependence_source} onChange={(scenario_dependence, scenario_dependence_source) => update({ scenario_dependence, scenario_dependence_source })}/>
    <div className="decision-grid">
      <label>反转检验半径<input inputMode="decimal" value={state.precision_radius ?? ''} onChange={event => update({ precision_radius: nullable(event.target.value) })}/></label>
      <label>参考方案<select value={state.reference_option_id ?? ''} onChange={event => update({ reference_option_id: nullable(event.target.value) })}><option value="">未指定</option>{state.options.map(option => <option key={option.id} value={option.id}>{option.label || '未命名方案'}</option>)}</select></label>
    </div>
    {state.scenarios.map((scenario, index) => {
      const set = (patch: Partial<typeof scenario>) => update({ scenarios: state.scenarios.map(item => item.id === scenario.id ? { ...item, ...patch } : item) });
      return <fieldset className="decision-quantity" key={scenario.id}><legend>{scenario.label || `情景 ${index + 1}`}</legend>
        <div className="decision-grid">
          <label>情景名称<input value={scenario.label} onChange={event => set({ label: event.target.value })}/></label>
          <label>情景性质<select value={scenario.kind} onChange={event => set({ kind: event.target.value as ValueKind })}>{Object.entries(kindLabels).map(([kind, text]) => <option key={kind} value={kind}>{text}</option>)}</select></label>
        </div>
        <label>情景来源或假设<input value={scenario.source} onChange={event => set({ source: event.target.value })}/></label>
        {state.options.map(option => <QuantityEditor key={option.id} label={`${scenario.label || '情景'} · ${option.label || '方案'}效用`} unit="效用" value={scenario.utilities[option.id]} onChange={value => set({ utilities: { ...scenario.utilities, [option.id]: value } })}/>)}
        <button type="button" className="quiet" onClick={() => update({
          scenarios: state.scenarios.filter(item => item.id !== scenario.id),
          ...(state.information ? { information: { ...state.information, prior: omit(state.information.prior, scenario.id), likelihoods: omit(state.information.likelihoods, scenario.id) } } : {}),
          ...(state.timing ? { timing: { ...state.timing,
            actions: Object.fromEntries(Object.entries(state.timing.actions).map(([key, value]) => [key, { ...value, delay_losses: omit(value.delay_losses, scenario.id) }])),
            investigation: state.timing.investigation && { ...state.timing.investigation, joint: state.timing.investigation.joint.filter(row => row.scenario_id !== scenario.id), completion_by_state: omit(state.timing.investigation.completion_by_state, scenario.id) },
          } } : {}),
        })}>移除情景 {index + 1}</button>
      </fieldset>;
    })}
    <button type="button" className="quiet" onClick={() => update({ scenarios: [...state.scenarios, { id: newId(), label: '', utilities: {}, kind: 'unknown', source: '', probability: null }] })}>添加情景</button>
  </>;

  return <section className="card decision-editor" aria-labelledby="decision-clarify-title">
    <div className="decision-section-heading"><div><h2 id="decision-clarify-title">澄清与确认</h2><p className="decision-question">{state.question}</p></div><span className="pill">{state.confirmed ? `已确认 · 修订 ${state.revision}` : '待核对'}</span></div>
    {understanding?.message && <p>{understanding.message}</p>}
    {!!understanding?.suggestions?.length && <div className="decision-prompts">
      <h3>从原文提取的候选信息</h3>
      <ul>{understanding.suggestions.map((suggestion, index) => <li key={`${suggestion.field}-${index}`}>
        <span>{suggestion.value} · {suggestion.source}</span>
        {suggestion.field === 'options' && <button type="button" className="text-button" disabled={state.options.some(option => option.label === suggestion.value)} onClick={() => {
          update({ options: [...state.options, { id: newId(), label: suggestion.value, measurements: {}, scores: {} }] });
          goTo('底线与方案');
        }}>采用为方案</button>}
      </li>)}</ul>
    </div>}
    {guided && plan && <DecisionPlan plan={plan} navigate={navigate}/>}
    {(!guided || !plan) && questions.length > 0 && <div className="decision-prompts"><h3>接下来请补充</h3><ol>{questions.map((question, index) => <li key={`${question.field}-${index}`}><span>{question.prompt}</span><button type="button" className="text-button" onClick={() => goTo(questionStep(question.field))}>填写{questionStep(question.field)}</button></li>)}</ol></div>}
    <nav className="decision-steps" aria-label="决策编辑步骤">{visibleSteps.map(name => <button type="button" key={name} className={step === name ? 'selected' : ''} aria-current={step === name ? 'step' : undefined} onClick={() => goTo(name)}>{name}</button>)}</nav>
    {guided && <button type="button" className="text-button decision-show-tools" aria-expanded={showAll} onClick={() => setShowAll(value => !value)}>{showAll ? '收起非相关编辑项' : '显示全部编辑项'}</button>}
    <div className="decision-edit-area"><h3 id="decision-editor-step" tabIndex={-1}>{step}</h3>
      {step === '问题与时限' && <>
        <label>决策问题<textarea value={state.question} readOnly/></label>
        <label>决策时限<input value={state.deadline ?? ''} placeholder="例如 周五晚，或 2026-12-01" onChange={event => update({ deadline: nullable(event.target.value) })}/></label>
      </>}
      {step === '底线与方案' && constraintStep}
      {step === '目标与权重' && objectiveStep}
      {step === '评分与误差' && scoreStep}
      {step === '情景与参考' && scenarioStep}
      {step === '决策意图与证据' && <IntentFields state={state} update={update}/>}
      {step === '信息价值' && <InformationFields state={state} update={update}/>}
      {step === '时机与行动' && <TimingFields state={state} update={update}/>}
      {step === '决策偏好' && <PreferenceInput state={state} update={update}/>}
    </div>
    <div className="decision-actions decision-editor-actions">
      {!state.confirmed && <button type="button" onClick={confirm} disabled={!state.question.trim()}>确认并分析</button>}
      {state.confirmed && <span className="muted">修改后自动计算预览，保存时确认当前修订。</span>}
      <button type="button" className="quiet" onClick={reset}>开始新决策</button>
    </div>
  </section>;
}
