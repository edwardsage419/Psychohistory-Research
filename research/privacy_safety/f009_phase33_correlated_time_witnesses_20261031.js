#!/usr/bin/env node
"use strict";
// F009 phase33: synthetic three-clock witness common-mode experiment.
// No network, signatures, credentials, personal data, or paid services.
const assert=require("node:assert/strict");
function evaluate(mask){
 const A=(mask&1)?110:90,B=(mask&2)?110:90,C=(mask&4)?110:90;
 const sharedAB=Boolean(mask&8),freshC=Boolean(mask&16);
 const epochCurrent=Boolean(mask&32),rootHealthy=Boolean(mask&64);
 const signaturesValid=Boolean(mask&128);
 const naive=signaturesValid&&[A,B,C].filter(t=>t>=100).length>=2;
 const strict=!signaturesValid?"REJECT":
  (!rootHealthy||!freshC||!epochCurrent)?"UNKNOWN":
  (A===110&&B===110&&C===110?"REVIEW":"UNKNOWN");
 // A and B share a failure domain when sharedAB is true; C is independent.
 // REVIEW means only eligible for human review, never automated authorization.
 return {A,B,C,sharedAB,freshC,epochCurrent,rootHealthy,signaturesValid,naive,strict};
}
const counts={REVIEW:0,UNKNOWN:0,REJECT:0,naive:0,naive_outside_review:0};
for(let i=0;i<256;i++){
 const s=evaluate(i);counts[s.strict]++;
 if(s.naive){counts.naive++;if(s.strict!=="REVIEW")counts.naive_outside_review++;}
 if(s.strict==="REVIEW"){
  assert.equal(s.A,110);assert.equal(s.B,110);assert.equal(s.C,110);
  assert.ok(s.freshC&&s.epochCurrent&&s.rootHealthy&&s.signaturesValid);
 }
}
assert.deepEqual(counts,{REVIEW:2,UNKNOWN:126,REJECT:128,naive:64,naive_outside_review:62});
assert.equal(evaluate(1|2|8|128).naive,true); // A/B agree in one failure domain.
assert.equal(evaluate(1|2|8|128).strict,"UNKNOWN");
console.log(JSON.stringify({states:256,assertions:"all_pass",counts,scope:"synthetic_E1"}));
