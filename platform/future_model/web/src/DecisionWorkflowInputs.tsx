import { useState } from 'react';
import { emptyQuantity, kindLabels, newId } from './decisionTypes';
import type { Cutoff, DecisionState, EvidenceItem, InformationInput, Investigation, PreferenceSnapshot, SourcedRange, TimingAction, TimingInput, ValueKind } from './decisionTypes';

export const emptyRange: SourcedRange = { lower: null, upper: null, kind: 'unknown', source: '' };
const emptyAction: TimingAction = { cutoff: null, switching_cost: null, delay_losses: {}, reversibility: null };
const emptyInformation: InformationInput = { signals: [], prior: {}, likelihoods: {}, cost: null, actions_by_signal: {}, unrestricted_actions: false, action_source: '', parameter_domain: 'unknown', parameter_domain_source: '', timing_basis: null, fixed_policy: {}, verification_source: null };
const emptyTiming: TimingInput = { confirmed: false, time_unit: null, time_origin: null, horizon: null, decision_deadline: null, desired_time: null, predicted_completion: null, wait_duration: null, actions: {}, status_quo_option_id: null, fallback_option_id: null, investigation: null };
const emptyInvestigation: Investigation = { mode: 'deterministic', cost: null, duration: null, kind: 'unknown', source: '', joint: [], completion_by_state: {} };
export const emptyPreference = (): PreferenceSnapshot => ({ values: [{ label: '', value: '' }], applicability: '', provenance: '', adopted_version_id: null });
export const completePreference = (preference: PreferenceSnapshot) => !!preference.applicability.trim() && !!preference.provenance.trim() && !!preference.values.length && preference.values.every(value => value.label.trim() && value.value.trim());
export const without = <T,>(entries: Record<string, T>, id: string) => Object.fromEntries(Object.entries(entries).filter(([key]) => key !== id));
type Update = (patch: Partial<Omit<DecisionState, 'question' | 'decision_id' | 'revision' | 'confirmed'>>) => void;
const nullable = (value: string) => value.trim() ? value : null;

function Kind({ label, value, onChange }: { label: string; value: ValueKind; onChange: (value: ValueKind) => void }) {
  return <label>{label}<select value={value} onChange={event => onChange(event.target.value as ValueKind)}>{Object.entries(kindLabels).map(([kind, name]) => <option key={kind} value={kind}>{name}</option>)}</select></label>;
}

function Range({ name, value, onChange, unit, clearable = false }: { name: string; value?: SourcedRange | null; onChange: (value: SourcedRange | null) => void; unit?: string; clearable?: boolean }) {
  const current = value ?? emptyRange;
  const change = (patch: Partial<SourcedRange>) => onChange({ ...current, ...patch });
  return <fieldset className="decision-quantity"><legend>{name}{unit && `（${unit}）`}</legend>
    <div className="decision-fields">
      <Kind label={`${name}数据性质`} value={current.kind} onChange={kind => change(kind === 'unknown' ? { kind, lower: null, upper: null } : { kind })}/>
      <label>{name}下界<input inputMode="decimal" disabled={current.kind === 'unknown'} value={current.lower ?? ''} onChange={event => change({ lower: nullable(event.target.value) })}/></label>
      <label>{name}上界<input inputMode="decimal" disabled={current.kind === 'unknown'} value={current.upper ?? ''} onChange={event => change({ upper: nullable(event.target.value) })}/></label>
      <label>{name}来源<input value={current.source} onChange={event => change({ source: event.target.value })}/></label>
    </div>
    {clearable && value && <button type="button" className="quiet" onClick={() => onChange(null)}>清除{name}</button>}
  </fieldset>;
}

function CutoffEditor({ name, value, onChange }: { name: string; value: Cutoff | null; onChange: (value: Cutoff | null) => void }) {
  const change = (patch: Partial<Cutoff>) => onChange({ at: '', inclusive: true, kind: 'unknown', source: '', ...value, ...patch });
  return <fieldset className="decision-quantity"><legend>{name}</legend><div className="decision-fields">
    <label>{name}时点<input inputMode="decimal" value={value?.at ?? ''} onChange={event => change({ at: event.target.value })}/></label>
    <Kind label={`${name}数据性质`} value={value?.kind ?? 'unknown'} onChange={kind => change({ kind })}/>
    <label>{name}来源<input value={value?.source ?? ''} onChange={event => change({ source: event.target.value })}/></label>
    <label className="decision-check"><input type="checkbox" checked={value?.inclusive ?? true} onChange={event => change({ inclusive: event.target.checked })}/>{name}包含端点</label>
  </div>{value && <button type="button" className="quiet" onClick={() => onChange(null)}>清除{name}</button>}</fieldset>;
}

