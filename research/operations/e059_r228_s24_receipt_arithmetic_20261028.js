#!/usr/bin/env node
"use strict";
// Run from repository root: node research/operations/e059_r228_s24_receipt_arithmetic_20261028.js
const fs=require("fs");
function auditReceipt(txt, originalTxt) {
 const data=JSON.parse(txt), original=JSON.parse(originalTxt);
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a};
 const F=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
 const P=s=>{let z=String(s).split("/");return F(z[0],z[1]||1)};
 const S=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
 const sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const Z=F(0);
 let n=0;const ok=(v,msg)=>{n++;if(!v)throw Error("E059 "+msg)};
 ok(data.rows.length===56,"56 rows");ok(data.worlds===8&&data.scenarios===7&&data.conditions===56,"metadata");
 ok(data.structural_source_slots===2688&&data.positive_source_slots===2520,"slots");
 ok(data.evidence==="E1_FINITE_ARTIFICIAL_ONLY"&&data.external_human_E2===0&&data.external_history_E3===0,"E1");
 const seen=new Set(), worlds=new Set(), scenarios=new Set();
 for(const row of data.rows){
  const id=row.world+"|"+row.scenario;ok(!seen.has(id),"duplicate "+id);seen.add(id);worlds.add(row.world);scenarios.add(row.scenario);
  const fields=["old_full_brier","new_full_brier","old_score_brier","new_score_brier","full_drift_excess","score_drift_excess","old_full_calibration_bias","old_score_calibration_bias","new_score_minus_full"];
  for(const k of fields)ok(typeof row[k]==="string"&&S(P(row[k]))===row[k],"canonical rational "+id+" "+k);
  ok(eq(sub(P(row.old_full_brier),P(row.new_full_brier)),P(row.full_drift_excess)),"full excess "+id);
  ok(eq(sub(P(row.old_score_brier),P(row.new_score_brier)),P(row.score_drift_excess)),"score excess "+id);
  ok(eq(sub(P(row.new_score_brier),P(row.new_full_brier)),P(row.new_score_minus_full)),"score minus full "+id);
  ok(P(row.full_drift_excess)[0]>=0n&&P(row.score_drift_excess)[0]>=0n,"nonnegative excess "+id);
  ok(P(row.new_score_minus_full)[0]>=0n,"nonnegative info gain "+id);
  ok(row.structural_atoms===48&&row.positive_atoms>=0&&row.positive_atoms<=48,"support "+id);
  if(row.scenario==="STABLE"){
   const o=original.world_results.find(x=>x.world===row.world);
   ok(!!o,"original world "+id);
   ok(eq(P(row.old_full_brier),P(o.independent_fourth_item_full_pattern_brier)),"stable full "+id);
   ok(eq(P(row.old_score_brier),P(o.independent_fourth_item_total_score_brier)),"stable score "+id);
   ok(eq(P(row.old_full_calibration_bias),Z)&&eq(P(row.old_score_calibration_bias),Z),"stable calibration "+id);
  }
  if(row.scenario.startsWith("GLOBAL_")&&row.scenario!=="STABLE"){
   let expected=row.scenario.includes("MINUS")?1:-1;
   ok(P(row.old_full_calibration_bias)[0]*BigInt(expected)>0n,"global full sign "+id);
   ok(P(row.old_score_calibration_bias)[0]*BigInt(expected)>0n,"global score sign "+id);
  }
 }
 ok(worlds.size===8&&scenarios.size===7&&seen.size===56,"complete grid");
 ok(data.rows.reduce((s,x)=>s+x.positive_atoms,0)===2520,"positive slots summed");
 for(const [a,b] of [["BASE_RASCH","LOCATION_SHIFT_ALIAS"],["SCALE_HIGH_DISCRIM","SCALE_LOW_DISCRIM_ALIAS"]]){
  for(const scenario of scenarios){
   const x=data.rows.find(z=>z.world===a&&z.scenario===scenario),y=data.rows.find(z=>z.world===b&&z.scenario===scenario);
   ok(!!x&&!!y,"alias rows");
   for(const k of ["old_full_brier","new_full_brier","old_score_brier","new_score_brier","full_drift_excess","score_drift_excess","old_full_calibration_bias","old_score_calibration_bias","new_score_minus_full"])ok(eq(P(x[k]),P(y[k])),"alias "+a+" "+scenario+" "+k);
  }
 }
 return {checks:n,failures:0,conditions:56,scope:"receipt_arithmetic_and_original_stable_regression_only",third_source_replay:false};
}
if(require.main===module){
 const receipt=fs.readFileSync("research/validation/R228_S24_56_CONDITION_EXACT_RECEIPT_2026-10-28.json","utf8");
 const original=fs.readFileSync("research/R228/R228_EXACT_RESULTS.json","utf8");
 process.stdout.write(JSON.stringify(auditReceipt(receipt,original),null,2)+"\n");
}
