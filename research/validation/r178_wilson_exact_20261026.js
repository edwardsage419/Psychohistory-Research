#!/usr/bin/env node
"use strict";
const fs=require("fs");
function mainCalc(src){
 const assert=(b,s)=>{if(!b)throw Error(s)};
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a};
 const F=(a,b=1n)=>{if(Array.isArray(a))return a;if(typeof a==="string"){let z=a.split("/");return F(BigInt(z[0]),BigInt(z[1]||"1"))}a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]};
 const add=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const neg=x=>[-x[0],x[1]];
 const sub=(x,y)=>add(x,neg(y));
 const mul=(x,y)=>F(x[0]*y[0],x[1]*y[1]);
 const div=(x,y)=>F(x[0]*y[1],x[1]*y[0]);
 const le=(x,y)=>x[0]*y[1]<=y[0]*x[1];
 const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
 const str=x=>x[1]===1n?x[0].toString():x[0]+"/"+x[1];
 const num=x=>Number(x[0])/Number(x[1]);
 const ONE=F(1),ZERO=F(0),z=F("49/25"),z2=mul(z,z);
 assert(src.source_worlds.length===30,"wrong source world count");
 let rows=[],checks=0;
 for(const r of src.source_worlds){
  let n=r.sample_size,p=F(r.true_marginal_p),N=F(n),pmf=r.full_training_count_pmf.map(F),total=ZERO,mean=ZERO,wald=ZERO,wilson=ZERO,wi=[],wa=[];
  assert(pmf.length===n+1,"support mismatch");
  for(let k=0;k<=n;k++){
   let w=pmf[k],ph=F(k,n),d=sub(ph,p),d2=mul(d,d);
   total=add(total,w);mean=add(mean,mul(F(k),w));
   let passWald=le(d2,div(mul(z2,mul(ph,sub(ONE,ph))),N));
   let passWilson=le(mul(N,d2),mul(z2,mul(p,sub(ONE,p))));
   if(passWald)wald=add(wald,w);
   if(passWilson)wilson=add(wilson,w);
   wa.push(passWald?1:0);wi.push(passWilson?1:0);checks++;
  }
  assert(eq(total,ONE),"PMF sum mismatch "+r.training_mechanism);
  assert(eq(mean,mul(N,p)),"marginal mean mismatch "+r.training_mechanism);
  assert(eq(wald,F(r.wald_nominal_95_actual_coverage)),"original Wald mismatch "+r.training_mechanism);
  rows.push({sample_size:n,true_marginal_p:str(p),training_mechanism:r.training_mechanism,
   wald_exact:str(wald),wilson_exact:str(wilson),wilson_minus_wald_exact:str(sub(wilson,wald)),
   wald_coverage:num(wald),wilson_coverage:num(wilson),wilson_includes:wi,wald_includes:wa,
   wilson_under_nominal:!le(F("19/20"),wilson),wald_under_nominal:!le(F("19/20"),wald)});
 }
 assert(checks===270,"cell count mismatch");
 const summary={worlds:rows.length,probability_cells:checks,
  improved:rows.filter(r=>r.wilson_coverage>r.wald_coverage+1e-15).length,
  tied:rows.filter(r=>Math.abs(r.wilson_coverage-r.wald_coverage)<=1e-15).length,
  worsened:rows.filter(r=>r.wilson_coverage<r.wald_coverage-1e-15).length,
  wilson_under_nominal:rows.filter(r=>r.wilson_under_nominal).length,
  wald_under_nominal:rows.filter(r=>r.wald_under_nominal).length,
  fixed_n8_p_quarter:rows.filter(r=>r.sample_size===8&&r.true_marginal_p==="1/4").map(r=>({mechanism:r.training_mechanism,wald:r.wald_exact,wilson:r.wilson_exact,delta:r.wilson_minus_wald_exact,wald_decimal:r.wald_coverage,wilson_decimal:r.wilson_coverage}))};
 assert(summary.improved+summary.tied+summary.worsened===30,"coverage counts mismatch");
 return {research_id:"R178",date:"2026-10-26",source_blob:"3b4a5abeaa14b5be32fb258a15aa6bf502b2756c",protocol:"protocols/R178_WILSON_SCORE_COVERAGE_THIRD_METHOD_FREEZE_2026-10-26.md",evidence:"E1_ARTIFICIAL",z:"49/25",summary,worlds:rows};
}
if(process.argv.length<3)throw Error("Usage: node r178_wilson_exact_20261026.js research/R178/R178_EXACT_RESULTS.json [output.json]");
const output=mainCalc(JSON.parse(fs.readFileSync(process.argv[2],"utf8")));
if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(output,null,2)+"\n");
console.log(JSON.stringify(output.summary,null,2));
