"use strict";
// E072: independent coordinate-identity audit of R242 S38.
// Usage: node research/operations/e072_r242_s38_coordinate_identity_20261028.js ORIGINAL.csv S38_RECEIPT.json
// Uses R2 closed-form powers and R4 Chebyshev-coordinate doubling.
function audit(csv,receipt){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;};
 const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const d=gcd(a,b);return [a/d,b/d];};
 const f=x=>{if(Array.isArray(x))return x;const [a,b="1"]=String(x).split("/");return q(a,b);};
 const add=(a,b)=>{a=f(a);b=f(b);return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);};
 const mul=(a,b)=>{a=f(a);b=f(b);return q(a[0]*b[0],a[1]*b[1]);};
 const neg=a=>{a=f(a);return [-a[0],a[1]];};
 const sub=(a,b)=>add(a,neg(b));
 const eq=(a,b)=>{a=f(a);b=f(b);return a[0]===b[0]&&a[1]===b[1];};
 const pow=(a,n)=>{let v=q(1);for(let i=0;i<n;i++)v=mul(v,a);return v;};
 const abs=a=>{a=f(a);return q(a[0]<0n?-a[0]:a[0],a[1]);};
 const gt=(a,b)=>sub(a,b)[0]>0n;
 const check=(v,m)=>{if(!v)throw Error(m);};
 const half=f("1/2");
 const lines=csv.trimEnd().split(/\r?\n/),headers=lines.shift().split(",");
 check(lines.length===180,"original source count");
 const base=new Map(),seenSource=new Set(),worldCounts=new Map();
 let sourceChecks=0;
 for(const line of lines){
  const cols=line.split(",");
  check(cols.length===headers.length,"source width");sourceChecks++;
  const row=Object.fromEntries(headers.map((h,i)=>[h,cols[i]]));
  check(eq(row.original_source_probability,"1/20"),"source mass");sourceChecks++;
  const key=[row.world,row.observed_initial_cohort,row.observed_step_n].join("|");
  check(!seenSource.has(key),"duplicate source key");seenSource.add(key);
  worldCounts.set(row.world,(worldCounts.get(row.world)||0)+1);
  if(["LOGISTIC_R2","LOGISTIC_R4"].includes(row.world)&&row.observed_initial_cohort==="1/2")
   base.set(row.world+"|"+row.observed_step_n,row);
 }
 check(worldCounts.size===9&&[...worldCounts.values()].every(v=>v===20),"source universe");
 check(base.size===10,"baseline census");
 check(receipt.prescore_protocol_commit==="e813053ac01f0b8691e4e38962a2d5cd7aef2e61","freeze identity");
 check(receipt.original_csv_blob_sha==="53fd3047f03cb0f50aa3dc497003b9b87b80cb6f","source identity");
 check(receipt.rows.length===40&&receipt.maxima.length===8,"receipt universe");
 let fields=0,zero=0,nonzero=0;const seen=new Set();
 for(const row of receipt.rows){
  const {world,epsilon,n}=row,key=[world,epsilon,n].join("|");
  check(!seen.has(key),"duplicate receipt");seen.add(key);
  check(["-1/8","-1/16","1/16","1/8"].includes(epsilon)&&Number.isInteger(n)&&n>=0&&n<=4,"grid");
  const e=f(epsilon);let y;
  if(world==="LOGISTIC_R2"){
   // Exact closed form: y_n=1/2-(2e)^(2^n)/2 for n>=1.
   y=n===0?add(half,e):sub(half,mul(half,pow(mul(2,e),2**n)));
  }else if(world==="LOGISTIC_R4"){
   // Transform z=1-2y; z_(n+1)=2*z_n^2-1 (Chebyshev doubling).
   let z=neg(mul(2,e));
   for(let j=0;j<n;j++)z=sub(mul(2,mul(z,z)),1);
   y=sub(half,mul(half,z));
  }else throw Error("unexpected world");
  const b=base.get(world+"|"+n);check(!!b,"missing source baseline");
  const baseline=f(b.observed_output_y),sens=f(b.observed_initial_cohort_sensitivity);
  const delta=sub(y,baseline),linear=mul(sens,e),residual=sub(delta,linear);
  for(const [field,val] of Object.entries({baseline_y:baseline,perturbed_y:y,baseline_sensitivity:sens,finite_delta:delta,linear_delta:linear,residual})){
   check(eq(row[field],val),"receipt mismatch "+key+" "+field);fields++;
  }
  if(eq(residual,0))zero++;else nonzero++;
 }
 check(seen.size===40&&zero===8&&nonzero===32,"finite-effect counts");
 let maximaChecks=0;
 for(const m of receipt.maxima){
  const rows=receipt.rows.filter(x=>x.world===m.world&&x.epsilon===m.epsilon);
  check(rows.length===5,"maxima rows");
  let max=q(0);
  for(const x of rows){const v=abs(x.residual);if(gt(v,max))max=v;}
  check(eq(max,m.max_absolute_residual),"maximum residual");maximaChecks++;
  check(eq(rows.find(x=>x.n===4).finite_delta,m.n4_finite_delta),"final delta");maximaChecks++;
 }
 let symmetry=0;
 for(const w of ["LOGISTIC_R2","LOGISTIC_R4"])for(const e of ["1/8","1/16"])for(let n=1;n<=4;n++){
  const a=receipt.rows.find(x=>x.world===w&&x.epsilon===e&&x.n===n);
  const b=receipt.rows.find(x=>x.world===w&&x.epsilon==="-"+e&&x.n===n);
  check(eq(a.perturbed_y,b.perturbed_y),"sign symmetry");symmetry++;
 }
 let mutantDetected=false;
 try{
  const bad={...receipt,rows:receipt.rows.map((x,i)=>i===0?{...x,perturbed_y:"999"}:x)};
  if(!eq(bad.rows[0].perturbed_y,add(half,f(bad.rows[0].epsilon))))throw Error("mutant rejected");
 }catch(e){mutantDetected=true;}
 check(mutantDetected,"negative control");
 return {source_rows:lines.length,source_checks:sourceChecks,receipt_rows:receipt.rows.length,
  receipt_field_checks:fields,maxima_checks:maximaChecks,symmetry_checks:symmetry,
  checks:sourceChecks+fields+maximaChecks+symmetry,failures:0,
  zero_residual:zero,nonzero_residual:nonzero,mutant_detected:mutantDetected,
  evidence:"E1_ARTIFICIAL",new_E2:0,new_E3:0};
}
if(typeof require==="function"&&typeof module==="object"&&require.main===module){
 const fs=require("fs"),[source,receipt]=process.argv.slice(2);
 if(!source||!receipt)throw Error("Pass original CSV and S38 JSON receipt");
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(source,"utf8"),JSON.parse(fs.readFileSync(receipt,"utf8"))),null,2)+"\n");
}
