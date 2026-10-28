"use strict";
const OBS=["observed_X01","observed_X02","observed_X03","observed_X11","observed_X12","observed_X13"];
const RULES={ALL:x=>true,BASELINE_ITEM1_POS:x=>x[0]>0,FOLLOWUP_ITEM1_POS:x=>x[3]>0,FOLLOWUP_ITEM1_NONNEG:x=>x[3]>=0,FOLLOWUP_COMPOSITE_GAIN_POS:x=>x[3]+x[4]+x[5]>x[0]+x[1]+x[2]};
function f(n,d){if(!d)return null;let a=Math.abs(n),b=d;while(b){const t=a%b;a=b;b=t}const g=a||1;return d/g===1?String(n/g):n/g+"/"+d/g}
function assertEq(a,b,s,c){c.n++;if(a!==b)throw Error(s+": "+a+" vs "+b)}
function bcount(s){const [a,b="1"]=s.split("/").map(Number),n=256*a/b;if(!Number.isInteger(n))throw Error("noninteger mass");return n}
function aggregate(m,rule){const q=new Map(),s=[0,0,0,0,0,0];let n=0;for(const [k,v] of m){const x=k.split(",").map(Number);if(rule(x)){q.set(k,v);n+=v;for(let i=0;i<6;i++)s[i]+=v*x[i]}}return {q,n,means:s.map(x=>f(x,n)),changes:[0,1,2].map(i=>f(s[i+3]-s[i],n)),composite:f(s[3]+s[4]+s[5]-s[0]-s[1]-s[2],3*n)}}
function run(csv,json){
 const c={n:0},lines=csv.trim().split(/\r?\n/),head=lines.shift().split(","),idx=Object.fromEntries(head.map((v,i)=>[v,i])),groups=new Map();
 for(const line of lines){const row=line.split(","),w=row[idx.world];if(!groups.has(w))groups.set(w,[]);groups.get(w).push(row)}
 const baseline=JSON.parse(json),world_results=[],alias={};assertEq(lines.length,2304,"source rows",c);assertEq(groups.size,9,"world count",c);
 for(const w of baseline.world_results){
  const rows=groups.get(w.world),joint=new Map(Object.entries(w.exact_full_paired_observed_joint).map(([k,v])=>[k,bcount(v)]));assertEq(rows.length,256,"rows",c);assertEq([...joint.values()].reduce((a,b)=>a+b,0),256,"mass",c);
  const result={};alias[w.world]={};
  for(const [name,rule] of Object.entries(RULES)){
   const selected=rows.filter(r=>rule(OBS.map(k=>Number(r[idx[k]])))),rmap=new Map(),sum=[0,0,0,0,0,0];let oracle=0;
   for(const r of selected){const x=OBS.map(k=>Number(r[idx[k]])),key=x.join(",");rmap.set(key,(rmap.get(key)||0)+1);for(let i=0;i<6;i++)sum[i]+=x[i];oracle+=Number(r[idx.oracle_true_individual_latent_change])}
   const b=aggregate(joint,rule),n=selected.length;assertEq(n,b.n,"selected mass",c);
   if(!n){result[name]={status:"EMPTY_SUPPORT"};continue}
   assertEq(rmap.size,b.q.size,"support",c);for(const [k,v] of rmap)assertEq(v,b.q.get(k),"joint",c);
   for(let i=0;i<6;i++)assertEq(f(sum[i],n),b.means[i],"mean",c);
   for(let i=0;i<3;i++)assertEq(f(sum[i+3]-sum[i],n),b.changes[i],"change",c);
   assertEq(f(sum[3]+sum[4]+sum[5]-sum[0]-sum[1]-sum[2],3*n),b.composite,"composite",c);
   result[name]={status:"OK",selected:n,retention:f(n,256),support:rmap.size,observed_means:b.means,observed_item_change:b.changes,observed_composite_change:b.composite,oracle_true_latent_change_mean:f(oracle,n)};
   alias[w.world][name]=JSON.stringify([...b.q.entries()].sort((a,b)=>a[0].localeCompare(b[0])));
  }
  world_results.push({world:w.world,selection_results:result});
 }
 const pairs=[["TRUE_LATENT_SHIFT","UNIFORM_INTERCEPT_DRIFT_ALIAS"],["STABLE_BASE","LATENT_SCALE_REANCHOR_ALIAS"]];
 for(const [a,b] of pairs)for(const name of Object.keys(RULES))assertEq(alias[a][name],alias[b][name],"alias",c);
 const stable=world_results.find(x=>x.world==="STABLE_BASE").selection_results.FOLLOWUP_ITEM1_POS;
 assertEq(stable.observed_item_change[0],"1","stable selection artifact",c);assertEq(stable.oracle_true_latent_change_mean,"0","stable true change",c);
 let caught=false;try{assertEq(1,2,"injected corruption",c)}catch(e){caught=true}if(!caught)throw Error("failed fault injection");
 return {research_id:"R234",stage:"S30",scope:"E1_ARTIFICIAL",original_source_rows:2304,worlds:9,selection_rules:Object.keys(RULES),conditions:45,exact_checks:c.n,failed_checks:0,fault_injection_detected:caught,empty_support:world_results.flatMap(w=>Object.entries(w.selection_results).filter(([k,v])=>v.status==="EMPTY_SUPPORT").map(([k])=>w.world+"/"+k)),observational_alias_pairs:pairs,world_results,external_independent_replications:0,new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");const csv=fs.readFileSync(path.join(root,"research/R234/R234_ALL_2304_ORIGINAL_TWO_WAVE_SOURCES.csv"),"utf8"),json=fs.readFileSync(path.join(root,"research/R234/R234_EXACT_RESULTS.json"),"utf8");process.stdout.write(JSON.stringify(run(csv,json),null,2)+"\n")}
if(typeof module!=="undefined")module.exports={run};
