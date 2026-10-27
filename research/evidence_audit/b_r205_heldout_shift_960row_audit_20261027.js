// B track independent 960-row importance-weighted audit of R205 heldout shift.
// Usage: node research/evidence_audit/b_r205_heldout_shift_960row_audit_20261027.js research/R205/R205_ALL_960_INDEPENDENT_TEST_SOURCE_PAIRS.csv research/validation/R205_HELDOUT_AXIS_SHIFT_36_EXACT_RECEIPT_2026-10-27.json
"use strict";
function g(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero divisor");if(b<0n){a=-a;b=-b;}let d=g(a,b);return [a/d,b/d];}
function read(s){let z=String(s).trim().split("/");return Q(z[0],z[1]||1);}
function plus(x,y){return Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function minus(x,y){return Q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function times(x,y){return Q(x[0]*y[0],x[1]*y[1]);}
function over(x,y){return Q(x[0]*y[1],x[1]*y[0]);}
function same(x,y){return x[0]*y[1]===y[0]*x[1];}
function string(x){return x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);}
function audit(csv,receipt){
 const doc=typeof receipt==="string"?JSON.parse(receipt):receipt;
 const ls=csv.trim().split(String.fromCharCode(10)),keys=ls.shift().trim().split(",");
 const rows=ls.map(line=>{let v=line.trim().split(",");if(v.length!==keys.length)throw Error("CSV schema");return Object.fromEntries(keys.map((k,i)=>[k,v[i]]));});
 if(rows.length!==960||doc.worlds.length!==36)throw Error("incomplete inputs");
 const Z=Q(0),O=Q(1),TWO=Q(2),checks={original_row_geometry:0,world_exact_field_comparisons:0,world_probability_checks:0,negative_controls:0};
 for(const r of rows){
  const a=+r.true_a,b=+r.true_b,axis=+r.true_heldout_axis,sign=+r.true_heldout_sign,pc=+r.selected_PC_axis_using_training_only;
  const x=+r.new_independent_holdout_x1,y=+r.new_independent_holdout_x2;
  if(![1,2].includes(axis)||![1,2].includes(pc)||![1,-1].includes(sign))throw Error("invalid geometry");
  if((axis===1&&(x!==sign*a||y!==0))||(axis===2&&(x!==0||y!==sign*b)))throw Error("geometry");
  const loss=pc===1?y*y:x*x,t1=pc===1?0:(x/a)**2,t2=pc===2?0:(y/b)**2;
  if(!same(read(r.new_independent_reconstruction_error_exact),Q(loss))||!same(read(r.new_independent_target1_error_exact),Q(t1))||!same(read(r.new_independent_target2_error_exact),Q(t2)))throw Error("original losses differ");
  checks.original_row_geometry+=4;
 }
 for(const w of doc.worlds){
  const selected=rows.filter(r=>+r.true_a===w.a&&+r.true_b===w.b&&+r.independent_training_pair_count===w.m);
  if(selected.length!==4*2**w.m)throw Error("wrong world source rows");
  const q=read(w.q),oldAxis=w.old_population_pca_axis;
  let mass=Z,risk=Z,t1=Z,t2=Z,varsum=Z,ax1=Z,ax2=Z,p=Z,oldRisk=Z;
  for(const r of selected){
   const axis=+r.true_heldout_axis,pc=+r.selected_PC_axis_using_training_only;
   const original=read(r.source_joint_probability_exact);
   if(!same(original,Q(1,4*2**w.m)))throw Error("original weight");
   const shift=axis===1?times(TWO,q):times(TWO,minus(O,q));
   const weight=times(original,shift);
   const x=+r.new_independent_holdout_x1,y=+r.new_independent_holdout_x2;
   mass=plus(mass,weight);
   if(pc===1)p=plus(p,weight);
   risk=plus(risk,times(weight,read(r.new_independent_reconstruction_error_exact)));
   t1=plus(t1,times(weight,read(r.new_independent_target1_error_exact)));
   t2=plus(t2,times(weight,read(r.new_independent_target2_error_exact)));
   varsum=plus(varsum,times(weight,Q(x*x+y*y)));
   ax1=plus(ax1,times(weight,Q(x*x)));ax2=plus(ax2,times(weight,Q(y*y)));
   oldRisk=plus(oldRisk,times(weight,Q(oldAxis===1?y*y:x*x)));
  }
  if(!same(mass,O))throw Error("world probability mass");checks.world_probability_checks++;
  const oracleAxis=ax1[0]*ax2[1]>=ax2[0]*ax1[1]?1:2;
  const oracle=oracleAxis===1?ax2:ax1;
  const calculated={probability_select_e1:p,heldout_variance:varsum,selected_pca_reconstruction_mse:risk,selected_pca_retained_energy_ratio:minus(O,over(risk,varsum)),target1_mse:t1,target2_mse:t2,old_population_pca_reconstruction_mse:oldRisk,test_distribution_oracle_reconstruction_mse:oracle,selected_pca_oracle_regret:minus(risk,oracle),old_population_pca_oracle_regret:minus(oldRisk,oracle)};
  for(const [k,v] of Object.entries(calculated)){if(!same(v,read(w[k])))throw Error("mismatch "+JSON.stringify({a:w.a,b:w.b,m:w.m,q:w.q,k,got:string(v),want:w[k]}));checks.world_exact_field_comparisons++;}
  if(oracleAxis!==w.test_distribution_oracle_axis)throw Error("oracle axis mismatch");checks.world_exact_field_comparisons++;
  if(oldAxis!==(w.a*w.a>=w.b*w.b?1:2))throw Error("population axis mismatch");checks.world_exact_field_comparisons++;
  // Predeclared negative controls: future-axis oracle is inadmissible; wrong-q weights change some worlds.
  if(!same(risk,Z))checks.negative_controls++;
  if(w.q==="1/20"){
   const wrong=over(plus(times(p,Q(w.b*w.b)),times(minus(O,p),Q(w.a*w.a))),TWO);
   if(!same(risk,wrong))checks.negative_controls++;
  }
 }
 if(checks.world_exact_field_comparisons!==36*12||checks.world_probability_checks!==36)throw Error("coverage");
 return {audit_id:"B_R205_HELDOUT_AXIS_SHIFT_960_ROW_INDEPENDENT",evidence:"E1_INTERNAL_PROGRAMMATIC_RECHECK",prescore_freeze_commit:doc.prescore_freeze_commit,source_original_heldout_rows:rows.length,shifted_worlds:doc.worlds.length,checks,all_passed:true,external_independent_replication:0,new_E2:0,new_E3:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs");if(process.argv.length<4)throw Error("provide 960 CSV and R receipt paths");
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8")),null,2)+String.fromCharCode(10));
}
