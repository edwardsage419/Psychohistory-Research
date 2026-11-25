import assert from 'node:assert/strict';
import test from 'node:test';
import { analyze, start } from '../src/decision.mjs';

const intakeModule = () => import('../src/decision-intake.mjs');
const fixture = '我该留在现岗位，还是去新公司？我的目标是积累专业经验。每月收入至少 12000 元。';

function claim(intake, field, role) {
  const result = intake.claims.find(item => item.field === field && (!role || item.role === role));
  assert.ok(result, `Missing ${role ?? ''} ${field}`);
  return result;
}

test('offline intake preserves exact question and stages candidates without authorizing use', async () => {
  const original = `  ${fixture}\n`;
  const { state, intake } = start(original);
  assert.equal(state.question, original);
  assert.equal(intake.phase, 'CLARIFY');
  assert.equal(intake.summary.question, '月收入底线会排除不达标的岗位。两个岗位各自有依据的月收入是多少？');
  assert.ok(intake.summary.conclusion);
  assert.ok(intake.summary.differences.length);
  assert.ok(intake.summary.unknowns.length);
  assert.equal(intake.local_model_status, 'RETIRED');
  assert.equal(intake.local_model_receipt.bridge, 'UNAVAILABLE');
  assert.deepEqual(state.options, []);
  assert.deepEqual(state.constraints, []);
  assert.equal(state.information, null);
  assert.equal(state.weights_confirmed, false);
  assert.deepEqual(intake.claims.filter(item => item.field === 'option').map(item => item.value),
    ['留在现岗位', '去新公司']);
  const income = claim(intake, 'income_min', 'constraint');
  assert.equal(income.status, 'PROVISIONAL');
  assert.equal(income.value, '12000');
  assert.equal(income.unit, 'yuan/month');
  assert.ok(original.includes(income.source));
  assert.equal((await analyze(state)).status, 'CLARIFY');
});

test('user-confirmed correction replaces only a matching constraint and preserves its identity', async () => {
  const { respond, resolveClaim } = await intakeModule();
  const { state, intake } = start(fixture);
  const accepted = resolveClaim(state, intake, claim(intake, 'income_min').id, 'accept');
  const previous = accepted.state.constraints[0];
  assert.equal(previous.threshold, '12000');
  assert.equal(previous.unit, 'yuan/month');
  assert.equal(accepted.state.confirmed, false);
  const next = respond(accepted.state, accepted.intake, '原来收入至少 12000 元，现在把收入底线改为 11500 元。');
  assert.equal(accepted.state.constraints[0].threshold, '12000');
  const changed = claim(next, 'income_min', 'revision');
  const applied = resolveClaim(accepted.state, next, changed.id, 'correct', '11600');
  assert.equal(applied.state.constraints[0].id, previous.id);
  assert.equal(applied.state.constraints[0].threshold, '11600');
  assert.match(applied.state.constraints[0].source, /用户确认更正/);
  assert.equal(applied.intake.claims.find(item => item.id === changed.id).status, 'USER_CONFIRMED');
  assert.equal(claim(applied.intake, 'income_min', 'constraint').status, 'SUPERSEDED');
  assert.equal(applied.state.constraints_confirmed, false);
});

test('conditional, historical, and estimated input never becomes a hard limit', async () => {
  const { resolveClaim } = await intakeModule();
  const { state, intake } = start('如果能退费，预算最多 5000 元。以前最多花 6000 元。预算大概 3000 元。成功率不知道。');
  for (const [kind, value] of [['conditional', '5000'], ['previous', '6000'], ['estimate', '3000']]) {
    const proposal = claim(intake, 'cost_max', kind);
    assert.equal(proposal.value, value);
    assert.throws(() => resolveClaim(state, intake, proposal.id, 'accept'), /只能保留为待核对线索/);
  }
  assert.equal(intake.claims.some(item => item.field === 'probability'), false);
  assert.deepEqual(state.constraints, []);
});

test('a confirmed option and scoped measurement keep unrelated alternatives unknown', async () => {
  const { resolveClaim } = await intakeModule();
  const { state, intake } = start('方案甲：费用 450 元；方案乙：每周学习 3 小时。预算最多 500 元。');
  const first = resolveClaim(state, intake, intake.claims.find(item => item.value === '方案甲').id, 'accept');
  const second = resolveClaim(first.state, first.intake, intake.claims.find(item => item.value === '方案乙').id, 'accept');
  const bounded = resolveClaim(second.state, second.intake, claim(intake, 'cost_max').id, 'accept');
  const cost = claim(intake, 'cost', 'measurement');
  assert.equal(cost.subject, '方案甲');
  const measured = resolveClaim(bounded.state, bounded.intake, cost.id, 'accept');
  assert.equal(Object.values(measured.state.options[0].measurements)[0].lower, '450');
  assert.deepEqual(measured.state.options[1].measurements, {});
});

test('rejecting a candidate changes only intake status and keeps the missing field visible', async () => {
  const { resolveClaim } = await intakeModule();
  const { state, intake } = start(fixture);
  const income = claim(intake, 'income_min');
  const rejected = resolveClaim(state, intake, income.id, 'reject');
  assert.deepEqual(rejected.state, state);
  assert.equal(rejected.intake.claims.find(item => item.id === income.id).status, 'DISMISSED');
  assert.match(rejected.intake.summary.question, /哪些行动确实可选/);
});

test('ambiguous budgets and periods are not silently converted into limits', () => {
  const { intake } = start('预算至少 3000 元。这个月开销是 500 元。每月预算最多 700 元。');
  assert.deepEqual(intake.claims.filter(item => item.field === 'cost_max' && item.role === 'constraint')
    .map(({ value, unit }) => [value, unit]), [['700', 'yuan/month']]);
});

test('a revision affects only its explicitly named metric', async () => {
  const { respond } = await intakeModule();
  const { state, intake } = start(fixture);
  const latest = respond(state, intake, '每周工时不超过 42 小时，现在月收入底线改为 11500 元。');
  assert.deepEqual(latest.claims.filter(item => item.role === 'revision').map(item => [item.field, item.value]),
    [['income_min', '11500']]);
});

test('foreign currency stays out of a yuan-denominated calculation', () => {
  const { intake } = start('我该留在原岗位，还是去新公司？每月收入至少 12000 美元。');
  assert.equal(intake.claims.some(candidate => candidate.field === 'income_min'), false);
});

test('a future deadline is not treated as historical merely because it says before', async () => {
  const { resolveClaim } = await intakeModule();
  const { state, intake } = start(`${fixture}周五之前必须决定。`);
  const date = claim(intake, 'deadline', 'deadline');
  assert.equal(date.value, '周五之前');
  assert.equal(resolveClaim(state, intake, date.id, 'accept').state.deadline, '周五之前');
});

test('a short answer fills only the option and units identified by the next question', async () => {
  const { respond, resolveClaim } = await intakeModule();
  let turn = start('我该留在虚构岗位甲，还是接受虚构岗位乙？每周最多到岗两天。');
  for (const item of [...turn.intake.claims]) {
    turn = resolveClaim(turn.state, turn.intake, item.id, 'accept');
  }
  const { state, intake } = turn;
  assert.equal(intake.summary.focus, 'onsite:留在虚构岗位甲');
  const proposal = claim(respond(state, intake, '一天。'), 'onsite', 'measurement');
  assert.equal(proposal.subject, '留在虚构岗位甲');
  assert.equal(proposal.value, '1');
  assert.equal(proposal.unit, 'days/week');
  assert.equal(start('一天。').intake.claims.length, 0);
});
