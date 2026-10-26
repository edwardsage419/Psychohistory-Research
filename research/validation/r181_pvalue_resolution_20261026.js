"use strict";
// node research/validation/r181_pvalue_resolution_20261026.js from repository root
const fs=require("node:fs");
function calc(worlds){
 const G=(a,b)=>b?G(b,a%b):(a<0n?-a:a);
 const f=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);let g=G(n,d);return [n/g,d/g]};
 const plus=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),times=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
 const read=s=>{let [a,b="1"]=s.split("/");return f(a,b)},str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
 const fact=n=>{let x=1n;for(let i=2;i<=n;i++)x*=BigInt(i);return x};
 const combos=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)for(let k=j+1;k<6;k++)combos.push([i,j,k]);
 const rows=[];const dist={};
 function walk(a){if(a.length<6){for(let i=a.length?a.at(-1):0;i<5;i++)walk([...a,i]);return;}
  let s=a.reduce((x,y)=>x+y,0),v=combos.map(ids=>Math.abs(2*ids.reduce((z,i)=>z+a[i],0)-s));
  let numer=v.map(x=>v.filter(y=>y>=x).length),minimum=Math.min(...numer);
  if(numer.some(n=>n<2||n%2))throw Error("invalid two-sided p");
  let counts={};for(let x of a)counts[x]=(counts[x]||0)+1;
  let mult=fact(6)/Object.values(counts).reduce((x,n)=>x*fact(n),1n);
  dist[minimum]=(dist[minimum]||0)+1;
  rows.push({k:a.join(""),m:String(mult),min_p:str(f(minimum,20)),reject05:numer.filter(n=>n<=1).length,reject10:numer.filter(n=>n<=2).length});
 }walk([]);
 const summary=worlds.map(w=>{let mass=f(0),r=f(0);for(let row of rows){let q=f(row.m);for(let x of row.k)q=times(q,read(w.source_count_pmf[+x]));mass=plus(mass,q);r=plus(r,times(q,f(row.reject10,20)));}
  if(str(mass)!=="1"||str(r)!==str(read(w.true_frequentist_false_positive_probabilities.cluster_alpha_0p1)))throw Error("archived rate mismatch");
  return {p:w.true_p,source:w.source,alpha05:"0",alpha10:str(r),matches_archived:true};
 });
 return {source_git_blob:"077be6f63f49326935f0ac8b812f95524ff9ec09",postscore:true,profiles:rows.length,assignments:20,minimum_p:"1/10",minimum_p_distribution_numerator_over_20:dist,alpha05_total_rejections:rows.reduce((s,x)=>s+x.reject05,0),rows,worlds:summary};
}
const w=JSON.parse(fs.readFileSync("research/R181/R181_EXACT_RESULTS.json","utf8")).all_source_worlds;
process.stdout.write(JSON.stringify(calc(w),null,2)+"\n");
