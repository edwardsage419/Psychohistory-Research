import assert from 'node:assert/strict';
import test from 'node:test';

import * as scoring from '../src/scoring.mjs';

const quantity = (lower, upper = lower, extra = {}) => ({
  lower, upper, unit: 'utility', kind: 'synthetic', source: '合成测试', ...extra,
});
const criteria = ['growth', 'resources'];
function decisions(a, b, extra = {}) {
  return {
    confirmed: true,
    constraints_confirmed: true,
    deadline: '12个月',
    objectives: criteria.map(id => ({ id, label: id, unit: 'utility', direction: 'max' })),
    options: [a, b].map((scores, i) => ({
      id: i === 0 ? 'a' : 'b', label: i === 0 ? 'A' : 'B',
      scores: Object.fromEntries(scores.map((value, j) => [criteria[j], value])),
    })),
    weights_confirmed: true,
    weights: {
      growth: { lower: '.60', upper: '.65' },
      resources: { lower: '.35', upper: '.40' },
    },
    score_basis: '合成共同基数效用刻度',
    score_dependence: 'rectangle',
    score_dependence_source: '合成矩形假设',
    score_transform: 'identity',
    ...extra,
  };
}

test('contradictory measures of the same metric prevent acceptance', () => {
  const gate = scoring.feasibility({
    constraints_confirmed: true,
    deadline: '一年',
    constraints: ['a', 'b', 'c'].map(id => ({
      id, label: id === 'c' ? '另外的指标' : '同一指标', unit: 'utility',
      operator: '>=', threshold: 1, source: '合成阈值',
    })),
    options: [{ id: 'x', label: 'X', measurements: { a: quantity(2), b: quantity(3), c: quantity(1) } }],
  });
  assert.equal(gate.status, 'EXECUTED');
  assert.equal(gate.result.feasibility[0].status, 'UNRESOLVED');
  assert.deepEqual(gate.result.feasibility[0].checks.map(check => check.status), ['UNKNOWN', 'UNKNOWN', 'CERTAIN_PASS']);
});

test('Pareto permits distinct objective horizons but weighted models require one common horizon', () => {
  const state = decisions(
    [quantity('.8', '.8', { horizon: '三个月' }), quantity('.4')],
    [quantity('.5', '.5', { horizon: '三个月' }), quantity('.8')],
  );
  assert.equal(scoring.score(state).result.status, 'COMPARABLE_BY_OBJECTIVE');
  assert.equal(scoring.dominance(state).result.pairs[0].relation, 'INCOMPARABLE');
  assert.equal(scoring.sensitivity(state).status, 'INELIGIBLE');
});

test('fixed-score weights preserve the exact rational tie threshold', () => {
  const state = decisions([quantity('.8'), quantity('.4')], [quantity('.5'), quantity('.8')], {
    weights: Object.fromEntries(criteria.map(id => [id, { lower: '.3', upper: '.7' }])),
  });
  const pair = scoring.sensitivity(state, { model_id: 'weight_sensitivity' }).result.pairs[0];
  assert.deepEqual(pair.threshold, { objective: 'growth', value: '4/7' });
  assert.deepEqual([pair.lower, pair.upper, pair.relation], ['-0.19', '0.09', 'UNRESOLVED']);
  assert.deepEqual(pair.possible_outcomes, ['B_LEADS', 'TIE', 'A_LEADS']);
});

test('C034 preserves a rectangular endpoint tie and supplies replayable witnesses', () => {
  const state = decisions(
    [quantity('.79', '.81'), quantity('.39', '.41')],
    [quantity('.49', '.51'), quantity('.79', '.81')],
  );
  const pair = scoring.sensitivity(state).result.pairs[0];
  assert.deepEqual([pair.lower, pair.upper, pair.relation], ['0', '0.075', 'UNRESOLVED']);
  assert.deepEqual(pair.score_radius_threshold, { preferred: 'a', strict_upper: '0.01' });
  assert.deepEqual(pair.minimum, {
    weights: { growth: '0.6', resources: '0.4' },
    a_scores: { growth: '0.79', resources: '0.39' },
    b_scores: { growth: '0.51', resources: '0.81' },
  });
});

test('C034 clipping preserves outer bounds and only reports feasible witnesses for documented rectangular offsets', () => {
  const state = decisions([quantity('.8'), quantity('.4')], [quantity('.5'), quantity('.8')], {
    score_dependence: 'shared_additive',
    score_transform: 'clip_01',
    shared_offsets: Object.fromEntries(criteria.map(id => [id, { lower: '-.3', upper: '.3' }])),
  });
  const outer = scoring.sensitivity(state).result.pairs[0];
  assert.deepEqual([outer.lower, outer.upper, outer.relation, outer.bounds], ['-0.04', '0.09', 'UNKNOWN', 'outer']);
  assert.equal(outer.minimum, undefined);
  const sharp = scoring.sensitivity({ ...state, shared_offset_dependence: 'rectangle' }).result.pairs[0];
  assert.deepEqual(sharp.minimum.offsets, { growth: '0.3', resources: '-0.3' });
  assert.deepEqual(sharp.minimum.a_scores, { growth: '1', resources: '0.1' });
});

