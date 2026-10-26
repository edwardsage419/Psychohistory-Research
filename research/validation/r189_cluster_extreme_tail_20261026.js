"use strict";
// R189 postacceptance artificial extreme group count probabilities, exact BigInt fractions.
// node research/validation/r189_cluster_extreme_tail_20261026.js
function calculate(original){
 const abs=x=>x<0n?-x:x;
 function gcd(a,b){a=abs(a);b=abs(b);while(b){let z=a%b;a=b;b=z;}return a||1n;}
 function R(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
 const add=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>add(a,[-b[0],b[1]]),mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
 const parse=s=>{const p=String(s).split("/");return R(p[0],p[1]||1);};
 const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
 const pow=(a,n)=>R(a[0]**BigInt(n),a[1]**BigInt(n));
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const one=R(1),zero=R(0);
 if(!original||!Array.isArray(original.all_worlds)||original.all_worlds.length!==24)throw Error("wrong original R189 source");
 let zeroCases=0,positiveCases=0,n2covChecks=0,minPositive=null,maxPositive=zero,maxCase=null;
 const cases=[];
 for(let wi=0;wi<24;wi++){
  const w=original.all_worlds[wi],n=w.n_per_cluster,h=w.source_latent_odds_multiplier_h;
  if(![2,4].includes(n)||![1,3].includes(h))throw Error("unexpected frozen world");
  for(let x=0;x<2;x++){
   const pmf=w["true_cluster"+x+"_count_PMF"].map(parse);
   if(pmf.length!==n+1)throw Error("bad PMF");
   const mu=parse(w["true_single_event_marginal_p"+x]);
   const true0=pmf[0],truen=pmf[n],ind0=pow(sub(one,mu),n),indn=pow(mu,n);
   const d0=sub(true0,ind0),dn=sub(truen,indn),tail=add(d0,dn);
   if(d0[0]<0n||dn[0]<0n)throw Error("Jensen violated");
   if(h===1){if(!eq(d0,zero)||!eq(dn,zero))throw Error("h=1 negative control");zeroCases++;}
   else {if(d0[0]<=0n||dn[0]<=0n)throw Error("h=3 strict tail missing");positiveCases++;}
   if(n===2){const cov=parse(w["true_same_cluster_event_cov_x"+x]);if(!eq(tail,mul(R(2),cov)))throw Error("n2 covariance identity");n2covChecks++;}
   if(tail[0]>0n){
    if(minPositive===null||tail[0]*minPositive[1]<minPositive[0]*tail[1])minPositive=tail;
    if(tail[0]*maxPositive[1]>maxPositive[0]*tail[1]){maxPositive=tail;maxCase={world:wi,x,n,o:w.source_base_odds_o,t:w.source_conditional_odds_multiplier_t,h};}
   }
   cases.push({world:wi,x,n,o:w.source_base_odds_o,t:w.source_conditional_odds_multiplier_t,h,mu:fmt(mu),true_zero:fmt(true0),independent_zero:fmt(ind0),zero_excess:fmt(d0),true_all_success:fmt(truen),independent_all_success:fmt(indn),all_success_excess:fmt(dn),total_extreme_excess:fmt(tail)});
  }
 }
 if(cases.length!==48||zeroCases!==24||positiveCases!==24||n2covChecks!==24)throw Error("wrong counts");
 return {research_id:"R189",source_blob:"29180ee83570e4faef528b85d8d4daaada368344",evidence:"E1_ARTIFICIAL_ONLY",worlds:24,condition_cases:48,h1_zero_cases:zeroCases,h3_strict_positive_cases:positiveCases,n2_covariance_identities:n2covChecks,min_strict_positive_extreme_excess:fmt(minPositive),max_extreme_excess:fmt(maxPositive),max_case:maxCase,cases};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
 const original=JSON.parse(fs.readFileSync(path.join(root,"research/R189/R189_EXACT_RESULTS.json"),"utf8"));
 process.stdout.write(JSON.stringify(calculate(original),null,2)+"\n");
}
