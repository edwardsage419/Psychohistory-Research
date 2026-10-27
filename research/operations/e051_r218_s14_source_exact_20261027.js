#!/usr/bin/env node
// E051 independent exact source audit. Node >=18, no network or external packages.
// Usage: node e051_r218_s14_source_exact_20261027.js original.csv receipt.json
const fs=require("fs"),crypto=require("crypto");
const sha=s=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex");
function audit(csv,receipt){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;};
 const f=s=>{if(Array.isArray(s))return s;let [a,b="1"]=String(s).split("/");a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(b===0n)throw Error("zero denominator");let g=gcd(a,b);return [a/g,b/g];};
 const rat=(a,b)=>f(String(a)+"/"+String(b));
 const add=(x,y)=>{x=f(x);y=f(y);return rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);};
 const sub=(x,y)=>{x=f(x);y=f(y);return rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);};
 const mul=(x,y)=>{x=f(x);y=f(y);return rat(x[0]*y[0],x[1]*y[1]);};
 const div=(x,y)=>{x=f(x);y=f(y);return rat(x[0]*y[1],x[1]*y[0]);};
 const fmt=x=>{x=f(x);return x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);};
 const eq=(x,y)=>fmt(x)===fmt(y);
 let checks=0,slots=0;const check=(v,m)=>{checks++;if(!v)throw Error(m);};
 const [head,...lines]=csv.trim().split(/\r?\n/),keys=head.split(",");
 const rows=lines.map(s=>Object.fromEntries(s.split(",").map((v,i)=>[keys[i],v])));
 check(rows.length===101,"source rows");check(receipt.records.length===303,"receipt rows");
 for(const cond of receipt.conditions){
  const group=rows.filter(r=>r.world===cond.world),clip=f(cond.clip);
  let mean=f(0),second=f(0),mass=f(0),supported=true;
  for(const row of group){
   const z=row.original_8_unit_treatment_assignment.split("|").map(Number);
   const x=row.observed_8_X.split("|").map(Number);
   const y=row.observed_only_actual_8_outcomes.split("|").map(f);
   const ps=row.observable_e_X0_e_X1.split("|").map(f);
   const p=f(row.original_assignment_true_probability_exact);mass=add(mass,p);
   const overlap=ps.every(v=>v[0]>0n&&v[0]<v[1]);let est=null;
   if(overlap){
    let sum=f(0);
    for(let i=0;i<8;i++){
     let q=ps[x[i]],upper=sub(f(1),clip);
     if(clip[0]*q[1]>q[0]*clip[1])q=clip;
     if(q[0]*upper[1]>upper[0]*q[1])q=upper;
     sum=add(sum,z[i]===1?div(y[i],q):mul(f(-1),div(y[i],sub(f(1),q))));
    }
    est=div(sum,f(8));mean=add(mean,mul(p,est));second=add(second,mul(p,mul(est,est)));
    if(cond.clip==="0")check(eq(est,row.observed_X_complete_matching_estimator_exact),"X match");
    if(cond.clip==="1/2")check(eq(est,row.naive_unmatched_observed_difference_exact),"naive match");
   }else supported=false;
   const rec=receipt.records.find(v=>v.world===cond.world&&v.clip===cond.clip&&v.assignment===row.original_8_unit_treatment_assignment);
   check(!!rec,"missing record");
   check(rec.estimate===(est===null?null:fmt(est)),"estimate mismatch");
   check(rec.status===(overlap?"OK":"NO_COMMON_SUPPORT"),"status mismatch");
   check(eq(rec.source_probability,p),"source probability");
   slots++;
  }
  check(eq(mass,1),"probability mass");
  check(group.length===cond.original_assignment_count,"source count");
  check(cond.status===(supported?"OK":"NO_COMMON_SUPPORT"),"condition status");
  if(supported){
   const variance=sub(second,mul(mean,mean)),bias=sub(mean,f(2));
   const mse=add(variance,mul(bias,bias));
   for(const [key,v] of Object.entries({mean,bias,variance,mse}))check(eq(cond[key],v),"moment "+key);
  }else for(const key of ["mean","bias","variance","mse"])check(cond[key]===null,"unsupported must be null");
 }
 return {checks,sourceRows:rows.length,sourceSlots:slots,conditions:receipt.conditions.length,failures:0};
}
if(require.main===module){
 if(process.argv.length!==4)throw Error("usage: node script.js original_R218.csv R218_S14_receipt.json");
 const csv=fs.readFileSync(process.argv[2],"utf8"),rec=fs.readFileSync(process.argv[3],"utf8");
 if(sha(csv)!=="83fc87bc6b82f8e08c10519134d49972168e982d")throw Error("source SHA mismatch");
 if(sha(rec)!=="bfd942dade581726d315e69cb34f3b8dbd24cf56")throw Error("receipt SHA mismatch");
 console.log(JSON.stringify(audit(csv,JSON.parse(rec)),null,2));
}
module.exports={audit};
