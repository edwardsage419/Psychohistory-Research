#!/usr/bin/env node
"use strict";
const fs=require("fs");

function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a||1}
function f(n,d=1){if(d<1)throw Error("denominator");let g=gcd(n,d);return d/g===1?String(n/g):n/g+"/"+d/g}
function v(s){let a=s.split("/").map(Number);return a[0]/(a[1]||1)}
function compute(csv){
 let lines=csv.trim().split(/\r?\n/),header=lines.shift().split(",");
 let rows=lines.map(s=>{let a=s.split(",");if(a.length!==header.length)throw Error("CSV");return Object.fromEntries(header.map((h,i)=>[h,a[i]]))});
 if(rows.length!==256)throw Error("source count");
 let worlds=[...new Set(rows.map(r=>r.world))],results=[];
 if(worlds.length!==8)throw Error("world count");
 for(let w of worlds){
  let rs=rows.filter(r=>r.world===w);
  if(rs.length!==32||rs.filter(r=>r.observed_group_G==="0").length!==16)throw Error("group counts");
  for(let r of rs)if(r.original_probability!=="1/32")throw Error("probability");
  for(let q of [0,1,2,4]){
   let mass=new Map();
   for(let r of rs){let g=Number(r.observed_group_G),x=[1,2,3].map(j=>Number(r["observed_X"+j]));
    for(let [h,k] of [[g,4-q],[1-g,q]]){if(!k)continue;let key=[h,...x].join(",");mass.set(key,(mass.get(key)||0)+k)}
   }
   let sorted=Object.fromEntries([...mass].sort((a,b)=>a[0].localeCompare(b[0])));
   let n=[0,0],s=[[0,0,0],[0,0,0]];
   for(let [key,k] of mass){let [h,...x]=key.split(",").map(Number);n[h]+=k;for(let j=0;j<3;j++)s[h][j]+=k*x[j]}
   if(n[0]!==64||n[1]!==64)throw Error("group mass");
   results.push({world:w,q:f(q,4),q_numerator_over_4:q,source_atoms:32,joint_mass_units_denominator:128,joint_mass_units:sorted,positive_joint_cells:mass.size,observed_group_mass_units:n,observed_mean_difference:[0,1,2].map(j=>f(s[1][j]-s[0][j],64))});
  }
 }
 for(let [a,b] of [["TRUE_LATENT_MEAN_SHIFT","INTERCEPT_SHIFT_ALIAS"],["FULL_STRICT_INVARIANT","LATENT_SCALE_ALIAS"]])for(let q of [0,1,2,4]){
  let x=results.find(z=>z.world===a&&z.q_numerator_over_4===q),y=results.find(z=>z.world===b&&z.q_numerator_over_4===q);
  if(JSON.stringify(x.joint_mass_units)!==JSON.stringify(y.joint_mass_units))throw Error("alias");
 }
 for(let w of worlds){let base=results.find(z=>z.world===w&&z.q_numerator_over_4===0).observed_mean_difference.map(v);
  for(let z of results.filter(z=>z.world===w))for(let j=0;j<3;j++)if(v(z.observed_mean_difference[j])!==base[j]*(1-z.q_numerator_over_4/2))throw Error("attenuation "+w+" "+z.q);
 }
 return {study:"R233_S29",scope:"E1_FINITE_ARTIFICIAL_GROUP_LABEL_MISCLASSIFICATION",protocol_commit:"879010bc5a6f0d1cfd47c646be21fb53a1216925",frozen_source_blob:"7a9b212ea722771ab6762b8cc6a0d647a33de0a8",worlds:8,conditions:results.length,source_atoms:rows.length,expanded_weighted_slots:rows.length*4*2,probability_denominator:128,alias_pairs_checked:2,attenuation_identity_pass:true,new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",results};
}

if(require.main===module){if(process.argv.length!==3)throw Error("usage: node r233_s29_group_label_exact_20261028.js <R233 CSV>");console.log(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2))}
module.exports={compute};
