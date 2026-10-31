#!/usr/bin/env node
// Free standard-library synthetic or nonblind archival audit.
function audit(inputs){
"use strict";
function run(){
 const outcomes={NO_BACKUP:0,REPLAY_ERASURE_REVIEW:0,UNKNOWN_QUARANTINE:0};
 let cases=0,automatic=0;
 for(let mask=0;mask<32;mask++){
  const stale=!!(mask&1),rotated=!!(mask&2),tombstone=!!(mask&4),mapping=!!(mask&8),anchor=!!(mask&16);
  let status="NO_BACKUP";
  if(stale)status=tombstone&&(!rotated||mapping)&&anchor?"REPLAY_ERASURE_REVIEW":"UNKNOWN_QUARANTINE";
  outcomes[status]++;cases++;
  if(status==="AUTO_RESTORE")automatic++;
  if(stale&&rotated&&tombstone&&!mapping&&status!=="UNKNOWN_QUARANTINE")throw Error("lost identity mapping");
  if(stale&&tombstone&&!anchor&&status!=="UNKNOWN_QUARANTINE")throw Error("missing anchor");
 }
 const oldId="deviceA/caseX",newId="deviceB/caseX";
 const tombstones=new Set([oldId]);
 const naiveRestoreAllowed=!tombstones.has(newId);
 if(!naiveRestoreAllowed)throw Error("negative control must demonstrate stale restoration");
 const bridge=new Map([[newId,oldId]]);
 const guardedRestoreAllowed=!tombstones.has(bridge.get(newId));
 if(guardedRestoreAllowed)throw Error("bridge guard failed");
 const indistinguishable={visibleActive:[],visibleTombstones:[],staleBackup:[newId],mapping:null,hiddenHistories:["never_erased","erased_before_rotation"]};
 if(indistinguishable.hiddenHistories.length!==2)throw Error("indistinguishable history");
 if(cases!==32||automatic!==0||outcomes.NO_BACKUP!==16)throw Error("matrix");
 return {status:"PASS",cases,outcomes,automatic,naiveRestoreAllowed,guardedRestoreAllowed,indistinguishable,scope:"SYNTHETIC_E1_ONLY"};
}
return run();
}
const inputs={};
console.log(JSON.stringify(audit(inputs),null,2));
