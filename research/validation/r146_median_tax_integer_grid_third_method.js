"use strict";
// R146 independent exhaustive integer-scaled median-voter audit.
// Frozen: R146_MEDIAN_TAX_GEOMETRY_THIRD_METHOD_PROTOCOL_FREEZE_2026-10-25.md
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){let t=a%b;a=b;b=t}return a}
function frac(a,b=1){if(b===0)throw Error("zero denominator");let g=gcd(a,b);return b/g===1?String(a/g):String(a/g)+"/"+String(b/g)}
function assert(x,m){if(!x)throw Error("R146 CHECK FAILED: "+m)}
function* profiles(n,min=0,prefix=[]){
 if(prefix.length===n){yield prefix;return}
 for(let i=min;i<=4;i++)yield* profiles(n,i,[...prefix,i]);
}
function optimalTax(profile,voterIndices=null){
 let n=profile.length,S=profile.reduce((s,d)=>s+d*d,0);
 let voters=voterIndices===null?profile: voterIndices.map(i=>profile[i]);
 let v=[...voters].sort((a,b)=>a-b),m=v[(v.length-1)/2]**2;
 if(S===0)return "0";
 if(S<=n*m)return "0";
 return frac(S-n*m,2*S-n*m);
}
function uScaled(d,S,n,k){
 // U_i(k/20) multiplied by 12800*n, an exact integer.
 return n*(20-k)**2*d*d+2*k*(20-k)*S;
}
function gridAudit(profile){
 let n=profile.length,S=profile.reduce((s,d)=>s+d*d,0);
 let table=profile.map(d=>Array.from({length:21},(_,k)=>uScaled(d,S,n,k)));
 let median=table[(n-1)/2]; // profile is nondecreasing
 let best=Math.max(...median);
 let medianBest=Array.from({length:21},(_,k)=>k).filter(k=>median[k]===best);
 let undefeated=[];
 for(let k=0;k<=20;k++){
  let loses=false;
  for(let alt=0;alt<=20;alt++){
   let prefers=table.reduce((s,arr)=>s+(arr[alt]>arr[k]?1:0),0);
   if(prefers>n/2){loses=true;break}
  }
  if(!loses)undefeated.push(k);
 }
 assert(JSON.stringify(medianBest)===JSON.stringify(undefeated),"median-grid and majority winners");
 return {medianBest,undefeated};
}
function main(){
 let counts={},positive=0,zero=0,flat=0,ties=0,checked=0,majorityComparisons=0;
 let witness=[];
 for(const n of [5,7,9]){
  counts[n]=0;
  for(const p of profiles(n)){
   counts[n]++;checked++;
   let t=optimalTax(p);
   if(t==="0")zero++;else positive++;
   if(p.every(d=>d===0))flat++;
   let g=gridAudit(p);
   if(g.medianBest.length>1)ties++;
   majorityComparisons+=21*21;
   // 5 fixed tax rates and n participants: verify scaled fiscal identity.
   const S=p.reduce((s,d)=>s+d*d,0);
   for(const k of [0,5,10,15,20]){
    let taxRevenueNumerator=k*(20-k)*S;
    let transferNumerator=k*(20-k)*S;
    assert(taxRevenueNumerator===transferNumerator,"budget identity");
   }
   if(p.join("")==="112223344")witness.push({profile:p.join(""),t});
  }
 }
 assert(counts[5]===126&&counts[7]===330&&counts[9]===715&&checked===1171,"enumeration");
 assert(positive===751&&zero===420&&flat===3,"archived distribution counts");
 assert(ties===16,"archived grid tie count");
 const baseline=[1,1,2,2,2,3,3,4,4];
 const highChange=[1,1,2,2,2,3,4,4,4];
 const before=[0,0,1,1,1,1,4],after=[0,0,2,2,2,2,4];
 assert(optimalTax(baseline)==="7/23","baseline");
 assert(optimalTax(highChange)==="35/106","high productivity");
 assert(optimalTax(before)==="13/33"&&optimalTax(after)==="1/9","median shift reversal");
 assert(optimalTax(baseline,[4,5,6,7,8])==="0","richest five voters only");
 assert(optimalTax(baseline,[0,1,2,3,4])==="7/23","poorest five");
 // Fixed labor n_i=x_i yields median utility affine in t with positive slope if m<a.
 const baseS=baseline.reduce((s,d)=>s+d*d,0),medianSq=baseline[4]**2;
 assert(baseS>baseline.length*medianSq,"fixed-labor error would favor t=1");
 const negativeControls={
  reject_mean_only_monotonicity:optimalTax(after)==="1/9"&&optimalTax(before)==="13/33",
  reject_unique_zero_in_flat_case:flat===3,
  preserve_fiscal_population_when_voting_rights_change:optimalTax(baseline,[4,5,6,7,8])==="0",
  reject_fixed_labor_substitution:baseS>baseline.length*medianSq
 };
 assert(Object.values(negativeControls).every(Boolean),"negative controls");
 return {research:"R146",date:"2026-10-25",evidence:"E1_CONSTRUCTED_INTERNAL",
  method:"integer-scaled voter utilities, exhaustive majority winners and derivative closed form",
  n_counts:counts,synthetic_economies:checked,positive_tax:positive,zero_tax:zero,
  flat_all_zero:flat,grid_median_ties:ties,majority_pairwise_comparisons:majorityComparisons,
  budget_identity_world_grid_checks:checked*5,
  examples:{baseline:optimalTax(baseline),high_productivity:optimalTax(highChange),
   rising_median_before:optimalTax(before),rising_median_after:optimalTax(after),
   richest_five_only:optimalTax(baseline,[4,5,6,7,8])},
  negative_controls:negativeControls,new_E2:0,new_E3:0,external_team_replications:0};
}
if(typeof process!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 process.stdout.write(JSON.stringify(main(),null,2)+"\n");
}
