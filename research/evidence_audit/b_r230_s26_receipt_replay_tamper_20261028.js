#!/usr/bin/env node
'use strict';
// Replays the exact R230 S26 receipt from pinned original sources using Node standard library.
// R enumeration and B histogram/multinomial routes are implemented separately inside the invoked research script.
// Usage: node research/evidence_audit/b_r230_s26_receipt_replay_tamper_20261028.js
const fs=require('fs'),path=require('path'),assert=require('assert'),cp=require('child_process');
const root=path.resolve(__dirname,'../..');
const script=path.join(root,'research/validation/r230_s26_finite_sample_exact_20261028.js');
const receiptPath=path.join(root,'research/validation/R230_S26_FINITE_SAMPLE_EXACT_RECEIPT_2026-10-28.json');
const computed=JSON.parse(cp.execFileSync(process.execPath,[script],{encoding:'utf8',maxBuffer:8*1024*1024}));
const archived=JSON.parse(fs.readFileSync(receiptPath,'utf8'));
assert.deepStrictEqual(computed,archived,'source first exact replay differs from archived receipt');
assert.strictEqual(computed.checks_passed,557);
assert.strictEqual(computed.ordered_source_sequences,270336);
const bad=JSON.parse(JSON.stringify(archived));
bad.results.NO_COMMON_FACTOR.n2.offdiag_sign_counts[0][0]+=1;
assert.notDeepStrictEqual(computed,bad,'deliberate tamper unexpectedly accepted');
assert.strictEqual(bad.results.NO_COMMON_FACTOR.n2.offdiag_sign_counts[0].reduce((a,b)=>a+b,0),1025);
console.log(JSON.stringify({source_replay:'PASS',archive_match:'PASS',checks_passed:557,deliberate_sign_count_tamper:'DETECTED',external_replication:false}));
