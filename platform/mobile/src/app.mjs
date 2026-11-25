import { analyze, normalizeDecision, start } from './decision.mjs';
import { offlineModelStatus, refreshIntake, resolveClaim, respond } from './decision-intake.mjs';
import {
  exportEncryptedBlob, loadAuthorizedRecordWithVersion, localRecordStatus, removeLocalRecord,
  restoreEncryptedBlob, saveAuthorizedRecord,
} from './vault.mjs';
import { button, check, drawEditor, element, input, sampleQuestion, sampleState, select } from './ui-input.mjs';
import { display, drawClarifications, drawIntake, drawResult } from './ui-output.mjs';

const $ = id => document.getElementById(id);
const freshId = () => crypto.randomUUID().replaceAll('-', '');
const ARCHIVE = 'psychohistory-mobile-workbench-1';
const MAX_STATE_BYTES = 16 * 1024 * 1024;
let draft;
let intake;
let guidance;
let computed;
let archive;
let recordId;
let session = 0;
let edit = 0;
let busy = false;
let workerRequest = 0;
let vaultStatusRequest = 0;

function message(id, content, error = false) {
  const node = $(id);
  node.textContent = content;
  node.dataset.error = String(error);
}

function focus(id) {
  $(id)?.focus();
}

function focusStage(id) {
  const heading = $(id);
  heading.focus({ preventScroll: true });
  heading.closest('section').scrollIntoView({ block: 'start' });
}

function clearAnalysis() {
  computed = null;
  $('results').hidden = true;
  $('result-content').replaceChildren();
  $('save').disabled = true;
  $('go-to-save').disabled = true;
}

function changed() {
  const record = archive?.records.find(item => item.decision_id === draft?.decision_id);
  if (record && !record.action && record.snapshots.at(-1)?.state.revision === draft.revision) draft.revision++;
  edit++;
  $('confirm-state').checked = false;
  clearAnalysis();
  message('analysis-message', '');
}

function jump(field, target = {}) {
  if (field === 'methods') {
    focus('method-results');
    return;
  }
  if (field === 'confirmed') {
    focus('confirm-state');
    return;
  }
  const details = Array.from($('editor').querySelectorAll('details')).find(node => node.dataset.editorSection === field);
  if (details) {
    details.open = true;
    const id = target.constraint_id ?? target.objective_id ?? target.scenario_id ?? target.evidence_id;
    const row = Array.from(details.querySelectorAll('[data-item-id]')).find(node => node.dataset.itemId === id);
    const option = Array.from((row || details).querySelectorAll('[data-option-id]')).find(node => node.dataset.optionId === target.option_id);
    const part = Array.from(details.querySelectorAll('[data-target-part]')).find(node => node.dataset.targetPart === target.part);
    ((option || row || part || details).querySelector('input, select, button') || details.querySelector('summary'))?.focus();
    return;
  }
  const index = { options: 0, intent: 1, deadline: 2 }[field];
  if (field === 'options') {
    $('editor').querySelector('.option-list input, .option-list + button')?.focus();
  } else if (index) {
    $('editor').querySelectorAll(':scope > div > .editor-grid input')[index - 1]?.focus();
  } else {
    focus('clarify-title');
  }
}

function renderIntake() {
  drawIntake($('intake'), intake, text => {
    try {
      intake = respond(draft, intake, text);
      renderIntake();
      message('intake-message', '已检查这次补充。请核对新增线索。');
      focus('intake-message');
    } catch (error) {
      message('intake-message', error.message, true);
    }
  }, (id, action, correction) => {
    try {
      const result = resolveClaim(draft, intake, id, action, correction);
      if (action === 'reject') {
        intake = result.intake;
        renderIntake();
      } else {
        const open = Array.from($('editor').querySelectorAll('details[open][data-editor-section]'),
          section => section.dataset.editorSection);
        showDraft(result.state, { ...guidance, intake: result.intake, open, moveFocus: false });
      }
      message('intake-message', action === 'reject' ? '已略过这一线索。' : '已采用草稿条件。计算前仍须核对。');
      focus('intake-message');
    } catch (error) {
      message('intake-message', error.message, true);
    }
  });
}

