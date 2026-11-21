// Run after npm run build. Playwright and the selected browser are supplied by the caller.
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { pathToFileURL } from 'node:url';

const modulePath = process.env.PLAYWRIGHT_MODULE;
const browserName = process.env.MOBILE_BROWSER || 'chromium';
assert.ok(['chromium', 'webkit'].includes(browserName), 'MOBILE_BROWSER must be chromium or webkit');
const playwright = await import(modulePath ? pathToFileURL(modulePath).href : 'playwright');
const dist = new URL('../dist/', import.meta.url);
const release = JSON.parse(await readFile(new URL('release-manifest.json', dist), 'utf8'));
const files = new Map(release.files.map(file => [file.path, file.contentType]));
files.set('sw.js', 'text/javascript');
files.set('release-manifest.json', 'application/json');
const received = [];
const server = createServer(async (request, response) => {
  const path = request.url === '/' ? 'index.html' : request.url.slice(1);
  received.push({ method: request.method, path });
  if (!files.has(path) || request.method !== 'GET') {
    response.writeHead(404).end();
    return;
  }
  try {
    const bytes = await readFile(new URL(path, dist));
    response.writeHead(200, { 'Cache-Control': 'no-store', 'Content-Type': files.get(path) }).end(bytes);
  } catch {
    response.writeHead(503).end();
  }
});

async function closeServer() {
  const closed = once(server, 'close');
  server.close();
  server.closeAllConnections();
  await closed;
}

const passphrase = 'fictional workbench playthrough long password';
const source = '虚构专用数据，仅用于浏览器验收';
const score = (value, unit) => ({ lower: String(value), upper: String(value), unit, kind: 'synthetic', source });
const options = labels => labels.map((label, index) => ({ id: String.fromCharCode(97 + index), label }));
const caseState = (id, question, labels, objective, extra = {}) => ({
  decision_id: id.repeat(32), revision: 1, question,
  deadline: '一个月内', constraints_confirmed: true,
  options: options(labels), objectives: [{ id: 'goal', label: objective, unit: '分', direction: 'max' }],
  ...extra,
});

const career = caseState('a', '我该接受虚构岗位还是留在现有岗位？唤回标记 CAREER_FIXTURE_ONLY',
  ['接受虚构岗位', '留在现有岗位'], '岗位适配', {
    scenario_basis: '同一效用量尺与一个月观察期，效用越高越好',
    scenarios: [
      { id: 'high', label: '适应顺利', kind: 'synthetic', source, utilities: { a: score(9, '效用点'), b: score(6, '效用点') } },
      { id: 'low', label: '适应较慢', kind: 'synthetic', source, utilities: { a: score(1, '效用点'), b: score(5, '效用点') } },
    ],
  });
const learning = caseState('b', '我该报名虚构课程还是按计划自学？唤回标记 LEARNING_FIXTURE_ONLY',
  ['报名虚构课程', '按计划自学'], '学习进度', {
    evidence: [{ id: 'scope', label: '虚构课程进度表', kind: 'synthetic', source, scope: '一个月', verification: 'user_supplied' }],
    options: options(['报名虚构课程', '按计划自学']).map((option, index) => ({
      ...option, scores: { goal: score(['0.3', '0.7'][index], '分') },
    })),
  });
const household = caseState('c', '我该搬进虚构住房还是续租现在的住房？唤回标记 HOUSEHOLD_FIXTURE_ONLY',
  ['搬进虚构住房', '续租现在的住房'], '居住质量', {
    constraints: [{ id: 'budget', label: '每月费用', unit: '元', operator: '<=', threshold: '1600', source }],
    options: options(['搬进虚构住房', '续租现在的住房']).map((option, index) => ({
      ...option, measurements: { budget: score([1700, 1500][index], '元') },
      scores: { goal: score(['0.8', '0.6'][index], '分') },
    })),
  });

async function visible(locator) { await locator.waitFor({ state: 'visible' }); }

async function describeQuestion(page, state, hint) {
  await page.locator('#question').fill(state.question);
  await page.locator('#question-form button[type="submit"]').click();
  const clarification = page.locator('#clarifications');
  await visible(clarification.getByText(hint, { exact: true }));
  for (const { label } of state.options) {
    await visible(clarification.getByText(`${label} · 原文片段`, { exact: true }));
  }
}

