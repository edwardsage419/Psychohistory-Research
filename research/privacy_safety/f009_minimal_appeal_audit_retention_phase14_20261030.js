"use strict";
// F009 phase14 synthetic audit minimization and retention gate; no legal decision authority.
function check(x,m){if(!x)throw new Error(m)}
const keys=["event_class","status","created_day","expiry_day","purpose","evidence_ref"];
function validateReceipt(r){
 if(!r||typeof r!=="object"||Array.isArray(r))throw new Error("object");
 const actual=Object.keys(r).sort(),expected=keys.slice().sort();
 if(actual.length!==expected.length||actual.some((x,i)=>x!==expected[i]))throw new Error("extra or missing field");
 if(!["RECOVERY_APPEAL","RECOVERY_NOTICE"].includes(r.event_class))throw new Error("event");
 if(!["PENDING","RESOLVED","REJECTED"].includes(r.status))throw new Error("status");
 if(r.purpose!=="SECURITY_DISPUTE")throw new Error("purpose");
 if(!Number.isSafeInteger(r.created_day)||!Number.isSafeInteger(r.expiry_day)||
 r.created_day<0||r.expiry_day<r.created_day)throw new Error("time");
 if(typeof r.evidence_ref!=="string"||!/^[A-Z0-9_]{1,20}$/.test(r.evidence_ref))throw new Error("reference");
 return true;
}
function retention(s){
 const flags=["appeal_open","basis_verified","legal_hold_verified","deletion_requested","expired"];
 if(!s||flags.some(k=>typeof s[k]!=="boolean")||Object.keys(s).length!==flags.length)throw new Error("state");
 if(s.basis_verified&&(s.appeal_open||s.legal_hold_verified))return "REVIEW_HOLD";
 if(s.deletion_requested||s.expired)return "ERASE";
 return "RETAIN_WITH_REVIEW_DATE";
}
function deletionScope(expected,acks){
 if(!Number.isSafeInteger(expected)||expected<=0||!Number.isSafeInteger(acks)||acks<0||acks>expected)throw new Error("counts");
 return acks===expected?"ACKNOWLEDGED_WITHIN_DECLARED_SCOPE":"UNKNOWN";
}
function run(){
 let checks=0;const ok=(x,m)=>{check(x,m);checks++};
 const base={event_class:"RECOVERY_APPEAL",status:"PENDING",created_day:1,expiry_day:30,purpose:"SECURITY_DISPUTE",evidence_ref:"REF_01"};
 ok(validateReceipt(base),"minimal");
 const invalid=[{...base,email:"person@example.test"},{...base,token:"SECRET"},
 {...base,evidence_ref:"person@example.test"},{...base,expiry_day:0},
 {...base,status:"SENT"},{...base,created_day:1.5}];
 for(const bad of invalid){let rejected=false;try{validateReceipt(bad)}catch(e){rejected=true}ok(rejected,"invalid receipt")}
 const counts={REVIEW_HOLD:0,ERASE:0,RETAIN_WITH_REVIEW_DATE:0};
 for(let bits=0;bits<32;bits++){
  const s={appeal_open:!!(bits&1),basis_verified:!!(bits&2),
   legal_hold_verified:!!(bits&4),deletion_requested:!!(bits&8),expired:!!(bits&16)};
  const decision=retention(s);counts[decision]++;
  ok(!(decision==="REVIEW_HOLD"&&!s.basis_verified),"verified basis for hold");
  if(s.expired&&!s.basis_verified)ok(decision==="ERASE","expired without basis");
  if(s.deletion_requested&&!s.basis_verified)ok(decision==="ERASE","delete without basis");
 }
 ok(deletionScope(3,2)==="UNKNOWN","partial replicas");
 ok(deletionScope(3,3)==="ACKNOWLEDGED_WITHIN_DECLARED_SCOPE","declared replicas");
 let rejected=false;try{deletionScope(3,4)}catch(e){rejected=true}ok(rejected,"invalid ack");
 return {checks,states:32,decisions:counts,raw_pii_rejected:true,
  replica_scope_only:true,evidence:"INTERNAL_NONBLIND_ARTIFICIAL_E1"};
}
if(typeof module!=="undefined"&&module.exports)module.exports={run,retention,validateReceipt,deletionScope};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
