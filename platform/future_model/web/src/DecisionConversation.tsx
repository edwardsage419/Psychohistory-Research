import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { DecisionEditor } from './DecisionEditor';
import { DecisionResources } from './DecisionResources';
import { DecisionHistory } from './DecisionHistory';
import { DecisionResults, type ResultScope } from './DecisionResults';
import { structuredIssue } from './DecisionWorkbench';
import type { Claim, ConversationStatus, ConversationView } from './decisionConversationTypes';
import type { Api, DecisionState, PersonalApiVersion, PreferenceVersion } from './decisionTypes';
import './conversation.css';

const noFilter: ResultScope = { options: 'all', methods: 'all' };
const endpoint = (name: string) => `decisions/${name}`;
const evidenceLabels: Record<string, string> = { PROVISIONAL: '待核对', USER_CONFIRMED: '由你核对', EXTERNALLY_VERIFIED: '已由外部来源核实', DISMISSED: '已略过', SUPERSEDED: '已被替换', CONFLICT: '来源有冲突', INCOMPARABLE: '口径不可比较', UNKNOWN: '仍未知' };
const feasibilityLabels: Record<string, string> = { ACCEPT: '通过底线', REJECT: '未通过底线', UNRESOLVED: '底线待核实' };
const operators: Record<string, string> = { '>=': '至少', '>': '超过', '<=': '至多', '<': '低于' };
const isPending = (claim: Claim) => claim.status === 'PROVISIONAL';
const isConstraint = (claim: Claim) => claim.kind.endsWith('constraint') || /_max$|_min$|move_allowed/.test(claim.field);

function readback(claim: Claim) {
  return claim.source || [claim.subject, claim.value, claim.unit].filter(Boolean).join(' ');
}

function List({ items }: { items: string[] }) {
  if (!items.length) return null;
  return <ul>{items.map((item, index) => <li key={index}>{item}</li>)}</ul>;
}

type Confirmation = { claim_ids: string[]; option_ids: string[]; accept_context: boolean; dismiss_claim_ids: string[]; corrections: { claim_id: string; supersedes: string }[] };
function ConfirmGroup({ view, busy, onConfirm }: { view: ConversationView; busy: boolean; onConfirm: (choice: Confirmation) => void }) {
  const [checked, setChecked] = useState(false);
  const [context, setContext] = useState(false);
  const [claimChoices, setClaimChoices] = useState<Record<string, string>>({});
  const [optionChoices, setOptionChoices] = useState<Record<string, boolean>>({});
  const [superseded, setSuperseded] = useState<Record<string, string>>({});
  const proposals = view.claims.filter(isPending);
  const options = view.options.filter(option => option.status.toUpperCase() !== 'CONFIRMED');
  const needsContext = !view.state.confirmed || !view.state.constraints_confirmed;
  if (!proposals.length && !options.length && !needsContext) return null;
  function send(event: FormEvent) {
    event.preventDefault();
    if (!checked || busy) return;
    const confirmed = proposals.filter(claim => !claimChoices[claim.id] || claimChoices[claim.id] === 'confirm');
    onConfirm({
      claim_ids: confirmed.map(claim => claim.id),
      option_ids: options.filter(option => optionChoices[option.id] !== false).map(option => option.id),
      accept_context: context,
      dismiss_claim_ids: proposals.filter(claim => claimChoices[claim.id] === 'dismiss').map(claim => claim.id),
      corrections: confirmed.filter(claim => superseded[claim.id]).map(claim => ({ claim_id: claim.id, supersedes: superseded[claim.id] })),
    });
  }
  return <form onSubmit={send} className="conversation-confirm" aria-label="核对与确认">
    <h3>核对与确认</h3>
    {proposals.length > 0 && <ul className="conversation-claim-list">{proposals.map(claim => {
      const previous = claim.prior_ids;
      const value = readback(claim);
      return <li key={claim.id} data-claim-id={claim.id} data-claim-status={claim.status}>
        <strong>{value}</strong>
        <label className="conversation-claim-choice">处理<select aria-label={`处理：${value}`} value={claimChoices[claim.id] ?? 'confirm'} disabled={busy} onChange={event => setClaimChoices({ ...claimChoices, [claim.id]: event.target.value })}>
          <option value="confirm">确认</option><option value="leave">继续核实</option><option value="dismiss">舍弃这项理解</option>
        </select></label>
        {previous.length > 0 && <label>用此项替换此前内容<select disabled={busy} value={superseded[claim.id] ?? ''} onChange={event => setSuperseded({ ...superseded, [claim.id]: event.target.value })}>
          <option value="">暂不替换</option>{previous.map(id => {const prior = view.claims.find(item => item.id === id);return <option key={id} value={id}>{prior ? readback(prior) : id}</option>;})}
        </select></label>}
      </li>;
    })}</ul>}
    {options.length > 0 && <fieldset className="conversation-option-confirm"><legend>本次要考虑的方案</legend>{options.map(option => <label key={option.id} className="decision-check"><input type="checkbox" checked={optionChoices[option.id] !== false} disabled={busy} onChange={event => setOptionChoices({ ...optionChoices, [option.id]: event.target.checked })}/>{option.label}</label>)}</fieldset>}
    <p className="muted">舍弃一项理解只表示那项提取有误。如果原来的底线仍然适用，请补充正确条件，或选择继续核实。只有全部底线已说明时才确认下方范围。</p>
    <label className="decision-check"><input type="checkbox" checked={context} disabled={busy} onChange={event => setContext(event.target.checked)}/>我已说明本次目的和硬约束</label>
    <label className="decision-check"><input type="checkbox" checked={checked} disabled={busy} onChange={event => setChecked(event.target.checked)}/>我已核对本组理解</label>
    <button type="submit" disabled={!checked || busy}>确认本组理解</button>
  </form>;
}