async function importState(page, state) {
  const advanced = page.locator('#advanced');
  if (!await advanced.evaluate(node => node.open)) await advanced.locator('summary').click();
  await page.locator('#matrix').fill(JSON.stringify(state, null, 2));
  await page.locator('#apply-json').click();
  await visible(page.locator('#json-message').filter({ hasText: /已将这些条件载入新决策/ }));
  const firstOption = page.locator('#editor').getByLabel('方案 1', { exact: true });
  assert.equal(await firstOption.inputValue(), state.options[0].label);
}

async function enterQuestion(page, state, hint) {
  await describeQuestion(page, state, hint);
  await importState(page, state);
}

async function calculate(page) {
  await page.locator('#confirm-state').check();
  await page.locator('#analyze').click();
  const result = page.locator('#result-content');
  await visible(result.getByRole('table', { name: '硬约束与时间可用性', exact: true }));
  return result;
}

async function verifySaveAffordance(page) {
  const save = page.locator('#save');
  const shortcut = page.locator('#go-to-save');
  await importState(page, career);
  await calculate(page);
  assert.equal(await save.isEnabled() && await shortcut.isEnabled(), true);

  const question = '我该学习虚构木工还是研究虚构绘图？';
  await page.locator('#question').fill(question);
  await page.locator('#question-form button[type="submit"]').click();
  assert.equal(await page.locator('#results').isHidden(), true);
  assert.equal(await page.locator('#result-content').textContent(), '');
  assert.equal(await save.isDisabled() && await shortcut.isDisabled(), true);

  await page.locator('#confirm-state').check();
  await page.locator('#analyze').click();
  await visible(page.locator('#result-content').getByRole('heading', { name: '待澄清', exact: true }));
  assert.equal(await save.isDisabled() && await shortcut.isDisabled(), true);

  await importState(page, career);
  await calculate(page);
  assert.equal(await save.isEnabled() && await shortcut.isEnabled(), true);
  await importState(page, household);
  assert.equal(await page.locator('#results').isHidden(), true);
  assert.equal(await page.locator('#result-content').textContent(), '');
  assert.equal(await save.isDisabled() && await shortcut.isDisabled(), true);
}

async function openEditorSection(page, name) {
  const section = page.locator(`#editor details[data-editor-section="${name}"]`);
  if (!await section.evaluate(node => node.open)) await section.locator('summary').first().click();
  return section;
}

async function credentials(page) {
  await page.locator('#passphrase').fill(passphrase);
  await page.locator('#save-consent').check();
}

async function waitClearedPassphrase(page) {
  await page.waitForFunction(() => document.querySelector('#passphrase')?.value === '');
}

async function save(page) {
  await credentials(page);
  await page.locator('#save').click();
  await visible(page.locator('#message').filter({ hasText: /已加密保存当前决策/ }));
  await waitClearedPassphrase(page);
}

function historyEntry(page, state) {
  return page.locator('#history-list .record-block').filter({ hasText: state.question });
}

async function openRecord(page, state) {
  await page.locator('#passphrase').fill(passphrase);
  await page.locator('#load').click();
  const record = historyEntry(page, state).getByRole('button', { name: '查看记录', exact: true });
  await visible(record);
  await record.click();
  await visible(page.locator('#record-content'));
  await waitClearedPassphrase(page);
  return page.locator('#record-content');
}

async function careerFlow(page) {
  await enterQuestion(page, career, '核对工作内容、合同条件和机会是否仍然可用。');
  const results = await calculate(page);
  const chart = results.locator('figure').filter({ has: page.getByText('最大情景后悔值', { exact: true }) });
  await visible(chart);
  await chart.getByRole('button', { name: '接受虚构岗位：4 至 4 效用点', exact: true }).click();
  await visible(chart.locator('.interval-selection').filter({ hasText: '接受虚构岗位：4 至 4 效用点' }));
  await chart.getByText('查看区间数值表', { exact: true }).click();
  const numbers = chart.getByRole('table', { name: '最大情景后悔值', exact: true });
  await visible(numbers.getByRole('row', { name: '接受虚构岗位 4 4', exact: true }));

  await page.locator('#passphrase').fill(passphrase);
  await page.locator('#save').click();
  await visible(page.locator('#message').filter({ hasText: /请先勾选本次加密保存授权/ }));
  await visible(page.locator('#vault-status').filter({ hasText: /尚无可读取的已授权本机记录/ }));
  await save(page);

  await page.locator('#edit').click();
  const scenarios = await openEditorSection(page, 'scenarios');
  const adapted = scenarios.getByRole('group', { name: '适应较慢', exact: true })
    .getByRole('group', { name: '接受虚构岗位', exact: true });
  await adapted.getByLabel('上界', { exact: true }).fill('4');
  await adapted.getByLabel('下界', { exact: true }).fill('4');
  await calculate(page);
  await visible(chart.getByRole('button', { name: '接受虚构岗位：1 至 1 效用点', exact: true }));
  await save(page);
}

