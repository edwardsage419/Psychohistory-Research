"use strict";
// F009 synthetic deletion evidence contract, no real device or user data.
function check(x,m){if(!x)throw Error(m);}
function audit(s){
  if(!s||!Number.isInteger(s.epoch)||s.epoch<1)throw Error("epoch");
  if(!Array.isArray(s.expected)||!Array.isArray(s.devices))throw Error("manifest");
  if(new Set(s.expected).size!==s.expected.length||new Set(s.devices.map(d=>d.id)).size!==s.devices.length)throw Error("duplicate");
  if(!Number.isInteger(s.unknown)||s.unknown<0)throw Error("unknown count");
  if(s.backup&&Number.isInteger(s.backup.references)&&s.backup.references<0)throw Error("negative references");
  if(!s.expected.length)return "UNKNOWN_DEVICE_UNIVERSE";
  if(s.unknown>0||s.cloud_unknown>0)return "UNKNOWN_REPLICA";
  if(s.legal_hold)return "PENDING_LEGAL_HOLD";
  if(s.expected.some(id=>!s.devices.some(d=>d.id===id)))return "UNKNOWN_DEVICE_RECEIPT";
  if(s.devices.some(d=>!Number.isInteger(d.ack)||d.ack<s.epoch))return "PENDING_REPLICA";
  if(s.devices.some(d=>d.ack>s.epoch||d.verified!==true))return "UNKNOWN_DEVICE_RECEIPT";
  if(!s.archive||s.archive.cleaned!==true)return "PENDING_ARCHIVE";
  if(s.archive.epoch!==s.epoch||s.archive.verified!==true)return "UNKNOWN_ARCHIVE_RECEIPT";
  if(!s.backup||!Number.isInteger(s.backup.references))return "UNKNOWN_BACKUP_REFERENCES";
  if(s.backup.references>0)return "PENDING_BACKUP_REFERENCE";
  if(s.backup.pruned!==true)return "PENDING_PRUNE";
  if(s.backup.epoch!==s.epoch||s.backup.verified!==true)return "UNKNOWN_PRUNE_RECEIPT";
  return "MODEL_SCOPE_COMPLETE";
}
const base={epoch:2,expected:["A","B","C"],devices:["A","B","C"].map(id=>({id,ack:2,verified:true})),unknown:0,cloud_unknown:0,legal_hold:false,archive:{cleaned:true,epoch:2,verified:true},backup:{references:0,pruned:true,epoch:2,verified:true}};
const clone=()=>JSON.parse(JSON.stringify(base));
function run(){
  check(audit(clone())==="MODEL_SCOPE_COMPLETE","positive");
  const controls=[
    ["offline",s=>s.devices[1].ack=1,"PENDING_REPLICA"],
    ["unknown",s=>s.unknown=1,"UNKNOWN_REPLICA"],
    ["cloud",s=>s.cloud_unknown=1,"UNKNOWN_REPLICA"],
    ["missing_device",s=>s.devices.pop(),"UNKNOWN_DEVICE_RECEIPT"],
    ["unsigned",s=>s.devices[0].verified=false,"UNKNOWN_DEVICE_RECEIPT"],
    ["archive_pending",s=>s.archive.cleaned=false,"PENDING_ARCHIVE"],
    ["archive_stale",s=>s.archive.epoch=1,"UNKNOWN_ARCHIVE_RECEIPT"],
    ["shared_backup",s=>s.backup.references=1,"PENDING_BACKUP_REFERENCE"],
    ["prune_interrupted",s=>s.backup.pruned=false,"PENDING_PRUNE"],
    ["prune_stale",s=>s.backup.epoch=1,"UNKNOWN_PRUNE_RECEIPT"],
    ["legal_hold",s=>s.legal_hold=true,"PENDING_LEGAL_HOLD"],
    ["missing_backup",s=>delete s.backup,"UNKNOWN_BACKUP_REFERENCES"]
  ];
  const results={};
  for(const [name,mutate,expected] of controls){const s=clone();mutate(s);const actual=audit(s);check(actual===expected,name+":"+actual);results[name]=actual;}
  const invalid=[s=>s.epoch=0,s=>s.expected=["A","A"],s=>s.devices.push({...s.devices[0]}),s=>s.unknown=-1,s=>s.backup.references=-1];
  for(const mutate of invalid){const s=clone();mutate(s);let rejected=false;try{audit(s);}catch(_){rejected=true;}check(rejected,"malformed input accepted");}
  return {kind:"ARTIFICIAL_E1_NONBLIND",positive:"MODEL_SCOPE_COMPLETE",negative:results,invalid_rejected:invalid.length,physical_erasure:"NOT_VERIFIED"};
}
const results=run();
if(typeof console!=="undefined")console.log(JSON.stringify(results));