function AnalysisPurpose({ status }: { status?: ConversationStatus | null }) {
  const purposes = status?.purpose_consent;
  return <details className="conversation-purpose"><summary>理解方式与用途</summary>
    <p>本地规则识别部分数量、条件和方案。理解有缺口时会保留未知。保存记录需要单独授权。</p>
    {purposes && <dl className="conversation-purposes">
      {Object.entries({ save: '保存记录', personalization: '自动个性化', research: '科研复用', training: '训练' }).map(([purpose, label]) => purposes[purpose] && <div key={purpose}>
        <dt>{label}</dt><dd>{purpose === 'save' ? '在记录区另行授权' : purposes[purpose].available ? (purposes[purpose].authorized ? '已授权' : '待授权') : '不可用'}</dd>
      </div>)}
    </dl>}
  </details>;
}

function EvidenceAudit({ claims }: { claims: Claim[] }) {
  if (!claims.length) return null;
  return <section className="card" aria-label="对话证据核对">
    <h2>对话证据核对</h2>
    <div className="table-wrap"><table className="decision-table"><thead><tr><th scope="col">原文依据</th><th scope="col">核对状态</th></tr></thead><tbody>
      {claims.map(claim => <tr key={claim.id}><th scope="row">{readback(claim)}</th><td>{evidenceLabels[claim.status] ?? claim.status}</td></tr>)}
    </tbody></table></div>
  </section>;
}

