'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict');
const lines=fs.readFileSync('research/R202/R202_ALL_96_ORIGINAL_CENSORED_TRAINING_WORLDS.csv','utf8').trim().split(/\r?\n/);
const headers=lines.shift().split(',');
const csv=lines.map(s=>Object.fromEntries(s.split(',').map((v,i)=>[headers[i],v])));
const receipt=JSON.parse(fs.readFileSync('research/validation/R202_HORIZON_TRANSPORT_24_WORLDS_384_EXACT_RECEIPT_2026-10-27.json','utf8'));
const gcd=(a,b)=>b===0n?a:gcd(b,a%b);
function F(x){if(Array.isArray(x))return x;let [n,d='1']=String(x).split('/').map(BigInt);if(d<0n){n=-n;d=-d}const g=gcd(n<0n?-n:n,d);return [n/g,d/g]}
const add=(a,b)=>F(`${a[0]*b[1]+b[0]*a[1]}/${a[1]*b[1]}`);
const sub=(a,b)=>add(a,[-b[0],b[1]]);
const mul=(a,b)=>F(`${a[0]*b[0]}/${a[1]*b[1]}`);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],key=a=>`${a[0]}/${a[1]}`;
const ZERO=F(0),ONE=F(1),BASE=[1,2,4,8].map(F),CAND=[F(1),F('1/2'),F(2)];
const checks={source:0,fit:0,row:0,world:0,mass:0,negatives:0};
function test(a,b,kind){assert.ok(eq(F(a),F(b)),`${kind}: ${a} != ${b}`);checks[kind]++}
function probability(a,H){const h=F(H);return F(`${BASE.filter(t=>{const z=mul(t,a);return z[0]*h[1]<=h[0]*z[1]}).length}/4`)}
function likelihood(a,exposed,observed,flag,cutoff){
 const c=F(cutoff),count=BASE.filter(t=>{
 const z=exposed?mul(t,a):t,occurred=z[0]*c[1]<=c[0]*z[1];
 return eq(occurred?z:c,F(observed))&&Number(occurred)===Number(flag)
 }).length;return F(`${count}/4`)
}
const receiptRows=new Map(receipt.rows.map(r=>[[r.true_a,r.C,r.H,r.source_x0_T0,r.source_x1_T0].join('|'),r]));
const worlds=new Map();
for(const r of csv){
 const a=F(r.true_time_scale_a),C=Number(r.administrative_censor_time),x0=F(r.original_x0_baseline_T0),x1=mul(F(r.original_x1_baseline_T0),a),c=F(C);
 const event0=x0[0]*c[1]<=c[0]*x0[1],event1=x1[0]*c[1]<=c[0]*x1[1];
 test(event0?x0:c,r.x0_visible_time,'source');
 assert.equal(Number(event0),Number(r.x0_event_flag));
 assert.equal(Number(event1),Number(r.x1_event_flag));
 assert.ok(eq(event1?x1:c,F(r.x1_visible_time)));
 const scores=CAND.map(t=>mul(likelihood(t,0,r.x0_visible_time,r.x0_event_flag,C),likelihood(t,1,r.x1_visible_time,r.x1_event_flag,C)));
 const maximum=scores.reduce((v,t)=>t[0]*v[1]>v[0]*t[1]?t:v,ZERO);
 const fitted=CAND[scores.findIndex(s=>eq(s,maximum))];
 test(fitted,r.selected_a,'fit');
 for(const H of receipt.horizons){
  const id=[r.true_time_scale_a,C,H,r.original_x0_baseline_T0,r.original_x1_baseline_T0].join('|'),z=receiptRows.get(id);
  assert.ok(z,`missing ${id}`);
  const p=probability(a,H),q=probability(fitted,H),risk=add(mul(p,mul(sub(ONE,q),sub(ONE,q))),mul(sub(ONE,p),mul(q,q)));
  for(const [field,expected] of [['p',p],['q',q],['expected_brier',risk],['fitted_a',fitted],['source_weight',F('1/16')]])test(z[field],expected,'row');
  const w=[r.true_time_scale_a,C,H].join('|');
  if(!worlds.has(w))worlds.set(w,{mass:ZERO,risk:ZERO,selected:new Map()});
  const item=worlds.get(w);
  item.mass=add(item.mass,F('1/16'));item.risk=add(item.risk,mul(F('1/16'),risk));
  item.selected.set(key(fitted),add(item.selected.get(key(fitted))||ZERO,F('1/16')));
 }
}
for(const w of receipt.worlds){
 const id=[w.true_a,w.C,w.H].join('|'),item=worlds.get(id);assert.ok(item);
 const p=probability(F(w.true_a),w.H),q=probability(F(1),w.H);
 const baseline=add(mul(p,mul(sub(ONE,q),sub(ONE,q))),mul(sub(ONE,p),mul(q,q))),oracle=mul(p,sub(ONE,p));
 for(const [field,expected] of [['source_mass',item.mass],['selected_brier',item.risk],['null_brier',baseline],['oracle_brier',oracle],['oracle_gap',sub(item.risk,oracle)],['selected_minus_null',sub(item.risk,baseline)]])test(w[field],expected,'world');
 for(const [a,v] of Object.entries(w.selected_a_mass))test(v,item.selected.get(key(F(a)))||ZERO,'mass');
}
assert.ok(!eq(add(F('1/16'),F('1/64')),F('1/16')));checks.negatives++;
assert.ok(!eq(F('3/16'),F('1/4')));checks.negatives++;
assert.equal(csv.length,96);assert.equal(receipt.rows.length,384);assert.equal(receipt.worlds.length,24);
assert.equal(Object.values(checks).reduce((a,b)=>a+b,0),2310);
console.log(JSON.stringify({checks,total:2310,failures:0,scope:'internal exact E1'}));
