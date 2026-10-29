#!/usr/bin/env node
"use strict";
// MKT127: synthetic unequal Bernoulli feedback audit, exact BigInt enumeration.
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a<0n?-a:a;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<=0n)throw Error("denominator");let g=gcd(a,b);return [a/g,b/g];}
function add(x,y){return F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function sub(x,y){return add(x,F(-y[0],y[1]));}
function mul(x,y){return F(x[0]*y[0],x[1]*y[1]);}
function div(x,y){if(y[0]===0n)throw Error("zero inclusion");let a=x[0]*y[1],b=x[1]*y[0];return b<0n?F(-a,-b):F(a,b);}
function eq(x,y){return x[0]===y[0]&&x[1]===y[1];}
function fmt(x){return x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);}
function ensure(x,s){if(!x)throw Error(s);}
function run(){
 const N=8,L=[1,1,16,16,1,16,16,16].map(x=>F(x,25));
 const pi=L.map((_,i)=>i<4?F(3,4):F(1,4));
 const ids=Array.from({length:N},(_,i)=>"synthetic-"+i);
 function valid(names,ps){ensure(names.length===N&&new Set(names).size===N,"source identity");ensure(ps.length===N&&ps.every(p=>p[0]>0n&&p[0]<=p[1]),"positive inclusion");}
 valid(ids,pi);
 let mass=F(0),mean=F(0),second=F(0),naive=F(0),empty=F(0),above=F(0),maximum=F(0);
 for(let mask=0;mask<256;mask++){
  let weight=F(1),estimate=F(0),raw=F(0),count=0;
  for(let i=0;i<N;i++){let selected=Boolean(mask&(1<<i));weight=mul(weight,selected?pi[i]:sub(F(1),pi[i]));if(selected){count++;estimate=add(estimate,div(L[i],pi[i]));raw=add(raw,L[i]);}}
  estimate=div(estimate,F(N));mass=add(mass,weight);mean=add(mean,mul(weight,estimate));second=add(second,mul(weight,mul(estimate,estimate)));
  naive=add(naive,mul(weight,div(raw,F(4))));
  if(count===0)empty=add(empty,weight);
  if(estimate[0]>estimate[1])above=add(above,weight);
  if(estimate[0]*maximum[1]>maximum[0]*estimate[1])maximum=estimate;
 }
 const target=div(L.reduce(add,F(0)),F(N)),variance=sub(second,mul(mean,mean));
 const analytic=div(L.reduce((s,l,i)=>add(s,mul(div(sub(F(1),pi[i]),pi[i]),mul(l,l))),F(0)),F(N*N));
 const tests=[
 [mass,F(1)],[target,F(83,200)],[mean,target],[variance,F(1487,24000)],[variance,analytic],
 [naive,F(151,400)],[sub(naive,target),F(-3,80)],[empty,F(81,65536)],
 [above,F(15,1024)],[maximum,F(181,150)]
 ];
 for(const [x,y] of tests)ensure(eq(x,y),"exact invariant "+fmt(x)+" != "+fmt(y));
 let negatives=0;
 for(const [names,ps] of [[["x","x","2","3","4","5","6","7"],pi],[ids,[F(0),...pi.slice(1)]]]){try{valid(names,ps);}catch(e){negatives++;}}
 ensure(negatives===2,"negative controls");
 ensure(!eq(F(16,25),F(1,25)),"counterfactual distinction");
 return {status:"PASS",synthetic_population:8,inclusion_patterns:256,assertions:14,
  target_risk:fmt(target),HT_expectation:fmt(mean),HT_variance:fmt(variance),
  naive_expected_count_estimate:fmt(naive),naive_bias:fmt(sub(naive,target)),
  no_label_probability:fmt(empty),HT_above_one_probability:fmt(above),
  maximum_HT:fmt(maximum),unobserved_B_risk_world_A:"16/25",unobserved_B_risk_world_B:"1/25",
  negative_controls_rejected:negatives,evidence:"E1_SYNTHETIC_ONLY"};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
if(typeof module!=="undefined")module.exports={run};
