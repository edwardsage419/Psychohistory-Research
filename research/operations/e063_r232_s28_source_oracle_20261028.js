#!/usr/bin/env node
'use strict';
// E063: independent source potential-outcome and observable-moment checks.
// Usage: node research/operations/e063_r232_s28_source_oracle_20261028.js
// Uses only Node.js standard library and frozen repository files.
const fs=require('fs'),path=require('path');
function audit(csv,receipt){
 const lines=csv.trim().split(/\r?\n/),head=lines.shift().split(",");
 const data=lines.map(l=>Object.fromEntries(l.split(",").map((v,i)=>[head[i],v])));
 const groups={};for(const r of data)(groups[r.world]??=[]).push(r);
 let checks=0,failures=[];
 const check=(ok,msg)=>{checks++;if(!ok&&failures.length<30)failures.push(msg);};
 const fraction=s=>{const [n,d="1"]=String(s).split("/");return [BigInt(n),BigInt(d)];};
 const equal=(n,d,s)=>{const [a,b]=fraction(s);return n*b===a*d;};
 const add=(a,b)=>[a[0]*b[1]+b[0]*a[1],a[1]*b[1]];
 const sub=(a,b)=>[a[0]*b[1]-b[0]*a[1],a[1]*b[1]];
 const mul=(a,b)=>[a[0]*b[0],a[1]*b[1]];
 const div=(a,b)=>[a[0]*b[1],a[1]*b[0]];
 check(data.length===1024,"original row count");
 check(Object.keys(groups).length===8,"world count");
 check(receipt.rows.length===32,"grid count");
 for(const [world,rows] of Object.entries(groups)){
  check(rows.length===128,"rows "+world);
  const identities=new Set();
  const ref=receipt.rows.find(x=>x.world===world&&x.lambda===0);
  check(!!ref,"missing baseline "+world);
  if(!ref)continue;
  for(const r of rows){
   const ex=["U","R","EM","EY","EW","EZ1","EZ2"].map(k=>r["oracle_original_"+k]);
   check(ex.every(v=>v==="1"||v==="-1"),"exogenous "+world);
   identities.add(ex.join(","));
   check(r.original_source_probability==="1/128","probability "+world);
   for(const [name,minus,plus] of [
    ["total","oracle_Y_doAminus1","oracle_Y_doAplus1"],
    ["direct","oracle_Y_at_fixedM_Aminus1","oracle_Y_at_fixedM_Aplus1"],
    ["indirect","oracle_Y_at_actualA_MdoMinus1","oracle_Y_at_actualA_MdoPlus1"]
   ])check(equal(BigInt(r[plus])-BigInt(r[minus]),2n,ref.truth[name]),"source potential outcome "+world+" "+name);
  }
  check(identities.size===128,"unique source "+world);
 }
 for(const row of receipt.rows){
  const rows=groups[row.world]||[],lambda=row.lambda;
  check(rows.length===128,"missing world "+row.world);
  if(rows.length!==128)continue;
  const obs=rows.map(r=>[+r.observed_A,+r.observed_W+lambda*(+r.oracle_original_EW),+r.observed_Y,+r.observed_Z1,+r.observed_Z2]);
  for(let i=0;i<5;i++){
   check(obs.reduce((s,x)=>s+BigInt(x[i]),0n)===0n,"mean "+row.world+" "+lambda+" "+i);
   for(let j=0;j<5;j++){
    const n=obs.reduce((s,x)=>s+BigInt(x[i])*BigInt(x[j]),0n);
    check(equal(n,128n,row.covariance[i][j]),"cov "+row.world+" "+lambda+" "+i+" "+j);
   }
  }
  check(new Set(obs.map(x=>x.join(","))).size===row.observed_joint_support,"support "+row.world+" "+lambda);
  const c=row.covariance,A=fraction(c[0][0]),W=fraction(c[1][1]),AW=fraction(c[0][1]),AY=fraction(c[0][2]),WY=fraction(c[1][2]);
  const det=sub(mul(A,W),mul(AW,AW));
  check(det[0]*det[1]>0n,"positive determinant "+row.world+" "+lambda);
  const total=div(AY,A),a=div(AW,A),b=div(sub(mul(WY,A),mul(AY,AW)),det),d=div(sub(mul(AY,W),mul(WY,AW)),det),product=mul(a,b),bias=sub(product,fraction(row.truth.indirect));
  for(const [key,val] of Object.entries({total,a_to_w:a,y_on_w_given_a:b,y_on_a_given_w:d,proxy_indirect:product,proxy_bias:bias}))
   check(equal(val[0],val[1],row.paths[key]),"OLS "+row.world+" "+lambda+" "+key);
  check(equal(add(d,product)[0],add(d,product)[1],row.paths.total),"path decomposition "+row.world+" "+lambda);
 }
 for(let lambda=0;lambda<4;lambda++){
  const as=groups.LATENT_CAUSAL_ALIAS,bs=groups.LATENT_COMMON_ALIAS;
  const freq=rows=>{const m=new Map();for(const r of rows){const key=[r.observed_A,+r.observed_W+lambda*(+r.oracle_original_EW),r.observed_Y,r.observed_Z1,r.observed_Z2].join(",");m.set(key,(m.get(key)||0)+1);}return JSON.stringify([...m].sort(([a],[b])=>a.localeCompare(b)));};
  check(freq(as)===freq(bs),"observable alias lambda "+lambda);
 }
 return {source_rows:data.length,worlds:Object.keys(groups).length,grid_conditions:receipt.rows.length,checks,failures};
}
const root=path.resolve(__dirname,'../..');
const csv=fs.readFileSync(path.join(root,'research/R232/R232_ALL_1024_ORIGINAL_SEM_EXOGENOUS_SOURCES.csv'),'utf8');
const receipt=JSON.parse(fs.readFileSync(path.join(root,'research/validation/R232_S28_PROXY_NOISE_RECEIPT_2026-10-28.json'),'utf8'));
const out=audit(csv,receipt);
process.stdout.write(JSON.stringify(out,null,2)+'\n');
if(out.failures.length)process.exitCode=1;
