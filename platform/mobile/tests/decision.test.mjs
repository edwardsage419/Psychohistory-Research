import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { analyze, registry, start } from '../src/decision.mjs';

test('guidance keeps free text and extracted alternatives provisional', async () => {
  const original = '我该去学设计，还是继续工作？等反馈再决定可以吗？';
  const { state, understanding, plan } = start(original);
  assert.equal(state.question, original);
  assert.deepEqual(state.options, []);
  assert.deepEqual(understanding.suggestions.map(x => x.value), ['去学设计', '继续工作']);
  assert.ok(plan.items.some(x => x.target.field === 'timing'));
  assert.equal((await analyze(state)).status, 'CLARIFY');
});

test('opposing strict limits block comparison until conflicting inputs are resolved', async () => {
  const state = start('我该换工作吗？').state;
  Object.assign(state, {
    confirmed: true, constraints_confirmed: true, deadline: '月末',
    options: [{ id: 'a', label: '换' }, { id: 'b', label: '留' }],
    objectives: [{ id: 'm', label: '余额', unit: '元', direction: 'max' }],
    constraints: [
      { id: 'one', label: '余额', unit: '元', operator: '>', threshold: '1', source: '合成' },
      { id: 'two', label: '余额', unit: '元', operator: '<=', threshold: '1', source: '合成' },
    ],
  });
  const result = await analyze(state);
  assert.equal(result.status, 'CLARIFY');
  assert.ok(result.questions.some(x => /互相冲突/.test(x.prompt)));
  assert.ok(result.methods.every(x => x.status === 'INELIGIBLE' || x.status === 'UNSUPPORTED'));
});

test('registry identifies exact v0.5 version and labels desktop-only candidates', () => {
  assert.equal(registry.find(x => x.model_id === 'C030').version, '1.0.0');
  assert.equal(registry.find(x => x.model_id === 'voi_randomized_certificate').mobile_support, 'UNSUPPORTED');
});

test('analysis identifies the shared capability contract without upgrading its workflow version', async () => {
  const manifest = JSON.parse(readFileSync(new URL('../src/platform-capabilities.json', import.meta.url), 'utf8'));
  const { state } = start('我该换工作吗？');
  const report = await analyze(state);
  assert.deepEqual(report.capability_contract, {
    schema: 'psychohistory.cross-end-capabilities.v1', platform_version: '0.7.0', runtime: 'OFFLINE_PWA',
  });
  assert.equal(report.mobile_version, manifest.mobile.package_version);
  assert.equal(report.hub_version, state.workflow_version);
  assert.deepEqual(report.methods.filter(row => row.status !== 'UNSUPPORTED')
    .map(({ model_id, version }) => ({ model_id, version })), manifest.shared_methods);
});
