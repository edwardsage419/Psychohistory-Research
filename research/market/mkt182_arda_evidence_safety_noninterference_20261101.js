#!/usr/bin/env node
'use strict';
// Synthetic contract study. This does not implement or test ARDA software.
const assert = require('node:assert/strict');
const bits = [false, true];
function candidateGate(x) {
  let ratingState, confidence;
  if (x.correctionAccepted && !x.acceptedEvidence) {
    ratingState = 'RECONCILE_ORPHAN_CORRECTION'; confidence = 'UNKNOWN';
  } else if (!x.acceptedEvidence) {
    ratingState = 'UNASSESSABLE'; confidence = 'UNKNOWN';
  } else if (x.correctionAccepted) {
    ratingState = 'REASSESS_FROM_CORRECTED_ACCEPTED_EVIDENCE';
    confidence = x.missingRelevantEvidence ? 'REDUCED' : 'SOURCE_REVIEW_REQUIRED';
  } else {
    ratingState = 'ASSESS_FROM_ACCEPTED_EVIDENCE';
    confidence = x.missingRelevantEvidence ? 'REDUCED' : 'AVAILABLE';
  }
  return {ratingState,confidence,safetyRoute:x.safetySignal?'SEPARATE_SAFETY_REVIEW':'NONE'};
}
function naiveProxy(x) {
  // Deliberately defective toy proxy, not an ARDA score.
  return Number(x.acceptedEvidence)+Number(x.unacceptedAiProposal)
    -Number(x.safetySignal)-Number(x.missingRelevantEvidence)+Number(x.correctionAccepted);
}
const cases=[];
for(const acceptedEvidence of bits) for(const unacceptedAiProposal of bits)
for(const correctionAccepted of bits) for(const safetySignal of bits)
for(const missingRelevantEvidence of bits) {
  const x={acceptedEvidence,unacceptedAiProposal,correctionAccepted,safetySignal,missingRelevantEvidence};
  const result=candidateGate(x);
  const flippedSafety=candidateGate({...x,safetySignal:!safetySignal});
  const flippedAi=candidateGate({...x,unacceptedAiProposal:!unacceptedAiProposal});
  assert.equal(result.ratingState,flippedSafety.ratingState);
  assert.equal(result.confidence,flippedSafety.confidence);
  assert.equal(result.ratingState,flippedAi.ratingState);
  assert.equal(result.confidence,flippedAi.confidence);
  if(correctionAccepted&&!acceptedEvidence) assert.equal(result.ratingState,'RECONCILE_ORPHAN_CORRECTION');
  if(!acceptedEvidence&&!correctionAccepted) assert.equal(result.ratingState,'UNASSESSABLE');
  if(acceptedEvidence&&missingRelevantEvidence) assert.equal(result.confidence,'REDUCED');
  if(acceptedEvidence&&correctionAccepted) assert.equal(result.ratingState,'REASSESS_FROM_CORRECTED_ACCEPTED_EVIDENCE');
  cases.push({x,result,naiveProxy:naiveProxy(x)});
}
assert.equal(cases.length,32);
const counts={};
for(const c of cases) counts[c.result.ratingState]=(counts[c.result.ratingState]||0)+1;
const naiveContamination=cases.filter(({x})=>naiveProxy(x)!==naiveProxy({...x,unacceptedAiProposal:false,safetySignal:false})).length;
assert.equal(naiveContamination,16);
console.log(JSON.stringify({kind:'SYNTHETIC_E1_NONBLIND',cases:cases.length,ratingStates:counts,
  safetyFlipInvarianceChecks:cases.length,unacceptedAiFlipInvarianceChecks:cases.length,
  naiveProxyContaminatedStates:naiveContamination,
  claimsExcluded:['ARDA_INTERNAL_IMPLEMENTATION','REAL_WORLD_RATING_VALIDITY','PERSONAL_VALUE_WEIGHTS','PRODUCT_SECURITY_TEST']},null,2));
