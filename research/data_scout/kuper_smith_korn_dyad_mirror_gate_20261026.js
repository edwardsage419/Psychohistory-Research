"use strict";
// Public, already anonymized human data. Never upload raw participant rows.
// Usage: node research/data_scout/kuper_smith_korn_dyad_mirror_gate_20261026.js /path/to/data_Exp_1_2_3_cleaned.csv
// Self test: node research/data_scout/kuper_smith_korn_dyad_mirror_gate_20261026.js --selftest
function auditCsv(csv,synthetic=false){
 const lines=csv.split(/\r?\n/).filter(s=>s.trim().length);
 const byKey=new Map(), groups=new Map(), people=new Set(), pairs=new Set();
 const expRows={1:0,2:0,3:0},missingLag={self:0,opponent:0};
 let badColumns=0,duplicate=0,badActions=0,badOpponentId=0,missingOpponentIdentityExp1=0;
 for(const [i,line] of lines.entries()){
   const fields=line.split(",");
   if(fields.length!==31){badColumns++;continue;}
   const a=fields.map(x=>x.trim().toLowerCase()==="nan"||x.trim()===""?NaN:Number(x.trim()));
   const [exp,group,self,opp,trial]=a;
   if(![1,2,3].includes(exp)||!Number.isInteger(group)||!Number.isInteger(self)||!Number.isInteger(trial))throw Error("invalid identity at line "+(i+1));
   const k=[exp,group,self,trial].join(":");
   if(byKey.has(k))duplicate++;
   const rec={exp,group,self,opp,trial,own:a[24],other:a[25],block:a[7],prevOwn:a[29],prevOther:a[30]};
   byKey.set(k,rec);
   expRows[exp]++;people.add(exp+":"+self);
   if(!groups.has(exp+":"+group))groups.set(exp+":"+group,new Set());
   groups.get(exp+":"+group).add(self);
   if(![0,1].includes(rec.own)||![0,1].includes(rec.other))badActions++;
   if(Number.isNaN(rec.prevOwn))missingLag.self++;
   if(Number.isNaN(rec.prevOther))missingLag.opponent++;
   if(exp===1){if(Number.isNaN(opp))missingOpponentIdentityExp1++;}
   else {if(!Number.isInteger(opp)||opp===self)badOpponentId++;
     if(Number.isInteger(opp)){const p=[exp,group,Math.min(self,opp),Math.max(self,opp)].join(":");pairs.add(p);}
   }
 }
 let reciprocalPresent=0,reciprocalAbsent=0,reciprocalIdentityConflict=0,reciprocalActionConflict=0,reciprocalBlockConflict=0,completeUndirected=0;
 for(const r of byKey.values()){
   if(r.exp===1)continue;
   if(!Number.isInteger(r.opp))continue;
   const other=byKey.get([r.exp,r.group,r.opp,r.trial].join(":"));
   if(!other){reciprocalAbsent++;continue;}
   reciprocalPresent++;
   if(other.opp!==r.self)reciprocalIdentityConflict++;
   if(other.own!==r.other||other.other!==r.own)reciprocalActionConflict++;
   if(other.block!==r.block)reciprocalBlockConflict++;
   if(r.self<r.opp&&other.opp===r.self&&other.own===r.other&&other.other===r.own)completeUndirected++;
 }
 const summary={
   source:"dnhi-lab/losses_gains_2x2 fixed commit 345348cdc0018e8e030b05fb47dc845fd3e0d29a",
   input_kind:synthetic?"SYNTHETIC_SELFTEST":"PUBLIC_AUTHOR_CLEANED_CSV",
   total_rows:lines.length,parsed_rows:byKey.size,experiments:expRows,participants:people.size,groups:groups.size,
   experiment_2_3_directed_rows:expRows[2]+expRows[3],distinct_experiment_2_3_dyads:pairs.size,
   group_participant_counts:[...groups.entries()].map(([group,p])=>({group,count:p.size})).sort((a,b)=>a.group.localeCompare(b.group)),
   reciprocal_present_directed_rows:reciprocalPresent,reciprocal_missing_directed_rows:reciprocalAbsent,
   reciprocal_identity_conflicts:reciprocalIdentityConflict,reciprocal_action_conflicts:reciprocalActionConflict,
   reciprocal_block_conflicts:reciprocalBlockConflict,complete_undirected_trial_events:completeUndirected,
   bad_column_rows:badColumns,duplicate_participant_trial_keys:duplicate,bad_actions:badActions,
   bad_opponent_identity_exp2_3:badOpponentId,exp1_rows_missing_opponent_id:missingOpponentIdentityExp1,missing_lag_fields:missingLag,
   prior_audit_counts_match:synthetic?null:lines.length===33702&&people.size===114&&groups.size===20&&expRows[2]+expRows[3]===26601&&pairs.size===239,
   model_or_scoring_modified:false,R073_transfer_approved:false,license_gate:"PENDING_SEPARATE_DATA_SCOPE_REVIEW"
 };
 return summary;
}
function selfTest(){
 function row(exp,group,self,opp,trial,own,other){
  const a=Array(31).fill("NaN");a[0]=exp;a[1]=group;a[2]=self;a[3]=opp;a[4]=trial;a[7]=1;a[24]=own;a[25]=other;return a.join(",");
 }
 const r=auditCsv([row(2,5,111,112,1,1,0),row(2,5,112,111,1,0,1)].join("\n"),true);
 if(r.reciprocal_present_directed_rows!==2||r.complete_undirected_trial_events!==1||r.reciprocal_action_conflicts!==0)throw Error("mirror positive selftest");
 const b=auditCsv([row(2,5,111,112,1,1,0),row(2,5,112,111,1,1,1)].join("\n"),true);
 if(b.reciprocal_action_conflicts!==2)throw Error("mirror negative selftest");
 return {selftest:"PASS",positive_mirrors:2,negative_mirror_conflicts:2};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");
 if(process.argv[2]==="--selftest")process.stdout.write(JSON.stringify(selfTest(),null,2)+"\n");
 else if(process.argv[2])process.stdout.write(JSON.stringify(auditCsv(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");
 else {process.stderr.write("Provide public cleaned CSV path or --selftest\n");process.exitCode=2;}
}
