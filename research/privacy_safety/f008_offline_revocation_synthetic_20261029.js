"use strict";
// F008 phase 1: artificial two-device consent epoch and derived cache revocation.
// Run: node research/privacy_safety/f008_offline_revocation_synthetic_20261029.js
function runF008(){
  let checks=0;function ok(x,m){checks++;if(!x)throw Error("CHECK_"+checks+" "+m);}
  const server={epoch:7,grant:true,raw:true,derived:true,backup_verified:false};
  const A={name:"A",online:true,seenEpoch:7,grant:true,cache:true,ack:7};
  const B={name:"B",online:false,seenEpoch:7,grant:true,cache:true,ack:7};
  function canInfer(device,impact){
    if(impact==="HIGH"&&!device.online)return false;
    return device.online&&device.seenEpoch===server.epoch&&server.grant&&device.grant;
  }
  function upload(device,epoch){
    if(!device.online)return "OFFLINE";
    if(epoch!==server.epoch||!server.grant)return "REJECTED_STALE_OR_REVOKED";
    return "ACCEPTED";
  }
  ok(canInfer(A,"HIGH"),"initial A authorized");
  ok(!canInfer(B,"HIGH"),"offline B high impact denied");
  ok(upload(B,7)==="OFFLINE","offline cannot upload");
  server.epoch=8;server.grant=false;server.derived=false;
  A.seenEpoch=8;A.grant=false;A.cache=false;A.ack=8;
  ok(!canInfer(A,"HIGH"),"revoked A inference denied");
  ok(B.cache===true,"offline B physical cache still present");
  ok(B.seenEpoch===7,"offline B unaware of epoch");
  ok(!canInfer(B,"HIGH"),"offline high impact blocked");
  ok(server.raw===true,"primary raw data still exists until deletion");
  ok(server.backup_verified===false,"backup proof missing");
  B.online=true;
  ok(upload(B,7)==="REJECTED_STALE_OR_REVOKED","stale offline update rejected");
  function sync(device){
    if(!device.online)return "WAIT_OFFLINE";
    if(device.seenEpoch<server.epoch){
      device.seenEpoch=server.epoch;device.grant=server.grant;
      if(!server.grant)device.cache=false;
      device.ack=server.epoch;
    }
    return "SYNCED";
  }
  ok(sync(B)==="SYNCED","B receives revocation");
  ok(!B.cache,"B derived cache purged after sync");
  ok(B.ack===8&&A.ack===8,"both device acknowledgements");
  ok(upload(B,7)==="REJECTED_STALE_OR_REVOKED","old epoch cannot resurrect cache");
  ok(!canInfer(B,"HIGH"),"B inference denied after sync");
  const deviceAcks=[A,B].every(d=>d.ack===server.epoch);
  ok(deviceAcks,"device acknowledgements complete");
  const globallyErased=(!server.raw&&!server.derived&&!A.cache&&!B.cache&&server.backup_verified);
  ok(!globallyErased,"global erasure remains unverified");
  server.raw=false;
  ok(!(!server.raw&&!server.derived&&!A.cache&&!B.cache&&server.backup_verified),"backup remains open after raw removal");
  server.backup_verified=true;
  ok(!server.raw&&!server.derived&&!A.cache&&!B.cache&&server.backup_verified,"all synthetic flags clear");
  ok(!server.grant,"erasure does not silently restore consent");
  const regrant={epoch:9,approvedByHuman:false};
  ok(!regrant.approvedByHuman,"no automatic regrant");
  regrant.approvedByHuman=true;
  ok(regrant.approvedByHuman,"explicit human approval represented");
  return {checks,failures:0,offline_stale_copy_observed:true,
    stale_upload_rejected:true,post_reconnect_cache_purged:true,
    global_erase_before_backup_proof:"UNVERIFIED",
    high_impact_offline:"DENY",new_grant_requires_human:true,
    model:"SYNTHETIC_CUSTOM_POLICY_NOT_AUTOMERGE_IMPLEMENTATION"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(runF008(),null,2));
