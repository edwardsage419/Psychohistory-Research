"use strict";
const PAIRS=[["IID","LAG2_REPEAT"],["IID","LAG2_SWITCH"],["LAG2_SWITCH","LAG2_REPEAT"]];
const CHANNELS=["FULL","LAST_ADJACENT_PAIR","LAST_LAG2_PAIR"];
const LENGTHS=[3,4], MVALUES=[1,2,3,4];
function gcd(a,b){while(b){[a,b]=[b,a%b]}return a}
function frac(a,b){if(b<=0n)throw Error("bad denominator");let g=gcd(a,b);return String(a/g)+"/"+String(b/g)}
function sourceWeights(src,L,channel){
 const D=4**L, out=new Map();
 for(let mask=0;mask<2**L;mask++){
  const x=Array.from({length:L},(_,i)=>(mask>>(L-1-i))&1);
  let w;
  if(src==="IID")w=2**L;
  else if(src==="LAG2_REPEAT"||src==="LAG2_SWITCH"){
   const same=src==="LAG2_REPEAT"?3:1;
   w=4;for(let t=2;t<L;t++)w*=x[t]===x[t-2]?same:4-same;
  }else throw Error("source");
  const k=channel==="FULL"?x.join(""):channel==="LAST_ADJACENT_PAIR"?""+x[L-2]+x[L-1]:""+x[L-3]+x[L-1];
  out.set(k,(out.get(k)||0)+w);
 }
 if([...out.values()].reduce((a,b)=>a+b,0)!==D)throw Error("PMF normalization");
 return {D,weights:out};
}
function evaluate(srcA,srcB,L,m,channel){
 const a=sourceWeights(srcA,L,channel),b=sourceWeights(srcB,L,channel);
 const categories=[...new Set([...a.weights.keys(),...b.weights.keys()])].sort();
 let states=new Map([["1,1",{a:1n,b:1n,n:1n}]]);
 for(let t=0;t<m;t++){
  let next=new Map();
  for(const s of states.values())for(const key of categories){
   const x=s.a*BigInt(a.weights.get(key)||0),y=s.b*BigInt(b.weights.get(key)||0);
   const label=x+","+y;const old=next.get(label);
   if(old)old.n+=s.n;else next.set(label,{a:x,b:y,n:s.n});
  }
  states=next;
 }
 let abs=0n,totalA=0n,totalB=0n;
 for(const s of states.values()){abs+=s.n*(s.a>s.b?s.a-s.b:s.b-s.a);totalA+=s.n*s.a;totalB+=s.n*s.b}
 const D=BigInt(a.D)**BigInt(m);
 if(totalA!==D||totalB!==D||abs>2n*D)throw Error("mass conservation");
 return {source_a:srcA,source_b:srcB,L,m,channel,TV:frac(abs,2n*D),bayes_error:frac(2n*D-abs,4n*D),aggregated_likelihood_states:states.size,category_count:categories.length,full_ordered_observations:categories.length**m,pmf_a:[...a.weights].sort(),pmf_b:[...b.weights].sort()};
}
function ratio(s){const [n,d]=s.split("/");return Number(n)/Number(d)}
function compute(){
 let rows=[];for(const [a,b] of PAIRS)for(const L of LENGTHS)for(const m of MVALUES)for(const channel of CHANNELS)rows.push(evaluate(a,b,L,m,channel));
 let checks=0;for(const [a,b] of PAIRS)for(const L of LENGTHS){
  for(const m of MVALUES){
   const get=c=>rows.find(x=>x.source_a===a&&x.source_b===b&&x.L===L&&x.m===m&&x.channel===c);
   const full=get("FULL"),adj=get("LAST_ADJACENT_PAIR"),lag=get("LAST_LAG2_PAIR");
   if(adj.TV!=="0/1"||ratio(full.TV)+1e-12<ratio(lag.TV)||ratio(full.TV)+1e-12<ratio(adj.TV))throw Error("coarsening invariant");checks++;
   if(L===3&&full.TV!==lag.TV)throw Error("L3 equality");if(L===3)checks++;
   if(m>1)for(const c of CHANNELS){const prev=rows.find(x=>x.source_a===a&&x.source_b===b&&x.L===L&&x.m===m-1&&x.channel===c);if(ratio(get(c).TV)+1e-12<ratio(prev.TV))throw Error("monotonicity");checks++;}
  }
 }
 const normal=evaluate("IID","LAG2_REPEAT",3,1,"FULL"),bad=evaluate("IID","IID",3,1,"FULL"),coarse=evaluate("IID","LAG2_REPEAT",3,1,"LAST_ADJACENT_PAIR");
 if(normal.TV==="0/1"||bad.TV!=="0/1"||coarse.TV!=="0/1")throw Error("negative control failed");
 return {protocol:"protocols/R194_LAST_PAIR_VS_LAG2_PAIR_FULL_TRAJECTORY_THIRD_METHOD_FREEZE_2026-10-27.md",source_model:"research/R194/r194_exact_binary_markov_order.py",source_blob_sha1:"d1a4e5c061add45b929dd9fe701b36b08231c67b",evidence:"E1_ARTIFICIAL_EXACT",worlds:72,checks,negative_controls_rejected:2,rows,new_E2:0,new_E3:0,external_replication:0};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(compute(),null,2));
