import { useCallback, useEffect, useRef, useState } from 'react';
import { MechanismResult, methodLabel, timeLabel } from './MechanismResult';
import type { Artifact, Config, Method, Parameters, Source } from './MechanismResult';

type Api = <T>(path: string, body?: unknown, version?: 'v1' | 'v2' | 'v3') => Promise<T>;
type Model = { model_id: string; version: string; research_id: string; permission: string };
type Run = {
  id: string; status: string; config: Config; logs: string[]; error: string | null;
  config_sha256: string; code_sha256: string;
};
type Comparison = { samples: number; max_abs_difference: number; max_abs_difference_decimal: string; points: unknown };
type Draft = { vector: string; matrix: string; method: Method; steps: string; stepSize: string };
type Branch = { runId: string; snapshot: string; time: string; timeKind: string; values: string };

const modelNames: Record<string, string> = { R123: 'DeGroot 共识', R132: '复制子动力学' };
const statusLabels: Record<string, string> = {
  PENDING: '待审批', APPROVED: '已批准', RUNNING: '运行中', COMPLETED: '已完成',
  FAILED: '失败', CANCELED: '已取消', BLOCKED: '已阻塞',
};
const sourceWarnings: Record<string, string> = {
  DUPLICATE_SOURCE_ID: '此固定来源已登记。', OTHER_SOURCE_VERSION_REGISTERED: '这个研究编号已有其他来源版本。',
};
const comparisonRejections: Record<string, string> = {
  'Trajectory mechanisms have no common forecast target; Brier and Log Loss belong to v2': '机制轨迹缺少共同的预测目标。Brier 分数和对数损失适用于研究工作流。',
  'Models, scientific sources or time semantics are incompatible': '模型、科研来源或时间语义不相容。',
  'The trajectories have different payoff matrices': '轨迹的收益矩阵不同。',
  'The trajectories have different influence weights': '轨迹的影响权重不同。',
  'Trajectory comparison requires the same initial state and observation times': '比较要求相同的初始状态与观测时间。',
  'Trajectory observation grids are incompatible': '轨迹的观测时间不相容。',
};
const activeStatuses = ['PENDING', 'APPROVED', 'RUNNING'];
const pinned = (source: Source, researchId?: string) => source.research_id === researchId
  && source.origin === 'MAIN' && source.engineering_status === 'MAIN_PIN_VERIFIED';
const modelKey = (model: Model) => `${model.model_id}@${model.version}`;
const runMethod = (run: Run) => 'method' in run.config.parameters ? run.config.parameters.method : 'weighted-average';

const replicatorPresets = {
  logistic: { label: '常量优势', vector: '1/4, 3/4', matrix: '2, 2\n1, 1' },
  'hawk-dove': { label: '鹰鸽博弈', vector: '1/2, 1/2', matrix: '-2, 2\n0, 1' },
  'stag-hunt': { label: '猎鹿博弈', vector: '4/5, 1/5', matrix: '4, 0\n3, 3' },
  'rock-paper-scissors': { label: '零和石头剪刀布', vector: '1/2, 3/10, 1/5', matrix: '0, -1, 1\n1, 0, -1\n-1, 1, 0' },
};
const consensusPresets = {
  published: { label: '两主体权重示例', vector: '0, 1', matrix: '1/2, 1/2\n1/4, 3/4' },
  influence: { label: '不对称影响', vector: '1/4, 3/4', matrix: '3/4, 1/4\n1/8, 7/8' },
};

function defaultDraft(replicator: boolean): Draft {
  const preset = replicator ? replicatorPresets.logistic : consensusPresets.published;
  return { vector: preset.vector, matrix: preset.matrix, method: 'rk4', steps: replicator ? '40' : '8', stepSize: '1/40' };
}

function parseDraft(draft: Draft, replicator: boolean): Parameters {
  const vector = (text: string) => text.trim().split(/[\s,，]+/).filter(Boolean);
  const initial = vector(draft.vector);
  const matrix = draft.matrix.trim().split(/\r?\n/).filter(line => line.trim()).map(vector);
  const steps = Number(draft.steps);
  if (!replicator) return { opinions: initial, weights: matrix, steps };
  return { initial, payoff: matrix, steps, method: draft.method,
    ...(draft.method === 'eq3' ? {} : { step_size: draft.stepSize.trim() }) };
}

