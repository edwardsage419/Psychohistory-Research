#!/usr/bin/env node
'use strict';
// R245 S41 source-row Brier oracle. Run from a checkout with the original R245 CSV.
const fs=require('node:fs'),path=require('node:path');
const file=path.resolve(__dirname,'../R245/R245_ALL_4608_ORIGINAL_RENEWAL_GAP_SOURCES.csv');
const lines=fs.readFileSync(file,'utf8').trim().split(/\r?\n/);
const cols=lines.shift().split(',');
const rows=lines.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[cols[i],v])));
const byWorld=new Map();
for(const row of rows){if(!byWorld.has(row.world))byWorld.set(row.world,[]);byWorld.get(row.world).push(row)}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a}
function rat(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error('zero denominator');let g=gcd(a,b);return [a/g,b/g]}
function add(x,y){return rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
function fmt(x){return x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1])}
const F=['F0','F3','F23','F123'];
function key(r,f){if(f==='F0')return 'all';if(f==='F3')return r.observed_reported_count_Y3;if(f==='F23')return r.observed_reported_count_Y2+','+r.observed_reported_count_Y3;return r.observed_reported_count_Y1+','+r.observed_reported_count_Y2+','+r.observed_reported_count_Y3}
let checks=0,results=[];
for(const [world,rs] of byWorld){
 if(rs.length!==512)throw Error('world row count');
 const seen=new Set();
 for(const r of rs){
  const bits=[r.oracle_exogenous_U].concat([1,2,3,4].flatMap(i=>[r['oracle_original_R'+i+'1'],r['oracle_original_R'+i+'2']])).join('');
  if(!/^[01]{9}$/.test(bits)||seen.has(bits))throw Error('source identity');seen.add(bits);checks++;
  if(r.original_source_probability!=='1/512')throw Error('mass');checks++;
  const y=[0,1,2,3,4].map(t=>Number(r['observed_reported_count_Y'+t]));
  if(y[0]!==0||y.some((v,i)=>!Number.isInteger(v)||(i>0&&![0,1].includes(v-y[i-1]))))throw Error('count path');
  checks++;
 }
 const risk={};
 for(const f of F){
  const groups=new Map();
  for(const r of rs){const k=key(r,f),g=groups.get(k)||{n:0,a:0};g.n++;g.a+=Number(r.observed_reported_count_Y4)-Number(r.observed_reported_count_Y3);groups.set(k,g)}
  let v=rat(0);
  for(const g of groups.values()){v=add(v,rat(BigInt(g.a*(g.n-g.a)),BigInt(512*g.n)));checks++}
  risk[f]=v;
 }
 for(let i=1;i<F.length;i++){let a=risk[F[i-1]],b=risk[F[i]];if(a[0]*b[1]<b[0]*a[1])throw Error('monotonicity');checks++}
 const minus=(a,b)=>add(a,[-b[0],b[1]]);
 results.push({world,risks:Object.fromEntries(F.map(f=>[f,fmt(risk[f])])),gain_F0_F123:fmt(minus(risk.F0,risk.F123)),gain_F3_F123:fmt(minus(risk.F3,risk.F123))});
}
if(byWorld.size!==9||rows.length!==4608)throw Error('universe incomplete');
if(JSON.stringify(results[0].risks)!==JSON.stringify(results[8].risks))throw Error('observed alias');
console.log(JSON.stringify({study:'R245_S41',evidence:'E1_SYNTHETIC_ORACLE',source_rows:rows.length,worlds:byWorld.size,checks,failed:0,results,new_E2:0,new_E3:0},null,2));
