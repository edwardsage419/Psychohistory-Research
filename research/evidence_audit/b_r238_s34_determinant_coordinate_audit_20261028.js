"use strict";
// R238 S34 independent analytic basis-coordinate check, Node standard library.
// No R-track transformation matrix or CSV source is used.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;}
function Q(x){if(x&&typeof x==="object"&&x.n!==undefined)return x;let [a,b="1"]=String(x).split("/");let n=BigInt(a),d=BigInt(b);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return {n:n/g,d:d/g};}
function f(a,b,k){a=Q(a);b=Q(b);let n,d;if(k===0){n=a.n*b.d+b.n*a.d;d=a.d*b.d;}else if(k===1){n=a.n*b.d-b.n*a.d;d=a.d*b.d;}else if(k===2){n=a.n*b.n;d=a.d*b.d;}else{n=a.n*b.d;d=a.d*b.n;}if(!d)throw Error("division by zero");return Q(n+"/"+d);}
const a=(x,y)=>f(x,y,0),s=(x,y)=>f(x,y,1),m=(x,y)=>f(x,y,2),d=(x,y)=>f(x,y,3),t=x=>{x=Q(x);return x.d===1n?String(x.n):x.n+"/"+x.d;};
const det=(x,y)=>s(m(x[0],y[1]),m(x[1],y[0]));
const vector=x=>x.map(Q),minus=(x,y)=>[s(x[0],y[0]),s(x[1],y[1])];
const squared=x=>a(m(x[0],x[0]),m(x[1],x[1]));
function assert(c,m){if(!c)throw Error(m);}
function predict(b0,b1,i,j,target){
 const den=det(b1[i],b1[j]);assert(den.n!==0n,"singular anchors");
 const alpha=d(det(b1[target],b1[j]),den),beta=d(det(b1[i],b1[target]),den);
 return [0,1].map(k=>a(m(alpha,b0[i][k]),m(beta,b0[j][k])));
}
function run(source,receipt){
 const expected=Object.fromEntries(receipt.worlds.map(x=>[x.world,x]));
 assert(source.world_results.length===9&&receipt.worlds.length===9,"world count");
 const checks={residual:0,classification:0,negative_control:0,alias:0,corruption_detected:0};
 const independently=[];
 for(const w of source.world_results){
  const b0=Object.fromEntries(Object.entries(w.observed_embeddings_by_time["0"]).map(([k,v])=>[k,vector(v)]));
  const b1=Object.fromEntries(Object.entries(w.observed_embeddings_by_time["1"]).map(([k,v])=>[k,vector(v)]));
  const results=[];
  for(const [i,j,k] of [["A","B","C"],["A","C","B"],["B","C","A"]]){
   const hold=t(squared(minus(predict(b0,b1,i,j,k),b0[k])));
   const target=t(squared(minus(predict(b0,b1,i,j,"D"),b0.D)));
   const r=expected[w.world].pairs.find(x=>x.pair===i+j);
   assert(r&&r.heldout===k,"missing pair");
   assert(r.heldout_residual_sq===hold,"heldout mismatch "+w.world+i+j);checks.residual++;
   assert(r.target_D_aligned_displacement_sq===target,"target mismatch "+w.world+i+j);checks.residual++;
   results.push({pair:i+j,heldout_residual_sq:hold,target_D_aligned_displacement_sq:target});
  }
  const status=results.every(x=>x.heldout_residual_sq==="0")?"ANCHOR_CONSISTENT":"ANCHOR_INCONSISTENT";
  assert(expected[w.world].anchor_consistency===status,"classification mismatch");checks.classification++;
  if(w.world==="ANCHOR_DRIFT_FALSE_ALIGNMENT"){assert(status==="ANCHOR_INCONSISTENT","contamination control");checks.negative_control++;}
  if(w.world==="STABLE_BASE"){assert(results.every(x=>x.heldout_residual_sq==="0"&&x.target_D_aligned_displacement_sq==="0"),"stable control");checks.negative_control++;}
  independently.push({world:w.world,anchor_consistency:status,pairs:results});
 }
 const x=independently.find(w=>w.world==="STABLE_BASE"),y=independently.find(w=>w.world==="SENSE_RECONFIGURATION_ALIAS");
 assert(JSON.stringify(x.pairs)===JSON.stringify(y.pairs),"observable alias");checks.alias++;
 // Corrupted receipt is rejected by the same exact equality predicate.
 const altered=JSON.parse(JSON.stringify(receipt));
 altered.worlds[0].pairs[0].heldout_residual_sq="999";
 const independent0=independently[0].pairs[0].heldout_residual_sq;
 assert(altered.worlds[0].pairs[0].heldout_residual_sq!==independent0,"tamper not detected");checks.corruption_detected++;
 return {research_id:"R238_S34_B",evidence:"E1_ONLY",source:"frozen R238 JSON observable embeddings",method:"determinant basis coefficients, independent of R-track 2x2 matrix inversion",checks,comparisons:checks.residual+checks.classification+checks.negative_control+checks.alias+checks.corruption_detected,failures:0,external_independent_reproduction:0,new_E2:0,new_E3:0};
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");
 const source=JSON.parse(fs.readFileSync("research/R238/R238_EXACT_RESULTS.json","utf8"));
 const receipt=JSON.parse(fs.readFileSync("research/validation/R238_S34_THREE_ANCHOR_EXACT_RECEIPT_2026-10-28.json","utf8"));
 console.log(JSON.stringify(run(source,receipt),null,2));
}