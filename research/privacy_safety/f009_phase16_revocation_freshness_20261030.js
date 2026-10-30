#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
// These booleans are assumed oracle results. No actual cryptographic verification.
function decide(x){
 if(!x.signatureVerified||!x.accountBound||!x.nonceUnused||x.keyEpoch==='REVOKED'||x.revocation==='REVOKED')return 'REJECT';
 if(x.keyEpoch==='UNKNOWN'||x.revocation==='UNKNOWN'||x.freshness==='STALE')return 'DEFER_UNKNOWN';
 return 'REVIEWABLE_SOURCE_CLAIM';
}
const states=[];
for(const keyEpoch of ['CURRENT','REVOKED','UNKNOWN'])
 for(const revocation of ['GOOD','REVOKED','UNKNOWN'])
  for(const freshness of ['FRESH','STALE'])
   for(const signatureVerified of [false,true])
    for(const accountBound of [false,true])
     for(const nonceUnused of [false,true]){
      const x={keyEpoch,revocation,freshness,signatureVerified,accountBound,nonceUnused};
      states.push({...x,decision:decide(x)});
     }
const counts={REJECT:0,DEFER_UNKNOWN:0,REVIEWABLE_SOURCE_CLAIM:0};
for(const x of states)counts[x.decision]++;
let assertions=0;const t=(x,msg)=>{assert.ok(x,msg);assertions++};
t(states.length===144,'all states');t(counts.REVIEWABLE_SOURCE_CLAIM===1,'only one reviewable');
t(Object.values(counts).reduce((a,b)=>a+b,0)===144,'partition');
for(const x of states){
 t(['REJECT','DEFER_UNKNOWN','REVIEWABLE_SOURCE_CLAIM'].includes(x.decision),'known state');
 if(x.decision==='REVIEWABLE_SOURCE_CLAIM')t(x.signatureVerified&&x.accountBound&&x.nonceUnused&&x.keyEpoch==='CURRENT'&&x.revocation==='GOOD'&&x.freshness==='FRESH','reviewable');
 if(x.revocation==='REVOKED')t(x.decision==='REJECT','revoked');
 if(x.keyEpoch==='REVOKED')t(x.decision==='REJECT','old key');
 if(x.freshness==='STALE'&&x.signatureVerified&&x.accountBound&&x.nonceUnused&&x.keyEpoch==='CURRENT'&&x.revocation==='GOOD')t(x.decision==='DEFER_UNKNOWN','stale');
}
t(decide({keyEpoch:'CURRENT',revocation:'GOOD',freshness:'STALE',signatureVerified:true,accountBound:true,nonceUnused:true})==='DEFER_UNKNOWN','stale good');
t(decide({keyEpoch:'REVOKED',revocation:'GOOD',freshness:'FRESH',signatureVerified:true,accountBound:true,nonceUnused:true})==='REJECT','rotated key');
t(decide({keyEpoch:'UNKNOWN',revocation:'GOOD',freshness:'FRESH',signatureVerified:true,accountBound:true,nonceUnused:true})==='DEFER_UNKNOWN','offline unknown');
t(decide({keyEpoch:'CURRENT',revocation:'REVOKED',freshness:'FRESH',signatureVerified:true,accountBound:true,nonceUnused:true})==='REJECT','revoked status');
t(decide({keyEpoch:'CURRENT',revocation:'GOOD',freshness:'FRESH',signatureVerified:true,accountBound:true,nonceUnused:true})==='REVIEWABLE_SOURCE_CLAIM','valid');
console.log(JSON.stringify({status:'PASS',artificial:true,states:states.length,counts,assertions,actual_signatures_verified:0,actual_online_revocation_queries:0,actual_user_data:0}));
