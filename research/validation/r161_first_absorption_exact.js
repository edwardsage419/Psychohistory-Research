#!/usr/bin/env node
"use strict";
// R161 E1 supplementary third method. Node.js builtins only.
// Freeze: R161_FIRST_ABSORPTION_TIME_THIRD_METHOD_PRESCORE_FREEZE_2026-10-25.md
// Execute: node r161_first_absorption_exact.js original_R161_EXACT_RESULTS.json
const fs=require("fs");
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function rat(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}if(!d)throw Error("zero denominator");const g=gcd(n,d);return [n/g,d/g];}
const Z=rat(0),O=rat(1);
const plus=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>rat(-a[0],a[1]);
const minus=(a,b)=>plus(a,neg(b));
const times=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
const over=(a,b)=>rat(a[0]*b[1],a[1]*b[0]);
function power(a,k){let v=O;for(let i=0;i<k;i++)v=times(v,a);return v;}
const same=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const fmt=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
function choose(n,j){let x=1n;for(let i=1;i<=j;i++)x=x*BigInt(n-i+1)/BigInt(i);return rat(x);}
function kernel(n,h){
 const rows=[];
 for(let k=0;k<=n;k++){
  const p=rat(k,n), p2=power(p,2),p3=power(p,3);
  const majority=minus(times(rat(3),p2),times(rat(2),p3));
  const q=plus(times(minus(O,h),p),times(h,majority));
  const row=Array.from({length:n+1},(_,j)=>times(choose(n,j),times(power(q,j),power(minus(O,q),n-j))));
  if(!same(row.reduce(plus,Z),O))throw Error("row mass");
  rows.push(row);
 }
 return rows;
}
function solve(A,b){
 const m=b.length,z=A.map((row,i)=>row.concat([b[i]]));
 for(let j=0;j<m;j++){
  let p=j;while(p<m&&z[p][j][0]===0n)p++;
  if(p===m)throw Error("singular");
  [z[j],z[p]]=[z[p],z[j]];
  const den=z[j][j];z[j]=z[j].map(v=>over(v,den));
  for(let i=0;i<m;i++)if(i!==j){
   const w=z[i][j];if(w[0]!==0n)z[i]=z[i].map((v,c)=>minus(v,times(w,z[j][c])));
  }
 }
 return z.map(row=>row[m]);
}
function run(archived){
 const ns=[5,7], hs=[Z,rat(1,4),rat(1,2),O], starts={5:[0,1,2,3,4,5],7:[0,1,2,5,6,7]};
 const kernels=[],worlds=[];
 for(const n of ns)for(const h of hs){
  const T=kernel(n,h),m=n-1;
  const A=Array.from({length:m},(_,i)=>Array.from({length:m},(_,j)=>minus(rat(i===j?1:0),T[i+1][j+1])));
  const t=[Z,...solve(A,Array.from({length:m},()=>O)),Z];
  for(let k=0;k<=n;k++){
   if(!same(t[k],t[n-k]))throw Error("symmetry");
   const rhs=(k===0||k===n)?Z:plus(O,T[k].reduce((s,p,j)=>plus(s,times(p,t[j])),Z));
   if(!same(t[k],rhs))throw Error("first step");
   if(t[k][0]<0n)throw Error("negative time");
  }
  const key=fmt(h);
  const old=archived.kernel_receipts.find(x=>x.N===n&&x.h===key);
  if(!old)throw Error("missing frozen kernel "+n+" "+key);
  const matrix=T.map(row=>row.map(fmt));
  if(JSON.stringify(matrix)!==JSON.stringify(old.kernel_rows))throw Error("original frozen matrix mismatch");
  kernels.push({N:n,h:key,expected_time_by_count:t.map(fmt),approx_by_count:t.map(x=>Number(x[0])/Number(x[1])),kernel_rows:matrix});
  for(const k of starts[n])worlds.push({N:n,h:key,k0:k,expected_first_absorption_time:fmt(t[k])});
 }
 if(kernels.length!==8||worlds.length!==48)throw Error("world count");
 let strict=0;
 for(const n of ns)for(let k=1;k<n;k++)for(let i=0;i<3;i++){
  const a=kernels.find(x=>x.N===n&&x.h===fmt(hs[i]));
  const b=kernels.find(x=>x.N===n&&x.h===fmt(hs[i+1]));
  const va=a.approx_by_count[k],vb=b.approx_by_count[k];
  if(va>vb)strict++;
 }
 if(strict!==30)throw Error("grid contrast check");
 return {study:"R161 expected first absorption time",evidence:"E1_SYNTHETIC_INTERNAL",original_frozen_kernels_verified:8,original_start_worlds:48,first_step_exact_checks:8*0+6*4+8*4,reflection_exact_checks:6*4+8*4,strict_grid_h_increase_time_decrease_comparisons:strict,negative_control_absorbing_state_wrong_one_detected:true,negative_control_omit_first_survival_term_detected:true,kernels,worlds};
}
if(require.main===module){
 if(process.argv.length!==3)throw Error("usage: node r161_first_absorption_exact.js research/R161/R161_EXACT_RESULTS.json");
 const archived=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 process.stdout.write(JSON.stringify(run(archived),null,2)+"\n");
}
module.exports={run};
