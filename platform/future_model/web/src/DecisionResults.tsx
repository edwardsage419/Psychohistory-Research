import { useId, useState } from 'react';
import type { Analysis, DecisionChart, DecisionMethod, DecisionState, DecisionTable } from './decisionTypes';

const statusText: Record<string, string> = {
  feasible: '可行', infeasible: '不可行', unknown: '未知', pass: '满足', fail: '不满足',
  supportive: '支持', selected: '已选用', computed: '已计算', applied: '已应用',
  skipped: '未调用', rejected: '排除', blocked: '待补条件', insufficient: '信息不足',
  unconfirmed: '待确认', clarification: '待澄清', ready: '已分析', complete: '已完成',
  conditional: '有条件', synthetic: '合成演示', user_attested: '用户声明核对，系统未独立验证',
  verified: '旧版用户声明核对，系统未独立验证', conflict: '存在分歧', undecided: '待比较',
  accept: '可行', reject: '不可行', unresolved: '待核实', certain: '证实满足', possible: '可能满足',
  executed: '已执行', ineligible: '不适用', failed: '执行失败', clarify: '待澄清', analyzed: '已分析',
};

const own = <T,>(entries: Record<string, T>, key: string) => Object.hasOwn(entries, key) ? entries[key] : undefined;
const displayStatus = (status: string) => own(statusText, status.toLowerCase()) ?? status;
const valueLabels: Record<string, string> = {
  status: '状态', summary: '摘要', title: '标题', label: '名称', reason: '理由', reasons: '理由',
  conditions: '适用条件', alternatives: '其他方案', tradeoffs: '主要取舍', reversal: '反转条件',
  next_information: '优先补充信息', option_id: '方案', option_ids: '方案',
  method_ids: '依据方法', support: '支持依据', supported_by: '支持依据',
  conflicts: '方法分歧', sources: '来源', source: '来源', assumptions: '假设', limitations: '局限',
  evidence: '证据等级', evidence_status: '证据等级', input: '输入', output: '输出', permission: '许可',
  applicability: '适用范围', failure_conditions: '退出条件', counterexamples: '反例', baseline: '基线',
  formula: '规则', verification: '复算', reference: '参考', message: '说明', field: '字段', prompt: '问题',
};

function hasContent(value: unknown): boolean {
  if (value == null || value === '') return false;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === 'object') return Object.keys(value).length > 0;
  return true;
}

type Names = Record<string, string>;
function Value({ value, names }: { value: unknown; names: Names }) {
  if (!hasContent(value)) return <span className="muted">—</span>;
  if (Array.isArray(value)) return <ul className="decision-values">{value.map((entry, index) => <li key={index}><Value value={entry} names={names}/></li>)}</ul>;
  if (value && typeof value === 'object') return <dl className="decision-value-grid">{Object.entries(value).filter(([, entry]) => hasContent(entry)).map(([key, entry]) => <div key={key}>
    <dt>{own(valueLabels, key) ?? own(names, key) ?? key}</dt><dd><Value value={entry} names={names}/></dd>
  </div>)}</dl>;
  if (typeof value === 'boolean') return <>{value ? '是' : '否'}</>;
  const scalar = String(value);
  return <>{own(names, scalar) ?? displayStatus(scalar)}</>;
}

function Table({ table, names }: { table: DecisionTable; names: Names }) {
  return <div className="table-wrap"><table className="decision-table">
    <caption>{table.title}</caption>
    <thead><tr>{table.columns.map((column, index) => <th key={index} scope="col">{own(names, column) ?? column}</th>)}</tr></thead>
    <tbody>{table.rows.map((row, rowIndex) => {
      const entries = Array.isArray(row) ? row : table.columns.map(column => (row as Record<string, unknown>)?.[column]);
      return <tr key={rowIndex}>{entries.map((entry, columnIndex) => <td key={columnIndex}><Value value={entry} names={names}/></td>)}</tr>;
    })}</tbody>
  </table></div>;
}

