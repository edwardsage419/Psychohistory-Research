#!/usr/bin/env node
// Free standard-library synthetic or nonblind archival audit.
function audit(inputs){
"use strict";
function check(ok,msg){if(!ok)throw Error(msg)}
function run(){
 const source=[{day:1,value:1},{day:2,value:1},{day:3,value:1}];
 const original=source.reduce((a,x)=>a+x.value,0);
 const correction={day:2,value:0,revision:2};
 const out=[];
 for(const correctionArrivesOn of [4,14]){
  const age=correctionArrivesOn-correction.day;
  const existMirror=age<=7?2:original;
  const sourceTruth=2;
  const goalMirror=2; // hypothetical historical replay, not Beeminder implementation
  const reconciled=existMirror===sourceTruth?"CONSISTENT":"UNKNOWN_RECONCILIATION_REQUIRED";
  out.push({correctionArrivesOn,age,sourceTruth,existMirror,goalMirror,reconciled});
 }
 check(original===3,"baseline");
 check(out[0].existMirror===2&&out[0].reconciled==="CONSISTENT","in-window");
 check(out[1].existMirror===3&&out[1].reconciled==="UNKNOWN_RECONCILIATION_REQUIRED","out-of-window");
 check(out.every(x=>x.goalMirror===2),"hypothetical goal replay");
 check(out.every(x=>x.sourceTruth===2),"source correction");
 const missedWebhook={fullSource:3,mirror:2,status:"UNKNOWN_RECONCILIATION_REQUIRED"};
 check(missedWebhook.fullSource!==missedWebhook.mirror,"webhook loss");
 return {status:"PASS",assertions:6,rows:out,missedWebhook,scope:"SYNTHETIC_POLICY_COMPARISON_ONLY"};
}
return run();
}
const inputs={};
console.log(JSON.stringify(audit(inputs),null,2));
