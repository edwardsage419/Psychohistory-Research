#!/usr/bin/env node
// Deterministic R218 S14 exact rational source enumeration; node >=18.
const fs=require("fs");
function compute(csv){
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n};
const F=x=>{if(typeof x==="object"&&x.n!==undefined)return x;let s=String(x).split("/");let n=BigInt(s[0]),d=BigInt(s[1]||"1");if(d<0n){n=-n;d=-d;}if(d===0n)throw Error("zero denominator");let g=gcd(n,d);return {n:n/g,d:d/g}};
const A=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d+y.n*x.d)+"/"+(x.d*y.d))};
const N=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d-y.n*x.d)+"/"+(x.d*y.d))};
const M=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.n)+"/"+(x.d*y.d))};
const D=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d)+"/"+(x.d*y.n))};
const S=x=>{x=F(x);return x.d===1n?String(x.n):x.n+"/"+x.d};
const eq=(x,y)=>S(x)===S(y),zero=F(0),one=F(1);
const lines=csv.trim().split(/\r?\n/);const hdr=lines.shift().split(",");
const rows=lines.map(l=>{let parts=l.split(",");if(parts.length!==hdr.length)throw Error("bad CSV column count");return Object.fromEntries(hdr.map((h,i)=>[h,parts[i]]))});
if(rows.length!==101)throw Error("original 101 missing");
const worlds=[...new Set(rows.map(r=>r.world))];
if(worlds.length!==6)throw Error("world count mismatch");
const clips=["0","1/3","1/2"],records=[],conditions=[];
let nRawMatch=0,nHalfNaive=0,nBalanced=0,slots=0;
for(const w of worlds){
 const wr=rows.filter(r=>r.world===w);
 const mass=wr.reduce((s,r)=>A(s,F(r.original_assignment_true_probability_exact)),zero);
 if(!eq(mass,one))throw Error("source mass mismatch "+w);
 for(const clip of clips){
  const c=F(clip), vals=[];let valid=true;
  for(const r of wr){
   const z=r.original_8_unit_treatment_assignment.split("|").map(Number);
   const x=r.observed_8_X.split("|").map(Number);
   const y=r.observed_only_actual_8_outcomes.split("|").map(F);
   const e=r.observable_e_X0_e_X1.split("|").map(F);
   if(z.length!==8||x.length!==8||y.length!==8||e.length!==2)throw Error("bad original row");
   const overlap=e.every(t=>t.n>0n&&t.n<t.d);
   let estimate=null;
   if(overlap){
    let sum=zero;
    for(let i=0;i<8;i++){
     let p=e[x[i]];
     if(p.n*c.d<c.n*p.d)p=c;
     const upper=N(one,c);
     if(p.n*upper.d>upper.n*p.d)p=upper;
     const term=z[i]===1?D(y[i],p):M(F(-1),D(y[i],N(one,p)));
     sum=A(sum,term);
    }
    estimate=D(sum,F(8));
    if(clip==="0"){if(!eq(estimate,F(r.observed_X_complete_matching_estimator_exact)))throw Error("unclipped matching identity fails");nRawMatch++}
    if(clip==="1/2"){if(!eq(estimate,F(r.naive_unmatched_observed_difference_exact)))throw Error("half naive identity fails");nHalfNaive++}
    if(w==="BALANCED_QUOTA_NEG_CONTROL"){if(!eq(estimate,F(r.naive_unmatched_observed_difference_exact)))throw Error("balanced invariant fails");nBalanced++}
    vals.push([estimate,F(r.original_assignment_true_probability_exact)]);
   }else valid=false;
   records.push({world:w,clip,assignment:r.original_8_unit_treatment_assignment,source_probability:r.original_assignment_true_probability_exact,estimate:estimate===null?null:S(estimate),status:overlap?"OK":"NO_COMMON_SUPPORT"});
   slots++;
  }
  if(valid&&vals.length!==wr.length)throw Error("mixed overlap");
  let mean=null,variance=null,mse=null,bias=null;
  if(valid){
   mean=vals.reduce((s,[v,p])=>A(s,M(v,p)),zero);
   variance=vals.reduce((s,[v,p])=>A(s,M(p,M(N(v,mean),N(v,mean)))),zero);
   bias=N(mean,F(2));mse=A(variance,M(bias,bias));
  }
  conditions.push({world:w,clip,original_assignment_count:wr.length,source_mass:S(mass),status:valid?"OK":"NO_COMMON_SUPPORT",mean:valid?S(mean):null,bias:valid?S(bias):null,variance:valid?S(variance):null,mse:valid?S(mse):null});
 }
}
if(slots!==303||nRawMatch!==100||nHalfNaive!==100||nBalanced!==108)throw Error("precommitted counts fail: "+[slots,nRawMatch,nHalfNaive,nBalanced]);
const mut=rows.find(r=>r.world==="RANDOM_X_CONFOUNDED");
const z=mut.original_8_unit_treatment_assignment.split("|").map(Number);
const x=mut.observed_8_X.split("|").map(Number);
const e=mut.observable_e_X0_e_X1.split("|").map(F);
const before=F(records.find(r=>r.world===mut.world&&r.clip==="0"&&r.assignment===mut.original_8_unit_treatment_assignment).estimate);
const changed=A(before,D(F(z[0]===1?1:-1),M(F(8),z[0]===1?e[x[0]]:N(one,e[x[0]]))));
if(eq(before,changed))throw Error("mutation failed");
return {research:"R218_S14",evidence:"E1_ARTIFICIAL",frozen_protocol:"protocols/R218_S14_OBSERVED_PROPENSITY_CLIPPING_PRESCORE_FREEZE_2026-10-27.md",original_csv_blob:"83fc87bc6b82f8e08c10519134d49972168e982d",worlds:6,source_rows:101,source_slots:slots,valid_slots:300,unsupported_slots:3,conditions,records,checks:{raw_equals_X_matching_rows:nRawMatch,half_equals_naive_rows:nHalfNaive,balanced_invariance_rows:nBalanced,observed_outcome_mutation_detected:!eq(before,changed)},new_E2:0,new_E3:0};

}
if(require.main===module){if(!process.argv[2])throw Error("usage: node script.js original_R218.csv");process.stdout.write(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}
module.exports={compute};
