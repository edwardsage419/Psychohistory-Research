"use strict";
// Run from repository root: node research/operations/e040_r207_mnar_source_moment_recheck_20261027.js
const fs=require("node:fs");

function audit(receipt){
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n};
const f=(n,d=1)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]};
const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>f(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
const fmt=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const sources=Array.from({length:64},(_,i)=>{let v=Array.from({length:6},(_,k)=>1+((i>>k)&1));return Array.from({length:9},(_,k)=>v[Math.floor(k/3)]*v[3+k%3])});
const masks=[];function combos(start,a){if(a.length===5){masks.push(a);return}for(let i=start;i<=9-(5-a.length);i++)combos(i+1,[...a,i])}combos(0,[]);
const reference=new Map(receipt.worlds.map(x=>[x.mask,x]));
const keys=["mass","correct_weighted_mse","ignore_weighted_mse","visible_weighted_mse","zero_weighted_mse","excess_weighted_mse"];
const gkeys=["mass","correct","ignore","visible","zero","excess"];
let total=Array.from({length:6},()=>f(0)),comparisons=0,constantQ=0,observed=0,positive=0;
for(const mask of masks){
 const anchor=mask.includes(8),den=64*4*(anchor?70:56),hidden=Array.from({length:9},(_,i)=>i).filter(k=>!mask.includes(k));
 const groups=new Map();
 for(const m of sources){const sig=mask.map(k=>m[k]),id=sig.join(","),q=({1:1,2:2,4:3})[m[8]],w=anchor?q:4-q;if(!groups.has(id))groups.set(id,{sig,vals:[]});groups.get(id).vals.push({m,w})}
 const result=Array.from({length:6},()=>f(0));
 for(const {sig,vals} of groups.values()){
  const s0=vals.reduce((a,x)=>a+x.w,0),n=vals.length,vis=f(sig.reduce((a,b)=>a+b,0),5);
  result[0]=add(result[0],f(s0,den));
  for(const k of hidden){
   const s1=vals.reduce((a,x)=>a+x.w*x.m[k],0),s2=vals.reduce((a,x)=>a+x.w*x.m[k]*x.m[k],0),u1=vals.reduce((a,x)=>a+x.m[k],0);
   const mu=f(s1,s0),ui=f(u1,n),factor=f(1,4*den);
   const loss=p=>mul(add(sub(f(s2),mul(f(2*s1),p)),mul(mul(p,p),f(s0))),factor);
   result[1]=add(result[1],mul(sub(f(s2),f(s1*s1,s0)),factor));
   result[2]=add(result[2],loss(ui));
   result[3]=add(result[3],loss(vis));
   result[4]=add(result[4],mul(f(s2),factor));
   result[5]=add(result[5],mul(mul(mul(sub(mu,ui),sub(mu,ui)),f(s0)),factor));
   const equalWeight=f(vals.reduce((a,x)=>a+x.m[k],0),n);
   if(!eq(equalWeight,ui))throw Error("constant q");
   constantQ++;
   if(anchor){if(!eq(mu,ui))throw Error("anchor observed");observed++}
  }
 }
 const label=mask.map(i=>String(Math.floor(i/3))+String(i%3)).join("|"),row=reference.get(label);
 if(!row)throw Error("missing mask "+label);
 keys.forEach((k,j)=>{if(fmt(result[j])!==row[k])throw Error(label+" "+k+" "+fmt(result[j])+" != "+row[k]);comparisons++;total[j]=add(total[j],result[j])});
 if(result[5][0]>0n)positive++;
 if(!eq(sub(result[2],result[1]),result[5]))throw Error("excess identity "+label);
}
gkeys.forEach((k,j)=>{if(fmt(total[j])!==receipt.totals[k])throw Error("global "+k)});
if(comparisons!==756||constantQ!==26496||observed!==14720||positive!==16)throw Error("counts");
if(fmt(add(total[1],f(1)))===receipt.totals.correct)throw Error("mutation missed");
return {masks:126,sourcePaths:64,sourceMaskPairs:8064,hiddenItems:32256,exactMaskFields:comparisons,exactTotals:6,constantQChecks:constantQ,anchorObservedChecks:observed,positiveMasks:positive,mutationRejected:true,totals:Object.fromEntries(gkeys.map((k,j)=>[k,fmt(total[j])]))};
}
const receipt=JSON.parse(fs.readFileSync("research/validation/R207_MNAR_ANCHOR_126_EXACT_RECEIPT_2026-10-27.json","utf8"));
console.log(JSON.stringify(audit(receipt),null,2));