function showDraft(state, { understanding, questions, plan, intake: nextIntake, open = [], moveFocus = true } = {}) {
  draft = state;
  intake = nextIntake;
  guidance = { understanding, questions, plan };
  changed();
  $('question').value = state.question;
  $('clarify').hidden = false;
  $('editor').replaceChildren();
  drawEditor($('editor'), draft, () => {
    changed();
    if (intake) {
      intake = refreshIntake(draft, intake);
      renderIntake();
    }
  }, open);
  renderIntake();
  drawClarifications($('clarifications'), understanding, questions, plan, jump);
  if (moveFocus) focusStage('clarify-title');
}

function begin(question, demo = false) {
  const preparation = start(question);
  const state = demo ? sampleState(preparation.state) : preparation.state;
  message('question-message', '');
  showDraft(state, { ...preparation, intake: demo ? null : preparation.intake, open: demo ? [] : ['constraints'] });
}

function clearSession(notice = '') {
  session++;
  edit++;
  busy = false;
  draft = archive = recordId = intake = guidance = undefined;
  for (const id of ['question', 'matrix', 'passphrase', 'state-file', 'backup-file']) $(id).value = '';
  for (const id of ['confirm-state', 'save-consent', 'restore-confirm', 'delete-confirm']) $(id).checked = false;
  for (const id of ['intake', 'clarifications', 'editor', 'history-list', 'record-content']) $(id).replaceChildren();
  for (const id of ['intake', 'clarify', 'history-list', 'record-content']) $(id).hidden = true;
  for (const id of ['advanced', 'privacy']) $(id).open = false;
  for (const id of ['question-message', 'json-message', 'analysis-message']) message(id, '');
  clearAnalysis();
  message('message', notice);
}

$('question-form').addEventListener('submit', event => {
  event.preventDefault();
  try { begin($('question').value); }
  catch (error) { message('question-message', error.message, true); }
});
$('question').addEventListener('input', () => {
  if (!draft || $('question').value === draft.question) return;
  changed();
  intake = undefined;
  renderIntake();
  $('clarify').hidden = true;
});
$('demo').addEventListener('click', () => begin(sampleQuestion, true));
$('mobile-model-status').textContent = offlineModelStatus.message;
$('back-to-question').addEventListener('click', () => focus('question'));
$('edit').addEventListener('click', () => focusStage('clarify-title'));
$('go-to-save').addEventListener('click', () => focus('passphrase'));
$('confirm-state').addEventListener('change', event => {
  if (!event.target.checked) clearAnalysis();
});

$('analyze').addEventListener('click', async () => {
  if (!$('confirm-state').checked) {
    message('analysis-message', '请先核对条件、假设和资料。', true);
    focus('confirm-state');
    return;
  }
  const version = edit;
  const epoch = session;
  try {
    const state = normalizeDecision({ ...draft, confirmed: true });
    const report = await analyze(state);
    if (version !== edit || epoch !== session || !$('confirm-state').checked) return;
    computed = { state, report };
    drawResult($('result-content'), state, report, jump);
    $('results').hidden = false;
    const savable = state.options.length > 0 && report.status !== 'CLARIFY';
    $('save').disabled = !savable;
    $('go-to-save').disabled = !savable;
    message('analysis-message', '已按当前条件完成本机计算。');
    focusStage('result-title');
  } catch (error) {
    if (version === edit && epoch === session) message('analysis-message', `无法计算：${error.message}`, true);
  }
});

