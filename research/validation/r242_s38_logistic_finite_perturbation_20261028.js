"use strict";
// R242 S38: four exact off-grid perturbations, preserving all 180 original R242 source rows.
// Usage: node research/validation/r242_s38_logistic_finite_perturbation_20261028.js ORIGINAL.csv
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return {a:a/g,b:b/g};}
function F(s){if(typeof s==="object"&&s&&"a" in s)return s;let m=String(s).match(/^(-?\d+)(?:\/(\d+))?$/);if(!m)throw Error("bad rational "+s);return Q(m[1],m[2]||1);}
function plus(a,b){a=F(a);b=F(b);return Q(a.a*b.b+b.a*a.b,a.b*b.b);}
function neg(a){a=F(a);return Q(-a.a,a.b);}
function sub(a,b){return plus(a,neg(b));}
function mul(a,b){a=F(a);b=F(b);return Q(a.a*b.a,a.b*b.b);}
function div(a,b){a=F(a);b=F(b);return Q(a.a*b.b,a.b*b.a);}
function st(a){a=F(a);return a.b===1n?""+a.a:a.a+"/"+a.b;}
function eq(a,b){return st(a)===st(b);}
function abs(a){a=F(a);return Q(a.a<0n?-a.a:a.a,a.b);}
function cmp(a,b){return sub(a,b).a<0n?-1:sub(a,b).a>0n?1:0;}
function assert(x,msg){if(!x)throw Error(msg);}
const WORLDS=["LOGISTIC_R2","LOGISTIC_R4"],EPS=["-1/8","-1/16","1/16","1/8"];
function iterate(r,x){return mul(mul(r,x),sub(1,x));}
function run(csv){
 const lines=csv.trimEnd().split(/\r?\n/),headers=lines.shift().split(",");
 assert(lines.length===180,"source census");
 const seen=new Set(),base=new Map(),perWorld=new Map();
 for(const line of lines){
  const parts=line.split(",");assert(parts.length===headers.length,"source width");
  const row=Object.fromEntries(headers.map((h,i)=>[h,parts[i]]));
  const w=row.world,x=row.observed_initial_cohort,n=row.observed_step_n;
  const key=[w,x,n].join("|");assert(!seen.has(key),"source duplicate");seen.add(key);
  assert(eq(row.original_source_probability,"1/20"),"source probability");
  perWorld.set(w,(perWorld.get(w)||0)+1);
  if(WORLDS.includes(w)&&x==="1/2")base.set([w,n].join("|"),row);
 }
 assert(seen.size===180&&perWorld.size===9&&[...perWorld.values()].every(n=>n===20),"world source coverage");
 assert(base.size===10,"baseline source count");
 const rows=[];
 for(const w of WORLDS)for(const e of EPS){
  let x=plus("1/2",e),r=w==="LOGISTIC_R2"?2:4,y=x;
  for(let n=0;n<=4;n++){
   const original=base.get([w,n].join("|"));assert(original,"missing baseline");
   const baseline=F(original.observed_output_y),sensitivity=F(original.observed_initial_cohort_sensitivity);
   const delta=sub(y,baseline),linear=mul(sensitivity,e),residual=sub(delta,linear);
   rows.push({world:w,epsilon:e,n,baseline_y:st(baseline),perturbed_y:st(y),
    baseline_sensitivity:st(sensitivity),finite_delta:st(delta),linear_delta:st(linear),
    residual:st(residual)});
   if(n===0){assert(eq(sensitivity,1)&&eq(residual,0),"n0 linearization");}
   else{assert(eq(sensitivity,0)&&!eq(delta,0)&&!eq(residual,0),"nonzero finite effect after zero derivative");}
   if(n<4)y=iterate(r,y);
  }
 }
 assert(rows.length===40,"perturbation grid count");
 let symmetry=0;
 for(const w of WORLDS)for(const m of ["1/16","1/8"])for(let n=1;n<=4;n++){
  const a=rows.find(z=>z.world===w&&z.epsilon===m&&z.n===n);
  const b=rows.find(z=>z.world===w&&z.epsilon==="-"+m&&z.n===n);
  assert(a.perturbed_y===b.perturbed_y,"sign symmetry violation");
  symmetry++;
 }
 function at(w,e,n){return rows.find(z=>z.world===w&&z.epsilon===e&&z.n===n);}
 assert(at("LOGISTIC_R4","1/8",1).finite_delta==="-1/16","R4 step1");
 assert(at("LOGISTIC_R4","1/8",2).finite_delta==="15/64","R4 step2");
 const maxima=[];
 for(const w of WORLDS)for(const e of EPS){
  let z=rows.filter(v=>v.world===w&&v.epsilon===e);
  let mx=z.map(v=>abs(v.residual)).reduce((a,b)=>cmp(a,b)>0?a:b,Q(0));
  maxima.push({world:w,epsilon:e,max_absolute_residual:st(mx),n4_finite_delta:z[4].finite_delta});
 }
 return {research_id:"R242",supplement:"S38",date:"2026-10-28",evidence:"E1_ARTIFICIAL",
  prescore_protocol_commit:"e813053ac01f0b8691e4e38962a2d5cd7aef2e61",
  original_csv_blob_sha:"53fd3047f03cb0f50aa3dc497003b9b87b80cb6f",
  original_source_rows:180,perturbation_worlds:2,perturbations_per_world:4,
  perturbed_timepoints:40,exact_linearization_n0:8,
  nonzero_finite_effect_with_zero_linear_derivative:32,sign_symmetric_future_pairs:16,
  maxima,rows,new_real_human_E2:0,new_real_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
}
if(typeof require==="function"&&typeof process==="object"&&require.main===module){
 const fs=require("fs");if(!process.argv[2])throw Error("pass original R242 CSV");
 process.stdout.write(JSON.stringify(run(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");
}
