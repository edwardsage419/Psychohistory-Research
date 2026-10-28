"use strict";
// R247 S43 B route. Independent source counting, no calls to the R route.
const fs = typeof require==="function" ? require("fs") : null;
const PREFIXES=["F0","F1","F2","F12"];
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero");const g=gcd(n,d);return [n/g,d/g];}
function plus(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function txt(q){return q[1]===1n?String(q[0]):q[0]+"/"+q[1];}
function key(a,b,f){if(f==="F0")return "all";if(f==="F1")return String(a);if(f==="F2")return String(b);return a+","+b;}
function compute(csv,reference=null){
 const lines=csv.trim().split(/\r?\n/);const hdr=lines.shift().split(",");const ix={};hdr.forEach((x,i)=>ix[x]=i);
 for(const x of ["world","oracle_hidden_environment_U","observed_generation_size_Y1","observed_generation_size_Y2","observed_generation_size_Y3","oracle_true_hidden_generation_H3","original_complete_source_probability",...Array.from({length:7},(_,i)=>"oracle_original_node_bit_B"+i)])if(ix[x]===undefined)throw Error("missing column "+x);
 const by={};for(const line of lines){const a=line.split(",");(by[a[ix.world]]??=[]).push(a);}
 if(Object.keys(by).length!==9||lines.length!==2304)throw Error("source universe");
 const receipt={research_id:"R247",study:"S43",evidence:"E1_SYNTHETIC",source_blob:"42de5332f4aafae65487a71f03fc0dce5beb59df",original_rows:lines.length,results:{},checks:0};
 for(const [world,rows] of Object.entries(by)){
  if(rows.length!==256)throw Error("source count");const keys=new Set();
  for(const a of rows){
   if(a[ix.original_complete_source_probability]!=="1/256")throw Error("weight");
   const bits=[a[ix.oracle_hidden_environment_U],...Array.from({length:7},(_,i)=>a[ix["oracle_original_node_bit_B"+i]])];
   if(bits.some(x=>x!=="0"&&x!=="1"))throw Error("bit");keys.add(bits.join(""));
   if(world==="STATIC_HIDDEN_TREE_SENSOR_ALIAS"&&a[ix.oracle_true_hidden_generation_H3]!=="0")throw Error("hidden alias");
   receipt.checks++;
  }
  if(keys.size!==256)throw Error("duplicate exogenous bits");receipt.checks++;
  const row={};
  for(const f of PREFIXES){
   const counts=new Map();
   for(const a of rows){const y1=Number(a[ix.observed_generation_size_Y1]),y2=Number(a[ix.observed_generation_size_Y2]),t=Number(a[ix.observed_generation_size_Y3])>0?1:0;
    const k=key(y1,y2,f),pair=counts.get(k)||[0,0];pair[0]++;pair[1]+=t;counts.set(k,pair);}
   let risk=frac(0n);for(const [m,s] of counts.values())risk=plus(risk,frac(BigInt(s)*BigInt(m-s),256n*BigInt(m)));
   row[f]={risk:txt(risk),support:counts.size};receipt.checks++;
  }
  receipt.results[world]=row;
 }
 if(JSON.stringify(receipt.results.IID_FAIR_0_OR_2)!==JSON.stringify(receipt.results.STATIC_HIDDEN_TREE_SENSOR_ALIAS))throw Error("alias");
 receipt.checks++;
 let comparisons=0;
 if(reference){
  for(const [world,record] of Object.entries(reference.results)){if(!receipt.results[world])throw Error("missing world");
   for(const f of PREFIXES)for(const field of ["risk","support"]){comparisons++;if(record[f][field]!==receipt.results[world][f][field])throw Error("independent mismatch "+world+" "+f+" "+field);}}
 }
 receipt.comparisons=comparisons;
 if(reference){const corrupted=JSON.parse(JSON.stringify(reference));corrupted.results.IID_FAIR_0_OR_2.F12.risk="999";
  receipt.mutation_rejected=corrupted.results.IID_FAIR_0_OR_2.F12.risk!==receipt.results.IID_FAIR_0_OR_2.F12.risk;if(!receipt.mutation_rejected)throw Error("mutation");}
 receipt.future_target_leakage_negative_control="ILLEGAL_RISK_ZERO";receipt.external_replication=0;return receipt;
}
if(typeof module!=="undefined")module.exports={compute};
if(typeof require==="function"&&require.main===module){
 const src=process.argv[2]||"research/R247/R247_ALL_2304_ORIGINAL_BINARY_TREE_FAMILY_SOURCES.csv";
 const ref=process.argv[3]?JSON.parse(fs.readFileSync(process.argv[3],"utf8")):null;
 process.stdout.write(JSON.stringify(compute(fs.readFileSync(src,"utf8"),ref),null,2)+"\n");
}
