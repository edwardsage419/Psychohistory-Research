"use strict";
/* B independent audit of R234 S30. Reads original R234 observable joint
   and S30 archived receipt. Does not use S30 source enumeration. */
const rules={
 ALL:x=>true,
 BASELINE_ITEM1_POS:x=>x[0]>0,
 FOLLOWUP_ITEM1_POS:x=>x[3]>0,
 FOLLOWUP_ITEM1_NONNEG:x=>x[3]>=0,
 FOLLOWUP_COMPOSITE_GAIN_POS:x=>x[3]+x[4]+x[5]>x[0]+x[1]+x[2]
};
function rational(n,d){if(!d)return null;let a=Math.abs(n),b=d;while(b){let c=a%b;a=b;b=c}let g=a||1;return d/g===1?String(n/g):n/g+"/"+d/g}
function audit(baseText,receiptText){
 const base=JSON.parse(baseText),receipt=JSON.parse(receiptText),checks={n:0};
 const verify=(a,b,what)=>{checks.n++;if(a!==b)throw Error(what+" mismatch: "+a+" / "+b)};
 const worldMap=new Map(receipt.world_results.map(x=>[x.world,x.selection_results]));
 const alias=new Map();
 for(const world of base.world_results){
  const entries=Object.entries(world.exact_full_paired_observed_joint).map(([k,v])=>{const [a,b="1"]=v.split("/").map(Number),n=256*a/b;if(!Number.isInteger(n))throw Error("invalid source mass");return {k,x:k.split(",").map(Number),n}});
  verify(entries.reduce((a,b)=>a+b.n,0),256,"baseline mass");
  const saved=worldMap.get(world.world);if(!saved)throw Error("world missing");
  alias.set(world.world,{});
  for(const [name,keep] of Object.entries(rules)){
   let n=0,support=0,totals=[0,0,0,0,0,0],selected=[];
   for(const entry of entries)if(keep(entry.x)){n+=entry.n;support++;selected.push(entry.k+":"+entry.n);for(let j=0;j<6;j++)totals[j]+=entry.x[j]*entry.n}
   const record=saved[name];verify(record.selected,n,"selection count");verify(record.retention,rational(n,256),"retention");
   verify(record.support,support,"joint support");
   for(let j=0;j<6;j++)verify(record.observed_means[j],rational(totals[j],n),"six mean");
   for(let j=0;j<3;j++)verify(record.observed_item_change[j],rational(totals[j+3]-totals[j],n),"three changes");
   verify(record.observed_composite_change,rational(totals[3]+totals[4]+totals[5]-totals[0]-totals[1]-totals[2],3*n),"composite");
   alias.get(world.world)[name]=selected.sort().join("|");
  }
 }
 for(const [a,b] of [["TRUE_LATENT_SHIFT","UNIFORM_INTERCEPT_DRIFT_ALIAS"],["STABLE_BASE","LATENT_SCALE_REANCHOR_ALIAS"]])for(const name of Object.keys(rules))verify(alias.get(a)[name],alias.get(b)[name],"alias");
 let fault=false;try{verify("1/3","2/3","injected mean")}catch(e){fault=true}if(!fault)throw Error("negative control escaped");
 return {audit:"B_R234_S30_INDEPENDENT_OBSERVABLE_JOINT_MOMENT",source:"R234 original archived six-variable joint only",conditions:45,checks:checks.n,failed_checks:0,fault_injection_detected:fault,oracle_true_change_independently_verified:false,external_independent_replications:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");const a=fs.readFileSync(path.join(root,"research/R234/R234_EXACT_RESULTS.json"),"utf8"),b=fs.readFileSync(path.join(root,"research/validation/R234_S30_OBSERVED_ATTRITION_45_CONDITION_RECEIPT_2026-10-28.json"),"utf8");process.stdout.write(JSON.stringify(audit(a,b),null,2)+"\n")}
if(typeof module!=="undefined")module.exports={audit};
