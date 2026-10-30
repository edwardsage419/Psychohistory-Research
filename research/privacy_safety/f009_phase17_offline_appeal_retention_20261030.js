#!/usr/bin/env node
'use strict';
// Candidate offline appeal triage, synthetic states only. Not a standards compliance test.
const assert=require('node:assert/strict');
const keys=['signatureValid','accountBound','retentionExpired','legalHold','revocationFresh','appealOpen','reviewChannel'];
function decide(s){
  if(!s.signatureValid||!s.accountBound)return 'REJECT_SOURCE';
  if(s.retentionExpired&&!s.legalHold)return 'PURGE_LIMITED';
  if(!s.revocationFresh)return 'DEFER_REFRESH';
  if(s.appealOpen)return s.reviewChannel?'HUMAN_REVIEW':'DEFER_REVIEW';
  return 'REVIEWABLE_ONLY';
}
const allowedReceiptKeys=['event_ref','status','purpose_code','review_due_day','retention_basis_code'];
function minimalReceipt(input){
  const out={};for(const k of allowedReceiptKeys)if(Object.hasOwn(input,k))out[k]=input[k];
  return out;
}
const counts={},examples={};let checks=0;
for(let mask=0;mask<128;mask++){
  const s=Object.fromEntries(keys.map((k,i)=>[k,Boolean(mask&(1<<i))]));
  const result=decide(s);counts[result]=(counts[result]||0)+1;
  if(!(result in examples))examples[result]=s;
  assert.ok(['REJECT_SOURCE','PURGE_LIMITED','DEFER_REFRESH','HUMAN_REVIEW','DEFER_REVIEW','REVIEWABLE_ONLY'].includes(result));checks++;
  if(!s.signatureValid||!s.accountBound){assert.equal(result,'REJECT_SOURCE');checks++;}
  if(s.signatureValid&&s.accountBound&&s.retentionExpired&&!s.legalHold){assert.equal(result,'PURGE_LIMITED');checks++;}
  if(result==='HUMAN_REVIEW'){assert.ok(s.appealOpen&&s.reviewChannel&&s.revocationFresh);checks++;}
}
assert.equal(Object.values(counts).reduce((a,b)=>a+b,0),128);checks++;
assert.deepEqual(counts,{REJECT_SOURCE:96,PURGE_LIMITED:8,DEFER_REFRESH:12,DEFER_REVIEW:3,HUMAN_REVIEW:3,REVIEWABLE_ONLY:6});checks++;
const receipt=minimalReceipt({event_ref:'synthetic-01',status:'DEFER_REFRESH',purpose_code:'appeal',review_due_day:7,retention_basis_code:'none',email:'private@example.test',access_token:'secret',health:'sensitive'});
assert.deepEqual(Object.keys(receipt).sort(),allowedReceiptKeys.slice().sort());checks++;
assert.ok(!JSON.stringify(receipt).includes('private@example.test'));checks++;
assert.ok(!JSON.stringify(receipt).includes('secret'));checks++;
assert.equal(decide({signatureValid:true,accountBound:true,retentionExpired:false,legalHold:false,revocationFresh:false,appealOpen:true,reviewChannel:true}),'DEFER_REFRESH');checks++;
assert.equal(decide({signatureValid:true,accountBound:true,retentionExpired:false,legalHold:false,revocationFresh:true,appealOpen:true,reviewChannel:false}),'DEFER_REVIEW');checks++;
const output={research:'F009_PHASE17',evidence:'INTERNAL_NONBLIND_ARTIFICIAL_E1',states:128,counts,assertions_passed:checks,receipt_keys:Object.keys(receipt)};
if(require.main===module)console.log(JSON.stringify(output,null,2));
module.exports={decide,minimalReceipt,output};
