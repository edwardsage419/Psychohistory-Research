"use strict";
// R203 prespecified covariate-pattern transport, exact BigInt rational calculation.
// Run from repository root: node research/validation/r203_covariate_transport_third_method_20261027.js
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(b===0n)throw Error("zero denominator");let g=gcd(a,b);return [a/g,b/g];}
function P(s){let t=String(s).split("/");return F(t[0],t[1]||1);}
function A(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function N(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function M(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function D(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function S(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function E(a,b){return a[0]===b[0]&&a[1]===b[1];}
const Z=F(0),O=F(1),Q=F(1,4),H=F(1,2);
const X={SMOOTH:[1,1,1,1],ALTERNATING:[1,-1,1,-1],MIXED:[1,0,0,-1]};
const C=["IID","SAR_POS","SEM_POS","SAR_NEG","SEM_NEG"];
function mean(c,x){
 if(!c.startsWith("SAR"))return x.map(z=>F(z));
 let r=c.endsWith("POS")?H:F(-1,2),rr=M(r,r),den=N(O,rr),k1=D(r,den),k2=D(rr,den);
 return x.map((v,i)=>{
  let w=D(A(F(x[(i+1)%4]),F(x[(i+3)%4])),F(2));
  let w2=D(A(F(x[i]),F(x[(i+2)%4])),F(2));
  return A(A(F(v),M(k1,w)),M(k2,w2));
 });
}
function risk(s,c,x,z,stale){
 let actual=mean(s,X[z]),prediction=mean(c,X[stale?x:z]);
 let square=Z;
 for(let i=0;i<4;i++){let d=N(actual[i],prediction[i]);square=A(square,M(d,d));}
 return A(s==="IID"?O:F(29,18),M(Q,square));
}
function run(original){
 if(original.research_id!=="R203"||original.worlds.length!==15)throw Error("source identity mismatch");
 let rows=[],checks=0;
 for(const old of original.worlds){
  let x=old.pattern,s=old.true_source;
  if(!X[x]||!C.includes(s))throw Error("unexpected source");
  let probs=C.map(c=>P(old.selected_candidate_probabilities_exact[c]));
  if(!E(probs.reduce((a,b)=>A(a,b),Z),O))throw Error("selection probability sum");
  for(const z of Object.keys(X)){
   let current=Z,stale=Z;
   for(let i=0;i<5;i++){
    current=A(current,M(probs[i],risk(s,C[i],x,z,false)));
    stale=A(stale,M(probs[i],risk(s,C[i],x,z,true)));
   }
   if(x===z){
    if(!E(current,P(old.expected_independent_new_region_MSE_exact)))throw Error("original score mismatch "+x+" "+s);
    if(!E(current,stale))throw Error("same-pattern mismatch");
    checks++;
   }
   rows.push({train_pattern:x,test_pattern:z,true_source:s,
    original_training_vectors:16,independent_test_shocks_per_training:16,
    selected_current_MSE_exact:S(current),selected_stale_MSE_exact:S(stale),
    stale_minus_current_exact:S(N(stale,current)),
    fixed_IID_current_MSE_exact:S(risk(s,"IID",x,z,false)),
    fixed_IID_stale_MSE_exact:S(risk(s,"IID",x,z,true)),
    oracle_known_true_MSE_exact:S(s==="IID"?O:F(29,18)),
    selected_candidate_probabilities_exact:old.selected_candidate_probabilities_exact});
  }
 }
 if(rows.length!==45||checks!==15)throw Error("count mismatch");
 let stats={different_pattern_worlds:0,stale_worse:0,stale_equal:0,stale_better:0,selected_current_better_than_fixed_IID:0,selected_current_equal_fixed_IID:0,selected_current_worse_than_fixed_IID:0};
 function sign(q){let a=P(q);return a[0]>0n?1:a[0]<0n?-1:0;}
 for(let row of rows){
  if(row.train_pattern!==row.test_pattern){
   stats.different_pattern_worlds++;
   let v=sign(row.stale_minus_current_exact);
   if(v>0)stats.stale_worse++;else if(v===0)stats.stale_equal++;else stats.stale_better++;
  }
  let v=sign(S(N(P(row.selected_current_MSE_exact),P(row.fixed_IID_current_MSE_exact))));
  if(v<0)stats.selected_current_better_than_fixed_IID++;
  else if(v===0)stats.selected_current_equal_fixed_IID++;
  else stats.selected_current_worse_than_fixed_IID++;
 }
 return {research_id:"R203",method:"third_covariate_pattern_transport",evidence_class:"E1_ARTIFICIAL_ONLY",
 original_result_git_blob:"ed9cc4865132ebb33de1b22908d1932237586af8",
 protocol_path:"protocols/R203_COVARIATE_TRANSPORT_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",
 worlds:45,original_training_vectors:240,independent_source_pairs:11520,
 original_same_pattern_exact_checks:checks,statistics:stats,results:rows,
 new_E2_predictions:0,new_E3_predictions:0,external_independent_replications:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 const input=JSON.parse(fs.readFileSync("research/R203/R203_EXACT_RESULTS.json","utf8"));
 process.stdout.write(JSON.stringify(run(input),null,2)+"\n");
}
