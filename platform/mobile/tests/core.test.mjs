import test from 'node:test';
import assert from 'node:assert/strict';
import { analyze, decimal, exact, feasibility, informationValue, minimaxRegret, rat } from '../src/core.mjs';
const q = (n, kind='synthetic', unit='points') => ({ lower:String(n), upper:String(n), unit, kind, source:'unseen fixture' });
const p = (n, kind='synthetic') => ({ lower:String(n), upper:String(n), kind, source:'unseen fixture' });
function fixture() { return {
  options:[{id:'a',label:'A',measurements:{income:q(6,'synthetic','USD')}},{id:'b',label:'B',measurements:{income:q(10,'synthetic','USD')}}],
  constraints:[], utility_unit:'points',
  scenarios:[{id:'wet',utilities:{a:q(4),b:q(9)}},{id:'dry',utilities:{a:q(4),b:q(-1)}}],
  information:{signals:[{id:'alert'},{id:'clear'}],prior:{wet:p('.3'),dry:p('.7')},
    likelihoods:{wet:{alert:p('.8'),clear:p('.2')},dry:{alert:p('.2'),clear:p('.8')}},
    cost:q('.3')}
}; }
test('exact rationals preserve decimal information value', () => {
  assert.equal(exact(decimal('0.2')), '0.2');
  assert.equal(exact(rat(1,3)), '1/3');
  assert.equal(exact(decimal('-1.2500')), '-1.25');
});
test('minimax regret finite scenario picks robust a', () => {
  const result=minimaxRegret(fixture());
  assert.equal(result.status,'CONDITIONAL');
  assert.deepEqual(result.worst_regret, {a:'5',b:'5'});
  assert.deepEqual(result.leaders,['a','b']);
});
test('independent event enumeration checks baseline and EVSI', () => {
  const result=informationValue(fixture());
  assert.equal(result.baseline,'4');assert.equal(result.with_information,'4.5');
  assert.equal(result.gross_information_value,'0.5'); assert.equal(result.net_value,'0.2');
  assert.equal(result.status,'INVESTIGATE');assert.equal(result.evidence_status,'SYNTHETIC');
});
test('no investigation distribution is ineligible', () => {
  const s=fixture(); delete s.information;
  assert.equal(analyze(s).information.status,'INELIGIBLE');
});
test('hard income threshold rejects and preserves all options', () => {
  const s=fixture();s.constraints=[{id:'income',threshold:'9',operator:'>=',unit:'USD'}];
  assert.deepEqual(feasibility(s).map(x=>x.status),['REJECT','ACCEPT']);
  assert.equal(minimaxRegret(s).leaders[0],'b');
});
test('strict boundary equality on greater-than becomes rejected',()=>{
  const s=fixture();s.constraints=[{id:'income',threshold:'6',operator:'>',unit:'USD'}];
  assert.deepEqual(feasibility(s).map(x=>x.status),['REJECT','ACCEPT']);
});
test('unknown interval is not silently feasible',()=>{
  const s=fixture();s.constraints=[{id:'income',threshold:'9',operator:'>=',unit:'USD'}];
  s.options[1].measurements.income={lower:'8',upper:'10',unit:'USD',kind:'estimate',source:'rough'};
  assert.deepEqual(feasibility(s).map(x=>x.status),['REJECT','UNRESOLVED']);
  assert.equal(minimaxRegret(s).status,'UNKNOWN');
});
test('unit mismatch is rejected, never converted',()=>{
  const s=fixture();s.scenarios[0].utilities.b.unit='EUR';
  assert.equal(minimaxRegret(s).status,'UNKNOWN');
  assert.equal(informationValue(s).status,'UNKNOWN');
});
test('unknown utility becomes UNKNOWN',()=>{
  const s=fixture();s.scenarios[0].utilities.a.kind='unknown';
  assert.equal(informationValue(s).status,'UNKNOWN');
});
test('non-summing prior probabilities are refused',()=>{
  const s=fixture();s.information.prior.wet=p('.31');
  assert.equal(informationValue(s).status,'UNKNOWN');
});
test('negative survey cost is refused',()=>{
  const s=fixture();s.information.cost=q('-.1');
  assert.equal(informationValue(s).status,'UNKNOWN');
});
test('zero probability signal requires no action policy',()=>{
  const s=fixture();s.information.prior.wet=p('1');s.information.prior.dry=p('0');
  s.information.likelihoods.wet.alert=p('1');s.information.likelihoods.wet.clear=p('0');
  s.information.actions_by_signal={alert:['a'],clear:[]};
  assert.equal(informationValue(s).policy.length,1);
});
test('no feasible action for positive signal is refused',()=>{
  const s=fixture();s.information.actions_by_signal={alert:[],clear:['a']};
  assert.equal(informationValue(s).status,'UNKNOWN');
});
test('cost reversal is exact and negative recommendation abstains',()=>{
  const s=fixture();s.information.cost=q('.8');
  assert.equal(informationValue(s).net_value,'-0.3');
  assert.equal(informationValue(s).status,'ACT_NOW');
});
test('changing user kind never upgrades evidence to VERIFIED',()=>{
  const s=fixture();const i=s.information;
  for(const v of Object.values(i.prior))v.kind='fact';
  for(const row of Object.values(i.likelihoods))for(const v of Object.values(row))v.kind='fact';
  i.cost.kind='fact';for(const sc of s.scenarios)for(const v of Object.values(sc.utilities))v.kind='fact';
  assert.equal(informationValue(s).evidence_status,'CONDITIONAL');
});
test('duplicate option identities are rejected',()=>{
  const s=fixture();s.options[1].id='a';
  assert.throws(()=>feasibility(s),/唯一/);
});
