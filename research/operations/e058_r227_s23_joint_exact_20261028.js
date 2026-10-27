#!/usr/bin/env node
"use strict";
// Run from the Psychohistory-Research repository root:
// node research/operations/e058_r227_s23_joint_exact_20261028.js
// This is an internal independent implementation of the mixture identity.
// It is not an independent human replication or a separate mathematical proof.
const fs=require("node:fs");
const receipt=JSON.parse(fs.readFileSync(process.argv[2]||"research/validation/R227_S23_40_CONDITION_EXACT_RECEIPT_2026-10-28.json","utf8"));
const base=JSON.parse(fs.readFileSync(process.argv[3]||"research/R227/R227_EXACT_RESULTS.json","utf8"));
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a};
const f=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]};
const P=s=>{let z=String(s).split("/");return f(BigInt(z[0]),BigInt(z[1]||"1"))};
const plus=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
const minus=(a,b)=>plus(a,[-b[0],b[1]]);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const one=P("1"),zero=P("0");
let checks=0,cells=0;const failed=[];
const ck=(ok,label)=>{checks++;if(!ok)failed.push(label)};
ck(receipt.results.length===40,"result count");
ck(receipt.conditions===40,"metadata conditions");
const worlds=new Map(base.world_results.map(w=>[w.world,w]));
for(const r of receipt.results){
 const b=worlds.get(r.world);ck(!!b,"world "+r.world);if(!b)continue;
 const rho=P(r.rho),scoreMass=new Map();
 for(const [key,val] of Object.entries(b.single_observation_joint)){
   const [x,y]=key.split(",").map(Number),score=String(x+y);
   scoreMass.set(score,plus(scoreMass.get(score)||zero,P(val)));
 }
 const p0=b.retest_sum_joint,p1={};
 for(const [score,mass] of scoreMass)p1[score+","+score]=mass;
 const keys=new Set([...Object.keys(p0),...Object.keys(p1),...Object.keys(r.retest_joint)]);
 let total=zero;
 for(const key of keys){
   const expected=plus(mul(minus(one,rho),P(p0[key]||"0")),mul(rho,p1[key]||zero));
   const observed=P(r.retest_joint[key]||"0");
   ck(eq(observed,expected),r.world+"/"+r.rho+"/"+key);
   cells++;total=plus(total,observed);
 }
 ck(eq(total,one),r.world+"/"+r.rho+" total");
 ck(eq(P(r.two_item_alpha),P(b.two_item_alpha)),r.world+"/"+r.rho+" alpha");
 ck(eq(P(r.true_reliability),P(b.true_reliability_conditional_stable_trait)),r.world+"/"+r.rho+" true");
 const expected=plus(P(b.true_reliability_conditional_stable_trait),mul(rho,minus(one,P(b.true_reliability_conditional_stable_trait))));
 ck(eq(P(r.retest_correlation),expected),r.world+"/"+r.rho+" corr");
 ck(eq(P(r.retest_minus_true),minus(expected,P(r.true_reliability))),r.world+"/"+r.rho+" delta");
 ck(eq(P(r.cross_occasion_covariance),mul(expected,P(b.variance_sum))),r.world+"/"+r.rho+" covariance");
 ck(eq(P(r.single_score_variance),P(b.variance_sum)),r.world+"/"+r.rho+" variance");
 ck(r.source_slots===128,r.world+"/"+r.rho+" slots");
 ck(r.positive_source_slots===(r.rho==="1"?16:128),r.world+"/"+r.rho+" positive");
}
const endpoint=receipt.results.filter(x=>x.rho==="1");
const trait=endpoint.find(x=>x.world==="PERFECT_TRAIT");
const method=endpoint.find(x=>x.world==="PERFECT_METHOD");
ck(JSON.stringify(trait.retest_joint)===JSON.stringify(method.retest_joint),"endpoint alias");
ck(trait.true_reliability==="1"&&method.true_reliability==="0","endpoint true");
console.log(JSON.stringify({checks,passed:checks-failed.length,failed,joint_cells_checked:cells,worlds:worlds.size,conditions:receipt.results.length},null,2));
if(failed.length)process.exitCode=1;
