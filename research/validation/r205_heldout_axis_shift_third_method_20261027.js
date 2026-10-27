// R205 third method: exact heldout axis-mixture shift. Node 18+ standard library only.
// Usage: node research/validation/r205_heldout_axis_shift_third_method_20261027.js research/R205/R205_ALL_240_ORIGINAL_PAIRED_PCA_TRAINING_HISTORIES.csv
"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};}
function P(s){const v=String(s).trim().split("/");return F(v[0],v[1]||1);}
function add(a,b){return F(a.n*b.d+b.n*a.d,a.d*b.d);}
function sub(a,b){return F(a.n*b.d-b.n*a.d,a.d*b.d);}
function mul(a,b){return F(a.n*b.n,a.d*b.d);}
function div(a,b){return F(a.n*b.d,a.d*b.n);}
function cmp(a,b){const z=a.n*b.d-b.n*a.d;return z<0n?-1:z>0n?1:0;}
function S(a){return a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);}
function eq(a,b){if(cmp(a,b)!==0)throw Error("exact mismatch "+S(a)+" != "+S(b));}
const ONE=F(1),ZERO=F(0),HALF=F(1,2);
function compute(csv){
 const lines=csv.trim().split(String.fromCharCode(10)),header=lines.shift().trim().split(",");
 const required=["true_a","true_b","independent_training_pair_count","ordered_training_pair_axes","source_train_probability","training_selected_PC_axis","true_independent_new_event_recon_mse_exact","true_independent_new_event_retained_ratio_exact","true_independent_new_event_target1_mse_exact","true_independent_new_event_target2_mse_exact"];
 for(const k of required)if(!header.includes(k))throw Error("missing "+k);
 const rows=lines.map(line=>{const a=line.trim().split(",");if(a.length!==header.length)throw Error("bad CSV");return Object.fromEntries(header.map((k,i)=>[k,a[i]]));});
 if(rows.length!==240)throw Error("expected 240 training histories");
 const scales=[[1,1],[2,1],[1,2],[3,1],[1,3],[2,2]],qs=["1/20","1/2","19/20"],worlds=[];
 let original_row_regressions=0;
 for(const [a,b] of scales)for(const m of [3,5]){
  const group=rows.filter(r=>+r.true_a===a&&+r.true_b===b&&+r.independent_training_pair_count===m);
  if(group.length!==2**m)throw Error("wrong training history count");
  let sum=ZERO,p=ZERO;
  const seen=new Set();
  for(const r of group){
   const axes=r.ordered_training_pair_axes.split("|").map(Number),k=axes.filter(x=>x===1).length;
   if(axes.length!==m||axes.some(x=>x!==1&&x!==2))throw Error("invalid axes");
   if(seen.has(r.ordered_training_pair_axes))throw Error("duplicate training history");seen.add(r.ordered_training_pair_axes);
   const axis=k*a*a>=(m-k)*b*b?1:2;
   if(axis!==+r.training_selected_PC_axis)throw Error("original PCA mismatch");
   const weight=P(r.source_train_probability);eq(weight,F(1,2**m));
   sum=add(sum,weight);if(axis===1)p=add(p,weight);
   const origRisk=axis===1?F(b*b,2):F(a*a,2);
   eq(origRisk,P(r.true_independent_new_event_recon_mse_exact));original_row_regressions++;
   const origRet=div(sub(F(a*a+b*b),mul(F(2),origRisk)),F(a*a+b*b));
   eq(origRet,P(r.true_independent_new_event_retained_ratio_exact));original_row_regressions++;
   eq(axis===1?ZERO:HALF,P(r.true_independent_new_event_target1_mse_exact));original_row_regressions++;
   eq(axis===1?HALF:ZERO,P(r.true_independent_new_event_target2_mse_exact));original_row_regressions++;
  }
  eq(sum,ONE);
  for(const qstr of qs){
   const q=P(qstr),other=sub(ONE,q),v1=mul(q,F(a*a)),v2=mul(other,F(b*b)),variance=add(v1,v2);
   const risk=add(mul(p,v2),mul(sub(ONE,p),v1));
   const retained=sub(ONE,div(risk,variance));
   const y1=mul(sub(ONE,p),q),y2=mul(p,other);
   const oracleAxis=cmp(v1,v2)>=0?1:2,oracle=oracleAxis===1?v2:v1;
   const oldAxis=a*a>=b*b?1:2,oldRisk=oldAxis===1?v2:v1;
   const regret=sub(risk,oracle),oldRegret=sub(oldRisk,oracle);
   if(cmp(regret,ZERO)<0||cmp(oldRegret,ZERO)<0)throw Error("negative regret");
   if(qstr==="1/2"){const legacy=add(mul(p,F(b*b,2)),mul(sub(ONE,p),F(a*a,2)));eq(risk,legacy);}
   worlds.push({a,b,m,q:qstr,ordered_train_histories:group.length,probability_select_e1:S(p),heldout_variance:S(variance),selected_pca_reconstruction_mse:S(risk),selected_pca_retained_energy_ratio:S(retained),target1_mse:S(y1),target2_mse:S(y2),old_population_pca_axis:oldAxis,old_population_pca_reconstruction_mse:S(oldRisk),test_distribution_oracle_axis:oracleAxis,test_distribution_oracle_reconstruction_mse:S(oracle),selected_pca_oracle_regret:S(regret),old_population_pca_oracle_regret:S(oldRegret)});
  }
 }
 if(worlds.length!==36||original_row_regressions!==960)throw Error("coverage mismatch");
 return {research_id:"R205",method:"HELDOUT_AXIS_MIXTURE_SHIFT_THIRD_METHOD",evidence:"E1_ARTIFICIAL_ONLY",training_csv_git_blob:"89eb97bf0dff7986fbe7b65a46dcdf8c2b0aefa1",prescore_freeze_commit:"773064c873f5bf835b3be7a42965d9bde6e3de81",training_history_rows:rows.length,source_training_worlds:12,shifted_evaluation_worlds:worlds.length,weighted_heldout_event_evaluations:rows.length*4*qs.length,original_row_exact_regressions:original_row_regressions,heldout_axis1_probabilities:qs,new_E2:0,new_E3:0,external_independent_replication:0,worlds};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs");if(process.argv.length<3)throw Error("provide original 240-row CSV path");
 process.stdout.write(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2)+String.fromCharCode(10));
}
