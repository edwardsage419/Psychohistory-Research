#!/usr/bin/env node
"use strict";
const fs=require("fs");

function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a||1}
function f(n,d=1){let g=gcd(n,d);return d/g===1?String(n/g):n/g+"/"+d/g}
function n32(s){let [a,b=1]=s.split("/").map(Number);if((a*32)%b!==0)throw Error("nonintegral 32 unit");return a*32/b}
function audit(original,receipt){
 if(original.research_id!=="R233"||receipt.study!=="R233_S29"||receipt.conditions!==32)throw Error("identity");
 let checks=0,checkedCells=0;
 function equal(a,b,msg){checks++;if(a!==b)throw Error(msg+": "+a+" != "+b)}
 function expected(w,q){
  let m=new Map();
  for(let [key,p] of Object.entries(w.full_observed_group_item_joint)){
   let [g,...xs]=key.split(",").map(Number),unit=n32(p);
   for(let [h,k] of [[g,4-q],[1-g,q]]){if(!k)continue;let kk=[h,...xs].join(",");m.set(kk,(m.get(kk)||0)+unit*k)}
  }
  return m;
 }
 for(let r of receipt.results){
  let w=original.world_results.find(x=>x.world===r.world);if(!w)throw Error("missing original world");
  let m=expected(w,r.q_numerator_over_4),actual=r.joint_mass_units;
  equal(Object.keys(actual).length,m.size,"cell count");
  for(let [k,val] of m){equal(actual[k],val,"joint "+r.world+" "+r.q+" "+k);checkedCells++}
  let count=[0,0],sum=[[0,0,0],[0,0,0]];
  for(let [key,val] of m){let [h,...x]=key.split(",").map(Number);count[h]+=val;for(let j=0;j<3;j++)sum[h][j]+=x[j]*val}
  equal(count[0],64,"group0");equal(count[1],64,"group1");
  for(let j=0;j<3;j++)equal(r.observed_mean_difference[j],f(sum[1][j]-sum[0][j],64),"mean difference");
  equal([...m.values()].reduce((a,b)=>a+b,0),128,"total");
 }
 let mutant=JSON.parse(JSON.stringify(receipt)),key=Object.keys(mutant.results[0].joint_mass_units)[0];
 mutant.results[0].joint_mass_units[key]++;
 let baseline=expected(original.world_results.find(w=>w.world===mutant.results[0].world),mutant.results[0].q_numerator_over_4);
 let mutantDetected=mutant.results[0].joint_mass_units[key]!==baseline.get(key);
 if(!mutantDetected)throw Error("mutant missed");
 return {study:"B_R233_S29",basis:"original R233 archived joint distribution, separate probability mixing route",R_source:"original frozen 256 source rows",B_source:"R233_EXACT_RESULTS.json full_observed_group_item_joint",conditions:receipt.results.length,compared_joint_cells:checkedCells,exact_checks:checks,failures:0,mutant_detected:mutantDetected,external_independent_replication:0,new_E2:0,new_E3:0};
}

if(require.main===module){if(process.argv.length!==4)throw Error("usage: node b_r233_s29_independent_mixture_20261028.js <R233 results JSON> <S29 receipt JSON>");console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2))}
module.exports={audit};
