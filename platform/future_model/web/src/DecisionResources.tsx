import { useState } from 'react';
import type { FormEvent } from 'react';
import type { ConversationView } from './decisionConversationTypes';

const feasibility: Record<string, string> = {
  FEASIBLE: '符合已核对的资源条件',
  INFEASIBLE: '资源不足',
  UNKNOWN: '资源条件待核实',
};

export function DecisionResources({ view, busy, onApply }: {
  view: ConversationView;
  busy: boolean;
  onApply: (resources: unknown) => void;
}) {
  const snapshot = view.resources;
  const currentDay = new Date().toISOString().slice(0, 10);
  const [draft, setDraft] = useState(() => JSON.stringify(snapshot?.state ?? {
    as_of: currentDay,
    options: view.options.map(option => ({ option_id: option.id, future_cost: null, tasks: null })),
  }, null, 2));
  const [confirmed, setConfirmed] = useState(false);
  const [problem, setProblem] = useState('');

  function submit(event: FormEvent) {
    event.preventDefault();
    try {
      const payload: unknown = JSON.parse(draft);
      if (typeof payload !== 'object' || payload === null || Array.isArray(payload)) {
        setProblem('请填写一组资源数据。');
        return;
      }
      setProblem('');
      onApply(payload);
    } catch {
      setProblem('资源数据格式有误，请核对括号、引号和分隔符。');
    }
  }

  return <div className="card">
    <p>现金按核对日的实际余额计算，预测收入和预计退款另外列出。工时按任务剩余量、日期和期限计算。</p>
    {snapshot && <div>
      {snapshot.result.cash.balance && <p>可用余额 {snapshot.result.cash.balance} {snapshot.result.cash.currency}</p>}
      {snapshot.result.cash.status === 'UNKNOWN' && <p>实际余额待核实。</p>}
      <ul>{view.options.map(option => {
        const item = snapshot.result.options[option.id];
        return <li key={option.id}>
          <strong>{option.label}</strong> · {feasibility[item?.status ?? 'UNKNOWN']}
          {item?.cash.margin && <> · 扣除未来费用和预留后的余额 {item.cash.margin} {snapshot.result.cash.currency}</>}
          {item?.time.reason === 'TASK_DIVISIBILITY_UNSUPPORTED' && <> · 连续工作时段待核实</>}
        </li>;
      })}</ul>
    </div>}
    <form onSubmit={submit}>
      <label htmlFor="resource-state">共同资源数据</label>
      <textarea id="resource-state" rows={10} maxLength={60000} disabled={busy} value={draft}
        onChange={event => { setDraft(event.target.value); setConfirmed(false); }} />
      <ul>{view.options.map(option => <li key={option.id}>{option.label} <code>{option.id}</code></li>)}</ul>
      <label className="decision-check"><input type="checkbox" disabled={busy} checked={confirmed}
        onChange={event => setConfirmed(event.target.checked)}/>我已核对资源、日期和来源</label>
      <button type="submit" disabled={busy || !confirmed}>应用资源并重新计算</button>
      {snapshot && <button type="button" className="quiet" disabled={busy || !confirmed}
        onClick={() => onApply(null)}>移除此会话中的资源输入</button>}
      {problem && <p role="alert">{problem}</p>}
    </form>
  </div>;
}
