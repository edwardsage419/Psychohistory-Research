"use strict";
/* R227 S23 exact source-first artificial E1 analysis. Node.js standard library only.
   Usage: node research/validation/r227_s23_cross_occasion_coupling_exact_20261028.js
   Prints machine JSON to stdout. Does not modify frozen R227 files. */
const EXPECTED_SHA256="e6e5d6784dbe1d56faacec02d6044609f6574af1b0d4a64294750263ea87b667";
const FREEZE="997a86829623affab68e8bdbf1d5e753c03cf376";
const RHO=[[0,1],[1,8],[1,4],[1,2],[1,1]];
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;};
const f=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};};
const add=(a,b)=>f(a.n*b.d+b.n*a.d,a.d*b.d);
const neg=a=>f(-a.n,a.d);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>f(a.n*b.n,a.d*b.d);
const div=(a,b)=>f(a.n*b.d,a.d*b.n);
const same=(a,b)=>a.n===b.n&&a.d===b.d;
const fmt=a=>a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);
const ZERO=f(0),ONE=f(1);
function compute(csv,original){
  const lines=csv.trim().split(/\r?\n/),headers=lines.shift().split(",");
  const required=["world","stable_trait_T","first_E1","first_E2","first_shared_M","second_E1","second_E2","second_shared_M","first_item_X","first_item_Y","first_sum_S","second_sum_S","source_probability"];
  for(const k of required)if(!headers.includes(k))throw Error("missing source column "+k);
  const rows=lines.map(line=>{const v=line.split(",");if(v.length!==headers.length)throw Error("malformed CSV");const o={};headers.forEach((h,i)=>o[h]=v[i]);if(o.source_probability!=="1/128")throw Error("changed original weight");for(const k of required.filter(x=>!["world","source_probability"].includes(x)))o[k]=Number(o[k]);return o;});
  if(rows.length!==1024)throw Error("expected 1024 original pair atoms");
  const by={};for(const r of rows)(by[r.world]??=[]).push(r);
  const worlds=Object.keys(by).sort();
  if(worlds.length!==8||worlds.some(w=>by[w].length!==128))throw Error("unexpected worlds or source counts");
  const results=[];
  for(const world of worlds){
    const rr=by[world],orig=original.world_results.find(x=>x.world===world);
    if(!orig)throw Error("original world absent "+world);
    const first=rr.filter(r=>r.second_E1===-1&&r.second_E2===-1&&r.second_shared_M===-1);
    if(first.length!==16)throw Error("original first source not 16");
    const mom=(xs,weights,D,cols)=>{
      const mean={};for(const k of cols)mean[k]=f(xs.reduce((a,r,i)=>a+BigInt(weights[i])*BigInt(r[k]),0n),D);
      const cov=(k,l)=>sub(f(xs.reduce((a,r,i)=>a+BigInt(weights[i])*BigInt(r[k])*BigInt(r[l]),0n),D),mul(mean[k],mean[l]));
      return {mean,cov};
    };
    const m=mom(first,first.map(()=>1),16,["first_item_X","first_item_Y","first_sum_S"]);
    const vx=m.cov("first_item_X","first_item_X"),vy=m.cov("first_item_Y","first_item_Y");
    const cxy=m.cov("first_item_X","first_item_Y"),vs=m.cov("first_sum_S","first_sum_S");
    const alpha=div(mul(f(4),cxy),vs);
    const cond={};
    for(const t of [-1,1]){const s=first.filter(r=>r.stable_trait_T===t);cond[t]=f(s.reduce((a,r)=>a+BigInt(r.first_sum_S),0n),s.length);}
    const trueVar=div(mul(sub(cond[1],cond[-1]),sub(cond[1],cond[-1])),f(4));
    const truth=div(trueVar,vs);
    for(const [key,val] of [["two_item_alpha",alpha],["true_reliability_conditional_stable_trait",truth],["variance_sum",vs],["true_score_variance",trueVar]]){
      if(fmt(val)!==orig[key])throw Error("original R227 regression "+world+" "+key);
    }
    for(const [p,q] of RHO){
      const weights=rr.map(r=>q-p+((r.first_E1===r.second_E1&&r.first_E2===r.second_E2&&r.first_shared_M===r.second_shared_M)?8*p:0));
      const D=128*q,total=weights.reduce((a,b)=>a+b,0);
      if(total!==D)throw Error("not normalized "+world+" "+p+"/"+q);
      const v=mom(rr,weights,D,["first_sum_S","second_sum_S"]);
      const cv=v.cov("first_sum_S","second_sum_S");
      const rel=div(cv,vs),bias=sub(rel,truth);
      const expected=add(trueVar,mul(f(p,q),sub(vs,trueVar)));
      if(!same(cv,expected))throw Error("analytic identity mismatch "+world+" "+p+"/"+q);
      const joint={};
      rr.forEach((r,i)=>{const k=r.first_sum_S+","+r.second_sum_S;joint[k]=(joint[k]||0)+weights[i];});
      const sorted={};for(const k of Object.keys(joint).sort((a,b)=>{const aa=a.split(",").map(Number),bb=b.split(",").map(Number);return aa[0]-bb[0]||aa[1]-bb[1];}))if(joint[k]>0)sorted[k]=fmt(f(joint[k],D));
      if(p===0){if(fmt(rel)!==orig.retest_reliability_from_independent_occasion_pairs)throw Error("baseline retest mismatch");if(JSON.stringify(sorted)!==JSON.stringify(orig.retest_sum_joint))throw Error("baseline retest joint mismatch "+world);}
      results.push({world,rho:fmt(f(p,q)),source_slots:128,positive_source_slots:weights.filter(x=>x>0).length,total_probability:"1",two_item_alpha:fmt(alpha),true_reliability:fmt(truth),cross_occasion_covariance:fmt(cv),retest_correlation:fmt(rel),retest_minus_true:fmt(bias),single_score_variance:fmt(vs),retest_joint:sorted});
    }
  }
  const get=(w,r)=>results.find(x=>x.world===w&&x.rho===r);
  if(JSON.stringify(get("PERFECT_TRAIT","1").retest_joint)!==JSON.stringify(get("PERFECT_METHOD","1").retest_joint))throw Error("two occasion alias missing");
  if(get("PERFECT_METHOD","1").true_reliability!=="0"||get("PERFECT_METHOD","1").retest_correlation!=="1")throw Error("method false stability");
  if(get("PERFECT_METHOD","1/2").retest_correlation!=="1/2")throw Error("method half coupling");
  if(results.length!==40)throw Error("expected 40 conditions");
  return {research_id:"R227",supplement:"S23",date:"2026-10-28",evidence:"E1_ARTIFICIAL_ONLY",freeze_commit:FREEZE,original_retest_csv_sha256:EXPECTED_SHA256,original_source_pairs:1024,worlds:8,coupling_levels:RHO.map(([p,q])=>fmt(f(p,q))),conditions:40,weighted_source_slots:5120,positive_source_slots:results.reduce((a,x)=>a+x.positive_source_slots,0),original_R227_unchanged:true,independent_R073_scoring_unchanged:true,PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0,results};
}
if(typeof module!=="undefined"){module.exports={compute};if(require.main===module){
  const fs=require("fs"),path=require("path"),crypto=require("crypto");
  const csvPath=path.join(__dirname,"../R227/R227_ALL_1024_ORIGINAL_RETEST_SOURCE_PAIRS.csv");
  const origPath=path.join(__dirname,"../R227/R227_EXACT_RESULTS.json");
  const csv=fs.readFileSync(csvPath,"utf8");
  const digest=crypto.createHash("sha256").update(csv).digest("hex");
  if(digest!==EXPECTED_SHA256)throw Error("original CSV SHA256 mismatch: "+digest);
  process.stdout.write(JSON.stringify(compute(csv,JSON.parse(fs.readFileSync(origPath,"utf8"))),null,2)+"\n");
}}
