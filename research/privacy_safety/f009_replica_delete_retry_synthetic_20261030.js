#!/usr/bin/env node
"use strict";
// F009 synthetic three-replica deletion acknowledgement model.
// Acknowledgement is only local model state; never proof of physical erasure.
function start(){return{
  epoch:1,deleted:false,
  devices:{A:{online:true,live:true,ack:1,archive:false},
           B:{online:false,live:true,ack:1,archive:false},
           C:{online:true,live:true,ack:1,archive:false}}};}
function requestDelete(s,newEpoch){
  if(!Number.isInteger(newEpoch)||newEpoch<=s.epoch)throw Error("invalid epoch");
  s.epoch=newEpoch;s.deleted=true;
  s.devices.A.live=false;s.devices.A.ack=newEpoch;
}
function receive(s,id,opts={}){
  const d=s.devices[id];if(!d||!d.online)throw Error("offline or unknown");
  if(!s.deleted)throw Error("no tombstone");
  if(opts.ignoreDelete)return false;
  if(d.live&&opts.versioning)d.archive=true;
  d.live=false;d.ack=s.epoch;return true;
}
function staleWrite(s,id,version){
  if(!s.devices[id]||!Number.isInteger(version)||version<0)throw Error("invalid write");
  if(s.deleted&&version<s.epoch)return false;
  s.devices[id].live=true;return true;
}
function status(s){
  if(!s.deleted)return "ACTIVE";
  if(Object.values(s.devices).some(d=>d.live||d.ack<s.epoch))return "PENDING_REPLICA";
  if(Object.values(s.devices).some(d=>d.archive))return "PENDING_ARCHIVE";
  return "MODEL_ACK_COMPLETE";
}
function run(){
  let checks=0,invalid_rejected=0;
  function eq(a,b){if(a!==b)throw Error("assert "+a+" != "+b);checks++;}
  const s=start();eq(status(s),"ACTIVE");
  requestDelete(s,2);receive(s,"C",{versioning:true});
  eq(status(s),"PENDING_REPLICA");eq(s.devices.C.archive,true);
  s.devices.B.online=true;eq(staleWrite(s,"B",1),false);
  receive(s,"B");eq(status(s),"PENDING_ARCHIVE");
  s.devices.C.archive=false;eq(status(s),"MODEL_ACK_COMPLETE");
  const t=start();requestDelete(t,2);
  eq(receive(t,"C",{ignoreDelete:true}),false);
  eq(status(t),"PENDING_REPLICA");
  eq(t.devices.C.live,true);
  const bad=[()=>requestDelete(t,2),()=>receive(t,"B"),()=>staleWrite(t,"X",1)];
  for(const f of bad){let caught=false;try{f();}catch(_){caught=true;}if(!caught)throw Error("bad input accepted");invalid_rejected++;}
  return{status:"PASS",checks,invalid_rejected,
    strict:["PENDING_REPLICA","PENDING_ARCHIVE","MODEL_ACK_COMPLETE"],
    ignore_delete:"PENDING_REPLICA",
    scope:"synthetic state machine, no Syncthing executable, backup erasure or device tests"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
