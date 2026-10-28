"use strict";
// R242 S38 B track: exact polynomial composition, independent of R's pointwise recurrence.
// Usage: node research/evidence_audit/b_r242_s38_polynomial_composition_20261028.js ORIGINAL.csv S38_RECEIPT.json
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];}
function f(s){if(Array.isArray(s))return s;let m=String(s).match(/^(-?\d+)(?:\/(\d+))?$/);if(!m)throw Error("bad rational "+s);return q(m[1],m[2]||1);}
function add(a,b){a=f(a);b=f(b);return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){a=f(a);b=f(b);return q(a[0]*b[0],a[1]*b[1]);}
function neg(a){a=f(a);return q(-a[0],a[1]);}
function sub(a,b){return add(a,neg(b));}
function eq(a,b){a=f(a);b=f(b);return a[0]===b[0]&&a[1]===b[1];}
function check(v,m){if(!v)throw Error(m);}
function polySquare(a){let out=Array(2*a.length-1).fill(0n);for(let i=0;i<a.length;i++)for(let j=0;j<a.length;j++)out[i+j]+=a[i]*a[j];return out;}
function polyNext(a,r){let b=polySquare(a),out=[];for(let i=0;i<b.length;i++)out.push(BigInt(r)*((a[i]||0n)-b[i]));return out;}
function horner(coeff,x){let v=q(0);for(let i=coeff.length-1;i>=0;i--)v=add(mul(v,x),q(coeff[i]));return v;}
function derivativeCoefficients(a){return a.slice(1).map((z,i)=>z*BigInt(i+1));}
function audit(csv,receipt){
 check(receipt.prescore_protocol_commit==="e813053ac01f0b8691e4e38962a2d5cd7aef2e61","freeze");
 check(receipt.original_csv_blob_sha==="53fd3047f03cb0f50aa3dc497003b9b87b80cb6f","source blob");
 let lines=csv.trimEnd().split(/\r?\n/),header=lines.shift().split(",");
 check(lines.length===180,"source count");
 let originals=new Map();
 for(const line of lines){
  let v=line.split(",");check(v.length===header.length,"source width");
  let row=Object.fromEntries(header.map((h,i)=>[h,v[i]]));
  if(["LOGISTIC_R2","LOGISTIC_R4"].includes(row.world)&&row.observed_initial_cohort==="1/2"){
   let key=row.world+"|"+row.observed_step_n;check(!originals.has(key),"duplicate baseline");
   originals.set(key,row);
  }
 }
 check(originals.size===10,"baseline count");
 const polys={};
 for(const [w,r] of [["LOGISTIC_R2",2],["LOGISTIC_R4",4]]){
  let a=[0n,1n];polys[w]=[a];
  for(let n=1;n<=4;n++){a=polyNext(a,r);polys[w].push(a);}
 }
 let sourceChecks=0;
 for(const w of Object.keys(polys))for(let n=0;n<=4;n++){
  const row=originals.get(w+"|"+n),poly=polys[w][n];
  check(eq(horner(poly,f("1/2")),row.observed_output_y),"baseline polynomial");
  check(eq(horner(derivativeCoefficients(poly),f("1/2")),row.observed_initial_cohort_sensitivity),"baseline derivative");
  sourceChecks+=2;
 }
 check(receipt.rows.length===40,"receipt count");
 let fieldChecks=0,nonzero=0,zero=0;
 for(const row of receipt.rows){
  const {world:w,epsilon:e,n}=row;
  check(Object.hasOwn(polys,w)&&["-1/8","-1/16","1/16","1/8"].includes(e)&&Number.isInteger(n)&&n>=0&&n<=4,"perturbation grid");
  const P=polys[w][n],x=f("1/2"),xp=add(x,f(e));
  const base=horner(P,x),perturbed=horner(P,xp),sensitivity=horner(derivativeCoefficients(P),x);
  const delta=sub(perturbed,base),linear=mul(sensitivity,f(e)),residual=sub(delta,linear);
  for(const [field,value] of [["baseline_y",base],["perturbed_y",perturbed],["baseline_sensitivity",sensitivity],
    ["finite_delta",delta],["linear_delta",linear],["residual",residual]]){
   check(eq(row[field],value),"polynomial mismatch "+w+" "+e+" "+n+" "+field);fieldChecks++;
  }
  if(eq(residual,0))zero++;else nonzero++;
 }
 check(fieldChecks===240&&zero===8&&nonzero===32,"field census");
 let symmetry=0;
 for(const w of Object.keys(polys))for(const m of ["1/8","1/16"])for(let n=1;n<=4;n++){
  const P=polys[w][n],x=f("1/2");
  check(eq(horner(P,add(x,f(m))),horner(P,sub(x,f(m)))),"polynomial symmetry");
  symmetry++;
 }
 let mutationDetected=false;
 try{
  const bad={...receipt.rows[0],perturbed_y:"999"};
  const expected=horner(polys[bad.world][bad.n],add(f("1/2"),f(bad.epsilon)));
  check(eq(bad.perturbed_y,expected),"mutant rejected");
 }catch(e){mutationDetected=true;}
 check(mutationDetected,"mutant not detected");
 return {research_id:"R242",supplement:"S38",date:"2026-10-28",evidence:"E1_ARTIFICIAL",
  method:"integer polynomial coefficient composition and Horner evaluation",
  original_baseline_polynomial_checks:sourceChecks,perturbation_rows:40,compared_fields:fieldChecks,
  exact_linearization_rows:zero,nonzero_finite_residual_rows:nonzero,
  positive_negative_symmetry_checks:symmetry,corrupted_perturbation_negative_control_detected:mutationDetected,
  failures:0,external_independent_replication:0,new_real_human_E2:0,new_real_historical_E3:0};
}
if(typeof require==="function"&&typeof process==="object"&&require.main===module){
 const fs=require("fs"),[csv,rec]=process.argv.slice(2);
 if(!csv||!rec)throw Error("pass original CSV and R receipt");
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(csv,"utf8"),JSON.parse(fs.readFileSync(rec,"utf8"))),null,2)+"\n");
}
