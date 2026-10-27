#!/usr/bin/env node
"use strict";
// Read-only structural validation of publicly provided experimental CSV; no private data.
const fs=require("node:fs"),crypto=require("node:crypto");
function auditCSV(csv){
const header="period,subject,group,profit,contrib,received,reduction,opp1,opp2,opp3,pun1,pun2,pun3,con1,con2,con3,session,base,punish,you_punished,got,expend,below,above,gave_more_than_avg,diff,set,mod_period".split(",");
const lines=csv.trimEnd().split(/\r?\n/);
if(lines.shift()!==header.join(","))throw Error("header mismatch");
const rows=lines.map(line=>{let parts=line.split(",");if(parts.length!==28)throw Error("field count");return Object.fromEntries(header.map((h,i)=>[h,parts[i]]))});
const groups=new Map(),persons=new Map(),rounds=new Map(),sessions=new Map(),keys=new Set();
let duplicate=0,missing=0,contribRange=0,invalidPunish=0;
for(const r of rows){
const person=r.session+"|"+r.subject,group=r.session+"|"+r.period+"|"+r.group,round=r.session+"|"+r.period,key=person+"|"+r.period;
if(keys.has(key))duplicate++;keys.add(key);
if(!groups.has(group))groups.set(group,[]);groups.get(group).push(r);
if(!persons.has(person))persons.set(person,[]);persons.get(person).push(r);
rounds.set(round,(rounds.get(round)||0)+1);
if(!sessions.has(r.session))sessions.set(r.session,{rows:0,persons:new Set(),periods:new Set(),groups:new Set()});
const s=sessions.get(r.session);s.rows++;s.persons.add(r.subject);s.periods.add(+r.period);s.groups.add(r.group);
if(header.some(h=>r[h]===""))missing++;
if(!Number.isInteger(+r.contrib)||+r.contrib<0||+r.contrib>20)contribRange++;
if(!Number.isInteger(+r.punish)||+r.punish<0||+r.punish>3)invalidPunish++;
}
let badGroup=0,badPeer=0,badPeerDuplicate=0;
for(const rr of groups.values()){
if(rr.length!==4)badGroup++;
for(const r of rr){
const peers=rr.filter(z=>z.subject!==r.subject).map(z=>z.subject).sort((a,b)=>+a-+b);
const obs=[r.opp1,r.opp2,r.opp3].sort((a,b)=>+a-+b);
if(new Set(obs).size!==3)badPeerDuplicate++;
if(peers.join(",")!==obs.join(","))badPeer++;
}}
let switched=0,sequenceGaps=0;const trialCounts={};
for(const rr of persons.values()){
const p=rr.map(x=>+x.period).sort((a,b)=>a-b),g=new Set(rr.map(x=>x.group));
if(g.size>1)switched++;
if(p.some((x,i)=>x!==i+1))sequenceGaps++;
trialCounts[p.length]=(trialCounts[p.length]||0)+1;
}
const report={source:"MIT-Blueprint-Labs/unobserved_punishment",source_blob_sha1:"f5767dd72928b16eaa30c8cc67af15b17ad25d4c",raw_public_csv_bytes:csv.length,columns:header.length,rows:rows.length,sessions:Object.fromEntries([...sessions].sort().map(([name,s])=>[name,{rows:s.rows,participants:s.persons.size,periods:s.periods.size,group_labels:s.groups.size}])),session_count:sessions.size,participant_session_identities:persons.size,session_period_group_cells:groups.size,group_size_four_errors:badGroup,peer_id_set_mismatches:badPeer,peer_id_duplicates:badPeerDuplicate,duplicate_person_period:duplicate,missing_field_rows:missing,invalid_contribution:contribRange,invalid_punish_count:invalidPunish,participants_with_changed_group_label:switched,nonconsecutive_person_periods:sequenceGaps,participant_round_counts:trialCounts,unique_session_rounds:rounds.size,license:"NO_EXPLICIT_DATA_LICENSE_VERIFIED",R073_direct_compatibility:"NO_4_PERSON_PUBLIC_GOODS_GAME_NOT_FROZEN_2_PERSON_100_ROUND_PD",E2_prediction_new:0};
if(rows.length!==2400||persons.size!==132||groups.size!==600||badGroup||badPeer||badPeerDuplicate||duplicate||missing||contribRange||invalidPunish||sequenceGaps||switched!==132)throw Error("dataset structure gate failed");
return report;
}
function main(){const file=process.argv[2];if(!file)throw Error("Usage: node a_fudenberg_pathak_unobserved_punishment_source_gate_20261028.js /path/to/unobserved_dataset.csv");const csv=fs.readFileSync(file,"utf8");const hash=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+Buffer.byteLength(csv)+"\0"),Buffer.from(csv)])).digest("hex");if(hash!=="f5767dd72928b16eaa30c8cc67af15b17ad25d4c")throw Error("Git blob identity mismatch");process.stdout.write(JSON.stringify(auditCSV(csv),null,2)+"\n");}
if(require.main===module)main();module.exports={auditCSV};
