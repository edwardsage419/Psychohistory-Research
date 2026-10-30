'use strict';
// Candidate policy with artificial day numbers. 30 days is an illustrative local parameter, not a NIST requirement.
const assert=require('node:assert/strict');
let checks=0;
function check(v,msg){assert.ok(v,msg);checks++;}
function decide(x){
  const required=['nowDay','oldVerifiedDay','oldStatus','newVerified','deletionRequested','legalHold','appealOpen','recoveryMethods','freshAuth'];
  if(required.some(k=>!(k in x)))throw Error('missing field');
  if(!Number.isInteger(x.nowDay)||!Number.isInteger(x.oldVerifiedDay)||x.nowDay<x.oldVerifiedDay)throw Error('time');
  if(!['ACTIVE','STALE','COMPROMISED'].includes(x.oldStatus))throw Error('status');
  if(!Array.isArray(x.recoveryMethods)||new Set(x.recoveryMethods).size!==x.recoveryMethods.length)throw Error('recovery duplication');
  if(x.recoveryMethods.some(v=>!['saved_code','issued_code','recovery_contact','single_factor'].includes(v)))throw Error('method');
  const retentionDays=30;
  const oldAge=x.nowDay-x.oldVerifiedDay;
  const purgeOld=(x.deletionRequested&&!x.legalHold)||oldAge>=retentionDays||x.oldStatus==='COMPROMISED';
  const notifyOld=!purgeOld&&x.oldStatus==='ACTIVE';
  const notifyNew=x.newVerified===true;
  const noticeRoutes=[...(notifyOld?['old_verified']:[]),...(notifyNew?['new_verified']:[])];
  const recoveryReady=x.recoveryMethods.includes('saved_code')&&x.recoveryMethods.includes('single_factor');
  const highRiskAllowed=!!(x.newVerified&&x.freshAuth&&recoveryReady&&!x.appealOpen&&noticeRoutes.length>0);
  return {purgeOld,noticeRoutes,notificationIssued:noticeRoutes.length>0,
    oldDeliveryVerified:false,highRiskAllowed,reviewRequired:!highRiskAllowed,
    audit:{event:'RECOVERY_REVIEW',routeCount:noticeRoutes.length,oldPurged:purgeOld},
    policy:'ARTIFICIAL_LOCAL_30_DAY_RETENTION_EXAMPLE'};
}
const base={nowDay:10,oldVerifiedDay:0,oldStatus:'ACTIVE',newVerified:true,
  deletionRequested:false,legalHold:false,appealOpen:false,
  recoveryMethods:['saved_code','single_factor'],freshAuth:true};
const run=x=>decide({...base,...x});
check(run({}).highRiskAllowed,'happy candidate');
check(run({}).noticeRoutes.length===2,'two notice routes');
check(run({}).oldDeliveryVerified===false,'send is not delivery');
check(run({nowDay:29}).purgeOld===false,'before expiration');
check(run({nowDay:30}).purgeOld===true,'expiration');
check(run({nowDay:30}).noticeRoutes.length===1,'expired not notified');
check(run({oldStatus:'STALE'}).noticeRoutes.length===1,'stale not notified');
check(run({oldStatus:'COMPROMISED'}).purgeOld,'compromise purge');
check(run({oldStatus:'COMPROMISED'}).noticeRoutes.length===1,'compromise no old notify');
check(run({deletionRequested:true}).purgeOld,'deletion');
check(run({deletionRequested:true,legalHold:true}).purgeOld===false,'hold exception reviewed');
check(run({newVerified:false,oldStatus:'STALE'}).noticeRoutes.length===0,'no route');
check(run({newVerified:false,oldStatus:'STALE'}).highRiskAllowed===false,'no route block');
check(run({appealOpen:true}).highRiskAllowed===false,'appeal block');
check(run({freshAuth:false}).highRiskAllowed===false,'reauth block');
check(run({recoveryMethods:['saved_code']}).highRiskAllowed===false,'insufficient methods');
check(run({newVerified:false}).highRiskAllowed===false,'new address unverified');
check(run({}).audit.event==='RECOVERY_REVIEW','minimal event label');
check(!('email' in run({}).audit),'no raw email in receipt');
for(const invalid of [
 {nowDay:-1},{oldStatus:'UNKNOWN'},{recoveryMethods:['saved_code','saved_code']},
 {recoveryMethods:['unapproved']},{oldVerifiedDay:11}]){
 let rejected=false;try{run(invalid)}catch{rejected=true}check(rejected,'invalid case');
}
console.log(JSON.stringify({checks,scope:'ARTIFICIAL_E1_NONBLIND',candidateRetentionDays:30,
  legalRuleClaimed:false,realNotificationTested:false,realAccountTested:false}));