async function prepareLearning(page) {
  await describeQuestion(page, learning, '核对参与条件、时间投入和预期学习成果。');
  await page.getByLabel('最后决定时间（选填）', { exact: true }).fill(learning.deadline);
  const constraints = await openEditorSection(page, 'constraints');
  await constraints.getByLabel('我已确认列出的硬约束，或确认没有硬约束', { exact: true }).check();
  const objectives = await openEditorSection(page, 'objectives');
  await objectives.getByRole('button', { name: '添加目标', exact: true }).click();
  await objectives.getByLabel('目标名称', { exact: true }).fill(learning.objectives[0].label);
  for (const option of learning.options) {
    const group = objectives.getByRole('group', { name: option.label, exact: true });
    await group.getByRole('combobox', { name: '数值类型', exact: true }).selectOption('synthetic');
    await group.getByLabel('下界', { exact: true }).fill(option.scores.goal.lower);
    await group.getByLabel('上界', { exact: true }).fill(option.scores.goal.upper);
    await group.getByLabel('来源或假设依据', { exact: true }).fill(source);
  }
  const evidence = await openEditorSection(page, 'evidence');
  await evidence.getByRole('button', { name: '添加证据', exact: true }).click();
  await evidence.getByLabel('证据名称', { exact: true }).fill(learning.evidence[0].label);
  await evidence.getByRole('combobox', { name: '证据类型', exact: true }).selectOption('synthetic');
  await evidence.getByLabel('来源', { exact: true }).fill(source);
  await evidence.getByLabel('适用范围', { exact: true }).fill(learning.evidence[0].scope);
  await evidence.getByRole('combobox', { name: '核对状态', exact: true }).selectOption('user_supplied');
}

async function learningFlow(page) {
  await prepareLearning(page);
  const result = await calculate(page);
  const table = result.getByRole('table', { name: '逐目标支配关系', exact: true });
  const comparison = table.getByRole('row', { name: /报名虚构课程.*按计划自学/ });
  await visible(comparison.getByRole('cell', { name: '乙保证支配甲', exact: true }));

  await page.locator('#edit').click();
  const objectives = await openEditorSection(page, 'objectives');
  const course = objectives.getByRole('group', { name: '报名虚构课程', exact: true });
  await course.getByLabel('上界', { exact: true }).fill('0.9');
  await course.getByLabel('下界', { exact: true }).fill('0.9');
  await calculate(page);
  await visible(comparison.getByRole('cell', { name: '甲保证支配乙', exact: true }));
  await save(page);
}

async function householdFlow(page) {
  await enterQuestion(page, household, '核对居住条件、完整支出和变更成本。');
  const result = await calculate(page);
  const rows = result.getByRole('table', { name: '硬约束与时间可用性', exact: true });
  const housing = rows.getByRole('row', { name: /搬进虚构住房/ });
  await visible(housing.getByRole('cell', { name: '不通过', exact: true }));
  await visible(rows.getByRole('row', { name: /续租现在的住房/ }).getByRole('cell', { name: '通过', exact: true }));

  await page.locator('#edit').click();
  const constraints = await openEditorSection(page, 'constraints');
  await constraints.getByLabel('阈值', { exact: true }).fill('1800');
  await calculate(page);
  await visible(housing.getByRole('cell', { name: '通过', exact: true }));
  await save(page);
}

async function recordedOutcome(page) {
  const record = await openRecord(page, career);
  assert.equal(await record.locator('#observation').count(), 0, 'Observation was offered before action');
  await record.locator('#chosen-option').selectOption({ label: career.options[0].label });
  await credentials(page);
  await record.locator('#record-action').click();
  await visible(record.locator('#observation'));
  await waitClearedPassphrase(page);

  const outcome = '虚构复盘：实际体验符合预期，未选择方案没有可观察结果。';
  await record.locator('#observation').fill(outcome);
  await record.locator('#review-kind').selectOption('synthetic');
  await credentials(page);
  await record.locator('#record-review').click();
  await visible(record.getByText(outcome, { exact: false }));
  await waitClearedPassphrase(page);
  return outcome;
}

