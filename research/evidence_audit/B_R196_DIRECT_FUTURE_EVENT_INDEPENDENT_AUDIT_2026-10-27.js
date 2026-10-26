#!/usr/bin/env node
"use strict";
const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
const src=JSON.parse(fs.readFileSync(path.join(root,"research/R196/R196_ALL_12_EXACT_POSTERIOR_SOURCES.json"),"utf8"));
const worlds=JSON.parse(fs.readFileSync(path.join(root,"research/R196/R196_EXACT_RESULTS.json"),"utf8"));
const receipt=JSON.parse(fs.readFileSync(path.join(root,"research/validation/R196_POSTERIOR_PREDICTIVE_BRIER_60_EXACT_RECEIPT_2026-10-27.json"),"utf8"));
const audit=function audit(src,worlds,receipt){
 const abs=x=>x<0n?-x:x;
 function red(n,d){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}let a=abs(n),b=d;while(b){const t=a%b;a=b;b=t;}return [n/a,d/a];}
 function from(x){const s=String(x).split("/");return red(s[0],s[1]||"1");}
 const plus=(a,b)=>red(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const minus=(a,b)=>red(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const times=(a,b)=>red(a[0]*b[0],a[1]*b[1]);
 const equal=(a,b)=>a[0]*b[1]===b[0]*a[1];
 const z=from(0),one=from(1),quarter=from("1/4");
 const all=worlds.all_worlds;
 let comparisons=0,normalizations=0,errors=[],positiveControl=0,wrongRiskCaught=0;
 for(const s of src.exact_source_truths){
  const truth=s.exact_posterior_00_01_10_11.map(from),rates=s.weights.map(w=>red(w,Math.max(...s.weights)));
  const qtypes={ORACLE:truth,PRIOR:[quarter,quarter,quarter,quarter],FORWARD_PRODUCT:s.forward_KL_optimum_product_of_true_marginals.map(from)};
  for(const grid of ["COARSE","FINE"]){const w=all.find(x=>x.source===s.source&&x.m_positive_likelihood_observations===s.positive_observations_m&&x.grid===grid);if(!w)throw Error("missing world");qtypes[grid]=w.selected_mean_field_joint_exact.map(from);}
  const predTruth=truth.reduce((a,b,i)=>plus(a,times(b,rates[i])),z);
  const priorPred=rates.reduce((a,b)=>plus(a,times(quarter,b)),z);
  if(!equal(predTruth,priorPred))positiveControl++;
  for(const [method,q] of Object.entries(qtypes)){
   const mass=q.reduce(plus,z);if(!equal(mass,one))throw Error("mass "+method);normalizations++;
   const a=q.reduce((acc,qi,i)=>plus(acc,times(qi,rates[i])),z);
   const falseForecast=minus(one,a);
   const directRisk=truth.reduce((acc,p,i)=>{
    const future1=times(rates[i],times(falseForecast,falseForecast));
    const future0=times(minus(one,rates[i]),times(a,a));
    return plus(acc,times(p,plus(future1,future0)));
   },z);
   const oracleRisk=times(predTruth,minus(one,predTruth));
   const excess=minus(directRisk,oracleRisk);
   const row=receipt.rows.find(x=>x.source===s.source&&x.m===s.positive_observations_m&&x.method===method);
   if(!row)throw Error("missing row");
   for(const [calc,field] of [[a,"forecast_success_probability"],[directRisk,"brier_risk"],[excess,"excess_brier"]]){
    comparisons++;if(!equal(calc,from(row[field])))errors.push(s.source+"|"+s.positive_observations_m+"|"+method+"|"+field);
   }
   const wrong=truth.reduce((acc,p,i)=>plus(acc,times(p,times(rates[i],times(falseForecast,falseForecast)))),z);
   if(!equal(wrong,directRisk))wrongRiskCaught++;
  }
 }
 if(comparisons!==180||normalizations!==60||errors.length||positiveControl===0||wrongRiskCaught===0)throw Error("audit failed "+JSON.stringify({comparisons,normalizations,errors,positiveControl,wrongRiskCaught}));
 return {audit:"B_R196_DIRECT_LATENT_FUTURE_EVENT_ENUMERATION",evidence_class:"INTERNAL_E1_PROGRAMMATIC_RECOMPUTATION",source_sha1:[ "490c30eb8bd912afcb6e8d2d1cafacb1928b2f39","f39ccf402edbfbc11f9d8eb135efec6fff838b0e"],main_receipt_blob_sha1:"PENDING",source_worlds:12,method_rows:60,exact_comparisons:comparisons,normalizations,errors,negative_controls:{wrong_independent_new_latent_detected_sources:positiveControl,missing_future_zero_term_detected_methods:wrongRiskCaught},external_independent_replication:false};
};
process.stdout.write(JSON.stringify(audit(src,worlds,receipt),null,2)+"\n");
