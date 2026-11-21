import { useEffect, useState, type FormEvent } from 'react';
import type { Api } from './decisionTypes';

type LocalStatus = { enabled: boolean; model: string | null; evidence: string };
type Method = { model_id: string; version: string; title: string; applicability: string };
type Proposal = {
  model_key: string;
  initial_analysis: string;
  reason: string;
  ask: string;
  candidate_options: string[];
};
type Reply = {
  status: string; calculated?: boolean; model?: string; proposal?: Proposal | null;
  candidate_method?: Method | null; evidence?: string;
};

export function LocalAIChat({ api, onOpenWorkbench }: { api: Api; onOpenWorkbench: () => void }) {
  const [status, setStatus] = useState<LocalStatus | null>(null);
  const [question, setQuestion] = useState('');
  const [reply, setReply] = useState<Reply | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let alive = true;
    api<LocalStatus>('decisions/local-ai/status', undefined, 'v5')
      .then(data => { if (alive) setStatus(data); })
      .catch(() => { if (alive) setError('无法读取本地 AI 服务状态。'); });
    return () => { alive = false; };
  }, [api]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!question.trim() || loading) return;
    setLoading(true);
    setError('');
    setReply(null);
    try {
      const result = await api<Reply>('decisions/local-ai/propose', { question }, 'v5');
      setReply(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : '本地 AI 请求失败。');
    } finally {
      setLoading(false);
    }
  }

  const unavailable: Record<string, string> = {
    LOCAL_MODEL_UNAVAILABLE: '请确认 Ollama 已在 Mac 上运行，并已下载指定模型。',
    LOCAL_AI_DISABLED: '服务未启用。',
    MODEL_BUSY: '模型正在处理其他问题。',
    MODEL_OUTPUT_REJECTED: '本次输出未通过结构化校验，未调用数学引擎。',
    INVALID_QUERY: '问题内容超出允许范围。',
  };

  return <div className="local-ai-view">
    <section className="card">
      <h2>本地智能决策助手</h2>
      <p className="muted">用日常语言描述你的选择。Qwen 在 Mac 本机建议适合的数学方法，只有确认事实和约束后才能由 v0.5 引擎计算。</p>
      <p className="muted">状态：{status ? (status.enabled ? '本地已启用：' + status.model : '未启用，请按本地部署指南设置') : '正在检查'}</p>
      <form onSubmit={submit}>
        <label htmlFor="local-ai-question">你想解决什么问题？</label>
        <textarea id="local-ai-question" rows={4} maxLength={3000} value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="比如：我有两个工作选择，收入提高但工时增加，应该怎么比较？"/>
        <div className="actions">
          <button type="submit" disabled={!status?.enabled || !question.trim() || loading}>{loading ? '正在分析' : '开始分析'}</button>
          <button className="quiet" type="button" onClick={onOpenWorkbench}>打开数学决策工作台</button>
        </div>
      </form>
      {error && <p role="alert" className="error">{error}</p>}
    </section>
    {reply && reply.status !== 'NEEDS_CONFIRMATION' && <section className="card" role="status">
      <h3>本地分析暂不可用</h3>
      <p>{unavailable[reply.status] ?? '本次调用未完成。'}</p>
    </section>}
    {reply?.status === 'NEEDS_CONFIRMATION' && reply.proposal && <section className="card" aria-live="polite">
      <h3>初步分析</h3>
      <p>{reply.proposal.initial_analysis}</p>
      <h3>建议使用的方法</h3>
      <p>{reply.candidate_method ? reply.candidate_method.title + '（' + reply.proposal.model_key + '）' : '暂时缺少适用条件，先补充信息'}</p>
      <p className="muted">{reply.proposal.reason}</p>
      {reply.proposal.candidate_options.length > 0 && <>
        <h3>从你的原话提取的候选方案，尚未确认</h3>
        <ul>{reply.proposal.candidate_options.map((option, i) => <li key={i + '-' + option}>{option}</li>)}</ul>
      </>}
      {reply.proposal.ask && <p><strong>下一项最关键的信息：</strong>{reply.proposal.ask}</p>}
      <p className="muted">这次生成的是待确认的理解和方法建议。没有执行数值计算，也没有保存你的问题。</p>
      <button className="quiet" type="button" onClick={onOpenWorkbench}>进入数学工作台核对并计算</button>
    </section>}
  </div>;
}
