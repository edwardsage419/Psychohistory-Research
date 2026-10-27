"use strict";
// Offline, deterministic third-route source-level audit. Node 18+ standard library.
const fs=require("node:fs");
function audit(csv,receipt){
 const F=s=>{if(typeof s==="number")s=String(s);const p=s.split("/");return [BigInt(p[0]),BigInt(p[1]||1)]};
 const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
 const norm=([a,b])=>{if(b<0n){a=-a;b=-b}const d=gcd(a,b);return [a/d,b/d]};
 const add=(a,b)=>norm([a[0]*b[1]+b[0]*a[1],a[1]*b[1]]);
 const sub=(a,b)=>norm([a[0]*b[1]-b[0]*a[1],a[1]*b[1]]);
 const mul=(a,b)=>norm([a[0]*b[0],a[1]*b[1]]);
 const div=(a,b)=>norm([a[0]*b[1],a[1]*b[0]]);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
 const str=a=>a[1]===1n?String(a[0]):`${a[0]}/${a[1]}`;
 const sum=arr=>arr.reduce((a,b)=>add(a,b),F(0));
 const worlds={RAMP_NULL:{y:[0,1,2,3,4,5],t:[0,0,0,0,0,0]},OUTLIER_NULL:{y:[0,0,0,0,0,12],t:[0,0,0,0,0,0]},RAMP_CONST_TWO:{y:[0,1,2,3,4,5],t:[2,2,2,2,2,2]},RAMP_SINGLE_HET:{y:[0,1,2,3,4,5],t:[0,0,0,0,0,6]},RAMP_ZERO_ATE_HET:{y:[0,1,2,3,4,5],t:[3,-3,2,-2,1,-1]},OUTLIER_HET:{y:[0,0,0,0,0,12],t:[0,1,2,3,4,5]},PAIR_INTERFERENCE:null};
 let assertions=0,errors=[],rows=csv.trim().split(/\r?\n/),head=rows.shift().split(","),groups=new Map(),seen=new Set();
 function check(ok,label){assertions++;if(!ok&&errors.length<12)errors.push(label)}
 check(rows.length===420,"rowcount");
 const expectedCombinations=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)for(let k=j+1;k<6;k++)expectedCombinations.push(`${i}|${j}|${k}`);
 for(const line of rows){const v=line.split(",");check(v.length===head.length,"column-count");const r=Object.fromEntries(head.map((k,i)=>[k,v[i]]));const z=r.z.split("|").map(Number),treated=z.map((x,i)=>x?i:-1).filter(x=>x>=0),control=z.map((x,i)=>x?-1:i).filter(x=>x>=0),key=r.world+"|"+r.policy,sourceKey=key+"|"+r.treated_ids;
 check(expectedCombinations.includes(r.treated_ids),"assignment "+sourceKey);
 check(!seen.has(sourceKey),"duplicate "+sourceKey);seen.add(sourceKey);
 check(treated.join("|")===r.treated_ids,"treated-ids "+sourceKey);
 check(treated.length===3&&control.length===3,"arm size "+sourceKey);
 const w=worlds[r.world];check(w!==undefined,"world "+r.world);
 const obs=z.map((x,i)=>w?(w.y[i]+x*w.t[i]):(i+2*x+3*z[i%2===0?i+1:i-1]));
 check(obs.join("|")===r.observed_outcomes,"observed "+sourceKey);
 const sorted=(ids,mode)=>[...ids].sort((i,j)=>mode==="max"?(obs[j]-obs[i]||i-j):(obs[i]-obs[j]||i-j));
 const removedT=r.policy==="FULL"?null:sorted(treated,"max")[0];
 const removedC=r.policy==="FULL"?null:sorted(control,r.policy==="ASYMMETRIC"?"min":"max")[0];
 const rt=treated.filter(i=>i!==removedT),rc=control.filter(i=>i!==removedC);
 check(rt.join("|")===r.retained_treated_ids,"retained treated "+sourceKey);
 check(rc.join("|")===r.retained_control_ids,"retained control "+sourceKey);
 check((removedT===null?"NA":String(removedT))===r.removed_treated_id,"removed treated "+sourceKey);
 check((removedC===null?"NA":String(removedC))===r.removed_control_id,"removed control "+sourceKey);
 const d=sub(div(F(rt.reduce((s,i)=>s+obs[i],0)),F(rt.length)),div(F(rc.reduce((s,i)=>s+obs[i],0)),F(rc.length)));
 check(eq(d,F(r.retained_difference)),"contrast "+sourceKey);
 check(r.source_probability==="1/20","probability "+sourceKey);
 const ate=w?div(F(w.t.reduce((a,b)=>a+b,0)),F(6)):null;
 check(r.finite_ATE===(ate?str(ate):"NOT_DEFINED_UNDER_INTERFERENCE"),"ATE "+sourceKey);
 if(!groups.has(key))groups.set(key,[]);groups.get(key).push(d);
 }
 check(groups.size===21,"group-count");
 const summary=[];
 for(const w of receipt.worlds)for(const p of w.policies){const key=w.world+"|"+p.policy,vals=groups.get(key)||[];check(vals.length===20,"20 assignments "+key);if(vals.length!==20)continue;
 const mu=div(sum(vals),F(20)),varr=div(sum(vals.map(x=>mul(sub(x,mu),sub(x,mu)))),F(20)),minimum=vals.reduce((a,b)=>cmp(a,b)<=0n?a:b),maximum=vals.reduce((a,b)=>cmp(a,b)>=0n?a:b);
 check(eq(mu,F(p.expected_contrast)),"expected "+key);check(eq(varr,F(p.design_variance)),"variance "+key);
 check(eq(minimum,F(p.min_contrast)),"minimum "+key);check(eq(maximum,F(p.max_contrast)),"maximum "+key);
 if(w.SUTVA_no_interference){const ate=F(w.finite_ATE),bias=sub(mu,ate),mse=div(sum(vals.map(x=>mul(sub(x,ate),sub(x,ate)))),F(20));check(eq(bias,F(p.bias_to_finite_ATE)),"bias "+key);check(eq(mse,F(p.design_MSE_to_finite_ATE)),"MSE "+key);}
 else {check(p.bias_to_finite_ATE==="NOT_DEFINED_UNDER_INTERFERENCE","interference bias flag");check(p.design_MSE_to_finite_ATE==="NOT_DEFINED_UNDER_INTERFERENCE","interference MSE flag")}
 summary.push({world:w.world,policy:p.policy,expected:str(mu),variance:str(varr)});
 }
 return {assertions,errors,rows:rows.length,groups:groups.size,summary:summary.filter(x=>x.policy==="ASYMMETRIC")};
}
const result=audit(fs.readFileSync("research/validation/R210_POST_ASSIGNMENT_SELECTION_420_SOURCE_ROWS_2026-10-27.csv","utf8"),JSON.parse(fs.readFileSync("research/validation/R210_POST_ASSIGNMENT_SELECTION_21_WORLD_POLICY_RECEIPT_2026-10-27.json","utf8")));
if(result.errors.length||result.assertions!==6029)throw new Error(JSON.stringify(result));
console.log(JSON.stringify(result,null,2));
