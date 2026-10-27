#!/usr/bin/env node
// MKT080 pinned-source contract: Node.js only, offline, no personal data.
// pymoo main 23110c155aa8f31b5f1b86928227fb3931ba7f00
// pinsga2.py blob 207726ffba920eca75f739b2d0cccaf0c23d92b8
const assert=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto');
let checks=0;function ok(b,s){checks++;assert.ok(b,s);}
function perms(a){if(a.length<2)return[a];return a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(y=>[x,...y]));}
function sourceV2(r){return r[1]-1;}
function rank2(r){return r.indexOf(2);}
function sourceValid(r,n){return r.length>0&&Math.max(...r)<=n&&Math.min(...r)>=1;}
function strict(r,n){return r.length===n&&new Set(r).size===n&&r.every(x=>Number.isInteger(x)&&x>=1&&x<=n);}
if(process.argv[2]){
 const b=fs.readFileSync(process.argv[2]);
 const hash=crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
 ok(hash==='207726ffba920eca75f739b2d0cccaf0c23d92b8','pinned blob');
 const s=b.toString('utf8');
 ok(s.includes('eta_F[dm_ranks[1] - 1]'),'v2 expression');
 ok(s.includes('if len(ranks) > 0 and max(ranks) <= fc and min(ranks) >= 1:'),'absolute rank guard');
 ok(s.includes('if len(set(rank)) == 0:'),'population-rank tie guard');
}
const mismatch={};
for(const n of [3,4,5]){
 let count=0;
 for(const r of perms(Array.from({length:n},(_,i)=>i+1))){
   ok(sourceV2(r)>=0&&sourceV2(r)<n,'source index bounded');
   ok(r[rank2(r)]===2,'rank2 index');
   if(sourceV2(r)!==rank2(r))count++;
 }
 mismatch[n]=count;
}
ok(mismatch[3]===2,'3-point count');ok(mismatch[4]===12,'4-point count');ok(mismatch[5]===72,'5-point count');
const invalid=[[1],[1,1,1,1],[1,2,3,4,4],[1,2],[1,1,2,3]];
for(const r of invalid){ok(sourceValid(r,4),'source accepts malformed ranks');ok(!strict(r,4),'strict rejects');}
ok(!sourceValid([0,1,2,3],4),'zero rejected');ok(!sourceValid([1,2,3,5],4),'out of range rejected');
const example=[3,1,2,4];ok(sourceV2(example)===0,'source selects rank3');ok(rank2(example)===2,'rank2 at index2');
console.log(JSON.stringify({status:'PASS',checks,mismatch,invalidAccepted:invalid.length,example,sourceIndex:sourceV2(example),intendedIndex:rank2(example),scope:'pinned source expression plus synthetic permutations; no full pymoo execution'}));
