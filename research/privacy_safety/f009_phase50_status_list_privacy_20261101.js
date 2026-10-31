"use strict";
// Synthetic status-policy checks inspired by W3C Bitstring Status List v1.0.
// No VC signature verification, production issuer, real account or personal data.
function statusDecision(s) {
  if (!s.request) return "NO_REQUEST";
  if (!s.issuerTrusted || !s.proofVerified || !s.accountBound) return "UNKNOWN_QUARANTINE";
  if (!s.statusAvailable || !s.fresh) return "UNKNOWN_QUARANTINE";
  if (s.revoked || !s.deletionSafe) return "REJECT";
  return "REVIEW_ONLY"; // never automatic restoration
}
function privacyDiagnostics(s) {
  return {
    advertisedSlots:s.slots,
    activeIssued:s.issued,
    anonymityUpperBound:Math.min(s.slots,s.issued),
    indexCrossVerifierLinkable:s.sameIndexExposedToTwoVerifiers,
    issuerAccessTrackingRisk:s.issuerSeesFetches,
    warning:s.issued<100?"SMALL_REAL_COHORT":"REVIEW_POPULATION"
  };
}
function runTests() {
  const base={request:true,issuerTrusted:true,proofVerified:true,accountBound:true,statusAvailable:true,fresh:true,revoked:false,deletionSafe:true};
  const cases=[
    ["clean_requires_review",base,"REVIEW_ONLY"],
    ["stale_quarantine",{...base,fresh:false},"UNKNOWN_QUARANTINE"],
    ["unavailable_quarantine",{...base,statusAvailable:false},"UNKNOWN_QUARANTINE"],
    ["revoked_reject",{...base,revoked:true},"REJECT"],
    ["issuer_unknown",{...base,issuerTrusted:false},"UNKNOWN_QUARANTINE"],
    ["wrong_account",{...base,accountBound:false},"UNKNOWN_QUARANTINE"],
    ["deleted_reject",{...base,deletionSafe:false},"REJECT"],
    ["no_request",{...base,request:false},"NO_REQUEST"]
  ];
  for(const [name,s,expected] of cases)if(statusDecision(s)!==expected)throw Error("FAIL "+name);
  const small=privacyDiagnostics({slots:131072,issued:1,sameIndexExposedToTwoVerifiers:true,issuerSeesFetches:true});
  if(small.anonymityUpperBound!==1||!small.indexCrossVerifierLinkable||small.warning!=="SMALL_REAL_COHORT")throw Error("FAIL privacy");
  return {assertions:cases.length+3,smallPopulation:small,clean:statusDecision(base)};
}
if(typeof module!=="undefined")module.exports={statusDecision,privacyDiagnostics,runTests};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(runTests()));
