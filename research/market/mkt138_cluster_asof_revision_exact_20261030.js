#!/usr/bin/env node
"use strict";
// MKT138: finite synthetic cluster-shared labels and historical as-of revisions.
const clusters=[["A1","A",1,1],["B1","B",2,3],["A2","A",3,3],["B2","B",4,1]];
const events=[["A1",2,0],["B1",3,1],["B1",7,0],["A2",9,1]];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a||1n;}
function rat(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return[a/g,b/g];}
function sub(x,y){return rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function cmp(x,y){const d=x[0]*y[1]-y[0]*x[1];return d<0n?-1:d>0n?1:0;}
function str(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1];}
function snapshot(cs,es,t){
  if(!Number.isInteger(t)||t<0)throw Error("cutoff");
  const ids=new Set(),last=new Map(),seen=new Map();
  for(const [id,g,n,p] of cs){if(ids.has(id)||!["A","B"].includes(g)||!Number.isSafeInteger(n)||n<1||!Number.isInteger(p)||p<0||p>4)throw Error("cluster");ids.add(id);}
  for(const [id,at,y] of es){
    if(!ids.has(id)||!Number.isInteger(at)||at<0||![0,1].includes(y)||(last.has(id)&&at<=last.get(id)))throw Error("event");
    last.set(id,at);if(at<=t)seen.set(id,y);
  }
  return seen;
}
function risk(cs,y,group=null){
  let num=0n,den=0n;
  for(const [id,g,n,p] of cs)if(group===null||g===group){const d=BigInt(p-4*y.get(id));num+=BigInt(n)*d*d;den+=16n*BigInt(n);}
  return rat(num,den);
}
function evaluate(t){
  const seen=snapshot(clusters,events,t),missing=clusters.filter(c=>!seen.has(c[0])),worlds=[];
  for(let mask=0;mask<2**missing.length;mask++){
    const y=new Map(seen);missing.forEach((c,i)=>y.set(c[0],(mask>>i)&1));
    let sum=0n;for(const [id,g,n,p] of clusters){const d=BigInt(p-4*y.get(id));sum+=d*d;}
    worlds.push({risk:risk(clusters,y),equal:rat(sum,64n),gap:sub(risk(clusters,y,"A"),risk(clusters,y,"B"))});
  }
  function bounds(key){let lo=worlds[0][key],hi=lo;for(const w of worlds){if(cmp(w[key],lo)<0)lo=w[key];if(cmp(w[key],hi)>0)hi=w[key];}return[str(lo),str(hi)];}
  return{cutoff:t,observed_clusters:seen.size,missing_clusters:missing.length,cluster_completions:worlds.length,
    row_independent_completions:2**missing.reduce((a,c)=>a+c[2],0),
    observed_only_brier:str(risk(clusters.filter(c=>seen.has(c[0])),seen)),
    population_brier_bounds:bounds("risk"),equal_cluster_brier_bounds:bounds("equal"),
    group_A_minus_B_brier_bounds:bounds("gap")};
}
function run(){
  const results=[4,8,10].map(evaluate),expected=[
    ["1/16","1/16,33/80","1/16,5/16","-1/3,3/8",4,128],
    ["19/48","13/80,41/80","3/16,7/16","-1/2,5/24",4,128],
    ["11/48","13/80,29/80","3/16,5/16","-1/2,-1/6",2,16]];
  let assertions=0,invalid_rejected=0;
  for(let i=0;i<3;i++){const r=results[i],actual=[r.observed_only_brier,r.population_brier_bounds.join(","),r.equal_cluster_brier_bounds.join(","),r.group_A_minus_B_brier_bounds.join(","),r.cluster_completions,r.row_independent_completions];
    for(let j=0;j<6;j++){if(actual[j]!==expected[i][j])throw Error("mismatch "+i+"/"+j+" "+actual[j]);assertions++;}}
  const bad=[
    ()=>snapshot([["A1","A",0,1],...clusters.slice(1)],events,4),
    ()=>snapshot([["A1","A",1,5],...clusters.slice(1)],events,4),
    ()=>snapshot(clusters,[...events,["UNKNOWN",10,1]],10),
    ()=>snapshot(clusters,[...events,["A1",11,2]],11),
    ()=>snapshot(clusters,[...events,["A2",9,0]],10),
    ()=>snapshot(clusters,events,-1)];
  for(const f of bad){let rejected=false;try{f();}catch(_){rejected=true;}if(!rejected)throw Error("invalid accepted");invalid_rejected++;}
  return{status:"PASS",assertions,invalid_rejected,results,scope:"artificial E1, no sampling probabilities or confidence levels"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
