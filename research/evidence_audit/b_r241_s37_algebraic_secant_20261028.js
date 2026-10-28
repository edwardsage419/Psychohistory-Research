"use strict";
// R241 S37 B track: algebraic secants computed independently from frozen world formulas.
// Usage: node research/evidence_audit/b_r241_s37_algebraic_secant_20261028.js ORIGINAL.csv S37_RECEIPT.json
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let z=a%b;a=b;b=z;}return a;}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];}
function p(s){if(Array.isArray(s))return s;let m=String(s).match(/^(-?\d+)(?:\/(\d+))?$/);if(!m)throw Error("bad rational "+s);return R(m[1],m[2]||1);}
function plus(a,b){a=p(a);b=p(b);return R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function minus(a,b){a=p(a);b=p(b);return R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function times(a,b){a=p(a);b=p(b);return R(a[0]*b[0],a[1]*b[1]);}
function over(a,b){a=p(a);b=p(b);return R(a[0]*b[1],a[1]*b[0]);}
function sq(a){return times(a,a);}
function cube(a){return times(sq(a),a);}
function eq(a,b){a=p(a);b=p(b);return a[0]===b[0]&&a[1]===b[1];}
function sg(a){a=p(a);return a[0]===0n?0:a[0]<0n?-1:1;}
function mag(a){a=p(a);return R(a[0]<0n?-a[0]:a[0],a[1]);}
function check(v,msg){if(!v)throw Error(msg);}
const A={"DECAY_L1":1,"DECAY_L2":2,"DECAY_HIDDEN_DOUBLE_COORDINATE":1,"CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY":1,"GROWTH_L1":-1,"CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH":-1};
const WORLDS=[...Object.keys(A),"STATIONARY","CONSTANT_RATE_PLUS1","DECAY_NONLINEAR_SENSOR"];
const INITIALS=["1/4","1/2","3/4","1"],TIMES=["0","1/8","1/4","3/8","1/2"];
function D(a,x,t){return plus(1,times(times(a,x),t));}
function visible(w,x,t){
 if(Object.hasOwn(A,w))return over(x,D(A[w],x,t));
 if(w==="STATIONARY")return x;
 if(w==="CONSTANT_RATE_PLUS1")return plus(x,t);
 if(w==="DECAY_NONLINEAR_SENSOR")return sq(over(x,D(1,x,t)));
 throw Error("unknown world");
}
function derivative(w,x,t){
 if(Object.hasOwn(A,w))return over(times(-A[w],sq(x)),sq(D(A[w],x,t)));
 if(w==="STATIONARY")return R(0);
 if(w==="CONSTANT_RATE_PLUS1")return R(1);
 if(w==="DECAY_NONLINEAR_SENSOR")return over(times(-2,cube(x)),cube(D(1,x,t)));
 throw Error("unknown world");
}
function secant(w,x,t,h){
 if(Object.hasOwn(A,w))return over(times(-A[w],sq(x)),times(D(A[w],x,t),D(A[w],x,plus(t,h))));
 if(w==="STATIONARY")return R(0);
 if(w==="CONSTANT_RATE_PLUS1")return R(1);
 if(w==="DECAY_NONLINEAR_SENSOR"){
  const top=times(times(-1,cube(x)),plus(2,times(x,plus(times(2,t),h))));
  return over(top,times(sq(D(1,x,t)),sq(D(1,x,plus(t,h)))));
 }
 throw Error("unknown world");
}
function audit(csv,receipt){
 check(receipt.original_csv_blob_sha==="83ae446308789a88213a4a77d38a23dfcf14167b","source blob");
 check(receipt.prescore_protocol_commit==="eb3cb7dbfcaf090f0c0f879670ded4ab9848d32a","protocol freeze");
 const lines=csv.trimEnd().split(/\r?\n/),header=lines.shift().split(",");
 check(lines.length===180,"original source census");
 let rows=0,derivs=0;const seenSource=new Set();
 for(const line of lines){
  const v=line.split(",");check(v.length===header.length,"csv width");
  const o=Object.fromEntries(header.map((h,i)=>[h,v[i]]));
  const w=o.world,xs=o.observed_cohort_x0,ts=o.observed_time;
  check(WORLDS.includes(w)&&INITIALS.includes(xs)&&TIMES.includes(ts),"source identity");
  const key=[w,xs,ts].join("|");check(!seenSource.has(key),"source duplicate");seenSource.add(key);
  check(eq(visible(w,p(xs),p(ts)),o.observed_y),"observable formula");rows++;
  check(eq(derivative(w,p(xs),p(ts)),o.observed_y_time_derivative),"derivative formula");derivs++;
  check(eq(o.original_source_probability,"1/20"),"mass");
 }
 check(seenSource.size===180,"missing source");
 check(receipt.records.length===360,"record count");
 let comparisons=0,zero=0,nonzero=0;const seenRecords=new Set();
 function validate(rec){
  const {world:w,x:xs,left_t:l,right_t:r,reference_t:ref,method}=rec;
  check(WORLDS.includes(w)&&INITIALS.includes(xs)&&TIMES.includes(l)&&TIMES.includes(r)&&TIMES.includes(ref),"record identity");
  let i=TIMES.indexOf(l),j=TIMES.indexOf(r),k=TIMES.indexOf(ref);
  check((method==="FORWARD_1_8"&&j===i+1&&k===i)||(method==="FORWARD_1_4"&&j===i+2&&k===i)||(method==="CENTER_1_8"&&j===i+2&&k===i+1),"time geometry");
  let key=[w,xs,method,l].join("|");check(!seenRecords.has(key),"record duplicate");seenRecords.add(key);
  let x=p(xs),t=p(l),h=minus(p(r),t),slope=secant(w,x,t,h),d=derivative(w,x,p(ref)),err=minus(slope,d);
  const values=[["span",h],["slope",slope],["analytic_derivative",d],["error",err],["abs_error",mag(err)]];
  for(const [field,value] of values){check(eq(rec[field],value),"algebraic mismatch "+w+" "+method+" "+field);comparisons++;}
  check(rec.sign_agrees===(sg(slope)===sg(d)),"sign mismatch");comparisons++;
  if(sg(err)===0)zero++;else nonzero++;
 }
 for(const rec of receipt.records)validate(rec);
 check(seenRecords.size===360&&comparisons===2160,"record field count");
 check(zero===80&&nonzero===280,"error census");
 let mutant=false;const bad={...receipt.records[0],slope:"999"};
 try{
  const x=p(bad.x),t=p(bad.left_t),h=minus(p(bad.right_t),t);
  check(eq(bad.slope,secant(bad.world,x,t,h)),"mutant rejected");
 }catch(e){mutant=true;}
 check(mutant,"mutant escaped");
 let aliases=0;
 for(const [a,b] of [["DECAY_L1","DECAY_HIDDEN_DOUBLE_COORDINATE"],["DECAY_L1","CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY"],["GROWTH_L1","CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH"]]){
  for(const xs of INITIALS)for(let i=0;i<4;i++){
   check(eq(secant(a,p(xs),p(TIMES[i]),p("1/8")),secant(b,p(xs),p(TIMES[i]),p("1/8"))),"alias");
   aliases++;
  }
 }
 return {research_id:"R241",supplement:"S37",date:"2026-10-28",evidence:"E1_ARTIFICIAL",
  method:"independent algebraic factorization of observed secants",
  source_observation_formula_checks:rows,source_derivative_formula_checks:derivs,
  compared_secant_records:360,compared_secant_fields:comparisons,
  exact_zero_errors:zero,nonzero_errors:nonzero,alias_secant_checks:aliases,
  corrupted_slope_negative_control_detected:mutant,failures:0,
  external_independent_replication:0,new_real_human_E2:0,new_real_historical_E3:0};
}
if(typeof require==="function"&&typeof process==="object"&&require.main===module){
 const fs=require("fs"),[csv,rec]=process.argv.slice(2);
 if(!csv||!rec)throw Error("pass original CSV and S37 R receipt");
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(csv,"utf8"),JSON.parse(fs.readFileSync(rec,"utf8"))),null,2)+"\n");
}