export function PreferenceFields({ value, change }: { value: PreferenceSnapshot; change: (value: PreferenceSnapshot) => void }) {
  const update = (patch: Partial<PreferenceSnapshot>) => change({ ...value, ...patch, adopted_version_id: null });
  return <>
    <div className="decision-grid"><label>偏好适用范围<input value={value.applicability} onChange={event => update({ applicability: event.target.value })}/></label><label>偏好来源<input value={value.provenance} onChange={event => update({ provenance: event.target.value })}/></label></div>
    {value.values.map((item, index) => <fieldset className="decision-quantity" key={index}><legend>偏好 {index + 1}</legend><div className="decision-grid">
      <label>偏好名称<input value={item.label} onChange={event => update({ values: value.values.map((entry, i) => i === index ? { ...entry, label: event.target.value } : entry) })}/></label>
      <label>偏好内容<input value={item.value} onChange={event => update({ values: value.values.map((entry, i) => i === index ? { ...entry, value: event.target.value } : entry) })}/></label>
    </div><button type="button" className="quiet" onClick={() => update({ values: value.values.filter((_, i) => i !== index) })}>移除偏好 {index + 1}</button></fieldset>)}
    <button type="button" className="quiet" onClick={() => update({ values: [...value.values, { label: '', value: '' }] })}>添加偏好条目</button>
  </>;
}

export function IntentFields({ state, update }: { state: DecisionState; update: Update }) {
  const evidence = state.evidence ?? [];
  return <>
    <label>决策意图<textarea value={state.intent ?? ''} maxLength={400} placeholder="例如，确定接下来三个月内是否换岗，并保留目前岗位作为可行选项。" onChange={event => update({ intent: nullable(event.target.value) })}/></label>
    <h4>证据与待核实信息</h4><p className="muted">填写你掌握的来源和适用范围，注明哪些信息仍待核实。</p>
    {evidence.map((item, index) => {
      const change = (patch: Partial<EvidenceItem>) => update({ evidence: evidence.map(entry => entry.id === item.id ? { ...entry, ...patch } : entry) });
      return <fieldset className="decision-quantity" key={item.id}><legend>{item.label || `证据 ${index + 1}`}</legend><div className="decision-grid">
        <label>证据名称<input value={item.label} onChange={event => change({ label: event.target.value })}/></label>
        <Kind label="证据性质" value={item.kind} onChange={kind => change({ kind })}/>
        <label>证据来源<input value={item.source} onChange={event => change({ source: event.target.value })}/></label>
        <label>证据适用范围<input value={item.scope} onChange={event => change({ scope: event.target.value })}/></label>
        <label>证据核实状态<select value={item.verification} onChange={event => change({ verification: event.target.value as EvidenceItem['verification'] })}><option value="unverified">待核实</option><option value="user_supplied">用户提供</option><option value="user_confirmed">用户已核实</option></select></label>
      </div><button type="button" className="quiet" onClick={() => update({ evidence: evidence.filter(entry => entry.id !== item.id) })}>移除证据 {index + 1}</button></fieldset>;
    })}
    <button type="button" className="quiet" onClick={() => update({ evidence: [...evidence, { id: newId(), label: '', kind: 'unknown', source: '', verification: 'unverified', scope: '' }] })}>添加证据</button>
  </>;
}

