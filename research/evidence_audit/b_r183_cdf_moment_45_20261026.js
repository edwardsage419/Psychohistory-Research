"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denom");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
function parseQ(x){let a=String(x).split("/");return Q(a[0],a[1]||1)}
function plus(x,y){return Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
function minus(x,y){return Q(x[0]*y[1]-y[0]*x[1],x[1]*y[1])}
function times(x,y){return Q(x[0]*y[0],x[1]*y[1])}
function over(x,y){return Q(x[0]*y[1],x[1]*y[0])}
function sq(x){return times(x,x)}
function compare(x,y){let z=x[0]*y[1]-y[0]*x[1];return z<0n?-1:z>0n?1:0}
function str(x){return x[1]===1n?x[0].toString():x[0]+"/"+x[1]}
function dec(x){return Number(x[0])/Number(x[1])}
const ZERO=Q(0),ONE=Q(1),HALF=Q(1,2);
function audit(worlds,receipt){
 let results=[],signs=0,origBrier=0;
 for(let ix=0;ix<worlds.length;ix++){
  let w=worlds[ix],n=w.n_per_group,a=w.source_group0_full_count_PMF.map(parseQ),b=w.source_group1_full_count_PMF.map(parseQ);
  const sum=a.reduce(plus,ZERO),sumB=b.reduce(plus,ZERO);
  if(compare(sum,ONE)||compare(sumB,ONE))throw Error("audit normalization");
  let cdf=ZERO,pos=ZERO,tie=ZERO;
  for(let k=0;k<=n;k++){pos=plus(pos,times(b[k],cdf));tie=plus(tie,times(a[k],b[k]));cdf=plus(cdf,a[k]);}
  let neg=minus(minus(ONE,pos),tie);
  let p0=parseQ(w.true_p0),p1=parseQ(w.true_p1),delta=minus(p1,p0);
  const mom=arr=>{let m=ZERO,m2=ZERO;for(let k=0;k<arr.length;k++){m=plus(m,times(Q(k),arr[k]));m2=plus(m2,times(Q(k*k),arr[k]));}return {m,m2,v:minus(m2,sq(m))}};
  let A=mom(a),B=mom(b),m=minus(B.m,A.m),v=plus(A.v,B.v);
  const risk=s=>plus(over(v,Q(s*s)),sq(minus(over(m,Q(s)),delta)));
  const mseM=risk(n),mseH=risk(n+1);
  let r=receipt.rows[ix];
  for(const [key,value] of Object.entries({prob_positive_contrast:pos,prob_tied_contrast:tie,prob_negative_contrast:neg,contrast_mse_mle:mseM,contrast_mse_halfcount:mseH})){if(compare(parseQ(r[key]),value))throw Error("independent audit mismatch world "+ix+" "+key);}
  let brier=(s,half)=>{
   let risks=[];
   for(let j=0;j<2;j++){let p=j?p1:p0,T=j?B:A;let mPred=half?over(plus(T.m,HALF),Q(n+1)):over(T.m,Q(n));let m2Pred=half?over(plus(plus(T.m2,T.m),Q(1,4)),Q((n+1)*(n+1))):over(T.m2,Q(n*n));let risk=plus(p,minus(m2Pred,times(Q(2),times(p,mPred))));risks.push(risk);}
   return over(plus(risks[0],risks[1]),Q(2));
  };
  if(compare(brier(n,false),parseQ(w.expected_MLE_out_of_sample_Brier_exact)))throw Error("archived MLE Brier mismatch");
  if(compare(brier(n,true),parseQ(w.expected_halfcount_out_of_sample_Brier_exact)))throw Error("archived H Brier mismatch");
  origBrier+=2;
  results.push({world_index:ix+1,independent_cdf_and_moment_checks:"PASS",archived_Brier_pair:"PASS"});
  signs++;
 }
 return {status:"PASS_INTERNAL_INDEPENDENT_METHOD",worlds:signs,checked_probability_and_contrast_fields:signs*5,archived_Brier_fields_checked:origBrier,independent_method:"CDF prefix and two marginal moments; no ordered count-pair enumeration",external_reproduction:false,results};
}
if(require.main===module){const fs=require("fs");const src=JSON.parse(fs.readFileSync(process.argv[2]||"research/R183/R183_EXACT_RESULTS.json","utf8"));const receipt=JSON.parse(fs.readFileSync(process.argv[3]||"research/validation/R183_CONTRAST_DIRECTION_45_EXACT_RECEIPT_2026-10-26.json","utf8"));process.stdout.write(JSON.stringify(audit(src.worlds,receipt),null,2)+"\n");}
module.exports={audit};
