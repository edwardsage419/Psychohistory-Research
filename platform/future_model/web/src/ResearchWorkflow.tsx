import { useCallback, useEffect, useRef, useState } from 'react';

type Api = <T>(path: string, body?: unknown, version?: 'v1' | 'v2') => Promise<T>;
type CatalogEntry = { research_id: string; label: string; scope: string };
type Source = CatalogEntry & {
  source_id: string;
  commit: string;
  origin: 'MAIN' | 'CANDIDATE';
  permission: string;
  engineering_status: string;
  warnings: string[];
  files: { role: string; path: string; sha256: string; size: number }[];
  scientific_status: string;
  original_metadata: unknown;
};
type Model = { model_id: string; version: string };
type Spec = {
  protocol_version: string;
  dataset_version: string;
  seed: number;
  candidate: string;
  model_version: string;
};
type Protocol = { protocol_id: string; source_id: string; status: 'DRAFT' | 'APPROVED'; spec: Spec };
type Run = {
  id: string;
  status: string;
  config: { protocol_id: string; source_id: string; spec: Spec };
  config_sha256: string;
  code_sha256: string;
  retry_of: string | null;
  error: string | null;
  holdout_started_at?: number;
  logs: string[];
};
type Metrics = Record<string, { brier: number; log_loss: number } | null>;
type StudyScore = {
  study_id: string;
  study_label: string;
  target: string;
  units: string;
  window: [number, number];
  split: string;
  n: number;
  metrics: Metrics;
  baseline: { prevalence: number; training_n: number };
};
type Artifact = {
  artifact_sha256: string;
  result: {
    protocol_id: string;
    source_id: string;
    code_sha256: string;
    input: Run['config'];
    metrics: Metrics;
    study_results: StudyScore[];
    weight_sensitivity: { label: string; weights: Record<string, number>; metrics: Metrics }[];
    evidence: { kind: string; interpretation: string };
    scope: string;
    limitations: string[];
    selection: { split: string; horizon: number; test_used_for_selection: boolean };
    trajectory: {
      base: { content_hash: string };
      branches: { content_hash: string; payload: { branch: string; parent_hash: string; state: { time: number; opinions: string[] } } }[];
    };
    provenance: {
      protocol_sha256: string;
      input_sha256: string;
      source_reference: { commit?: string };
      protocol_version: string;
      dataset_version: string;
    };
  };
};

const statusLabels: Record<string, string> = {
  DRAFT: '草稿', PENDING: '待审批', APPROVED: '已批准', RUNNING: '运行中',
  COMPLETED: '已完成', FAILED: '失败', CANCELED: '已取消', BLOCKED: '已阻塞',
};
const activeStatuses = ['PENDING', 'APPROVED', 'RUNNING'];
const retryStatuses = ['FAILED', 'CANCELED', 'BLOCKED'];

function Status({ value }: { value: string }) {
  return <span className={`status ${value.toLowerCase()}`}>{statusLabels[value]} <small>{value}</small></span>;
}

function Json({ value }: { value: unknown }) {
  return <pre>{JSON.stringify(value, null, 2)}</pre>;
}

function SourceCard({ source, busy, verify }: { source: Source; busy: boolean; verify: () => void }) {
  return <article className="asset">
    <div className="section-heading">
      <h3>{source.research_id} · {source.label}</h3>
      <span className={source.origin === 'CANDIDATE' ? 'pill candidate-origin' : 'pill'}>{source.origin}</span>
    </div>
    <dl className="research-details">
      <dt>来源 ID</dt><dd><code>{source.source_id}</code></dd>
      <dt>固定提交</dt><dd><code>{source.commit}</code></dd>
      <dt>来源权限</dt><dd>{source.permission}</dd>
      <dt>工程状态</dt><dd>{source.engineering_status}</dd>
      <dt>原科研状态</dt><dd>{source.scientific_status}</dd>
    </dl>
    {source.origin === 'CANDIDATE' && <p className="muted">候选提交仅供查看。研究协议要求使用 MAIN 的 R123 固定来源。</p>}
    {source.warnings.length > 0 && <ul>{source.warnings.map(warning => <li key={warning}>{warning}</li>)}</ul>}
    <button type="button" className="quiet" disabled={busy} onClick={verify}>校验来源</button>
    <details>
      <summary>查看原始科研记录</summary>
      <p className="muted">{source.scope}</p>
      {source.original_metadata === null ? <p>该固定提交没有可展示的原始状态记录。</p> : <Json value={source.original_metadata}/>}
      <div className="table-wrap">
        <table className="source-file-table">
          <thead><tr><th>文件用途</th><th>仓库路径</th><th>SHA-256</th><th>字节数</th></tr></thead>
          <tbody>{source.files.map(file => <tr key={file.path}>
            <td>{file.role}</td><td><code>{file.path}</code></td><td><code>{file.sha256}</code></td><td>{file.size}</td>
          </tr>)}</tbody>
        </table>
      </div>
    </details>
  </article>;
}

