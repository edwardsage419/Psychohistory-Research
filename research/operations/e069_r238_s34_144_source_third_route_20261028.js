'use strict';
// E069 independent source-first exact replay. Node.js, repository root, no external packages.
const fs=require('fs');
const csv=fs.readFileSync('research/R238/R238_ALL_144_ORIGINAL_HIDDEN_SENSE_AND_OBSERVED_EMBEDDING_SOURCES.csv','utf8');
const obs=JSON.parse(fs.readFileSync('research/R238/R238_EXACT_RESULTS.json','utf8'));
const receipt=JSON.parse(fs.readFileSync('research/validation/R238_S34_THREE_ANCHOR_EXACT_RECEIPT_2026-10-28.json','utf8'));
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a||1n;}
function N(n,d){if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};}
function F(x){const p=String(x).split('/');return N(BigInt(p[0]),p[1]?BigInt(p[1]):1n);}
function A(a,b){return N(a.n*b.d+b.n*a.d,a.d*b.d);}
function S(a,b){return N(a.n*b.d-b.n*a.d,a.d*b.d);}
function M(a,b){return N(a.n*b.n,a.d*b.d);}
function D(a,b){if(b.n===0n)throw Error('singular anchor');return N(a.n*b.d,a.d*b.n);}
function T(a){return a.d===1n?String(a.n):String(a.n)+'/'+String(a.d);}
function det(a,b){return S(M(a[0],b[1]),M(a[1],b[0]));}
function fit(u,v,u0,v0,z){const den=det(u,v),x=D(det(z,v),den),y=D(det(u,z),den);return [A(M(x,u0[0]),M(y,v0[0])),A(M(x,u0[1]),M(y,v0[1]))];}
function sq(a,b){const x=S(a[0],b[0]),y=S(a[1],b[1]);return A(M(x,x),M(y,y));}
let checks=0;function ck(x,why){checks++;if(!x)throw Error('E069 FAIL '+why);}
const lines=csv.trim().split(/\r?\n/),h=lines.shift().split(','),data={};
for(const [i,line] of lines.entries()){
 const cells=line.split(',');ck(cells.length===h.length,'width '+i);
 const r=Object.fromEntries(h.map((k,n)=>[k,cells[n]]));
 ck(['0','1'].includes(r.time)&&['A','B','C','D'].includes(r.word)&&['0','1'].includes(r.oracle_sense),'key '+i);
 data[r.world]??={};const key=r.time+'|'+r.word;data[r.world][key]??=[];data[r.world][key].push(r);
 ck(T(M(F(r.observed_word_frequency),F('1/4')))===T(F(r.original_structural_source_probability)),'mass '+i);
}
ck(lines.length===144,'rows');ck(Object.keys(data).length===9,'worlds');
const out=[];
for(const w of Object.keys(data).sort()){
 const d=data[w];ck(Object.keys(d).length===8,'groups '+w);const t={0:{},1:{}};
 for(const [key,rows] of Object.entries(d)){
  ck(rows.length===2,'sense count');ck(rows.map(x=>x.oracle_sense).sort().join(',')==='0,1','sense unique');
  const [time,word]=key.split('|'),a=rows[0],b=rows[1];
  ck(a.observed_embedding_x===b.observed_embedding_x&&a.observed_embedding_y===b.observed_embedding_y&&a.observed_word_frequency===b.observed_word_frequency,'alias');
  t[time][word]=[F(a.observed_embedding_x),F(a.observed_embedding_y)];
  const v=obs.world_results.find(x=>x.world===w).observed_embeddings_by_time[time][word];
  ck(T(t[time][word][0])===T(F(v[0]))&&T(t[time][word][1])===T(F(v[1])),'frozen coord');
 }
 const rc=receipt.worlds.find(x=>x.world===w);ck(!!rc,'receipt world');
 const hs=[],ds=[];
 for(const p of rc.pairs){
  const [a,b]=p.pair.split(''),z=p.heldout;
  const x=fit(t[1][a],t[1][b],t[0][a],t[0][b],t[1][z]);
  const y=fit(t[1][a],t[1][b],t[0][a],t[0][b],t[1].D);
  const h=T(sq(x,t[0][z])),v=T(sq(y,t[0].D));
  ck(h===p.heldout_residual_sq,'heldout '+w+p.pair);ck(v===p.target_D_aligned_displacement_sq,'D '+w+p.pair);hs.push(h);ds.push(v);
 }
 ck((hs.every(x=>x==='0')?'ANCHOR_CONSISTENT':'ANCHOR_INCONSISTENT')===rc.anchor_consistency,'class');
 const o=[];for(const time of ['0','1']){
  const r=d[time+'|D'];
  o.push([D(A(F(r[0].oracle_true_semantic_sense_x),F(r[1].oracle_true_semantic_sense_x)),F('2')),
          D(A(F(r[0].oracle_true_semantic_sense_y),F(r[1].oracle_true_semantic_sense_y)),F('2'))]);
 }
 const truth=T(sq(o[1],o[0]));ck(truth===rc.oracle_target_D_semantic_change_sq,'oracle D');
 out.push({world:w,h:hs,d:ds,oracle:truth});
}
for(const key of Object.keys(data.STABLE_BASE)){
 const a=data.STABLE_BASE[key][0],b=data.SENSE_RECONFIGURATION_ALIAS[key][0];
 for(const f of ['observed_embedding_x','observed_embedding_y','observed_word_frequency','original_structural_source_probability'])
  ck(a[f]===b[f],'observed alias');
}
if(checks!==844)throw Error('expected 844 checks, got '+checks);
console.log(JSON.stringify({status:'PASS',checks,source_rows:lines.length,worlds:out.length,pairs:27,results:out}));
