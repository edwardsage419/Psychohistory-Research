#!/usr/bin/env node
"use strict";
/* Independent of R266 S62 source-row parser. Reconstructs PMFs by convoluting
 * one primitive draw over four equiprobable states, then checks the full receipt.
 * The researcher had read original R266 and R266 S62 results: NONBLIND INTERNAL. */
function gcd(a,b){while(b){let r=a%b;a=b;b=r;}return a;}
function frac(a,b=1){if(!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||b<=0)throw Error("unsafe fraction");const g=gcd(Math.abs(a),b);return (b/g===1)?String(a/g):String(a/g)+"/"+String(b/g);}
const functions=["THRESHOLD_Q1","THRESHOLD_HALF","THRESHOLD_Q3","SYMMETRIC_EXTREMES"];
const worlds=functions.slice(0,3).flatMap(f=>[2,4].map(n=>[f,n])).concat([2,4,6].map(n=>["SYMMETRIC_EXTREMES",n]));
function f(fn,u){if(fn==="THRESHOLD_Q1")return +(u===0);if(fn==="THRESHOLD_HALF")return +(u<=1);if(fn==="THRESHOLD_Q3")return +(u<=2);if(fn==="SYMMETRIC_EXTREMES")return +(u===0||u===3);throw Error("unfrozen function");}
function oracle(){
 const out=[];
 for(const [fn,n] of worlds){
  const a=fn==="THRESHOLD_Q1"?1:fn==="THRESHOLD_Q3"?3:2;
  for(const design of ["IID","ANTITHETIC"]){
   const m=design==="IID"?n:n/2;
   let counts=new Map([[0,1]]);
   for(let t=0;t<m;t++){
    const next=new Map();
    for(const [old,weight] of counts)for(let u=0;u<4;u++){
     const k=old+f(fn,u)+(design==="ANTITHETIC"?f(fn,3-u):0);
     next.set(k,(next.get(k)||0)+weight);
    }
    counts=next;
   }
   const total=4**m;
   if([...counts.values()].reduce((x,y)=>x+y,0)!==total)throw Error("bad convolution");
   let covered=0,plug=0,varianceNumer=0;
   for(const [k,weight] of counts){
    if((4*k-a*n)**2<=4*n*a*(4-a))covered+=weight;
    plug+=weight*k*(n-k);
    varianceNumer+=weight*(4*k-a*n)**2;
   }
   const actualNumer=varianceNumer,actualDenom=16*n*n*total;
   out.push({world:fn+"_N"+n,design,evaluations:n,source_atoms:total,covered_atoms:covered,
    exact_score_z2_coverage:frac(covered,total),exact_score_z2_miscoverage:frac(total-covered,total),
    expected_naive_IID_plugin_variance:frac(plug,n**3*total),
    actual_estimator_variance:frac(actualNumer,actualDenom),
    naive_plugin_over_actual_variance:actualNumer===0?null:frac(plug*actualDenom,n**3*total*actualNumer)});
  }
 }
 return out;
}
function check(receipt){
 if(!receipt||typeof receipt!=="object"||Array.isArray(receipt))throw Error("bad receipt");
 const exact={research_id:"R266_S62",protocol_freeze_commit:"6cdc35c36bdf6d2f06761dff5b04a8af8aa1bd8b",
 original_R266_source_sha256:"5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a",
 original_complete_source_types:5328,worlds:9,design_combinations:18,
 score_interval:"Wilson score inversion, z=2, evaluated as if n function calls IID",
 nominal_normal_reference:"about 95.45%, not exact finite coverage",
 evidence:"E1_EXHAUSTIVE_ARTIFICIAL_ONLY",new_real_human_E2:0,new_real_historical_E3:0,
 R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 for(const [k,v] of Object.entries(exact))if(typeof receipt[k]!==typeof v||receipt[k]!==v)throw Error("metadata mismatch: "+k);
 const exp=oracle();
 if(!Array.isArray(receipt.results)||receipt.results.length!==exp.length)throw Error("coverage size mismatch");
 for(let i=0;i<exp.length;i++){
  const x=receipt.results[i],y=exp[i];
  if(!x||typeof x!=="object"||Array.isArray(x))throw Error("invalid row "+i);
  if(Object.keys(x).sort().join("|")!==Object.keys(y).sort().join("|"))throw Error("row fields "+i);
  for(const [k,v] of Object.entries(y))if(typeof x[k]!==typeof v||x[k]!==v)throw Error("row "+i+" field "+k);
 }
 return {status:"PASS",worlds:9,designs:18,fields_compared:18*Object.keys(exp[0]).length,
  exact_oracle:"independent four-point success-count convolution",blind:false,external_replication:false};
}
function negativeTests(receipt){
 const mutations=[
  x=>{x.results[0].exact_score_z2_coverage="1";},
  x=>{x.results.pop();},
  x=>{x.results[1]=x.results[0];},
  x=>{x.evidence="E2_HUMAN";},
  x=>{x.results[0].covered_atoms=false;}
 ];
 let rejected=0;
 for(const mutate of mutations){const x=JSON.parse(JSON.stringify(receipt));mutate(x);try{check(x)}catch(e){rejected++;}}
 if(rejected!==mutations.length)throw Error("negative controls accepted: "+rejected);
 return rejected;
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 const input=process.argv[2];
 if(!input)throw Error("usage: node r266_s62_independent_convolution_gate.js path/to/receipt.json");
 const receipt=JSON.parse(fs.readFileSync(input,"utf8"));
 console.log(JSON.stringify({...check(receipt),negative_controls_rejected:negativeTests(receipt)}));
}
if(typeof module!=="undefined")module.exports={oracle,check,negativeTests};
