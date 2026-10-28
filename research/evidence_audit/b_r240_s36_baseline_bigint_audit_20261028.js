#!/usr/bin/env node
"use strict";
const fs=require("fs"),crypto=require("crypto"),path=require("path");
const BLOB="ea2dca9b93045e8c9765179e6b4e46dc82c0f267",RECEIPT_BLOB="2946e239550520cbbd0396c0a20620600ee9f50d";
function audit(base,receipt){
 let checks=0;const test=(x,m)=>{checks++;if(!x)throw Error("AUDIT_FAIL: "+m)};
 const gcd=(x,y)=>{while(y){const z=x%y;x=y;y=z}return x};
 const fraction=(a,b)=>{if(b===0n)return "UNDEFINED";const g=gcd(a<0n?-a:a,b);return (b/g===1n?String(a/g):String(a/g)+"/"+String(b/g))};
 const equivalent=(a,b)=>{if(a==="UNDEFINED"||b==="UNDEFINED")return a===b;const f=x=>{const [p,q="1"]=x.split("/");return [BigInt(p),BigInt(q)]};const [x,y]=f(a),[u,v]=f(b);return x*v===u*y};
 test(base.world_results.length===9,"nine worlds");test(receipt.results.length===36,"36 conditions");
 for(const world of base.world_results){
  const tab=world.observed_pair_table_2x2,raw=["00","01","10","11"].map(k=>BigInt(tab[k])),n=raw.reduce((a,b)=>a+b,0n);
  test(n===BigInt(world.observed_population_agreement_metrics.selected_source_units),"base n");
  for(const w of [1,2,4,8]){
   const item=receipt.results.find(v=>v.world===world.world&&v.weight_A1===w);test(!!item,"missing condition");
   const c=raw.map((x,i)=>i<2?x:x*BigInt(w)),W=c.reduce((a,b)=>a+b,0n),p=c[0]+c[3];
   const pe=(c[0]+c[1])*(c[0]+c[2])+(c[2]+c[3])*(c[1]+c[3]);
   test(BigInt(item.unweighted_complete_pair_source_types)===n,"n");
   for(let i=0;i<4;i++)test(BigInt(item.weighted_table_00_01_10_11[i])===c[i],"cell");
   test(BigInt(item.weighted_mass)===W,"W");
   test(equivalent(item.observed_agreement,fraction(p,W)),"Po");
   test(equivalent(item.independent_marginal_chance_agreement,fraction(pe,W*W)),"Pe");
   test(equivalent(item.cohens_kappa,fraction(p*W-pe,W*W-pe)),"kappa");
  }
 }
 const corrupt=JSON.parse(JSON.stringify(receipt));corrupt.results[0].weighted_table_00_01_10_11[0]++;
 let rejected=false;try{const x=corrupt.results[0],t=base.world_results.find(v=>v.world===x.world).observed_pair_table_2x2;if(x.weighted_table_00_01_10_11[0]!==t["00"])throw Error("injected mismatch")}catch{rejected=true}test(rejected,"negative control");
 return {study:"B_R240_S36",source_blob:BLOB,receipt_blob:RECEIPT_BLOB,conditions:36,exact_checks:checks,failed_checks:0,negative_control_detected:rejected,internal_procedural_audit:true,external_replication:false};
}
function read(f,sha){const bytes=fs.readFileSync(f),git=crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");if(git!==sha)throw Error("Git blob mismatch "+f);return JSON.parse(bytes.toString("utf8"))}
function main(){const a=read(process.argv[2]||path.join(__dirname,"../R240/R240_EXACT_RESULTS.json"),BLOB),b=read(process.argv[3]||path.join(__dirname,"../validation/R240_S36_CODER_A_REWEIGHT_EXACT_RECEIPT_2026-10-28.json"),RECEIPT_BLOB);console.log(JSON.stringify(audit(a,b),null,2))}
if(require.main===module)main();module.exports={audit};
