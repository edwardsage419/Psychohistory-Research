#!/usr/bin/env node
"use strict";
/*
 R127 additional E1/aggregate partial-identification audit.
 The synthetic "participant" paths are mathematical witnesses only.
 No source microdata or individual movement is inferred.
 Run: node research/validation/r127_table2_distinct_ever_change_sharp_20261117.js
*/
const fs=require("node:fs");
const path=require("node:path");
const crypto=require("node:crypto");
const SRC=path.join(__dirname,"r127_primary_table2_70_periods_source_audit_20261103.js");
const SRC_BLOB="aa575a803e5547afe24eabc1f232f2b539ef1709";
const raw=fs.readFileSync(SRC);
const blob=crypto.createHash("sha1").update(Buffer.concat([
  Buffer.from("blob "+raw.length+"\0","utf8"),raw
])).digest("hex");
if(blob!==SRC_BLOB)throw Error("PINNED_SOURCE_BLOB_MISMATCH");
const match=raw.toString("utf8").match(/const TABLES = (\{[\s\S]*?\});\nconst SIZES/);
if(!match)throw Error("SOURCE_TABLE_PARSER_MISMATCH");
const TABLES=JSON.parse(match[1].replace(/(?<!")\b([1-7]):(?=\[)/g,'"$1":'));

function audit(TABLES){
  const sizes=[16,16,14,15,16,16,14],periods=10,sessions=[];
  const insist=(condition,label)=>{if(condition!==true)throw Error("GATE:"+label);};
  const sum=xs=>xs.reduce((a,b)=>a+b,0);
  let total=0,ever=0,exited=0,endpoint=0,permanent=0,checked=0;
  insist(Object.keys(TABLES).length===7,"SESSION_UNIVERSE");
  for(let group=1;group<=7;group++){
    const rows=TABLES[group],n=sizes[group-1];
    insist(Array.isArray(rows)&&rows.length===7&&rows.every(r=>Array.isArray(r)&&r.length===periods),"MATRIX_SHAPE");
    for(let t=0;t<periods;t++){
      const column=rows.map(r=>r[t]);
      insist(column.every(v=>Number.isSafeInteger(v)&&v>=0)&&sum(column)===n,"SOURCE_COUNT");
      checked+=7;
    }
    // A person constant across all ten periods in category a needs one
    // available observation in that category in every period. This is sharp.
    const permanentByAction=rows.map(r=>Math.min(...r)),always=sum(permanentByAction);
    const minEver=n-always;
    const endpointMinimum=n-sum(rows.map(r=>Math.min(r[0],r[9])));
    const alwaysLabels=permanentByAction.flatMap((count,a)=>Array(count).fill(a));
    const fullPaths=Array.from({length:n},()=>[]);
    for(let t=0;t<periods;t++){
      const remaining=rows.flatMap((r,a)=>Array(r[t]-permanentByAction[a]).fill(a));
      insist(remaining.length===n-always,"RESIDUAL_CAPACITY");
      for(let i=0;i<n;i++)fullPaths[i].push(i<always?alwaysLabels[i]:remaining[i-always]);
    }
    insist(fullPaths.filter(seq=>seq.some((x,t)=>t>0&&x!==seq[t-1])).length===minEver,"EVER_CHANGED_SHARPNESS");
    for(let t=0;t<periods;t++)for(let a=0;a<7;a++)
      insist(fullPaths.filter(seq=>seq[t]===a).length===rows[a][t],"FULL_PATH_CELL_RECONSTRUCTION");

    // Lower bound on DISTINCT individuals who ever leave effort 1 equals
    // maximum drawdown of that category's published counts across time.
    const ones=rows[6];
    let maxSeen=0,drawdown=0;
    for(const p of ones){maxSeen=Math.max(maxSeen,p);drawdown=Math.max(drawdown,maxSeen-p);}
    const risky=drawdown,neverExit=n-risky;
    let permanentEffort1=0;
    const exitPaths=Array.from({length:n},()=>[]);
    for(let t=0;t<periods;t++){
      permanentEffort1=Math.max(permanentEffort1,ones[t]-risky,0);
      const riskEffort1=ones[t]-permanentEffort1;
      insist(permanentEffort1<=neverExit&&riskEffort1>=0&&riskEffort1<=risky,"EXIT_FEASIBILITY");
      const isOne=Array.from({length:n},(_,id)=>
        id<neverExit?id<permanentEffort1:id-neverExit<riskEffort1);
      const nonOneCategories=rows.slice(0,6).flatMap((r,a)=>Array(r[t]).fill(a));
      insist(nonOneCategories.length===n-ones[t],"NON_ONE_COUNTS");
      let off=0;
      for(let i=0;i<n;i++)exitPaths[i].push(isOne[i]?6:nonOneCategories[off++]);
    }
    for(let t=0;t<periods;t++)for(let a=0;a<7;a++)
      insist(exitPaths.filter(seq=>seq[t]===a).length===rows[a][t],"EXIT_PATH_CELL_RECONSTRUCTION");
    const actualExiters=exitPaths.filter(seq=>seq.some((action,t)=>t>0&&seq[t-1]===6&&action!==6)).length;
    insist(actualExiters===risky,"DISTINCT_EXIT_SHARPNESS");

    sessions.push({session:group,n,
      maximum_always_unchanged:always,
      minimum_distinct_ever_changed:minEver,
      minimum_different_first_last:endpointMinimum,
      minimum_distinct_ever_exited_effort1:actualExiters,
      effort1_counts:ones});
    total+=n;ever+=minEver;exited+=actualExiters;endpoint+=endpointMinimum;permanent+=always;
  }
  insist(checked===490&&total===107&&permanent===7&&ever===100&&exited===17&&endpoint===89,"FROZEN_AGGREGATE_BOUNDS");
  return {status:"PASS_R127_DISTINCT_PARTICIPANT_SHARP_BOUNDS",
    source_git_blob_sha1:SRC_BLOB,
    published_cells_verified:checked,published_group_subject_count:total,
    maximum_always_unchanged_participants:permanent,
    minimum_distinct_participants_ever_changed:ever,
    minimum_distinct_participants_ever_exited_effort1:exited,
    endpoint_only_minimum_distinct_different:endpoint,
    additional_over_endpoint:ever-endpoint,
    sharpness:"TWO_SEPARATE_TEN_ROUND_SYNTHETIC_PATH_CERTIFICATES",
    groups:sessions,
    real_individual_sequences_identified:false,additional_human_E2_prediction:0,historical_E3_prediction:0
  };
}
const receipt=audit(TABLES);
// Corrupt published group-period total: must be rejected by runtime audit.
const corrupt=JSON.parse(JSON.stringify(TABLES));
corrupt[1][0][1]++;
let rejected=false;
try{audit(corrupt);}catch(e){rejected=e.message.startsWith("GATE:SOURCE_COUNT");}
if(!rejected)throw Error("MUTATED_MARGINAL_ACCEPTED");
receipt.negative_controls=["ALTERED_GROUP_TOTAL_REJECTED","GIT_BLOB_PINNED"];
console.log(JSON.stringify(receipt,null,2));
