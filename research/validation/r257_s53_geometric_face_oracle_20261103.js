#!/usr/bin/env node
'use strict';
// Independent exact rational face-enumeration audit. Node.js standard library.
const fs=require('node:fs');
const PARAMS={
 INTERIOR_OFF_GRID:['1','3/5','1/5'],BINDING_SUM_BOTH:['1','3/4','3/4'],
 LOWER_X_ACTIVE:['1','-1/2','1/2'],LOWER_Y_ACTIVE:['1','1/2','-1/2'],
 VERTEX_ORIGIN:['1','-1/2','-1/2'],VERTEX_RIGHT:['1','2','1/4'],
 VERTEX_UPPER:['1','1/4','2'],CAPACITY_TWO_SLACK:['2','3/4','3/4']
};
const DELTAS=['-1/4','-1/16','0','1/16','1/4'], STEPS=['1/4','1/16'];
function need(ok,why){if(!ok)throw Error(why)}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);need(d!==0n,'zero denominator');if(d<0n){n=-n;d=-d}let g=gcd(n,d);return {n:n/g,d:d/g}}
function q(s){if(s&&typeof s==='object'&&typeof s.n==='bigint')return s;need(typeof s==='string'&&/^-?\d+(?:\/[1-9]\d*)?$/.test(s),'invalid rational');let [a,b]=s.split('/');return F(a,b||'1')}
function add(a,b){a=q(a);b=q(b);return F(a.n*b.d+b.n*a.d,a.d*b.d)}
function neg(a){a=q(a);return F(-a.n,a.d)}
function sub(a,b){return add(a,neg(b))}
function mul(a,b){a=q(a);b=q(b);return F(a.n*b.n,a.d*b.d)}
function div(a,b){a=q(a);b=q(b);return F(a.n*b.d,a.d*b.n)}
function cmp(a,b){a=q(a);b=q(b);let v=a.n*b.d-b.n*a.d;return v<0n?-1:v>0n?1:0}
function clamp(v,lo,hi){return cmp(v,lo)<0?lo:cmp(v,hi)>0?hi:v}
function fmt(a){a=q(a);return a.d===1n?String(a.n):String(a.n)+'/'+String(a.d)}
function score(x,y,a,b){let u=sub(x,a),v=sub(y,b);return add(mul(u,u),mul(v,v))}
function solve(C,a,b){
 let z=q('0');need(cmp(C,z)>0,'capacity');
 let x=clamp(div(add(sub(a,b),C),q('2')),z,C);
 let candidates=[[z,clamp(b,z,C)],[clamp(a,z,C),z],[x,sub(C,x)]];
 if(cmp(a,z)>=0&&cmp(b,z)>=0&&cmp(add(a,b),C)<=0)candidates.push([a,b]);
 let best=candidates[0],v=score(...best,a,b);
 for(let p of candidates.slice(1)){let w=score(...p,a,b);if(cmp(w,v)<0){best=p;v=w}}
 return {x:best[0],y:best[1],v};
}
function equal(actual,expected,label){need(cmp(q(actual),expected)===0,label+' mismatch')}
function keyed(rows,key,expected,label){
 need(Array.isArray(rows)&&rows.length===expected.length,label+' length');
 let m=new Map();
 for(let row of rows){
  need(row&&typeof row==='object'&&!Array.isArray(row),label+' row');
  let k=fmt(q(row[key]));need(expected.includes(k)&&!m.has(k),label+' duplicate/unknown '+k);m.set(k,row)
 }
 return m;
}
function audit(data){
 need(data&&data.research_id==='R257_S53'&&data.evidence==='E1','receipt identity');
 need(data.new_human_E2===0&&data.new_history_E3===0,'evidence class');
 need(data.nonconvex_negative_control==='KKT_stationary_0_vs_feasible_-1/4','control label');
 need(Array.isArray(data.worlds)&&data.worlds.length===8,'world count');
 let seen=new Set(),counts={worlds:0,coordinates:0,capacities:0,minimums:0,slopes:0,secants:0},diagnostics=[];
 for(let world of data.worlds){
  let name=world.world;need(Object.hasOwn(PARAMS,name)&&!seen.has(name),'duplicate/unknown world');
  seen.add(name);counts.worlds++;
  let [C0,a,b]=PARAMS[name].map(q);
  equal(world.baseline_capacity,C0,name+' baseline C');counts.capacities++;
  let rows=keyed(world.perturbations,'delta',DELTAS,name+' deltas'),vals=new Map();
  for(let delta of DELTAS){
   let row=rows.get(delta),C=add(C0,q(delta)),s=solve(C,a,b);
   equal(row.capacity,C,name+' capacity '+delta);counts.capacities++;
   need(Array.isArray(row.point)&&row.point.length===2,'point arity');
   equal(row.point[0],s.x,name+' x '+delta);counts.coordinates++;
   equal(row.point[1],s.y,name+' y '+delta);counts.coordinates++;
   equal(row.minimum,s.v,name+' value '+delta);counts.minimums++;
   vals.set(delta,s.v);
  }
  equal(world.baseline_minimum,vals.get('0'),name+' baseline value');counts.minimums++;
  let eps=q('1/4096');
  let slope=div(sub(solve(add(C0,eps),a,b).v,solve(sub(C0,eps),a,b).v),mul(q('2'),eps));
  equal(world.local_derivative,slope,name+' derivative');counts.slopes++;
  equal(world.baseline_lambda,neg(slope),name+' multiplier');counts.slopes++;
  let sec=keyed(world.secants,'step',STEPS,name+' steps');
  for(let h of STEPS){
   let left=div(sub(vals.get('0'),vals.get(fmt(neg(q(h))))),q(h));
   let right=div(sub(vals.get(h),vals.get('0')),q(h));
   equal(sec.get(h).left_secant,left,name+' left '+h);counts.secants++;
   equal(sec.get(h).right_secant,right,name+' right '+h);counts.secants++;
  }
  diagnostics.push({world:name,minimum:fmt(vals.get('0')),derivative:fmt(slope)});
 }
 need(seen.size===8,'missing world');
 return {status:'PASS',scope:'INTERNAL_NONBLIND_ARTIFICIAL_E1',
  counts,total_comparisons:Object.values(counts).reduce((a,b)=>a+b,0),diagnostics,
  historical_blind_order:'FAIL',full_scientific_acceptance:'PARTIAL',
  source_authentication:'NOT_RUN',external_team_replication:false};
}
function selftest(){
 let cases=[
  ['1','3/4','3/4','1/2','1/2','1/8'],
  ['3/4','3/5','1/5','23/40','7/40','1/800'],
  ['1','2','1/4','1','0','17/16'],
  ['1','-1/2','-1/2','0','0','1/2']
 ];
 for(let c of cases){let s=solve(q(c[0]),q(c[1]),q(c[2]));equal(c[3],s.x,'selftest x');equal(c[4],s.y,'selftest y');equal(c[5],s.v,'selftest value')}
 return {status:'PASS',closed_form_controls:12};
}
try{
 need(process.argv.length===3,'usage: node oracle.js RECEIPT.json | --selftest');
 let result=process.argv[2]==='--selftest'?selftest():audit(JSON.parse(fs.readFileSync(process.argv[2],'utf8')));
 console.log(JSON.stringify(result,null,2));
}catch(e){console.error('FAIL: '+e.message);process.exitCode=1}
