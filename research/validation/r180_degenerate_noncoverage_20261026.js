/* R180 third method, exact finite E1. Run: node research/validation/r180_degenerate_noncoverage_20261026.js
   Source: research/R180/R180_EXACT_RESULTS.json, pinned Git blob b30bc0964a8ce89df6d723e32daad10521c538c5.
   Historical R180 outcomes were visible before this postscore diagnostic. */
"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function F(x){const p=String(x).split("/");let a=BigInt(p[0]),b=BigInt(p[1]||"1");if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
function add(a,b){const g=gcd(a[1],b[1]);const n=a[0]*(b[1]/g)+b[0]*(a[1]/g),d=a[1]*(b[1]/g),h=gcd(n,d);return [n/h,d/h];}
function neg(a){return [-a[0],a[1]];}
function sub(a,b){return add(a,neg(b));}
function mul(a,b){const x=gcd(a[0],b[1]),y=gcd(b[0],a[1]);return [(a[0]/x)*(b[0]/y),(a[1]/y)*(b[1]/x)];}
function pow(a,n){let z=F(1);for(let i=0;i<n;i++)z=mul(z,a);return z;}
function cmp(a,b){const d=a[0]*b[1]-b[0]*a[1];return d<0n?-1:d>0n?1:0;}
function fmt(a){return a[1]===1n?String(a[0]):a[0]+"/"+a[1];}
function assert(ok,msg){if(!ok)throw Error(msg);}
function analyzeR180(input){
 assert(input.research_id==="R180"&&input.world_count===30&&input.all_worlds.length===30,"source universe");
 const out=[], one=F(1), zero=F(0), nominal=F("19/20");
 const names=["IID_BIN","CLUSTERED_BB_C2","CLUSTERED_BB_C8","INACTIVE_ZIB_Z1_8","INACTIVE_ZIB_Z1_4"];
 for(const w of input.all_worlds){
  assert([2,3,4].includes(w.m)&&["1/4","1/2"].includes(w.true_p)&&names.includes(w.source),"unexpected world");
  const q=w.source_count_pmf.map(F),m=w.m,truth=F(w.true_p);
  assert(q.length===5&&cmp(q.reduce(add,zero),one)===0&&q.every(v=>cmp(v,zero)>=0),"invalid source PMF");
  const trueK=4*Number(truth[0])/Number(truth[1]);
  assert(Number.isInteger(trueK)&&trueK>=0&&trueK<=4,"true p grid");
  let identical=zero,miss=zero;
  for(let k=0;k<5;k++){const term=pow(q[k],m);identical=add(identical,term);if(k!==trueK)miss=add(miss,term);}
  const hit=pow(q[trueK],m),ceiling=sub(one,miss);
  assert(cmp(add(hit,miss),identical)===0,"degenerate partition");
  assert(cmp(identical,F(w.probability_of_identical_cluster_counts_and_zero_cluster_variance))===0,"archived zero-variance mass");
  for(const key of ["cluster_corrected_wald","cluster_percentile"])
   assert(cmp(F(w.exact_interval_frequentist_coverages[key]),ceiling)<=0,"coverage exceeds mathematical ceiling");
  out.push({m,source:w.source,true_p:w.true_p,source_count_pmf:w.source_count_pmf,
   identical_mass:fmt(identical),degenerate_miss_mass:fmt(miss),degenerate_hit_mass:fmt(hit),
   cluster_coverage_ceiling:fmt(ceiling),archived_coverage:w.exact_interval_frequentist_coverages});
 }
 assert(out.length===30&&new Set(out.map(x=>x.m+"|"+x.true_p+"|"+x.source)).size===30,"world duplication");
 const below=out.filter(x=>cmp(F(x.cluster_coverage_ceiling),nominal)<0);
 const biggest=out.reduce((a,b)=>cmp(F(a.degenerate_miss_mass),F(b.degenerate_miss_mass))>0?a:b);
 const smallest=out.reduce((a,b)=>cmp(F(a.degenerate_miss_mass),F(b.degenerate_miss_mass))<0?a:b);
 const contrasts={cluster_wald_better:0,cluster_wald_worse:0,cluster_wald_equal:0,cluster_percentile_better:0,cluster_percentile_worse:0,cluster_percentile_equal:0};
 for(const x of out)for(const [prefix,k1,k2] of [["cluster_wald","cluster_corrected_wald","iid_wald"],["cluster_percentile","cluster_percentile","iid_percentile"]]){
  const v=cmp(F(x.archived_coverage[k1]),F(x.archived_coverage[k2]));
  contrasts[prefix+(v>0?"_better":v<0?"_worse":"_equal")]++;
 }
 let strictlyDecreasing=0;
 for(const p of ["1/4","1/2"])for(const source of names){
  const seq=out.filter(x=>x.true_p===p&&x.source===source).sort((a,b)=>a.m-b.m);
  assert(seq.length===3,"missing sequence");
  assert(cmp(F(seq[0].degenerate_miss_mass),F(seq[1].degenerate_miss_mass))>0&&cmp(F(seq[1].degenerate_miss_mass),F(seq[2].degenerate_miss_mass))>0,"nondecreasing miss");
  strictlyDecreasing++;
 }
 assert(cmp(F("0"),zero)===0&&cmp(F("1"),one)===0,"controls");
 const concentratedTrue=[zero,F(1),zero,zero,zero];
 const concentratedWrong=[F(1),zero,zero,zero,zero];
 function missFor(q,p,m){let v=zero;for(let k=0;k<5;k++)if(k!==p*4)v=add(v,pow(q[k],m));return v;}
 assert(cmp(missFor(concentratedTrue,0.25,3),zero)===0,"true point mass negative control");
 assert(cmp(missFor(concentratedWrong,0.25,3),one)===0,"wrong point mass negative control");
 return {research_id:"R180",study:"POSTSCORE_DEGENERATE_NONCOVERAGE_THIRD_METHOD",evidence:"E1_ARTIFICIAL_EXACT",
  source_git_blob_sha1:"b30bc0964a8ce89df6d723e32daad10521c538c5",
  prespecified_addendum_protocol:"protocols/R180_DEGENERATE_CLUSTER_NONCOVERAGE_THIRD_METHOD_PRECOMPUTATION_FREEZE_2026-10-26.md",
  status:"PASS_BOUNDED_INTERNAL_E1_POSTSCORE",world_count:30,all_worlds:out,
  summary:{coverage_ceiling_below_95pct_worlds:below.length,
   by_m:[2,3,4].map(m=>({m,worlds:10,below_95pct:below.filter(x=>x.m===m).length})),
   largest_degenerate_miss:{m:biggest.m,source:biggest.source,true_p:biggest.true_p,mass:biggest.degenerate_miss_mass,ceiling:biggest.cluster_coverage_ceiling},
   smallest_degenerate_miss:{m:smallest.m,source:smallest.source,true_p:smallest.true_p,mass:smallest.degenerate_miss_mass,ceiling:smallest.cluster_coverage_ceiling},
   contrasts,strictly_decreasing_m_sequences:strictlyDecreasing,negative_controls_passed:2,
   original_zero_variance_masses_matched:30,cluster_interval_ceiling_checks:60},
  new_E2:0,new_E3:0,external_independent_replication:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const root=path.resolve(__dirname,"../..");
 const input=JSON.parse(fs.readFileSync(path.join(root,"research/R180/R180_EXACT_RESULTS.json"),"utf8"));
 process.stdout.write(JSON.stringify(analyzeR180(input),null,2)+"\n");
}
if(typeof module!=="undefined")module.exports={analyzeR180};
