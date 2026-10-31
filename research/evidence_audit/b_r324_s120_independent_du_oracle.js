#!/usr/bin/env node
"use strict";
// Independent nonblind D/U multiplicity oracle for R324 S120, no R import.
const W=[[3,1],[1,3],[1,1],[2,2]],M=[1,2,1],P=["state_only","exact_score","threshold_ge_4","compare_dread","compare_unknown","compare_both"],N=["dread_weighted","unknown_weighted","balanced","scaled_balanced"];
const sign=x=>x>0?1:x<0?-1:0,gcd=(a,b)=>b?gcd(b,a%b):a,frac=(a,b)=>{const g=gcd(a,b);return b/g===1?String(a/g):a/g+"/"+b/g;},v=(d,u,w)=>d*w[0]+u*w[1];
function obs(p,d,u,w){const x=v(d,u,w);switch(p){case "state_only":return "S";case "exact_score":return "V"+x;case "threshold_ge_4":return "T"+Number(x>=4);case "compare_dread":return "D"+sign(x-2*w[0]);case "compare_unknown":return "U"+sign(x-2*w[1]);case "compare_both":return "B"+sign(x-2*w[0])+","+sign(x-2*w[1]);default:throw Error("unknown policy");}}
function independent(){
 const policies=P.map(policy=>{let n=0;for(let d=0;d<3;d++)for(let u=0;u<3;u++)n+=M[d]*M[u]*new Set(W.map(w=>obs(policy,d,u,w))).size;return {policy,observation_groups:n,accuracy:frac(n,64),accuracy_numerator:n,accuracy_denominator:64};});
 const pts=[];for(let d=0;d<3;d++)for(let u=0;u<3;u++)pts.push([d,u]);
 const profiles=W.map(w=>pts.flatMap(([d,u])=>pts.map(([e,f])=>sign(v(d,u,w)-v(e,f,w)))).join(",")),unique=[...new Set(profiles)];
 return {policies,distinct_profiles:unique.length,profile_groups:profiles.map(x=>unique.indexOf(x)),w2w3_rank:profiles[2]===profiles[3],w2w3_diff:pts.reduce((s,[d,u])=>s+M[d]*M[u]*Number(v(d,u,W[2])!==v(d,u,W[3])),0)};
}
function audit(original,csv,receipt){
 const a=original.trimEnd().split(/\r?\n/),b=csv.trimEnd().split(/\r?\n/);
 if(a.length!==65||a[0]!=="world_id,policy,dread1,dread2,unknown1,unknown2,weight,D,U,score"||b.length!==65||b[0]!=="world_id,state,D,U,score,threshold_ge_4,compare_dread,compare_unknown")throw Error("coverage/header");
 const src=new Map();
 for(const line of a.slice(1)){const x=line.split(","),i=Number(x[0]),s=x.slice(2,6).join(""),d=Number(x[7]),u=Number(x[8]),z=Number(x[9]),k=i+":"+s;
  if(x.length!==10||src.has(k)||i<0||i>3||!/^[01]{4}$/.test(s)||x[1]!==N[i]||x[6]!=="1/16"||d!==Number(s[0])+Number(s[1])||u!==Number(s[2])+Number(s[3])||z!==v(d,u,W[i]))throw Error("source identity");
  src.set(k,{d,u,z});
 }
 if(src.size!==64)throw Error("source count");
 const seen=new Set();
 for(const line of b.slice(1)){const x=line.split(","),i=Number(x[0]),k=i+":"+x[1],s=src.get(k);
  if(x.length!==8||!s||seen.has(k))throw Error("result identity");seen.add(k);
  if(Number(x[2])!==s.d||Number(x[3])!==s.u||Number(x[4])!==s.z||Number(x[5])!==Number(s.z>=4)||Number(x[6])!==sign(s.z-2*W[i][0])||Number(x[7])!==sign(s.z-2*W[i][1]))throw Error("result arithmetic");
 }
 if(seen.size!==64)throw Error("result count");
 let j;try{j=JSON.parse(receipt)}catch(e){throw Error("receipt parse")}
 const exp=independent();
 if(j.schema!=="r324_s120_ordinal_observation_e1_v1"||j.evidence!=="E1_SYNTHETIC_ONLY"||j.source_original_blob!=="1b0062eeea020606a3d510d566da43db03ace8d9"||j.frozen_protocol_commit!=="dc2bc2ad22a0130984cf0ecb497c2c54f04803f8"||j.original_catalogue_id!=="01-017"||j.world_count!==4||j.state_count!==16||j.atom_count!==64||j.atom_mass!=="1/64")throw Error("metadata");
 if(JSON.stringify(j.policies)!==JSON.stringify(exp.policies))throw Error("policy mismatch");
 if(j.full_ordinal_profile.distinct_profiles!==exp.distinct_profiles||j.full_ordinal_profile.accuracy!==frac(exp.distinct_profiles,4)||JSON.stringify(j.full_ordinal_profile.profile_groups)!==JSON.stringify(exp.profile_groups))throw Error("profile mismatch");
 if(j.witnesses.w2_w3_identical_weak_rank!==exp.w2w3_rank||j.witnesses.w2_w3_exact_score_differ_count!==exp.w2w3_diff)throw Error("witness mismatch");
 if(j.human_E2!=="NOT_ESTABLISHED"||j.historical_E3!=="NOT_ESTABLISHED"||j.external_independent_replication!=="NOT_RUN")throw Error("evidence overclaim");
 return {status:"PASS_NONBLIND_INTERNAL_E1",source_rows:64,verified_rows:64,policy_cells:6,profile_groups:exp.distinct_profiles,independent:exp};
}
function mutations(original,csv,receipt){
 const lines=csv.trimEnd().split("\n"),j=JSON.parse(receipt),tests=[];
 const run=(name,c,r)=>{let rejected=false;try{audit(original,c,r)}catch(e){rejected=true}tests.push({name,rejected})};
 run("missing_atom",lines.slice(0,-1).join("\n")+"\n",receipt);
 run("duplicate_atom",[...lines,lines[1]].join("\n")+"\n",receipt);
 for(const [name,row,col,f] of [["score_tamper",3,4,x=>Number(x)+1],["threshold_tamper",7,5,x=>1-Number(x)],["comparison_tamper",9,6,x=>Number(x)+1],["world_tamper",9,0,x=>3]]){
  const a=lines.slice(),x=a[row].split(",");x[col]=String(f(x[col]));a[row]=x.join(",");run(name,a.join("\n")+"\n",receipt);
 }
 const clone=()=>JSON.parse(JSON.stringify(j));
 const j7=clone();j7.policies[1].accuracy="1";run("accuracy_tamper",csv,JSON.stringify(j7));
 const j8=clone();j8.full_ordinal_profile.profile_groups=[0,1,2,3];run("profile_tamper",csv,JSON.stringify(j8));
 const j9=clone();j9.human_E2="PASS";run("evidence_overclaim",csv,JSON.stringify(j9));
 if(tests.length!==9||tests.some(t=>!t.rejected))throw Error("mutation false acceptance");
 return tests;
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
 const o=fs.readFileSync(path.join(root,"research/R324/R324_ALL_64_ARTIFICIAL_RISK_STATES.csv"),"utf8");
 const c=fs.readFileSync(path.join(root,"research/validation/R324_S120_64_ATOM_ORDINAL_OBSERVATIONS.csv"),"utf8");
 const j=fs.readFileSync(path.join(root,"research/validation/R324_S120_EXACT_OBSERVATION_RESULTS.json"),"utf8");
 console.log(JSON.stringify({audit:audit(o,c,j),mutations:mutations(o,c,j)},null,2));
}