"use strict";
const WORLDS=["ONE_FACTOR_VALID","ONE_FACTOR_SIGNED","TWO_FACTOR_BLOCK","CORRELATED_RESIDUAL_METHOD","SECOND_FACTOR_SEMANTIC_ALIAS","TETRAD_FALSE_REASSURANCE","CROSS_LOADING_CANCEL","ONE_FACTOR_UNEQUAL_LOAD"];
function parseCSV(csv){
 const lines=csv.trim().split(/\r?\n/);const h=lines.shift().split(",");
 const ix=[1,2,3,4].map(j=>h.indexOf("observed_X"+j));const wi=h.indexOf("world");
 if(ix.some(j=>j<0)||wi<0)throw Error("CSV headers absent");
 const groups={};for(const w of WORLDS)groups[w]=[];
 for(const line of lines){const a=line.split(",");if(!groups[a[wi]])throw Error("unexpected world");groups[a[wi]].push(ix.map(j=>Number(a[j])));}
 if(lines.length!==512||WORLDS.some(w=>groups[w].length!==64))throw Error("original 512 rows changed");
 return groups;
}
function pairTetrad(xs){
 const n=xs.length;
 function cross(i,j){let s=0;for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)s+=(xs[a][i]-xs[b][i])*(xs[a][j]-xs[b][j]);return s;}
 const a=cross(0,1)*cross(2,3),b=cross(0,2)*cross(1,3),c=cross(0,3)*cross(1,2);
 return [a-b,a-c,b-c];
}
function compute(csv){
 const g=parseCSV(csv),out=[];
 for(const world of WORLDS){
  const rows=g[world];
  for(const n of [2,3]){
   let zero=0,nonzero=0;
   for(let i=0;i<64;i++)for(let j=0;j<64;j++){
    if(n===2){const t=pairTetrad([rows[i],rows[j]]);if(t.every(x=>x===0))zero++;else nonzero++;}
    else for(let k=0;k<64;k++){const t=pairTetrad([rows[i],rows[j],rows[k]]);if(t.every(x=>x===0))zero++;else nonzero++;}
   }
   const total=64**n;if(zero+nonzero!==total)throw Error("mass mismatch");
   if(n===2&&nonzero!==0)throw Error("rank-one negative control");
   out.push({world,n,ordered_sequences:total,tetrad_all_zero:zero,tetrad_any_nonzero:nonzero,zero_probability_fraction:zero+"/"+total});
  }
 }
 for(const n of [2,3]){const a=out.find(x=>x.world==="CORRELATED_RESIDUAL_METHOD"&&x.n===n),b=out.find(x=>x.world==="SECOND_FACTOR_SEMANTIC_ALIAS"&&x.n===n);if(a.tetrad_all_zero!==b.tetrad_all_zero)throw Error("semantic alias mismatch");}
 return {research_id:"R231_S27",scope:"E1_ARTIFICIAL_EXACT_ORDERED_SAMPLING",original_csv_blob_sha:"f56003f4b18f1dfcbdcd00aabc22fa0815205b64",prescore_freeze_commit:"4f8a999530f8c8f6227c461b0c30f42d02574815",total_ordered_sequences:out.reduce((s,x)=>s+x.ordered_sequences,0),worlds:out,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs"),p=require("path");const root=p.resolve(__dirname,"../..");const csv=fs.readFileSync(p.join(root,"research/R231/R231_ALL_512_ORIGINAL_CFA_STRUCTURAL_ATOMS.csv"),"utf8");process.stdout.write(JSON.stringify(compute(csv),null,2)+"\n");}
if(typeof module!=="undefined")module.exports={compute,parseCSV,pairTetrad};
