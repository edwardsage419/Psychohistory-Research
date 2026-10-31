#!/usr/bin/env node
'use strict';
const assert = require('node:assert/strict');
const FIELDS = [
  'request', 'codePresent', 'codeUnspent', 'anchorAuthentic',
  'anchorBound', 'revocationFresh', 'logConsistent',
  'independentReview', 'deletionSafe',
];
function classify(s) {
  if (!s.request) return 'NO_REQUEST';
  if (!s.codePresent || !s.codeUnspent) return 'REJECT';
  if (!s.anchorAuthentic || !s.anchorBound) return 'REJECT';
  if (!s.revocationFresh || !s.logConsistent) return 'UNKNOWN_QUARANTINE';
  if (!s.independentReview || !s.deletionSafe) return 'REJECT';
  return 'REVIEW_ONLY';
}
function weak(s) {
  return s.request && s.codePresent && s.anchorAuthentic && s.independentReview && s.deletionSafe
    ? 'REVIEW_ONLY' : 'NO_APPROVAL';
}
const good = Object.fromEntries(FIELDS.map(k => [k, true]));
const cases = [
  [good, 'REVIEW_ONLY'],
  [{...good, request:false}, 'NO_REQUEST'],
  [{...good, codePresent:false}, 'REJECT'],
  [{...good, codeUnspent:false}, 'REJECT'],
  [{...good, anchorAuthentic:false}, 'REJECT'],
  [{...good, anchorBound:false}, 'REJECT'],
  [{...good, revocationFresh:false}, 'UNKNOWN_QUARANTINE'],
  [{...good, logConsistent:false}, 'UNKNOWN_QUARANTINE'],
  [{...good, independentReview:false}, 'REJECT'],
  [{...good, deletionSafe:false}, 'REJECT'],
];
for (const [input, expected] of cases) assert.equal(classify(input), expected);
const totals = {}, weakTotals = {};
let weakFalseReview = 0;
for (let mask=0; mask<(1<<FIELDS.length); mask++) {
  const state = Object.fromEntries(FIELDS.map((k,i) => [k, Boolean(mask & (1<<i))]));
  const decision=classify(state), weakDecision=weak(state);
  totals[decision]=(totals[decision]||0)+1;
  weakTotals[weakDecision]=(weakTotals[weakDecision]||0)+1;
  if (weakDecision==='REVIEW_ONLY' && decision!=='REVIEW_ONLY') weakFalseReview++;
}
assert.equal(Object.values(totals).reduce((a,b)=>a+b,0), 512);
assert.equal(totals.REVIEW_ONLY, 1);
assert.equal(weakTotals.REVIEW_ONLY, 16);
assert.equal(weakFalseReview, 15);
console.log(JSON.stringify({source:'NIST SP 800-63B-4 and RFC 9162 analogies; policy is project-only', evidence:'synthetic E1', states:512, directed_assertions:cases.length, totals, weakTotals, weakFalseReview, automaticRestore:0},null,2));
