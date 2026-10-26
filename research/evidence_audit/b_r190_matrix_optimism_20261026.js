"use strict";
// Independent R190 matrix-only risk audit. No training-table CSV and no main algorithm.
// Usage: node b_r190_matrix_optimism_20261026.js matrices.json results.json main_receipt.json
function audit(matrixArchive,original,main){
 const abs=x=>x<0n?-x:x;
 function G(a,b){a=abs(a);b=abs(b);while(b){const r=a%b;a=b;b=r;}return a;}
 function Q(v){if(Array.isArray(v))return v;if(typeof v==="string"&&v.includes("/")){const [a,b]=v.split("/");return norm(BigInt(a),BigInt(b));}return norm(BigInt(v),1n);}
 function norm(a,b){if(b<0n){a=-a;b=-b;}if(!b)throw Error("zero denominator");const g=G(a,b);return [a/g,b/g];}
 const plus=(a,b)=>norm(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const minus=(a,b)=>norm(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const times=(a,b)=>norm(a[0]*b[0],a[1]*b[1]);
 const over=(a,b)=>norm(a[0]*b[1],a[1]*b[0]);
 const equal=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const stringify=a=>a[1]===1n?a[0].toString():a[0]+"/"+a[1];
 const zero=Q(0),one=Q(1),five=Q(5);
 const smap=new Map(matrixArchive.matrices.map(m=>[m.n+":"+m.lambda,m.exact_5x5_smoothing_matrix.map(row=>row.map(Q))]));
 if(smap.size!==8||original.worlds.length!==10||main.rows.length!==40)throw Error("archive dimensions");
 const mainmap=new Map(main.rows.map(r=>[r.source+":"+r.n_trials_per_x+":"+r.lambda,r]));
 let exactComparisons=0,negativeDetected=0,affineInvariant=0,allPositive=0;
 const details=[];
 for(const w of original.worlds){
  const n=w.n_trials_per_x,mu=w.source_true_conditional_means.map(Q),v=w.source_true_conditional_variances.map(Q);
  for(const lam of ["0","1","4","16"]){
   const S=smap.get(n+":"+lam),sourceKey=w.source+":"+n+":"+lam;
   const r=mainmap.get(sourceKey);if(!r)throw Error("missing main row "+sourceKey);
   let train=zero,future=zero,optimism=zero;
   for(let i=0;i<5;i++){
    let smu=zero;
    for(let j=0;j<5;j++)smu=plus(smu,times(S[i][j],mu[j]));
    const bias=minus(mu[i],smu);
    let trainVariance=zero,futureVariance=zero;
    for(let j=0;j<5;j++){
     const delta=Q(i===j?1:0),residual=minus(delta,S[i][j]);
     trainVariance=plus(trainVariance,times(times(residual,residual),over(v[j],Q(n))));
     futureVariance=plus(futureVariance,times(times(S[i][j],S[i][j]),over(v[j],Q(n))));
    }
    train=plus(train,plus(plus(times(bias,bias),times(minus(one,over(one,Q(n))),v[i])),trainVariance));
    future=plus(future,plus(plus(v[i],times(bias,bias)),futureVariance));
    optimism=plus(optimism,times(S[i][i],v[i]));
    // The original source has a fixed affine-invariant smoother; verify row sums.
    let rowSum=zero;for(let j=0;j<5;j++)rowSum=plus(rowSum,S[i][j]);
    if(!equal(rowSum,one))throw Error("constant trend lost");affineInvariant++;
   }
   train=over(train,five);future=over(future,five);
   optimism=times(over(Q(2),Q(5*n)),optimism);
   if(!equal(minus(future,train),optimism))throw Error("analytic optimism identity failed");
   if(!equal(train,Q(r.expected_training_MSE_exact)))throw Error("train mismatch "+sourceKey);
   if(!equal(future,Q(r.expected_independent_future_MSE_exact)))throw Error("future mismatch "+sourceKey);
   if(!equal(optimism,Q(r.optimism_gap_exact)))throw Error("optimism mismatch "+sourceKey);
   exactComparisons+=4;if(optimism[0]>0n)allPositive++;
   // Negative control: corrupt only one smoother diagonal in the optimism identity.
   const wrong=plus(optimism,times(over(Q(2),Q(5*n)),times(Q("1/100"),v[0])));
   if(!equal(wrong,minus(future,train)))negativeDetected++;
   details.push({source:w.source,n_trials_per_x:n,lambda:lam,train: stringify(train),future:stringify(future),optimism:stringify(optimism)});
  }
 }
 if(exactComparisons!==160||negativeDetected!==40||affineInvariant!==200||allPositive!==40)throw Error("incomplete independent checks");
 return {research_id:"R190",audit:"INDEPENDENT_MATRIX_ONLY_EXACT_BIAS_VARIANCE_AND_OPTIMISM",
  method:"matrix bias variance plus weighted diagonal covariance, no training CSV enumeration",
  worlds:10,world_lambda_rows:40,exact_identity_checks:exactComparisons,
  constant_row_sum_checks:affineInvariant,corrupted_diagonal_negative_controls_detected:negativeDetected,
  strictly_positive_optimism_cases:allPositive,exact_mismatches:0,
  evidence:"INTERNAL_E1_DIFFERENT_ALGORITHM",external_independent_replications:0,new_E2:0,new_E3:0,
  R073_unchanged:true,PESEN_v01_unchanged:true,details};
}
if(typeof module!=="undefined"&&module.exports)module.exports={audit};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==5){process.stderr.write("Usage: node script matrices.json results.json main_receipt.json\n");process.exit(2);}
 const result=audit(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,"utf8"))));
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
}