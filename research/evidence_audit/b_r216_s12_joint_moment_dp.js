"use strict";
/* B R216 S12: independent 12-coordinate joint-state DP.
 Does not import R's enumerator or its receipt. Run with node. */
const WORLD=["VALID_CONSTANT","VALID_HETEROGENEOUS","VALID_DYNAMIC","POST_EVENT_SHOCK_MIMIC","DIFFERENTIAL_PRETREND","LATE_ANTICIPATION"];
const H=[0,1,2,4,"ALL"];
const EST=["E_k1_clean","L_k0_clean","E_k1_BAD_L_ALREADY_TREATED"];
/* Original R216 group-time coefficient vectors in order E0..E3,L0..L3,N0..N3. */
const C=[
 [-1,1,0,0,0,0,0,0,1,-1,0,0],
 [0,0,0,0,0,-1,1,0,0,1,-1,0],
 [0,-1,0,1,0,0,0,0,0,1,0,-1],
 [0,0,0,0,0,0,-1,1,0,0,1,-1],
 [0,-1,0,1,0,1,0,-1,0,0,0,0]
];
const MU=[
 [1,2,5,6,-1,0,1,4,0,1,2,3],
 [1,2,4,5,-1,0,1,5,0,1,2,3],
 [1,2,5,8,-1,0,1,3,0,1,2,3],
 [1,2,5,8,-1,0,1,3,0,1,2,3],
 [1,3,5,7,-1,0,1,2,0,1,2,3],
 [1,2,4,6,-1,0,2,5,0,1,2,3]
];
const TARGET=[[2,2,2],[1,3,1],[4,1,4],[0,0,0],[0,0,0],[2,3,2]];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(b===0n)throw Error("zero");let d=gcd(a,b);return b/d===1n?String(a/d):String(a/d)+"/"+String(b/d);}
function dot(a,b){return a.reduce((s,x,i)=>s+x*b[i],0);}
function noiseDP(){
 let states=new Map([["0,0,0,0,0",1]]);
 for(let j=0;j<12;j++){
  const next=new Map();
  for(const [key,m] of states){
   const v=key.split(",").map(Number);
   for(const sign of [-1,1]){
    const w=v.map((x,k)=>x+sign*C[k][j]),q=w.join(",");
    next.set(q,(next.get(q)||0)+m);
   }
  }
  states=next;
 }
 const mass=[...states.values()].reduce((s,n)=>s+n,0);
 if(mass!==4096)throw Error("DP mass");
 return states;
}
function run(){
 const dp=noiseDP(),rows=[];let massChecks=0;
 for(let w=0;w<6;w++){
  const shifts=C.map(c=>dot(c,MU[w]));
  for(const h of H){
   let n=0n,pre=[0n,0n],sums=[0n,0n,0n],squares=[0n,0n,0n],losses=[0n,0n,0n];
   for(const [key,mult] of dp){
    const nv=key.split(",").map(Number),x=nv.map((v,i)=>v+shifts[i]);
    if(h!=="ALL"&&Math.max(Math.abs(x[0]),Math.abs(x[1]))>h)continue;
    const m=BigInt(mult);n+=m;
    for(let i=0;i<2;i++)pre[i]+=m*BigInt(x[i]);
    for(let i=0;i<3;i++){
     const val=BigInt(x[i+2]),t=BigInt(TARGET[w][i]);
     sums[i]+=m*val;squares[i]+=m*val*val;losses[i]+=m*(val-t)*(val-t);
    }
   }
   const row={world:WORLD[w],threshold:h,accepted:Number(n),source_count:4096,acceptance_probability:f(n,4096n),pre_E_mean:n?f(pre[0],n):null,pre_L_mean:n?f(pre[1],n):null,estimators:{}};
   for(let i=0;i<3;i++){
    row.estimators[EST[i]]=n?{target:TARGET[w][i],mean:f(sums[i],n),variance:f(squares[i]*n-sums[i]*sums[i],n*n),bias:f(sums[i]-n*BigInt(TARGET[w][i]),n),mse:f(losses[i],n)}:{target:TARGET[w][i],mean:null,variance:null,bias:null,mse:null};
   }
   rows.push(row);massChecks++;
  }
 }
 if(massChecks!==30)throw Error("coverage");
 return {schema:"b_r216_s12_joint_moment_dp_v1",unique_noise_joint_states:dp.size,source_mass:4096,rows};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
