"use strict";
// F009 phase 5: candidate metadata and resurrection guard, artificial E1.
// No real identities, signatures, encryption, erasure, or network operations.
const assert=(p,m)=>{if(!p)throw Error("assertion: "+m);};
function evaluate(r,now,incoming=null){
 if(!r||!Number.isInteger(now)||now<0)throw Error("invalid clock or receipt");
 for(const k of ["delete_epoch","receipt_expires_at"])
   if(!Number.isInteger(r[k])||r[k]<0)throw Error("invalid "+k);
 if(typeof r.opaque_case_id!=="string"||!r.opaque_case_id||r.opaque_case_id.length>64)
   throw Error("opaque case token");
 if(r.receipt_expires_at<r.delete_epoch)throw Error("invalid retention horizon");
 const devices=["phone","laptop","tablet"];
 if(!r.device_receipts||typeof r.device_receipts!=="object")throw Error("device inventory");
 if(!Number.isInteger(r.backup_references)||r.backup_references<0)throw Error("backup count");
 if(!Number.isInteger(r.unknown_replicas)||r.unknown_replicas<0)throw Error("replica count");
 const missing=devices.filter(d=>!r.device_receipts[d]||
   r.device_receipts[d].verified!==true||
   !Number.isInteger(r.device_receipts[d].epoch)||
   r.device_receipts[d].epoch<r.delete_epoch);
 let status="MODEL_SCOPE_COMPLETE";
 if(now>r.receipt_expires_at)status="UNKNOWN_EXPIRED_RECEIPT";
 else if(r.unknown_replicas>0)status="UNKNOWN_REPLICA";
 else if(missing.length)status="PENDING_DEVICE";
 else if(r.legal_hold===true)status="PENDING_LEGAL_HOLD";
 else if(r.archive_cleared!==true)status="PENDING_ARCHIVE";
 else if(r.backup_references>0)status="PENDING_BACKUP";
 else if(r.prune_verified!==true)status="PENDING_PRUNE";
 let receive="NO_INCOMING";
 if(incoming!==null){
   if(!Number.isInteger(incoming.content_epoch)||incoming.content_epoch<0)throw Error("content epoch");
   if(status==="UNKNOWN_EXPIRED_RECEIPT")receive="QUARANTINE_EXPIRED_AUDIT";
   else if(incoming.content_epoch<=r.delete_epoch)receive="REJECT_STALE_OR_REVOKED";
   else if(incoming.verified_new_grant!==true)receive="QUARANTINE_UNVERIFIED_GRANT";
   else receive="CANDIDATE_REAUTHORIZED_NEEDS_REAL_CRYPTO_CHECK";
 }
 return {status,receive,missing_devices:missing.length,
   privacy_scope:"SYNTHETIC_METADATA_ONLY_NO_ERASURE_PROOF"};
}
function run(){
 const base={opaque_case_id:"random-case-token",delete_epoch:7,receipt_expires_at:30,
   device_receipts:{phone:{epoch:7,verified:true},laptop:{epoch:7,verified:true},
     tablet:{epoch:7,verified:true}},unknown_replicas:0,archive_cleared:true,
   backup_references:0,prune_verified:true,legal_hold:false};
 const clone=()=>JSON.parse(JSON.stringify(base));
 let tests=0;const check=(v,m)=>{tests++;assert(v,m);};
 check(evaluate(clone(),20).status==="MODEL_SCOPE_COMPLETE","complete scope");
 const off=clone();off.device_receipts.tablet.epoch=5;
 check(evaluate(off,20).status==="PENDING_DEVICE","offline device");
 check(evaluate(off,20,{content_epoch:5}).receive==="REJECT_STALE_OR_REVOKED","stale reject");
 check(evaluate(off,31,{content_epoch:5}).receive==="QUARANTINE_EXPIRED_AUDIT","expired tombstone");
 const unknown=clone();unknown.unknown_replicas=1;
 check(evaluate(unknown,20).status==="UNKNOWN_REPLICA","unknown replica");
 const backup=clone();backup.backup_references=1;
 check(evaluate(backup,20).status==="PENDING_BACKUP","shared backup");
 const archive=clone();archive.archive_cleared=false;
 check(evaluate(archive,20).status==="PENDING_ARCHIVE","archive");
 const hold=clone();hold.legal_hold=true;
 check(evaluate(hold,20).status==="PENDING_LEGAL_HOLD","legal hold");
 const prune=clone();prune.prune_verified=false;
 check(evaluate(prune,20).status==="PENDING_PRUNE","prune");
 check(evaluate(clone(),20,{content_epoch:8}).receive==="QUARANTINE_UNVERIFIED_GRANT","no regrant");
 check(evaluate(clone(),20,{content_epoch:8,verified_new_grant:true}).receive==="CANDIDATE_REAUTHORIZED_NEEDS_REAL_CRYPTO_CHECK","candidate regrant");
 const bad=[
   ()=>evaluate({...clone(),backup_references:-1},20),
   ()=>evaluate({...clone(),delete_epoch:-1},20),
   ()=>evaluate({...clone(),opaque_case_id:""},20),
   ()=>evaluate({...clone(),receipt_expires_at:6},20),
   ()=>evaluate(clone(),20,{content_epoch:-1})
 ];
 let rejected=0;for(const f of bad){try{f();}catch(e){rejected++;}}
 check(rejected===5,"invalid rejects");
 return {status:"PASS",tests,invalid_rejected:rejected,
   examples:{complete:evaluate(clone(),20),offline:evaluate(off,20,{content_epoch:5}),
     expired:evaluate(off,31,{content_epoch:5}),
     regrant:evaluate(clone(),20,{content_epoch:8})},
   evidence:"ARTIFICIAL_E1_NONBLIND",E2:0,E3:0};
}
if(typeof module!=="undefined")module.exports={run,evaluate};
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(run(),null,2));
