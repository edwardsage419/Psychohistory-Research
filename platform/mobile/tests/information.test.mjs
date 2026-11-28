import assert from 'node:assert/strict';
import test from 'node:test';
import { analyze, start } from '../src/decision.mjs';

const value = point => ({ lower: point, upper: point, kind: 'synthetic', source: '复算用合成模型' });
const utility = point => ({ ...value(point), unit: '分' });
const cutoff = (at, inclusive = true) => ({ at, inclusive, kind: 'synthetic', source: '合成窗口' });

function state() {
  return { ...start('我该选甲，还是选乙？').state, confirmed: true, constraints_confirmed: true, deadline: '两天',
    objectives: [{ id: 'value', label: '总效用', unit: '分', direction: 'max' }],
    options: [{ id: 'a', label: '甲' }, { id: 'b', label: '乙' }], scenario_basis: '两天内的同一效用尺度',
    scenarios: [
      { id: 'good', label: '顺利', kind: 'synthetic', source: '合成', utilities: { a: utility(6), b: utility(10) } },
      { id: 'bad', label: '不顺利', kind: 'synthetic', source: '合成', utilities: { a: utility(6), b: utility(0) } },
    ],
    information: { signals: [{ id: 'yes', label: '正' }, { id: 'no', label: '反' }],
      prior: { good: value('.5'), bad: value('.5') },
      likelihoods: { good: { yes: value('.9'), no: value('.1') }, bad: { yes: value('.3'), no: value('.7') } },
      cost: utility('.5'), unrestricted_actions: true, action_source: '合成可行集', timing_basis: '无时间损失' },
  };
}

async function run(input, id) {
  return (await analyze(input)).methods.find(method => method.model_id === id);
}

test('enumerating all four point signal policies gives the same EVSI and threshold', async () => {
  const input = state();
  // Each event weight uses tenths of the sample size doubled to 20.
  const utilities = [[6, 10], [6, 0]];
  const observations = [[9, 3], [1, 7]];
  const weighted = (weights, action) => weights.reduce((sum, weight, i) => sum + weight * utilities[i][action], 0);
  const totals = [0, 1].flatMap(first => [0, 1].map(next => weighted(observations[0], first) + weighted(observations[1], next)));
  const baseline = Math.max(weighted([10, 10], 0), weighted([10, 10], 1)) / 20;
  const expected = Math.max(...totals) / 20;
  const { status, result } = await run(input, 'voi_point');
  assert.equal(status, 'EXECUTED');
  assert.equal(Number(result.baseline_value), baseline);
  assert.equal(Number(result.information_value), expected);
  assert.equal(result.net_value, '0.4');
  assert.deepEqual(result.signals.yes.posterior, { good: '0.75', bad: '0.25' });
  input.information.cost = utility('0.900000000001');
  assert.equal((await run(input, 'voi_point')).result.net_value, '-0.000000000001');
});

test('unreachable states and signals add no utility, posterior or feasibility requirement', async () => {
  const input = state();
  input.scenarios[1] = { id: 'bad', label: '不发生', kind: 'unknown' };
  input.information.prior = { good: value(1), bad: value(0) };
  input.information.likelihoods = { good: { yes: value(1), no: value(0) } };
  input.information.unrestricted_actions = false;
  input.information.actions_by_signal = { yes: { option_ids: ['a'], kind: 'synthetic', source: '调查后仍可行' } };
  const { result } = await run(input, 'voi_point');
  assert.equal(result.evsi, null);
  assert.equal(result.net_value, '-4.5');
  assert.deepEqual(result.signals.no, { probability: '0', actions: [], posterior: null, joint_value: '0' });
  input.information.actions_by_signal.yes.kind = 'unknown';
  assert.equal((await run(input, 'voi_point')).status, 'INELIGIBLE');
});

test('positive-mass timed branches with no available action leave the net value unknown', async () => {
  const input = state();
  input.information = null;
  input.timing = { confirmed: true, time_unit: '天', time_origin: '现在', horizon: cutoff(2),
    decision_deadline: cutoff('.5', false), actions: { a: { switching_cost: value(0) }, b: { switching_cost: value(0) } },
    investigation: { mode: 'joint', kind: 'synthetic', source: '固定的合成联合概率', cost: value('.5'),
      joint: [{ duration: '.5', scenario_id: 'good', signal_id: 'yes', probability: 1 }] },
  };
  const { status, result } = await run(input, 'timing_investigation');
  assert.equal(status, 'EXECUTED');
  assert.equal(result.status, 'UNKNOWN');
  assert.equal(result.net_value, null);
  assert.deepEqual(result.policy[0].availability, { a: 'EXPIRED', b: 'EXPIRED' });
});
