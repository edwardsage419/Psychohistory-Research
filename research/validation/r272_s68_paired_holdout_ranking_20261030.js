// R272 S68: paired two-bit holdout ranking, exact arithmetic.
// E1 finite artificial source; frozen original R272 predictors, no third-party modules.
"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
const Z=F(0),O=F(1),H=F(1,2);
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>F(-a[0],a[1]);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
const pow=(a,k)=>F(a[0]**BigInt(k),a[1]**BigInt(k));
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const sign=a=>a[0]>0n?1:a[0]<0n?-1:0;
const fmt=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
const sum=a=>a.reduce(add,Z);
const binom=(n,k)=>{let x=1;for(let i=1;i<=k;i++)x=x*(n-i+1)/i;return x;};
const ps=[F(1,4),F(1,2),F(3,4)];
const pairs=[["TRAIN_MLE","LAPLACE_BETA11"],["TRAIN_MLE","CONSTANT_HALF"],["LAPLACE_BETA11","CONSTANT_HALF"]];
function forecast(m,k){if(m==="TRAIN_MLE")return F(k,4);if(m==="LAPLACE_BETA11")return F(k+1,6);if(m==="CONSTANT_HALF")return H;throw Error("bad model");}
function brier(y,q){return pow(sub(F(y),q),2);}
function diff(k,j,a,b){const qa=forecast(a,k),qb=forecast(b,k);const score=q=>div(add(mul(F(j),brier(1,q)),mul(F(2-j),brier(0,q))),F(2));return sub(score(qa),score(qb));}
function mass(p,n,k){return mul(pow(p,k),pow(sub(O,p),n-k));}
function tally(rows){const all=sum(rows.map(r=>r.mass));if(!eq(all,O))throw Error("mass not one");const mean=sum(rows.map(r=>mul(r.mass,r.d)));const second=sum(rows.map(r=>mul(r.mass,pow(r.d,2))));const variance=sub(second,pow(mean,2));const probs=[-1,0,1].map(s=>sum(rows.filter(r=>sign(r.d)===s).map(r=>r.mass)));const reversal=sum(rows.filter(r=>sign(r.d)!==0&&sign(r.d)!==sign(mean)).map(r=>r.mass));return [mean,second,variance,...probs,reversal];}
function routeR(p,a,b){const rows=[];for(let mask=0;mask<64;mask++){const bits=mask.toString(2).padStart(6,"0");const k=[...bits.slice(0,4)].filter(x=>x==="1").length;const j=[...bits.slice(4)].filter(x=>x==="1").length;const d=diff(k,j,a,b);rows.push({bits,k,j,d,mass:mass(p,6,k+j)});}return rows;}
function routeB(p,a,b){const rows=[];for(let k=0;k<=4;k++)for(let j=0;j<=2;j++){rows.push({k,j,d:diff(k,j,a,b),mass:mul(mul(F(binom(4,k)),mass(p,4,k)),mul(F(binom(2,j)),mass(p,2,j)))});}return rows;}
function compute(){
const results=[],source=[];
for(const p of ps)for(const [a,b] of pairs){
const r=routeR(p,a,b),s=routeB(p,a,b),x=tally(r),y=tally(s);
if(r.length!==64||s.length!==15||!x.every((v,i)=>eq(v,y[i])))throw Error("route mismatch "+fmt(p)+" "+a+"/"+b);
if(!eq(sum(x.slice(3,6)),O)||sign(x[2])<0)throw Error("invalid result");
const label=fmt(p)+":"+a+":"+b;
results.push({true_p:fmt(p),first:a,second:b,primitive_source_types:64,mean_difference:fmt(x[0]),second_moment:fmt(x[1]),variance:fmt(x[2]),prob_first_better:fmt(x[3]),prob_tie:fmt(x[4]),prob_first_worse:fmt(x[5]),prob_strict_wrong_population_ranking:fmt(x[6]),independent_binomial_route_agrees:true});
for(const z of r)source.push({true_p:fmt(p),first:a,second:b,original_six_bits:z.bits,train_successes:z.k,test_successes:z.j,first_forecast:fmt(forecast(a,z.k)),second_forecast:fmt(forecast(b,z.k)),paired_test_brier_difference:fmt(z.d),exact_source_mass:fmt(z.mass)});
}
// Negative controls: identical forecasts and reversed sign.
for(const p of ps){let self=tally(routeR(p,"TRAIN_MLE","TRAIN_MLE"));if(!eq(self[0],Z)||!eq(self[4],O))throw Error("identity control");}
let control=routeR(ps[0],...pairs[0]),old=tally(control);let flipped=tally(control.map(r=>({...r,d:neg(r.d)})));if(!eq(flipped[0],neg(old[0]))||eq(old[0],flipped[0]))throw Error("sign mutation not detected");
return {results,source,checks:{pairs:9,primitive_source_types_per_pair:64,comparison_labelled_source_rows:source.length,independent_binomial_cells_per_pair:15,exact_statistic_comparisons:63,route_agreement:true,identity_negative_control:true,sign_mutation_rejected:true,external_replication:false,E2:0,E3:0}};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){const r=compute();console.log(JSON.stringify({results:r.results,checks:r.checks},null,2));}
