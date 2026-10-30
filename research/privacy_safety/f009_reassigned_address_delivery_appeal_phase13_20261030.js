"use strict";
function route(s){
  const names=["verified","ownerMatch","active","compromised","appeal","deliveryAck"];
  if(!s||names.some(k=>typeof s[k]!=="boolean"))throw Error("incomplete or invalid state");
  const allowed=s.verified&&s.ownerMatch&&s.active&&!s.compromised&&!s.appeal;
  return {send:allowed,deliveryEvidence:allowed&&s.deliveryAck?"PROVIDER_ACK_ONLY":allowed?"SENT_NO_ACK":"NO_SEND",readBySubscriber:"UNKNOWN",highRiskRelease:allowed&&s.deliveryAck};
}
function study(){
  let tests=0;function ok(c,msg){tests++;if(!c)throw Error("assert "+msg);}
  const keys=["verified","ownerMatch","active","compromised","appeal","deliveryAck"];
  let naiveSends=0,safeSends=0,unsafeNaive=0,ackSends=0,highRisk=0;
  for(let mask=0;mask<64;mask++){
    const s=Object.fromEntries(keys.map((k,i)=>[k,!!(mask&(1<<i))]));
    const result=route(s);
    if(s.active)naiveSends++;
    if(result.send)safeSends++;
    if(s.active&&!result.send)unsafeNaive++;
    if(result.deliveryEvidence==="PROVIDER_ACK_ONLY")ackSends++;
    if(result.highRiskRelease)highRisk++;
    ok(result.readBySubscriber==="UNKNOWN","delivery not read proof");
    ok(!result.send||s.verified&&s.ownerMatch&&s.active&&!s.compromised&&!s.appeal,"guard");
    ok(!result.highRiskRelease||result.send&&s.deliveryAck,"high risk guard");
  }
  ok(naiveSends===32,"naive sends");
  ok(safeSends===2,"safe sends");
  ok(unsafeNaive===30,"unsafe naive sends");
  ok(ackSends===1,"provider ack");
  ok(highRisk===1,"candidate high-risk gate");
  const good={verified:true,ownerMatch:true,active:true,compromised:false,appeal:false,deliveryAck:true};
  ok(route(good).send,"valid verified route");
  ok(route({...good,ownerMatch:false}).send===false,"reassigned address");
  ok(route({...good,verified:false}).send===false,"unverified new address");
  ok(route({...good,compromised:true}).send===false,"compromised address");
  ok(route({...good,appeal:true}).highRiskRelease===false,"appeal hold");
  ok(route({...good,deliveryAck:false}).deliveryEvidence==="SENT_NO_ACK","no ack");
  ok(route({...good,deliveryAck:true}).readBySubscriber==="UNKNOWN","ack not read");
  for(const bad of [null,{}, {...good,ownerMatch:null},{...good,active:"yes"},{...good,deliveryAck:undefined}]){
    let failed=false;try{route(bad)}catch(_){failed=true;}ok(failed,"reject unknown state");
  }
  return {status:"PASS",tests,worlds:64,naive_send_worlds:naiveSends,guarded_send_worlds:safeSends,naive_unsafe_worlds:unsafeNaive,provider_ack_worlds:ackSends,high_risk_candidate_release_worlds:highRisk};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(study(),null,2));
