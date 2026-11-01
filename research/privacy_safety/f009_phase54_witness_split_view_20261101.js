#!/usr/bin/env node
"use strict";
// Artificial witness checkpoints only. No real signature or cryptographic validation.
const assert = require("node:assert/strict");
const values = ["A", "B", "MISSING"];
function classify(witnesses) {
  const present = [...new Set(witnesses.filter(v => v !== "MISSING"))];
  if (present.length > 1) return "CONFLICT_QUARANTINE";
  if (present.length === 1 && witnesses.filter(v => v === present[0]).length >= 2) return "REVIEW_ONLY";
  return "UNKNOWN_QUARANTINE";
}
function main() {
  const counts = {REVIEW_ONLY: 0, CONFLICT_QUARANTINE: 0, UNKNOWN_QUARANTINE: 0};
  let cases = 0;
  for (const a of values) for (const b of values) for (const c of values) {
    counts[classify([a,b,c])]++;
    cases++;
  }
  assert.equal(cases, 27);
  assert.deepEqual(counts, {REVIEW_ONLY: 8, CONFLICT_QUARANTINE: 12, UNKNOWN_QUARANTINE: 7});
  assert.equal(classify(["A","A","B"]), "CONFLICT_QUARANTINE");
  assert.equal(classify(["A","A","MISSING"]), "REVIEW_ONLY");
  assert.equal(classify(["A","MISSING","MISSING"]), "UNKNOWN_QUARANTINE");
  assert.equal(classify(["MISSING","MISSING","MISSING"]), "UNKNOWN_QUARANTINE");
  console.log(JSON.stringify({status:"PASS", cases, counts, assertions:6, scope:"synthetic only; no signatures"}));
}
if (require.main === module) main();
module.exports = {classify, main};
