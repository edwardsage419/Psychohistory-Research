#!/usr/bin/env node
"use strict";
const fs=require("fs");
function auditCalc(src,receipt){
 const fail=(s)=>{throw Error("independent B audit "+s)};
 const gcd=(a,b)=>{if(a<0n)a=-a;if(b<0n)b=-b;while(b!==0n){let t=a%b;a=b;b=t;}return a};
 const parse=(s)=>{let [a,b="1"]=String(s).split("/");return [BigInt(a),BigInt(b)]};
 const norm=(a,b)=>{if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]};
 const plus=(x,y)=>norm(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const minus=(x,y)=>norm(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
 const repr=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
 const include=(k,n,p,znum,zden,kind)=>{
  const [a,b]=p,K=BigInt(k),N=BigInt(n),v=K*b-N*a;
  if(kind==="score")return v*v*zden*zden<=N*znum*znum*a*(b-a);
  return v*v*N*zden*zden<=znum*znum*K*(N-K)*b*b;
 };
 let tests=0,errors=0,negative=0,sourceWald=0;
 for(let i=0;i<src.source_worlds.length;i++){
  let r=src.source_worlds[i],t=receipt.worlds[i],p=parse(r.true_marginal_p),n=r.sample_size;
  let excludedScore=[0n,1n],excludedWald=[0n,1n];
  for(let k=0;k<=n;k++){
   const s=include(k,n,p,49n,25n,"score"),w=include(k,n,p,49n,25n,"wald");
   if(Number(s)!==t.wilson_includes[k]||Number(w)!==t.wald_includes[k])errors++;
   if(!s)excludedScore=plus(excludedScore,parse(r.full_training_count_pmf[k]));
   if(!w)excludedWald=plus(excludedWald,parse(r.full_training_count_pmf[k]));
   if(s!==include(k,n,p,1n,1n,"score"))negative++;
   tests++;
  }
  let coverageS=minus([1n,1n],excludedScore),coverageW=minus([1n,1n],excludedWald);
  if(repr(coverageS)!==t.wilson_exact||repr(coverageW)!==t.wald_exact)errors++;
  if(repr(coverageW)!==r.wald_nominal_95_actual_coverage)sourceWald++;
 }
 if(tests!==270||errors||sourceWald||negative===0)fail(JSON.stringify({tests,errors,sourceWald,negative}));
 return {research_id:"R178",date:"2026-10-26",method:"independent_integer_cross_multiplication_and_complement_mass",
  source_blob:receipt.source_blob,worlds:30,cell_membership_checks:540,world_exact_coverage_checks:60,
  mismatches:errors,original_wald_mismatches:sourceWald,negative_control_z1_membership_changes:negative,
  external_replication:false,evidence:"E1_INTERNAL_METHOD_INDEPENDENT"};
}
if(process.argv.length<4)throw Error("Usage: node r178_b_score_integer_20261026.js R178_EXACT_RESULTS.json R178_WILSON_RECEIPT.json [output.json]");
const output=auditCalc(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));
if(process.argv[4])fs.writeFileSync(process.argv[4],JSON.stringify(output,null,2)+"\n");
console.log(JSON.stringify(output,null,2));
