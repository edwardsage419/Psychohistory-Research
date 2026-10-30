"use strict";
function assert(ok, msg) { if (!ok) throw Error(msg); }
function rejects(fn) { try { fn(); } catch (_) { return true; } return false; }
function account() {
  return {epoch:1,code:{S1:"ACTIVE",S2:"ACTIVE"}, recovery:"NONE",
    notice:{email:"NONE",alternate:"NONE"},freshAuth:false,confirmed:false,
    appeal:"NONE",highRiskAllowed:false};
}
function rotate(a, oldId, newId) {
  if (a.code[oldId]!=="ACTIVE" || a.code[newId]!==undefined) throw Error("invalid rotation");
  a.code[oldId]="REVOKED"; a.code[newId]="ACTIVE";
  a.notice.email="PENDING"; a.notice.alternate="PENDING";
}
function recover(a, methods, savedCode) {
  if (a.recovery!=="NONE" || !Array.isArray(methods) || methods.length!==2 ||
      new Set(methods).size!==2 || !methods.includes("SAVED") || !methods.includes("ISSUED") ||
      a.code[savedCode]!=="ACTIVE") throw Error("invalid recovery");
  a.code[savedCode]="CONSUMED";
  a.epoch++;
  a.recovery="LIMITED";
  a.freshAuth=false; a.confirmed=false; a.highRiskAllowed=false;
  a.notice.email="PENDING"; a.notice.alternate="PENDING";
}
function notify(a, address, next) {
  if (!["email","alternate"].includes(address)) throw Error("unknown address");
  const old=a.notice[address];
  if (!({PENDING:["SENT","FAILED"],SENT:["DELIVERED","FAILED"],
          FAILED:["SENT"]}[old]||[]).includes(next)) throw Error("bad notice transition");
  a.notice[address]=next;
}
function authorize(a, presentedEpoch) {
  const delivered=Object.values(a.notice).includes("DELIVERED");
  if (presentedEpoch!==a.epoch || a.recovery!=="LIMITED" ||
      !a.freshAuth || !a.confirmed || !delivered || a.appeal!=="NONE")
    return {allowed:false,reason:"hold"};
  a.highRiskAllowed=true;return {allowed:true,reason:"confirmed"};
}
function openAppeal(a) { a.appeal="OPEN";a.highRiskAllowed=false; }
function closeAppeal(a, reviewed) {
  if (a.appeal!=="OPEN" || reviewed!==true) throw Error("review required");
  a.appeal="RESOLVED";a.highRiskAllowed=false;
}
function run() {
  let tests=0;const check=(ok,msg)=>{assert(ok,msg);tests++;};
  const a=account();
  check(a.epoch===1,"initial epoch");
  check(a.code.S1==="ACTIVE","initial code");
  check(rejects(()=>recover(a,["ISSUED","ISSUED"],"S1")),"same method");
  check(rejects(()=>recover(a,["ISSUED"],"S1")),"one method");
  check(rejects(()=>recover(a,["SAVED","ISSUED"],"BAD")),"bad saved code");
  rotate(a,"S1","S3");
  check(a.code.S1==="REVOKED","old code revoked");
  check(a.code.S3==="ACTIVE","replacement active");
  check(rejects(()=>recover(a,["SAVED","ISSUED"],"S1")),"revoked code refused");
  check(rejects(()=>rotate(a,"S1","S4")),"revoked code cannot rotate");
  recover(a,["SAVED","ISSUED"],"S3");
  check(a.epoch===2 && a.recovery==="LIMITED","limited epoch");
  check(a.code.S3==="CONSUMED","one time code consumed");
  check(rejects(()=>recover(a,["SAVED","ISSUED"],"S3")),"reuse refused");
  check(authorize(a,1).allowed===false,"old epoch denied");
  check(authorize(a,2).allowed===false,"no fresh auth");
  a.freshAuth=true;a.confirmed=true;
  check(authorize(a,2).allowed===false,"notice pending hold");
  notify(a,"email","FAILED");
  notify(a,"alternate","FAILED");
  check(authorize(a,2).allowed===false,"both failed hold");
  check(rejects(()=>notify(a,"email","DELIVERED")),"no direct delivery from failed");
  notify(a,"email","SENT");
  check(authorize(a,2).allowed===false,"sent not delivered");
  notify(a,"email","DELIVERED");
  check(authorize(a,2).allowed===true,"one delivered and fresh proof");
  openAppeal(a);
  check(authorize(a,2).allowed===false,"appeal hold");
  check(rejects(()=>closeAppeal(a,false)),"appeal review mandatory");
  closeAppeal(a,true);
  check(a.appeal==="RESOLVED" && !a.highRiskAllowed,"appeal resolution no automatic high risk");
  check(authorize(a,2).allowed===false,"resolved appeal requires separate release policy");
  check(rejects(()=>notify(a,"invalid","SENT")),"bad address");
  check(rejects(()=>notify(a,"email","DELIVERED")),"repeated delivery refused");
  return {tests,epoch:a.epoch,rotated_code:a.code.S1,consumed_code:a.code.S3,
    notification:a.notice,appeal:a.appeal,highRiskAllowed:a.highRiskAllowed};
}
if (typeof module!=="undefined") module.exports={account,rotate,recover,notify,authorize,openAppeal,closeAppeal,run};
if (typeof require!=="undefined" && typeof module!=="undefined" && require.main===module) console.log(JSON.stringify(run()));