export function InformationFields({ state, update }: { state: DecisionState; update: Update }) {
  const information = state.information;
  if (!information) return <><p>如果先获取一项信息可能改变行动，可以比较调查及其成本。</p><button type="button" onClick={() => update({ information: emptyInformation })}>启用信息价值分析</button></>;
  const set = (patch: Partial<InformationInput>) => update({ information: { ...information, ...patch } });
  return <>
    <p className="muted">概率须填写来源。留空的概率继续显示为未知，同时仍可计算适用的非概率比较。</p>
    <div className="decision-grid">
      <label>概率参数依赖<select value={information.parameter_domain} onChange={event => set({ parameter_domain: event.target.value as InformationInput['parameter_domain'] })}><option value="unknown">未知</option><option value="rectangle">各概率行可独立组合（每行合计为 1）</option><option value="constrained">参数受共同条件限制</option></select></label>
      <label>概率参数依赖依据<input value={information.parameter_domain_source} onChange={event => set({ parameter_domain_source: event.target.value })}/></label>
      <label>调查不改变行动时机的依据<input value={information.timing_basis ?? ''} onChange={event => set({ timing_basis: nullable(event.target.value) })}/></label>
      <label>点概率核验证据（可选）<input value={information.verification_source ?? ''} onChange={event => set({ verification_source: nullable(event.target.value) })}/></label>
      <label>调查成本单位<input value={information.cost?.unit ?? ''} onChange={event => set({ cost: { ...(information.cost ?? emptyQuantity('效用')), unit: event.target.value } })}/></label>
    </div>
    <Range name="调查成本" value={information.cost} clearable onChange={value => set({ cost: value && { ...value, unit: information.cost?.unit || '效用' } })}/>
    <label className="decision-check"><input type="checkbox" checked={information.unrestricted_actions} onChange={event => set({ unrestricted_actions: event.target.checked })}/>所有通过硬约束的方案在收到信号后仍可选择</label>
    <label>调查后行动可用性依据<input value={information.action_source} onChange={event => set({ action_source: event.target.value })}/></label>
    {information.unrestricted_actions && Object.keys(information.actions_by_signal).length > 0 && <p className="muted">共同方案与逐信号方案同时存在。请选择一种行动范围，再比较调查价值。</p>}
    <h4>信号与后续行动</h4>
    {information.signals.map((signal, index) => {
      const available = information.actions_by_signal[signal.id] ?? { option_ids: [], kind: 'unknown', source: '' };
      const name = signal.label || `信号 ${index + 1}`;
      const setAvailable = (patch: Partial<typeof available>) => set({ actions_by_signal: { ...information.actions_by_signal, [signal.id]: { ...available, ...patch } } });
      return <fieldset className="decision-quantity" key={signal.id}><legend>{name}</legend>
        <label>信号名称<input value={signal.label} onChange={event => set({ signals: information.signals.map(entry => entry.id === signal.id ? { ...entry, label: event.target.value } : entry) })}/></label>
        {(!information.unrestricted_actions || information.actions_by_signal[signal.id]) && <>
          <div className="decision-grid"><Kind label={`${name}可用行动证据性质`} value={available.kind} onChange={kind => setAvailable({ kind })}/><label>{name}可用行动来源<input value={available.source} onChange={event => setAvailable({ source: event.target.value })}/></label></div>
          {state.options.map(option => <label key={option.id} className="decision-check"><input type="checkbox" checked={available.option_ids.includes(option.id)} onChange={event => setAvailable({ option_ids: event.target.checked ? [...available.option_ids, option.id] : available.option_ids.filter(id => id !== option.id) })}/>{name}后可选择{option.label}</label>)}
          {information.actions_by_signal[signal.id] && <button type="button" className="quiet" onClick={() => set({ actions_by_signal: without(information.actions_by_signal, signal.id) })}>清除{name}可用行动范围</button>}
        </>}
        <label>{name}固定策略<select value={information.fixed_policy?.[signal.id] ?? ''} onChange={event => set({ fixed_policy: event.target.value ? { ...information.fixed_policy, [signal.id]: event.target.value } : without(information.fixed_policy ?? {}, signal.id) })}><option value="">暂不指定</option>{state.options.map(option => <option key={option.id} value={option.id}>{option.label}</option>)}</select></label>
        <button type="button" className="quiet" onClick={() => {
          update({ information: { ...information, signals: information.signals.filter(entry => entry.id !== signal.id), actions_by_signal: without(information.actions_by_signal, signal.id), likelihoods: Object.fromEntries(Object.entries(information.likelihoods).map(([key, values]) => [key, without(values, signal.id)])), fixed_policy: without(information.fixed_policy ?? {}, signal.id) },
            ...(state.timing?.investigation ? { timing: { ...state.timing, investigation: { ...state.timing.investigation, joint: state.timing.investigation.joint.filter(row => row.signal_id !== signal.id) } } } : {}) });
        }}>移除信号 {index + 1}</button>
      </fieldset>;
    })}
    <button type="button" className="quiet" onClick={() => set({ signals: [...information.signals, { id: newId(), label: '' }] })}>添加信号</button>
    <h4>情景概率与信号条件概率</h4>
    {!state.scenarios.length && <p className="muted">先在「情景与参考」添加情景，随后填写先验和条件概率。</p>}
    {state.scenarios.map(scenario => <fieldset className="decision-quantity" key={scenario.id}><legend>{scenario.label}</legend>
      <Range name={`${scenario.label}先验概率`} value={information.prior[scenario.id]} onChange={value => set({ prior: value ? { ...information.prior, [scenario.id]: value } : without(information.prior, scenario.id) })}/>
      {information.signals.map(signal => <Range key={signal.id} name={`${scenario.label} · ${signal.label}条件概率`} value={information.likelihoods[scenario.id]?.[signal.id]} onChange={value => {
        const row = information.likelihoods[scenario.id] ?? {};
        set({ likelihoods: { ...information.likelihoods, [scenario.id]: value ? { ...row, [signal.id]: value } : without(row, signal.id) } });
      }}/>)}</fieldset>)}
    <button type="button" className="quiet" onClick={() => update({ information: null })}>移除本次信息价值输入</button>
  </>;
}

