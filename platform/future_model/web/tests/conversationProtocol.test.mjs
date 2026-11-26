import assert from 'node:assert/strict';
import test from 'node:test';
import { acceptConversationView, closingRequest, mutationIdentity, partialObservations } from '../src/conversationProtocol.ts';

const pending = { cancel_nonce: 'nonce-a' };
const active = { session_id: 'session-a', session_instance: 'instance-a', revision: 1 };
const reply = {
  ...active, revision: 2,
  result: { ...active, revision: 2, protocol: '0.8.0', authority_generation: 3, layers: {
    preparation: { sha256: 'b'.repeat(64) },
    partial_calculation: { parent_sha256: 'b'.repeat(64), version: '1.0.0', status: 'DESCRIPTIVE_ONLY' },
  } },
};

test('v0.8 binds every mutation to the revision and distinguishes cancellation from ending', () => {
  assert.deepEqual(mutationIdentity(active, 'v8'), active);
  assert.deepEqual(closingRequest(active, 'v8'), { operation: 'end', body: active });
  assert.deepEqual(closingRequest(active, 'v8', true), { operation: 'discard', body: active });
  assert.deepEqual(closingRequest(pending, 'v8'), { operation: 'cancel-start', body: pending });
  assert.deepEqual(closingRequest(pending, 'v7'), { operation: 'end', body: { session_id: 'nonce-a' } });
  assert.deepEqual(mutationIdentity(active, 'v7'), { session_id: 'session-a', revision: 1 });
});

test('starts bind a request nonce to a server-issued instance', () => {
  const start = { ...active, ...pending, result: { ...active, protocol: '0.8.0', authority_generation: 3 } };
  assert.equal(acceptConversationView(start, null, 'nonce-a', 'v8'), true);
  assert.equal(acceptConversationView(start, null, 'nonce-b', 'v8'), false);
  assert.equal(acceptConversationView({ ...start, session_instance: undefined }, null, 'nonce-a', 'v8'), false);
});

test('authorization cannot migrate to another instance with a matching label and revision', () => {
  const replacement = { ...reply, session_instance: 'instance-b', result: { ...reply.result, session_instance: 'instance-b' } };
  assert.equal(acceptConversationView(replacement, active, null, 'v8'), false);
  assert.equal(acceptConversationView(reply, active, null, 'v8'), true);
  assert.equal(acceptConversationView({ ...reply, result: { ...reply.result, session_instance: 'instance-b' } }, active, null, 'v8'), false);
});

test('partial data must bind to the current instance and stay descriptive', () => {
  const partial_analysis = {
    version: '1.0.0', authority: 'NONE', status: 'DESCRIPTIVE_ONLY', dependency_sha256: 'b'.repeat(64), authority_generation: 3,
    session_id: 'session-a', session_instance: 'instance-a', revision: 2, checks: [],
    differences: [{ label: '现金余额', amount: '100.25', unit: '元', higher_option_label: '方案甲', lower_option_label: '方案乙', horizon: '一个月' }],
  };
  assert.deepEqual(partialObservations({ ...reply, partial_analysis }), ['现金余额相差 100.25 元。方案甲的数值高于方案乙（一个月）。']);
  assert.deepEqual(partialObservations({ ...reply, partial_analysis: { ...partial_analysis, revision: 1 } }), []);
  assert.deepEqual(partialObservations({ ...reply, partial_analysis: { ...partial_analysis, authority: 'SELECT' } }), []);
  assert.deepEqual(partialObservations({ ...reply, partial_analysis: { ...partial_analysis, authority_generation: 2 } }), []);
  assert.deepEqual(partialObservations({ ...reply, partial_analysis: { ...partial_analysis, dependency_sha256: 'c'.repeat(64) } }), []);
});
