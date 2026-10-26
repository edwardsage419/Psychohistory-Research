"use strict";
// R190 third method: exact expected in-sample training loss and future risk.
// Usage: node r190_training_optimism_20261026.js training.csv matrices.json exact_results.json
// Standard Node.js only. No network or third-party dependencies.
function compute(csv,matrixArchive,archived){
 const abs=x=>x<0n?-x:x;
 function gcd(a,b){a=abs(a);b=abs(b);while(b){const t=a%b;a=b;b=t;}return a;}
 function F(a,b=1n){if(typeof a==="object"&&a!==null&&"n" in a)return a;
  if(typeof a==="string"){if(a.includes("/")){const p=a.split("/");return F(BigInt(p[0]),BigInt(p[1]));}return F(BigInt(a));}
  a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}
  const g=gcd(a,b);return {n:a/g,d:b/g};
 }
 const add=(a,b)=>F(a.n*b.d+b.n*a.d,a.d*b.d);
 const neg=a=>F(-a.n,a.d);
 const sub=(a,b)=>add(a,neg(b));
 const mul=(a,b)=>F(a.n*b.n,a.d*b.d);
 const div=(a,b)=>F(a.n*b.d,a.d*b.n);
 const sq=a=>mul(a,a);
 const eq=(a,b)=>a.n===b.n&&a.d===b.d;
 const show=a=>a.d===1n?a.n.toString():a.n+"/"+a.d;
 const z=()=>F(0),one=F(1),five=F(5);
 function parseLine(s){const out=[];let part="",quote=false;for(let i=0;i<s.length;i++){const c=s[i];if(c==='"'){quote=!quote;continue;}if(c===","&&!quote){out.push(part);part="";}else part+=c;}out.push(part);return out;}
 const lines=csv.trimEnd().split(/\r?\n/),headers=parseLine(lines.shift());
 if(lines.length!==1375||headers.length!==13)throw Error("source CSV shape mismatch "+lines.length+" "+headers.length);
 const lambdas=["0","1","4","16"],totals=new Map(),counts=new Map(),mass=new Map();
 let fits=0,trainingDominance=0;
 for(const line of lines){
  const a=parseLine(line);if(a.length!==13)throw Error("CSV column count "+a.length);
  const source=a[0],n=Number(a[1]),key=source+":"+n;
  const weight=F(a[3]),m=a[4].split(",").map(F);
  if(m.length!==5)throw Error("five positions expected");
  mass.set(key,add(mass.get(key)||z(),weight));
  counts.set(key,(counts.get(key)||0)+1);
  for(let j=0;j<4;j++){
   const lam=lambdas[j],f=a[5+j].split(",").map(F);
   if(f.length!==5)throw Error("five fitted positions expected");
   let training=z();
   for(let i=0;i<5;i++)training=add(training,add(sq(sub(m[i],f[i])),sub(one,sq(m[i]))));
   training=div(training,five);
   const future=F(a[9+j]);
   const k=key+":"+lam,t=totals.get(k)||{training:z(),future:z()};
   t.training=add(t.training,mul(weight,training));
   t.future=add(t.future,mul(weight,future));
   totals.set(k,t);fits++;
   if(j===0){var baseTrain=training;}else{
    if(sub(training,baseTrain).n<0n)throw Error("lambda0 is not training minimum");
    trainingDominance++;
   }
  }
 }
 if(fits!==5500||trainingDominance!==4125||counts.size!==10)throw Error("enumeration incomplete");
 const rows=[],summary=[];
 for(const world of archived.worlds){
  const source=world.source,n=world.n_trials_per_x,key=source+":"+n;
  if(!eq(mass.get(key),one))throw Error("training mass not normalized "+key);
  if(counts.get(key)!==(n===1?32:243))throw Error("training table count mismatch");
  const per={};
  for(const lam of lambdas){
   const t=totals.get(key+":"+lam);
   if(!eq(t.future,F(world.lambda_expected_independent_NEW_response_MSE_exact[lam])))throw Error("future archive mismatch "+key+":"+lam);
   const gap=sub(t.future,t.training);
   if(gap.n<=0n)throw Error("expected optimism must be positive");
   per[lam]={train:t.training,future:t.future,gap};
   rows.push({source,n_trials_per_x:n,lambda:lam,expected_training_MSE_exact:show(t.training),
     expected_independent_future_MSE_exact:show(t.future),optimism_gap_exact:show(gap)});
  }
  const train1=sub(per["1"].train,per["0"].train);
  const future1=sub(per["1"].future,per["0"].future);
  summary.push({source,n_trials_per_x:n,lambda1_minus_lambda0_training_MSE_exact:show(train1),
   lambda1_minus_lambda0_future_MSE_exact:show(future1),
   lambda0_training_preferred:train1.n>0n,lambda1_future_preferred:future1.n<0n});
 }
 const result={research_id:"R190",method:"complete 1375 source table weighted exact rational training residual enumeration",
  source_csv_git_blob:"980e757dbc630df68ac3627c2854518e2f6b3fe9",
  source_matrices_git_blob:"7093d918a491e3a6b25f05fcd2937b96a2adb897",
  source_original_results_git_blob:"b3d49f31f3481bb817fea620cd3a55120fe12116",
  worlds:10,training_tables:1375,exact_fitted_risk_cells:5500,world_lambda_rows:rows.length,
  lambda0_samplewise_training_dominance_checks:trainingDominance,
  lambda1_training_worse_worlds:summary.filter(x=>x.lambda0_training_preferred).length,
  lambda1_future_better_worlds:summary.filter(x=>x.lambda1_future_preferred).length,
  all_original_future_risks_exact_match:true,rows,world_summary:summary,
  evidence:"E1_ARTIFICIAL_POSTSCORE",new_E2:0,new_E3:0,external_independent_replications:0,
  R073_model_and_score_unchanged:true,PESEN_v01_unchanged:true};
 return result;
}
if(typeof module!=="undefined"&&module.exports)module.exports={compute};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==5){process.stderr.write("Usage: node script training.csv matrices.json results.json\n");process.exit(2);}
 const result=compute(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8")),JSON.parse(fs.readFileSync(process.argv[4],"utf8")));
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
}