async function offlineReload(page) {
  const response = await page.reload({ waitUntil: 'load' });
  assert.equal(response?.fromServiceWorker(), true, 'Offline navigation bypassed the service worker');
  assert.equal(await page.evaluate(() => navigator.onLine), false);
  assert.equal(await page.locator('#question').inputValue(), '', 'Private question survived reload without unlocking');
  assert.equal(await page.locator('#history-list').isHidden(), true);
}

async function verifySnapshots(record) {
  for (const [revision, expected] of [[1, 4], [2, 1]]) {
    const snapshot = record.locator('details').filter({ hasText: new RegExp(`^修订 ${revision} ·`) });
    await snapshot.locator(':scope > summary').click();
    const chart = snapshot.getByRole('figure', { name: '最大情景后悔值', exact: true });
    await visible(chart.getByRole('button', { name: `接受虚构岗位：${expected} 至 ${expected} 效用点`, exact: true }));
  }
  assert.equal(await record.getByRole('button', { name: '从最新快照编写下一修订', exact: true }).count(), 0,
    'A completed action left its pre-action snapshot editable');
}

async function restoreBackup(page, backup) {
  await page.locator('#privacy').evaluate(details => { details.open = true; });
  await page.locator('#backup-file').setInputFiles({ name: 'workbench-fixture.json', mimeType: 'application/json', buffer: backup });
  await page.locator('#restore-confirm').check();
  await page.locator('#passphrase').fill(passphrase);
  await page.locator('#restore').click();
}

function verifyPrivacy(requests, origin, page) {
  assert.equal(page.url(), origin.href, 'The workbench embedded data in its URL');
  for (const { method, url, postData } of requests) {
    const address = new URL(url);
    const path = address.pathname.slice(1);
    assert.equal(address.origin, origin.origin, 'The workbench requested a remote origin');
    assert.equal(address.search + address.hash, '', 'A request contained URL parameters or fragments');
    assert.ok(path === '' || path === 'favicon.ico' || files.has(path), 'A request escaped the public release file list');
    assert.equal(method, 'GET');
    assert.equal(postData, null);
  }
}

