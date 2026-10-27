"use strict";
/* B R216 S12 v2: actual injected-coefficient and threshold mutation execution. */
const C=[
 [-1,1,0,0,0,0,0,0,1,-1,0,0],
 [0,0,0,0,0,-1,1,0,0,1,-1,0],
 [0,-1,0,1,0,0,0,0,0,1,0,-1],
 [0,0,0,0,0,0,-1,1,0,0,1,-1],
 [0,-1,0,1,0,1,0,-1,0,0,0,0]
];
const MU_VALID_CONSTANT=[1,2,5,6,-1,0,1,4,0,1,2,3];
function dp(coef){
 let m=new Map([["0,0,0,0,0",1]]);
 for(let j=0;j<12;j++){
  let n=new Map();
  for(const [k,count] of m){
   let v=k.split(",").map(Number);
   for(let s of [-1,1]){
    let a=v.map((x,i)=>x+s*coef[i][j]),q=a.join(",");
    n.set(q,(n.get(q)||0)+count);
   }
  }m=n;
 }return m;
}
function aggregate(coef,threshold){
 const m=dp(coef),shifts=coef.map(c=>c.reduce((s,x,i)=>s+x*MU_VALID_CONSTANT[i],0));
 let n=0,sum=0;
 for(const [key,count] of m){
  const z=key.split(",").map((v,i)=>Number(v)+shifts[i]);
  if(threshold!=="ALL"&&Math.max(Math.abs(z[0]),Math.abs(z[1]))>threshold)continue;
  n+=count;sum+=count*z[2];
 }
 return {accepted:n,mean_E_k1:n?sum/n:null,unique_joint_states:m.size};
}
function run(){
 const original=aggregate(C,"ALL");
 const mutated=C.map(x=>x.slice());mutated[2][3]=-1;
 const changed=aggregate(mutated,"ALL");
 const strict=aggregate(C,1),relaxed=aggregate(C,2);
 if(original.accepted!==4096||original.mean_E_k1!==2)throw Error("original anchor");
 if(changed.mean_E_k1===original.mean_E_k1)throw Error("weight mutation not detected");
 if(strict.accepted===relaxed.accepted)throw Error("threshold mutation not detected");
 return {schema:"b_r216_s12_mutation_execution_v2",original,coefficient_mutation:{index:"E3",estimator:"E_k1_clean",from:1,to:-1,actual_mutated_DP:changed,detected:changed.mean_E_k1!==original.mean_E_k1},threshold_mutation:{from:1,to:2,strict,relaxed,detected:strict.accepted!==relaxed.accepted},source_type:"E1_ARTIFICIAL"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
