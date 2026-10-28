"use strict";
// R241 S37: exact rational finite differences on the immutable original 180-row E1 CSV.
// Usage: node research/validation/r241_s37_finite_difference_exact_20261028.js research/R241/R241_ALL_180_EXACT_ODE_IVP_TIME_SOURCES.csv
const WORLDS=[
 "DECAY_L1","DECAY_L2","DECAY_HIDDEN_DOUBLE_COORDINATE",
 "CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY","GROWTH_L1",
 "CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH","STATIONARY",
 "CONSTANT_RATE_PLUS1","DECAY_NONLINEAR_SENSOR"];
const INITIALS=["1/4","1/2","3/4","1"];
const TIMES=["0","1/8","1/4","3/8","1/2"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const z=a%b;a=b;b=z;}return a;}
function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};}
function f(s){if(typeof s==="object"&&s!==null&&"n" in s)return s;const m=String(s).trim().match(/^(-?\d+)(?:\/(\d+))?$/);if(!m)throw Error("invalid rational "+s);return q(m[1],m[2]||1);}
function add(a,b){a=f(a);b=f(b);return q(a.n*b.d+b.n*a.d,a.d*b.d);}
function sub(a,b){a=f(a);b=f(b);return q(a.n*b.d-b.n*a.d,a.d*b.d);}
function mul(a,b){a=f(a);b=f(b);return q(a.n*b.n,a.d*b.d);}
function div(a,b){a=f(a);b=f(b);return q(a.n*b.d,a.d*b.n);}
function cmp(a,b){a=f(a);b=f(b);const z=a.n*b.d-b.n*a.d;return z<0n?-1:z>0n?1:0;}
function abs(a){a=f(a);return q(a.n<0n?-a.n:a.n,a.d);}
function str(a){a=f(a);return a.d===1n?String(a.n):a.n+"/"+a.d;}
function sign(a){return cmp(a,0);}
function insist(ok,msg){if(!ok)throw Error(msg);}
function analyze(csv){
 const lines=csv.trimEnd().split(/\r?\n/),header=lines.shift().split(",");
 const expected=["world","observed_cohort_x0","observed_time","observed_y","observed_y_time_derivative","observed_y_sensitivity_to_initial_x0","oracle_hidden_initial_h0","oracle_hidden_h","oracle_state_ODE_rhs","oracle_hidden_dhdt","oracle_hidden_change_from_initial","original_source_probability"];
 insist(header.join("|")===expected.join("|"),"source header mismatch");
 insist(lines.length===180,"source count changed "+lines.length);
 const map=new Map(),perWorld=new Map();
 for(const line of lines){
  const parts=line.split(",");insist(parts.length===header.length,"source field count mismatch");
  const row=Object.fromEntries(header.map((h,i)=>[h,parts[i]]));
  const {world,observed_cohort_x0:x,observed_time:t}=row;
  insist(WORLDS.includes(world)&&INITIALS.includes(x)&&TIMES.includes(t),"unfrozen source identity");
  insist(str(f(row.original_source_probability))==="1/20","unfrozen probability");
  for(const field of ["observed_y","observed_y_time_derivative","observed_y_sensitivity_to_initial_x0"])f(row[field]);
  const key=[world,x,t].join("|");insist(!map.has(key),"duplicate original source");
  map.set(key,row);perWorld.set(world,(perWorld.get(world)||0)+1);
 }
 insist(map.size===180&&WORLDS.every(w=>perWorld.get(w)===20),"source coverage mismatch");
 const records=[],sums={};
 for(const w of WORLDS){
  sums[w]={};
  for(const x of INITIALS){
   const seq=TIMES.map(t=>map.get([w,x,t].join("|")));
   insist(seq.every(Boolean),"missing cohort-time source");
   function record(method,i,j,k){
    const a=seq[i],b=seq[j],ref=seq[k];
    const slope=div(sub(f(b.observed_y),f(a.observed_y)),sub(f(b.observed_time),f(a.observed_time)));
    const deriv=f(ref.observed_y_time_derivative),err=sub(slope,deriv),span=sub(f(b.observed_time),f(a.observed_time));
    const item={world:w,x,left_t:TIMES[i],right_t:TIMES[j],reference_t:TIMES[k],
     method,span:str(span),slope:str(slope),analytic_derivative:str(deriv),
     error:str(err),abs_error:str(abs(err)),sign_agrees:sign(slope)===sign(deriv)};
    insist(item.sign_agrees,"slope sign mismatch "+JSON.stringify(item));
    if(w==="STATIONARY"||w==="CONSTANT_RATE_PLUS1")insist(sign(err)===0,"affine exactness failed");
    else insist(sign(err)!==0,"nonaffine error unexpectedly zero");
    records.push(item);
   }
   for(let i=0;i<4;i++)record("FORWARD_1_8",i,i+1,i);
   for(let i=0;i<3;i++)record("FORWARD_1_4",i,i+2,i);
   for(let i=1;i<4;i++)record("CENTER_1_8",i-1,i+1,i);
  }
 }
 insist(records.length===360,"unexpected secant count");
 let strict=0,equal=0;
 for(const w of WORLDS)for(const x of INITIALS)for(let i=0;i<3;i++){
  const left=TIMES[i];
  const short=records.find(z=>z.world===w&&z.x===x&&z.left_t===left&&z.method==="FORWARD_1_8");
  const long=records.find(z=>z.world===w&&z.x===x&&z.left_t===left&&z.method==="FORWARD_1_4");
  const c=cmp(f(long.abs_error),f(short.abs_error));
  insist(c>=0,"forward longer step unexpectedly lower absolute error");
  if(w==="STATIONARY"||w==="CONSTANT_RATE_PLUS1"){insist(c===0,"affine span error changed");equal++;}
  else{insist(c>0,"nonlinear span error not strictly larger");strict++;}
 }
 insist(strict===84&&equal===24,"span pair census changed");
 function alias(a,b){
  const left=records.filter(z=>z.world===a),right=records.filter(z=>z.world===b);
  insist(left.length===40&&right.length===40,"alias record count");
  for(let i=0;i<40;i++)for(const field of ["x","left_t","right_t","reference_t","method","span","slope","analytic_derivative","error","abs_error"])
   insist(left[i][field]===right[i][field],"alias violated "+a+" "+b+" "+field);
 }
 alias("DECAY_L1","DECAY_HIDDEN_DOUBLE_COORDINATE");
 alias("DECAY_L1","CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY");
 alias("GROWTH_L1","CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH");
 const summary=[];
 for(const w of WORLDS){
  const z=records.filter(r=>r.world===w);
  const obj={world:w,total:40,exact_zero_error:z.filter(r=>r.error==="0").length,sign_agreement:z.filter(r=>r.sign_agrees).length};
  for(const m of ["FORWARD_1_8","FORWARD_1_4","CENTER_1_8"]){
   const s=z.filter(r=>r.method===m),v=s.map(r=>f(r.abs_error));
   obj[m]={n:s.length,mean_absolute_error:str(div(v.reduce(add,q(0)),q(v.length))),max_absolute_error:str(v.reduce((a,b)=>cmp(a,b)>0?a:b,q(0)))};
  }
  summary.push(obj);
 }
 const find=(w,x,t,m)=>records.find(r=>r.world===w&&r.x===x&&r.left_t===t&&r.method===m);
 insist(find("DECAY_L1","1","0","FORWARD_1_8").slope==="-8/9","decay anchor");
 insist(find("DECAY_L1","1","0","FORWARD_1_4").slope==="-4/5","decay long anchor");
 insist(find("GROWTH_L1","1","0","FORWARD_1_8").slope==="8/7","growth anchor");
 insist(find("GROWTH_L1","1","0","FORWARD_1_4").slope==="4/3","growth long anchor");
 const receipt={research_id:"R241",supplement:"S37",date:"2026-10-28",evidence:"E1_ARTIFICIAL",
  original_csv_blob_sha:"83ae446308789a88213a4a77d38a23dfcf14167b",
  prescore_protocol_commit:"eb3cb7dbfcaf090f0c0f879670ded4ab9848d32a",
  source_rows:180,worlds:9,cohorts:4,times:5,secant_records:360,
  forward_one_step:144,forward_two_step:108,centered:108,
  sign_agreement_count:360,exact_zero_error_count:80,nonzero_error_count:280,
  longer_step_strictly_larger_absolute_error_pairs:84,
  longer_step_equal_zero_error_pairs:24,alias_pairs_checked:3,
  summary,records,new_real_human_E2:0,new_real_historical_E3:0,
  R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 insist(records.filter(r=>r.error==="0").length===80,"zero error count mismatch");
 return receipt;
}
if(typeof require==="function"&&typeof process==="object"&&require.main===module){
 const fs=require("fs");const file=process.argv[2];
 if(!file)throw Error("pass original CSV path");
 process.stdout.write(JSON.stringify(analyze(fs.readFileSync(file,"utf8")),null,2)+"\n");
}
