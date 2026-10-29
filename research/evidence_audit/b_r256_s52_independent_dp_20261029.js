"use strict";
// R256 S52 B route: independent conditional-U transition count DP.
// Run: node research/evidence_audit/b_r256_s52_independent_dp_20261029.js
const worlds=[
["IDLE_NO_ARRIVALS",0,0.5,"SERVICE_FIRST"],["FAST_SERVICE_HALF_ARRIVAL",0.5,1,"SERVICE_FIRST"],
["BALANCED_INDEPENDENT_HALF_HALF",0.5,0.5,"SERVICE_FIRST"],
["DEMAND_ALWAYS_HALF_SERVICE",1,0.5,"SERVICE_FIRST"],
["NO_SERVICE_HALF_ARRIVAL",0.5,0,"SERVICE_FIRST"],
["DEMAND_ALWAYS_NO_SERVICE",1,0,"SERVICE_FIRST"],
["ARRIVAL_FIRST_BALANCED_HALF_HALF",0.5,0.5,"ARRIVAL_FIRST"],
["SHARED_DEMAND_ENV_HALF_HALF",0.5,0.5,"SERVICE_FIRST"],
["STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS",0.5,0.5,"SERVICE_FIRST"]];
function simplify(n,d){let a=n,b=d;while(b){let r=a%b;a=b;b=r;}return [n/a,d/a];}
function plus(x,y){return simplify(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function fmt(z){return z[1]===1n?""+z[0]:""+z[0]+"/"+z[1];}
function transition(q,a,s,policy){
 // Independent closed algebraic update, never calls R route's procedural source.
 if(policy==="SERVICE_FIRST"){
  let remaining=Math.max(0,q-s);
  let loss=a===1&&remaining===2?1:0;
  return [remaining+Math.min(a,2-remaining),loss];
 }
 let loss=a===1&&q===2?1:0;
 return [Math.max(0,q+Math.min(a,2-q)-s),loss];
}
function dpWorld(w){
 const [name,pa,ps,order]=w;let final=[];
 for(let u=0;u<2;u++){
  let dp=new Map([["0||0",{q:0,h:"",y:0,n:1}]]);
  for(let t=1;t<=4;t++){
   const next=new Map();
   for(const z of dp.values())for(let rawA=0;rawA<2;rawA++)for(let rawS=0;rawS<2;rawS++){
    let a=name==="SHARED_DEMAND_ENV_HALF_HALF"?u:pa===0.5?rawA:pa;
    let s=ps===0.5?rawS:ps;
    const [q,loss]=transition(z.q,a,s,order);
    const h=t<4?z.h+q:z.h;const y=t===4?loss:0;
    const id=q+"|"+h+"|"+y;
    let item=next.get(id);
    if(item)item.n+=z.n;else next.set(id,{q,h,y,n:z.n});
   }
   dp=next;
  }
  final.push(...dp.values());
 }
 if(final.reduce((s,z)=>s+z.n,0)!==512)throw Error("DP source mass");
 const feat={};
 for(const f of ["F0","F1","F12","F123","F3"]){
  const groups=new Map();
  for(const z of final){
   const h=f==="F0"?"":f==="F1"?z.h[0]:f==="F12"?z.h.slice(0,2):f==="F123"?z.h:z.h[2];
   const g=groups.get(h)||{n:0,k:0};g.n+=z.n;g.k+=z.n*z.y;groups.set(h,g);
  }
  let risk=[0n,1n],mixed=0;
  for(const z of groups.values()){
   if(z.k>0&&z.k<z.n)mixed++;
   risk=plus(risk,simplify(BigInt(z.k*(z.n-z.k)),BigInt(512*z.n)));
  }
  feat[f]={risk:fmt(risk),groups:groups.size,mixed};
 }
 return {world:name,target:"reported_rejection_r4",event_count:final.reduce((s,z)=>s+z.n*z.y,0),features:feat};
}
function compute(){return {research_id:"R256_S52_B",worlds:worlds.map(dpWorld),method:"CONDITIONAL_U_INDEPENDENT_EVENT_KERNEL_DP"};}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(compute(),null,2));
