"use strict";
// Deterministic, no external dependencies. Run: node research/validation/r210_post_assignment_selection_third_method_20261027.js [output-prefix]
const fs=require("node:fs");
const study=function study(){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;};
  const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(!b)throw Error("zero denominator");const g=gcd(a,b);return [a/g,b/g];};
  const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const sub=(a,b)=>q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
  const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]);
  const div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
  const sq=a=>mul(a,a);
  const show=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
  const lt=(a,b)=>a[0]*b[1]<b[0]*a[1];
  const avg=a=>div(a.reduce((s,x)=>add(s,x),q(0)),q(a.length));
  const worlds={
    RAMP_NULL:[[0,1,2,3,4,5],[0,0,0,0,0,0]],
    OUTLIER_NULL:[[0,0,0,0,0,12],[0,0,0,0,0,0]],
    RAMP_CONST_TWO:[[0,1,2,3,4,5],[2,2,2,2,2,2]],
    RAMP_SINGLE_HET:[[0,1,2,3,4,5],[0,0,0,0,0,6]],
    RAMP_ZERO_ATE_HET:[[0,1,2,3,4,5],[3,-3,2,-2,1,-1]],
    OUTLIER_HET:[[0,0,0,0,0,12],[0,1,2,3,4,5]]
  };
  const all=[];
  for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)for(let c=b+1;c<6;c++)all.push([a,b,c]);
  if(all.length!==20)throw Error("assignments");
  const policies=["FULL","SYMMETRIC_TOP","ASYMMETRIC"];
  const rows=[], summaries=[];
  const original={"RAMP_NULL":"0","OUTLIER_NULL":"0","RAMP_CONST_TWO":"2","RAMP_SINGLE_HET":"1","RAMP_ZERO_ATE_HET":"0","OUTLIER_HET":"5/2","PAIR_INTERFERENCE":"7/5"};
  for(const world of [...Object.keys(worlds),"PAIR_INTERFERENCE"]){
    const isInterference=world==="PAIR_INTERFERENCE";
    const [y0,tau]=isInterference?[null,null]:worlds[world];
    const ate=isInterference?null:avg(tau.map(qv=>q(qv)));
    const polResults=[];
    for(const policy of policies){
      const vals=[];
      for(const treated of all){
        const z=Array.from({length:6},(_,i)=>treated.includes(i)?1:0);
        const obs=isInterference?z.map((v,i)=>i+2*v+3*z[i^1]):y0.map((v,i)=>v+z[i]*tau[i]);
        let keptT=treated.slice(),keptC=[0,1,2,3,4,5].filter(i=>!treated.includes(i));
        let removedT=null,removedC=null;
        if(policy!=="FULL"){
          removedT=keptT.slice().sort((a,b)=>obs[b]-obs[a]||a-b)[0];
          removedC=keptC.slice().sort((a,b)=>policy==="SYMMETRIC_TOP"?(obs[b]-obs[a]||a-b):(obs[a]-obs[b]||a-b))[0];
          keptT=keptT.filter(i=>i!==removedT);
          keptC=keptC.filter(i=>i!==removedC);
        }
        const v=sub(avg(keptT.map(i=>q(obs[i]))),avg(keptC.map(i=>q(obs[i]))));
        vals.push(v);
        rows.push({world,policy,treated_ids:treated.join("|"),z:z.join("|"),observed_outcomes:obs.join("|"),retained_treated_ids:keptT.join("|"),retained_control_ids:keptC.join("|"),removed_treated_id:removedT===null?"NA":String(removedT),removed_control_id:removedC===null?"NA":String(removedC),source_probability:"1/20",retained_difference:show(v),finite_ATE:isInterference?"NOT_DEFINED_UNDER_INTERFERENCE":show(ate)});
      }
      const expectation=avg(vals), variance=avg(vals.map(v=>sq(sub(v,expectation))));
      const mse=ate===null?null:avg(vals.map(v=>sq(sub(v,ate))));
      const min=vals.reduce((a,b)=>lt(a,b)?a:b),max=vals.reduce((a,b)=>lt(a,b)?b:a);
      polResults.push({policy,expected_contrast:show(expectation),design_variance:show(variance),design_MSE_to_finite_ATE:mse===null?"NOT_DEFINED_UNDER_INTERFERENCE":show(mse),bias_to_finite_ATE:ate===null?"NOT_DEFINED_UNDER_INTERFERENCE":show(sub(expectation,ate)),min_contrast:show(min),max_contrast:show(max),assignments:20});
    }
    if(polResults[0].expected_contrast!==original[world])throw Error("original R210 regression "+world);
    if(!isInterference && polResults[0].bias_to_finite_ATE!=="0")throw Error("FULL not unbiased "+world);
    if(["RAMP_NULL","OUTLIER_NULL","RAMP_CONST_TWO"].includes(world)&&polResults[1].bias_to_finite_ATE!=="0")throw Error("symmetric null/constant");
    if(["RAMP_NULL","OUTLIER_NULL"].includes(world)&&!polResults[2].bias_to_finite_ATE.startsWith("-"))throw Error("asymmetric null bias");
    summaries.push({world,SUTVA_no_interference:!isInterference,finite_ATE:isInterference?"NOT_DEFINED_UNDER_INTERFERENCE":show(ate),controlled_direct_effect:isInterference?"2":"NOT_APPLICABLE",policies:polResults});
  }
  if(rows.length!==420||summaries.length!==7)throw Error("row count");
  const fields=["world","policy","treated_ids","z","observed_outcomes","retained_treated_ids","retained_control_ids","removed_treated_id","removed_control_id","source_probability","retained_difference","finite_ATE"];
  const csv=fields.join(",")+"\n"+rows.map(r=>fields.map(f=>r[f]).join(",")).join("\n")+"\n";
  return {receipt:{schema:"r210_post_assignment_selection_exact_v1",date:"2026-10-27",evidence:"E1_ARTIFICIAL_ONLY",protocol:"protocols/R210_POST_ASSIGNMENT_SELECTION_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",original_r210_status:"UNCHANGED_CLOSED_BOUNDED_E1",assignment_count:20,source_probability:"1/20",world_count:7,selection_rules:policies,row_count:rows.length,real_human_E2:0,historical_E3:0,worlds:summaries},csv,rows};
};
if(require.main===module){const x=study();const prefix=process.argv[2]||"/tmp/r210_selection";fs.writeFileSync(prefix+".json",JSON.stringify(x.receipt,null,2)+"\n");fs.writeFileSync(prefix+".csv",x.csv);console.log(JSON.stringify({rows:x.receipt.row_count,worlds:x.receipt.world_count,prefix}));}
module.exports=study;
