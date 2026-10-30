"use strict";
// MKT150 researcher-created weighted-score toy, NOT a reconstruction of Dcider's algorithm.
function check(x,m){if(!x)throw new Error(m)}
function weighted(v,a,b){
 if(!Array.isArray(v)||v.length!==2||!Number.isInteger(a)||!Number.isInteger(b)||
 a<0||b<0||a+b!==10||v.some(x=>!Number.isFinite(x)))throw new Error("invalid input");
 return a*v[0]+b*v[1]; // ten times the score
}
function run(){
 let checks=0;const ok=(x,m)=>{check(x,m);checks++};
 const A=[9,4],B=[6,8];
 ok(weighted(A,6,4)===70,"A baseline");
 ok(weighted(B,6,4)===68,"B baseline");
 ok(weighted(A,5,5)===65,"A equal");
 ok(weighted(B,5,5)===70,"B equal");
 ok(weighted(A,6,4)>weighted(B,6,4),"baseline rank");
 ok(weighted(A,5,5)<weighted(B,5,5),"equal rank");
 ok(weighted([9,8],6,4)===86,"rescaled A");
 ok(weighted([6,16],6,4)===100,"rescaled B");
 ok(weighted([9,8],6,4)<weighted([6,16],6,4),"scale rank flip");
 const grid=[];
 for(let w=0;w<=10;w++){
  const d=weighted(A,w,10-w)-weighted(B,w,10-w);
  ok(d===7*w-40,"exact delta "+w);
  grid.push({first_weight:w/10,difference:d/10});
 }
 const worlds=[{A:1,B:0},{A:1,B:1}];
 ok(worlds.every(w=>w.A===1),"same observed outcome");
 ok(worlds[0].A-worlds[0].B===1,"counterfactual world 1");
 ok(worlds[1].A-worlds[1].B===0,"counterfactual world 2");
 for(const v of [[A,6,5],[A,-1,11],[A,6.5,3.5],[[NaN,4],6,4]]){
  let rejected=false;try{weighted(...v)}catch(e){rejected=true}
  ok(rejected,"invalid input rejected");
 }
 return {checks,baseline:{A:7,B:6.8},equal_weights:{A:6.5,B:7},
  criterion_two_doubled:{A:8.6,B:10},threshold:"4/7",
  same_observed_chosen_outcome:1,counterfactual_effects:[1,0],
  weight_grid:grid,evidence:"INTERNAL_NONBLIND_ARTIFICIAL_E1"};
}
if(typeof module!=="undefined"&&module.exports)module.exports={run,weighted};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
