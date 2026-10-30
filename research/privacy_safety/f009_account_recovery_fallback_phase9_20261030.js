"use strict";
// Toy authorization state machine. No secrets, signatures, accounts, or personal data.
function initial(){
 return {epoch:1,oldCredential:"ACTIVE",savedCode:"UNUSED",
 recovery:"NONE",newCredential:"NONE",notifications:[],highRiskAllowed:false};
}
function recover(s,methods){
 if(s.recovery!=="NONE")throw Error("recovery already started");
 if(!Array.isArray(methods)||new Set(methods).size!==methods.length)throw Error("duplicate proofs");
 const allowed=["SAVED","ISSUED","CONTACT"];
 if(methods.some(x=>!allowed.includes(x)))throw Error("invalid proof");
 if(methods.length<2)throw Error("insufficient independent proofs");
 if(methods.includes("SAVED")&&s.savedCode!=="UNUSED")throw Error("reused code");
 return {...s,epoch:s.epoch+1,oldCredential:"REVOKED",
 savedCode:methods.includes("SAVED")?"CONSUMED":s.savedCode,
 recovery:"LIMITED",notifications:["ADDRESS_1","ADDRESS_2"],highRiskAllowed:false};
}
function bindNew(s,validFreshProof){
 if(s.recovery!=="LIMITED"||validFreshProof!==true)throw Error("bind denied");
 return {...s,newCredential:"ACTIVE",recovery:"BOUND",highRiskAllowed:false};
}
function highRisk(s,freshBoundAuth,userConfirmation){
 return s.recovery==="BOUND"&&s.newCredential==="ACTIVE"&&freshBoundAuth===true&&userConfirmation===true;
}
function oldAccepted(s,epoch){return s.oldCredential==="ACTIVE"&&s.epoch===epoch;}
function assert(ok,name){if(!ok)throw Error("ASSERT "+name);}
function runTests(){
 let count=0;
 function yes(ok,name){assert(ok,name);count++;}
 function no(fn,name){let rejected=false;try{fn();}catch(e){rejected=true;}yes(rejected,name);}
 const s0=initial();
 yes(oldAccepted(s0,1),"initial credential");
 no(()=>recover(s0,["ISSUED"]),"single email fallback");
 no(()=>recover(s0,["SAVED","SAVED"]),"same method twice");
 no(()=>recover(s0,["SAVED","UNTRUSTED"]),"unknown proof");
 const s1=recover(s0,["SAVED","ISSUED"]);
 yes(s1.epoch===2,"epoch advanced");
 yes(s1.oldCredential==="REVOKED","old credential revoked");
 yes(!oldAccepted(s1,1),"old credential rejected");
 yes(s1.savedCode==="CONSUMED","saved code consumed");
 yes(s1.notifications.length===2,"two notices queued");
 yes(s1.recovery==="LIMITED","limited recovery");
 yes(!highRisk(s1,true,true),"high risk blocked during recovery");
 no(()=>recover(s1,["SAVED","ISSUED"]),"recovery replay");
 no(()=>bindNew(s1,false),"unproven binding");
 const s2=bindNew(s1,true);
 yes(s2.newCredential==="ACTIVE","new bound");
 yes(!highRisk(s2,false,true),"fresh auth required");
 yes(!highRisk(s2,true,false),"confirmation required");
 yes(highRisk(s2,true,true),"confirmed after fresh auth");
 yes(!oldAccepted(s2,1),"old credential still rejected");
 return {passed:count,epoch:s2.epoch,notification_count:s2.notifications.length,
 high_risk_without_fresh_auth:highRisk(s2,false,true)};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(runTests()));
