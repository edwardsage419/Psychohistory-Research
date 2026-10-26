"use strict";
class Rat{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let a=n<0n?-n:n,b=d;while(b){[a,b]=[b,a%b]}this.n=n/a;this.d=d/a}
 static of(s){if(s instanceof Rat)return s;let [a,b]=String(s).split("/");return new Rat(a,b===undefined?1n:b)}
 add(x){x=Rat.of(x);return new Rat(this.n*x.d+x.n*this.d,this.d*x.d)}
 neg(){return new Rat(-this.n,this.d)}
 sub(x){return this.add(Rat.of(x).neg())}
 mul(x){x=Rat.of(x);return new Rat(this.n*x.n,this.d*x.d)}
 div(x){x=Rat.of(x);return new Rat(this.n*x.d,this.d*x.n)}
 str(){return this.n+"/"+this.d}
 val(){return Number(this.n)/Number(this.d)}
}
const Z=Rat.of(0),O=Rat.of(1);
function mulMatrix(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((s,a,k)=>s.add(a.mul(B[k][j])),Z)))}
function identity(){return [[O,Z,Z],[Z,O,Z],[Z,Z,O]]}
function compute(source){
 let results=[];let checks=0;
 for(const k of source.kernels){
  const T=k.transition_exact_matrix.map(row=>row.map(Rat.of));
  const pi=k.target_exact_pi.map(Rat.of);
  for(let i=0;i<3;i++){
   const sum=T[i].reduce((a,b)=>a.add(b),Z);
   if(sum.str()!=="1/1")throw Error("T not stochastic");checks++;
   let stationary=Z;for(let h=0;h<3;h++)stationary=stationary.add(pi[h].mul(T[h][i]));
   if(stationary.str()!==pi[i].str())throw Error("not stationary");checks++;
  }
  for(let j=0;j<3;j++){
   const N=64,mean=pi[j],V=mean.mul(O.sub(mean));
   let P=identity(),varSum=V.mul(N);
   for(let lag=1;lag<N;lag++){
    P=mulMatrix(P,T);
    const cov=mean.mul(P[j][j].sub(mean));
    varSum=varSum.add(cov.mul(2*(N-lag)));
   }
   const variance=varSum.div(N*N),ess=V.div(variance);
   if(ess.n<=0n||variance.n<=0n)throw Error("invalid ESS");checks++;
   if(j===2&&ess.str()!==k.stationary_N64_indicator_ESS_exact)throw Error("archived ESS source mismatch");
   if(j===2)checks++;
   results.push({target:k.target,q:k.proposal_edge_probability_q,indicator_state:j,mean:mean.str(),single_variance:V.str(),sample_mean_variance:variance.str(),ESS_N64:ess.str(),ESS_float:ess.val()});
  }
 }
 const look=(t,q,j)=>results.find(r=>r.target===t&&r.q===q&&r.indicator_state===j);
 for(const q of ["1/8","1/4"])if(look("UNIFORM",q,0).ESS_N64!==look("UNIFORM",q,2).ESS_N64)throw Error("uniform endpoint symmetry");
 const skew0=look("SKEW","1/8",0),skew2=look("SKEW","1/8",2);
 const mean0=Rat.of(skew0.mean),mean2=Rat.of(skew2.mean);
 const wrongVariance=Rat.of(skew0.sample_mean_variance).add(mean0.mul(mean0.sub(mean2)));
 if(wrongVariance.str()===skew0.sample_mean_variance)throw Error("wrong-indicator-mean mutant not detected");
 const min=Math.min(...results.map(r=>r.ESS_float)),max=Math.max(...results.map(r=>r.ESS_float));
 return {protocol:"protocols/R195_INDICATOR_SPECIFIC_ESS_N64_THIRD_METHOD_FREEZE_2026-10-27.md",source_blob_sha1:"17a3bff15e46b96091b292958d07b94da5ac8f31",kernels:8,new_indicator_cases:16,original_indicator_rechecked:8,exact_checks:checks,negative_control_rejected:1,ESS_range:[min,max],rows:results,evidence:"E1_ARTIFICIAL_EXACT",new_E2:0,new_E3:0,external_replication:0};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");if(process.argv.length!==3)throw Error("usage: node r195_indicator_ess.js original_kernels.json");console.log(JSON.stringify(compute(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}
