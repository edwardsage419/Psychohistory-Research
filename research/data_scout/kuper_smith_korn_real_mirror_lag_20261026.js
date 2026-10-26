"use strict";
// Public author-cleaned, deidentified CSV audit. Output aggregates only.
// Usage: node kuper_smith_korn_real_mirror_lag_20261026.js /path/to/cleaned.csv
function audit(csv){
 const rows=new Map(),members=new Map(),exp={1:0,2:0,3:0};
 const lines=csv.trim().split(/\r?\n/);
 for(const [i,line] of lines.entries()){
  const a=line.split(",").map(s=>s.trim()===""||s.trim().toLowerCase()==="nan"?NaN:Number(s));
  if(a.length!==31)throw Error("invalid 31-field record "+(i+1));
  const [e,g,s,o,t]=a;if(![1,2,3].includes(e)||![g,s,t].every(Number.isInteger))throw Error("invalid identity");
  const key=[e,g,s,t].join(":");if(rows.has(key))throw Error("duplicate participant-trial");
  rows.set(key,{e,g,s,o,t,block:a[7],own:a[24],other:a[25],prevOwn:a[29],prevOther:a[30]});
  const k=e+":"+g;if(!members.has(k))members.set(k,new Set());members.get(k).add(s);exp[e]++;
 }
 const mirror={paired_directed_rows:0,missing_partner_excluded_from_cleaned_group:0,missing_partner_trial_in_retained_group:0,
  reciprocal_identity_conflicts:0,reciprocal_action_conflicts:0,reciprocal_block_conflicts:0};
 const lag={prior_trial_present:0,prior_trial_absent:0,previous_self_action_match:0,previous_self_action_mismatch:0,
  previous_opponent_action_match:0,previous_opponent_action_mismatch:0,lag_own_missing_with_prior:0,
  lag_other_missing_with_prior:0,previous_trial_same_block:0,previous_trial_different_block:0};
 for(const x of rows.values()){
  if(x.e!==1){
   const m=rows.get([x.e,x.g,x.o,x.t].join(":"));
   if(m){mirror.paired_directed_rows++;
    if(m.o!==x.s)mirror.reciprocal_identity_conflicts++;
    if(m.own!==x.other||m.other!==x.own)mirror.reciprocal_action_conflicts++;
    if(m.block!==x.block)mirror.reciprocal_block_conflicts++;
   }else if(!members.get(x.e+":"+x.g).has(x.o))mirror.missing_partner_excluded_from_cleaned_group++;
   else mirror.missing_partner_trial_in_retained_group++;
  }
  const prev=rows.get([x.e,x.g,x.s,x.t-1].join(":"));
  if(!prev){lag.prior_trial_absent++;continue;}
  lag.prior_trial_present++;
  if(prev.block===x.block)lag.previous_trial_same_block++;else lag.previous_trial_different_block++;
  if(Number.isNaN(x.prevOwn))lag.lag_own_missing_with_prior++;
  else if(x.prevOwn===prev.own)lag.previous_self_action_match++;else lag.previous_self_action_mismatch++;
  if(Number.isNaN(x.prevOther))lag.lag_other_missing_with_prior++;
  else if(x.prevOther===prev.other)lag.previous_opponent_action_match++;else lag.previous_opponent_action_mismatch++;
 }
 if(lines.length!==rows.size)throw Error("row count mismatch");
 return {source_repository:"dnhi-lab/losses_gains_2x2",fixed_commit:"345348cdc0018e8e030b05fb47dc845fd3e0d29a",
  author_cleaned_csv_git_blob:"ffd6776f3e9fd1444c84e50e4c61e3ff418a2488",
  source_bytes:3139058,cleaned_rows:rows.size,rows_by_experiment:exp,retained_group_count:members.size,
  experiment_2_3_directed_rows:exp[2]+exp[3],mirror,lag,
  status:"REAL_PUBLIC_HUMAN_DATA_STRUCTURAL_AUDIT_ONLY",prediction_scores:0,R073_transfer_approved:false,
  data_specific_license:"PENDING",new_human_E2_predictive_evidence:0,new_E3:0};
}
if(typeof module!=="undefined"&&module.exports)module.exports={audit};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==3){process.stderr.write("Usage: node script cleaned.csv\n");process.exit(2);}
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");
}