function draftFromParameters(parameters: Parameters): Draft {
  const displayMatrix = (matrix: string[][]) => matrix.map(row => row.join(', ')).join('\n');
  return 'initial' in parameters
    ? { vector: parameters.initial.join(', '), matrix: displayMatrix(parameters.payoff),
        method: parameters.method, steps: String(parameters.steps), stepSize: parameters.step_size ?? '1/40' }
    : { ...defaultDraft(false), vector: parameters.opinions.join(', '),
        matrix: displayMatrix(parameters.weights), steps: String(parameters.steps) };
}

function Status({ value }: { value: string }) {
  return <span className={`status ${value.toLowerCase()}`}>{statusLabels[value] ?? value} <small>{value}</small></span>;
}

function CompareRuns({ request, runs }: { request: <T>(path: string, body?: unknown) => Promise<T>; runs: Run[] }) {
  const [left, setLeft] = useState('');
  const [right, setRight] = useState('');
  const [metric, setMetric] = useState('trajectory');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [comparison, setComparison] = useState<Comparison | null>(null);
  const completed = runs.filter(run => run.status === 'COMPLETED');
  const options = completed.map(run => <option key={run.id} value={run.id}>
    {run.config.model_id} · {methodLabel(runMethod(run))} · {run.id.slice(0, 12)}
  </option>);

  function clearComparison() {
    setError('');
    setComparison(null);
  }

  return <section className="card" aria-labelledby="mechanism-compare">
    <h2 id="mechanism-compare">轨迹比较</h2>
    <p className="muted">比较使用相同模型、版本、时间单位和观测时间的合成轨迹。Brier 分数需要预测目标。</p>
    <form onSubmit={async event => {
      event.preventDefault();
      clearComparison();
      setBusy(true);
      try {
        setComparison(await request<Comparison>('compare', { left, right, metric }));
      } catch (reason) {
        const message = reason instanceof Error ? reason.message : String(reason);
        setError(comparisonRejections[message] ?? message);
      } finally {
        setBusy(false);
      }
    }}>
      <div className="mechanism-grid mechanism-grid-three">
        <label>左侧实验<select required value={left} disabled={busy} onChange={event => { setLeft(event.target.value); clearComparison(); }}>
          <option value="">选择已完成实验</option>{options}
        </select></label>
        <label>右侧实验<select required value={right} disabled={busy} onChange={event => { setRight(event.target.value); clearComparison(); }}>
          <option value="">选择已完成实验</option>{options}
        </select></label>
        <label>比较指标<select value={metric} disabled={busy} onChange={event => { setMetric(event.target.value); clearComparison(); }}>
          <option value="trajectory">轨迹最大绝对差</option><option value="brier">Brier 分数（需要预测目标）</option>
        </select></label>
      </div>
      <button disabled={busy || !left || !right || left === right}>比较已完成实验</button>
    </form>
    {error && <p className="error mechanism-feedback" role="alert">比较未完成。{error}</p>}
    {comparison && <>
      <dl className="research-details mechanism-compare-result">
        <dt>最大绝对差</dt><dd><code aria-label="最大绝对差">{comparison.max_abs_difference_decimal}</code></dd>
        <dt>匹配时间点</dt><dd>{comparison.samples}</dd>
      </dl>
      <details><summary>查看逐时间点比较</summary><pre>{JSON.stringify(comparison.points, null, 2)}</pre></details>
    </>}
  </section>;
}

