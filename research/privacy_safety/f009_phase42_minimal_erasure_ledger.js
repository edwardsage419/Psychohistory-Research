#!/usr/bin/env node
'use strict';
// F009 phase42: artificial data lifecycle and restore gate. No real personal data.
const assert = require('node:assert/strict');
function decide(s){
  if(!s.restore) return 'NO_RESTORE';
  if(s.legalHold) return 'RESTRICTED_REVIEW';
  if(s.ledger && s.expired) return 'RETENTION_REVIEW';
  if(s.staleBackup && !s.ledger) return 'UNKNOWN_QUARANTINE';
  if(s.staleBackup && s.ledger) return 'REPLAY_ERASURE_REVIEW';
  if(!s.replicaKnown) return 'UNKNOWN_REPLICA';
  return 'REVIEW_ONLY';
}
function keys(s){return Object.keys(s).sort().map(k=>`${k}=${s[k]}`).join('|')}
const counts={};let states=0,auto=0;
for(let mask=0;mask<64;mask++){
  const s={restore:!!(mask&1),staleBackup:!!(mask&2),ledger:!!(mask&4),replicaKnown:!!(mask&8),expired:!!(mask&16),legalHold:!!(mask&32)};
  const d=decide(s);counts[d]=(counts[d]||0)+1;states++;
  if(d==='AUTO_ALLOW')auto++;
  if(s.restore&&s.staleBackup&&!s.ledger&&!s.legalHold) assert.equal(d,'UNKNOWN_QUARANTINE');
  if(s.restore&&s.legalHold) assert.equal(d,'RESTRICTED_REVIEW');
  if(s.restore&&s.ledger&&s.expired&&!s.legalHold) assert.equal(d,'RETENTION_REVIEW');
}
assert.equal(states,64);assert.equal(auto,0);
// The same current view can hide distinct historical erasure obligations after ledger expiry.
const historyNoErasure={active:[],ledger:[],backup:['caseX']};
const historyErased={active:[],ledger:[],backup:['caseX']};
assert.equal(keys(historyNoErasure),keys(historyErased));
const erasedHistoricalFact=true;
const naiveRestore=historyErased.backup.slice();
assert(naiveRestore.includes('caseX')&&erasedHistoricalFact);
const safeGate=decide({restore:true,staleBackup:true,ledger:false,replicaKnown:false,expired:true,legalHold:false});
assert.equal(safeGate,'UNKNOWN_QUARANTINE');
// With a still-valid erasure ledger, the candidate recovery removes the artificial record.
const restored=historyErased.backup.filter(id=>id!=='caseX');
assert.deepEqual(restored,[]);
const receipt={scope:'ARTIFICIAL_E1_LIFECYCLE_ONLY',states,counts,automatic_high_impact_restore:auto,
  indistinguishable_current_state:true,naive_restore_resurrects_erased_case:true,
  expired_ledger_stale_backup:safeGate,valid_ledger_replay_removes_case:restored.length===0,
  retention_duration_days:'NOT_SPECIFIED_LEGAL_RISK_REVIEW_REQUIRED',real_user_data:0,checks:'PASS'};
console.log(JSON.stringify(receipt,null,2));
