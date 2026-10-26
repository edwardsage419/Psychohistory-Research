// R202 third method: fixed four independent future horizons, exact Brier.
// Run: node research/validation/r202_horizon_transport_20261027.js research/R202/R202_ALL_96_ORIGINAL_CENSORED_TRAINING_WORLDS.csv
"use strict";
const scales=["1/2","1","2"], horizons=[1,3,5,9],base=[1,2,4,8];
function gcd(a,b){while(b){let c=a%b;a=b;b=c;}return a;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(!b)throw Error("zero");let g=gcd(a<0n?-a:a,b);return [a/g,b/g];}
function P(s){let a=s.split("/");return F(a[0],a[1]||1);}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return add(a,F(-b[0],b[1]));}
function fmt(a){return a[0]+"/"+a[1];}
const Z=F(0),O=F(1);
function prob(a,H){let x=P(a);return F(base.filter(t=>BigInt(t)*x[0]<=BigInt(H)*x[1]).length,4);}
function directBrier(truth,pred,H){let p=prob(truth,H),q=prob(pred,H),sq1=mul(sub(O,q),sub(O,q)),sq0=mul(q,q);return add(mul(p,sq1),mul(sub(O,p),sq0));}
function parseCSV(s){let lines=s.trim().split(/\r?\n/),header=lines.shift().split(",");return lines.map(line=>Object.fromEntries(line.split(",").map((x,i)=>[header[i],x])));}
function run(csv){let data=parseCSV(csv);if(data.length!==96)throw Error("source row count");let rows=[],worlds=[];
for(let a of scales)for(let C of [2,4]){let items=data.filter(r=>r.true_time_scale_a===a&&Number(r.administrative_censor_time)===C);if(items.length!==16)throw Error("source count");
for(let H of horizons){let total=Z,oracle=directBrier(a,a,H),nullRisk=directBrier(a,"1",H),mass=Z,selected={};for(let r of items){let w=P(r.original_training_source_probability),fit=r.selected_a;if(!scales.includes(fit))throw Error("fit");let risk=directBrier(a,fit,H);total=add(total,mul(w,risk));mass=add(mass,w);selected[fit]=add(selected[fit]||Z,w);rows.push({true_a:a,C,H,source_x0_T0:r.original_x0_baseline_T0,source_x1_T0:r.original_x1_baseline_T0,source_weight:fmt(w),fitted_a:fit,p:fmt(prob(a,H)),q:fmt(prob(fit,H)),expected_brier:fmt(risk)});}
if(fmt(mass)!=="1/1")throw Error("normalization");worlds.push({true_a:a,C,H,training_records:items.length,source_mass:fmt(mass),selected_a_mass:Object.fromEntries(Object.entries(selected).map(([k,v])=>[k,fmt(v)])),selected_brier:fmt(total),null_brier:fmt(nullRisk),oracle_brier:fmt(oracle),oracle_gap:fmt(sub(total,oracle)),selected_minus_null:fmt(sub(total,nullRisk))});}}
if(rows.length!==384||worlds.length!==24)throw Error("result counts");
let original={"1/2:2":"9/32","1/2:4":"15/64","1:2":"9/32","1:4":"17/64","2:2":"13/64","2:4":"7/32"};for(let w of worlds.filter(w=>w.H===3))if(w.selected_brier!==original[w.true_a+":"+w.C])throw Error("R202 original H3 mismatch");
return {research_id:"R202",date:"2026-10-27",status:"INTERNAL_BOUNDED_E1_POSTSCORE_ADDENDUM",horizons,original_training_rows:data.length,scored_cases:rows.length,world_count:worlds.length,worlds,rows};}
if(typeof require!=="undefined"&&require.main===module){let fs=require("node:fs");console.log(JSON.stringify(run(fs.readFileSync(process.argv[2],"utf8")),null,2));}
if(typeof module!=="undefined")module.exports={run};