$('state-file').addEventListener('change', async () => {
  const epoch = session;
  const file = $('state-file').files[0];
  if (!file) return;
  try {
    if (file.size > MAX_STATE_BYTES) throw new Error('状态文件过大。');
    const raw = await file.text();
    if (session === epoch) $('matrix').value = raw;
  } catch (error) {
    if (session === epoch) message('json-message', error.message, true);
  } finally {
    if (session === epoch) $('state-file').value = '';
  }
});
$('show-json').addEventListener('click', () => {
  if (!draft) {
    message('json-message', '请先整理一个决策问题。', true);
    return;
  }
  $('matrix').value = JSON.stringify({ ...draft, confirmed: false }, null, 2);
  message('json-message', '已将当前条件写入 JSON 编辑器。');
});
$('apply-json').addEventListener('click', () => {
  try {
    const raw = $('matrix').value;
    if (new TextEncoder().encode(raw).length > MAX_STATE_BYTES) throw new Error('状态 JSON 过大。');
    const imported = normalizeDecision(JSON.parse(raw));
    const current = draft?.decision_id === imported.decision_id && draft.question === imported.question && draft.revision === imported.revision
      && JSON.stringify(draft.understanding_receipt) === JSON.stringify(imported.understanding_receipt);
    if (!current) {
      imported.decision_id = freshId();
      imported.revision = 1;
    }
    imported.confirmed = false;
    showDraft(imported);
    message('json-message', current ? '已采用更新的条件，计算前请重新确认。' : '已将这些条件载入新决策，计算前请确认。');
  } catch (error) { message('json-message', `无法采用 JSON：${error.message}`, true); }
});

function verifyArchive(value) {
  if (value?.format !== ARCHIVE || !Array.isArray(value.records) || !Array.isArray(value.preferences)) {
    throw new Error('本机历史格式不兼容。');
  }
  return value;
}

async function readArchive(password, allowMissing = false) {
  if (allowMissing && await localRecordStatus() === 'missing') {
    return { value: { format: ARCHIVE, records: [], preferences: [] }, generation: null };
  }
  const loaded = await loadAuthorizedRecordWithVersion(password);
  return { value: verifyArchive(loaded.value), generation: loaded.generation };
}

let channel;
if ('BroadcastChannel' in globalThis) {
  try {
    channel = new BroadcastChannel('psychohistory-mobile-vault');
    channel.addEventListener('message', event => {
      if (event.data === 'vault-change' || event.data === 'lock-session') externalChange(event.data);
    });
  } catch { /* Older browser contexts can fall back to a storage signal. */ }
}
if (!channel) {
  window.addEventListener('storage', event => {
    if (event.key === 'psychohistory-mobile-vault' && event.newValue) externalChange(event.newValue.split(':')[0]);
  });
}

function externalChange(kind) {
  if (kind === 'lock-session') {
    clearSession('已从另一个标签页锁定并清空会话。');
  } else if (kind === 'vault-change') {
    clearSession('其他标签页已修改本机记录。当前会话已清空。');
    refreshVaultStatus();
  }
}

function broadcast(kind = 'vault-change') {
  if (channel) channel.postMessage(kind);
  else {
    try {
      localStorage.setItem('psychohistory-mobile-vault', `${kind}:${freshId()}`);
      localStorage.removeItem('psychohistory-mobile-vault');
    } catch { /* IndexedDB still enforces storage generation. */ }
  }
}

async function refreshVaultStatus() {
  const request = ++vaultStatusRequest;
  try {
    const status = await localRecordStatus();
    if (request !== vaultStatusRequest) return;
    $('vault-status').textContent = {
      available: '本机有加密记录。输入口令可以解锁。',
      recoverable: '本机记录缺失或已损坏。可校验当前加密备份，也可以撤回授权。',
      missing: '尚无可读取的已授权本机记录。',
    }[status];
  } catch {
    if (request !== vaultStatusRequest) return;
    $('vault-status').textContent = '当前浏览器无法使用本机加密存储。';
  }
}

function runVault(name, handle, { authorization = false, usePassword = true } = {}) {
  if (busy) {
    message('message', '本机正处理另一项存储操作。');
    return;
  }
  const password = $('passphrase').value;
  const authorized = $('save-consent').checked;
  const epoch = session;
  const live = () => epoch === session && !document.hidden;
  if (authorization && !authorized) {
    message('message', '请先勾选本次加密保存授权。', true);
    focus('save-consent');
    return;
  }
  if (usePassword && password.length < 12) {
    message('message', '请输入至少 12 个字符的加密口令。', true);
    focus('passphrase');
    return;
  }
  busy = true;
  $('passphrase').value = '';
  $('save-consent').checked = false;
  message('message', `正在本机处理${name}…`);
  (async () => {
    try { await handle({ password, authorized, live }); }
    catch (error) { if (live()) message('message', `${name}失败：${error.message}`, true); }
    finally {
      if (epoch === session) busy = false;
      refreshVaultStatus();
    }
  })();
}

