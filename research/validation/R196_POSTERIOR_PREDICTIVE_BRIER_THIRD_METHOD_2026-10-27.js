#!/usr/bin/env node
"use strict";
const fs=require("fs"),path=require("path");
const root=path.resolve(__dirname,"../..");
const src=JSON.parse(fs.readFileSync(path.join(root,"research/R196/R196_ALL_12_EXACT_POSTERIOR_SOURCES.json"),"utf8"));
const worlds=JSON.parse(fs.readFileSync(path.join(root,"research/R196/R196_EXACT_RESULTS.json"),"utf8"));
const compute=function calculate(source,worlds){
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
 function F(x){if(typeof x==="object"&&x.n!==undefined)return x;let s=String(x).split("/");let n=BigInt(s[0]),d=BigInt(s[1]||"1");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return {n:n/g,d:d/g};}
 const add=(a,b)=>F((a.n*b.d+b.n*a.d)+"/"+(a.d*b.d)),sub=(a,b)=>F((a.n*b.d-b.n*a.d)+"/"+(a.d*b.d)),mul=(a,b)=>F((a.n*b.n)+"/"+(a.d*b.d));
 const S=x=>x.d===1n?String(x.n):String(x.n)+"/"+String(x.d);
 const eq=(a,b)=>a.n*b.d===b.n*a.d,zero=F(0),one=F(1),quarter=F("1/4");
 const byKey=new Map(worlds.all_worlds.map(w=>[w.source+"|"+w.m_positive_likelihood_observations+"|"+w.grid,w]));
 const rows=[], comparisons=[];
 for(const s of source.exact_source_truths){
  const key=s.source+"|"+s.positive_observations_m;
  const rate=s.weights.map(w=>F(w+"/"+Math.max(...s.weights)));
  const p=s.exact_posterior_00_01_10_11.map(F);
  const mean=q=>q.reduce((acc,x,i)=>add(acc,mul(x,rate[i])),zero);
  const t=mean(p);
  const pred=[["ORACLE",p],["PRIOR",Array(4).fill(quarter)],["FORWARD_PRODUCT",s.forward_KL_optimum_product_of_true_marginals.map(F)]];
  for(const grid of ["COARSE","FINE"]){const w=byKey.get(key+"|"+grid);if(!w)throw Error("missing "+key+" "+grid);pred.push([grid,w.selected_mean_field_joint_exact.map(F)]);}
  const group={source:s.source,m:s.positive_observations_m,true_future_success_probability:S(t),methods:{}};
  for(const [name,q] of pred){
   const a=mean(q),risk=add(mul(t,mul(sub(one,a),sub(one,a))),mul(sub(one,t),mul(a,a))),oracle=mul(t,sub(one,t)),excess=sub(risk,oracle),bias2=mul(sub(a,t),sub(a,t));
   if(!eq(excess,bias2))throw Error("Brier identity "+key+" "+name);
   const r={source:s.source,m:s.positive_observations_m,method:name,forecast_success_probability:S(a),true_success_probability:S(t),brier_risk:S(risk),excess_brier:S(excess),exact_brier_identity_pass:true};
   rows.push(r);group.methods[name]=r;
  }
  comparisons.push({source:s.source,m:s.positive_observations_m,coarse_minus_fine_excess:S(sub(F(group.methods.COARSE.excess_brier),F(group.methods.FINE.excess_brier))),fine_worse_than_coarse:Number(sub(F(group.methods.FINE.excess_brier),F(group.methods.COARSE.excess_brier)).n)>0});
 }
 let fineBetter=0,fineWorse=0,fineEqual=0,priorBetter=0,priorWorse=0,priorEqual=0;
 for(const c of comparisons){
  const g=rows.filter(r=>r.source===c.source&&r.m===c.m);
  const c0=F(g.find(x=>x.method==="COARSE").excess_brier),f0=F(g.find(x=>x.method==="FINE").excess_brier),pr=F(g.find(x=>x.method==="PRIOR").excess_brier);
  const d=sub(c0,f0);if(d.n>0n)fineBetter++;else if(d.n<0n)fineWorse++;else fineEqual++;
  const d2=sub(pr,f0);if(d2.n>0n)priorWorse++;else if(d2.n<0n)priorBetter++;else priorEqual++;
 }
 const nontrivial=rows.filter(r=>r.method==="ORACLE"&&r.true_success_probability!==rows.find(v=>v.source===r.source&&v.m===r.m&&v.method==="PRIOR").forecast_success_probability).length;
 if(rows.length!==60||comparisons.length!==12||nontrivial===0)throw Error("coverage");
 return {protocol:"protocols/R196_POSTERIOR_PREDICTIVE_BRIER_24_THIRD_METHOD_FREEZE_2026-10-27.md",source_blobs:["490c30eb8bd912afcb6e8d2d1cafacb1928b2f39","f39ccf402edbfbc11f9d8eb135efec6fff838b0e"],evidence_class:"E1_ARTIFICIAL_INTERNAL",sources:12,selected_grid_worlds:24,predictors:5,exact_rows:rows.length,summary:{fine_better_than_coarse:fineBetter,fine_worse_than_coarse:fineWorse,fine_equal_to_coarse:fineEqual,prior_better_than_fine:priorBetter,prior_worse_than_fine:priorWorse,prior_equal_to_fine:priorEqual,oracle_vs_prior_nontrivial:nontrivial},comparisons,rows};
};
process.stdout.write(JSON.stringify(compute(src,worlds),null,2)+"\n");
