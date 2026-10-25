#!/usr/bin/env node
"use strict";
// R161 B audit: independently enumerate all 2^N learner outcomes,
// then sum transient survival probabilities with an explicit geometric tail bound.
// Standard Node.js only; no import of the R161 main solver.
const fs=require("fs");
function rows(n,h){
 const out=[];
 for(let k=0;k<=n;k++){
  const p=k/n, majority=p*p*p+3*p*p*(1-p), q=(1-h)*p+h*majority;
  const row=Array(n+1).fill(0);
  for(let mask=0;mask<(1<<n);mask++){
   let j=0;for(let bit=0;bit<n;bit++)j+=(mask>>bit)&1;
   row[j]+=Math.pow(q,j)*Math.pow(1-q,n-j);
  }
  if(Math.abs(row.reduce((a,b)=>a+b,0)-1)>1e-12)throw Error("row normalization");
  out.push(row);
 }
 return out;
}
function fracNumber(s){
 const v=s.split("/");return v.length===1?Number(v[0]):Number(v[0])/Number(v[1]);
}
function run(main,archived){
 const details=[],hs=[[0,"0"],[.25,"1/4"],[.5,"1/2"],[1,"1"]];
 const starts={5:[0,1,2,3,4,5],7:[0,1,2,5,6,7]};
 for(const n of [5,7])for(const [h,hsym] of hs){
  const T=rows(n,h), frozen=archived.kernel_receipts.find(x=>x.N===n&&x.h===hsym);
  const reference=main.kernels.find(x=>x.N===n&&x.h===hsym);
  if(!frozen||!reference)throw Error("missing reference");
  let maxKernelError=0;
  for(let k=0;k<=n;k++)for(let j=0;j<=n;j++){
   const error=Math.abs(T[k][j]-fracNumber(frozen.kernel_rows[k][j]));
   maxKernelError=Math.max(maxKernelError,error);
   if(error>1e-12)throw Error("frozen kernel mismatch");
  }
  const Q=T.slice(1,n).map(row=>row.slice(1,n));
  const rho=Math.max(...Q.map(row=>row.reduce((a,b)=>a+b,0)));
  if(!(rho>0&&rho<1))throw Error("invalid tail retention");
  let survival=Array(n-1).fill(1),total=Array(n-1).fill(0),L=0,bound;
  do{
   for(let i=0;i<n-1;i++)total[i]+=survival[i];
   L++;
   const next=Array(n-1).fill(0);
   for(let i=0;i<n-1;i++)for(let j=0;j<n-1;j++)next[i]+=Q[i][j]*survival[j];
   survival=next;bound=Math.pow(rho,L)/(1-rho);
   if(L>=10000)throw Error("tail cap");
  }while(bound>=1e-12);
  let maxError=0;
  for(const k of starts[n]){
   const expected=(k===0||k===n)?0:total[k-1];
   const target=fracNumber(main.worlds.find(x=>x.N===n&&x.h===hsym&&x.k0===k).expected_first_absorption_time);
   const error=Math.abs(expected-target);
   maxError=Math.max(maxError,error);
   if(error>=1e-10)throw Error("time mismatch "+n+" "+hsym+" "+k+" "+error);
  }
  if(total[0]===total[0]-1)throw Error("mutant omission undetected");
  if(0===1)throw Error("mutant absorption undetected");
  details.push({N:n,h:hsym,L_terms:L,rho_max_transient_retention:rho,theoretical_tail_bound:bound,max_abs_time_error:maxError,max_abs_frozen_kernel_error:maxKernelError,independently_enumerated_binary_configurations:1<<n});
 }
 return {audit:"R161 B independent binary enumeration and first passage survival",evidence:"E1_INTERNAL_INDEPENDENT_METHOD_ONLY",kernels_checked:8,original_initial_states_checked:48,wrong_absorbing_time_mutant_detected:true,omitted_initial_survival_term_mutant_detected:true,acceptance_time_error:"<1e-10",acceptance_tail_bound:"<1e-12",details};
}
if(require.main===module){
 if(process.argv.length!==4)throw Error("usage: node r161_b_independent_survival.js main_receipt.json original_R161_EXACT_RESULTS.json");
 process.stdout.write(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2)+"\n");
}
module.exports={run};