async function persist(context, update, { allowMissing = false } = {}) {
  const { value, generation } = await readArchive(context.password, allowMissing);
  if (!context.live()) return;
  const feedback = update(value);
  await saveAuthorizedRecord(value, context.password, context.authorized, { expectedGeneration: generation });
  broadcast();
  if (!context.live()) return;
  archive = value;
  if (feedback.recordId) recordId = feedback.recordId;
  drawHistory();
  message('message', feedback.notice);
}

function saveCurrent(archiveValue, { state, report }) {
  if (!state.confirmed || !state.options.length || report.status === 'CLARIFY') {
    throw new Error('请先完成澄清并确认可保存的事前条件。');
  }
  let record = archiveValue.records.find(item => item.decision_id === state.decision_id);
  if (!record) {
    if (state.revision !== 1) throw new Error('未找到前序版本，请将条件载入为新决策。');
    record = { decision_id: state.decision_id, snapshots: [], action: null, reviews: [] };
    archiveValue.records.push(record);
  }
  const last = record.snapshots.at(-1);
  if (record.action) throw new Error('已记录实际行动，事前条件已封存。');
  if (last?.analysis?.input_hash && last.analysis.input_hash === report.input_hash) throw new Error('这份分析已经保存。');
  if (state.revision !== record.snapshots.length + 1) throw new Error('记录已存在，请从历史中的最新快照继续编写下一修订。');
  if (last && (last.state.question !== state.question
    || JSON.stringify(last.state.understanding_receipt) !== JSON.stringify(state.understanding_receipt))) {
    throw new Error('同一决策的修订需保留原始问题与理解凭据。');
  }
  record.snapshots.push({ state, analysis: report, confirmed_at: new Date().toISOString() });
  return { recordId: record.decision_id, notice: '已加密保存当前决策及分析凭据。' };
}

$('save').addEventListener('click', () => {
  if (!computed) return;
  const snapshot = computed;
  runVault('保存', async context => {
    await persist(context, value => saveCurrent(value, snapshot), { allowMissing: true });
    if (context.live() && computed === snapshot) {
      $('save').disabled = true;
      $('go-to-save').disabled = true;
    }
  }, { authorization: true });
});
$('load').addEventListener('click', () => {
  runVault('解锁', async context => {
    const stored = await readArchive(context.password);
    if (!context.live()) return;
    archive = stored.value;
    drawHistory();
    message('message', '已解锁本次会话的本机历史。');
  });
});

function drawHistory() {
  const list = $('history-list');
  list.replaceChildren();
  list.hidden = false;
  element(list, 'h3', '本机历史');
  if (!archive.records.length) element(list, 'p', '这里还没有保存的决策。', 'help');
  for (const record of [...archive.records].reverse()) {
    const latest = record.snapshots.at(-1);
    const row = element(list, 'div', '', 'record-block');
    const label = element(row, 'p', `${latest.state.question} · 修订 ${latest.state.revision}`);
    label.id = `record-${record.decision_id}`;
    const control = button(row, '查看记录', () => { recordId = record.decision_id; drawRecord(); }, 'secondary');
    control.setAttribute('aria-describedby', label.id);
  }
  drawRecord();
}

function datetimeLabel(date = new Date()) {
  const local = new Date(date - date.getTimezoneOffset() * 60000);
  return local.toISOString().slice(0, 19);
}

function timeField(root, title, id) {
  const field = input(root, title, '', () => {});
  field.type = 'datetime-local';
  field.step = '1';
  field.value = datetimeLabel();
  field.id = id;
}

function eventTime(value, earliest) {
  const selected = new Date(value);
  const now = new Date();
  if (!value || !Number.isFinite(+selected) || +selected + 999 < +new Date(earliest) || selected > now) {
    throw new Error('时间须介于相应事前记录与现在之间。');
  }
  return new Date(Math.max(+selected, +new Date(earliest))).toISOString();
}

