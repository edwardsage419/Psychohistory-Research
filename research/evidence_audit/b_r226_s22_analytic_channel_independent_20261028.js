#!/usr/bin/env node
"use strict";
// Independent exact probability channel audit; reads frozen original results, not R S22 source code.
const fs=require("node:fs"),path=require("node:path");
function audit(original,receipt){
const fail=[],W=original.world_results,rows=receipt.rows;
const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b)[a,b]=[b,a%b];return a||1};
const f=(n,d=1)=>{if(!Number.isSafeInteger(n)||!Number.isSafeInteger(d)||d===0)throw Error("invalid fraction");if(d<0){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]};
const p=(s)=>{if(s===null)return null;let a=String(s).split("/").map(Number);return f(a[0],a[1]||1)};
const fmt=x=>x[1]===1?String(x[0]):x[0]+"/"+x[1];
const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>add(a,[-b[0],b[1]]);
const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
const eq=(a,b)=>a===null||b===null?a===b:a[0]===b[0]&&a[1]===b[1];
let fields=0,cell=0,normal=0,alias=0,gate=0;
const check=(v,s)=>{if(!v)fail.push(s)};
check(W.length===8&&rows.length===40,"identity");
const map=new Map(rows.map(r=>[r.world+"|"+r.p,r]));
check(map.size===40,"unique keys");
const randomized=new Set(["RANDOMIZED_PEER_COPY","RANDOMIZED_NO_COPY","RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK"]);
for(const orig of W){
for(let k=0;k<=4;k++){
const prob=f(k,8),r=map.get(orig.world+"|"+fmt(prob));
if(!r){fail.push("missing "+orig.world+"/"+k);continue}
const b=p(orig.observed_peer_difference_given_edge),d=p(orig.observed_discordance_probability_given_edge),trueEff=p(orig.oracle_true_connected_doA_peer_effect);
const expected={
connected_probability:p(orig.observed_edge_probability),
observed_discordance_given_edge:add(d,mul(prob,sub(f(1),mul(f(2),d)))),
observed_peer_contrast:mul(b,sub(f(1),mul(f(2),prob))),
true_connected_doA_effect:trueEff,
randomized_assignment_contrast:randomized.has(orig.world)?trueEff:null
};
for(const [field,x] of Object.entries(expected)){fields++;check(eq(p(r[field]),x),"field "+orig.world+"/"+k+"/"+field)}
gate++;check(randomized.has(orig.world)?r.randomized_assignment_contrast!==null:r.randomized_assignment_contrast===null,"assignment gate "+orig.world+"/"+k);
const expectedJoint=new Map();
for(const [key,value] of Object.entries(orig.observation_signature)){
const flip=key[0]+String(1-Number(key[1]))+key.slice(2);
expectedJoint.set(key,add(expectedJoint.get(key)||f(0),mul(p(value),sub(f(1),prob))));
expectedJoint.set(flip,add(expectedJoint.get(flip)||f(0),mul(p(value),prob)));
}
let sum=f(0);
for(let x=0;x<16;x++){
const key=x.toString(2).padStart(4,"0");
const exp=expectedJoint.get(key)||f(0);
const actual=p(r.observation_signature[key]||"0");
cell++;check(eq(actual,exp),"joint "+orig.world+"/"+k+"/"+key);
sum=add(sum,actual);
}
normal++;check(eq(sum,f(1)),"joint normalized "+orig.world+"/"+k);
}}
for(let k=0;k<=4;k++){
const pr=fmt(f(k,8));
for(const [x,y] of [["PEER_COPY","SHARED_LATENT_SHOCK"],["HOMOPHILY_ONLY","HOMOPHILY_WITH_COPY"]]){
const a=map.get(x+"|"+pr),b=map.get(y+"|"+pr);
alias++;check(a&&b&&JSON.stringify(a.observation_signature)===JSON.stringify(b.observation_signature),"alias "+x+"/"+y+"/"+pr);
}}
return {status:fail.length?"FAIL":"PASS",failures:fail,checks:{field_comparisons:fields,joint_cell_comparisons:cell,joint_normalizations:normal,alias_pair_checks:alias,randomization_gates:gate,total:fields+cell+normal+alias+gate},method:"independent exact rational convolution of frozen R226 observed distribution plus analytic attenuation; same-project algorithmic audit",external_independent_replications:0};
}
const ORIGINAL=path.join(__dirname,"..","R226","R226_EXACT_RESULTS.json");
const RECEIPT=path.join(__dirname,"..","validation","R226_S22_40_CONDITION_EXACT_RECEIPT_2026-10-28.json");
function main(){const original=JSON.parse(fs.readFileSync(ORIGINAL,"utf8")),receipt=JSON.parse(fs.readFileSync(RECEIPT,"utf8"));const pass=audit(original,receipt);const mutation=JSON.parse(JSON.stringify(receipt));mutation.rows[0].observed_peer_contrast="999";const negative=audit(original,mutation);if(pass.status!=="PASS"||negative.status!=="FAIL")throw Error(JSON.stringify({pass,negative}));process.stdout.write(JSON.stringify({pass,mutation_detected:negative.failures.length>0})+"\n");}
if(require.main===module)main();module.exports={audit};
