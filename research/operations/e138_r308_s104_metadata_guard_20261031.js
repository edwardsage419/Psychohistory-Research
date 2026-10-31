#!/usr/bin/env node
"use strict";
// R308 S104 supplemental receipt metadata guard. Standard Node.js only.
// Usage: node e138_r308_s104_metadata_guard_20261031.js <archived.csv> <archived.json>
const fs=require("node:fs");
const assert=require("node:assert/strict");
const COLS=["pattern","aggregation","B_num6","c_half","w_half","r_half","S0_A_num48","S1_Ac_num48","S1_Aw_num48","S1_Ar_num48","S2_Acw_num48","S2_Acr_num48","S2_Awr_num48"];
function parseCsv(s){
 const lines=s.trimEnd().split(/\r?\n/);
 assert.deepEqual(lines.shift().split(","),COLS);
 return lines.map(line=>{
  const parts=line.split(",");
  assert.equal(parts.length,COLS.length);
  return Object.fromEntries(COLS.map((k,i)=>[k,i<2?parts[i]:Number(parts[i])]));
 });
}
function verify(rows,d){
 assert.equal(d.schema,"R308_S104_E1_exact_integer_gate_observability_v1");
 assert.equal(d.freeze_path,"research/validation/R308_S104_GATE_OBSERVABILITY_PRESCORE_FREEZE_2026-10-31.md");
 assert.equal(d.freeze_commit,"e3d2b690a794d4fd3e748b43a59e71d56eda09cf");
 assert.deepEqual(d.schemes,["S0","S1","S2","S3"]);
 assert.equal(d.summary.worlds,432);
 assert.equal(d.summary.belief_groups,16);
 assert.equal(d.summary.zero_B_groups,6);
 assert.equal(d.summary.no_real_human_E2,0);
 assert.equal(d.summary.no_historical_E3,0);
 assert.deepEqual(d.summary.total_classes,[56,186,276,276]);
 assert.deepEqual(d.summary.singleton_worlds,[20,140,270,270]);
 assert.equal(rows.length,432);
 assert.equal(d.rows.length,432);
 assert.equal(d.groups.length,16);
 const keys=new Set();
 for(let i=0;i<432;i++){
  const r=rows[i],v=d.rows[i];
  for(const k of COLS)assert.equal(v[k],r[k]);
  const key=[r.pattern,r.aggregation,r.c_half,r.w_half,r.r_half].join("|");
  assert.ok(!keys.has(key));keys.add(key);
  const b=r.B_num6,c=r.c_half,w=r.w_half,t=r.r_half;
  const expect={S0_A_num48:b*c*w*t,S1_Ac_num48:b*2*w*t,S1_Aw_num48:b*c*2*t,
   S1_Ar_num48:b*c*w*2,S2_Acw_num48:b*4*t,S2_Acr_num48:b*4*w,S2_Awr_num48:b*4*c};
  for(const [k,x]of Object.entries(expect))assert.equal(r[k],x);
 }
 const sums=[0,1,2,3].map(i=>d.groups.reduce((s,g)=>s+g.classes[i],0));
 const single=[0,1,2,3].map(i=>d.groups.reduce((s,g)=>s+g.singleton_worlds[i],0));
 assert.deepEqual(sums,d.summary.total_classes);
 assert.deepEqual(single,d.summary.singleton_worlds);
 return {rows:432,algebra:3024,unique_keys:keys.size};
}
function main(){
 if(process.argv.length!==4)throw Error("Usage: node script.js archived.csv archived.json");
 const rows=parseCsv(fs.readFileSync(process.argv[2],"utf8"));
 const doc=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
 const baseline=verify(rows,doc);
 const cases=[
  ["schema",d=>d.schema="bad"],["freeze",d=>d.freeze_commit="bad"],
  ["freeze_path",d=>d.freeze_path="bad"],["schemes",d=>d.schemes.reverse()],
  ["summary_worlds",d=>d.summary.worlds=431],
  ["summary_E2",d=>d.summary.no_real_human_E2=1],
  ["summary_classes",d=>d.summary.total_classes[0]=55],
  ["duplicate_row",d=>d.rows[1]=d.rows[0]],
  ["row_math",d=>d.rows[100].S0_A_num48=-1],
  ["group_classes",d=>d.groups[2].classes[0]=999]
 ];
 for(const [name,mutate]of cases){
  const copy=JSON.parse(JSON.stringify(doc));mutate(copy);
  assert.throws(()=>verify(rows,copy),undefined,name);
 }
 console.log(JSON.stringify({baseline:"PASS",...baseline,mutations_rejected:cases.length,
  scope:"supplemental_nonblind_E1"}));
}
main();
