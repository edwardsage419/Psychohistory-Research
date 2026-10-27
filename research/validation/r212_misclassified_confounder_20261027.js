
"use strict";

function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}

const WORLDS=["CONFOUND","DIRECT","COMBINED"],Q=[0,1,2];
function Y(world,c,t){return world==="CONFOUND"?c:world==="DIRECT"?t:(t||c);}
function run(){
 const lines=["world,q,exogenous_C,exogenous_j,original_N,original_T,original_Y,measurement_slot,flip_E,observed_Cstar,observed_T,observed_Y,source_probability"];
 const worlds=[];let sourceRows=0;
 for(const world of WORLDS)for(const flipCount of Q){
  const cells=Array.from({length:2},()=>Array.from({length:2},()=>({n:0,y:0})));
  const raw=Array.from({length:2},()=>({n:0,y:0}));
  let total=0;
  for(let c=0;c<=1;c++)for(let j=0;j<4;j++)for(let slot=0;slot<4;slot++){
   const n=Number(j===0),t=c^n,y=Y(world,c,t),e=Number(slot<flipCount),s=c^e;
   cells[s][t].n++;cells[s][t].y+=y;raw[t].n++;raw[t].y+=y;total++;
   lines.push([world,flipCount+"/4",c,j,n,t,y,slot,e,s,t,y,"1/32"].join(","));sourceRows++;
  }
  if(total!==32||cells.some(a=>a.some(x=>x.n===0)))throw Error("positivity");
  let adj=F(0),support=[];
  for(let s=0;s<=1;s++){
   const ns=cells[s][0].n+cells[s][1].n,pt=F(ns,32);
   const difference=sub(F(cells[s][1].y,cells[s][1].n),F(cells[s][0].y,cells[s][0].n));
   adj=add(adj,mul(pt,difference));
   for(let t=0;t<=1;t++)support.push({cstar:s,t,n:cells[s][t].n,y:cells[s][t].y});
  }
  const obs=sub(F(raw[1].y,raw[1].n),F(raw[0].y,raw[0].n));
  const truth=world==="CONFOUND"?F(0):world==="DIRECT"?F(1):F(1,2);
  if(flipCount===0&&fmt(adj)!==fmt(truth))throw Error("q0 baseline parity");
  if(flipCount===2&&fmt(adj)!==fmt(obs))throw Error("q half independence");
  if(world==="DIRECT"&&fmt(adj)!=="1")throw Error("direct control");
  worlds.push({world,q:flipCount+"/4",source_rows:32,observational_difference:fmt(obs),proxy_adjusted_difference:fmt(adj),true_do_effect:fmt(truth),proxy_adjustment_bias:fmt(sub(adj,truth)),support});
 }
 if(sourceRows!==288||worlds.length!==9)throw Error("source count");
 return {csv:lines.join("\n")+"\n",receipt:{research:"R212",method:"misclassified_confounder_third_method",date:"2026-10-27",evidence:"E1_ARTIFICIAL",original_source_worlds:3,original_source_rows_per_world:8,independent_measurement_slots:4,misclassification_rates:["0","1/4","1/2"],augmented_source_rows:sourceRows,worlds,protocol:"protocols/R212_MISCLASSIFIED_CONFOUNDER_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",new_E2:0,new_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"}};
}

if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),out=process.argv[2]||".";
 fs.mkdirSync(out,{recursive:true});const r=run();
 fs.writeFileSync(path.join(out,"R212_MISCLASSIFIED_CONFOUNDER_288_SOURCE_ROWS_2026-10-27.csv"),r.csv);
 fs.writeFileSync(path.join(out,"R212_MISCLASSIFIED_CONFOUNDER_9_WORLD_RECEIPT_2026-10-27.json"),JSON.stringify(r.receipt,null,2)+"\n");
 console.log(JSON.stringify({rows:r.receipt.augmented_source_rows,worlds:r.receipt.worlds.length}));
}
if(typeof module!=="undefined")module.exports={run};
