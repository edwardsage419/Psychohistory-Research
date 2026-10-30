'use strict';
// Artificial binary histories. This is not the Exist application's correlation implementation.
const assert = require('node:assert/strict');
let checks = 0;
function check(ok, message) { assert.ok(ok, message); checks++; }
function merge(a,b) {
  if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length || !a.length) throw Error('length');
  if ([...a,...b].some(v => v !== 0 && v !== 1)) throw Error('binary');
  return a.map((v,i)=>Number(Boolean(v || b[i])));
}
function phi(a,b) {
  if (a.length !== b.length || a.length < 2) throw Error('length');
  const n=a.length, sa=a.reduce((x,y)=>x+y,0), sb=b.reduce((x,y)=>x+y,0);
  const sab=a.reduce((x,y,i)=>x+y*b[i],0);
  const denominator=Math.sqrt(sa*(n-sa)*sb*(n-sb));
  return denominator===0 ? null : (n*sab-sa*sb)/denominator;
}
const A=[1,0,1,0,0,0,0,0];
const B=[0,1,1,0,1,0,0,0];
const mood=[1,0,1,0,0,1,0,0];
const merged=merge(A,B);
const altA=[...merged], altB=Array(8).fill(0);
check(JSON.stringify(merged)===JSON.stringify([1,1,1,0,1,0,0,0]),'union');
check(A.reduce((a,b)=>a+b,0)===2,'A count');
check(B.reduce((a,b)=>a+b,0)===3,'B count');
check(merged.reduce((a,b)=>a+b,0)===4,'union count');
check(A.reduce((a,b,i)=>a+b*B[i],0)===1,'overlap');
check(A.reduce((a,b)=>a+b,0)+B.reduce((a,b)=>a+b,0)-1===4,'inclusion exclusion');
check(Math.abs(phi(A,mood)-Math.sqrt(5)/3)<1e-12,'A phi');
check(Math.abs(phi(B,mood)+1/15)<1e-12,'B phi');
check(Math.abs(phi(merged,mood)-1/Math.sqrt(15))<1e-12,'merged phi');
check(JSON.stringify(merge(altA,altB))===JSON.stringify(merged),'same post merge');
check(JSON.stringify(A)!==JSON.stringify(altA),'different lineage');
check(phi(A,mood)!==phi(altA,mood),'pre merge association not identified');
check(phi(altB,mood)===null,'constant feature undefined');
check(merge(A,B).every((x,i)=>x>=A[i]&&x>=B[i]),'monotonic union');
check(merge(A,B).every(x=>x===0||x===1),'binary union');
check(merge(B,A).every((x,i)=>x===merged[i]),'commutative');
check(merge(merged,merged).every((x,i)=>x===merged[i]),'idempotent');
for(const bad of [()=>merge([1],[0,1]),()=>merge([1,2],[0,0]),()=>merge([],[])]) {
  let rejected=false;try{bad()}catch{rejected=true}check(rejected,'invalid input');
}
const result={scope:'ARTIFICIAL_E1_NONBLIND',checks,days:8,
 counts:{A:2,B:3,overlap:1,merged:4},
 phi:{A:phi(A,mood),B:phi(B,mood),merged:phi(merged,mood)},
 same_merged_different_premerge:true,platform_algorithm_tested:false};
console.log(JSON.stringify(result));