function MetricTable({ metrics }: { metrics: Metrics }) {
  return <div className="table-wrap">
    <table>
      <thead><tr><th>模型</th><th>Brier 分数</th><th>对数损失</th></tr></thead>
      <tbody>{Object.entries(metrics).map(([model, score]) => <tr key={model}>
        <td><code>{model}</code></td><td>{score?.brier ?? 'UNKNOWN'}</td><td>{score?.log_loss ?? 'UNKNOWN'}</td>
      </tr>)}</tbody>
    </table>
  </div>;
}

function ResearchResult({ artifact, source }: { artifact: Artifact; source?: Source }) {
  const { result } = artifact;
  const { provenance } = result;
  return <section className="card" aria-labelledby="research-result">
    <div className="section-heading">
      <h2 id="research-result">不可变研究结果</h2>
      <span className="pill">{result.scope}</span>
    </div>
    <dl className="research-details">
      <dt>真实世界证据</dt><dd><strong className="unknown">{result.evidence.kind}</strong></dd>
      <dt>结果工件 SHA-256</dt><dd><code aria-label="结果工件 SHA-256">{artifact.artifact_sha256}</code></dd>
      <dt>协议 ID</dt><dd><code>{result.protocol_id}</code></dd>
      <dt>协议 SHA-256</dt><dd><code>{provenance.protocol_sha256}</code></dd>
      <dt>输入 SHA-256</dt><dd><code>{provenance.input_sha256}</code></dd>
      <dt>来源 ID</dt><dd><code>{result.source_id}</code></dd>
      <dt>来源提交</dt><dd><code>{provenance.source_reference.commit ?? source?.commit}</code></dd>
      <dt>代码 SHA-256</dt><dd><code>{result.code_sha256}</code></dd>
      <dt>版本与种子</dt><dd>{provenance.protocol_version} · {provenance.dataset_version} · {result.input.spec.seed}</dd>
    </dl>
    <h3>可比指标</h3>
    <p className="muted">使用 {result.selection.split} 集选择预测轮次 {result.selection.horizon}。测试集参与选择 {result.selection.test_used_for_selection ? '是' : '否'}。两项分数均以较低为优。</p>
    <MetricTable metrics={result.metrics}/>
    <div className="two-col research-score-grid">
      <div>
        <h3>逐来源评分</h3>
        {result.study_results.map(study => <article key={study.study_id} aria-label={study.study_label}>
          <h4>{study.study_label} <code>{study.study_id}</code></h4>
          <p className="muted">{study.split} · n = {study.n} · {study.target} · {study.units} · 时间窗 {study.window.join('–')}</p>
          <p className="muted">基线使用训练集事件比例 {study.baseline.prevalence}（训练样本 {study.baseline.training_n}）。</p>
          <MetricTable metrics={study.metrics}/>
        </article>)}
      </div>
      <div>
        <h3>权重敏感性</h3>
        {result.weight_sensitivity.map(scenario => <article key={scenario.label} aria-label={scenario.label}>
          <h4>{scenario.label}</h4>
          <p className="muted">{Object.entries(scenario.weights).map(([id, value]) => `${id} = ${value}`).join(' · ')}</p>
          <MetricTable metrics={scenario.metrics}/>
        </article>)}
      </div>
    </div>
    <h3>适用边界与局限</h3>
    <ul>{result.limitations.map(limitation => <li key={limitation}>{limitation}</li>)}</ul>
    <details><summary>查看不确定性记录</summary><p className="muted">{result.evidence.interpretation}</p></details>
    <details>
      <summary>查看理论情景快照</summary>
      <dl className="research-details"><dt>共同根快照</dt><dd><code>{result.trajectory.base.content_hash}</code></dd></dl>
      <div className="table-wrap"><table>
        <thead><tr><th>权重情景</th><th>终点轮次</th><th>终点意见</th><th>快照 SHA-256</th></tr></thead>
        <tbody>{result.trajectory.branches.map(branch => <tr key={branch.content_hash}>
          <td>{branch.payload.branch}</td><td>{branch.payload.state.time}</td>
          <td>{branch.payload.state.opinions.join(' / ')}</td><td><code>{branch.content_hash}</code></td>
        </tr>)}</tbody>
      </table></div>
    </details>
    <details><summary>查看固定的协议输入与来源记录</summary><Json value={result.input}/><Json value={provenance}/></details>
  </section>;
}

