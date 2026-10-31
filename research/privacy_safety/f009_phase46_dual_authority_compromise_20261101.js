#!/usr/bin/env node
'use strict';
// Artificial recovery-state audit only; no actual account, device or cryptography.
const assert=require('node:assert/strict');
const fields=['staleBackup','deletionProof','aliasProof','primaryNoticeCompromised',
  'independentSecondaryNotice','approvalAuthorityCompromised','independentHumanReview',
  'oldCredentialRevoked','freshTransaction','independentEvidenceAnchor'];
function candidatePolicy(x){
  if(!x.staleBackup) return 'NO_RESTORE_NEEDED';
  if(!x.deletionProof||!x.aliasProof||!x.oldCredentialRevoked||!x.freshTransaction) return 'UNKNOWN_QUARANTINE';
  if(x.approvalAuthorityCompromised&&!x.independentHumanReview) return 'REJECT_COMPROMISED_APPROVAL';
  if(x.primaryNoticeCompromised&&!x.independentSecondaryNotice) return 'UNKNOWN_QUARANTINE';
  if(x.primaryNoticeCompromised&&x.approvalAuthorityCompromised&&!x.independentEvidenceAnchor) return 'UNKNOWN_QUARANTINE';
  if(!x.independentHumanReview) return 'REJECT_MISSING_REVIEW';
  return 'REVIEW_ONLY';
}
function naivePolicy(x){
  // Intentionally weak: assumes compromised primary notice and approval are genuine.
  return x.staleBackup&&x.deletionProof&&x.aliasProof&&x.oldCredentialRevoked&&x.freshTransaction;
}
const counts={},cases=[];
for(let mask=0;mask<(1<<fields.length);mask++){
  const x=Object.fromEntries(fields.map((f,i)=>[f,Boolean(mask&(1<<i))]));
  const result=candidatePolicy(x);
  counts[result]=(counts[result]||0)+1;
  assert.notEqual(result,'AUTO_RESTORE');
  if(result==='REVIEW_ONLY'){
    assert(x.staleBackup&&x.deletionProof&&x.aliasProof&&x.oldCredentialRevoked&&x.freshTransaction);
    assert(x.independentHumanReview);
    assert(!x.primaryNoticeCompromised||x.independentSecondaryNotice);
    assert(!(x.primaryNoticeCompromised&&x.approvalAuthorityCompromised)||x.independentEvidenceAnchor);
  }
  cases.push({x,result,naive:naivePolicy(x)});
}
assert.equal(cases.length,1024);
const bothCompromised=cases.filter(c=>c.x.staleBackup&&c.x.primaryNoticeCompromised&&c.x.approvalAuthorityCompromised);
const naiveAcceptedDual=bothCompromised.filter(c=>c.naive).length;
const candidateDualReview=bothCompromised.filter(c=>c.result==='REVIEW_ONLY').length;
assert(bothCompromised.filter(c=>!c.x.independentHumanReview).every(c=>c.result!=='REVIEW_ONLY'));
assert(naiveAcceptedDual>candidateDualReview);
const dual=Object.fromEntries(fields.map(f=>[f,true]));
assert.equal(candidatePolicy(dual),'REVIEW_ONLY');
assert.equal(candidatePolicy({...dual,independentEvidenceAnchor:false}),'UNKNOWN_QUARANTINE');
assert.equal(candidatePolicy({...dual,independentSecondaryNotice:false}),'UNKNOWN_QUARANTINE');
assert.equal(candidatePolicy({...dual,independentHumanReview:false}),'REJECT_COMPROMISED_APPROVAL');
console.log(JSON.stringify({kind:'SYNTHETIC_E1_NONBLIND',states:cases.length,policyCounts:counts,
  dualCompromisedStaleStates:bothCompromised.length,naiveAcceptedDualCompromise:naiveAcceptedDual,
  candidateDualCompromiseReviewOnly:candidateDualReview,automaticHighImpactRestore:0,targetedControlsPassed:4,
  independentReviewerCompromise:'OUT_OF_SCOPE',
  claimsExcluded:['REAL_AUTHENTICATION','CRYPTOGRAPHIC_SECURITY','NIST_MANDATED_RESTORE_POLICY','ACTUAL_INCIDENT_RATE']},null,2));