function scenarioDecision(matrix, extra = {}) {
  const options = Object.keys(matrix).map(id => ({ id, label: id.toUpperCase() }));
  const scenarios = Object.values(matrix)[0].map((_, index) => ({
    id: `s${index + 1}`, label: `S${index + 1}`, kind: 'synthetic', source: '合成情景',
    utilities: Object.fromEntries(options.map(({ id }) => [id, quantity(...[].concat(matrix[id][index]))])),
  }));
  return {
    confirmed: true, constraints_confirmed: true, deadline: '一年',
    options, scenarios, scenario_basis: '相同量尺、观察范围，效用越高越好',
    scenario_dependence: 'rectangle', scenario_dependence_source: '合成矩形假设', ...extra,
  };
}

test('C030 computes interval regret against competitors and treats touching bounds as inconclusive', () => {
  const state = scenarioDecision({ a: [[7, 9], [1, 3]], b: [[5, 6], [5, 6]], c: [[2, 3], [7, 9]] });
  const result = scoring.regret(state).result;
  assert.equal(result.bound_type, 'sharp');
  assert.deepEqual(result.worst_regret_bounds, { a: ['4', '8'], b: ['1', '4'], c: ['4', '7'] });
  assert.deepEqual(result.leaders, ['b']);
  assert.deepEqual(result.strict_leaders, []);
  assert.deepEqual(result.midpoint_leaders, ['b']);
});

test('C030 preserves an outer claim without a rectangular source and assigns no regret against self', () => {
  const state = scenarioDecision({ a: [[1, 3]] }, { scenario_dependence_source: null });
  const result = scoring.regret(state).result;
  assert.equal(result.bound_type, 'outer');
  assert.deepEqual(result.worst_regret_bounds, { a: ['0', '0'] });
  assert.deepEqual(result.strict_leaders, []);
});

test('C029 keeps ties and rejects intervals or missing evidence', () => {
  const options = { model_id: 'C029' };
  const state = scenarioDecision({ a: [5, 1, 1], b: [1, 5, 5], c: [5, 0, 0] });
  const result = scoring.regret(state, options).result;
  assert.deepEqual(result.leaders, ['a', 'b']);
  assert.deepEqual(result.scenario_best, [['a', 'c'], ['b'], ['b']]);
  assert.deepEqual(result.worst_scenarios.a, ['S2', 'S3']);
  assert.equal(scoring.regret(scenarioDecision({ a: [[1, 2]] }), options).status, 'INELIGIBLE');
  state.scenarios[0].utilities.a.source = '';
  assert.equal(scoring.regret(state, options).status, 'INELIGIBLE');
});

test('C031 retains an exclusive precision threshold and provides the declared rectangular counterexample', () => {
  const state = scenarioDecision({ a: [8, 2], b: [5.5, 5.5], c: [2.5, 8] }, { precision_radius: '.75' });
  const result = scoring.regret(state, { model_id: 'C031' }).result;
  assert.deepEqual(result.precision_threshold, { option_id: 'b', upper_exclusive: '0.75' });
  assert.deepEqual(result.strict_leaders, []);
  assert.equal(result.sharp_threshold, true);
  assert.deepEqual(result.witness.worst_regret, { a: '7.5', b: '4', c: '4' });
});

test('all regret rows use only the vetted current-feasibility subset', () => {
  const state = scenarioDecision({ a: [8, 2], b: [5, 5], late: [100, 100] });
  const { result } = scoring.regret(state, { model_id: 'C029', feasible: state.options.slice(0, 2) });
  assert.deepEqual(result.regret, { a: ['0', '3'], b: ['3', '0'] });
});

test('direct model calls cannot use pending or rejected candidates supplied by a caller', () => {
  const state = scenarioDecision({ a: [8], b: [5] });
  state.constraints = [{ id: 'c', label: '条件', unit: 'utility', operator: '>=', threshold: 0, source: '合成测试' }];
  state.options[0].measurements = { c: quantity(1) };
  state.options[1].measurements = { c: quantity(-1) };
  assert.equal(scoring.regret(state, { feasible: state.options }).status, 'INELIGIBLE');
});

test('weighted methods retain assumptions that need confirmation when fewer than two options qualify', () => {
  const state = decisions([quantity('.8'), quantity('.4')], [quantity('.5'), quantity('.8')], {
    score_basis: null, weights_confirmed: false,
  });
  const result = scoring.sensitivity(state, { feasible: state.options.slice(0, 1) });
  assert.equal(result.status, 'INELIGIBLE');
  assert.equal(result.result, null);
  assert.equal(result.reasons.length, 3);
});

test('Python whitespace cannot supply missing hard-constraint evidence', () => {
  const state = {
    constraints_confirmed: true,
    deadline: '一年',
    constraints: [{
      id: 'threshold', label: '条件', unit: 'utility',
      operator: '>=', threshold: 1, source: '\u0085\u001f',
    }],
    options: [{ id: 'a', label: 'A', measurements: { threshold: quantity(1) } }],
  };
  const check = scoring.feasibility(state).result.feasibility[0];
  assert.equal(check.status, 'UNRESOLVED');
  assert.equal(check.checks[0].status, 'UNKNOWN');
});

test('Python whitespace around utility units and horizons preserves comparability', () => {
  const state = scenarioDecision({ a: [1], b: [2] });
  Object.assign(state.scenarios[0].utilities.a, { unit: '\u0085utility', horizon: '一年\u001f' });
  const result = scoring.regret(state, { model_id: 'C029' });
  assert.equal(result.status, 'EXECUTED');
  assert.deepEqual(result.result.leaders, ['b']);
});
