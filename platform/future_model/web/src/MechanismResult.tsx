import { useEffect, useRef, useState } from 'react';

export type Method = 'eq3' | 'euler' | 'rk4';
export type Parameters = {
  initial: string[]; payoff: string[][]; method: Method; steps: number; step_size?: string;
} | { opinions: string[]; weights: string[][]; steps: number };

export type Source = {
  research_id: string;
  label: string;
  source_id: string;
  commit: string;
  origin: 'MAIN' | 'CANDIDATE';
  permission: string;
  engineering_status: string;
  scientific_status: string;
  warnings: string[];
  files: { role: string; path: string; commit: string; blob: string; sha256: string; size: number }[];
};

export type Config = {
  model_id: string;
  model_version: string;
  source_id: string;
  parameters: Parameters;
  branch_from: string | null;
};

type Point = { time: string; values: (string | number)[] };
type NumericValue = string | number;
type Diagnostic = {
  code: string;
  time?: string;
};

export type Artifact = {
  artifact_sha256: string;
  result: {
    model_id: string;
    model_version: string;
    source: Source;
    scope: string;
    evidence: { kind: string; scope: string; interpretation: string };
    parameters: Parameters;
    time_kind: string;
    method: string;
    trajectory: Point[];
    diagnostics: {
      warnings?: Diagnostic[];
      analytic_reference?: { kind: string; final_first_share?: NumericValue; absolute_error?: NumericValue };
      max_mass_error?: NumericValue;
      product_invariant?: { theoretical_initial: NumericValue; final_drift: NumericValue; max_absolute_drift: NumericValue };
    };
    state: unknown;
    snapshot: { content_hash: string; payload: { parent_hash?: string | null } };
    code_sha256: string;
    input: Config;
  };
};

const methods: Record<string, string> = {
  eq3: '原论文 Eq. 3（精确世代）', euler: '前向 Euler', rk4: '四阶 Runge–Kutta',
  'weighted-average': '固定权重平均',
};

const clocks: Record<string, string> = {
  'discrete-generation': '离散世代', 'continuous-ode': '连续方程时间', 'discrete-round': '离散轮次',
};

export const methodLabel = (value: string) => methods[value] ?? value;
export const timeLabel = (value: string) => clocks[value] ?? value;

const plotColors = ['#167d6a', '#546bb5', '#a46a21'];
const pageSize = 25;

function plottedNumber(value: string | number) {
  if (typeof value === 'number' || !value.includes('/')) return Number(value);
  const [numerator, denominator] = value.split('/');
  const ratio = Number(numerator) / Number(denominator);
  if (Number.isFinite(ratio)) return ratio;
  // Exact Eq. 3 can produce fractions larger than the float range.
  const digits = numerator.replace(/^-/, '');
  const significant = (text: string) => Number(`${text[0]}.${text.slice(1, 16)}`);
  return Math.sign(Number(numerator)) * significant(digits) / significant(denominator)
    * 10 ** (digits.length - denominator.length);
}

function TrajectoryPlot({ data, labels, timeKind }: { data: Point[]; labels: string[]; timeKind: string }) {
  const canvas = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const element = canvas.current;
    const context = element?.getContext('2d');
    if (!element || !context || !data.length) return;
    const { width, height } = element;
    const left = 47, right = width - 23, top = 18, bottom = height - 43;
    const startTime = plottedNumber(data[0].time);
    const duration = plottedNumber(data[data.length - 1].time) - startTime;
    const x = (point: Point) => left + (duration ? (plottedNumber(point.time) - startTime) / duration : 0) * (right - left);
    const y = (value: number) => bottom - value * (bottom - top);
    context.clearRect(0, 0, width, height);
    context.font = '13px system-ui, sans-serif';
    context.lineWidth = 1;
    context.strokeStyle = '#dce4e8';
    context.fillStyle = '#607580';
    context.textAlign = 'right';
    [0, 0.25, 0.5, 0.75, 1].forEach(value => {
      context.beginPath();
      context.moveTo(left, y(value));
      context.lineTo(right, y(value));
      context.stroke();
      context.fillText(String(value), left - 8, y(value) + 4);
    });
    context.textAlign = 'left';
    context.fillText(data[0].time, left, bottom + 21);
    if (duration) {
      context.textAlign = 'right';
      context.fillText(data[data.length - 1].time, right, bottom + 21);
    }
    context.textAlign = 'center';
    context.fillText(timeLabel(timeKind), (left + right) / 2, bottom + 29);
    labels.forEach((_, series) => {
      const color = plotColors[series % plotColors.length];
      context.strokeStyle = color;
      context.fillStyle = color;
      context.lineWidth = 2.5;
      context.beginPath();
      data.forEach((point, index) => {
        const px = x(point), py = y(plottedNumber(point.values[series]));
        if (index === 0) context.moveTo(px, py);
        else context.lineTo(px, py);
      });
      context.stroke();
      const last = data[data.length - 1];
      context.beginPath();
      context.arc(x(last), y(plottedNumber(last.values[series])), 3.5, 0, 2 * Math.PI);
      context.fill();
    });
  }, [data, labels, timeKind]);

  return <figure className="mechanism-plot">
    <canvas ref={canvas} width={920} height={263} role="img" aria-label="机制状态随时间的变化"/>
    <figcaption>{labels.map((label, index) => <span key={label}>
      <span style={{ backgroundColor: plotColors[index % plotColors.length] }} aria-hidden="true"/>{label}
    </span>)}</figcaption>
  </figure>;
}

