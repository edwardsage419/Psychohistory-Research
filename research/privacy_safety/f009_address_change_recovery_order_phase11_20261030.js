"use strict";
// Artificial account-recovery sequence test. No actual credentials or notifications.
const must=(v,m)=>{if(!v)throw Error(m)};
const bad=f=>{try{f()}catch(_){return true}return false};
function initial(){
 return {epoch:1,active:["oldA","oldB"],pending:null,appeal:false,
         recovery:"IDLE",notices:[],prior:["oldA","oldB"]};
}
function propose(s,newAddress,proof){
 if(!newAddress||s.active.includes(newAddress)||s.pending||s.appeal||
    !proof||proof.fresh_auth!==true||proof.new_address_confirmed!==true)
   throw Error("change proposal rejected");
 s.pending={address:newAddress,epoch:s.epoch+1,old:[...s.active]};
 s.notices.push({event:"CHANGE_PROPOSED",destinations:[...s.active]});
 return s;
}
function commit(s,oldChannelAck){
 if(!s.pending||s.appeal||oldChannelAck!==true)throw Error("unconfirmed change");
 if(!s.pending.old.some(x=>s.active.includes(x)))throw Error("no surviving old channel");
 s.active=[...s.active,s.pending.address];
 s.epoch=s.pending.epoch;s.pending=null;
 s.notices.push({event:"CHANGE_COMMITTED",destinations:[...s.active]});
 return s;
}
function recover(s,methods){
 if(!Array.isArray(methods)||new Set(methods).size<2||
    methods.some(x=>!["saved","issued","contact"].includes(x)))throw Error("recovery methods");
 s.recovery="LIMITED";
 s.notices.push({event:"RECOVERY",destinations:[...new Set([...s.prior,...s.active])]});
 return s;
}
function highRisk(s,proof){
 if(s.appeal||s.pending||s.recovery!=="LIMITED"||!proof||
    proof.fresh_auth!==true||proof.user_confirmed!==true||
    proof.independent_old_delivery!==true)return "BLOCK";
 return "ALLOW_BY_CANDIDATE_POLICY";
}
function naiveAttack(){
 const channels=["oldA","oldB"];
 channels.splice(0,2,"newX");
 const recoveryNotices=[...channels];
 return {recoveryNotices,oldSubscriberAlerted:recoveryNotices.some(x=>x.startsWith("old"))};
}
function run(){
 let tests=0;const ck=(v,m)=>{must(v,m);tests++};
 const naive=naiveAttack();
 ck(naive.oldSubscriberAlerted===false,"naive overwrite hides alert");
 ck(naive.recoveryNotices.length===1&&naive.recoveryNotices[0]==="newX","attacker destination");
 const s=initial();
 ck(s.active.length===2,"two initial addresses");
 ck(bad(()=>propose(s,"newX",{fresh_auth:false,new_address_confirmed:true})),"fresh auth required");
 ck(bad(()=>propose(s,"newX",{fresh_auth:true,new_address_confirmed:false})),"new address verification required");
 propose(s,"newX",{fresh_auth:true,new_address_confirmed:true});
 ck(s.pending.address==="newX","pending");
 ck(s.notices[0].destinations.join(",")==="oldA,oldB","prior addresses notified");
 ck(bad(()=>commit(s,false)),"no old acknowledgement");
 recover(s,["saved","contact"]);
 ck(s.recovery==="LIMITED","recovery restricted");
 ck(s.notices.at(-1).destinations.includes("oldB"),"recovery alerts prior channel");
 ck(!s.notices.at(-1).destinations.includes("newX"),"pending attacker address excluded");
 ck(highRisk(s,{fresh_auth:true,user_confirmed:true,independent_old_delivery:true})==="BLOCK","pending change blocks");
 commit(s,true);
 ck(s.active.includes("oldA")&&s.active.includes("oldB")&&s.active.includes("newX"),"old addresses retained");
 ck(s.epoch===2,"epoch increment");
 ck(s.notices.at(-1).destinations.includes("oldA"),"commit notice old");
 ck(highRisk(s,{fresh_auth:true,user_confirmed:true,independent_old_delivery:false})==="BLOCK","no independent delivery");
 ck(highRisk(s,{fresh_auth:false,user_confirmed:true,independent_old_delivery:true})==="BLOCK","no fresh auth");
 ck(highRisk(s,{fresh_auth:true,user_confirmed:false,independent_old_delivery:true})==="BLOCK","no user confirmation");
 ck(highRisk(s,{fresh_auth:true,user_confirmed:true,independent_old_delivery:true})==="ALLOW_BY_CANDIDATE_POLICY","bounded allow");
 s.appeal=true;
 ck(highRisk(s,{fresh_auth:true,user_confirmed:true,independent_old_delivery:true})==="BLOCK","appeal freezes");
 ck(bad(()=>propose(s,"newY",{fresh_auth:true,new_address_confirmed:true})),"appeal blocks change");
 ck(bad(()=>commit(s,true)),"no pending commit");
 const t=initial();
 recover(t,["saved","issued"]);
 ck(t.notices.at(-1).destinations.join(",")==="oldA,oldB","recovery before address change");
 ck(highRisk(t,{fresh_auth:true,user_confirmed:true,independent_old_delivery:false})==="BLOCK","unacknowledged recovery");
 ck(bad(()=>recover(initial(),["saved","saved"])),"duplicate method rejected");
 ck(bad(()=>recover(initial(),["unknown","saved"])),"unknown method rejected");
 return {tests,naive_alerted:false,candidate_preserves_old:true,
         address_change_during_recovery:"PENDING_GUARD",appeal:"BLOCK",
         cryptographic_proof:"NOT_TESTED",delivery_authenticity:"NOT_TESTED"};
}
if(typeof module!=="undefined")module.exports={initial,propose,commit,recover,highRisk,run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
