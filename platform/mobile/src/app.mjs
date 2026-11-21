import { analyze } from './core.mjs';
import { saveAuthorizedRecord, loadAuthorizedRecord, exportEncryptedBlob, removeLocalRecord } from './vault.mjs';

const $ = id => document.getElementById(id);
const source = '虚构合成算例，未代表任何真实事件';
const value = (n, unit = '效用点') => ({ lower: String(n), upper: String(n), kind: 'synthetic', source, unit, horizon: '同一观察期限' });
const probability = n => ({ lower: String(n), upper: String(n), kind: 'synthetic', source });
const example = () => ({
  options: [{ id: 'stable', label: '稳定选择' }, { id: 'growth', label: '潜在高收益选择' }],
  constraints: [], utility_unit: '效用点',
  scenarios: [
    { id: 'good', label: '有利情景', kind: 'synthetic', source, utilities: { stable: value(4), growth: value(9) } },
    { id: 'bad', label: '不利情景', kind: 'synthetic', source, utilities: { stable: value(4), growth: value(-1) } }
  ],
  information: {
    signals: [{ id: 'positive', label: '正信号' }, { id: 'negative', label: '负信号' }],
    prior: { good: probability('0.3'), bad: probability('0.7') },
    likelihoods: {
      good: { positive: probability('0.8'), negative: probability('0.2') },
      bad: { positive: probability('0.2'), negative: probability('0.8') }
    },
    cost: value('0.3'),
    action_source: source
  }
});
const text = (parent, type, message, className) => {
  const element = document.createElement(type);
  element.textContent = message;
  if (className) element.className = className;
  parent.append(element); return element;
};
function section(parent, heading, details) {
  const root = document.createElement('div'); root.className = 'result-group';
  text(root, 'h3', heading);
  for (const [label, val] of details) text(root, 'p', `${label}：${val}`);
  parent.append(root);
}
function notify(message) { $('message').textContent = message; }
function parsed() {
  const question = $('question').value.trim();
  if (!question) throw new Error('请先输入自然语言决策问题');
  if (question.length > 6000) throw new Error('问题超出允许长度');
  const model = JSON.parse($('matrix').value);
  if (!model || Array.isArray(model) || typeof model !== 'object') throw new Error('模型需为 JSON 对象');
  return { question, model };
}
function render(answer) {
  const root = $('results'); root.replaceChildren(); text(root, 'h2', '分析结果');
  const r = answer.regret;
  section(root, '硬约束与情景后悔', [
    ['状态', r.status], ['条件性最低最坏后悔方案', r.leaders?.join('、') || 'UNKNOWN'],
    ['各方案最坏后悔值', r.worst_regret ? JSON.stringify(r.worst_regret) : (r.reason || '未知')],
    ['单位', r.unit || '待确认']
  ]);
  const list = document.createElement('ul');
  for (const row of (r.checks || [])) text(list, 'li', `${row.label}：${row.status}`);
  root.append(list);
  const i = answer.information;
  section(root, '有限信息价值', [
    ['模型状态', i.status], ['计算前基线', i.baseline ?? 'UNKNOWN'],
    ['调查后信息效用', i.with_information ?? 'UNKNOWN'],
    ['扣除调查成本后的信息净价值', i.net_value ?? 'UNKNOWN'],
    ['数据证据', i.evidence_status || 'UNKNOWN'], ['说明', i.reason || i.summary || '需要调查输入']
  ]);
  text(root, 'p', '所有输出是当前虚构或用户提供条件下的数学结果。未核实数据真实性、现实发生概率或行动结果。', 'help');
  notify('已完成本机计算；本次操作没有访问远程模型或上传数据。');
}
function updateNetwork() {
  $('network').textContent = navigator.onLine ? '可离线计算' : '飞行模式／离线';
}
$('demo').addEventListener('click', () => {
  $('question').value = '如果不确定未来环境，我该选择稳定方案还是可能收益更高的方案？';
  $('matrix').value = JSON.stringify(example(), null, 2);
  $('results').replaceChildren(text(document.createDocumentFragment(), 'p', '示例已载入。请检查所有虚构数据。'));
  notify('已加载完全虚构的双状态算例。');
});
$('analyze').addEventListener('click', () => {
  try { render(analyze(parsed().model)); } catch (error) { notify(`无法计算：${error.message}`); }
});
$('save').addEventListener('click', async () => {
  try {
    const doc = parsed();
    await saveAuthorizedRecord(doc, $('passphrase').value, $('saveConsent').checked);
    notify('已在本机加密保存；口令不会进入存储。');
  } catch (error) { notify(`保存失败：${error.message}`); }
});
$('load').addEventListener('click', async () => {
  try {
    const doc = await loadAuthorizedRecord($('passphrase').value);
    if (typeof doc.question !== 'string' || !doc.model || typeof doc.model !== 'object') throw new Error('记录格式无效');
    $('question').value = doc.question; $('matrix').value = JSON.stringify(doc.model, null, 2);
    notify('已在当前会话解锁本地记录，未发送到网络。');
  } catch (error) { notify(`解锁失败：${error.message}`); }
});
$('export').addEventListener('click', async () => {
  try {
    const ciphertext = await exportEncryptedBlob();
    const file = new Blob([ciphertext], { type: 'application/json' });
    const uri = URL.createObjectURL(file);
    const link = document.createElement('a'); link.href = uri; link.download = 'psychohistory-mobile-encrypted-dev.json';
    link.click(); URL.revokeObjectURL(uri);
    notify('已导出加密副本。当前开发版尚不提供安全恢复入口。');
  } catch (error) { notify(`导出失败：${error.message}`); }
});
$('delete').addEventListener('click', async () => {
  if (!window.confirm('删除此设备的本地加密记录？外部下载文件不会随之删除。')) return;
  try { await removeLocalRecord(); notify('已删除当前应用存储中的加密记录；外部备份不受此操作影响。'); }
  catch (error) { notify(`删除失败：${error.message}`); }
});
window.addEventListener('online', updateNetwork);
window.addEventListener('offline', updateNetwork);
updateNetwork();
if ('serviceWorker' in navigator && globalThis.isSecureContext) {
  navigator.serviceWorker.register('./sw.js').catch(() => notify('离线安装未完成，请核查 HTTPS 或设备限制。'));
}

$('endSession').addEventListener('click', () => {
  $('question').value = ''; $('matrix').value = ''; $('passphrase').value = ''; $('saveConsent').checked = false;
  $('results').replaceChildren();
  text($('results'), 'h2', '分析结果');
  notify('已清理当前页面的输入、口令和可见结果。系统级快照及已下载副本不受控制。');
});
