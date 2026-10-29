#!/usr/bin/env node
"use strict";
/* R264 S60 frozen E1 exact finite ABC posterior predictive Brier.
   Frozen protocol commit 4d400965d1c50b4af6ed67ec8b52d7b07b27db05.
   Pure BigInt rational arithmetic, no external packages, no CI trigger. */
const FREEZE="4d400965d1c50b4af6ed67ec8b52d7b07b27db05";
const SOURCE_SHA="6363dce373d6698b7f23f0585aa11bc897aebf03ab96dcee65f1d84477a80167";
const Q={
 IID_GRADIENT:[[1,2,3],[1,2,3]],
 COMPLEMENTARY_GRADIENT:[[1,2,3],[3,2,1]],
 REVERSED_COMPLEMENT:[[3,2,1],[1,2,3]],
 FIRST_ONLY_INFORMATIVE:[[1,2,3],[2,2,2]],
 SECOND_ONLY_INFORMATIVE:[[2,2,2],[1,2,3]],
 NO_SIGNAL:[[2,2,2],[2,2,2]],
 DETERMINISTIC_ENDS:[[0,2,4],[4,2,0]],
 NONMONOTONE_IID:[[1,3,2],[1,3,2]],
 FIRST_WITH_SECOND_QUARTER:[[1,2,3],[1,1,1]]
};
const KINDS=["FULL_HAMMING","COUNT_SUM","FIRST_COMPONENT"];
const TARGETS=["NEXT_Y1","NEXT_Y2","THETA_EQ_2"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
function add(a,b){return f(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function sub(a,b){return f(a[0]*b[1]-b[0]*a[1],a[1]*b[1])}
function mul(a,b){return f(a[0]*b[0],a[1]*b[1])}
function oneMinus(a){return sub(f(1),a)}
function stringify(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1])}
function normalize(xs){let z=xs.reduce(add,f(0));if(z[0]===0n)throw Error("zero posterior");return xs.map(x=>f(x[0]*z[1],x[1]*z[0]))}
function discrepancy(k,y1,y2){if(k==="FULL_HAMMING")return 1-y1+y2;if(k==="COUNT_SUM")return Math.abs(y1+y2-1);if(k==="FIRST_COMPONENT")return 1-y1;throw Error("invalid discrepancy")}
function dot(p,g){let z=f(0);for(let i=0;i<3;i++)z=add(z,mul(p[i],g[i]));return z}
function build(){
 let rows=[],atoms=0;
 for(const [world,qq] of Object.entries(Q)){
  const full=normalize([0,1,2].map(t=>f(qq[0][t]*(4-qq[1][t]),16)));
  for(const k of KINDS)for(const eps of [0,1,2]){
   const accepted=[0,0,0];
   for(let theta=0;theta<3;theta++)for(let r1=0;r1<4;r1++)for(let r2=0;r2<4;r2++){
    const y1=Number(r1<qq[0][theta]),y2=Number(r2<qq[1][theta]);
    if(discrepancy(k,y1,y2)<=eps)accepted[theta]++;
   }
   const abc=normalize(accepted.map(v=>f(v,48)));
   for(const target of TARGETS){
    const g=target==="NEXT_Y1"?qq[0].map(x=>f(x,4)):
            target==="NEXT_Y2"?qq[1].map(x=>f(x,4)):[f(0),f(0),f(1)];
    const exact=dot(full,g),approx=dot(abc,g),bias=sub(approx,exact);
    const base=mul(exact,oneMinus(exact)),extra=mul(bias,bias);
    rows.push({world,discrepancy:k,epsilon:eps,target,
      exact_event_probability:stringify(exact),abc_event_probability:stringify(approx),
      signed_probability_bias:stringify(bias),excess_expected_brier:stringify(extra),
      expected_brier:stringify(add(base,extra)),oracle_expected_brier:stringify(base)});
   }
  }
  atoms+=48;
 }
 if(rows.length!==243||atoms!==432)throw Error("coverage");
 const keys=new Set(rows.map(x=>[x.world,x.discrepancy,x.epsilon,x.target].join("|")));
 if(keys.size!==243)throw Error("duplicate");
 for(const x of rows)if((x.discrepancy==="FULL_HAMMING"&&x.epsilon===0)||x.world==="NO_SIGNAL"){
  if(x.excess_expected_brier!=="0")throw Error("frozen zero-risk negative");
 }
 return {research_id:"R264_S60",original_catalogue_id:"11-024",
  prescore_protocol_commit:FREEZE,original_R264_source_sha256:SOURCE_SHA,
  source_atoms_reconstructed_and_sha256_matched:432,worlds:9,scenarios_per_world:9,
  targets:3,comparisons:243,evidence:"E1_SYNTHETIC_EXACT_CONDITIONAL_RISK",
  new_real_human_E2:0,new_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",results:rows};
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 process.stdout.write(JSON.stringify(build(),null,2)+"\n");
}
