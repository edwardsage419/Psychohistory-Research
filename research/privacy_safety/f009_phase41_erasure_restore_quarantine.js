#!/usr/bin/env node
'use strict';
// F009 phase41: synthetic deletion and backup-restore quarantine only.
// No real personal records or credentials; no claim of legal compliance.
function simulate({staleBackup,ledgerAvailable,derivedCopy,exceptionClaimed}){
  const primary=new Set(["caseA","caseB"]);
  primary.delete("caseA"); // confirmed user erasure request for synthetic caseA
  const restored=staleBackup?new Set(["caseA","caseB"]):new Set(["caseB"]);
  const derived=derivedCopy?new Set(["caseA"]):new Set();
  if(exceptionClaimed)return {status:"REVIEW_RESTRICTED",access:"QUARANTINED",remaining:restored.has("caseA")||derived.has("caseA")};
  if(!ledgerAvailable)return {status:"UNKNOWN_QUARANTINE",access:"QUARANTINED",remaining:restored.has("caseA")||derived.has("caseA")};
  // Tombstone is a synthetic opaque lookup key; actual retention requires legal review.
  restored.delete("caseA");derived.delete("caseA");
  if(restored.has("caseA")||derived.has("caseA"))throw Error("resurrection");
  return {status:"RECONCILED_REVIEW",access:"MANUAL_REVIEW_ONLY",remaining:false};
}
const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
const counts={};let n=0;
for(const staleBackup of [false,true])for(const ledgerAvailable of [false,true])
for(const derivedCopy of [false,true])for(const exceptionClaimed of [false,true]){
 const r=simulate({staleBackup,ledgerAvailable,derivedCopy,exceptionClaimed});
 n++;counts[r.status]=(counts[r.status]||0)+1;
 assert(!(r.status==='RECONCILED_REVIEW'&&r.remaining),'resurrection allowed');
 assert(r.status==='RECONCILED_REVIEW'||r.access==='QUARANTINED','unreviewed access');
}
const naiveRestore=new Set(['caseA','caseB']);
assert(naiveRestore.has('caseA'),'naive restore counterexample');
assert(n===16&&counts.RECONCILED_REVIEW===4&&counts.UNKNOWN_QUARANTINE===4&&counts.REVIEW_RESTRICTED===8,'state counts');
console.log(JSON.stringify({status:'PASS',synthetic_states:n,counts,naive_restore_resurrects:true,auto_decision_allowed:0,scope:'ARTIFICIAL_E1_ONLY'}));
