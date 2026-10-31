#!/usr/bin/env node
"use strict";
// R317 S113 exact finite E1, frozen 2026-10-31. No external dependencies.
const fs=require("fs"),crypto=require("crypto"),edges=[[0,1],[0,2],[1,2]];
const maps=["PAIR_ONLY","FULL","MULTISET","STATIC","FIRST","LAST","DISTINCT_COUNT"];
function check(x,m){if(!x)throw Error(m)}
function gcd(a,b){while(b){let t=a%b;a=b;b=t}return a}
function plus(x,y){let n=x[0]*y[1]+y[0]*x[1],d=x[1]*y[1],g=gcd(n,d);return [n/g,d/g]}
function frac(x){return x[0].toString()+"/"+x[1].toString()}
function gitblob(s){return crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0").update(s).digest("hex")}
function arrival(seq,origin){
  let a=[null,null,null];a[origin]=0;
  seq.forEach((id,i)=>{let [u,v]=edges[id],t=i+1,old=a.slice();
    if(old[u]!==null&&old[v]===null)a[v]=t;
    if(old[v]!==null&&old[u]===null)a[u]=t;
  });return a;
}
function observed(m,seq){
  if(m==="PAIR_ONLY")return "none";
  if(m==="FULL")return seq.join("");
  if(m==="MULTISET")return seq.slice().sort().join("");
  if(m==="STATIC")return [...new Set(seq)].sort().join("");
  if(m==="FIRST")return String(seq[0]);
  if(m==="LAST")return String(seq[2]);
  if(m==="DISTINCT_COUNT")return String(new Set(seq).size);
  throw Error("unknown observation");
}
let source="schedule_id,schedule_code,time,contact_index,node_u,node_v\n",rows=[];
for(let s=0;s<27;s++){
  let seq=[Math.floor(s/9),Math.floor(s/3)%3,s%3],code=seq.join("");
  seq.forEach((id,i)=>{let [u,v]=edges[id];source+=[s,code,i+1,id,u,v].join(",")+"\n"});
  for(let origin=0;origin<3;origin++){
    let a=arrival(seq,origin);
    for(let target=0;target<3;target++)if(origin!==target)
      rows.push({schedule_id:s,schedule_code:code,origin,target,reachable:Number(a[target]!==null),arrival:a[target]});
  }
}
check(rows.length===162,"162 rows");
const blob=gitblob(source);
check(blob==="926c1fee6a473da6bbedb9746cf109f5a3a3eb16","original source blob");
let receipt={schema:"r317_s113_temporal_coarsening_exact_v1",evidence:"E1_FINITE_ARTIFICIAL_ONLY",
 source_git_blob:blob,instances:162,schedules:27,origins:3,ordered_targets_per_origin:2,
 totals:{positive:rows.filter(r=>r.reachable).length,negative:rows.filter(r=>!r.reachable).length},maps:{}};
for(let m of maps){
 let groups=new Map();
 for(let r of rows){let key=r.origin+">"+r.target+"|"+observed(m,r.schedule_code.split("").map(Number));
  if(!groups.has(key))groups.set(key,[0,0]);groups.get(key)[r.reachable]++}
 let correct=0,mixed=0,ties=0,brier=[0n,1n];
 for(let [n0,n1] of groups.values()){let n=n0+n1;correct+=Math.max(n0,n1);
  if(n0&&n1)mixed++;if(n0===n1)ties++;
  brier=plus(brier,[BigInt(n0*n1),BigInt(n)])}
 brier=plus([0n,1n],[brier[0],brier[1]*162n]);
 let accuracy=plus([0n,1n],[BigInt(correct),162n]);
 receipt.maps[m]={keys:groups.size,mixed_keys:mixed,tie_keys:ties,correct,
  accuracy:frac(accuracy),brier:frac(brier)};
}
check(receipt.maps.FULL.accuracy==="1/1"&&receipt.maps.FULL.brier==="0/1","full exact");
const labels="schedule_id,schedule_code,origin,target,reachable,arrival\n"+
 rows.map(r=>[r.schedule_id,r.schedule_code,r.origin,r.target,r.reachable,r.arrival===null?"":r.arrival].join(",")).join("\n")+"\n";
if(process.argv[2]==="--emit"){
 let dir=process.argv[3];check(dir,"output directory");fs.mkdirSync(dir,{recursive:true});
 fs.writeFileSync(dir+"/R317_S113_ALL_162_DIRECTED_LABELS.csv",labels);
 fs.writeFileSync(dir+"/R317_S113_OBSERVATION_MAPS_EXACT.json",JSON.stringify(receipt,null,2)+"\n");
}
console.log(JSON.stringify(receipt,null,2));