export function ResearchWorkflow({ api }: { api: Api }) {
  const request = useCallback(<T,>(path: string, body?: unknown) => api<T>(path, body, 'v2'), [api]);
  const [catalog, setCatalog] = useState<CatalogEntry[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [models, setModels] = useState<Model[]>([]);
  const [protocols, setProtocols] = useState<Protocol[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [researchId, setResearchId] = useState('R123');
  const [commit, setCommit] = useState('');
  const [sourceId, setSourceId] = useState('');
  const [modelKey, setModelKey] = useState('r123-degroot@1.0.0');
  const [seed, setSeed] = useState('7');
  const [lookupId, setLookupId] = useState('');
  const [selectedId, setSelectedId] = useState('');
  const [lookedUp, setLookedUp] = useState<Run | null>(null);
  const [artifact, setArtifact] = useState<{ runId: string; data: Artifact } | null>(null);
  const runRevision = useRef(0);
  const current = runs.find(run => run.id === selectedId) ?? (lookedUp?.id === selectedId ? lookedUp : null);
  const hasActiveRuns = runs.some(run => activeStatuses.includes(run.status)) || activeStatuses.includes(current?.status ?? '');
  const eligible = (source: Source) => source.research_id === 'R123'
    && source.origin === 'MAIN' && source.engineering_status === 'MAIN_PIN_VERIFIED';
  const selectedModel = models.find(model => `${model.model_id}@${model.version}` === modelKey);

  useEffect(() => {
    let active = true;
    Promise.all([
      request<CatalogEntry[]>('source-catalog'), request<Source[]>('sources'), request<Model[]>('models'),
      request<Protocol[]>('protocols'), request<Run[]>('experiments'),
    ]).then(([nextCatalog, nextSources, nextModels, nextProtocols, nextRuns]) => {
      if (!active) return;
      setCatalog(nextCatalog);
      setSources(nextSources);
      setModels(nextModels.filter(model => model.model_id === 'r123-degroot' && model.version === '1.0.0'));
      setProtocols(nextProtocols);
      setRuns(nextRuns);
      setLoaded(true);
    }).catch(reason => { if (active) setError(String(reason)); });
    return () => { active = false; };
  }, [request]);

  const refreshRuns = useCallback(async (id: string) => {
    const revision = ++runRevision.current;
    const next = await request<Run[]>('experiments');
    const extra = id && !next.some(run => run.id === id) ? await request<Run>(`experiments/${encodeURIComponent(id)}`) : null;
    if (revision === runRevision.current) {
      setRuns(next);
      setLookedUp(extra);
    }
  }, [request]);

  useEffect(() => {
    if (!hasActiveRuns) return;
    let active = true;
    const interval = window.setInterval(() => {
      refreshRuns(selectedId).catch(reason => { if (active) setError(String(reason)); });
    }, 900);
    return () => {
      active = false;
      ++runRevision.current;
      window.clearInterval(interval);
    };
  }, [hasActiveRuns, refreshRuns, selectedId]);

  useEffect(() => {
    if (!current || current.status !== 'COMPLETED') return;
    let active = true;
    const runId = current.id;
    request<Artifact>(`experiments/${runId}/result`).then(data => {
      if (active) setArtifact({ runId, data });
    }).catch(reason => { if (active) setError(String(reason)); });
    return () => { active = false; };
  }, [current?.id, current?.status, request]);

  async function act(operation: () => Promise<void>) {
    setBusy(true);
    setError('');
    setNotice('');
    try {
      await operation();
    } catch (reason) {
      setError(String(reason));
    } finally {
      setBusy(false);
    }
  }

  function rememberSource(source: Source) {
    setSources(previous => [source, ...previous.filter(item => item.source_id !== source.source_id)]);
  }

  function rememberProtocol(protocol: Protocol) {
    setProtocols(previous => [protocol, ...previous.filter(item => item.protocol_id !== protocol.protocol_id)]);
  }

  function selectRun(id: string) {
    setSelectedId(id);
    setLookupId(id);
  }

  function rememberRun(run: Run) {
    ++runRevision.current;
    setRuns(previous => previous.some(item => item.id === run.id)
      ? previous.map(item => item.id === run.id ? run : item)
      : [run, ...previous]);
    setLookedUp(run);
    selectRun(run.id);
  }

  return <div className="research-workflow">
    {error && <p className="error" role="alert">操作未完成。{error}</p>}
    {notice && <p className="research-notice" role="status">{notice}</p>}
    {!loaded && !error && <p className="muted" role="status">正在载入研究工作流…</p>}
    <section className="card" aria-labelledby="research-sources">
      <h2 id="research-sources">科研来源</h2>
      <p className="muted">登记后可校验固定提交和文件。来源记录保留原科研状态与浏览权限。</p>
      <form onSubmit={event => {
        event.preventDefault();
        void act(async () => {
          const source = await request<Source>('sources', { research_id: researchId, ...(commit ? { commit: commit.toLowerCase() } : {}) });
          rememberSource(source);
          if (eligible(source)) setSourceId(source.source_id);
        });
      }}>
        <div className="research-form-grid">
          <label>科研来源目录<select value={researchId} onChange={event => setResearchId(event.target.value)} required>
            {catalog.map(entry => <option key={entry.research_id} value={entry.research_id}>{entry.research_id} · {entry.label}</option>)}
          </select></label>
          <label>来源提交 SHA<input value={commit} onChange={event => setCommit(event.target.value.trim())}
            pattern="[0-9a-fA-F]{40}" placeholder="留空使用服务固定的 main 提交" spellCheck={false}/></label>
        </div>
        <button disabled={!loaded || busy}>登记来源</button>
      </form>
      {sources.map(source => <SourceCard key={source.source_id} source={source} busy={busy} verify={() => void act(async () => {
        rememberSource(await request<Source>(`sources/${source.source_id}/verify`, {}));
        setNotice(`已检查 ${source.research_id} 固定提交。`);
      })}/>)}
    </section>

    <section className="card" aria-labelledby="research-protocols">
      <h2 id="research-protocols">版本化研究协议</h2>
      <p className="muted">选择 MAIN 的 R123 来源和模型版本。协议批准后，才可提交实验审批。</p>
      <form onSubmit={event => {
        event.preventDefault();
        if (!selectedModel) return;
        void act(async () => {
          const protocol = await request<Protocol>('protocols', {
            source_id: sourceId, seed: Number(seed), model_id: selectedModel.model_id, model_version: selectedModel.version,
          });
          rememberProtocol(protocol);
        });
      }}>
        <div className="research-form-grid protocol-form">
          <label>协议来源<select value={sourceId} onChange={event => setSourceId(event.target.value)} required>
            <option value="">选择已登记的来源</option>
            {sources.map(source => <option key={source.source_id} value={source.source_id} disabled={!eligible(source)}>
              {source.research_id} · {source.origin} · {source.commit.slice(0, 12)}
            </option>)}
          </select></label>
          <label>模型版本<select value={modelKey} onChange={event => setModelKey(event.target.value)} required>
            {models.map(model => {
              const identity = `${model.model_id}@${model.version}`;
              return <option value={identity} key={identity}>{identity}</option>;
            })}
          </select></label>
          <label>协议随机种子<input type="number" min={0} max={4294967295} step={1} required value={seed}
            onChange={event => setSeed(event.target.value)}/></label>
        </div>
        <button disabled={!loaded || busy || !sourceId || !selectedModel}>创建版本化协议</button>
      </form>
      {protocols.map(protocol => <article className="asset" key={protocol.protocol_id}>
        <div className="section-heading">
          <h3>协议 <code>{protocol.protocol_id}</code></h3><Status value={protocol.status}/>
        </div>
        <p className="muted">{protocol.spec.candidate}@{protocol.spec.model_version} · {protocol.spec.protocol_version} · {protocol.spec.dataset_version} · 随机种子 {protocol.spec.seed}</p>
        <p className="muted">来源 ID <code>{protocol.source_id}</code></p>
        {protocol.status === 'DRAFT' && <button type="button" disabled={busy} onClick={() => void act(async () => {
          rememberProtocol(await request<Protocol>(`protocols/${protocol.protocol_id}/approve`, {}));
        })}>批准协议</button>}
        {protocol.status === 'APPROVED' && <button type="button" disabled={busy} onClick={() => void act(async () => {
          rememberRun(await request<Run>('experiments', { protocol_id: protocol.protocol_id }));
        })}>提交研究实验</button>}
        <details><summary>查看协议参数与预算</summary><Json value={protocol.spec}/></details>
      </article>)}
    </section>

    <section className="card" aria-labelledby="research-history">
      <div className="section-heading">
        <h2 id="research-history">研究实验历史</h2>
        <button type="button" className="quiet" disabled={!loaded || busy} onClick={() => void act(() => refreshRuns(selectedId))}>刷新历史</button>
      </div>
      <form className="research-lookup" onSubmit={event => {
        event.preventDefault();
        void act(async () => {
          const run = await request<Run>(`experiments/${encodeURIComponent(lookupId.trim())}`);
          rememberRun(run);
        });
      }}>
        <label>实验完整 ID<input value={lookupId} onChange={event => setLookupId(event.target.value)} required spellCheck={false}/></label>
        <button disabled={!loaded || busy || !lookupId.trim()}>按 ID 查找实验</button>
      </form>
      {runs.length ? <div className="table-wrap">
        <table>
          <thead><tr><th>实验 ID</th><th>随机种子</th><th>状态</th></tr></thead>
          <tbody>{runs.map(run => <tr key={run.id}>
            <td><button type="button" className="text-button mono" onClick={() => selectRun(run.id)}>{run.id}</button></td>
            <td>{run.config.spec.seed}</td><td><Status value={run.status}/></td>
          </tr>)}</tbody>
        </table>
      </div> : loaded && <p className="muted">尚无研究实验。</p>}
    </section>

    {current && <section className="card" aria-labelledby="research-run">
      <div className="section-heading"><h2 id="research-run">所选研究实验</h2><Status value={current.status}/></div>
      <dl className="research-details">
        <dt>实验 ID</dt><dd><code>{current.id}</code></dd>
        <dt>协议 ID</dt><dd><code>{current.config.protocol_id}</code></dd>
        <dt>执行配置 SHA-256</dt><dd><code>{current.config_sha256}</code></dd>
        {current.retry_of && <><dt>重试来源</dt><dd><code>{current.retry_of}</code></dd></>}
      </dl>
      {current.error && <p className="error">{current.error}</p>}
      {current.holdout_started_at !== undefined && retryStatuses.includes(current.status) &&
        <p className="muted">该留出集的执行名额已保留。如需再次试验，请用新种子创建协议。</p>}
      <div className="research-run-actions">
        {([
          ['approve', '批准研究执行', current.status === 'PENDING'],
          ['cancel', '取消研究实验', activeStatuses.includes(current.status)],
          ['retry', '重试研究实验', retryStatuses.includes(current.status) && current.holdout_started_at === undefined],
        ] as const).filter(([, , available]) => available).map(([operation, label]) =>
          <button key={operation} type="button" className={operation === 'cancel' ? 'quiet' : undefined}
            disabled={busy} onClick={() => void act(async () => {
              rememberRun(await request<Run>(`experiments/${current.id}/${operation}`, {}));
            })}>{label}</button>)}
      </div>
      <details><summary>查看运行日志</summary><pre>{current.logs.join('\n')}</pre></details>
    </section>}

    {current?.status === 'COMPLETED' && artifact?.runId === current.id && <ResearchResult artifact={artifact.data}
      source={sources.find(source => source.source_id === artifact.data.result.source_id)}/>}
  </div>;
}
