#!/usr/bin/env node
"use strict";
/*
 * R183 exploratory secondary analysis, version 1 (2026-11-17).
 * Input is the immutable 45-world artificial E1 archive; no re-fitting.
 * Standard Node.js only. No human data, APIs, or changed frozen artifacts.
 *
 * Usage: node independent_brier.js [path/to/R183_EXACT_RESULTS.json]
 */
const fs=require("node:fs");
const path=require("node:path");
const crypto=require("node:crypto");
const INPUT=process.argv[2]||path.resolve(__dirname,"../R183_EXACT_RESULTS.json");
const EXPECTED_SHA256="40927bae4616a9d9fc91ed964257a9d436372d9196abd8fabceb40740189a000";

function audit(data) {
  const gcd=(a,b)=>{
    a=a<0n?-a:a;b=b<0n?-b:b;
    while(b!==0n){const t=a%b;a=b;b=t;}
    return a;
  };
  const Q=(x,y=1n)=>{
    let n=BigInt(x),d=BigInt(y);
    if(d===0n)throw Error("ZERO_DENOMINATOR");
    if(d<0n){n=-n;d=-d;}
    const g=gcd(n,d);return {n:n/g,d:d/g};
  };
  const parse=(s)=>{
    const fields=String(s).split("/");
    return Q(fields[0],fields.length===2?fields[1]:1n);
  };
  const add=(a,b)=>Q(a.n*b.d+b.n*a.d,a.d*b.d);
  const sub=(a,b)=>Q(a.n*b.d-b.n*a.d,a.d*b.d);
  const mul=(a,b)=>Q(a.n*b.n,a.d*b.d);
  const div=(a,b)=>Q(a.n*b.d,a.d*b.n);
  const square=a=>mul(a,a);
  const eq=(a,b)=>a.n===b.n&&a.d===b.d;
  const fmt=a=>a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);
  const fnum=a=>Number(a.n)/Number(a.d);
  const sum=arr=>arr.reduce(add,Q(0));
  const brier=(p,q)=>add(mul(p,square(sub(Q(1),q))),mul(sub(Q(1),p),square(q)));
  function group(p,n,strings) {
    const pmf=strings.map(parse);
    if(pmf.length!==n+1||pmf.some(x=>x.n<0n)||!eq(sum(pmf),Q(1)))throw Error("PMF_INVALID");
    const ek=sum(pmf.map((mass,k)=>mul(mass,Q(k))));
    if(!eq(ek,mul(Q(n),p)))throw Error("MARGINAL_MEAN_MISMATCH");
    const ek2=sum(pmf.map((mass,k)=>mul(mass,Q(k*k))));
    const vq=div(sub(ek2,square(ek)),Q(n*n));
    const mle=sum(pmf.map((mass,k)=>mul(mass,brier(p,Q(k,n)))));
    const half=sum(pmf.map((mass,k)=>mul(mass,brier(p,Q(2*k+1,2*n+2)))));
    const shrinkGain=div(sub(mul(Q(2*n+1),vq),square(sub(Q(1,2),p))),Q((n+1)**2));
    if(!eq(sub(mle,half),shrinkGain))throw Error("MOMENT_AND_ENUMERATION_DISAGREE");
    return {mle,half,shrinkGain};
  }
  if(data.world_count!==45||data.worlds.length!==45||
     data.complete_training_count_pairs!==4125)throw Error("FROZEN_UNIVERSE_MISMATCH");
  const rows=[],seen=new Set();
  let pairs=0;
  for(const w of data.worlds){
    const n=w.n_per_group;
    if(![4,8,12].includes(n))throw Error("N_OUT_OF_SCOPE");
    const key=[n,w.true_p0,w.true_p1,w.mechanism].join("|");
    if(seen.has(key))throw Error("DUPLICATE_WORLD");
    seen.add(key);
    const a=group(parse(w.true_p0),n,w.source_group0_full_count_PMF);
    const b=group(parse(w.true_p1),n,w.source_group1_full_count_PMF);
    const mle=div(add(a.mle,b.mle),Q(2));
    const half=div(add(a.half,b.half),Q(2));
    const delta=div(add(a.shrinkGain,b.shrinkGain),Q(2));
    if(!eq(mle,parse(w.expected_MLE_out_of_sample_Brier_exact)))throw Error("ARCHIVED_MLE_RISK_MISMATCH");
    if(!eq(half,parse(w.expected_halfcount_out_of_sample_Brier_exact)))throw Error("ARCHIVED_HALF_RISK_MISMATCH");
    if(!eq(sub(mle,half),delta))throw Error("EXPECTED_RISK_DIFFERENCE_MISMATCH");
    pairs+=(n+1)*(n+1);
    rows.push({n,p0:w.true_p0,p1:w.true_p1,mechanism:w.mechanism,
               delta:fmt(delta),approx:fnum(delta),positive:delta.n>0n});
  }
  if(pairs!==4125||seen.size!==45)throw Error("COUNT_PAIRS_DRIFT");
  rows.sort((a,b)=>a.approx-b.approx);
  // Counterexample outside the 45-world frozen design: IID Bin(4, 1/100).
  // The frozen study used true rates 1/8, 1/4 and 1/2, not 1/100.
  const n=4,p=Q(1,100);
  const choose=(n,k)=>{let x=1;for(let i=1;i<=k;i++)x=x*(n-i+1)/i;return x;};
  const pmf=Array.from({length:n+1},(_,k)=>fmt(mul(
    Q(choose(n,k)),mul(Q(1n,100n**BigInt(k)),Q(99n**BigInt(n-k),100n**BigInt(n-k)))
  )));
  const counter=group(p,n,pmf);
  if(fmt(counter.shrinkGain)!=="-8713/1000000")throw Error("OFF_GRID_COUNTEREXAMPLE_DRIFT");
  const positives=rows.filter(x=>x.positive).length;
  if(positives!==45)throw Error("EXPECTED_45_POSITIVE_DIRECTIONS");
  return {
    status:"PASS_INDEPENDENT_FRACTION_RECOMPUTATION",
    result_scope:"SECONDARY_EXPLORATORY_ARTIFICIAL_E1_ONLY",
    archived_worlds:45,archived_training_pairs:4125,positive_count:positives,
    formula:"(2n+1)*Var(K/n)/(n+1)^2 - (1/2-p)^2/(n+1)^2, if E[K]=np",
    minimum:rows[0],maximum:rows[rows.length-1],
    grouped:[4,8,12].map(n=>({
      n,positive:rows.filter(x=>x.n===n&&x.positive).length,
      smallest:rows.find(x=>x.n===n),
      largest:rows.slice().reverse().find(x=>x.n===n)
    })),
    off_grid_counterexample:{
      n:4,true_p:"1/100",family:"IID_BIN",
      expected_MLE_Brier:fmt(counter.mle),
      expected_halfcount_Brier:fmt(counter.half),
      MLE_minus_halfcount:fmt(counter.shrinkGain)
    },
    empirical_E2:0,historical_E3:0,source_protocol_unchanged:true
  };
}

function main(){
  const raw=fs.readFileSync(INPUT),sha=crypto.createHash("sha256").update(raw).digest("hex");
  if(sha!==EXPECTED_SHA256)throw Error("SOURCE_SHA256_MISMATCH:"+sha);
  const data=JSON.parse(raw.toString("utf8"));
  const receipt=audit(data);
  // Negative controls exercise the independent runtime gate rather than the old author implementation.
  const a=JSON.parse(JSON.stringify(data));a.worlds[0].source_group0_full_count_PMF[0]="0";
  const b=JSON.parse(JSON.stringify(data));b.worlds[1].expected_halfcount_out_of_sample_Brier_exact="1/2";
  for(const [label,mutant] of [["pmf_mutation",a],["score_mutation",b]]){
    let rejected=false;
    try{audit(mutant);}catch(error){rejected=true;}
    if(!rejected)throw Error("MUTATION_WAS_ACCEPTED:"+label);
  }
  receipt.input_sha256=sha;
  receipt.negative_controls=["pmf_mutation_REJECTED","score_mutation_REJECTED"];
  process.stdout.write(JSON.stringify(receipt,null,2)+"\n");
}
if(require.main===module){main();}
module.exports={audit};