export function DecisionConversation({ api: appApi, registerConversation, closeConversation }: {
  api: Api; registerConversation: (id: string | null) => void; closeConversation: () => void;
}) {
  const controller = useRef<AbortController | null>(null);
  useLayoutEffect(() => {
    const active = new AbortController();
    controller.current = active;
    return () => active.abort();
  }, []);
  const api: Api = useCallback(<T,>(path: string, body?: unknown, version: PersonalApiVersion = 'v7') => appApi<T>(path, body, version, controller.current?.signal), [appApi]);
  const [status, setStatus] = useState<ConversationStatus | null>(null);
  const [view, setView] = useState<ConversationView | null>(null);
  const liveView = useRef<ConversationView | null>(null);
  const operation = useRef<string | null>(null);
  const sequence = useRef(0);
  const [draft, setDraft] = useState<DecisionState | null>(null);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState<string | null>(null);
  const [invalidating, setInvalidating] = useState(false);
  const [error, setError] = useState('');
  const [advanced, setAdvanced] = useState(false);
  const [scope, setScope] = useState<ResultScope>(noFilter);
  const [choosing, setChoosing] = useState<string | null>(null);
  const [trigger, setTrigger] = useState('');
  const [savedRevision, setSavedRevision] = useState(0);
  const entry = useRef<HTMLTextAreaElement>(null);
  const reply = useRef<HTMLTextAreaElement>(null);
  const state = view?.state ?? null;
  const dirty = !!draft && draft !== state;
  const analysis = !invalidating && !dirty ? view?.analysis ?? null : null;
  const summary = !invalidating && (!dirty || !view?.analysis) ? view?.summary : null;
  const confirmed = !!state?.confirmed && !!state.constraints_confirmed;
  const hasView = !!view;

  useEffect(() => {
    let active = true;
    api<ConversationStatus>(endpoint('status')).then(next => { if (active) setStatus(next); }).catch(() => {});
    return () => { active = false; };
  }, [api]);

  useEffect(() => {
    if (hasView) reply.current?.focus();
    else entry.current?.focus();
  }, [hasView]);

  function reset(onlyDecisionId?: string) {
    if (onlyDecisionId && liveView.current?.state.decision_id !== onlyDecisionId) return;
    sequence.current += 1;
    liveView.current = null;
    closeConversation();
    setView(null);
    setDraft(null);
    setInput('');
    setBusy(null);
    operation.current = null;
    setInvalidating(false);
    setError('');
    setAdvanced(false);
    setChoosing(null);
    setTrigger('');
    setScope(noFilter);
    setSavedRevision(0);
  }

  async function perform(name: string, body: Record<string, unknown>, whose = liveView.current, invalidates = false) {
    if (operation.current || (whose && liveView.current !== whose)) return false;
    const request = ++sequence.current;
    const startId = name === 'start' ? crypto.randomUUID().replaceAll('-', '') : null;
    if (startId) registerConversation(startId);
    operation.current = name;
    setBusy(name);
    setError('');
    if (invalidates) setInvalidating(true);
    try {
      const next = await api<ConversationView>(endpoint(name), { ...(whose ? { session_id: whose.session_id, revision: whose.revision } : startId ? { session_id: startId } : {}), ...body });
      if (request !== sequence.current) return false;
      if (next.session_id !== (whose?.session_id ?? startId)
          || (whose && next.revision !== whose.revision + 1)
          || next.result.session_id !== next.session_id || next.result.revision !== next.revision
          || next.result.protocol !== '0.7.0') throw new Error('返回内容与当前对话不一致。');
      liveView.current = next;
      registerConversation(next.session_id);
      setView(next);
      setDraft(next.state);
      setInvalidating(false);
      setChoosing(null);
      if (name === 'start' || name === 'turn') {
        setInput('');
            setTrigger('');
      }
      return true;
    } catch (failure) {
      if (startId && request === sequence.current) closeConversation();
      if (request === sequence.current && !(failure instanceof DOMException && failure.name === 'AbortError')) setError(failure instanceof Error ? failure.message : '操作未完成，请重试。');
      return false;
    } finally {
      if (request === sequence.current) {
        operation.current = null;
        setBusy(null);
      }
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    if (!input.trim()) return;
    if (view) void perform('turn', { text: input }, view, true);
    else void perform('start', { question: input }, null);
  }

  function applyAdvanced() {
    if (!view || !draft || !dirty) return;
    const issue = structuredIssue(draft);
    if (issue) {
      setError(issue);
      return;
    }
    void perform('analyze', { state: draft, confirmed: true }, view, true);
  }

  async function save(epoch: string) {
    const current = liveView.current;
    if (!current || !analysis || dirty || operation.current) throw new Error('请先等待当前对话更新。');
    const request = ++sequence.current;
    operation.current = 'save';
    setBusy('save');
    try {
      await api(endpoint('save'), { session_id: current.session_id, revision: current.revision, epoch, save_confirmed: true });
    } finally {
      if (request === sequence.current) {
        operation.current = null;
        setBusy(null);
      }
    }
  }

  function applyPreference(version: PreferenceVersion) {
    setDraft(current => current && ({ ...current, preferences: { ...version.preferences, adopted_version_id: version.version_id } }));
    setAdvanced(true);
  }

  return <div id="decision-conversation" className="decision-workbench decision-conversation" data-workflow="v07" data-phase={view?.phase} data-conversation-revision={view?.revision} data-local-model-status={view?.local_model_status ?? status?.local_model?.status}>
    {!view && <section className="card conversation-entry" aria-labelledby="conversation-entry-title">
      <h2 id="conversation-entry-title">你正在考虑什么？</h2>
      <p>说说你面临的选择，以及现在最难判断的地方。</p>
      <form onSubmit={submit}>
        <label>你的决策问题<textarea ref={entry} value={input} onChange={event => setInput(event.target.value)} placeholder="例如，我该继续住在现在的地方，还是搬到通勤更短的地方？" required maxLength={6000} autoComplete="off" disabled={!!busy}/></label>
        <button type="submit" disabled={!!busy || !input.trim()}>开始对话</button>
        <AnalysisPurpose status={status}/>
      </form>
    </section>}
    {view && <>
      <section className="card conversation-main" aria-label="决策对话">
        <div className="conversation-thread-top"><h2>决策对话</h2><button type="button" className="text-button" disabled={!!busy} onClick={() => reset()}>开始新决策</button></div>
        <p className="conversation-user"><span>你</span>{view.dialogue.filter(message => message.role === 'user').at(-1)?.text ?? state?.question}</p>
        {summary && <div className="conversation-answer" aria-live="polite">
          {summary.warning && <p className="conversation-warning">{summary.warning}</p>}
          {summary.conclusion && <p className="conversation-conclusion">{summary.conclusion}</p>}
          {!!view.changes?.length && <section className="conversation-changes" aria-label="这次改动"><h3>这次改动</h3><List items={view.changes}/></section>}
          {summary.differences?.length > 0 && <div><h3>哪些地方有差别</h3><List items={summary.differences}/></div>}
          {summary.unknowns?.length > 0 && <div><h3>仍待核实</h3><List items={summary.unknowns}/></div>}
          {summary.question && <section className="conversation-followup" aria-label="待回答的问题" data-focus={summary.focus}><strong>{summary.question}</strong></section>}
        </div>}
        {view.dialogue.length > 1 && <details className="conversation-transcript"><summary>查看对话记录</summary><ol>{view.dialogue.map((message, index) => <li key={index}><strong>{message.role === 'user' ? '你' : '工作台'}</strong><p>{message.text}</p></li>)}</ol></details>}
        <form className="conversation-reply" onSubmit={submit}>
          <label>补充或修正<textarea ref={reply} value={input} onChange={event => setInput(event.target.value)} placeholder="直接说明你知道的情况，或指出需要改正的内容。" required maxLength={6000} autoComplete="off" disabled={!!busy}/></label>
          {dirty && <p className="muted">若先发送对话，工作台会按新回复重新整理高级输入。</p>}
          <button type="submit" disabled={!!busy || !input.trim()}>发送</button>
          <AnalysisPurpose status={status}/>
        </form>
      </section>
      {state && <section className="card conversation-context" aria-label="方案与硬约束">
        <h2>方案与硬约束</h2>
        {state.constraints.length > 0 ? <ul className="conversation-constraints">{state.constraints.map(item => <li key={item.id}><strong>{item.label}</strong><span>{operators[item.operator]} {item.threshold} {item.unit}</span></li>)}</ul> : <p className="muted">{state.constraints_confirmed ? '已确认没有硬约束。' : '硬约束清单待确认。'}</p>}
        {view.claims.filter(claim => isConstraint(claim) && isPending(claim)).map(claim => <p className="conversation-constraint-pending" key={claim.id}>待核对的底线 · {readback(claim)}</p>)}
        <div className="conversation-options">{view.options.map(option => {
          const chosen = view.selected_option_id === option.id;
          const verdict = analysis?.feasibility.find(item => item.option_id === option.id)?.status;
          const selectable = verdict === 'ACCEPT' && (analysis?.temporal_scope?.[option.id] ?? 'FEASIBLE') === 'FEASIBLE';
          return <article key={option.id} data-option-id={option.id} data-option-status={option.status} data-feasibility={verdict} className="conversation-option">
            <h3>{option.label}</h3>
            <span className="pill">{verdict ? feasibilityLabels[verdict] ?? verdict : option.status.toUpperCase() === 'CONFIRMED' ? '已核对' : '候选待核对'}</span>
            {option.status.toUpperCase() === 'CONFIRMED' && (chosen ? <span className="conversation-chosen">你已选择</span> : <button type="button" className="quiet" disabled={!!busy || dirty || invalidating || !selectable} onClick={() => setChoosing(option.id)}>选择此方案</button>)}
            {option.status !== 'CONFIRMED' && <button type="button" className="text-button" disabled={!!busy} onClick={() => { setInput(current => current.trim() ? current : `${option.label}：`); reply.current?.focus(); }}>补充此方案</button>}
            {choosing === option.id && <div className="conversation-choice-prompt"><p>确认你的选择：{option.label}</p><div className="decision-actions">
              <button type="button" disabled={!!busy} onClick={() => void perform('select', { option_id: option.id, confirmed: true })}>确认选择</button>
              <button type="button" className="quiet" disabled={!!busy} onClick={() => setChoosing(null)}>取消选择</button>
            </div></div>}
          </article>;
        })}</div>
        <ConfirmGroup key={`${view.session_id}:${view.revision}`} view={view} busy={!!busy} onConfirm={choice => void perform('confirm', choice, view, true)}/>
        <div className="decision-actions conversation-compute">
          {confirmed && <button type="button" disabled={!!busy || dirty} onClick={() => void perform('analyze', {}, view, true)}>计算并比较</button>}
          {dirty && <button type="button" className="quiet" disabled={!!busy} onClick={() => { setDraft(state); setInvalidating(false); setError(''); }}>撤销未应用的高级编辑</button>}
        </div>
        {view.selected_option_id && <form className="conversation-plan" onSubmit={event => { event.preventDefault(); if (trigger.trim()) void perform('plan', { option_id: view.selected_option_id, trigger, confirmed: true }); }}>
          <h3>为这个选择写一个条件计划</h3>
          <label>触发条件<input value={trigger} onChange={event => setTrigger(event.target.value)} maxLength={400} placeholder="如果……再采取这个行动" disabled={!!busy}/></label>
          <button type="submit" disabled={!!busy || dirty || invalidating || !trigger.trim()}>确认条件计划</button>
          {view.selected_plan && <p>已确认条件计划：{view.selected_plan.trigger}</p>}
          <p className="muted">实际发生的行动可在本地记录中单独登记。</p>
        </form>}
      </section>}
      <details className="conversation-details">
        <summary>共同资源与进度</summary>
        <DecisionResources key={view.result.receipt_sha256} view={view} busy={!!busy}
          onApply={resources => { void perform('update_resources', { resources, confirmed: true }, view, true); }}/>
      </details>
      {!!view.knowledge?.search.hits.length && <details className="conversation-details">
        <summary>本地知识与待补资料</summary>
        <p>这些是本地研究参考。决定是否适用前仍需核对来源、适用条件和个人事实。</p>
        {view.knowledge.methods.map(method => <div key={method.method}>
          <h3>{method.title ?? method.method}</h3>
          <List items={method.requirements?.map(item => item.description) ?? []}/>
        </div>)}
        <ul>{view.knowledge.search.hits.map(({ card, snippet }) => <li key={card.path}>
          <strong>{card.title}</strong><p>{snippet}</p><code>{card.path} · {card.version.slice(0, 12)}</code>
          {card.applicability_boundary && <p>{card.applicability_boundary}</p>}
        </li>)}</ul>
      </details>}
      {draft && <details className="conversation-details" open={advanced} onToggle={event => setAdvanced(event.currentTarget.open)}>
        <summary>高级输入与审计</summary>
        <p className="conversation-advanced-note">请在对话中修正已核对的方案与数值。选择「应用高级输入并比较」将确认此处填写的数据、来源、情景和比较条件。</p>
        <EvidenceAudit claims={view.claims}/>
        <DecisionEditor key={view.session_id} state={draft} understanding={null} questions={analysis?.questions ?? []} plan={analysis?.plan} guided update={patch => setDraft(current => current && ({ ...current, ...patch }))} confirm={applyAdvanced} advancedApply={{ label: '应用高级输入并比较', disabled: !!busy || !dirty }}/>
        {analysis && <DecisionResults analysis={analysis} state={state ?? draft} guided preview={false} scope={scope} onScope={setScope}/>}
        {dirty && <p className="decision-notice">应用高级输入后会显示新的比较。</p>}
      </details>}
    </>}
    {busy && <p role="status" className="decision-notice">{busy === 'analyze' ? '正在计算当前输入…' : busy === 'save' ? '正在保存已确认的修订…' : '正在更新对话…'}</p>}
    {error && <p className="error" role="alert">{error}</p>}
    <details className="conversation-details conversation-records">
      <summary>本地记录与隐私</summary>
      <DecisionHistory api={api} version="v5" state={state} analysis={busy ? null : analysis} savedRevision={savedRevision} onSave={saved => setSavedRevision(saved.revision)} onClear={reset} onApplyPreference={applyPreference} saveConfirmed={{ revision: view?.revision ?? 0, save }}/>
    </details>
    <p className="conversation-footer">离开工作台会清除未保存的对话。共享设备请结束本地会话。 <a href="?workflow=v05">v0.5 工作台</a> <a href="?workflow=v04">v0.4 工作台</a></p>
  </div>;
}
