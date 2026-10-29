"use strict";
// R256 S52 R route. Run: node research/validation/r256_s52_rejection_prefix_20261029.js
const worlds=[
["IDLE_NO_ARRIVALS",0,1,"SERVICE_FIRST"],["FAST_SERVICE_HALF_ARRIVAL",0.5,1,"SERVICE_FIRST"],
["BALANCED_INDEPENDENT_HALF_HALF",0.5,0.5,"SERVICE_FIRST"],
["DEMAND_ALWAYS_HALF_SERVICE",1,0.5,"SERVICE_FIRST"],
["NO_SERVICE_HALF_ARRIVAL",0.5,0,"SERVICE_FIRST"],
["DEMAND_ALWAYS_NO_SERVICE",1,0,"SERVICE_FIRST"],
["ARRIVAL_FIRST_BALANCED_HALF_HALF",0.5,0.5,"ARRIVAL_FIRST"],
["SHARED_DEMAND_ENV_HALF_HALF",0.5,0.5,"SERVICE_FIRST"],
["STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS",0.5,0.5,"SERVICE_FIRST"]];
const features=["F0","F1","F12","F123","F3"];
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a;}
function add([a,b],[c,d]){let n=a*d+c*b,den=b*d,g=gcd(n,den);return [n/g,den/g];}
function fmt([a,b]){return b===1n?String(a):String(a)+"/"+String(b);}
function source(w,mask){
 const [name,pa,ps,order]=w;
 const bit=i=>(mask>>(8-i))&1;const u=bit(0);
 let q=0,history=[],reject=[],conservation=0;
 for(let t=0;t<4;t++){
  const a=name==="SHARED_DEMAND_ENV_HALF_HALF"?u:pa===0.5?bit(1+2*t):pa;
  const s=ps===0.5?bit(2+2*t):ps;let served,admitted,rejected,qn;
  if(order==="SERVICE_FIRST"){
   served=q>0&&s===1?1:0;
   admitted=a===1&&q-served<2?1:0;
   rejected=a-admitted;qn=q-served+admitted;
  }else{
   admitted=a===1&&q<2?1:0;rejected=a-admitted;
   served=q+admitted>0&&s===1?1:0;qn=q+admitted-served;
  }
  if(q+a!==qn+served+rejected||qn<0||qn>2)throw Error("flow conservation");
  conservation++;q=qn;history.push(q);reject.push(rejected);
 }
 return {history,y:reject[3],physical_y:name==="STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS"?0:reject[3],checks:conservation};
}
function key(h,f){if(f==="F0")return "";if(f==="F1")return String(h[0]);if(f==="F12")return h.slice(0,2).join("");if(f==="F123")return h.slice(0,3).join("");return String(h[2]);}
function score(rows,f){
 const groups=new Map();
 for(const r of rows){let k=key(r.history,f),z=groups.get(k)||[0,0];z[0]++;z[1]+=r.y;groups.set(k,z);}
 let risk=[0n,1n],mixed=0;
 for(const [n,k] of groups.values()){
  if(k>0&&k<n)mixed++;
  risk=add(risk,[BigInt(k*(n-k)),BigInt(512*n)]);
 }
 return {risk:fmt(risk),groups:groups.size,mixed};
}
function compute(){
 let result=[],checks=0,cache={};
 for(const w of worlds){
  let rows=[];for(let mask=0;mask<512;mask++){const r=source(w,mask);rows.push(r);checks+=r.checks;}
  cache[w[0]]=rows;
  const scores={};for(const f of features)scores[f]=score(rows,f);
  const count=rows.reduce((a,r)=>a+r.y,0);
  if(scores.F0.risk!==fmt([BigInt(count*(512-count))/gcd(BigInt(count*(512-count)),262144n),262144n/gcd(BigInt(count*(512-count)),262144n)]))throw Error("baseline risk");
  result.push({world:w[0],target:"reported_rejection_r4",event_count:count,features:scores});
 }
 for(let i=0;i<512;i++){
  const a=cache.BALANCED_INDEPENDENT_HALF_HALF[i],b=cache.STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS[i];
  if(a.y!==b.y||a.history.join("")!==b.history.join("")||b.physical_y!==0)throw Error("alias mismatch");
 }
 return {research_id:"R256_S52",freeze:"d078de426aa6c530419f234bd7c019465675d07b",evidence:"E1_ARTIFICIAL",worlds:result.length,source_atoms:4608,conservation_checks:checks,source_status:"RECONSTRUCTED_FROM_FROZEN_MECHANISMS_ORIGINAL_CSV_NOT_FULLY_REREAD",results:result,new_E2:0,new_E3:0,R073:"FROZEN",PESEN:"FROZEN"};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(compute(),null,2));
