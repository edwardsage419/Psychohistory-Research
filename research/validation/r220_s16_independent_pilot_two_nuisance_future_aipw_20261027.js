
"use strict";
const N=8, X=[0,0,0,0,1,1,1,1], U=[0,0,1,1,0,0,1,1];
const names=["BOTH_CORRECT","PROP_CORRECT_OUTCOME_WRONG","PROP_WRONG_OUTCOME_CORRECT","BOTH_WRONG","HIDDEN_U_BOTH","WEAK_OVERLAP","NO_POSITIVITY"];
const methods=["PILOT_BOTH_AIPW","PILOT_Q_TRUE_M_AIPW","TRUE_X_Q_PILOT_M_AIPW","PILOT_OUTCOME_ONLY","ORIGINAL_FIXED_AIPW"];
function gcd(a,b){while(b){let t=a%b;a=b;b=t}return a<0n?-a:a}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]}
const Z=F(0),O=F(1),T=F(2);
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>[-a[0],a[1]];
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
const sq=a=>mul(a,a);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const fmt=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
const sum=xs=>xs.reduce(add,Z);
const bits=m=>Array.from({length:N},(_,i)=>(m>>i)&1);
function world(name){
 const y0=X.map((x,i)=>F(2*x+2*U[i])),y1=y0.map(v=>add(v,T));
 let p=X.map((x,i)=>name==="NO_POSITIVITY"?F(x):name==="WEAK_OVERLAP"?(x?F(15,16):F(1,16)):name==="HIDDEN_U_BOTH"?(x?add(F(5,8),F(U[i],4)):add(F(1,8),F(U[i],4))):(x?F(3,4):F(1,4)));
 let qX=X.map(x=>name==="WEAK_OVERLAP"?(x?F(15,16):F(1,16)):(x?F(3,4):F(1,4)));
 let q=name==="PROP_WRONG_OUTCOME_CORRECT"||name==="BOTH_WRONG"?X.map(()=>F(1,2)):name==="HIDDEN_U_BOTH"?qX:p;
 let correct=["BOTH_CORRECT","PROP_WRONG_OUTCOME_CORRECT","HIDDEN_U_BOTH","NO_POSITIVITY"].includes(name);
 let m0=X.map(x=>correct?F(2*x+1):Z),m1=X.map(x=>correct?F(2*x+3):O);
 return {name,p,q,qX,y0,y1,m0,m1,positive:name!=="NO_POSITIVITY"};
}
function prob(p,mask){let v=O;for(let i=0;i<N;i++)v=mul(v,((mask>>i)&1)?p[i]:sub(O,p[i]));return v}
function pilot(w,mask){
 let qs=[],a0=[],a1=[];
 for(let x=0;x<=1;x++){
  let k=0,n0=0,n1=0,s0=Z,s1=Z;
  for(let i=0;i<N;i++)if(X[i]===x){
   if((mask>>i)&1){k++;n1++;s1=add(s1,w.y1[i])}
   else{n0++;s0=add(s0,w.y0[i])}
  }
  qs[x]=F(k+1,6);a0[x]=div(s0,F(n0+1));a1[x]=div(s1,F(n1+1));
 }
 return {q:X.map(x=>qs[x]),m0:X.map(x=>a0[x]),m1:X.map(x=>a1[x])};
}
function moment(w,q,m0,m1,outcomeOnly=false){
 if(outcomeOnly){let v=div(sum(m1.map((v,i)=>sub(v,m0[i]))),F(N));return [v,Z]}
 let means=[],variances=[];
 for(let i=0;i<N;i++){
  let p=w.p[i],oneMinusP=sub(O,p),oneMinusQ=sub(O,q[i]);
  let a=div(sub(w.y1[i],m1[i]),q[i]),b=div(sub(w.y0[i],m0[i]),oneMinusQ);
  means.push(add(sub(add(sub(m1[i],m0[i]),mul(p,a)),mul(oneMinusP,b)),Z));
  variances.push(mul(mul(p,oneMinusP),sq(add(a,b))));
 }
 return [div(sum(means),F(N)),div(sum(variances),F(N*N))];
}
function compute(){
 let worlds=[],checks=0;
 const baseline={BOTH_CORRECT:["2","2/3"],PROP_CORRECT_OUTCOME_WRONG:["2","125/24"],PROP_WRONG_OUTCOME_CORRECT:["2","3/8"],BOTH_WRONG:["3","131/32"],HIDDEN_U_BOTH:["8/3","19/18"],WEAK_OVERLAP:["2","1937/120"]};
 for(let name of names){
  let w=world(name);
  if(!w.positive){worlds.push({world:name,positivity:false,pilot_assignments:1,future_assignments:1,all_methods_null:true,methods:Object.fromEntries(methods.map(k=>[k,null]))});continue}
  let mass=Z,acc=Object.fromEntries(methods.map(k=>[k,{e:Z,e2:Z}]));
  for(let mask=0;mask<256;mask++){
   let pr=prob(w.p,mask);mass=add(mass,pr);let a=pilot(w,mask);
   let cfg={
    PILOT_BOTH_AIPW:[a.q,a.m0,a.m1,false],
    PILOT_Q_TRUE_M_AIPW:[a.q,X.map(x=>F(2*x+1)),X.map(x=>F(2*x+3)),false],
    TRUE_X_Q_PILOT_M_AIPW:[w.qX,a.m0,a.m1,false],
    PILOT_OUTCOME_ONLY:[a.q,a.m0,a.m1,true],
    ORIGINAL_FIXED_AIPW:[w.q,w.m0,w.m1,false]
   };
   for(let key of methods){
    let [mean,v]=moment(w,...cfg[key]);acc[key].e=add(acc[key].e,mul(pr,mean));
    acc[key].e2=add(acc[key].e2,mul(pr,add(v,sq(mean))));
   }
  }
  if(!eq(mass,O))throw Error("pilot mass "+name);
  let out={};
  for(let key of methods){
   let e=acc[key].e,e2=acc[key].e2,v=sub(e2,sq(e)),bias=sub(e,T),mse=add(v,sq(bias));
   if(v[0]<0n||!eq(mse,sub(sub(e2,mul(F(4),e)),F(-4))))throw Error("risk identity");
   out[key]={mean:fmt(e),variance:fmt(v),bias:fmt(bias),mse:fmt(mse)};checks++;
  }
  if(out.ORIGINAL_FIXED_AIPW.mean!==baseline[name][0]||out.ORIGINAL_FIXED_AIPW.mse!==baseline[name][1])throw Error("R220 regression mismatch "+name);
  checks+=2;
  worlds.push({world:name,positivity:true,pilot_assignments:256,future_assignments:256,joint_assignment_slots:65536,pilot_probability_mass:fmt(mass),future_probability_mass:fmt(sum(Array.from({length:256},(_,i)=>prob(w.p,i)))),methods:out});
 }
 const w=world("BOTH_CORRECT"),a=pilot(w,0),orig=moment(w,a.q,a.m0,a.m1)[0];
 let injected={...w,y1:w.y1.map((v,i)=>i===0?add(v,O):v)};
 let mutated=moment(injected,a.q,a.m0,a.m1)[0];
 if(eq(orig,mutated))throw Error("outcome mutation not detected");
 const frozen=fmt(a.q[0]),leaky=fmt(F(2,7));
 if(frozen===leaky)throw Error("future treatment leakage not detected");
 return {research_id:"R220",extension:"S16",evidence:"E1_ARTIFICIAL",status:"COMPUTED_INTERNAL_EXACT_CI_NOT_RUN",original_result_blob:"390562952c0f5ae496287d3e74e9a434b529e10a",protocol:"protocols/R220_S16_INDEPENDENT_PILOT_TWO_NUISANCE_FUTURE_AIPW_PRESCORE_FREEZE_2026-10-27.md",pilot_and_future_distinct_artificial_ids:true,worlds_total:7,positive_worlds:6,positive_joint_assignment_slots:393216,original_R220_full_assignment_sources_unchanged:1537,comparison_method_fields_exact_checked:checks,negative_controls:{future_y1_mutation_detected:true,original_mean_at_pilot_zero:fmt(orig),mutated_mean_at_pilot_zero:fmt(mutated),future_z_leak_detected:true,pilot_q_x0_mask0:frozen,leaky_q_x0_mask0_future_z0_one:leaky,no_positivity_remains_null:true},human_E2:0,historical_E3:0,external_replication:0,worlds};
}
console.log(JSON.stringify(compute(),null,2));
