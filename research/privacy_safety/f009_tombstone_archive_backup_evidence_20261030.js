"use strict";
function initial(){return {epoch:2,devices:{A:{active:false,ack:2},B:{active:true,ack:1},C:{active:false,ack:2}},archive:1,snapshotRefs:1,pruned:false,unknown:0};}
function status(s){if(s.unknown)return "UNKNOWN_REPLICA";if(Object.values(s.devices).some(d=>d.active||d.ack<s.epoch))return "PENDING_REPLICA";if(s.archive)return "PENDING_ARCHIVE";if(s.snapshotRefs)return "PENDING_BACKUP_REFERENCE";if(!s.pruned)return "PENDING_PRUNE";return "MODEL_SCOPE_COMPLETE";}
function write(s,id,epoch){if(!Number.isInteger(epoch)||epoch<0)throw Error("epoch");if(!s.devices[id])throw Error("device");return epoch<=s.epoch?"REJECT_STALE":"REQUIRES_NEW_AUTHORIZATION";}
function ack(s,id,epoch){if(!s.devices[id]||epoch!==s.epoch)throw Error("ack");s.devices[id].active=false;s.devices[id].ack=epoch;}
function run(){
 let s=initial(),checks=0;const test=(b,n)=>{if(!b)throw Error(n);checks++;};
 test(status(s)==="PENDING_REPLICA","offline");
 test(write(s,"B",1)==="REJECT_STALE","stale");
 test(s.devices.B.active,"reject no erasure");
 ack(s,"B",2);test(status(s)==="PENDING_ARCHIVE","archive");
 s.archive=0;test(status(s)==="PENDING_BACKUP_REFERENCE","backup");
 s.snapshotRefs=0;test(status(s)==="PENDING_PRUNE","forget");
 s.pruned=true;test(status(s)==="MODEL_SCOPE_COMPLETE","scope");
 s.unknown=1;test(status(s)==="UNKNOWN_REPLICA","unknown");
 s.unknown=0;s.snapshotRefs=1;test(status(s)==="PENDING_BACKUP_REFERENCE","shared ref");
 s.snapshotRefs=0;s.pruned=false;test(status(s)==="PENDING_PRUNE","interrupted");
 let rejected=0;for(const fn of [()=>write(s,"B",-1),()=>write(s,"X",1),()=>ack(s,"X",2),()=>ack(s,"B",1)])try{fn();}catch(e){rejected++;}
 test(rejected===4,"negative controls");
 return {checks,rejected,sequence:["PENDING_REPLICA","PENDING_ARCHIVE","PENDING_BACKUP_REFERENCE","PENDING_PRUNE","MODEL_SCOPE_COMPLETE"],realErasureVerified:false};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
