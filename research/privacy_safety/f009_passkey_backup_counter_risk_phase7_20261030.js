'use strict';
// Candidate risk classification from WebAuthn/NIST docs, artificial inputs only.
// signatureVerified is an externally supplied simulation flag, never a cryptographic verifier.
const assert = require('node:assert/strict');
function classify(x) {
  if (!x || ['be','bs','previousBe','previousBs','signatureVerified','revoked'].some(k=>typeof x[k]!=='boolean') ||
      ![x.previousCount,x.currentCount,x.boundEpoch,x.operationEpoch].every(v=>Number.isSafeInteger(v)&&v>=0)) throw Error('BAD_INPUT');
  if ((!x.be && x.bs) || (!x.previousBe && x.previousBs)) return {decision:'REJECT_INVALID_FLAGS',risk:['invalid_be_bs']};
  if (x.previousBe!==x.be) return {decision:'REVIEW_INCONSISTENT_BE',risk:['be_immutable']};
  if (!x.signatureVerified) return {decision:'BLOCK_UNVERIFIED',risk:['signature_not_verified']};
  if (x.revoked || x.operationEpoch<x.boundEpoch) return {decision:'BLOCK_REVOKED_OR_STALE',risk:['authorization_epoch']};
  const risk=[];
  if (x.previousBs && !x.bs) risk.push('backup_lost_recovery_review');
  if (x.previousCount>0 || x.currentCount>0) {
    if (x.currentCount<=x.previousCount) risk.push('counter_anomaly_not_clone_proof');
  } else risk.push('zero_counter_uninformative');
  if (x.be) risk.push('syncable_exportable_not_aal3');
  if (risk.some(x=>x==='backup_lost_recovery_review'||x==='counter_anomaly_not_clone_proof')) return {decision:'REVIEW',risk};
  return {decision:'CONDITIONAL_ACCEPT_ARTIFICIAL',risk};
}
const assertBase={be:true,bs:true,previousBe:true,previousBs:true,signatureVerified:true,revoked:false,previousCount:0,currentCount:0,boundEpoch:8,operationEpoch:8};
let checks=0;function eq(a,b){assert.deepEqual(a,b);checks++;}function rejects(f,code){assert.throws(f,e=>e.message===code);checks++;}
eq(classify(assertBase).decision,'CONDITIONAL_ACCEPT_ARTIFICIAL');
eq(classify(assertBase).risk.includes('zero_counter_uninformative'),true);
eq(classify(assertBase).risk.includes('syncable_exportable_not_aal3'),true);
eq(classify({...assertBase,previousBs:false,bs:true}).decision,'CONDITIONAL_ACCEPT_ARTIFICIAL');
eq(classify({...assertBase,previousBs:true,bs:false}).decision,'REVIEW');
eq(classify({...assertBase,previousCount:3,currentCount:3}).decision,'REVIEW');
eq(classify({...assertBase,previousCount:3,currentCount:2}).decision,'REVIEW');
eq(classify({...assertBase,previousCount:3,currentCount:4}).decision,'CONDITIONAL_ACCEPT_ARTIFICIAL');
eq(classify({...assertBase,be:false,bs:false,previousBe:false,previousBs:false,previousCount:3,currentCount:4}).risk.includes('syncable_exportable_not_aal3'),false);
eq(classify({...assertBase,be:false,bs:true}).decision,'REJECT_INVALID_FLAGS');
eq(classify({...assertBase,previousBe:false,previousBs:false}).decision,'REVIEW_INCONSISTENT_BE');
eq(classify({...assertBase,signatureVerified:false}).decision,'BLOCK_UNVERIFIED');
eq(classify({...assertBase,revoked:true}).decision,'BLOCK_REVOKED_OR_STALE');
eq(classify({...assertBase,operationEpoch:7}).decision,'BLOCK_REVOKED_OR_STALE');
rejects(()=>classify(null),'BAD_INPUT');
rejects(()=>classify({...assertBase,currentCount:-1}),'BAD_INPUT');
rejects(()=>classify({...assertBase,be:1}),'BAD_INPUT');
rejects(()=>classify({...assertBase,operationEpoch:1.5}),'BAD_INPUT');
console.log(JSON.stringify({study:'F009_PHASE7',checks,baseline:classify(assertBase),counterRegression:classify({...assertBase,previousCount:3,currentCount:2}),backupLoss:classify({...assertBase,bs:false}),scope:'ARTIFICIAL_E1_ONLY',node:process.version}));
module.exports={classify};
