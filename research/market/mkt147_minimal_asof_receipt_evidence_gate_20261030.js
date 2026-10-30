"use strict";
// Synthetic historical audit receipts. Version labels are not cryptographic proof.
const must=(v,m)=>{if(!v)throw Error(m)};
const bad=f=>{try{f()}catch(_){return true}return false};
function aggregate(rows,priority){
  if(!Array.isArray(rows)||!rows.length||!["A","B"].includes(priority))throw Error("bad input");
  const cells=new Map();
  for(const r of rows){
    if(!["A","B"].includes(r.origin)||!Number.isInteger(r.start)||!Number.isInteger(r.end)||
       r.start<0||r.end<=r.start||!Number.isSafeInteger(r.rate)||r.rate<0)throw Error("bad row");
    for(let t=r.start;t<r.end;t++){
      const cell=cells.get(t)||{};
      if(Object.hasOwn(cell,r.origin))throw Error("duplicate source-minute");
      cell[r.origin]=r.rate;cells.set(t,cell);
    }
  }
  let total=0;
  for(const cell of cells.values())total+=cell[priority]===undefined?cell[priority==="A"?"B":"A"]:cell[priority];
  if(!Number.isSafeInteger(total))throw Error("unsafe total");
  return total;
}
const fields=["snapshot_id","source_version","rule_version","priority","window",
 "asof_utc","algorithm_version","permission_complete","source_complete"];
function receipt(rows,m){
  if(!m||fields.some(k=>!Object.hasOwn(m,k)))throw Error("missing field");
  for(const k of fields.slice(0,3).concat(["window","asof_utc","algorithm_version"]))
    if(typeof m[k]!=="string"||!m[k])throw Error("bad label");
  if(m.window!=="0:20"||m.algorithm_version!=="synthetic-minute-priority-v1"||
     !["A","B"].includes(m.priority)||typeof m.permission_complete!=="boolean"||
     typeof m.source_complete!=="boolean")throw Error("bad metadata");
  return Object.freeze({...m,aggregate_value:aggregate(rows,m.priority)});
}
function assess(r,context){
  if(!r||fields.some(k=>r[k]===undefined||r[k]===null)||
     !Number.isSafeInteger(r.aggregate_value)||r.aggregate_value<0)
    return {status:"ABSTAIN",reason:"incomplete receipt"};
  if(r.permission_complete!==true||r.source_complete!==true)
    return {status:"ABSTAIN",reason:"incomplete source/permission"};
  if(r.window!=="0:20"||r.algorithm_version!=="synthetic-minute-priority-v1"||
     !["A","B"].includes(r.priority))return {status:"ABSTAIN",reason:"unsupported rule"};
  if(!context||!context.rows)return {status:"CLAIM_ONLY",reason:"no original data"};
  for(const k of fields.slice(0,7))
    if(context[k]!==r[k])return {status:"FAIL",reason:"context mismatch "+k};
  let value;try{value=aggregate(context.rows,r.priority)}
  catch(_){return {status:"FAIL",reason:"invalid source"}}
  return value===r.aggregate_value?{status:"CONSISTENT_INTERNAL",value}:
    {status:"FAIL",reason:"aggregate mismatch"};
}
function run(){
  let tests=0;const ck=(v,m)=>{must(v,m);tests++};
  const w1=[{origin:"A",start:0,end:10,rate:100},{origin:"A",start:10,end:20,rate:50},
    {origin:"B",start:0,end:10,rate:80}];
  const w2=[{origin:"A",start:0,end:10,rate:200},{origin:"A",start:10,end:20,rate:50},
    {origin:"B",start:0,end:10,rate:80}];
  const w3=[{origin:"A",start:0,end:10,rate:100},{origin:"A",start:10,end:20,rate:50},
    {origin:"B",start:0,end:10,rate:90}];
  const m={snapshot_id:"s0",source_version:"d1",rule_version:"p2",priority:"B",
    window:"0:20",asof_utc:"2026-10-30T00:00:00Z",
    algorithm_version:"synthetic-minute-priority-v1",permission_complete:true,source_complete:true};
  const c1=receipt(w1,m),c2=receipt(w2,{...m,source_version:"d2"});
  const h1=receipt(w1,{...m,priority:"A",rule_version:"p1"});
  const h2=receipt(w2,{...m,priority:"A",rule_version:"p1",source_version:"d2"});
  ck(c1.aggregate_value===1300,"current world1");
  ck(c2.aggregate_value===1300,"current world2");
  ck(h1.aggregate_value===1500,"historical world1");
  ck(h2.aggregate_value===2500,"historical world2");
  ck(h2.aggregate_value-h1.aggregate_value===1000,"hidden historical difference");
  ck(!Object.hasOwn(c1,"rows"),"receipt excludes raw rows");
  ck(!Object.hasOwn(c1,"records"),"receipt excludes raw records");
  ck(assess(c1).status==="CLAIM_ONLY","receipt alone");
  ck(assess(h1).status==="CLAIM_ONLY","historical receipt alone");
  ck(assess(c1,{...m,rows:w1}).status==="CONSISTENT_INTERNAL","full original data");
  ck(assess(c2,{...m,source_version:"d2",rows:w2}).status==="CONSISTENT_INTERNAL","second source");
  ck(assess(c1,{...m,rows:w2}).status==="CONSISTENT_INTERNAL","same total cannot expose source change");
  ck(assess(c1,{...m,rows:w3}).status==="FAIL","changed aggregate detected");
  ck(assess(c1,{...m,rule_version:"p1",rows:w1}).status==="FAIL","rule mismatch");
  ck(assess(c1,{...m,source_version:"d2",rows:w1}).status==="FAIL","source mismatch");
  ck(assess(c1,{...m,window:"10:20",rows:w1}).status==="FAIL","window mismatch");
  ck(assess({...c1,permission_complete:false},{...m,rows:w1}).status==="ABSTAIN","permission missing");
  ck(assess({...c1,source_complete:false},{...m,rows:w1}).status==="ABSTAIN","source missing");
  ck(assess({...c1,rule_version:null},{...m,rows:w1}).status==="ABSTAIN","rule absent");
  ck(assess({...c1,aggregate_value:-1},{...m,rows:w1}).status==="ABSTAIN","bad total");
  ck(assess({...c1,aggregate_value:1301},{...m,rows:w1}).status==="FAIL","total tampered");
  ck(bad(()=>receipt(w1,{...m,source_version:undefined})),"invalid source version");
  ck(bad(()=>receipt(w1,{...m,priority:"X"})),"invalid priority");
  ck(bad(()=>aggregate([{origin:"A",start:0,end:1,rate:1},{origin:"A",start:0,end:1,rate:2}],"A")),"duplicate");
  ck(bad(()=>aggregate([{origin:"A",start:0,end:1,rate:-1}],"A")),"negative");
  return {tests,current_B:1300,historical_A:[1500,2500],receipt_without_raw:"CLAIM_ONLY",
    identical_total_different_raw:"UNDETECTABLE_WITH_THIS_RECEIPT",cryptographic_proof:"NOT_TESTED"};
}
if(typeof module!=="undefined")module.exports={aggregate,receipt,assess,run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
