"use strict";
// R203 independent B audit. Integer /6 spatial kernels, 16 future shocks, 240 original train rows.
// Usage: node research/evidence_audit/b_r203_covariate_transport_independent_20261027.js
const X={SMOOTH:[1,1,1,1],ALTERNATING:[1,-1,1,-1],MIXED:[1,0,0,-1]};
const C=["IID","SAR_POS","SEM_POS","SAR_NEG","SEM_NEG"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function frac(n,d){n=BigInt(n);d=BigInt(d);let g=gcd(n,d);return d/g===1n?String(n/g):String(n/g)+"/"+String(d/g);}
function kernel(name){
 if(name==="IID")return [[6,0,0,0],[0,6,0,0],[0,0,6,0],[0,0,0,6]];
 let sg=name.endsWith("POS")?1:-1;
 return Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>{
  let delta=(j-i+4)%4;return delta===0?7:delta===2?1:sg*2;
 }));
}
function mv(K,v){return K.map(row=>row.reduce((a,k,j)=>a+k*v[j],0));}
function mu(name,x){return name.startsWith("SAR")?mv(kernel(name),x):x.map(v=>6*v);}
function observed(source,x,shock){
 let y=mu(source,x),noise=mv(kernel(source),shock);
 return y.map((v,i)=>v+noise[i]);
}
function csvRows(raw){
 let lines=raw.trim().split(/\r?\n/),header=lines.shift().split(",");
 return lines.map(line=>{let vals=line.split(",");if(vals.length!==header.length)throw Error("CSV width mismatch");return Object.fromEntries(header.map((h,i)=>[h,vals[i]]));});
}
function run(csv,receipt){
 let input=csvRows(csv);
 if(input.length!==240)throw Error("original training rows count mismatch");
 let map=new Map(),testShockCount=0,selectedCount=0;
 for(let row of input){
  if(!X[row.covariate_pattern]||!C.includes(row.true_source)||!C.includes(row.selected_candidate))throw Error("unknown source");
  if(row.original_training_source_probability!=="1/16")throw Error("source probability changed");
  selectedCount++;
  for(let test of Object.keys(X)){
   let key=row.covariate_pattern+"|"+row.true_source+"|"+test;
   if(!map.has(key))map.set(key,{train_pattern:row.covariate_pattern,true_source:row.true_source,test_pattern:test,train_count:0,shock_count:0,totals:[0n,0n,0n,0n,0n]});
   let v=map.get(key);v.train_count++;
   let train=X[row.covariate_pattern],z=X[test];
   let predictions=[
    mu(row.selected_candidate,z),mu(row.selected_candidate,train),
    mu("IID",z),mu("IID",train),mu(row.true_source,z)];
   for(let mask=0;mask<16;mask++){
    let eps=Array.from({length:4},(_,i)=>(mask>>i)&1?1:-1);
    let actual=observed(row.true_source,z,eps);
    v.shock_count++;testShockCount++;
    for(let k=0;k<5;k++){
     for(let i=0;i<4;i++){
      let d=BigInt(actual[i]-predictions[k][i]);v.totals[k]+=d*d;
     }
    }
   }
  }
 }
 if(map.size!==45||selectedCount!==240||testShockCount!==11520)throw Error("enumeration count");
 let mismatches=[],fieldChecks=0,oldChecks=0,zeroShockNegatives=0;
 for(let expected of receipt.results){
  let key=expected.train_pattern+"|"+expected.true_source+"|"+expected.test_pattern;
  let row=map.get(key);
  if(!row||row.train_count!==16||row.shock_count!==256)throw Error("incomplete independent source");
  let actual=row.totals.map(n=>frac(n,16n*16n*4n*36n));
  let fields=["selected_current_MSE_exact","selected_stale_MSE_exact","fixed_IID_current_MSE_exact","fixed_IID_stale_MSE_exact","oracle_known_true_MSE_exact"];
  fields.forEach((name,i)=>{fieldChecks++;if(actual[i]!==expected[name])mismatches.push({key,field:name,actual:actual[i],expected:expected[name]});});
  if(expected.train_pattern===expected.test_pattern){oldChecks++;if(actual[0]!==actual[1])throw Error("same-pattern mismatch");}
  if(row.totals[4]>0n)zeroShockNegatives++;
 }
 if(mismatches.length)throw Error("independent risk mismatch: "+JSON.stringify(mismatches.slice(0,5)));
 let transportNegatives=receipt.results.filter(r=>r.train_pattern!==r.test_pattern&&r.selected_current_MSE_exact!==r.selected_stale_MSE_exact).length;
 if(transportNegatives===0||zeroShockNegatives!==45)throw Error("negative control not detected");
 return {audit:"B_R203_COVARIATE_TRANSPORT_INDEPENDENT_INTEGER_ENUMERATION",
 evidence_class:"INTERNAL_E1_PROGRAMMATIC_CROSSCHECK",original_training_rows:240,
 independent_train_test_shock_pairs:11520,worlds:45,exact_field_comparisons:fieldChecks,
 exact_mismatches:mismatches.length,original_same_pattern_checks:oldChecks,
 negative_control_stale_covariate_detected_worlds:transportNegatives,
 negative_control_zero_future_shock_detected_worlds:zeroShockNegatives,
 external_independent_replications:0,real_E2_prediction:0,real_E3_prediction:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 let csv=fs.readFileSync("research/R203/R203_ALL_240_ORIGINAL_SPATIAL_TRAINING_WORLDS.csv","utf8");
 let receipt=JSON.parse(fs.readFileSync("research/validation/R203_COVARIATE_TRANSPORT_45_WORLDS_EXACT_RECEIPT_2026-10-27.json","utf8"));
 process.stdout.write(JSON.stringify(run(csv,receipt),null,2)+"\n");
}
