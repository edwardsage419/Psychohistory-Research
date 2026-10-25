#!/usr/bin/env node
"use strict";
// R161 predeclared negative controls: actually compute two altered algorithms.
// The two earlier boolean sentinel checks alone were weak; this addendum executes mutants.
const fs=require("fs");
function choose(n,k){let x=1;for(let j=1;j<=k;j++)x=x*(n-j+1)/j;return x;}
function run(exact){
 let missingTermDetections=0,absorbingDetections=0,baselinePasses=0;
 const details=[],starts={5:[0,1,2,3,4,5],7:[0,1,2,5,6,7]};
 for(const n of [5,7])for(const h of [0,.25,.5,1]){
  const hs=h===0?"0":h===.25?"1/4":h===.5?"1/2":"1";
  const Q=[];
  for(let k=1;k<n;k++){
   const p=k/n,c=p*p*p+3*p*p*(1-p),q=(1-h)*p+h*c;
   Q.push(Array.from({length:n-1},(_,j)=>choose(n,j+1)*Math.pow(q,j+1)*Math.pow(1-q,n-j-1)));
  }
  const rho=Math.max(...Q.map(row=>row.reduce((a,b)=>a+b,0)));
  let s=Array(n-1).fill(1),correct=Array(n-1).fill(0),mutant=Array(n-1).fill(0),L=0,bound;
  do{
   for(let i=0;i<n-1;i++){correct[i]+=s[i];if(L>0)mutant[i]+=s[i];}
   L++;
   const next=Array(n-1).fill(0);
   for(let i=0;i<n-1;i++)for(let j=0;j<n-1;j++)next[i]+=Q[i][j]*s[j];
   s=next;bound=Math.pow(rho,L)/(1-rho);
   if(L>=10000)throw Error("tail cap");
  }while(bound>=1e-12);
  for(const k of starts[n]){
   const z=exact.worlds.find(x=>x.N===n&&x.h===hs&&x.k0===k);
   const ab=z.expected_first_absorption_time.split("/");
   const target=ab.length===1?Number(ab[0]):Number(ab[0])/Number(ab[1]);
   if(k===0||k===n){
    const wrong=1;
    if(Math.abs(wrong-target)<=.9)throw Error("absorbing mutant undetected");
    absorbingDetections++;
   }else{
    const base=correct[k-1],wrong=mutant[k-1];
    if(Math.abs(base-target)>1e-10)throw Error("baseline failed");
    if(Math.abs(wrong-target)<.9)throw Error("omitted term mutant undetected");
    if(Math.abs((base-wrong)-1)>1e-12)throw Error("mutant not one term");
    baselinePasses++;missingTermDetections++;
   }
  }
  details.push({N:n,h:hs,survival_terms:L,certified_truncation_tail_bound:bound});
 }
 if(missingTermDetections!==32||absorbingDetections!==16||baselinePasses!==32)throw Error("control coverage");
 return {evidence:"E1_INTERNAL_MUTANT_AUDIT",kernels:8,baseline_transient_passes:baselinePasses,actual_omitted_first_survival_term_mutant_detections:missingTermDetections,actual_wrong_absorbing_time_one_mutant_detections:absorbingDetections,details};
}
if(require.main===module){
 if(process.argv.length!==3)throw Error("usage: node r161_b_mutant_controls.js exact_receipt.json");
 process.stdout.write(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2)+"\n");
}
module.exports={run};
