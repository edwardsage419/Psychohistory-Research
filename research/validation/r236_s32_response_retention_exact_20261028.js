"use strict";
// R236 S32. Input CSV is the fixed R236 576-row artificial source archive.
// Independent B route uses only R236's frozen observable joint JSON.
function run(csvText,base) {
 const cols=csvText.trim().split(/\r?\n/), hdr=cols[0].split(",");
 const rows=cols.slice(1).map(line=>Object.fromEntries(line.split(",").map((v,i)=>[hdr[i],v])));
 const worlds=base.world_results.map(x=>x.world);
 const rules=["ALL","Y1_POS_HALF","Y1_NEG_HALF","R1_POS_HALF","R1_NEG_HALF","PROXY_P_MISSING_HALF"];
 const obs=["observed_mode_R","observed_prior_proxy_P","observed_prior_proxy_Z","observed_report_Y1","observed_report_Y2"];
 function weight(r,p,y,rule){
  if(rule==="ALL")return 2;
  if(rule==="Y1_POS_HALF")return y===1?1:2;
  if(rule==="Y1_NEG_HALF")return y===0?1:2;
  if(rule==="R1_POS_HALF")return r===1&&y===1?1:2;
  if(rule==="R1_NEG_HALF")return r===1&&y===0?1:2;
  if(rule==="PROXY_P_MISSING_HALF")return p===-1?1:2;
  throw Error("unknown rule");
 }
 function gcd(a,b){while(b){const z=a%b;a=b;b=z;}return a;}
 function frac(n,d){if(!d)throw Error("zero denominator");const g=gcd(Math.abs(n),Math.abs(d));n/=g;d/=g;return d===1?String(n):n+"/"+d;}
 function fromString(s){const a=s.split("/").map(Number);return a.length===1?[a[0],1]:a;}
 function sumObj(m,k,v){m[k]=(m[k]||0)+v;}
 function fromRows(world,rule){
  const j={},g=[0,0],y=[0,0],subset=rows.filter(x=>x.world===world);
  if(subset.length!==64)throw Error("source count "+world);
  for(const x of subset){
   if(x.original_probability!=="1/64")throw Error("source mass");
   const [r,p,z,yy,yyy]=obs.map(k=>Number(x[k]));
   const w=weight(r,p,yy,rule);
   sumObj(j,[r,p,z,yy,yyy].join(","),w);g[r]+=w;y[r]+=w*yy;
  }
  const total=g[0]+g[1];
  if(!g[0]||!g[1])throw Error("empty mode group");
  return {total,groups:g,success:y,joint:j,itt:frac(y[1]*g[0]-y[0]*g[1],g[0]*g[1])};
 }
 function fromJoint(baseWorld,rule){
  const j={},g=[0,0],y=[0,0];
  for(const [key,pstr] of Object.entries(baseWorld.complete_observed_mode_proxy_and_two_question_joint)){
   const [n,d]=fromString(pstr);
   if(64*n%d)throw Error("source denominator not 64");
   const count=64*n/d, v=key.split(",").map(Number),w=weight(v[0],v[1],v[3],rule);
   const mass=count*w;
   sumObj(j,key,mass);g[v[0]]+=mass;y[v[0]]+=mass*v[3];
  }
  return {total:g[0]+g[1],groups:g,success:y,joint:j,itt:frac(y[1]*g[0]-y[0]*g[1],g[0]*g[1])};
 }
 let checks=0, conditions=[], allByWorld={};
 for(const bw of base.world_results){
  const world=bw.world;allByWorld[world]={};
  for(const rule of rules){
   const a=fromRows(world,rule),b=fromJoint(bw,rule);
   if(a.total!==b.total||a.groups.join()!=b.groups.join()||a.success.join()!=b.success.join()||a.itt!==b.itt)throw Error("route mismatch "+world+" "+rule);
   checks+=4;
   const keys=new Set([...Object.keys(a.joint),...Object.keys(b.joint)]);
   for(const k of keys){if((a.joint[k]||0)!==(b.joint[k]||0))throw Error("joint mismatch "+world+" "+rule+" "+k);checks++;}
   if(Object.values(a.joint).reduce((s,n)=>s+n,0)!==a.total)throw Error("normalization");checks++;
   if(rule==="ALL"&&a.itt!==bw.observed_mode_R_ITT_on_report_Y1)throw Error("original ITT regression");if(rule==="ALL")checks++;
   if(rule==="PROXY_P_MISSING_HALF"&&a.itt!==bw.observed_mode_R_ITT_on_report_Y1)throw Error("proxy negative control");if(rule==="PROXY_P_MISSING_HALF")checks++;
   const item={world,rule,retention_probability:frac(a.total,128),retained_mode_R0_probability:frac(a.groups[0],a.total),retained_mode_R1_probability:frac(a.groups[1],a.total),reported_ITT:a.itt,baseline_reported_ITT:bw.observed_mode_R_ITT_on_report_Y1,oracle_private_mode_effect:bw.oracle_mode_effect_on_current_private_B1,observable_joint_support:keys.size,observable_joint:Object.fromEntries([...keys].sort().map(k=>[k,frac(a.joint[k]||0,a.total)]))};
   conditions.push(item);allByWorld[world][rule]=item;
  }
 }
 const aliasPairs=[["TRUE_MODE_CHANGE","REPORT_MODE_CHANGE_ALIAS"],["TRUE_MODE_COMPLIER_ONLY","REPORT_MODE_COMPLIER_ONLY_ALIAS"],["SHARED_ACQUIESCENCE_RESPONSE","SHARED_TRUE_CONSTRUCT_ALIAS"]];
 for(const [a,b] of aliasPairs)for(const rule of rules){
  if(JSON.stringify(allByWorld[a][rule].observable_joint)!==JSON.stringify(allByWorld[b][rule].observable_joint))throw Error("alias broken");checks++;
 }
 const stable=allByWorld.TRUTHFUL_STABLE;
 if(stable.R1_POS_HALF.reported_ITT!=="-1/6"||stable.R1_NEG_HALF.reported_ITT!=="1/6")throw Error("negative control failed");checks+=2;
 const tampered=JSON.parse(JSON.stringify(stable.R1_POS_HALF));tampered.reported_ITT="999";
 const detected=tampered.reported_ITT!==fromJoint(base.world_results[0],"R1_POS_HALF").itt;
 if(!detected)throw Error("mutation undetected");checks++;
 return {research_id:"R236",supplement:"S32",date:"2026-10-28",prescore_protocol_commit:"e891710fb2013a3cfe566cb73bcde7acc5d7e239",input_source_blob:"c612b226c3db493e1c8dd96f16eff68b98f8704c",input_results_blob:"00e0d819816062964e629b1da49d4d5f065a5257",source_rows:rows.length,worlds:worlds.length,rules,conditions_count:conditions.length,exact_checks:checks,failed_checks:0,mutation_detected:detected,conditions,scope:"E1 artificial exact only; no real E2/E3 or external replication"};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 if(process.argv.length!==5)throw Error("usage: node script.js ORIGINAL.csv R236_EXACT_RESULTS.json output.json");
 const result=run(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));
 fs.writeFileSync(process.argv[4],JSON.stringify(result,null,2)+"\n");
 console.log(JSON.stringify({conditions:result.conditions_count,checks:result.exact_checks,failed:result.failed_checks}));
}
