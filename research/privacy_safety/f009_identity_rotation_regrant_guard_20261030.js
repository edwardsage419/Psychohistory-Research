// F009 phase6 artificial credential rotation and deleted-epoch replay guard.
// Boolean verification fields are mock inputs, not cryptographic verification.
"use strict";
function check(s,op){
 if(!s||!op||!Number.isSafeInteger(s.deleteEpoch)||!Number.isSafeInteger(op.epoch)||s.deleteEpoch<0||op.epoch<0)throw Error("bad epoch");
 if(typeof op.credential!=="string"||!Array.isArray(s.credentials))throw Error("bad credential");
 if(s.auditExpired)return "QUARANTINE_AUDIT_EXPIRED";
 if(s.rosterComplete!==true)return "QUARANTINE_ROSTER_UNKNOWN";
 const c=s.credentials.find(x=>x.id===op.credential);
 if(!c)return "QUARANTINE_UNKNOWN_CREDENTIAL";
 if(c.revoked===true)return "REJECT_REVOKED_CREDENTIAL";
 if(c.verified!==true)return "QUARANTINE_UNVERIFIED_BINDING";
 if(op.epoch<=s.deleteEpoch)return "REJECT_OLD_CONTENT";
 if(c.boundEpoch>s.deleteEpoch && c.boundEpoch>op.epoch)return "QUARANTINE_PRE_BIND_OPERATION";
 if(c.boundEpoch>s.deleteEpoch && s.regrantVerified!==true)return "QUARANTINE_REGRANT_UNVERIFIED";
 if(s.lostDevicePending===true)return "QUARANTINE_LOST_DEVICE";
 return "MODEL_SCOPE_ACCEPT";
}
function run(){
 let checks=0,rejections=0;const ok=(x)=>{if(!x)throw Error("assert "+checks);checks++};
 const base={deleteEpoch:7,auditExpired:false,rosterComplete:true,regrantVerified:true,lostDevicePending:false,credentials:[{id:"old",revoked:true,verified:true,boundEpoch:1},{id:"new",revoked:false,verified:true,boundEpoch:8}]};
 const op={credential:"new",epoch:8};
 ok(check(base,op)==="MODEL_SCOPE_ACCEPT");
 ok(check(base,{credential:"old",epoch:9})==="REJECT_REVOKED_CREDENTIAL");
 ok(check(base,{credential:"new",epoch:7})==="REJECT_OLD_CONTENT");
 ok(check(base,{credential:"fake",epoch:9})==="QUARANTINE_UNKNOWN_CREDENTIAL");
 ok(check({...base,rosterComplete:false},op)==="QUARANTINE_ROSTER_UNKNOWN");
 ok(check({...base,auditExpired:true},op)==="QUARANTINE_AUDIT_EXPIRED");
 ok(check({...base,regrantVerified:false},op)==="QUARANTINE_REGRANT_UNVERIFIED");
 ok(check({...base,lostDevicePending:true},op)==="QUARANTINE_LOST_DEVICE");
 ok(check({...base,credentials:[{id:"new",revoked:false,verified:false,boundEpoch:8}]},op)==="QUARANTINE_UNVERIFIED_BINDING");
 ok(check(base,{credential:"new",epoch:6})==="REJECT_OLD_CONTENT");
 ok(check({...base,credentials:[{id:"new",revoked:false,verified:true,boundEpoch:10}]},op)==="QUARANTINE_PRE_BIND_OPERATION");
 ok(check(base,{credential:"new",epoch:11})==="MODEL_SCOPE_ACCEPT");
 for(const [s,o] of [[{...base,deleteEpoch:-1},op],[base,{credential:"new",epoch:-1}],[base,{credential:7,epoch:9}],[{...base,credentials:null},op]]){let rejected=false;try{check(s,o)}catch(e){rejected=true}if(!rejected)throw Error("negative");rejections++;}
 return {checks,rejections,warning:"MOCK_BOOLEAN_NOT_CRYPTOGRAPHIC_EVIDENCE"};
}
if(typeof module!=="undefined")module.exports={check,run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