export function MechanismWorkflow({ api }: { api: Api }) {
  const request = useCallback(<T,>(path: string, body?: unknown) => api<T>(path, body, 'v3'), [api]);
  const sourcesApi = useCallback(<T,>(path: string, body?: unknown) => api<T>(path, body, 'v2'), [api]);
  const [models, setModels] = useState<Model[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [selectedModel, setSelectedModel] = useState('r132-replicator@1.0.0');
  const [selectedSource, setSelectedSource] = useState('');
  const [verified, setVerified] = useState('');
  const [draft, setDraft] = useState<Draft>(defaultDraft(true));
  const [preset, setPreset] = useState('logistic');
  const [branch, setBranch] = useState<Branch | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [lookupId, setLookupId] = useState('');
  const [selectedId, setSelectedId] = useState('');
  const [lookedUp, setLookedUp] = useState<Run | null>(null);
  const [artifact, setArtifact] = useState<{ runId: string; data: Artifact } | null>(null);
  const runRevision = useRef(0);
  const setupHeading = useRef<HTMLHeadingElement>(null);

  const model = models.find(entry => modelKey(entry) === selectedModel);
  const replicator = model?.research_id === 'R132';
  const eligible = sources.filter(source => pinned(source, model?.research_id));
  const source = eligible.find(source => source.source_id === selectedSource);
  const current = runs.find(run => run.id === selectedId) ?? (lookedUp?.id === selectedId ? lookedUp : null);
  const hasActiveRuns = [...runs, current].some(run => run && activeStatuses.includes(run.status));
  const shownArtifact = current?.status === 'COMPLETED' && artifact?.runId === current.id ? artifact.data : null;
  const presets: Record<string, { label: string; vector: string; matrix: string }> = replicator ? replicatorPresets : consensusPresets;
  const maximumSteps = replicator ? (draft.method === 'eq3' ? 8 : 4096) : 32 - Number(branch?.time ?? 0);

  useEffect(() => {
    let active = true;
    Promise.all([request<Model[]>('models'), sourcesApi<Source[]>('sources'), request<Run[]>('experiments')])
      .then(([available, registered, history]) => {
        if (!active) return;
        const initialModel = available.find(model => model.research_id === 'R132') ?? available[0];
        const initialIsReplicator = initialModel?.research_id === 'R132';
        setModels(available);
        setSources(registered);
        setRuns(history);
        setSelectedModel(initialModel ? modelKey(initialModel) : '');
        setSelectedSource(registered.find(source => pinned(source, initialModel?.research_id))?.source_id ?? '');
        setDraft(defaultDraft(initialIsReplicator));
        setPreset(initialIsReplicator ? 'logistic' : 'published');
        setLoaded(true);
      }).catch(reason => { if (active) setError(String(reason)); });
    return () => { active = false; };
  }, [request, sourcesApi]);

  useEffect(() => {
    if (!hasActiveRuns) return;
    let active = true;
    async function refresh() {
      const revision = ++runRevision.current;
      try {
        const history = await request<Run[]>('experiments');
        const extra = selectedId && !history.some(run => run.id === selectedId)
          ? await request<Run>(`experiments/${encodeURIComponent(selectedId)}`) : null;
        if (active && revision === runRevision.current) {
          setRuns(history);
          setLookedUp(extra);
        }
      } catch (reason) {
        if (active && revision === runRevision.current) setError(String(reason));
      }
    }
    const interval = window.setInterval(() => { void refresh(); }, 650);
    return () => { active = false; window.clearInterval(interval); };
  }, [hasActiveRuns, request, selectedId]);

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
    try {
      await operation();
    } catch (reason) {
      setError(String(reason));
    } finally {
      setBusy(false);
    }
  }

  function chooseModel(key: string) {
    const next = models.find(model => modelKey(model) === key);
    const isReplicator = next?.research_id === 'R132';
    setSelectedModel(key);
    setSelectedSource(sources.find(source => pinned(source, next?.research_id))?.source_id ?? '');
    setPreset(isReplicator ? 'logistic' : 'published');
    setDraft(defaultDraft(isReplicator));
    setBranch(null);
  }

  function rememberSource(source: Source) {
    setSources(previous => [source, ...previous.filter(item => item.source_id !== source.source_id)]);
  }

  function chooseRun(id: string) {
    setSelectedId(id);
    setLookupId(id);
  }

  function rememberRun(run: Run) {
    ++runRevision.current;
    setRuns(previous => previous.some(item => item.id === run.id)
      ? previous.map(item => item.id === run.id ? run : item) : [run, ...previous]);
    setLookedUp(run);
    chooseRun(run.id);
  }

  function startBranch(runId: string, artifact: Artifact) {
    const { result } = artifact;
    const point = result.trajectory[result.trajectory.length - 1];
    setSelectedModel(`${result.model_id}@${result.model_version}`);
    rememberSource(result.source);
    setSelectedSource(result.source.source_id);
    setPreset('custom');
    const next = draftFromParameters(result.parameters);
    if (result.time_kind === 'discrete-round') next.steps = String(Math.min(Number(next.steps), 32 - Number(point.time)));
    setDraft(next);
    setBranch({ runId, snapshot: result.snapshot.content_hash, time: point.time, timeKind: result.time_kind, values: point.values.join(', ') });
    setupHeading.current?.focus();
  }

  return <div className="mechanism-workflow">
    {error && <p className="error" role="alert">操作未完成。{error}</p>}
    {!loaded && !error && <p className="muted" role="status">正在载入机制实验…</p>}
    <section className="card" aria-labelledby="mechanism-source">
      <div className="section-heading">
        <h2 id="mechanism-source">模型与来源</h2>
        {model && <span className="pill">{model.permission}</span>}
      </div>
      <p className="muted">合成实验使用平台内置实现。来源登记保留原研究状态、Git 提交及文件身份。</p>
      <div className="mechanism-grid">
        <label>实验模型<select value={selectedModel} disabled={busy || !loaded} onChange={event => chooseModel(event.target.value)}>
          {models.map(model => <option key={modelKey(model)} value={modelKey(model)}>
            {model.research_id} · {modelNames[model.research_id] ?? model.model_id} · {model.version}
          </option>)}
        </select></label>
        <label>固定科研来源<select value={selectedSource} disabled={busy || !!branch || !eligible.length}
          onChange={event => setSelectedSource(event.target.value)}>
          <option value="">请选择固定来源</option>
          {eligible.map(entry => <option key={entry.source_id} value={entry.source_id}>
            {entry.research_id} · {entry.origin} · {entry.source_id.slice(0, 12)}
          </option>)}
        </select></label>
      </div>
      <div className="mechanism-controls">
        <button type="button" disabled={!model || busy || !!branch} onClick={() => void act(async () => {
          if (!model) return;
          const registered = await sourcesApi<Source>('sources', { research_id: model.research_id });
          rememberSource(registered);
          setSelectedSource(registered.source_id);
          setVerified('');
        })}>登记固定来源</button>
        <button type="button" className="quiet" disabled={!source || busy} onClick={() => void act(async () => {
          if (!source) return;
          const confirmed = await sourcesApi<Source>(`sources/${source.source_id}/verify`, {});
          rememberSource(confirmed);
          setVerified(confirmed.source_id);
        })}>校验固定来源</button>
        {source && verified === source.source_id && <span className="mechanism-verified" role="status">已校验固定来源</span>}
      </div>
      {source && <dl className="research-details">
        <dt>固定 Git 提交</dt><dd><code>{source.commit}</code></dd>
        <dt>来源状态</dt><dd>{source.origin} · {source.permission} · {source.engineering_status}</dd>
      </dl>}
      {source && source.warnings.length > 0 && <ul className="mechanism-warnings">{source.warnings.map(warning =>
        <li key={warning}>{sourceWarnings[warning] ?? warning}</li>)}</ul>}
    </section>

    <section className="card" aria-labelledby="mechanism-parameters">
      <h2 ref={setupHeading} tabIndex={-1} id="mechanism-parameters">合成参数</h2>
      {branch && <div className="mechanism-branch">
        <strong>从父快照续算</strong>
        <dl className="research-details">
          <dt>父实验 ID</dt><dd><code>{branch.runId}</code></dd>
          <dt>父快照 SHA-256</dt><dd><code>{branch.snapshot}</code></dd>
          <dt>恢复状态</dt><dd>{timeLabel(branch.timeKind)} {branch.time} · <code>{branch.values}</code></dd>
        </dl>
        <button type="button" className="quiet" disabled={busy} onClick={() => chooseModel(selectedModel)}>清除父快照</button>
      </div>}
      <form onSubmit={event => {
        event.preventDefault();
        void act(async () => {
          if (!model || !source) return;
          const parameters = parseDraft(draft, replicator);
          rememberRun(await request<Run>('experiments', {
            model_id: model.model_id, model_version: model.version, source_id: source.source_id,
            parameters, ...(branch ? { branch_from: branch.runId } : {}),
          }));
          if (branch) setBranch(null);
        });
      }}>
        <fieldset className="mechanism-fields" disabled={!model || busy}>
          <div className={`mechanism-grid ${replicator ? 'mechanism-grid-three' : ''}`}>
            <label>合成预设<select value={preset} disabled={!!branch} onChange={event => {
              const key = event.target.value;
              setPreset(key);
              if (presets[key]) setDraft(previous => ({ ...previous, vector: presets[key].vector, matrix: presets[key].matrix }));
            }}>
              {Object.entries(presets).map(([key, entry]) => <option key={key} value={key}>{entry.label}</option>)}
              <option value="custom">自定义参数</option>
            </select></label>
            {replicator && <label>动力学方法<select value={draft.method} onChange={event => {
              const method = event.target.value as Method;
              setDraft(previous => ({ ...previous, method,
                steps: method === 'eq3' && Number(previous.steps) > 8 ? '4' : previous.steps }));
            }}>
              {(['eq3', 'euler', 'rk4'] as const).map(method => <option key={method} value={method}
                disabled={!!branch && ((method === 'eq3') !== (branch.timeKind === 'discrete-generation'))}>
                {methodLabel(method)}
              </option>)}
            </select></label>}
            <label>步数<input type="number" min={1} max={maximumSteps} value={draft.steps} required
              onChange={event => setDraft({ ...draft, steps: event.target.value })}/></label>
          </div>
          <p className="muted">分数示例 <code>1/4</code>。向量用逗号分隔，矩阵每行用换行分隔。</p>
          <div className="mechanism-grid">
            <div>
              <label>{replicator ? '初始比例' : '初始意见'}<input type="text" value={draft.vector} readOnly={!!branch} required
                onChange={event => { setDraft({ ...draft, vector: event.target.value }); setPreset('custom'); }}/></label>
              {replicator && draft.method !== 'eq3' && <label>积分步长<input type="text" value={draft.stepSize} required
                onChange={event => setDraft({ ...draft, stepSize: event.target.value })}/></label>}
            </div>
            <label>{replicator ? '收益矩阵' : '权重矩阵'}<textarea rows={3} value={draft.matrix} required
              onChange={event => { setDraft({ ...draft, matrix: event.target.value }); setPreset('custom'); }}/></label>
          </div>
          {replicator && <p className="muted">{draft.method === 'eq3'
            ? 'Eq. 3 按离散世代计算，使用精确分数。'
            : '通过所选方法积分连续 Eq. 2，保留数值误差及诊断。'}</p>}
          <button disabled={!source || maximumSteps < 1}>提交机制实验</button>
        </fieldset>
      </form>
    </section>

    {current && <section className="card" aria-labelledby="mechanism-selected">
      <div className="section-heading"><h2 id="mechanism-selected">所选机制实验</h2><Status value={current.status}/></div>
      <dl className="research-details">
        <dt>实验 ID</dt><dd><code>{current.id}</code></dd>
        <dt>计算方法</dt><dd>{methodLabel(runMethod(current))}</dd>
        <dt>配置 SHA-256</dt><dd><code>{current.config_sha256}</code></dd>
        {current.config.branch_from && <><dt>父实验 ID</dt><dd><code>{current.config.branch_from}</code></dd></>}
      </dl>
      <div className="mechanism-controls">
        {current.status === 'PENDING' && <button disabled={busy} onClick={() => void act(async () => {
          rememberRun(await request<Run>(`experiments/${current.id}/approve`, {}));
        })}>批准机制执行</button>}
        {activeStatuses.includes(current.status) && <button className="quiet" disabled={busy} onClick={() => void act(async () => {
          rememberRun(await request<Run>(`experiments/${current.id}/cancel`, {}));
        })}>取消机制实验</button>}
      </div>
      {current.error && <p className="error" role="alert">{current.error}</p>}
      {current.logs.length > 0 && <details><summary>查看执行日志</summary><pre>{current.logs.join('\n')}</pre></details>}
    </section>}
    {shownArtifact && current && <MechanismResult key={current.id} artifact={shownArtifact} runId={current.id}
      disabled={busy || (shownArtifact.result.time_kind === 'discrete-round'
        && shownArtifact.result.trajectory.at(-1)?.time === '32')}
      branch={() => startBranch(current.id, shownArtifact)}/>}

    <section className="card" aria-labelledby="mechanism-history">
      <h2 id="mechanism-history">机制实验历史</h2>
      <form className="research-lookup" onSubmit={event => {
        event.preventDefault();
        void act(async () => {
          const run = await request<Run>(`experiments/${encodeURIComponent(lookupId.trim())}`);
          rememberRun(run);
        });
      }}>
        <label>机制实验完整 ID<input value={lookupId} required onChange={event => setLookupId(event.target.value)}/></label>
        <button className="quiet" disabled={busy || !lookupId.trim()}>按 ID 查看机制实验</button>
      </form>
      {runs.length ? <div className="table-wrap"><table aria-label="机制实验记录" className="mechanism-history-table">
        <thead><tr><th>实验 ID</th><th>模型</th><th>方法</th><th>状态</th></tr></thead>
        <tbody>{runs.map(run => <tr key={run.id} className={run.id === selectedId ? 'mechanism-active-row' : ''}>
          <td><button type="button" className="text-button mono" onClick={() => chooseRun(run.id)}>{run.id}</button></td>
          <td>{run.config.model_id} · {run.config.model_version}</td>
          <td>{methodLabel(runMethod(run))}</td><td><Status value={run.status}/></td>
        </tr>)}</tbody>
      </table></div> : <p className="empty">尚无机制实验</p>}
    </section>
    <CompareRuns request={request} runs={runs}/>
  </div>;
}