function actionForm(root, record, snapshot) {
  element(root, 'h3', '记录实际行动');
  const option = select(root, '你实际选择的方案', [['', '请选择'], ...snapshot.state.options.map(item => [item.id, item.label])], '', () => {});
  option.id = 'chosen-option';
  timeField(root, '行动时间（本机时区）', 'action-time');
  const saveAction = button(root, '保存实际行动', () => {
    const chosen = option.value;
    const rawTime = $('action-time').value;
    const target = record.decision_id;
    const revision = snapshot.state.revision;
    runVault('行动记录', context => persist(context, value => {
      const current = value.records.find(item => item.decision_id === target);
      const latest = current?.snapshots.at(-1);
      if (!latest || current.action || latest.state.revision !== revision) throw new Error('记录已更新，请重新解锁。');
      const options = latest.state.options;
      if (!options.some(item => item.id === chosen)) throw new Error('请选择你实际采取的方案。');
      current.action = {
        option_id: chosen, revision,
        occurred_at: eventTime(rawTime, latest.confirmed_at), recorded_at: new Date().toISOString(),
        coverage: Object.fromEntries(options.map(item => [item.id, item.id === chosen ? 'CHOSEN' : 'NOT_OBSERVED'])),
      };
      return { recordId: target, notice: '已加密记录实际行动。' };
    }), { authorization: true });
  });
  saveAction.id = 'record-action';
}

function reviewForm(root, record) {
  element(root, 'h3', '添加事后观察');
  element(root, 'p', '观察只归属于实际选择的方案。未选择方案保持 NOT_OBSERVED。', 'help');
  const observation = input(root, '实际观察到什么？', '', () => {}, { rows: 3, limit: 6000 });
  observation.id = 'observation';
  timeField(root, '观察时间（本机时区）', 'observed-time');
  const kind = select(root, '观察类型', [['', '请选择'], ['real', '真实观察（用户提供）'], ['synthetic', '虚构示例']], '', () => {});
  kind.id = 'review-kind';
  const facts = input(root, '事后才获得的新证据（选填）', '', () => {}, { rows: 2, limit: 6000 });
  const process = input(root, '对事前决策过程的评价（选填）', '', () => {}, { rows: 2, limit: 6000 });
  const preference = input(root, '这次复盘中的当前偏好（选填）', '', () => {});
  const scope = input(root, '偏好适用范围（填写偏好时必填）', '', () => {});
  const adopt = check(root, '我确认把这项当前偏好纳入未来决策的可选记录', false, () => {});
  const saveReview = button(root, '保存事后观察', () => {
    const note = observation.value.trim();
    const rawTime = $('observed-time').value;
    const evidence = facts.value.trim() || null;
    const processQuality = process.value.trim() || null;
    const preferences = preference.value.trim();
    const applicability = scope.value.trim();
    const sourceKind = kind.value;
    const authorizedAdoption = adopt.checked;
    const target = record.decision_id;
    runVault('复盘', context => persist(context, value => {
      const current = value.records.find(item => item.decision_id === target);
      if (!current?.action) throw new Error('请先记录实际行动。');
      if (!note || !['real', 'synthetic'].includes(sourceKind)) throw new Error('请填写观察内容并选择类型。');
      if ((preferences && !applicability) || (authorizedAdoption && !preferences)) throw new Error('请补充当前偏好及其适用范围。');
      const observed_at = eventTime(rawTime, current.action.occurred_at);
      const recorded_at = new Date().toISOString();
      const current_preferences = preferences ? {
        values: [{ label: '当前偏好', value: preferences }], applicability,
        provenance: '用户在事后复盘中主动记录', adopted_version_id: null,
      } : null;
      const review = { observation: note, option_id: current.action.option_id, kind: sourceKind, observed_at, recorded_at };
      if (evidence || processQuality || current_preferences) {
        review.hindsight = { evidence, process_quality: processQuality, current_preferences };
      }
      current.reviews.push(review);
      if (authorizedAdoption) {
        const adoption = {
          version_id: freshId(), adopted_at: recorded_at, decision_id: target,
          review_index: current.reviews.length, source_kind: sourceKind, preferences: current_preferences,
        };
        review.adopted_preferences = adoption;
        value.preferences.push(adoption);
      }
      return { recordId: target, notice: '已加密保存事后观察。' };
    }), { authorization: true });
  });
  saveReview.id = 'record-review';
}

