"use strict";
// Independent finite-population order-statistic audit. Run from repository root: node research/evidence_audit/b_r210_selection_orderstat_independent_20261027.js [receipt-json] [source-csv]
const fs=require("node:fs");
const audit=function audit(receipt,rows){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;};
  const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
  const plus=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const minus=(x,y)=>Q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const times=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
  const over=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
  const str=x=>x[1]===1n?""+x[0]:x[0]+"/"+x[1];
  const mean=a=>Q(a.reduce((s,x)=>s+x,0),a.length);
  const choose2=n=>n<2?0:n*(n-1)/2;
  const extreme=(values,kind)=>{const x=values.slice().sort((a,b)=>a-b);let total=0;for(let k=0;k<6;k++)total+=(kind==="max"?choose2(k):choose2(5-k))*x[k];return Q(total,20);};
  const W={
    RAMP_NULL:[[0,1,2,3,4,5],[0,0,0,0,0,0]],
    OUTLIER_NULL:[[0,0,0,0,0,12],[0,0,0,0,0,0]],
    RAMP_CONST_TWO:[[0,1,2,3,4,5],[2,2,2,2,2,2]],
    RAMP_SINGLE_HET:[[0,1,2,3,4,5],[0,0,0,0,0,6]],
    RAMP_ZERO_ATE_HET:[[0,1,2,3,4,5],[3,-3,2,-2,1,-1]],
    OUTLIER_HET:[[0,0,0,0,0,12],[0,1,2,3,4,5]]
  };
  let comparisons=0,source_checks=0,negative_controls=0,failures=[];
  const independent=[];
  for(const [world,[y0,tau]] of Object.entries(W)){
    const y1=y0.map((v,i)=>v+tau[i]);
    const mu0=mean(y0),mu1=mean(y1);
    const mx0=extreme(y0,"max"),mn0=extreme(y0,"min"),mx1=extreme(y1,"max"),mn1=extreme(y1,"min");
    const expected={
      FULL:minus(mu1,mu0),
      SYMMETRIC_TOP:over(minus(minus(times(Q(3),mu1),mx1),minus(times(Q(3),mu0),mx0)),Q(2)),
      ASYMMETRIC:over(minus(minus(times(Q(3),mu1),mx1),minus(times(Q(3),mu0),mn0)),Q(2))
    };
    const original=receipt.worlds.find(w=>w.world===world);
    if(!original){failures.push("missing "+world);continue;}
    for(const [policy,v] of Object.entries(expected)){
      const recorded=original.policies.find(x=>x.policy===policy)?.expected_contrast;
      comparisons++;
      if(recorded!==str(v))failures.push(world+" "+policy+" "+recorded+" != "+str(v));
      independent.push({world,policy,analytic_expected_contrast:str(v),R_enumeration_expected_contrast:recorded,match:recorded===str(v)});
    }
    const swapped=over(minus(minus(times(Q(3),mu1),mn1),minus(times(Q(3),mu0),mx0)),Q(2));
    if(str(swapped)!==str(expected.ASYMMETRIC))negative_controls++;
    const wrong=plus(expected.ASYMMETRIC,Q(1,20));
    if(str(wrong)!==str(expected.ASYMMETRIC))negative_controls++;
  }
  if(rows.length!==420)failures.push("row count");
  for(const row of rows){
    source_checks++;
    const treated=row.treated_ids.split("|").map(Number);
    const z=row.z.split("|").map(Number);
    const keptT=row.retained_treated_ids.split("|").map(Number);
    const keptC=row.retained_control_ids.split("|").map(Number);
    if(treated.length!==3||new Set(treated).size!==3||z.filter(x=>x===1).length!==3||row.source_probability!=="1/20")failures.push("source assignment "+row.world);
    if(keptT.length!==(row.policy==="FULL"?3:2)||keptC.length!==(row.policy==="FULL"?3:2))failures.push("retention "+row.world);
    if(!keptT.every(i=>treated.includes(i))||!keptC.every(i=>!treated.includes(i)))failures.push("retained arm "+row.world);
  }
  const byWorld=new Map();
  for(const row of rows){const key=row.world+"|"+row.policy;byWorld.set(key,(byWorld.get(key)||0)+1);}
  for(const [key,count] of byWorld)if(count!==20)failures.push("world policy count "+key);
  if(comparisons!==18||source_checks!==420||negative_controls<10||failures.length)throw Error(JSON.stringify({comparisons,source_checks,negative_controls,failures}));
  return {schema:"b_r210_orderstat_internal_exact_audit_v1",date:"2026-10-27",evidence:"INTERNAL_INDEPENDENT_ALGORITHM_E1",analytic_comparisons:comparisons,source_integrity_checks:source_checks,negative_control_detections:negative_controls,failures:0,external_replications:0,world_policy_analytic:independent,scope:"Order statistics analytically check expected contrast only; R enumeration remains sole route for MSE and interference descriptive results; no external reproduction."};
};
function parseCsv(s){const lines=s.trim().split(/\r?\n/);const keys=lines.shift().split(",");return lines.map(line=>{const vals=line.split(",");return Object.fromEntries(keys.map((k,i)=>[k,vals[i]]));});}
if(require.main===module){const p=process.argv[2]||"research/validation/R210_POST_ASSIGNMENT_SELECTION_21_WORLD_POLICY_RECEIPT_2026-10-27.json";const c=process.argv[3]||"research/validation/R210_POST_ASSIGNMENT_SELECTION_420_SOURCE_ROWS_2026-10-27.csv";const out=audit(JSON.parse(fs.readFileSync(p,"utf8")),parseCsv(fs.readFileSync(c,"utf8")));console.log(JSON.stringify(out,null,2));}
module.exports=audit;
