import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeDecision, canonicalDecision } from '../src/decision-contract.mjs';

const base = { decision_id: 'a'.repeat(32), question: '我该选择什么？', revision: 1 };

test('v0.5 defaults and Decimal spellings match the desktop exchange format', () => {
  const state = normalizeDecision({ ...base, constraints: [
    { id: 'limit', label: '最低要求', unit: '分', operator: '>', threshold: '+000.300' },
  ], precision_radius: '1e-7' });
  assert.equal(state.workflow_version, '0.5.0');
  assert.equal(state.constraints[0].threshold, '0.300');
  assert.equal(state.precision_radius, '1E-7');
  assert.equal(state.information, null);
  assert.deepEqual(state.weights, {});
  assert.equal(canonicalDecision({ b: '中文', a: [true, null] }), '{"a":[true,null],"b":"中文"}');
});

test('malformed and contradictory inputs are rejected without including input values', () => {
  assert.throws(() => normalizeDecision({ ...base, confirmed: 'true' }), /confirmed/);
  assert.throws(() => normalizeDecision({ ...base, secret: 'private' }), err => !err.message.includes('private'));
  assert.throws(() => normalizeDecision({ ...base, reference_option_id: 'missing' }), /基准/);
  assert.throws(() => normalizeDecision({ ...base, timing: { wait_duration: { kind: 'unknown', lower: '1' } } }), /未知/);
  assert.throws(() => normalizeDecision({ ...base, precision_radius: '-0.1' }), /precision_radius/);
  assert.throws(() => normalizeDecision({ ...base, precision_radius: '1e-13' }), /precision_radius/);
  assert.throws(() => normalizeDecision({ ...base, evidence: [{ id: 'e', label: '凭证', kind: 'fact', verification: 'VERIFIED' }] }), /verification/);
});

test('numeric bounds normalize on nullable fields and legal map keys stay ordinary identifiers', () => {
  const state = normalizeDecision({ ...base,
    objectives: [{ id: 'lower', label: '低界', unit: '分', direction: 'max' }],
    options: [{ id: 'a', label: '甲', scores: { lower: { lower: 0.5, upper: 1, unit: '分', kind: 'synthetic' } } }],
    timing: { wait_duration: { lower: 0.5, upper: 1, kind: 'synthetic' } },
  });
  assert.equal(state.options[0].scores.lower.lower, '0.5');
  assert.equal(state.timing.wait_duration.upper, '1');
  assert.throws(() => normalizeDecision({ ...base, timing: { wait_duration: { lower: -1, kind: 'synthetic' } } }), /timing/);
  assert.throws(() => normalizeDecision({ ...base, information: { prior: { a: { kind: 'synthetic', lower: '1.01' } } } }), /information/);
});

test('Python whitespace and case-folding rules preserve confirmation boundaries', () => {
  assert.throws(() => normalizeDecision({ ...base, question: '\u0085\u001c' }), /question/);
  assert.throws(() => normalizeDecision({ ...base, preferences: {
    values: [{ label: 'Straße', value: '1' }, { label: 'STRASSE', value: '2' }],
    applicability: '这次', provenance: '用户自述',
  } }), /唯一/);
});