function IntervalChart({ chart, names }: { chart: DecisionChart; names: Names }) {
  const chartId = useId();
  const [selected, setSelected] = useState('');
  const rows = chart.rows.map(row => ({ ...row, label: own(names, row.label) ?? row.label }));
  if (!rows.length) return null;
  const plottable = rows.filter(row => row.lower != null && row.upper != null && Number.isFinite(Number(row.lower)) && Number.isFinite(Number(row.upper)));
  const minimum = Math.min(...plottable.map(row => Number(row.lower)));
  const maximum = Math.max(...plottable.map(row => Number(row.upper)));
  const extent = maximum - minimum;
  function position(value: number | string) {
    return extent > 0 ? (Number(value) - minimum) / extent * 100 : 50;
  }
  const selectedRow = selected === '' ? null : rows[Number(selected)];
  return <figure className="decision-interval">
    <figcaption id={chartId}>{chart.title}{chart.unit ? ` · ${chart.unit}` : ''}</figcaption>
    {plottable.length > 0 && <div role="img" aria-labelledby={chartId} aria-label={chart.title} className="decision-plot">
      {rows.map((row, index) => <div className={`decision-plot-row${selected === String(index) ? ' highlighted' : ''}`} key={index}>
        <span>{row.label}</span><div className="decision-plot-track" aria-hidden="true">
          {plottable.includes(row) && <span className="decision-plot-range" style={{ left: `${position(row.lower)}%`, width: `${position(row.upper) - position(row.lower)}%` }}/>}
        </div><span className="decision-range-value">{row.lower ?? '未知'} – {row.upper ?? '未知'}</span>
      </div>)}
      {extent > 0 && <div className="decision-plot-scale" aria-hidden="true"><span/><div><span>{minimum}</span><span>{maximum}</span></div><span/></div>}
    </div>}
    <div className="decision-chart-control">
      <label>查看 {chart.title} 的区间<select value={selected} onChange={event => setSelected(event.target.value)}><option value="">全部方案</option>{rows.map((row, index) => <option key={index} value={index}>{row.label}</option>)}</select></label>
      {selectedRow && <p role="status">{selectedRow.label} · {selectedRow.lower ?? '未知'} 至 {selectedRow.upper ?? '未知'} {chart.unit}</p>}
    </div>
    <details><summary>查看 {chart.title} 数据表</summary><Table table={{ title: chart.title, columns: ['项目', '下界', '上界'], rows: rows.map(row => [row.label, row.lower, row.upper]) }} names={names}/></details>
  </figure>;
}

function Method({ method, names }: { method: DecisionMethod; names: Names }) {
  const { model_id, version, title, status, reasons, result, ...metadata } = method;
  const { summary, tables = [], charts = [], ...details } = result ?? {};
  return <article className="decision-method" data-model-id={model_id}>
    <div className="decision-section-heading"><h4>{title || model_id}</h4><span className="pill" data-status={status}>{displayStatus(status)}</span></div>
    <code className="decision-method-identity">{model_id}@{version}</code>
    {hasContent(reasons) && <div className="decision-method-reasons"><Value value={reasons} names={names}/></div>}
    {hasContent(summary) && <div className="decision-method-summary"><Value value={summary} names={names}/></div>}
    {tables.map((table, index) => <Table key={index} table={table} names={names}/>)}
    {charts.map((chart, index) => <IntervalChart key={index} chart={chart} names={names}/>)}
    {!!Object.keys(details).length && <details><summary>计算细节</summary><Value value={details} names={names}/></details>}
    {!!Object.keys(metadata).length && <details><summary>适用条件、假设与证据来源</summary><Value value={metadata} names={names}/></details>}
  </article>;
}

export type ResultScope = { options: string; methods: string };