function TrajectoryTable({ data, labels, timeKind }: { data: Point[]; labels: string[]; timeKind: string }) {
  const [page, setPage] = useState(0);
  const pages = Math.ceil(data.length / pageSize);
  return <>
    <div className="table-wrap">
      <table aria-label={timeKind === 'continuous-ode' ? '数值轨迹' : '精确轨迹'} className="mechanism-trajectory-table">
        <thead><tr><th>{timeLabel(timeKind)}</th>{labels.map(label => <th key={label}>{label}</th>)}</tr></thead>
        <tbody>{data.slice(page * pageSize, (page + 1) * pageSize).map(point => <tr key={point.time}>
          <th scope="row"><code>{point.time}</code></th>
          {point.values.map((value, column) => <td key={column}><code>{String(value)}</code></td>)}
        </tr>)}</tbody>
      </table>
    </div>
    {pages > 1 && <div className="mechanism-controls" aria-label="轨迹分页">
      <button type="button" className="quiet" disabled={page === 0} onClick={() => setPage(page - 1)}>上一页</button>
      <span className="muted">第 {page + 1} / {pages} 页 · {data.length} 个时间点</span>
      <button type="button" className="quiet" disabled={page + 1 >= pages} onClick={() => setPage(page + 1)}>下一页</button>
    </div>}
  </>;
}

export function MechanismResult({ artifact, runId, disabled, branch }: {
  artifact: Artifact; runId: string; disabled: boolean; branch: () => void;
}) {
  const { result } = artifact;
  const series = result.trajectory[0]?.values.map((_, index) =>
    `${result.model_id === 'r123-degroot' ? '意见' : '类型'} ${index + 1}`) ?? [];
  const { analytic_reference: reference, max_mass_error: massError, product_invariant: invariant } = result.diagnostics;
  const warnings = result.diagnostics.warnings ?? [];
  return <section className="card mechanism-result" aria-labelledby="mechanism-result">
    <div className="section-heading">
      <h2 id="mechanism-result">不可变机制结果</h2>
      <span className="pill">{result.scope}</span>
    </div>
    <div className="mechanism-result-facts">
      <div><small>模型与版本</small><strong>{result.source.research_id} · {result.model_version}</strong></div>
      <div><small>计算方法</small><strong>{methodLabel(result.method)}</strong></div>
      <div><small>真实世界证据</small><strong className="unknown">{result.evidence.kind}</strong></div>
    </div>
    {warnings.length > 0 && <ul className="mechanism-warnings">{warnings.map((warning, index) => <li key={index}>
      <strong>{warning.code === 'FALSE_EXTINCTION' ? '数值警告：伪灭绝' : warning.code}</strong>
      {warning.time !== undefined && <span> · 时间 {warning.time}</span>}
    </li>)}</ul>}
    {massError !== undefined && <dl className="research-details">
      <dt>比例总和最大偏差</dt><dd><code>{massError}</code></dd>
      {reference?.kind === 'ANALYTIC' && <>
        <dt>首类型解析终点</dt><dd><code>{reference.final_first_share}</code></dd>
        <dt>终点绝对误差</dt><dd><code>{reference.absolute_error}</code></dd>
      </>}
      {invariant && <>
        <dt>类型比例乘积初值</dt><dd><code>{invariant.theoretical_initial}</code></dd>
        <dt>乘积最大绝对漂移</dt><dd><code>{invariant.max_absolute_drift}</code></dd>
      </>}
    </dl>}
    <TrajectoryPlot data={result.trajectory} labels={series} timeKind={result.time_kind}/>
    <TrajectoryTable data={result.trajectory} labels={series} timeKind={result.time_kind}/>

    <h3>快照与科研溯源</h3>
    <dl className="research-details">
      <dt>实验 ID</dt><dd><code>{runId}</code></dd>
      <dt>结果工件 SHA-256</dt><dd><code aria-label="结果工件 SHA-256">{artifact.artifact_sha256}</code></dd>
      <dt>状态快照 SHA-256</dt><dd><code>{result.snapshot.content_hash}</code></dd>
      {result.input.branch_from && <><dt>父实验 ID</dt><dd><code>{result.input.branch_from}</code></dd></>}
      {result.snapshot.payload.parent_hash && <><dt>父快照 SHA-256</dt><dd><code>{result.snapshot.payload.parent_hash}</code></dd></>}
      <dt>来源 ID</dt><dd><code>{result.source.source_id}</code></dd>
      <dt>来源 Git 提交</dt><dd><code>{result.source.commit}</code></dd>
      <dt>原科研状态</dt><dd>{result.source.scientific_status}</dd>
      <dt>代码 SHA-256</dt><dd><code>{result.code_sha256}</code></dd>
    </dl>
    <button type="button" className="quiet" disabled={disabled} onClick={branch}>从此快照创建分支</button>
    <details>
      <summary>查看来源文件与固定输入</summary>
      <p className="muted">{result.source.origin} · {result.source.permission} · {result.source.engineering_status}</p>
      <div className="table-wrap"><table aria-label="来源文件" className="source-file-table">
        <thead><tr><th>用途与仓库路径</th><th>Git 提交与 blob</th><th>SHA-256</th></tr></thead>
        <tbody>{result.source.files.map(file => <tr key={file.path}>
          <td>{file.role}<br/><code>{file.path}</code></td>
          <td><code>{file.commit}</code><br/><code>{file.blob}</code></td><td><code>{file.sha256}</code></td>
        </tr>)}</tbody>
      </table></div>
      <pre>{JSON.stringify(result.input, null, 2)}</pre>
    </details>
    <details>
      <summary>查看诊断、状态与证据边界</summary>
      <p className="muted">{result.evidence.interpretation}</p>
      <pre>{JSON.stringify(result.diagnostics, null, 2)}</pre>
      <pre>{JSON.stringify(result.state, null, 2)}</pre>
    </details>
  </section>;
}
