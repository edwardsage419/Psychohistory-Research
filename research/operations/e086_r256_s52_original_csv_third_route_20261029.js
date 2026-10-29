"use strict";
// Third-route exact Brier recomputation directly from the archived original CSV.
// Run at repo root: node research/operations/e086_r256_s52_original_csv_third_route_20261029.js
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict"),crypto=require("node:crypto");
const root=path.join(__dirname,"..");
const csvFile=path.join(root,"R256","R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_ATOMS.csv");
const receiptFile=path.join(root,"validation","R256_S52_EXACT_RECEIPT_2026-10-29.json");
const raw=fs.readFileSync(csvFile),csv=raw.toString("utf8"),receipt=JSON.parse(fs.readFileSync(receiptFile,"utf8"));
assert.equal(crypto.createHash("sha256").update(raw).digest("hex"),"8be5360465497321c15bffc554c7088fad48bcef71847e43e2ee2f714ed5119b");
const lines=csv.trimEnd().split("\n"),columns=lines[0].split(","),idx=Object.fromEntries(columns.map((x,i)=>[x,i]));
assert.equal(lines.length,4609);assert.equal(columns.length,44);
function gcd(a,b){while(b){const t=a%b;a=b;b=t}return a}
function add([a,b],[c,d]){const n=a*d+c*b,q=b*d,g=gcd(n,q);return[n/g,q/g]}
function fmt([a,b]){return b===1n?String(a):String(a)+"/"+String(b)}
const f=["F0","F1","F12","F123","F3"];
const key=[()=>"",r=>String(r.q[0]),r=>r.q.slice(0,2).join(""),r=>r.q.slice(0,3).join(""),r=>String(r.q[2])];
let checks=0,flow=0;const all={};
const verify=(condition,message)=>{checks++;assert.ok(condition,message)};
for(let wi=0;wi<9;wi++){
 const expected=receipt.results[wi],rows=[];
 for(let j=0;j<512;j++){
  const vals=lines[1+wi*512+j].split(",");
  assert.ok(vals.length===44&&vals[idx.world]===expected.world,"world/columns");
  let previous=0,q=[],reject=[];
  for(let t=1;t<=4;t++){
   const val=n=>Number(vals[idx[n+t]]);
   const a=val("oracle_exogenous_realized_offered_arrival_a"),d=val("oracle_model_served_d"),g=val("oracle_model_admitted_g"),r=val("oracle_model_rejected_r"),qt=val("observed_reported_queue_Q");
   verify(previous+a===qt+d+r,"conservation");verify(a===g+r,"arrival accounting");verify(qt>=0&&qt<=2,"capacity");
   q.push(qt);reject.push(r);previous=qt;flow++;
  }
  rows.push({q,y:reject[3]});checks++;
 }
 all[expected.world]=rows;
 verify(rows.reduce((s,r)=>s+r.y,0)===expected.event_count,"event count");
 const risks={};
 for(let fi=0;fi<5;fi++){
  const groups=new Map();
  for(const row of rows){const k=key[fi](row),v=groups.get(k)||[0,0];v[0]++;v[1]+=row.y;groups.set(k,v)}
  let risk=[0n,1n],mixed=0;
  for(const [n,k] of groups.values()){if(k>0&&k<n)mixed++;risk=add(risk,[BigInt(k*(n-k)),BigInt(512*n)])}
  risks[f[fi]]=risk;
  verify(fmt(risk)===expected.features[f[fi]].risk,"risk");
  verify(groups.size===expected.features[f[fi]].groups,"group count");
  verify(mixed===expected.features[f[fi]].mixed,"mixed groups");
 }
 for(const [a,b] of [["F0","F1"],["F1","F12"],["F12","F123"],["F0","F3"],["F3","F123"]])verify(risks[a][0]*risks[b][1]>=risks[b][0]*risks[a][1],"information monotonicity");
}
for(let i=0;i<512;i++){
 const a=all.BALANCED_INDEPENDENT_HALF_HALF[i],b=all.STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS[i];
 verify(a.y===b.y&&a.q.join(",")===b.q.join(","),"sensor alias");
}
console.log(JSON.stringify({checks,failures:0,rows:4608,flow_checks:flow,source_sha256:crypto.createHash("sha256").update(raw).digest("hex"),evidence:"INTERNAL_E1",original_receipt_source_status:"STALE_SEE_ADDENDUM"},null,2));
