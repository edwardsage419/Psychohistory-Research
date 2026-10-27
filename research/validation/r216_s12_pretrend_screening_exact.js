"use strict";
/* R216 S12: exact 4096-source per-world conditional risk. Frozen protocol:
 protocols/R216_S12_PRETREND_SCREENING_CONDITIONAL_RISK_PRESCORE_FREEZE_2026-10-27.md
 Run: node r216_s12_pretrend_screening_exact.js
 Standard Node.js only. No external data or paid computation. */
const WORLDS=["VALID_CONSTANT","VALID_HETEROGENEOUS","VALID_DYNAMIC","POST_EVENT_SHOCK_MIMIC","DIFFERENTIAL_PRETREND","LATE_ANTICIPATION"];
const THRESHOLDS=[0,1,2,4,"ALL"];
const EST=["E_k1_clean","L_k0_clean","E_k1_BAD_L_ALREADY_TREATED"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function frac(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return b/g===1n?String(a/g):String(a/g)+"/"+String(b/g);}
function mu(world){
  const y=[1,2,3,4,-1,0,1,2,0,1,2,3];
  const e=world==="VALID_CONSTANT"?[2,2,2]:world==="VALID_HETEROGENEOUS"?[1,1,3]:world==="VALID_DYNAMIC"||world==="POST_EVENT_SHOCK_MIMIC"?[2,4,1]:world==="LATE_ANTICIPATION"?[1,2,3]:[0,0,0];
  if(world==="DIFFERENTIAL_PRETREND"){for(let t=0;t<4;t++)y[t]+=t;}
  else {y[2]+=e[0];y[3]+=e[1];y[7]+=e[2];}
  if(world==="LATE_ANTICIPATION")y[6]+=1;
  return y;
}
function targets(world){return world==="VALID_CONSTANT"?[2,2,2]:world==="VALID_HETEROGENEOUS"?[1,3,1]:world==="VALID_DYNAMIC"?[4,1,4]:world==="LATE_ANTICIPATION"?[2,3,2]:[0,0,0];}
function measures(y){
 const ep=(y[1]-y[0])-(y[9]-y[8]);
 const lp=(y[6]-y[5])-(y[10]-y[9]);
 const e=(y[3]-y[1])-(y[11]-y[9]);
 const l=(y[7]-y[6])-(y[11]-y[10]);
 const bad=(y[3]-y[1])-(y[7]-y[5]);
 return [ep,lp,e,l,bad];
}
function run(){
 const rows=[];let sourceCount=0,comparisonCount=0;
 for(const world of WORLDS){
  const base=mu(world),tar=targets(world),vectors=[];
  for(let mask=0;mask<4096;mask++){
   const y=base.map((m,i)=>m+((mask&(1<<i))?1:-1));
   vectors.push(measures(y));sourceCount++;
  }
  for(const h of THRESHOLDS){
   const kept=vectors.filter(v=>h==="ALL"||Math.max(Math.abs(v[0]),Math.abs(v[1]))<=h);
   const n=kept.length;const row={world,threshold:h,accepted:n,source_count:4096,acceptance_probability:frac(n,4096),pre_E_mean:n?frac(kept.reduce((s,v)=>s+v[0],0),n):null,pre_L_mean:n?frac(kept.reduce((s,v)=>s+v[1],0),n):null,estimators:{}};
   for(let j=0;j<3;j++){
    const k=j+2,t=tar[j],sum=kept.reduce((s,v)=>s+v[k],0),sq=kept.reduce((s,v)=>s+v[k]*v[k],0),loss=kept.reduce((s,v)=>s+(v[k]-t)**2,0);
    row.estimators[EST[j]]=n?{target:t,mean:frac(sum,n),variance:frac(BigInt(sq)*BigInt(n)-BigInt(sum)*BigInt(sum),BigInt(n)*BigInt(n)),bias:frac(sum-n*t,n),mse:frac(loss,n)}:{target:t,mean:null,variance:null,bias:null,mse:null};
    comparisonCount++;
   }
   if(h==="ALL"){
    if(n!==4096)throw Error("ALL count");
    for(const name of EST)if(row.estimators[name].variance!=="4")throw Error("ALL variance");
   }
   rows.push(row);
  }
 }
 const a=rows.filter(r=>r.world==="VALID_DYNAMIC"),b=rows.filter(r=>r.world==="POST_EVENT_SHOCK_MIMIC");
 for(let i=0;i<a.length;i++){
  if(a[i].accepted!==b[i].accepted||a[i].pre_E_mean!==b[i].pre_E_mean||a[i].pre_L_mean!==b[i].pre_L_mean)throw Error("observational alias pre");
  for(const e of EST)if(a[i].estimators[e].mean!==b[i].estimators[e].mean||a[i].estimators[e].variance!==b[i].estimators[e].variance)throw Error("observational alias post");
 }
 for(const w of WORLDS){
  const r=rows.filter(r=>r.world===w);
  for(let i=1;i<r.length;i++)if(r[i].accepted<r[i-1].accepted)throw Error("nonmonotone selection");
 }
 if(sourceCount!==24576||rows.length!==30||comparisonCount!==90)throw Error("coverage");
 const result={schema:"r216_s12_exact_v1",protocol:"protocols/R216_S12_PRETREND_SCREENING_CONDITIONAL_RISK_PRESCORE_FREEZE_2026-10-27.md",original_R216_artificial_source_worlds:6,original_complete_source_histories:sourceCount,conditions:rows.length,estimator_condition_cells:comparisonCount,conditional_on_observed_pretrend_only:true,original_R216_unchanged:true,source_type:"E1_ARTIFICIAL",new_real_E2:0,new_historical_E3:0,external_independent_replications:0,rows};
 return result;
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