function ActionSelection({ label, state, value, change }: { label: string; state: DecisionState; value: string | null; change: (value: string | null) => void }) {
  return <label>{label}<select value={value ?? ''} onChange={event => change(nullable(event.target.value))}><option value="">暂不指定</option>{state.options.map(option => <option key={option.id} value={option.id}>{option.label}</option>)}</select></label>;
}

function PlanChoice({ state, update }: { state: DecisionState; update: Update }) {
  const [option, setOption] = useState(state.intended_option_id ?? null);
  const [note, setNote] = useState(state.plan_note ?? '');
  return <fieldset className="decision-quantity"><legend>我的行动计划</legend><div className="decision-grid">
    <ActionSelection label="计划选择" state={state} value={option} change={setOption}/>
    <label>行动计划说明<input value={note} onChange={event => setNote(event.target.value)}/></label>
  </div><div className="decision-actions">
    <button type="button" disabled={!option && !note.trim()} onClick={() => update({ intended_option_id: option, plan_note: nullable(note) })}>确认行动计划</button>
    {(state.intended_option_id || state.plan_note) && <button type="button" className="quiet" onClick={() => { setOption(null); setNote(''); update({ intended_option_id: null, plan_note: null }); }}>清除行动计划</button>}
  </div>{(state.intended_option_id || state.plan_note) && <p role="status">已确认计划：{state.options.find(option => option.id === state.intended_option_id)?.label}{state.plan_note && ` · ${state.plan_note}`}</p>}<p className="muted">实际采取行动后，在本地记录中填写发生的事实。</p></fieldset>;
}