function drawRecord() {
  const root = $('record-content');
  root.replaceChildren();
  const record = archive?.records.find(item => item.decision_id === recordId);
  root.hidden = !record;
  if (!record) return;
  const overview = element(root, 'div', '', 'record-block');
  const snapshot = record.snapshots.at(-1);
  element(overview, 'h3', snapshot.state.question);
  element(overview, 'p', '事前快照', 'stage-label');
  for (const historical of record.snapshots) {
    const details = element(overview, 'details');
    element(details, 'summary', `修订 ${historical.state.revision} · ${new Date(historical.confirmed_at).toLocaleString('zh-CN')}`);
    const body = element(details, 'div');
    details.addEventListener('toggle', () => {
      if (!details.open || body.childElementCount) return;
      drawResult(body, historical.state, historical.analysis);
      const inputs = element(body, 'details');
      element(inputs, 'summary', '查看事前输入');
      element(inputs, 'pre', JSON.stringify(historical.state, null, 2));
    });
  }
  if (!record.action) {
    button(overview, '从最新快照编写下一修订', () => {
      showDraft({ ...structuredClone(snapshot.state), revision: snapshot.state.revision + 1, confirmed: false });
    });
    actionForm(overview, record, snapshot);
  } else {
    const chosen = snapshot.state.options.find(item => item.id === record.action.option_id);
    element(overview, 'p', `实际行动：${chosen?.label} · ${new Date(record.action.occurred_at).toLocaleString('zh-CN')}`);
    const coverage = element(overview, 'ul');
    for (const option of snapshot.state.options) {
      element(coverage, 'li', `${option.label} · ${option.id === chosen?.id ? '已选择' : `${display('NOT_OBSERVED')} (NOT_OBSERVED)`}`);
    }
    for (const review of record.reviews) {
      const item = element(overview, 'div', '', 'record-block');
      element(item, 'h4', `${review.kind === 'synthetic' ? '虚构' : '用户提供的真实'}观察 · ${new Date(review.observed_at).toLocaleString('zh-CN')}`);
      element(item, 'p', review.observation);
      if (review.hindsight?.evidence) element(item, 'p', `事后证据：${review.hindsight.evidence}`);
      if (review.hindsight?.process_quality) element(item, 'p', `过程评价：${review.hindsight.process_quality}`);
      const preference = review.hindsight?.current_preferences;
      if (preference) element(item, 'p', `当前偏好：${preference.values[0].value} · ${preference.applicability}`);
      if (review.adopted_preferences) element(item, 'p', '已经授权作为未来决策可选偏好。', 'help');
    }
    reviewForm(overview, record);
  }
  if (archive.preferences.length) {
    const section = element(root, 'details', '', 'record-block');
    element(section, 'summary', '已授权的未来偏好');
    for (const preference of archive.preferences) {
      const { values, applicability } = preference.preferences;
      const row = element(section, 'div', '', 'record-block');
      element(row, 'p', `${values[0].value} · ${applicability}`);
      button(row, '应用到当前草稿', () => {
        if (!draft || $('clarify').hidden) {
          message('message', '请先整理要应用偏好的新决策。', true);
          return;
        }
        if (preference.source_kind === 'synthetic') {
          message('message', '虚构示例偏好保留在历史中。', true);
          return;
        }
        draft.preferences = { ...structuredClone(preference.preferences), adopted_version_id: preference.version_id };
        showDraft(draft);
        message('message', '已将获授权的偏好加到当前草稿。请重新确认条件。');
      });
    }
  }
}

