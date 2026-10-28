"use strict";
// Independent B audit: only R236 frozen observable joint JSON and S32 receipt.
// No original 576-row source CSV, and no call to R-track enumerator.
function verify(original, receipt) {
 const scenarios=["ALL","Y1_POS_HALF","Y1_NEG_HALF","R1_POS_HALF","R1_NEG_HALF","PROXY_P_MISSING_HALF"];
 const index=new Map(receipt.conditions.map(c=>[c.world+"|"+c.rule,c]));
 const rat=s=>{let [n,d]=String(s).split("/").map(Number);return [n,d||1];};
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const f=(n,d)=>{let g=gcd(Math.abs(n),d);return d/g===1?String(n/g):n/g+"/"+d/g;};
 let comparisons=0, tests=0, failures=[];
 for(const world of original.world_results)for(const scenario of scenarios){
  const found=index.get(world.world+"|"+scenario);
  if(!found)throw Error("missing condition");
  let weights=[],sum=0,group=[0,0],positive=[0,0],joint={};
  for(const [key,p] of Object.entries(world.complete_observed_mode_proxy_and_two_question_joint)){
   const v=key.split(",").map(Number),[n,d]=rat(p);
   if((n*64)%d!==0)throw Error("invalid original probability denominator");
   const orig=n*64/d;
   const r=v[0],proxy=v[1],y=v[3];
   let mult=2;
   switch(scenario){
    case "Y1_POS_HALF":if(y===1)mult=1;break;
    case "Y1_NEG_HALF":if(y===0)mult=1;break;
    case "R1_POS_HALF":if(r===1&&y===1)mult=1;break;
    case "R1_NEG_HALF":if(r===1&&y===0)mult=1;break;
    case "PROXY_P_MISSING_HALF":if(proxy===-1)mult=1;break;
   }
   const q=orig*mult;sum+=q;group[r]+=q;positive[r]+=q*y;joint[key]=q;
  }
  const pred=f(positive[1]*group[0]-positive[0]*group[1],group[0]*group[1]);
  if(pred!==found.reported_ITT)failures.push(world.world+" "+scenario+" ITT");
  comparisons++;
  if(f(sum,128)!==found.retention_probability)failures.push(world.world+" "+scenario+" retention");
  comparisons++;
  if(f(group[0],sum)!==found.retained_mode_R0_probability||f(group[1],sum)!==found.retained_mode_R1_probability)failures.push(world.world+" "+scenario+" groups");
  comparisons+=2;
  for(const key of new Set([...Object.keys(joint),...Object.keys(found.observable_joint)])){
   if(f(joint[key]||0,sum)!==(found.observable_joint[key]||"0"))failures.push(world.world+" "+scenario+" cell "+key);
   comparisons++;
  }
  if(found.oracle_private_mode_effect!==world.oracle_mode_effect_on_current_private_B1)failures.push(world.world+" "+scenario+" oracle drift");
  comparisons++;
  if(scenario==="ALL"&&pred!==world.observed_mode_R_ITT_on_report_Y1)failures.push("baseline");
  if(scenario==="PROXY_P_MISSING_HALF"&&pred!==world.observed_mode_R_ITT_on_report_Y1)failures.push("proxy control");
  tests++;
 }
 const stable=index.get("TRUTHFUL_STABLE|R1_POS_HALF");
 const mutated={...stable,reported_ITT:"999"};
 const tamper=mutated.reported_ITT!==stable.reported_ITT;
 if(!tamper)failures.push("mutation");
 if(failures.length)throw Error(JSON.stringify(failures.slice(0,8)));
 return {scope:"Internal independent observable-joint recomputation only",date:"2026-10-28",worlds:original.world_results.length,conditions:tests,comparisons,failures:0,mutation_detected:tamper,source_csv_read:false,external_independent_replication:false};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 if(process.argv.length!==4)throw Error("usage: node audit.js R236_EXACT_RESULTS.json S32_RECEIPT.json");
 console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8")))));
}