export function DecisionResults({ analysis, state, preview, guided, scope, onScope }: {
  analysis: Analysis; state: DecisionState; preview: boolean; guided: boolean; scope: ResultScope; onScope: (scope: ResultScope) => void;
}) {
  const remainingGaps = Array.isArray(analysis.gaps) && analysis.priority_gap
    ? analysis.gaps.filter(gap => gap !== analysis.priority_gap) : analysis.gaps;
  const options = analysis.feasibility.filter(option => scope.options === 'all' || option.status === scope.options);
  const methods = analysis.methods.filter(method => scope.methods === 'all' || method.status === scope.methods);
  const names: Names = Object.fromEntries([...state.options, ...state.constraints, ...state.objectives, ...state.scenarios].map(item => [item.id, item.label]));
  return <div data-analysis-revision={analysis.revision}>
    <section className="card decision-result" aria-labelledby="decision-result-title">
      <div className="decision-section-heading"><div><h2 id="decision-result-title">当前分析</h2><p className="muted">修订 {analysis.revision} · 协调中枢 {analysis.hub_version}{preview ? ' · 自动重算预览' : ''}</p></div><span className="pill" data-status={analysis.status}>{displayStatus(analysis.status)}</span></div>
      {guided && analysis.execution && <p className="decision-execution" data-authorization={analysis.execution.authorization}>外部执行：{analysis.execution.authorization === 'NOT_REQUESTED' ? '未授权' : analysis.execution.authorization} · 实际行动由你决定和执行。</p>}
      <h3>硬约束可行性</h3>
      {guided && analysis.feasibility.length > 0 && <div className="decision-scope">
        <label>选择方案显示范围<select value={scope.options} onChange={event => onScope({ ...scope, options: event.target.value })}>
          <option value="all">全部方案</option><option value="ACCEPT">可行</option><option value="UNRESOLVED">待核实</option><option value="REJECT">不可行</option>
        </select></label><p>显示 {options.length} / {analysis.feasibility.length} 项方案</p>
      </div>}
      {options.length ? <div className="table-wrap"><table className="decision-table"><thead><tr><th scope="col">方案</th><th scope="col">可行性</th><th scope="col">逐项检查</th></tr></thead><tbody>
        {options.map(option => <tr key={option.option_id} data-option-id={option.option_id}><th scope="row">{option.label || own(names, option.option_id)}</th><td><span className="pill" data-status={option.status}>{displayStatus(option.status)}</span></td><td>
          {option.checks.length > 0 && <ul className="decision-values">{option.checks.map(check => <li key={check.constraint_id}>{own(names, check.constraint_id) ?? check.constraint_id} · {displayStatus(check.status)} · {check.reason}</li>)}</ul>}
        </td></tr>)}
      </tbody></table></div> : <p className="muted">{analysis.feasibility.length ? '当前显示范围内没有方案。' : '请先填写候选方案。'}</p>}
      <div className="decision-advice"><h3>条件性建议</h3>{hasContent(analysis.advice) ? <Value value={analysis.advice} names={names}/> : <p>当前信息尚不足以给出建议。</p>}</div>
      {hasContent(analysis.risks) && <><h3>风险与长期影响</h3><Value value={analysis.risks} names={names}/></>}
      {hasContent(analysis.gaps) && <><h3>优先补充的信息</h3>
        {analysis.priority_gap && <p><strong>{analysis.priority_gap}</strong></p>}
        <Value value={remainingGaps} names={names}/>
      </>}
      <details><summary>分析输入摘要</summary><code className="hash">{analysis.input_hash}</code></details>
    </section>
    <section className="card decision-result" aria-labelledby="decision-methods-title"><h2 id="decision-methods-title" tabIndex={-1}>方法审计</h2>
      {guided && <div className="decision-scope">
        <label>选择方法显示范围<select value={scope.methods} onChange={event => onScope({ ...scope, methods: event.target.value })}>
          <option value="all">全部方法</option><option value="EXECUTED">已执行</option><option value="INELIGIBLE">不适用</option><option value="FAILED">执行失败</option>
        </select></label><p>显示 {methods.length} / {analysis.methods.length} 项方法</p>
      </div>}
      {methods.length ? methods.map(method => <Method key={`${method.model_id}@${method.version}`} method={method} names={names}/>) : <p className="muted">{analysis.methods.length ? '当前显示范围内没有方法。' : '当前修订没有可审计的分析方法。'}</p>}
    </section>
  </div>;
}
