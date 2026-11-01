'use strict';
const cached=Object.freeze({account:'A',epoch:4,issued:0,ttl:24,signed:true,status:'active'});
const naive=(s,t)=>s.signed&&s.status==='active'&&t>=s.issued&&t-s.issued<=s.ttl;
function gate({s=cached,account='A',request=true,high=true,local=6,
  trustedHour=null,trustedEpoch=null}={}){
 if(!request)return 'NO_REQUEST';
 if(!s.signed||s.account!==account)return 'REJECT_IDENTITY';
 if(s.status==='revoked')return 'REJECT_REVOKED';
 if(s.status!=='active')return 'UNKNOWN_QUARANTINE';
 if(trustedEpoch!==null&&s.epoch<trustedEpoch)return 'REJECT_EPOCH_ROLLBACK';
 if(trustedHour!==null){
   if(s.issued>trustedHour||trustedHour-s.issued>s.ttl)return 'UNKNOWN_QUARANTINE';
   return 'REVIEW_ONLY';
 }
 return 'UNKNOWN_QUARANTINE';
}
let tests=0;function check(x){if(!x)throw Error('assertion '+tests);tests++;}
check(naive(cached,6)===true);check(naive(cached,30)===false);
check(gate()==='UNKNOWN_QUARANTINE');
check(gate({trustedHour:28})==='UNKNOWN_QUARANTINE');
check(gate({trustedEpoch:5})==='REJECT_EPOCH_ROLLBACK');
check(gate({trustedEpoch:4})==='UNKNOWN_QUARANTINE');
check(gate({request:false})==='NO_REQUEST');
check(gate({account:'B'})==='REJECT_IDENTITY');
check(gate({s:{...cached,signed:false}})==='REJECT_IDENTITY');
check(gate({s:{...cached,status:'revoked'}})==='REJECT_REVOKED');
check(gate({s:{...cached,epoch:6,issued:30},trustedHour:30,trustedEpoch:5})==='REVIEW_ONLY');
check(gate({s:{...cached,epoch:6,issued:30,status:'revoked'},trustedHour:30,trustedEpoch:5})==='REJECT_REVOKED');
check(gate({s:{...cached,epoch:6,issued:31},trustedHour:30,trustedEpoch:5})==='UNKNOWN_QUARANTINE');
check(gate({s:{...cached,epoch:6,issued:30},trustedHour:55,trustedEpoch:5})==='UNKNOWN_QUARANTINE');
console.log(JSON.stringify({tests,trueHour:30,rolledBackLocalHour:6,oldEpoch:4,
 trustedEpoch:5,naiveAccepted:naive(cached,6),unknownTime:gate(),
 trustedLowerBound:gate({trustedHour:28}),epochRollback:gate({trustedEpoch:5}),
 freshActive:gate({s:{...cached,epoch:6,issued:30},trustedHour:30,trustedEpoch:5})},null,2));
