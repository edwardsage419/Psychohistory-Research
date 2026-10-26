// Reproducible expression: node -e 'console.log(JSON.stringify(require("./")))' is not supported; use node to eval source and print JSON.
// Exact finite Bernoulli enumeration; returns receipt object when evaluated.
(()=>{
"use strict";
const sources=["LOW","HIGH","MID","UP2","UP3","DOWN2","DOWN3","SPIKE2","SPIKE3"];
const changes=["UP2","UP3","DOWN2","DOWN3"];
function w(name,t){
 if(name==="LOW")return 1;
 if(name==="HIGH")return 3;
 if(name==="MID")return 2;
 if(name==="UP2")return t>=2?3:1;
 if(name==="UP3")return t>=3?3:1;
 if(name==="DOWN2")return t>=2?1:3;
 if(name==="DOWN3")return t>=3?1:3;
 if(name==="SPIKE2")return t===2?3:1;
 if(name==="SPIKE3")return t===3?3:1;
 throw Error("bad source");
}
function ratioPass(bits,t,name){
 let numerator=1;
 for(let i=0;i<t;i++){const q=w(name,i+1);numerator*=bits[i]===1?q:4-q;}
 return numerator>=4*(2**t);
}
function alarm(bits,t,mode){return (mode==="scan"?changes:["UP2"]).some(n=>ratioPass(bits,t,n));}
function gcd(a,b){while(b){const c=a%b;a=b;b=c;}return a;}
function frac(n,d){const g=gcd(n,d);return (n/g)+"/"+(d/g);}
const worlds=[];
let paths=0,identityChecks=0,strictEver=0,wrongTerminalOnly=0;
for(const T of [4,5]){
 const den=4**T;
 for(const source of sources){
  const modes={scan:{first:Array(T+1).fill(0),terminal:0,ever:0},single:{first:Array(T+1).fill(0),terminal:0,ever:0}};
  let mass=0;
  for(let i=0;i<2**T;i++){
   const bits=Array.from({length:T},(_,k)=>(i>>(T-1-k))&1);
   const weight=bits.reduce((p,b,k)=>p*(b?w(source,k+1):4-w(source,k+1)),1);
   mass+=weight;paths++;
   for(const mode of ["scan","single"]){
    const x=modes[mode];
    if(alarm(bits,T,mode))x.terminal+=weight;
    for(let t=3;t<=T;t++)if(alarm(bits,t,mode)){x.first[t]+=weight;x.ever+=weight;break;}
   }
  }
  if(mass!==den)throw Error("mass "+source+" "+T);
  const row={source,T,ordered_trajectories:2**T,source_mass_exact:"1/1",modes:{}};
  for(const mode of ["scan","single"]){
   const x=modes[mode],first={};let fsum=0;
   for(let t=3;t<=T;t++){first["t"+t]=frac(x.first[t],den);fsum+=x.first[t];}
   if(fsum!==x.ever||x.ever>den||x.ever<x.terminal)throw Error("decomposition");
   identityChecks+=3;
   if(x.ever>x.terminal){strictEver++;wrongTerminalOnly++;}
   row.modes[mode]={terminal:frac(x.terminal,den),ever:frac(x.ever,den),first_alarm:first,never:frac(den-x.ever,den),excess_ever_over_terminal:frac(x.ever-x.terminal,den)};
  }
  if(modes.scan.ever<modes.single.ever)throw Error("scan dominance");
  identityChecks++;
  worlds.push(row);
 }
}
const mid4=worlds.find(r=>r.source==="MID"&&r.T===4),mid5=worlds.find(r=>r.source==="MID"&&r.T===5);
if(mid4.modes.scan.terminal!=="1/4"||mid5.modes.scan.terminal!=="1/8"||mid4.modes.single.terminal!=="1/16"||mid5.modes.single.terminal!=="1/32")throw Error("old R200 terminal mismatch");
return {schema:"r200_sequential_prefix_third_method_v1",date:"2026-10-27",protocol:"protocols/R200_SEQUENTIAL_PREFIX_LOOKS_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",sources,T_values:[4,5],looks_start:3,threshold_LR:4,zero_source:"MID",modes:["scan","single"],worlds,checks:{worlds:worlds.length,weighted_ordered_paths:paths,exact_identities:identityChecks,old_terminal_anchors:4,strict_ever_over_terminal_world_modes:strictEver,terminal_only_misses_early_alarm_world_modes:wrongTerminalOnly},evidence:"E1_INTERNAL_ARTIFICIAL_ONLY"};
})()
