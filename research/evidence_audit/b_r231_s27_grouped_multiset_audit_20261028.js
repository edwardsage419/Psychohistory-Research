"use strict";
const WORLDS=["ONE_FACTOR_VALID","ONE_FACTOR_SIGNED","TWO_FACTOR_BLOCK","CORRELATED_RESIDUAL_METHOD","SECOND_FACTOR_SEMANTIC_ALIAS","TETRAD_FALSE_REASSURANCE","CROSS_LOADING_CANCEL","ONE_FACTOR_UNEQUAL_LOAD"];
function sourceGroups(csv){
 const lines=csv.trim().split(/\r?\n/),h=lines.shift().split(",");
 const xi=[1,2,3,4].map(i=>h.indexOf("observed_X"+i)),wi=h.indexOf("world");
 const g={};for(const w of WORLDS)g[w]=new Map();
 for(const l of lines){const a=l.split(","),w=a[wi],x=xi.map(i=>Number(a[i])),key=x.join(",");if(!g[w])throw Error("world changed");const v=g[w].get(key);if(v)v.freq++;else g[w].set(key,{x,freq:1});}
 if(lines.length!==512||WORLDS.some(w=>[...g[w].values()].reduce((s,z)=>s+z.freq,0)!==64))throw Error("source mass");
 return g;
}
function tetradFromMoments(obs){
 const n=obs.length, s=[0,0,0,0],p=Array.from({length:4},()=>[0,0,0,0]);
 for(const x of obs){for(let i=0;i<4;i++){s[i]+=x[i];for(let j=0;j<4;j++)p[i][j]+=x[i]*x[j];}}
 function cov(i,j){return n*p[i][j]-s[i]*s[j];}
 const a=cov(0,1)*cov(2,3),b=cov(0,2)*cov(1,3),c=cov(0,3)*cov(1,2);
 return a===b&&a===c;
}
function groupedAudit(csv,receipt){
 const groups=sourceGroups(csv),rows=[];let checked=0;
 for(const world of WORLDS){const vals=[...groups[world].values()];
  for(const n of [2,3]){
   let zero=0,nonzero=0,weightedTotal=0,multisets=0;
   for(let i=0;i<vals.length;i++)for(let j=i;j<vals.length;j++){
    const maxK=n===2?j:vals.length-1;
    for(let k=j;k<=maxK;k++){
     const ids=n===2?[i,j]:[i,j,k],xs=ids.map(t=>vals[t].x);
     const mult=n===2?(i===j?1:2):(i===j&&j===k?1:(i===j||j===k?3:6));
     const weight=mult*ids.reduce((a,t)=>a*vals[t].freq,1);
     if(tetradFromMoments(xs))zero+=weight;else nonzero+=weight;
     weightedTotal+=weight;multisets++;
    }
   }
   if(weightedTotal!==64**n||zero+nonzero!==weightedTotal)throw Error("weighted mass mismatch "+world+n);
   rows.push({world,n,ordered_sequences:weightedTotal,tetrad_all_zero:zero,tetrad_any_nonzero:nonzero,observable_multisets:multisets});
  }
 }
 if(receipt){
  if(receipt.worlds.length!==rows.length)throw Error("receipt case count changed");
  for(const b of rows){const a=receipt.worlds.find(x=>x.world===b.world&&x.n===b.n);if(!a)throw Error("missing case");for(const f of ["ordered_sequences","tetrad_all_zero","tetrad_any_nonzero"]){checked++;if(a[f]!==b[f])throw Error("AUDIT_MISMATCH "+b.world+" n="+b.n+" field="+f+" R="+a[f]+" B="+b[f]);}}
 }
 return {status:"PASS",independent_method:"OBSERVABLE_GROUPED_UNORDERED_MULTISET_WITH_PERMUTATION_WEIGHTS",cases:rows.length,compared_fields:checked,weighted_multisets:rows.reduce((s,x)=>s+x.observable_multisets,0),rows};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),p=require("path"),root=p.resolve(__dirname,"../..");
 const csv=fs.readFileSync(p.join(root,"research/R231/R231_ALL_512_ORIGINAL_CFA_STRUCTURAL_ATOMS.csv"),"utf8");
 const receipt=JSON.parse(fs.readFileSync(p.join(root,"research/validation/R231_S27_FINITE_SAMPLE_TETRAD_RECEIPT_2026-10-28.json"),"utf8"));
 process.stdout.write(JSON.stringify(groupedAudit(csv,receipt),null,2)+"\n");
}
if(typeof module!=="undefined")module.exports={groupedAudit,sourceGroups,tetradFromMoments};
