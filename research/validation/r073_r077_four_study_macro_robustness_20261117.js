#!/usr/bin/env node
"use strict";
/*
 R073/R074/R075/R077: bounded human cross-study MACRO evidence robustness.
 Source documents are the already-published anonymous study-level receipts.
 No participant, session-specific scores, original per-action rows or new
 E2/E3 scoring are accessed. Study-level observations are not i.i.d. samples.

 Run from repository root:
   node research/validation/r073_r077_four_study_macro_robustness_20261117.js
 */
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const ROOT = path.resolve(__dirname, "../..");
const INPUTS = [
  {id:"R073", path:"research/R073/R073_E2_HUMAN_12_SESSION_MEMORY_LOSO_RESULTS.json",
   blob:"6dc0b5958c4dd0418f09e66cdbc7ae363d8186e4", class:"internal_same_author_E2_LOSO"},
  {id:"R074", path:"research/R074/R074_EXTERNAL_REAL_HUMAN_18_SESSION_E3_RESULTS.json",
   blob:"c10edcc19526278aac6be6811b5cab00e24d7b20", class:"independent_author_study_refit_within_treatment_E3"},
  {id:"R075", path:"research/R075/R075_REAL_THIRD_HUMAN_18_SESSION_E3_RESULTS.json",
   blob:"50e3cbef9184ea36cd5edb5e3fe7abae40dd19e6", class:"independent_author_study_refit_intended_target_E3"},
  {id:"R077", path:"research/R077/R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json",
   blob:"13946754afc06e529f2d3a2072a7bae297453fa9", class:"independent_author_target_R073_donor_zero_target_fit_E3"}
];
const NAME31="M3_JOINT_LAST_VS_M1_OWN_LAST";
const NAME43="M4_JOINT_TWO_LAGS_VS_M3_JOINT_LAST";
const MODEL_NAMES=["M1_OWN_LAST","M3_JOINT_LAST","M4_JOINT_TWO_LAGS"];
function requireTrue(v,k) {if(v!==true)throw new Error("FAIL_CLOSED_R073_R077_"+k);}
function blobSHA(buf) {return crypto.createHash("sha1").update(Buffer.from("blob "+buf.length+"\0")).update(buf).digest("hex");}
function allFinite(v) {return v.every(x=>typeof x==="number"&&Number.isFinite(x));}
function groupPair(x) {
  return {
    delta: (x.fix.Brier_delta_compared_to_reference+x.rand.Brier_delta_compared_to_reference)/2,
    better:x.fix.sessions_better+x.rand.sessions_better,
    worse:x.fix.sessions_worse+x.rand.sessions_worse,
    equal:(x.fix.sessions_equal??0)+(x.rand.sessions_equal??0)
  };
}
function readStudy(input,raw) {
  const j=JSON.parse(raw);
  requireTrue(j.research_id===input.id,"STUDY_ID_"+input.id);
  let names,m,counts,session,p31,p43;
  if(input.id==="R073") {
    names=j.Brier_and_logloss_session_macro;
    m=key=>names[key].all_12_sessions_equal_weight_Brier;
    session=j.source_universe.sessions;
    p31=groupPair(j.session_equal_paired_Brier_comparisons[NAME31]);
    p43=groupPair(j.session_equal_paired_Brier_comparisons[NAME43]);
    requireTrue(j.source_universe.individual_scorable_outcomes===18424,"R073_COUNT");
  } else if(input.id==="R074") {
    names=j.results.model_macro;
    m=key=>names[key].all_sessions_equal_weight_Brier;
    session=j.original_session_count;
    const r=j.results.paired_comparisons;
    const parsed=v=>({delta:v.all_sessions_equal_weight_Brier_delta,better:v.all_sessions_better,worse:v.all_sessions_worse,equal:v.all_sessions_equal});
    p31=parsed(r[NAME31]);p43=parsed(r[NAME43]);
    requireTrue(j.results.scored_decisions===15338,"R074_COUNT");
  } else if(input.id==="R075") {
    names=j.results.model_macro;
    m=key=>names[key].all_18_sessions_equal_weight_Brier;
    session=j.true_source_sessions;
    const r=j.results.paired_comparisons;
    const parsed=v=>({delta:v.Brier_delta_all_sessions_equal_weight,better:v.sessions_better,worse:v.sessions_worse,equal:v.sessions_equal});
    p31=parsed(r[NAME31]);p43=parsed(r[NAME43]);
    requireTrue(j.scored_targets===26116,"R075_COUNT");
  } else if(input.id==="R077") {
    names=j.results.models;
    m=key=>names[key].all_original_sessions_equal_Brier;
    session=j.results.original_session_count;
    const r=j.results.paired_differences;
    const parsed=v=>({delta:v.Brier_delta_all_original_sessions_equal,better:v.better,worse:v.worse,equal:v.equal});
    p31=parsed(r[NAME31]);p43=parsed(r[NAME43]);
    requireTrue(j.results.scored_t3_human_events===1040 && j.results.target_labels_used_in_training===0,"R077_COUNT");
  } else throw Error("unknown study");

  requireTrue([12,18,18,15][INPUTS.findIndex(x=>x.id===input.id)]===session,"SESSION_COUNT_"+input.id);
  const scores=MODEL_NAMES.map(m);
  requireTrue(allFinite(scores)&&scores.every(x=>x>=0&&x<=1),"SCORE_DOMAIN_"+input.id);
  const pairs=[p31,p43];
  for(const [index,p] of pairs.entries()) {
    requireTrue(allFinite([p.delta,p.better,p.worse,p.equal??0]),"PAIR_FIELDS_"+input.id);
    requireTrue(p.better+p.worse+(p.equal??0)===session,"SIGN_DENOM_"+input.id);
    requireTrue(Math.abs((scores[index+1]-scores[index])-p.delta)<=1e-12,"MACRO_PAIRED_MISMATCH_"+input.id);
  }
  return {
    study:input.id,
    original_study_equal_session_count:session,
    study_fitting_design:input.class,
    M1_Brier:scores[0],M3_Brier:scores[1],M4_Brier:scores[2],
    M3_minus_M1:p31.delta,M4_minus_M3:p43.delta,
    M3_vs_M1_session_better:p31.better,M3_vs_M1_session_worse:p31.worse,
    M4_vs_M3_session_better:p43.better,M4_vs_M3_session_worse:p43.worse,
    M3_over_M1_relative_improvement:-(p31.delta/scores[0]),
    M4_over_M3_relative_improvement:-(p43.delta/scores[1])
  };
}
function mean(a) {return a.reduce((s,v)=>s+v,0)/a.length;}
function summarize(rows) {
  requireTrue(rows.length===4&&rows.map(x=>x.study).join(",")==="R073,R074,R075,R077","STUDY_UNIVERSE");
  const keys=["M3_minus_M1","M4_minus_M3"];
  const primary=Object.fromEntries(keys.map(k=>[k,mean(rows.map(x=>x[k]))]));
  const leaveOneOut=rows.map((row,i)=>({
    excluded_study:row.study,
    M3_minus_M1:mean(rows.filter((_,j)=>i!==j).map(x=>x.M3_minus_M1)),
    M4_minus_M3:mean(rows.filter((_,j)=>i!==j).map(x=>x.M4_minus_M3))
  }));
  const convexHull=Object.fromEntries(keys.map(k=>[k,{
     min:Math.min(...rows.map(x=>x[k])),max:Math.max(...rows.map(x=>x[k]))
  }]));
  const positive=rows.filter(x=>x.M4_minus_M3>0);
  requireTrue(positive.length===1&&positive[0].study==="R074","HETEROGENEITY_WITNESS");
  const otherAvg=mean(rows.filter(x=>x.study!=="R074").map(x=>x.M4_minus_M3));
  const threshold=-otherAvg/(positive[0].M4_minus_M3-otherAvg);
  requireTrue(threshold>0&&threshold<1,"WEIGHT_THRESHOLD");
  requireTrue(convexHull.M3_minus_M1.max<0,"M3_ANY_CONVEX_WEIGHT_STILL_NEGATIVE");
  requireTrue(primary.M4_minus_M3<0 && leaveOneOut.every(x=>x.M4_minus_M3<0),"M4_EQUAL_WEIGHT_LOO");
  const events=[18424,15338,26116,1040];
  return {
    status:"PASS_FOUR_DISTINCT_STUDY_ARCHIVED_MACRO_ROBUSTNESS",
    scope:"POST_HOC_NONBLIND_REANALYSIS_OF_FOUR_EXISTING_HUMAN_STUDY_MACRO_RECEIPTS",
    participant_level_original_data_accessed:false,
    all_study_records_exist_before_this_audit:true,
    original_study_count:4,
    sum_of_reported_sessions_descriptive_only:rows.reduce((s,x)=>s+x.original_study_equal_session_count,0),
    original_individual_scored_events_by_study:events,
    studies:rows,
    equal_four_study_average_Brier_delta:primary,
    exact_leave_one_study_out_equal_others:leaveOneOut,
    arbitrary_nonnegative_study_weight_delta_range:convexHull,
    R074_weight_cutoff_with_three_other_studies_equal:threshold,
    R074_weight_cutoff_definition:"M4_vs_M3 study mixture changes sign at this R074 weight, with other three studies sharing remaining weight equally",
    primary_M3_sign_robust_for_any_convex_study_weights:true,
    secondary_M4_sign_robust_for_any_convex_study_weights:false,
    subject_level_standard_errors_reconstructable:false,
    study_level_independent_recruitment_verified_this_run:false,
    descriptive_sensitivity_only_no_independence_based_p_values:true,
    transfer_methods_not_identical:"R073 internal refit; R074/R075 external refit; R077 R073 source-trained zero target fit",
    causal_mechanism_identified:false,
    earlier_frozen_study_results_modified:false,
    new_real_human_E2:0,new_historical_E3:0
  };
}
function main() {
 const inputData=INPUTS.map(x=>{
   const f=fs.readFileSync(path.join(ROOT,x.path));
   requireTrue(blobSHA(f)===x.blob,"SOURCE_BLOB_MISMATCH_"+x.id);
   return {identity:x,data:JSON.parse(f.toString("utf8"))};
 });
 const studies=inputData.map(x=>readStudy(x.identity,JSON.stringify(x.data)));
 const saved=JSON.parse(JSON.stringify(inputData[1].data));
 saved.results.model_macro.M3_JOINT_LAST.all_sessions_equal_weight_Brier+=0.03;
 let rejected=false;
 try {readStudy(INPUTS[1],JSON.stringify(saved));}catch(e){rejected=String(e.message)==="FAIL_CLOSED_R073_R077_MACRO_PAIRED_MISMATCH_R074";}
 requireTrue(rejected,"MACRO_SCORE_MUTANT_FAIL_OPEN");
 const x=summarize(studies);
 x.original_git_blob_sha1=Object.fromEntries(INPUTS.map(v=>[v.id,v.blob]));
 x.negative_controls=["R074_MACRO_SCORE_MUTATION_REJECTED","ALL_FOUR_GIT_BLOB_SHA1_PINNED"];
 console.log(JSON.stringify(x,null,2));
}
if(require.main===module)main();
module.exports={readStudy,summarize};
