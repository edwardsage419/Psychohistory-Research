#!/usr/bin/env node
"use strict";
/*
 R273 secondary E1 synthetic partial-identification analysis (2026-11-17).
 Full replay of all original 1728 records. New source-only minimax theorem
 over target Bernoulli probabilities {1/4, 3/4}, after original freeze.
 No original science files, scoring rules or historical receipts are modified.

 Usage:
 node research/R273/secondary_source_only_minimax_20261117/verify.js
 node .../verify.js path/to/source.csv path/to/exact_results.json
*/
const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
const HERE=path.resolve(__dirname,"..");
const FILES=[
 path.join(HERE,"R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv"),
 path.join(HERE,"R273_EXACT_CROSS_POPULATION_RESULTS.json"),
];
const PINS=[
 "b4f417d0b218fd1aaa9082ab7a49e52675df59af9fd80841e74888b31dcd6d52",
 "1f1e35d20ddd486bb7d71c65cea96e9590912268c93f17ad1ec99b7f6ac463b8",
];
const HEADER=[
 "world","source_group_true_p","target_group_true_p","fixed_predictor",
 "original_full_source_target_sixbits","original_source_group_fourbits",
 "original_target_group_twobits","source_training_successes",
 "target_test_successes","exact_two_population_source_probability",
 "frozen_before_target_observation_forecast",
 "original_source_group_train_Brier_per_row",
 "original_target_group_test_Brier_per_row",
 "source_mean_Brier","target_independent_mean_Brier","target_forecast_bias"
];
const PROBS=["1/4","1/2","3/4"], MODELS=["SOURCE_ORACLE","SOURCE_LAPLACE","TARGET_ORACLE"];
function requireTrue(value,tag){if(value!==true)throw Error("R273_FAIL_CLOSED_"+tag);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a;}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);requireTrue(d!==0n,"DENOMINATOR");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return[n/g,d/g];}
function F(v){const str=String(v),parts=str.split("/");requireTrue(parts.length<=2,"FRACTION_PARSE");const q=Q(parts[0],parts.length===2?parts[1]:1n);requireTrue(show(q)===str,"CANONICAL_FRACTION");return q;}
const add=(a,b)=>Q(a[0]*b[1]+a[1]*b[0],a[1]*b[1]);
const sub=(a,b)=>Q(a[0]*b[1]-a[1]*b[0],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const sq=a=>mul(a,a);
const pow=(a,n)=>Q(a[0]**BigInt(n),a[1]**BigInt(n));
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const sum=xs=>xs.reduce(add,Q(0));
const show=a=>a[1]===1n?String(a[0]):a.join("/");
const lt=(a,b)=>a[0]*b[1]<b[0]*a[1];
const brier=(p,q)=>add(mul(p,sq(sub(Q(1),q))),mul(sub(Q(1),p),sq(q)));
const fmtP=p=>"P"+p.replace("/","OF");
const world=(a,b,model)=>"A"+fmtP(a).slice(1)+"_B"+fmtP(b).slice(1)+"_"+model;
function bitCount(bits){return [...bits].reduce((s,c)=>s+Number(c),0);}
function modelQ(a,b,k,model){if(model==="SOURCE_ORACLE")return F(a);if(model==="TARGET_ORACLE")return F(b);if(model==="SOURCE_LAPLACE")return Q(k+1,6);throw Error("UNKNOWN_MODEL");}
function binomial(n,k){let p=1;for(let i=1;i<=k;i++)p=p*(n-i+1)/i;return p;}
function formulaRisk(a,b,model) {
 const aa=F(a),bb=F(b),targetNoise=mul(bb,sub(Q(1),bb));
 if(model==="TARGET_ORACLE")return targetNoise;
 if(model==="SOURCE_ORACLE")return add(targetNoise,sq(sub(aa,bb)));
 const mean=div(add(mul(Q(4),aa),Q(1)),Q(6));
 const variance=div(mul(aa,sub(Q(1),aa)),Q(9));
 return add(targetNoise,add(variance,sq(sub(mean,bb))));
}
function compute(sourceText,resultsText){
 const lines=sourceText.trimEnd().split(/\r?\n/);
 requireTrue(lines.length===1729,"SOURCE_RECORD_COUNT");
 requireTrue(lines[0]===HEADER.join(","),"SOURCE_HEADER");
 const archive=JSON.parse(resultsText);
 requireTrue(archive.worlds===27&&archive.all_artificial_source_types===1728,"OLD_RESULT_UNIVERSE");
 const exact=archive.world_results;
 requireTrue(exact.length===27,"OLD_RESULT_WORLDS");
 const observed=new Map(), sourceMargins=new Map(), seen=new Set();
 let all=0;
 for(let i=1;i<lines.length;i++){
  const cells=lines[i].split(",");
  requireTrue(cells.length===HEADER.length,"CSV_COLUMNS");
  const row=Object.fromEntries(HEADER.map((h,j)=>[h,cells[j]]));
  const a=row.source_group_true_p,b=row.target_group_true_p,m=row.fixed_predictor;
  requireTrue(PROBS.includes(a)&&PROBS.includes(b)&&MODELS.includes(m),"MODEL_UNIVERSE");
  const bits=row.original_full_source_target_sixbits,aa=row.original_source_group_fourbits,bb=row.original_target_group_twobits;
  requireTrue(bits.length===6&&/^[01]{6}$/.test(bits)&&aa===bits.slice(0,4)&&bb===bits.slice(4),"SIX_BIT_SOURCE");
  requireTrue(row.world===world(a,b,m),"WORLD_LABEL");
  const key=row.world+"|"+bits;requireTrue(!seen.has(key),"DUPLICATE_SOURCE");seen.add(key);
  const k=bitCount(aa),j=bitCount(bb);
  requireTrue(row.source_training_successes===String(k)&&row.target_test_successes===String(j),"COUNT_FIELDS");
  const pa=F(a),pb=F(b);
  const w=mul(mul(pow(pa,k),pow(sub(Q(1),pa),4-k)),
              mul(pow(pb,j),pow(sub(Q(1),pb),2-j)));
  requireTrue(eq(w,F(row.exact_two_population_source_probability)),"SOURCE_MASS");
  const q=modelQ(a,b,k,m);
  requireTrue(eq(q,F(row.frozen_before_target_observation_forecast)),"FORECAST");
  const losses=[...bits].map(x=>sq(sub(Q(Number(x)),q)));
  const savedTrain=row.original_source_group_train_Brier_per_row.split(";").map(F),savedTest=row.original_target_group_test_Brier_per_row.split(";").map(F);
  requireTrue(savedTrain.length===4&&savedTest.length===2,"LOSS_LENGTHS");
  requireTrue(savedTrain.every((v,i)=>eq(v,losses[i]))&&savedTest.every((v,i)=>eq(v,losses[i+4])),"PER_BIT_LOSS");
  const training=div(sum(losses.slice(0,4)),Q(4)),test=div(sum(losses.slice(4)),Q(2));
  requireTrue(eq(training,F(row.source_mean_Brier))&&eq(test,F(row.target_independent_mean_Brier)),"SCORE_MEANS");
  requireTrue(eq(sub(q,pb),F(row.target_forecast_bias)),"FORECAST_BIAS");
  const current=observed.get(row.world)||{mass:Q(0),risk:Q(0),count:0};
  current.mass=add(current.mass,w);current.risk=add(current.risk,mul(w,test));current.count++;
  observed.set(row.world,current);
  const mkey=[a,b,m,aa].join("|");
  sourceMargins.set(mkey,add(sourceMargins.get(mkey)||Q(0),w));
  all++;
 }
 requireTrue(all===1728&&seen.size===1728,"SOURCE_UNIVERSE");
 for(const archived of exact){
  const a=archived.source_p,b=archived.target_p,m=archived.predictor,expectedWorld=world(a,b,m);
  requireTrue(archived.world===expectedWorld,"OLD_WORLD_LABEL");
  const v=observed.get(expectedWorld);
  requireTrue(Boolean(v)&&v.count===64&&eq(v.mass,Q(1)),"WORLD_SOURCE_COUNTS_AND_MASS");
  requireTrue(eq(v.risk,F(archived.complete_source_expected_target_test_Brier)),"OLD_WORLD_TEST_RISK");
  requireTrue(eq(v.risk,formulaRisk(a,b,m)),"INDEPENDENT_MOMENT_FORMULA");
 }
 // The same 4-bit training history is exactly equally probable under every
 // target b; target labels remain unobserved by a source-only algorithm.
 let identicalMarginals=0;
 for(const a of PROBS)for(const m of MODELS)for(let k=0;k<16;k++){
  const bits=k.toString(2).padStart(4,"0");
  const probs=PROBS.map(b=>sourceMargins.get([a,b,m,bits].join("|")));
  requireTrue(probs.every(p=>Boolean(p)&&eq(p,probs[0])),"SOURCE_ONLY_INDISTINGUISHABILITY");
  identicalMarginals++;
 }
 const targetEnds=["1/4","3/4"],rows=[];
 for(const a of PROBS){
  const row={source_p:a,source_only_training_histories:16,source_only_marginals_identical_across_all_three_targets:true,predictors:[]};
  const aa=F(a);
  for(const candidate of ["SOURCE_ORACLE","SOURCE_LAPLACE","CONSTANT_HALF"]){
   const regrets=targetEnds.map(b=>{
    if(candidate==="CONSTANT_HALF")return sq(sub(Q(1,2),F(b)));
    const full=observed.get(world(a,b,candidate)).risk;
    return sub(full,mul(F(b),sub(Q(1),F(b))));
   });
   const average=div(add(regrets[0],regrets[1]),Q(2));
   const maximum=lt(regrets[0],regrets[1])?regrets[1]:regrets[0];
   const theoreticalMean=candidate==="SOURCE_ORACLE"?aa:
      candidate==="SOURCE_LAPLACE"?div(add(mul(Q(4),aa),Q(1)),Q(6)):Q(1,2);
   const variance=candidate==="SOURCE_LAPLACE"?div(mul(aa,sub(Q(1),aa)),Q(9)):Q(0);
   const lowerBoundRHS=add(add(variance,sq(sub(theoreticalMean,Q(1,2)))),Q(1,16));
   requireTrue(eq(average,lowerBoundRHS),"AVERAGE_MINIMAX_IDENTITY");
   requireTrue(!lt(maximum,Q(1,16)),"MINIMAX_LOWER_BOUND");
   row.predictors.push({name:candidate,
      target_one_quarter_excess_brier:show(regrets[0]),
      target_three_quarters_excess_brier:show(regrets[1]),
      average_two_target_excess_brier:show(average),
      worst_two_target_excess_brier:show(maximum),
      theorem_average_identity_holds:true});
  }
  const halfway=row.predictors.find(x=>x.name==="CONSTANT_HALF");
  requireTrue(halfway.worst_two_target_excess_brier==="1/16","SHARP_UPPER_WITNESS");
  rows.push(row);
 }
 return {
  status:"PASS_R273_SOURCE_ONLY_TARGET_INDISCERNIBILITY_MINIMAX_BOUND",
  evidence:"SECONDARY_ARTIFICIAL_E1_NONBLIND",
  archived_source_rows:all,archived_frozen_worlds:exact.length,
  identical_source_marginal_checks:identicalMarginals,
  source_only_observable:"only 4 independent Bernoulli(a) training bits",
  target_set:"Bernoulli(1/4) versus Bernoulli(3/4)",
  excess_risk_definition:"expected_Brier - b*(1-b)",
  theorem:"(excess_risk_b=1/4 + excess_risk_b=3/4)/2 = E[(q(A)-1/2)^2] + 1/16",
  minimax_excess_lower_bound:"1/16",
  minimax_witness:"CONSTANT_HALF_q=1/2_SOURCE_ONLY",
  not_a_frozen_predictor:"CONSTANT_HALF is a post hoc comparison; original frozen models unchanged",
  source_target_pairs:rows,new_real_human_E2:0,new_real_historical_E3:0,
  frozen_study_grade_upgraded:false,
 };
}
function main(){
 const files=[process.argv[2]||FILES[0],process.argv[3]||FILES[1]];
 const blobs=files.map(x=>fs.readFileSync(x));
 for(let i=0;i<blobs.length;i++){
  const actual=crypto.createHash("sha256").update(blobs[i]).digest("hex");
  requireTrue(actual===PINS[i],"ARCHIVE_SHA256_"+i);
 }
 const result=compute(blobs[0].toString("utf8"),blobs[1].toString("utf8"));
 result.input_sha256=PINS[0];result.result_json_sha256=PINS[1];
 const mutated=blobs[0].toString("utf8").replace("729/4096","731/4096");
 requireTrue(mutated!==blobs[0].toString("utf8"),"NEGATIVE_CONTROL_PREIMAGE");
 let rejected=false;
 try{compute(mutated,blobs[1].toString("utf8"));}catch(error){rejected=error.message==="R273_FAIL_CLOSED_SOURCE_MASS";}
 requireTrue(rejected,"SOURCE_PROBABILITY_NEGATIVE_CONTROL");
 result.negative_controls=["SOURCE_MASS_MUTATION_REJECTED","ARCHIVE_INPUT_SHA256_PINNED"];
 console.log(JSON.stringify(result,null,2));
}
if(require.main===module)main();
module.exports={compute};
