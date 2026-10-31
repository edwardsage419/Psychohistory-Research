#!/usr/bin/env node
'use strict';
// MKT178: hypothetical event-time and ingest-time replay; no Beeminder API use.
const assert = require('node:assert/strict');
const threshold = 3;
const initial = [
  {id:'a', eventDay:1, receivedDay:1, amount:1},
  {id:'b', eventDay:2, receivedDay:2, amount:1},
  {id:'c', eventDay:3, receivedDay:3, amount:1}
];
function total(records, deadline, key='eventDay') {
  const seen = new Set();
  let sum = 0;
  for (const r of records) {
    if (seen.has(r.id)) throw new Error('duplicate id '+r.id);
    seen.add(r.id);
    if (r[key] <= deadline) sum += r.amount;
  }
  return sum;
}
function applyCorrection(records, correction) {
  if (!records.some(r=>r.id===correction.id)) throw new Error('unknown id');
  return records.map(r=>r.id===correction.id ? {...r,amount:correction.amount,receivedDay:correction.receivedDay} : {...r});
}
function snapshot(records) {return records.map(r=>({...r}));}
function state(value) {return value >= threshold ? 'SAFE' : 'BELOW';}
const original = total(initial,3);
const corrected = applyCorrection(initial,{id:'b',amount:0,receivedDay:4});
const eventTime = total(corrected,3,'eventDay');
// An event-day 2 correction arrives at day 4. A receipt-time view misses it at day 3.
assert.equal(original,3);
assert.equal(eventTime,2);
// The actual naive error is retaining the old immutable snapshot after the correction.
const staleSnapshot = snapshot(initial);
assert.equal(total(staleSnapshot,3),3);
assert.equal(state(total(staleSnapshot,3)),'SAFE');
assert.equal(state(eventTime),'BELOW');
// A silently lost webhook datapoint causes a mirror to disagree with a source export.
const droppedWebhook = initial.filter(r=>r.id!=='c');
assert.equal(total(droppedWebhook,3),2);
assert.equal(total(initial,3),3);
// Duplicate webhook delivery can cause a false safe result without ID deduplication.
const underGoal = initial.filter(r=>r.id!=='c');
const duplicated = [...underGoal, {...underGoal[1]}];
const naiveDuplicateTotal = duplicated.reduce((s,r)=>s+r.amount,0);
assert.equal(naiveDuplicateTotal,3);
assert.throws(()=>total(duplicated,3),/duplicate id/);
const deduplicated = [...new Map(duplicated.map(r=>[r.id,r])).values()];
assert.equal(total(deduplicated,3),2);
// Source snapshot reconciliation fixes the missing-event mirror without charging anyone.
const reconciled = snapshot(initial);
assert.deepEqual(reconciled,initial);
assert.equal(total(reconciled,3),3);
assert.throws(()=>applyCorrection(initial,{id:'missing',amount:0,receivedDay:4}),/unknown id/);
const report={scope:'SYNTHETIC_E1_NOT_BEEMINDER_EXECUTION',deadlineDay:3,threshold,
  original:{total:original,state:state(original)},
  retroactiveCorrection:{eventDay:2,receivedDay:4,correctedTotal:eventTime,correctedState:state(eventTime),staleSnapshotTotal:total(staleSnapshot,3),staleState:state(total(staleSnapshot,3))},
  silentWebhookLoss:{mirrorTotal:total(droppedWebhook,3),sourceTotal:total(initial,3)},
  duplicateWebhook:{naiveTotal:naiveDuplicateTotal,deduplicatedTotal:total(deduplicated,3)},
  reconciliation:{sourceTotal:total(reconciled,3)},
  checks:'PASS',real_product_api_calls:0,charges:0};
console.log(JSON.stringify(report,null,2));
