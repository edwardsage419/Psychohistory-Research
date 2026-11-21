import { useEffect, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { DecisionApiError, decisionPath } from './decisionTypes';
import type { Analysis, Api, Consent, DecisionRecord, DecisionState, DecisionVersion, HistoryItem, PreferenceSnapshot, PreferenceVersion, RestoreResponse } from './decisionTypes';

import { completePreference, emptyPreference, PreferenceFields } from './DecisionWorkflowInputs';

const endpoint = (name: string) => `${decisionPath}/${name}`;
const timestamp = (value: string) => value ? new Date(value).toISOString() : new Date().toISOString();
const formatTime = (value: string) => new Date(value).toLocaleString();
type Notice = { text: string; error?: boolean };

export function DecisionHistory({ api, version, state, analysis, savedRevision, onSave, onLoad, onClear, onApplyPreference }: {
  api: Api; version: DecisionVersion; state: DecisionState | null; analysis: Analysis | null; savedRevision: number;
  onSave: (state: DecisionState) => void; onLoad: (state: DecisionState) => void; onClear: (decisionId?: string) => void;
  onApplyPreference: (preference: PreferenceVersion) => void;
}) {
  const guided = version === 'v5';
  const [consent, setConsent] = useState<Consent | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [record, setRecord] = useState<DecisionRecord | null>(null);
  const [notice, setNotice] = useState<Notice | null>(null);
  const [busy, setBusy] = useState(false);
  const [confirmation, setConfirmation] = useState<'revoke' | 'delete' | null>(null);
  const [option, setOption] = useState('');
  const [actionAt, setActionAt] = useState('');
  const [observation, setObservation] = useState('');
  const [reviewAt, setReviewAt] = useState('');
  const [reviewKind, setReviewKind] = useState('');
  const [hindsightEvidence, setHindsightEvidence] = useState('');
  const [processQuality, setProcessQuality] = useState('');
  const [hindsightPreference, setHindsightPreference] = useState<PreferenceSnapshot | null>(null);
  const [adoptingReview, setAdoptingReview] = useState<number | null>(null);
  const [preferenceVersions, setPreferenceVersions] = useState<PreferenceVersion[] | null>(null);
  const [preferenceSelection, setPreferenceSelection] = useState<{ decisionId: string; preferenceId: string } | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<{ backup: unknown; report: RestoreResponse } | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const downloadUrls = useRef(new Set<string>());
  useEffect(() => { const urls = downloadUrls.current; return () => { for (const url of urls) URL.revokeObjectURL(url); urls.clear(); }; }, []);
  const latest = record?.snapshots.at(-1);
  const epoch = consent?.authorized ? consent.epoch : null;

  async function refreshHistory(currentEpoch: string) {
    setHistory(await api<HistoryItem[]>(endpoint('history'), { epoch: currentEpoch }, version));
  }
  async function open(decision_id: string, currentEpoch: string) {
    const next = await api<DecisionRecord>(endpoint('record'), { epoch: currentEpoch, decision_id }, version);
    setRecord(next);
    setOption('');
    setActionAt('');
    setObservation('');
    setReviewAt('');
    setReviewKind('');
    setHindsightEvidence('');
    setProcessQuality('');
    setHindsightPreference(null);
    setAdoptingReview(null);
    setConfirmation(null);
  }
  function clearBackup() {
    setFile(null);
    setPreview(null);
    if (fileInput.current) fileInput.current.value = '';
  }
  function clearRecord() {
    setRecord(null);
    setOption('');
    setActionAt('');
    setObservation('');
    setReviewAt('');
    setReviewKind('');
    setHindsightEvidence('');
    setProcessQuality('');
    setHindsightPreference(null);
    setAdoptingReview(null);
    setConfirmation(null);
  }
  function forgetPersonalData(next: Consent) {
    setConsent(next);
    setHistory([]);
    setPreferenceVersions(null);
    setPreferenceSelection(null);
    clearRecord();
    clearBackup();
    onClear();
  }
  async function run(work: () => Promise<void>) {
    setBusy(true);
    setNotice(null);
    try {
      await work();
    } catch (error) {
      if (epoch && error instanceof DecisionApiError && error.status === 403) {
        const latestConsent = await api<Consent>(endpoint('consent'), undefined, version).catch(() => null);
        if (latestConsent && latestConsent.epoch !== epoch) {
          forgetPersonalData(latestConsent);
          if (latestConsent.epoch) await refreshHistory(latestConsent.epoch).catch(() => {});
          setNotice({ text: '本地保存授权已更新，已清空此前会话内容。' });
          return;
        }
      }
      setNotice({ text: error instanceof Error ? error.message : '操作失败，请重试。', error: true });
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    let active = true;
    api<Consent>(endpoint('consent'), undefined, version).then(async next => {
      if (!active) return;
      setConsent(next);
      if (next.authorized && next.epoch) {
        const records = await api<HistoryItem[]>(endpoint('history'), { epoch: next.epoch }, version);
        if (active) setHistory(records);
      }
    }).catch(() => {
      if (active) setNotice({ text: '未能读取本地保存状态。', error: true });
    });
    return () => { active = false; };
  }, [api, version]);

  function save() {
    if (!state || !analysis || !epoch) return;
    void run(async () => {
      await api(endpoint('save'), { epoch, state }, version);
      onSave(state);
      setNotice({ text: '已保存当前修订' });
      await refreshHistory(epoch);
      await open(state.decision_id, epoch);
    });
  }
  function recordAction(event: FormEvent) {
    event.preventDefault();
    if (!epoch || !record || !latest || !option) return;
    void run(async () => {
      await api(endpoint('action'), { epoch, decision_id: record.decision_id, option_id: option, revision: latest.revision, occurred_at: timestamp(actionAt) }, version);
      await open(record.decision_id, epoch);
      setNotice({ text: '已记录实际行动' });
    });
  }
  function appendReview(event: FormEvent) {
    event.preventDefault();
    if (!epoch || !record?.action || !reviewKind || !observation.trim() || (hindsightPreference && !completePreference(hindsightPreference))) return;
    const hindsight = guided && (hindsightEvidence.trim() || processQuality.trim() || hindsightPreference) ? {
      evidence: hindsightEvidence.trim() ? hindsightEvidence : null,
      process_quality: processQuality.trim() ? processQuality : null,
      current_preferences: hindsightPreference,
    } : null;
    void run(async () => {
      await api(endpoint('review'), { epoch, decision_id: record.decision_id, observation, observed_at: timestamp(reviewAt), kind: reviewKind, ...(hindsight ? { hindsight } : {}) }, version);
      await open(record.decision_id, epoch);
      setNotice({ text: '已追加观察回访' });
    });
  }

  async function refreshPreferences(currentEpoch: string) {
    setPreferenceVersions(await api<PreferenceVersion[]>(endpoint('preferences'), { epoch: currentEpoch }, version));
  }
  function adoptPreference(index: number) {
    if (!epoch || !record) return;
    void run(async () => {
      await api<PreferenceVersion>(endpoint('adopt-preferences'), { epoch, decision_id: record.decision_id, review_index: index, confirmed: true }, version);
      await refreshPreferences(epoch);
      await open(record.decision_id, epoch);
      setNotice({ text: '已采纳为未来可选偏好' });
    });
  }

  return <section className="card decision-history" aria-labelledby="decision-history-title">
    <div className="decision-section-heading"><h2 id="decision-history-title">本地决策记录</h2><span className="pill">{epoch ? '已授权' : '仅在页面内存中'}</span></div>
    <p className="muted">需要授权才会把已确认修订、实际行动和观察保存到本机。导出的文件由你保管；删除或撤回只覆盖应用的本地存储。</p>
    <p className="muted">导出的备份文件未经加密，包含个人决策内容。请仅在自己控制的安全位置保存。若本机授权账本完全丢失，当前版本无法将导出自动恢复为可编辑历史，只能人工查阅。删除或撤回也不会清除自行保存的外部副本。</p>
    {notice && <p role={notice.error ? 'alert' : 'status'} className={notice.error ? 'error' : 'decision-notice'}>{notice.text}</p>}
    {!epoch && <button type="button" disabled={consent === null || busy} onClick={() => void run(async () => {
      const next = await api<Consent>(endpoint('consent'), {}, version);
      setConsent(next);
      if (next.epoch) await refreshHistory(next.epoch);
      setNotice({ text: '已授权本地保存' });
    })}>授权本地保存</button>}
    {epoch && <>
      {state?.confirmed && analysis && analysis.status !== 'CLARIFY' && state.revision > savedRevision && <p className="muted">选择「保存当前决策」即确认本修订的底线、方案、目标、权重及依据，并保存事前分析。</p>}
      <div className="decision-actions">
        <button type="button" disabled={busy || !state?.confirmed || !analysis || analysis.status === 'CLARIFY' || state.revision <= savedRevision || (record?.decision_id === state.decision_id && !!record.action)} onClick={save}>保存当前决策</button>
        <button type="button" className="quiet" disabled={busy} onClick={() => void run(async () => {
          const data = await api<unknown>(endpoint('export'), { epoch }, version);
          const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
          downloadUrls.current.add(url);
          const link = document.createElement('a');
          link.href = url;
          link.download = 'personal-decisions-backup.json';
          document.body.appendChild(link);
          link.click();
          link.remove();
          window.setTimeout(() => { URL.revokeObjectURL(url); downloadUrls.current.delete(url); }, 1000);
          setNotice({ text: '已导出本地备份' });
        })}>导出本地备份</button>
        <button type="button" className="quiet decision-danger" disabled={busy || confirmation === 'revoke'} onClick={() => setConfirmation('revoke')}>撤回保存授权</button>
      </div>
      {confirmation === 'revoke' && <div className="decision-confirmation">
        <p>撤回会删除本地决策记录，并清空工作台中的个人信息。</p>
        <div className="decision-actions"><button type="button" className="decision-danger-primary" disabled={busy} onClick={() => void run(async () => {
          const next = await api<Consent>(endpoint('revoke'), { epoch }, version);
          forgetPersonalData(next);
          setNotice({ text: '已撤回保存授权' });
        })}>确认撤回授权</button><button type="button" className="quiet" disabled={busy} onClick={() => setConfirmation(null)}>取消</button></div>
      </div>}
      <h3>已保存决策</h3>
      {!history.length && <p className="muted">当前没有已保存的决策。</p>}
      {history.length > 0 && <ul className="decision-history-list">{history.map(item => <li key={item.decision_id}>
        <button type="button" className="text-button" disabled={busy} onClick={() => void run(() => open(item.decision_id, epoch))}>{item.question}</button><span>修订 {item.revision}</span>
      </li>)}</ul>}
      {record && latest && <section className="decision-record" aria-label="决策记录详情">
        <h3>{latest.state.question}</h3>
        <div className="decision-actions">
          <button type="button" className="quiet" disabled={busy} onClick={() => onLoad(latest.state)}>载入最新修订</button>
          <button type="button" className="quiet decision-danger" disabled={busy || confirmation === 'delete'} onClick={() => setConfirmation('delete')}>删除此决策</button>
        </div>
        {confirmation === 'delete' && <div className="decision-confirmation"><p>删除会移除该决策的修订、实际行动和回访。</p><div className="decision-actions">
          <button type="button" className="decision-danger-primary" disabled={busy} onClick={() => void run(async () => {
            await api(endpoint('delete'), { epoch, decision_id: record.decision_id }, version);
            onClear(record.decision_id);
            clearRecord();
            clearBackup();
            await refreshHistory(epoch);
            if (preferenceVersions) await refreshPreferences(epoch);
            setPreferenceSelection(null);
            setNotice({ text: '已删除此决策' });
          })}>确认删除决策</button>
          <button type="button" className="quiet" disabled={busy} onClick={() => setConfirmation(null)}>取消</button>
        </div></div>}
        <h4>事前确认与版本</h4>
        {record.snapshots.map(snapshot => <details className="decision-snapshot" key={snapshot.revision}><summary>修订 {snapshot.revision} · {formatTime(snapshot.confirmed_at)}</summary>
          <dl className="decision-value-grid"><div><dt>时限</dt><dd>{snapshot.state.deadline}</dd></div><div><dt>方案</dt><dd>{snapshot.state.options.map(item => item.label).join('、')}</dd></div><div><dt>分析</dt><dd>{snapshot.analysis ? `中枢 ${snapshot.analysis.hub_version}` : '恢复后需要重新计算'}</dd></div>{(snapshot.state.intended_option_id || snapshot.state.plan_note) && <div><dt>事前计划</dt><dd>{snapshot.state.options.find(item => item.id === snapshot.state.intended_option_id)?.label}{snapshot.state.plan_note && ` · ${snapshot.state.plan_note}`}</dd></div>}</dl>
          <details><summary>查看确认内容与分析记录</summary><pre>{JSON.stringify({ state: snapshot.state, analysis: snapshot.analysis }, null, 2)}</pre></details>
        </details>)}
        <h4>实际行动</h4>
        {record.action ? <>
          <p>{latest.state.options.find(item => item.id === record.action?.option_id)?.label} · {formatTime(record.action.occurred_at)}</p>
          {latest.state.options.some(item => item.id !== record.action?.option_id) && <p className="muted">未观察：{latest.state.options.filter(item => item.id !== record.action?.option_id).map(item => item.label).join('、')}</p>}
        </> : <form onSubmit={recordAction}>
          <fieldset className="decision-grid decision-event-fields" disabled={busy}>
            <label>实际选择<select value={option} required onChange={event => setOption(event.target.value)}><option value="">请选择实际采取的方案</option>{latest.state.options.map(item => <option value={item.id} key={item.id}>{item.label}</option>)}</select></label>
            <label>行动时间（留空使用当前时间）<input type="datetime-local" value={actionAt} onChange={event => setActionAt(event.target.value)}/></label>
          </fieldset>
          <button type="submit" disabled={busy || !option}>记录实际行动</button>
        </form>}
        {record.action && <><h4>事后观察</h4>
          {record.reviews.length > 0 && <ol className="decision-reviews">{record.reviews.map((review, index) => <li key={index}>
            <span>{review.kind === 'synthetic' ? '合成回访' : '真实观察'} · {formatTime(review.observed_at)}</span><p>{review.observation}</p>
            {guided && review.hindsight?.process_quality && <p><strong>事前流程质量</strong> · {review.hindsight.process_quality}</p>}
            {guided && review.hindsight?.evidence && <p><strong>事后新证据</strong> · {review.hindsight.evidence}</p>}
            {guided && review.hindsight?.current_preferences && <div>
              <p><strong>回访时的偏好</strong> · {review.hindsight.current_preferences.values.map(item => `${item.label}：${item.value}`).join('、')}</p>
              {review.adopted_preferences ? <p className="muted">已采纳为未来可选偏好</p> : adoptingReview === index + 1 ? <div className="decision-confirmation"><p>这会保存一条今后可选用的偏好版本。</p><div className="decision-actions">
                <button type="button" disabled={busy} onClick={() => adoptPreference(index + 1)}>确认采纳为未来偏好</button>
                <button type="button" className="quiet" disabled={busy} onClick={() => setAdoptingReview(null)}>取消采纳</button>
              </div></div> : <button type="button" className="quiet" disabled={busy} onClick={() => setAdoptingReview(index + 1)}>保留此偏好供将来使用</button>}
            </div>}
          </li>)}</ol>}
          <form onSubmit={appendReview}>
            <fieldset className="decision-event-fields" disabled={busy}>
              <label>观察结果<textarea value={observation} required maxLength={6000} onChange={event => setObservation(event.target.value)}/></label>
              <div className="decision-grid">
                <label>回访性质<select value={reviewKind} required onChange={event => setReviewKind(event.target.value)}><option value="">选择观察性质</option><option value="real">真实观察</option><option value="synthetic">合成回访</option></select></label>
                <label>观察时间（留空使用当前时间）<input type="datetime-local" value={reviewAt} onChange={event => setReviewAt(event.target.value)}/></label>
              </div>
              {guided && <details className="decision-disclosure"><summary>记录事后证据与当前偏好</summary>
                <label>事前流程质量<textarea value={processQuality} maxLength={6000} placeholder="回看决定前的信息收集、底线核对和取舍。" onChange={event => setProcessQuality(event.target.value)}/></label>
                <label>事后新证据<textarea value={hindsightEvidence} maxLength={6000} onChange={event => setHindsightEvidence(event.target.value)}/></label>
                {!hindsightPreference ? <button type="button" className="quiet" onClick={() => setHindsightPreference(emptyPreference())}>填写回访时的偏好</button> : <>
                  <PreferenceFields value={hindsightPreference} change={setHindsightPreference}/>
                  <button type="button" className="quiet" onClick={() => setHindsightPreference(null)}>清除回访偏好输入</button>
                </>}
              </details>}
            </fieldset>
            <button type="submit" disabled={busy || !observation.trim() || !reviewKind || !!(hindsightPreference && !completePreference(hindsightPreference))}>追加回访</button>
          </form>
        </>}
      </section>}
      {guided && <section className="decision-restore" aria-label="未来可选偏好">
        <h3>未来可选偏好</h3><p className="muted">每次决策由你单独选用偏好。数值权重需要在对应编辑项确认。</p>
        {!preferenceVersions && <button type="button" className="quiet" disabled={busy} onClick={() => void run(() => refreshPreferences(epoch))}>查看已采纳偏好</button>}
        {preferenceVersions?.length === 0 && <p className="muted">当前没有已采纳偏好。</p>}
        {preferenceVersions?.map(preference => <details className="decision-snapshot" key={preference.version_id}>
          <summary>{preference.preferences.applicability} · {formatTime(preference.adopted_at)}</summary>
          <p>{preference.preferences.provenance} · {preference.source_kind === 'synthetic' ? '合成回访' : '真实回访'}</p>
          <ul>{preference.preferences.values.map(item => <li key={item.label}>{item.label}：{item.value}</li>)}</ul>
          {preferenceSelection?.preferenceId === preference.version_id && preferenceSelection.decisionId === state?.decision_id ? <div className="decision-actions">
            <button type="button" disabled={busy} onClick={() => { onApplyPreference(preference); setPreferenceSelection(null); setNotice({ text: '已选用为本次决策偏好' }); }}>确认用于本次决策</button>
            <button type="button" className="quiet" onClick={() => setPreferenceSelection(null)}>取消选用</button>
          </div> : <button type="button" className="quiet" disabled={busy || !state} onClick={() => state && setPreferenceSelection({ decisionId: state.decision_id, preferenceId: preference.version_id })}>选用此偏好</button>}
        </details>)}
      </section>}
      <section className="decision-restore" aria-labelledby="decision-restore-title">
        <h3 id="decision-restore-title">恢复本地备份</h3>
        <div className="decision-actions"><label>选择备份文件<input ref={fileInput} type="file" accept=".json,application/json" disabled={busy} onChange={event => { setFile(event.target.files?.[0] ?? null); setPreview(null); setNotice(null); }}/></label>
          <button type="button" className="quiet" disabled={busy || !file} onClick={() => void run(async () => {
            if (!file) return;
            if (file.size > 32 * 1024 * 1024) throw new Error('此备份超出网页恢复的 32 MiB 限制。请使用本地命令行恢复。');
            let backup: unknown;
            try { backup = JSON.parse(await file.text()); } catch { throw new Error('请选择有效的 JSON 备份文件。'); }
            const report = await api<RestoreResponse>(endpoint('restore'), { epoch, backup, confirm: false }, version);
            setPreview({ backup, report });
          })}>预览备份</button>
        </div>
        {preview && <div className="decision-preview" aria-label="备份预览">
          <h4>备份预览</h4><p>隔离预览 · {preview.report.eligible ? `可恢复 ${preview.report.decision_count} 项决策` : '此备份无法恢复'}</p>
          {preview.report.reason && <p>{preview.report.reason}</p>}
          <div className="decision-actions">
            <button type="button" disabled={busy || preview.report.isolated !== true || preview.report.eligible !== true} onClick={() => void run(async () => {
              const report = await api<RestoreResponse>(endpoint('restore'), { epoch, backup: preview.backup, confirm: true }, version);
              clearBackup();
              await refreshHistory(epoch);
              if (preferenceVersions) await refreshPreferences(epoch);
              setNotice({ text: `恢复完成 · 写入 ${report.decision_count} 项决策` });
            })}>确认恢复</button>
            <button type="button" className="quiet" disabled={busy} onClick={clearBackup}>关闭预览</button>
          </div>
        </div>}
      </section>
    </>}
  </section>;
}
