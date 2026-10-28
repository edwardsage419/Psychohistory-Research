"use strict";
// R251 S47 source-first exact audit. Node >=18, standard library only.
// Usage: node research/validation/r251_s47_finite_window_exact_20261029.js [source_csv]
const WORLDS=["HALF_CONTRACTION","NEGATIVE_HALF_CONTRACTION","ZERO_MAP","DOUBLE_EXPANSION","IDENTITY_NEUTRAL","SIGN_FLIP_NEUTRAL","CUBIC_LOCAL_INWARD","CUBIC_OUTWARD","LOGISTIC_R3_CENTERED"];
const INITIALS=["-1/2","-1/4","-1/12","-1/24","0","1/24","1/12","1/4","1/2"];
const Z=[0n,1n],ONE=[1n,1n];
function gcd(a,b){a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t;}return a||1n}
function frac(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
function parse(s){let t=s.split("/");return frac(t[0],t[1]||1)}
function repr(x){return x[1]===1n?""+x[0]:x[0]+"/"+x[1]}
function add(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function neg(a){return [-a[0],a[1]]}
function sub(a,b){return add(a,neg(b))}
function mul(a,b){return frac(a[0]*b[0],a[1]*b[1])}
function sq(a){return mul(a,a)}
function cmp(a,b){let d=a[0]*b[1]-b[0]*a[1];return d<0n?-1:d>0n?1:0}
function abs(a){return [a[0]<0n?-a[0]:a[0],a[1]]}
function sign(a){let x=cmp(a,Z);return x<0?"-":x>0?"+":"0"}
function map(w,x){if(w==="HALF_CONTRACTION")return mul(x,frac(1,2));if(w==="NEGATIVE_HALF_CONTRACTION")return mul(x,frac(-1,2));if(w==="ZERO_MAP")return Z;if(w==="DOUBLE_EXPANSION")return mul(x,frac(2));if(w==="IDENTITY_NEUTRAL")return x;if(w==="SIGN_FLIP_NEUTRAL")return neg(x);if(w==="CUBIC_LOCAL_INWARD")return sub(x,mul(sq(x),x));if(w==="CUBIC_OUTWARD")return add(x,mul(sq(x),x));if(w==="LOGISTIC_R3_CENTERED")return sub(neg(x),mul(frac(3),sq(x)));throw Error("world")}
function deriv(w,x){if(w==="HALF_CONTRACTION")return frac(1,2);if(w==="NEGATIVE_HALF_CONTRACTION")return frac(-1,2);if(w==="ZERO_MAP")return Z;if(w==="DOUBLE_EXPANSION")return frac(2);if(w==="IDENTITY_NEUTRAL")return ONE;if(w==="SIGN_FLIP_NEUTRAL")return frac(-1);if(w==="CUBIC_LOCAL_INWARD")return sub(ONE,mul(frac(3),sq(x)));if(w==="CUBIC_OUTWARD")return add(ONE,mul(frac(3),sq(x)));if(w==="LOGISTIC_R3_CENTERED")return sub(frac(-1),mul(frac(6),x));throw Error("world")}
function run(csv){
 let lines=csv.trim().split(/\r?\n/),headers=lines.shift().split(",");
 if(lines.length!==405)throw Error("source count");
 const required=["world","original_initial_x0","original_time_n","observed_state_xn","observed_positive_candidate_Vn","observed_next_state_fx","observed_one_step_delta_V","observed_local_derivative_fprime","observed_initial_sensitivity_Dn","original_structural_source_mass"];
 if(JSON.stringify(headers)!==JSON.stringify(required))throw Error("header");
 let data=Object.fromEntries(WORLDS.map(w=>[w,new Map()])),checks=0;
 for(const line of lines){
  let cells=line.split(",");if(cells.length!==headers.length)throw Error("columns");
  let r=Object.fromEntries(headers.map((h,i)=>[h,cells[i]])),w=r.world,x0=r.original_initial_x0,t=Number(r.original_time_n);
  if(!data[w]||!INITIALS.includes(x0)||!Number.isInteger(t)||t<0||t>4)throw Error("unfrozen key");
  let key=x0+"|"+t;if(data[w].has(key))throw Error("duplicate source");
  let x=parse(x0),D=ONE;for(let j=0;j<t;j++){D=mul(D,deriv(w,x));x=map(w,x)}
  let next=map(w,x),expected={
   observed_state_xn:x,observed_positive_candidate_Vn:sq(x),observed_next_state_fx:next,
   observed_one_step_delta_V:sub(sq(next),sq(x)),observed_local_derivative_fprime:deriv(w,x),
   observed_initial_sensitivity_Dn:D,original_structural_source_mass:frac(1,45)
  };
  for(const [field,val] of Object.entries(expected)){if(cmp(parse(r[field]),val)!==0)throw Error("field "+field+" "+key+" "+w);checks++}
  data[w].set(key,r);
 }
 let worlds=[];
 for(const w of WORLDS){
  let rr=data[w];if(rr.size!==45)throw Error("world source count");
  let delta={negative:0,zero:0,positive:0},strict4=0,net4={shrink:0,equal:0,grow:0},local={count:0,strict4:0,net4_shrink:0},cohorts=[];
  for(const x0 of INITIALS)for(let t=0;t<5;t++){
   let r=rr.get(x0+"|"+t);if(!r)throw Error("missing source");
   let s=sign(parse(r.observed_one_step_delta_V));delta[s==="-"?"negative":s==="+"?"positive":"zero"]++;
  }
  for(const x0 of INITIALS.filter(x=>x!=="0")){
   let rows=[0,1,2,3,4].map(t=>rr.get(x0+"|"+t));
   let signs=rows.slice(0,4).map(r=>sign(parse(r.observed_one_step_delta_V))).join("");
   let strict=signs==="----";if(strict)strict4++;
   let d=cmp(abs(parse(rows[4].observed_state_xn)),abs(parse(x0)));
   let cls=d<0?"shrink":d>0?"grow":"equal";net4[cls]++;
   let isLocal=cmp(abs(parse(x0)),frac(1,12))<=0;
   if(isLocal){local.count++;local.strict4+=Number(strict);local.net4_shrink+=Number(cls==="shrink")}
   cohorts.push({x0,delta_signs_t0_t3:signs,strict4:strict,net4:cls});
  }
  worlds.push({world:w,source_rows:rr.size,delta_sign_counts:delta,strict4_cohorts:strict4,net4_cohorts:net4,local,cohorts});
 }
 let get=w=>worlds.find(x=>x.world===w);
 if(get("ZERO_MAP").strict4_cohorts!==0||get("ZERO_MAP").net4_cohorts.shrink!==8)throw Error("zero map control");
 if(get("LOGISTIC_R3_CENTERED").local.net4_shrink!==4||get("LOGISTIC_R3_CENTERED").local.strict4!==0)throw Error("two-step control");
 for(let w of ["IDENTITY_NEUTRAL","SIGN_FLIP_NEUTRAL"])if(get(w).net4_cohorts.equal!==8)throw Error("neutral control");
 return {research_id:"R251_S47",source_rows:405,independent_cohorts:72,source_field_checks:checks,failed_checks:0,worlds};
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require==="function"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const file=process.argv[2]||path.join(__dirname,"..","R251","R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv");
 console.log(JSON.stringify(run(fs.readFileSync(file,"utf8")),null,2));
}