export function TimingFields({ state, update }: { state: DecisionState; update: Update }) {
  const timing = state.timing;
  if (!timing) return <><PlanChoice state={state} update={update}/><p>如果等候、调查或错过截止时点会改变选择，可以比较行动时机。</p><button type="button" onClick={() => update({ timing: emptyTiming })}>启用时机分析</button></>;
  const set = (patch: Partial<TimingInput>) => update({ timing: { ...timing, ...patch } });
  const investigation = timing.investigation;
  const setInvestigation = (patch: Partial<Investigation>) => set({ investigation: { ...emptyInvestigation, ...investigation, ...patch } });
  const recordRange = (field: 'desired_time' | 'predicted_completion' | 'wait_duration') => (value: SourcedRange | null) => set({ [field]: value });
  return <>
    <PlanChoice state={state} update={update}/>
    <div className="decision-grid"><label>时机单位<input value={timing.time_unit ?? ''} onChange={event => set({ time_unit: nullable(event.target.value) })}/></label><label>时间原点<input value={timing.time_origin ?? ''} onChange={event => set({ time_origin: nullable(event.target.value) })}/></label>
      <ActionSelection label="维持现状方案" state={state} value={timing.status_quo_option_id} change={status_quo_option_id => set({ status_quo_option_id })}/>
      <ActionSelection label="备用方案" state={state} value={timing.fallback_option_id} change={fallback_option_id => set({ fallback_option_id })}/>
    </div>
    <p className="muted">固定等待期间不获得新信息。调查需等到完成，之后根据收到的信号和实际完成时点选择。方案填写了时机规则但无单独截止时点时，只使用共同期限。切换成本采用情景效用单位，延迟损失按每个时间单位填写。</p>
    <label className="decision-check"><input type="checkbox" checked={timing.confirmed} onChange={event => set({ confirmed: event.target.checked })}/>确认时机假设</label>
    <CutoffEditor name="分析期限" value={timing.horizon} onChange={horizon => set({ horizon })}/>
    <CutoffEditor name="决策截止" value={timing.decision_deadline} onChange={decision_deadline => set({ decision_deadline })}/>
    <Range name="希望行动时点" value={timing.desired_time} onChange={recordRange('desired_time')} clearable/>
    <Range name="预计完成时点" value={timing.predicted_completion} onChange={recordRange('predicted_completion')} clearable/>
    <Range name="等待时长" value={timing.wait_duration} onChange={recordRange('wait_duration')} clearable/>
    <h4>各方案的有效期限、切换和延迟代价</h4>
    {state.options.map(option => {
      const action = timing.actions[option.id] ?? emptyAction;
      const updateAction = (patch: Partial<TimingAction>) => set({ actions: { ...timing.actions, [option.id]: { ...action, ...patch } } });
      const reversible = action.reversibility ?? { description: '', kind: 'unknown' as const, source: '' };
      return <details className="decision-disclosure" key={option.id}><summary>{option.label}的行动时机</summary>
        <CutoffEditor name={`${option.label}截止`} value={action.cutoff} onChange={cutoff => updateAction({ cutoff })}/>
        <Range name={`${option.label}切换成本`} value={action.switching_cost} onChange={switching_cost => updateAction({ switching_cost })} clearable/>
        <div className="decision-grid"><label>{option.label}可逆性说明<input value={reversible.description} onChange={event => updateAction({ reversibility: { ...reversible, description: event.target.value } })}/></label><Kind label={`${option.label}可逆性数据性质`} value={reversible.kind} onChange={kind => updateAction({ reversibility: { ...reversible, kind } })}/><label>{option.label}可逆性来源<input value={reversible.source} onChange={event => updateAction({ reversibility: { ...reversible, source: event.target.value } })}/></label></div>
        {action.reversibility && <button type="button" className="quiet" onClick={() => updateAction({ reversibility: null })}>清除{option.label}可逆性</button>}
        {state.scenarios.map(scenario => <Range key={scenario.id} name={`${option.label} · ${scenario.label}延迟损失`} value={action.delay_losses[scenario.id]} onChange={value => updateAction({ delay_losses: value ? { ...action.delay_losses, [scenario.id]: value } : without(action.delay_losses, scenario.id) })} clearable/>)}
        {timing.actions[option.id] && <button type="button" className="quiet" onClick={() => set({ actions: without(timing.actions, option.id) })}>清除{option.label}行动时机</button>}
      </details>;
    })}
    <h4>调查时机</h4>
    {state.information && <p className="muted">请在「信息价值」确认收到信号后仍可选择的行动，并填写依据。</p>}
    {!investigation && <button type="button" className="quiet" onClick={() => set({ investigation: emptyInvestigation })}>添加调查时机</button>}
    {investigation && <>
      <div className="decision-grid">
        <label>调查完成模型<select value={investigation.mode} onChange={event => setInvestigation({ mode: event.target.value as Investigation['mode'] })}><option value="deterministic">确定完成时长</option><option value="joint">情景、信号、时长的联合分布</option><option value="conditional">按情景的完成时长分布</option></select></label>
        <Kind label="调查时机数据性质" value={investigation.kind} onChange={kind => setInvestigation({ kind })}/>
        <label>调查时机依据<input value={investigation.source} onChange={event => setInvestigation({ source: event.target.value })}/></label>
      </div>
      <Range name="时机分析中的调查成本" value={investigation.cost} onChange={cost => setInvestigation({ cost })} clearable/>
      {investigation.mode === 'deterministic' && <Range name="确定调查时长" value={investigation.duration} onChange={duration => setInvestigation({ duration })} clearable/>}
      {investigation.mode === 'joint' && <>
        <datalist id="decision-joint-signals">{state.information?.signals.map(signal => <option key={signal.id} value={signal.id}>{signal.label}</option>)}</datalist>
        {investigation.joint.map((row, index) => {
          const setRow = (patch: Partial<typeof row>) => setInvestigation({ joint: investigation.joint.map((entry, i) => i === index ? { ...entry, ...patch } : entry) });
          return <fieldset className="decision-quantity" key={index}><legend>联合分布行 {index + 1}</legend><div className="decision-fields">
            <label>关联情景<select value={row.scenario_id} onChange={event => setRow({ scenario_id: event.target.value })}><option value="">选择情景</option>{state.scenarios.map(scenario => <option key={scenario.id} value={scenario.id}>{scenario.label}</option>)}</select></label>
            <label>关联信号<input value={row.signal_id} list="decision-joint-signals" pattern="[A-Za-z0-9_\-]{1,48}" onChange={event => setRow({ signal_id: event.target.value })}/></label>
            <label>联合时长<input inputMode="decimal" value={row.duration} onChange={event => setRow({ duration: event.target.value })}/></label>
            <label>联合概率<input inputMode="decimal" value={row.probability} onChange={event => setRow({ probability: event.target.value })}/></label>
          </div><button type="button" className="quiet" onClick={() => setInvestigation({ joint: investigation.joint.filter((_, i) => i !== index) })}>移除联合分布行 {index + 1}</button></fieldset>;
        })}
        <button type="button" className="quiet" onClick={() => setInvestigation({ joint: [...investigation.joint, { scenario_id: '', signal_id: '', duration: '', probability: '' }] })}>添加联合分布行</button>
      </>}
      {investigation.mode === 'conditional' && state.scenarios.map(scenario => {
        const entries = investigation.completion_by_state[scenario.id] ?? [];
        const setRows = (rows: typeof entries) => setInvestigation({ completion_by_state: { ...investigation.completion_by_state, [scenario.id]: rows } });
        return <fieldset className="decision-quantity" key={scenario.id}><legend>{scenario.label}完成分布</legend>
          {entries.map((row, index) => <div key={index} className="decision-grid">
            <label>{scenario.label}完成时长<input inputMode="decimal" value={row.duration} onChange={event => setRows(entries.map((value, i) => i === index ? { ...value, duration: event.target.value } : value))}/></label>
            <label>{scenario.label}完成概率<input inputMode="decimal" value={row.probability} onChange={event => setRows(entries.map((value, i) => i === index ? { ...value, probability: event.target.value } : value))}/></label>
            <button type="button" className="quiet" onClick={() => setRows(entries.filter((_, i) => i !== index))}>移除时长分布行 {index + 1}</button>
          </div>)}<button type="button" className="quiet" onClick={() => setRows([...entries, { duration: '', probability: '' }])}>添加{scenario.label}完成时长</button>
        </fieldset>;
      })}
      <div className="decision-actions"><button type="button" className="quiet" onClick={() => set({ investigation: null })}>移除调查时机</button></div>
    </>}
    <button type="button" className="quiet" onClick={() => update({ timing: null })}>移除本次时机分析输入</button>
  </>;
}

export function PreferenceInput({ state, update }: { state: DecisionState; update: Update }) {
  return <><p className="muted">这些偏好只适用于当前决策。模型中的数值权重在「目标与权重」单独确认。</p>
    {!state.preferences ? <button type="button" className="quiet" onClick={() => update({ preferences: emptyPreference() })}>填写本次决策偏好</button> : <>
      {state.preferences.adopted_version_id && <p>已选用一条保存的偏好版本。编辑会取消来源关联。</p>}
      <PreferenceFields value={state.preferences} change={preferences => update({ preferences })}/>
      <div className="decision-actions"><button type="button" className="quiet" onClick={() => update({ preferences: null })}>清除本次偏好</button></div>
    </>}
  </>;
}
