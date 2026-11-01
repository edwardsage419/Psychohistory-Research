"use strict";
// F009 phase53: synthetic cross-device status fork, no real keys or credentials.
const assert=require("node:assert/strict");
function guard(s){
 if(!s.request)return "NO_REQUEST";
 if(!s.accountBound||!s.signatureValid||!s.authorityCurrent)return "REJECT";
 if(!s.trustedCheckpoint||!s.trustedTime)return "UNKNOWN_QUARANTINE";
 if(s.forkDetected||s.keyLineageConflict)return "UNKNOWN_QUARANTINE";
 if(s.epoch<s.trustedCheckpoint.epoch)return "REJECT_STALE";
 if(s.epoch>s.trustedCheckpoint.epoch)return "UNKNOWN_QUARANTINE";
 if(s.status==="revoked")return "REJECT_REVOKED";
 if(s.status!=="active")return "UNKNOWN_QUARANTINE";
 return "REVIEW_ONLY";
}
const base={request:true,accountBound:true,signatureValid:true,authorityCurrent:true,trustedCheckpoint:{epoch:8},trustedTime:true,forkDetected:false,keyLineageConflict:false,epoch:8,status:"active"};
let tests=0;function check(p,expected){assert.equal(guard({...base,...p}),expected);tests++;}
check({},"REVIEW_ONLY");check({request:false},"NO_REQUEST");
check({epoch:7},"REJECT_STALE");check({epoch:9},"UNKNOWN_QUARANTINE");
check({status:"revoked"},"REJECT_REVOKED");check({trustedCheckpoint:null},"UNKNOWN_QUARANTINE");
check({trustedTime:false},"UNKNOWN_QUARANTINE");check({forkDetected:true},"UNKNOWN_QUARANTINE");
check({keyLineageConflict:true},"UNKNOWN_QUARANTINE");check({authorityCurrent:false},"REJECT");
check({signatureValid:false},"REJECT");check({accountBound:false},"REJECT");
const offline={...base,epoch:7,trustedCheckpoint:null};
assert.equal(guard(offline),"UNKNOWN_QUARANTINE");tests++;
assert.equal(offline.signatureValid&&offline.status==="active",true);tests++;
assert.equal(guard({...base,status:"revoked"}),"REJECT_REVOKED");tests++;
console.log(JSON.stringify({tests,naive_offline_accepts:true,strict_offline:"UNKNOWN_QUARANTINE",scope:"synthetic nonblind E1; no cryptographic implementation"}));
