// Independent absorbing-prefix probability DP; run with node. No packages.
console.log(JSON.stringify((()=>{
"use strict";
const sources=["LOW","HIGH","MID","UP2","UP3","DOWN2","DOWN3","SPIKE2","SPIKE3"];
const alt=["UP2","UP3","DOWN2","DOWN3"];
function prob4(s,t){
 switch(s){
 case "LOW":return 1;case "HIGH":return 3;case "MID":return 2;
 case "UP2":return t>=2?3:1;case "UP3":return t>=3?3:1;
 case "DOWN2":return t>=2?1:3;case "DOWN3":return t>=3?1:3;
 case "SPIKE2":return t===2?3:1;case "SPIKE3":return t===3?3:1;
 default:throw Error("source");
 }
}
function hits(prefix,mode,threshold){
 if(prefix.length<3)return false;
 const candidates=mode==="scan"?alt:["UP2"];
 return candidates.some(s=>{
  let n=1;
  for(let i=0;i<prefix.length;i++){
   const p=prob4(s,i+1);n*=prefix[i]==="1"?p:4-p;
  }
  return n>=threshold*2**prefix.length;
 });
}
function gcd(a,b){while(b){[a,b]=[b,a%b]}return a;}
function f(n,d){const g=gcd(n,d);return n/g+"/"+d/g;}
function propagate(s,T,mode,threshold,stop){
 let states=new Map([["",1]]),first=Array(T+1).fill(0),terminal=0;
 for(let t=1;t<=T;t++){
  const next=new Map();
  for(const [prefix,mass] of states){
   for(const bit of ["0","1"]){
    const p=prob4(s,t),n=mass*(bit==="1"?p:4-p),child=prefix+bit,alert=hits(child,mode,threshold);
    if(stop&&alert){first[t]+=n*4**(T-t);continue;}
    if(t===T&&!stop&&alert)terminal+=n;
    next.set(child,(next.get(child)||0)+n);
   }
  }
  states=next;
 }
 const never=[...states.values()].reduce((a,b)=>a+b,0);
 return {first,never,terminal};
}
const rows=[];let negativeChecks=0,fullLeaves=0;
for(const T of [4,5])for(const source of sources){
 const row={source,T,modes:{}},den=4**T;
 for(const mode of ["scan","single"]){
  const absorbed=propagate(source,T,mode,4,true);
  const full=propagate(source,T,mode,4,false);
  fullLeaves+=2**T;
  const ever=absorbed.first.reduce((a,b)=>a+b,0);
  if(ever+absorbed.never!==den)throw Error("mass not conserved");
  const first={};for(let t=3;t<=T;t++)first["t"+t]=f(absorbed.first[t],den);
  row.modes[mode]={terminal:f(full.terminal,den),ever:f(ever,den),first_alarm:first,never:f(absorbed.never,den),excess_ever_over_terminal:f(ever-full.terminal,den)};
  if(propagate(source,T,mode,Number.POSITIVE_INFINITY,true).first.some(x=>x!==0))throw Error("infinite threshold");
  negativeChecks++;
 }
 rows.push(row);
}
const mid5=rows.find(x=>x.source==="MID"&&x.T===5);
if(mid5.modes.scan.ever!=="1/4"||mid5.modes.scan.terminal!=="1/8")throw Error("MID look boundary");
if(rows.find(x=>x.source==="UP2"&&x.T===5).modes.scan.ever===rows.find(x=>x.source==="SPIKE2"&&x.T===5).modes.scan.ever)throw Error("source swap undetected");
return {schema:"b_r200_prefix_absorbing_dp_v1",worlds:rows,checks:{worlds:rows.length,full_trajectory_leaves_scanned_in_terminal_dp:fullLeaves,infinite_threshold_zero_alarm_controls:negativeChecks,mid5_terminal_only_negative_control:1,UP2_to_SPIKE2_source_swap_negative_control:1}};
})(),null,2));
