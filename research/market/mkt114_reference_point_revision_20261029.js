#!/usr/bin/env node
'use strict';
/* Synthetic preference-point selection and explicit approval/revocation audit.
   Run: node research/market/mkt114_reference_point_revision_20261029.js
   Only deterministic local calculations; no external libraries, user data or services. */
const candidates = [
  {id:'A', money:0, days:8},
  {id:'B', money:40, days:4},
  {id:'C', money:100, days:0},
  {id:'D', money:1000, days:0}
];
let checks=0;
function ok(condition, message) {checks++; if(!condition) throw Error(message);}
function dominates(a,b) {
  return a.money<=b.money && a.days<=b.days &&
         (a.money<b.money || a.days<b.days);
}
function front(items) {
  return items.filter(x=>!items.some(y=>y.id!==x.id && dominates(y,x)));
}
function select(ref, options={}) {
  const {moneyScale=100, dayScale=8, maxDays=null}=options;
  if(moneyScale<=0 || dayScale<=0) throw Error('invalid normalization');
  const feasible=candidates.filter(x=>maxDays===null || x.days<=maxDays);
  if(!feasible.length) return {status:'NO_FEASIBLE',selected:null};
  const pareto=front(feasible);
  const scores=pareto.map(x=>({id:x.id,score:((x.money-ref[0])/moneyScale)**2 +
                                        ((x.days-ref[1])/dayScale)**2}));
  const best=Math.min(...scores.map(x=>x.score));
  const ties=scores.filter(x=>Math.abs(x.score-best)<1e-12);
  return {status:ties.length===1?'SELECTED':'TIE_REQUIRES_HUMAN',
          selected:ties.length===1?ties[0].id:null,
          feasible:feasible.map(x=>x.id),front:pareto.map(x=>x.id),scores};
}
function currentPreference(events) {
  const latest=events.filter(x=>x.type==='APPROVE').at(-1);
  if(!latest) return null;
  return events.some(x=>x.type==='REVOKE' && x.target===latest.id)?null:latest;
}
function result(events) {
  const preference=currentPreference(events);
  return preference?select(preference.ref):{status:'NO_ACTIVE_PREFERENCE',selected:null};
}
function run() {
  ok(JSON.stringify(front(candidates).map(x=>x.id))===JSON.stringify(['A','B','C']),
     'Pareto front');
  for(const [ref,expected] of [ [[0,8],'A'], [[40,4],'B'], [[100,0],'C'],
                                 [[0,0],'B'], [[1000,0],'C'] ]) {
    const r=select(ref);ok(r.status==='SELECTED','selection status');
    ok(r.selected===expected,'reference selection '+JSON.stringify(ref));
    ok(!r.front.includes('D'),'dominated candidate excluded');
  }
  ok(select([0,0],{moneyScale:1000}).selected==='C',
     'reference normalization sensitivity');
  ok(select([0,0],{moneyScale:10000,dayScale:8}).selected==='C',
     'scale sensitivity repeat');
  ok(select([0,0],{moneyScale:10000,dayScale:800}).selected==='B',
     'consistent unit conversion');
  ok(select([0,8],{maxDays:4}).selected==='B','hard delay bound');
  ok(select([0,8],{maxDays:-1}).status==='NO_FEASIBLE','no feasible');
  for(const [ref,days,expected] of [ [[0,8],8,'A'],[[0,8],4,'B'],[[0,8],0,'C'] ])
    ok(select(ref,{maxDays:days}).selected===expected,'hard constraint '+days);
  const events=[{type:'APPROVE',id:'v1',ref:[0,8]}];
  ok(result(events).selected==='A','first approval');
  events.push({type:'APPROVE',id:'v2',ref:[100,0]});
  ok(result(events).selected==='C','second approval');
  events.push({type:'REVOKE',target:'v2'});
  ok(result(events).status==='NO_ACTIVE_PREFERENCE','revocation must stop selection');
  events.push({type:'APPROVE',id:'v3',ref:[0,8]});
  ok(result(events).selected==='A','explicit reapproval');
  events.push({type:'REVOKE',target:'v3'});
  ok(result(events).selected===null,'revoke again');
  ok(result([]).status==='NO_ACTIVE_PREFERENCE','empty approvals');
  ok(select([40,4]).scores.length===3,'front size');
  for(const x of candidates)ok(x.money>=0 && x.days>=0,'valid synthetic candidate');
  const output={checks,failures:0,front:front(candidates).map(x=>x.id),
    reference_choices:{A:select([0,8]).selected,B:select([40,4]).selected,
                       C:select([100,0]).selected,unreachable:select([0,0]).selected},
    scale_flip:{baseline:select([0,0]).selected,changed:select([0,0],{moneyScale:1000}).selected},
    after_revoke:result(events).status};
  process.stdout.write(JSON.stringify(output)+'\n');
}
if(require.main===module) run();
module.exports={select,front,currentPreference,result,run};
