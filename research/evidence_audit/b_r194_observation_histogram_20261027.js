"use strict";
// B audit: independently reconstruct path probabilities, enumerate unordered category histograms.
function gcf(a,b){while(b!==0n){let r=a%b;a=b;b=r}return a}
function format(n,d){const g=gcf(n,d);return (n/g).toString()+"/"+(d/g).toString()}
function factorial(n){let z=1n;for(let i=2;i<=n;i++)z*=BigInt(i);return z}
function enumerateCounts(k,m,callback){
 const vec=Array(k).fill(0);
 function step(j,remain){if(j===k-1){vec[j]=remain;callback(vec);return}for(let v=0;v<=remain;v++){vec[j]=v;step(j+1,remain-v)}}
 step(0,m);
}
function channelMass(source,L,channel){
 const denominator=BigInt(4**L);
 const counts=new Map();
 for(let n=0;n<(1<<L);n++){
  const bits=n.toString(2).padStart(L,"0").split("").map(Number);
  let numerator=1n,divisor;
  if(source==="IID"){divisor=BigInt(2**L)}
  else{
   divisor=4n;
   const q=source==="LAG2_REPEAT"?3n:source==="LAG2_SWITCH"?1n:null;
   if(q===null)throw Error("bad source");
   for(let j=2;j<L;j++){numerator*=bits[j]===bits[j-2]?q:4n-q;divisor*=4n}
  }
  if(denominator%divisor!==0n)throw Error("denominator scaling");
  const scaled=numerator*(denominator/divisor);
  let label;
  if(channel==="FULL")label=bits.join("");
  else if(channel==="LAST_ADJACENT_PAIR")label=bits.slice(L-2).join("");
  else if(channel==="LAST_LAG2_PAIR")label=""+bits[L-3]+bits[L-1];
  else throw Error("channel");
  counts.set(label,(counts.get(label)||0n)+scaled);
 }
 let total=0n;for(const v of counts.values())total+=v;
 if(total!==denominator)throw Error("B source normalization");
 return {counts,denominator};
}
function histogramRisk(a,b,L,m,channel){
 const P=channelMass(a,L,channel),Q=channelMass(b,L,channel);
 const keys=[...new Set([...P.counts.keys(),...Q.counts.keys()])].sort();
 const p=keys.map(k=>P.counts.get(k)||0n),q=keys.map(k=>Q.counts.get(k)||0n);
 const f=Array.from({length:m+1},(_,j)=>factorial(j));
 let diff=0n,sumP=0n,sumQ=0n,histograms=0;
 enumerateCounts(keys.length,m,(counts)=>{
  let multiplicity=f[m],massP=1n,massQ=1n;
  for(let i=0;i<keys.length;i++){multiplicity/=f[counts[i]];for(let j=0;j<counts[i];j++){massP*=p[i];massQ*=q[i]}}
  // factorial division must be exact; compute numerator first instead of progressive truncation.
  multiplicity=f[m];let den=1n;for(const c of counts)den*=f[c];multiplicity/=den;
  const aMass=massP*multiplicity,bMass=massQ*multiplicity;
  sumP+=aMass;sumQ+=bMass;diff+=aMass>bMass?aMass-bMass:bMass-aMass;histograms++;
 });
 const D=P.denominator**BigInt(m);
 if(sumP!==D||sumQ!==D)throw Error("B histogram mass");
 return {TV:format(diff,2n*D),bayes_error:format(2n*D-diff,4n*D),histograms,pmf_a:[...P.counts].map(([k,v])=>[k,Number(v)]).sort(),pmf_b:[...Q.counts].map(([k,v])=>[k,Number(v)]).sort()};
}
function audit(reference){
 if(reference.worlds!==72)throw Error("receipt worlds");
 let compared=0,histograms=0,probs=0;
 for(const row of reference.rows){
  const got=histogramRisk(row.source_a,row.source_b,row.L,row.m,row.channel);
  if(got.TV!==row.TV||got.bayes_error!==row.bayes_error)throw Error("B risk mismatch "+JSON.stringify(row));
  compared+=2;
  if(JSON.stringify(got.pmf_a)!==JSON.stringify(row.pmf_a)||JSON.stringify(got.pmf_b)!==JSON.stringify(row.pmf_b))throw Error("B source PMF mismatch");
  probs+=2;histograms+=got.histograms;
 }
 const real=histogramRisk("IID","LAG2_REPEAT",3,1,"FULL");
 const mutated=histogramRisk("IID","IID",3,1,"FULL");
 const coarsened=histogramRisk("IID","LAG2_REPEAT",3,1,"LAST_ADJACENT_PAIR");
 if(real.TV==="0/1"||mutated.TV!=="0/1"||coarsened.TV!=="0/1")throw Error("negative controls failed");
 return {status:"PASS_BOUNDED_INTERNAL_E1_DIFFERENT_ALGORITHM",worlds:reference.worlds,exact_risk_fields_compared:compared,exact_source_pmfs_compared:probs,histogram_configurations_examined:histograms,negative_controls_rejected:2,method:"independent path-probability numerator and unordered multinomial histogram risk",external_replication:0,new_E2:0,new_E3:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==3)throw Error("usage: node b_r194_histogram_audit.js R194_RECEIPT.json");
 console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));
}