server.listen(0, '127.0.0.1');
await once(server, 'listening');
let browser;
try {
  const origin = new URL(`http://127.0.0.1:${server.address().port}/`);
  browser = await playwright[browserName].launch({
    executablePath: browserName === 'chromium' ? process.env.CHROMIUM_BIN : undefined,
  });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true,
  });
  const requests = [];
  const errors = [];
  const visited = [];
  const browserLogs = [];
  context.on('request', request => requests.push({ url: request.url(), method: request.method(), postData: request.postData() }));
  context.on('weberror', event => errors.push(event.error().message));
  context.on('page', tab => {
    tab.on('websocket', () => errors.push('Unexpected WebSocket connection'));
    tab.on('console', message => browserLogs.push(message.text()));
    tab.on('framenavigated', frame => {
      if (frame === tab.mainFrame()) visited.push(frame.url());
    });
  });
  const page = await context.newPage();
  page.setDefaultTimeout(7000);
  await page.goto(origin.href);
  await page.waitForFunction(() => Boolean(navigator.serviceWorker.controller), undefined, { timeout: 15_000 });
  assert.equal(await page.evaluate(async () => Boolean((await navigator.serviceWorker.ready).active)), true);
  await visible(page.locator('#runtime-status').filter({ hasText: '本机离线资源已准备。' }));
  await closeServer();
  await context.setOffline(true);
  await offlineReload(page);
  const previousDraft = 'BROWSER_HISTORY_FIXTURE_ONLY';
  await page.locator('#question').fill(previousDraft);
  await page.locator('#passphrase').fill(passphrase);
  await page.evaluate(() => {
    history.pushState({ workbench_test: true }, '', location.href);
    history.back();
  });
  await page.waitForFunction(() => !document.querySelector('#question').value && !document.querySelector('#passphrase').value);
  await verifySaveAffordance(page);

  await careerFlow(page);
  console.log('Passed fictional career flow, including interactive chart, value table and recalculation.');
  await learningFlow(page);
  console.log('Passed fictional learning flow using the guided editor, including a changed score and recalculation.');
  await householdFlow(page);
  console.log('Passed fictional household flow, including a changed constraint and feasibility update.');

  await offlineReload(page);
  const outcome = await recordedOutcome(page);
  await offlineReload(page);
  const record = await openRecord(page, career);
  await visible(record.getByText(outcome, { exact: false }));
  await visible(record.getByText('留在现有岗位 · 未观察 (NOT_OBSERVED)', { exact: true }));
  await verifySnapshots(record);
  for (const state of [learning, household]) {
    await visible(historyEntry(page, state));
  }

  await page.locator('#privacy > summary').click();
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.locator('#export').click(),
  ]);
  const backup = await readFile(await download.path());
  const envelope = JSON.parse(backup.toString());
  assert.ok(typeof envelope.ciphertext === 'string' && envelope.ciphertext.length > 0);
  await restoreBackup(page, backup);
  await visible(page.locator('#message').filter({ hasText: /加密备份已通过校验并恢复至本机/ }));

  const plaintext = await page.evaluate(() => JSON.stringify([localStorage, sessionStorage]));
  for (const token of [previousDraft, 'CAREER_FIXTURE_ONLY', 'LEARNING_FIXTURE_ONLY', 'HOUSEHOLD_FIXTURE_ONLY', passphrase, outcome]) {
    assert.equal(plaintext.includes(token), false, 'Private content reached browser Web Storage');
    assert.equal(backup.includes(token), false, 'A personal field was exported as plaintext');
  }

  await visible(record.getByText(outcome, { exact: false }));
  await page.locator('#end-session').click();
  await record.waitFor({ state: 'hidden' });
  await page.locator('#history-list').waitFor({ state: 'hidden' });

  const peer = await context.newPage();
  const peerResponse = await peer.goto(origin.href);
  assert.equal(peerResponse?.fromServiceWorker(), true);
  const peerRecord = await openRecord(peer, career);
  await visible(peerRecord.getByText(outcome, { exact: false }));
  // Keep the other tab foregrounded so a visibility change cannot satisfy these checks.
  await page.locator('#end-session').evaluate(button => button.click());
  await peerRecord.waitFor({ state: 'hidden' });
  await visible(peer.locator('#message').filter({ hasText: /已从另一个标签页锁定并清空会话/ }));
  await openRecord(peer, career);
  await visible(peerRecord.getByText(outcome, { exact: false }));

  await page.locator('#privacy').evaluate(details => { details.open = true; });
  await page.locator('#delete-confirm').evaluate(checkbox => checkbox.click());
  await page.locator('#delete').evaluate(button => button.click());
  await visible(page.locator('#message').filter({ hasText: /已撤回授权并删除/ }));
  await peerRecord.waitFor({ state: 'hidden' });
  await visible(peer.locator('#message').filter({ hasText: /其他标签页已修改本机记录/ }));
  assert.equal(await peer.locator('#question').inputValue(), '');
  assert.equal(await page.locator('#question').inputValue(), '');
  assert.equal(await page.locator('#passphrase').inputValue(), '');
  await restoreBackup(page, backup);
  await visible(page.locator('#message').filter({ hasText: /备份与当前本地授权不匹配/ }));
  assert.equal(await page.locator('#history-list').isHidden(), true);

  verifyPrivacy(requests, origin, page);
  verifyPrivacy(requests, origin, peer);
  for (const address of visited) assert.equal(address, origin.href, 'The workbench navigated with private data in its URL');
  for (const { method, path } of received) {
    assert.equal(method, 'GET');
    assert.ok(path === 'favicon.ico' || files.has(path), 'The server received a non-public path');
  }
  for (const token of [previousDraft, 'CAREER_FIXTURE_ONLY', 'LEARNING_FIXTURE_ONLY', 'HOUSEHOLD_FIXTURE_ONLY', passphrase, outcome]) {
    assert.ok(browserLogs.every(message => !message.includes(token)), 'Private content reached browser console output');
  }
  assert.deepEqual(errors, [], 'Unhandled browser errors');
  console.log(`Passed ${browserName} offline reloads, encrypted history, action and review, backup restore, two-tab lock and revocation, and request privacy.`);
} finally {
  await browser?.close();
  if (server.listening) await closeServer();
}
