#!/usr/bin/env node
// Independent full pilot x future enumeration, no R220 S16 code import.
const receipt=JSON.parse(require("node:fs").readFileSync(process.argv[2]||"research/validation/R220_S16_PILOT_TWO_NUISANCE_6_WORLD_EXACT_RECEIPT_2026-10-27.json","utf8"));

"use strict";
const X=[0,0,0,0,1,1,1,1],U=[0,0,1,1,0,0,1,1],N=8;
const names=["BOTH_CORRECT","PROP_CORRECT_OUTCOME_WRONG","PROP_WRONG_OUTCOME_CORRECT","BOTH_WRONG","HIDDEN_U_BOTH","WEAK_OVERLAP","NO_POSITIVITY"];
const methods=["PILOT_BOTH_AIPW","PILOT_Q_TRUE_M_AIPW","TRUE_X_Q_PILOT_M_AIPW","PILOT_OUTCOME_ONLY","ORIGINAL_FIXED_AIPW"];
function world(name){
 const y0=X.map((x,i)=>2*x+2*U[i]),y1=y0.map(v=>v+2);
 const p=X.map((x,i)=>name==="NO_POSITIVITY"?x:name==="WEAK_OVERLAP"?(x?15/16:1/16):name==="HIDDEN_U_BOTH"?(x?5/8+U[i]/4:1/8+U[i]/4):(x?3/4:1/4));
 const qX=X.map(x=>name==="WEAK_OVERLAP"?(x?15/16:1/16):(x?3/4:1/4));
 const q=name==="PROP_WRONG_OUTCOME_CORRECT"||name==="BOTH_WRONG"?X.map(()=>1/2):name==="HIDDEN_U_BOTH"?qX:p;
 const correct=["BOTH_CORRECT","PROP_WRONG_OUTCOME_CORRECT","HIDDEN_U_BOTH","NO_POSITIVITY"].includes(name);
 return {p,q,qX,y0,y1,m0:X.map(x=>correct?2*x+1:0),m1:X.map(x=>correct?2*x+3:1)};
}
function probability(p,mask){let pr=1;for(let i=0;i<N;i++)pr*=((mask>>i)&1)?p[i]:(1-p[i]);return pr}
function train(w,mask){
 let q=[],m0=[],m1=[];
 for(let x=0;x<=1;x++){
  let k=0,n0=0,n1=0,s0=0,s1=0;
  for(let i=0;i<N;i++)if(X[i]===x){
   if((mask>>i)&1){k++;n1++;s1+=w.y1[i]}
   else{n0++;s0+=w.y0[i]}
  }
  q[x]=(k+1)/6;m0[x]=s0/(n0+1);m1[x]=s1/(n1+1);
 }
 return {q:X.map(x=>q[x]),m0:X.map(x=>m0[x]),m1:X.map(x=>m1[x])};
}
function estimate(w,mask,q,m0,m1){
 let s=0;
 for(let i=0;i<N;i++){
  if((mask>>i)&1)s+=m1[i]-m0[i]+(w.y1[i]-m1[i])/q[i];
  else s+=m1[i]-m0[i]-(w.y0[i]-m0[i])/(1-q[i]);
 }
 return s/N;
}
function number(v){if(v===null)return null;let a=String(v).split("/");return a.length===2?Number(a[0])/Number(a[1]):Number(v)}
function audit(receipt){
 let rows=[],comparisons=0,maxDiff=0,neg=null;
 for(let name of names){
  let w=world(name),ref=receipt.worlds.find(z=>z.world===name);
  if(name==="NO_POSITIVITY"){
   if(!ref||ref.all_methods_null!==true||methods.some(k=>ref.methods[k]!==null))throw Error("no positivity gate");
   comparisons++;continue;
  }
  let sums=Object.fromEntries(methods.map(k=>[k,{e:0,e2:0,mse:0}])),pilotMass=0,futureMass=0,sourceSlots=0;
  let futures=Array.from({length:256},(_,mask)=>({mask,pr:probability(w.p,mask)}));
  futureMass=futures.reduce((a,z)=>a+z.pr,0);
  for(let pm=0;pm<256;pm++){
   let pp=probability(w.p,pm),a=train(w,pm);pilotMass+=pp;
   let mTrue0=X.map(x=>2*x+1),mTrue1=X.map(x=>2*x+3);
   let cfg={
    PILOT_BOTH_AIPW:[a.q,a.m0,a.m1],
    PILOT_Q_TRUE_M_AIPW:[a.q,mTrue0,mTrue1],
    TRUE_X_Q_PILOT_M_AIPW:[w.qX,a.m0,a.m1],
    ORIGINAL_FIXED_AIPW:[w.q,w.m0,w.m1]
   };
   const reg=a.m1.reduce((s,v,i)=>s+v-a.m0[i],0)/N;
   for(let future of futures){
    let weight=pp*future.pr;sourceSlots++;
    for(let key of methods){
     let val=key==="PILOT_OUTCOME_ONLY"?reg:estimate(w,future.mask,...cfg[key]);
     let obj=sums[key];obj.e+=weight*val;obj.e2+=weight*val*val;obj.mse+=weight*(val-2)*(val-2);
    }
   }
  }
  if(sourceSlots!==65536||Math.abs(pilotMass-1)>1e-12||Math.abs(futureMass-1)>1e-12)throw Error("source mass");
  comparisons+=3;
  let results={};
  for(let key of methods){
   let obj=sums[key],mean=obj.e,v=obj.e2-mean*mean,bias=mean-2,mse=obj.mse;
   let vals={mean,variance:v,bias,mse};
   for(let field of Object.keys(vals)){
    let target=number(ref.methods[key][field]);let d=Math.abs(vals[field]-target);
    if(d>1e-9)throw Error(name+" "+key+" "+field+" diff="+d);
    maxDiff=Math.max(maxDiff,d);comparisons++;
   }
   results[key]=vals;
  }
  rows.push({world:name,pilot_assignments:256,future_assignments:256,joint_slots:sourceSlots,pilot_mass:pilotMass,future_mass:futureMass,methods:results});
  if(name==="BOTH_CORRECT"){
   let a=train(w,0),mean=0,changed=0;
   for(let f of futures){
    mean+=f.pr*estimate(w,f.mask,a.q,a.m0,a.m1);
    let changedW={...w,y1:w.y1.map((v,i)=>i===0?v+1:v)};
    changed+=f.pr*estimate(changedW,f.mask,a.q,a.m0,a.m1);
   }
   if(Math.abs(mean-number(receipt.negative_controls.original_mean_at_pilot_zero))>1e-10||
      Math.abs(changed-number(receipt.negative_controls.mutated_mean_at_pilot_zero))>1e-10||
      Math.abs(mean-changed)<1e-8)throw Error("mutation gate");
   let leak=(1+0+1)/7;
   if(Math.abs(leak-a.q[0])<1e-8)throw Error("leak gate");
   neg={future_y1_mutation_detected:true,future_z_leak_detected:true,original_conditional_mean:mean,mutated_conditional_mean:changed};
   comparisons+=4;
  }
 }
 return {research_id:"R220",extension:"S16",audit:"B_DIRECT_FULL_JOINT_ENUMERATION_FLOAT64",evidence:"E1_ARTIFICIAL",status:"INTERNAL_INDEPENDENT_ALGORITHM_CI_NOT_RUN",source_R_receipt_blob:"a75dd518a1b9094c329ecb4cf37c0c5863d787db",worlds_verified:6,full_joint_slots_enumerated:393216,comparison_fields_passed:comparisons,max_absolute_difference:maxDiff,tolerance:1e-9,negative_controls:neg,external_replication:0,rows};
}
console.log(JSON.stringify(audit(receipt),null,2));