$('export').addEventListener('click', () => {
  runVault('导出', async context => {
    const encrypted = await exportEncryptedBlob();
    if (!context.live()) return;
    const uri = URL.createObjectURL(new Blob([encrypted], { type: 'application/json' }));
    const anchor = document.createElement('a');
    anchor.href = uri;
    anchor.download = 'psychohistory-mobile-encrypted.json';
    anchor.hidden = true;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(uri), 1000);
    message('message', '已请求下载加密备份。');
  }, { usePassword: false });
});

$('restore').addEventListener('click', () => {
  const file = $('backup-file').files[0];
  const confirmed = $('restore-confirm').checked;
  if (!file || !confirmed) {
    message('message', '请选择加密备份并单独确认恢复。', true);
    return;
  }
  runVault('恢复', async context => {
    $('restore-confirm').checked = false;
    $('backup-file').value = '';
    const raw = await file.text();
    if (!context.live()) return;
    await restoreEncryptedBlob(raw, context.password, confirmed);
    broadcast();
    if (!context.live()) return;
    const restored = await readArchive(context.password);
    if (!context.live()) return;
    archive = restored.value;
    drawHistory();
    message('message', '加密备份已通过校验并恢复至本机。');
  });
});

$('delete').addEventListener('click', () => {
  if (!$('delete-confirm').checked) {
    message('message', '请先单独确认撤回与删除。', true);
    return;
  }
  runVault('撤回与删除', async context => {
    $('delete-confirm').checked = false;
    await removeLocalRecord();
    broadcast();
    if (context.live()) clearSession('已撤回授权并删除本机记录。');
  }, { usePassword: false });
});

$('end-session').addEventListener('click', () => {
  clearSession('本机会话已锁定，页面中的个人资料已清空。');
  broadcast('lock-session');
});
document.addEventListener('visibilitychange', () => { if (document.hidden) clearSession(); });
window.addEventListener('pagehide', () => clearSession());
window.addEventListener('pageshow', event => { if (event.persisted) clearSession(); });
window.addEventListener('popstate', () => clearSession());
window.addEventListener('online', updateNetwork);
window.addEventListener('offline', updateNetwork);

function updateNetwork() {
  $('network').textContent = navigator.onLine ? '本机计算' : '离线';
}

function workerStatus(worker) {
  const status = $('runtime-status');
  const request = ++workerRequest;
  if (!worker) {
    status.textContent = '离线缓存正在准备。';
    return;
  }
  const connection = new MessageChannel();
  const timeout = setTimeout(() => {
    connection.port1.close();
    if (request === workerRequest) status.textContent = '离线缓存状态未确认。';
  }, 2500);
  connection.port1.onmessage = event => {
    clearTimeout(timeout);
    connection.port1.close();
    if (request !== workerRequest) return;
    const value = event.data;
    if (value?.type !== 'mobile-release-status' || !value.ready) {
      status.textContent = '本机离线资源有缺失。请在联网时打开以恢复。';
    } else {
      status.textContent = value.fallback ? '本机使用上一个可用离线版本。' : '本机离线资源已准备。';
    }
  };
  worker.postMessage({ type: 'mobile-release-status' }, [connection.port2]);
}

async function startOffline() {
  const workers = navigator.serviceWorker;
  if (!workers || !globalThis.isSecureContext) {
    $('runtime-status').textContent = '离线安装和加密需要浏览器支持与可信 HTTPS。';
    return;
  }
  const timeout = workers.controller ? undefined : setTimeout(() => {
    $('runtime-status').textContent = '离线安装尚未完成。';
  }, 6000);
  if (workers.controller) workerStatus(workers.controller);
  workers.addEventListener('controllerchange', () => {
    clearTimeout(timeout);
    workerStatus(workers.controller);
  });
  try {
    await workers.register('./sw.js', { updateViaCache: 'none' });
    const registration = await workers.ready;
    clearTimeout(timeout);
    workerStatus(workers.controller || registration.active);
  } catch {
    clearTimeout(timeout);
    if (workers.controller) workerStatus(workers.controller);
    else $('runtime-status').textContent = '离线安装未完成。请核对来源和浏览器的离线存储权限。';
  }
}

updateNetwork();
refreshVaultStatus();
startOffline();
