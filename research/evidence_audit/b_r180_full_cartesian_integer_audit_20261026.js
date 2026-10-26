/* R180 independent exact audit. Run: node research/evidence_audit/b_r180_full_cartesian_integer_audit_20261026.js */
"use strict";
const fs=require("fs"),path=require("path");
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
function lcm(a,b){return a/gcd(a,b)*b;}
function frac(x){const v=String(x).split("/");return [BigInt(v[0]),BigInt(v[1]||"1")];}
function equal(n,d,f){const [a,b]=frac(f);return n*b===a*d;}
function assert(x,msg){if(!x)throw Error(msg);}
function binom(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-i+1)/BigInt(i);return v;}
const iidCache=new Map(),clusterCache=new Map();
function quantile(counts,total,alphaNumerator){let sum=0n;for(let j=0;j<counts.length;j++){sum+=counts[j];if(40n*sum>=alphaNumerator*total)return j;}throw Error("quantile");}
function iidLimits(n,S){
 const key=n+":"+S;if(iidCache.has(key))return iidCache.get(key);
 const ss=BigInt(S),nn=BigInt(n),weights=[];
 for(let j=0;j<=n;j++)weights.push(binom(n,j)*ss**BigInt(j)*(nn-ss)**BigInt(n-j));
 const den=nn**nn;assert(weights.reduce((a,b)=>a+b,0n)===den,"IID binomial mass");
 const ans=[quantile(weights,den,1n),quantile(weights,den,39n)];iidCache.set(key,ans);return ans;
}
function clusterLimits(sorted){
 const m=sorted.length,key=sorted.join(",");
 if(clusterCache.has(key))return clusterCache.get(key);
 const dist=Array(4*m+1).fill(0n),paths=m**m;
 for(let i=0;i<paths;i++){
  let z=i,total=0;for(let j=0;j<m;j++){total+=sorted[z%m];z=Math.floor(z/m);}dist[total]++;
 }
 const den=BigInt(paths);assert(dist.reduce((a,b)=>a+b,0n)===den,"cluster mass");
 const ans=[quantile(dist,den,1n),quantile(dist,den,39n)];clusterCache.set(key,ans);return ans;
}
function auditR180(original,main){
 assert(original.all_worlds.length===30&&main.all_worlds.length===30,"source count");
 const rows=[];let paths=0,parities=0;
 for(const w of original.all_worlds){
  const m=w.m,n=4*m,t=w.true_p==="1/4"?1:2,target=m*t;
  assert([2,3,4].includes(m),"m");
  const rational=w.source_count_pmf.map(frac);
  let D=1n;for(const x of rational)D=lcm(D,x[1]);
  const weights=rational.map(x=>x[0]*(D/x[1]));
  assert(weights.reduce((a,b)=>a+b,0n)===D,"source mass");
  const den=D**BigInt(m),count=5**m;
  let total=0n,same=0n,miss=0n,hit=0n;
  const covers={iid_wald:0n,cluster_corrected_wald:0n,iid_percentile:0n,cluster_percentile:0n};
  for(let code=0;code<count;code++){
   let z=code,product=1n,S=0,Q=0,first=-1,allSame=true;
   const ks=[];
   for(let j=0;j<m;j++){const k=z%5;z=Math.floor(z/5);ks.push(k);S+=k;Q+=k*k;product*=weights[k];if(first<0)first=k;else if(k!==first)allSame=false;}
   total+=product;paths++;
   if(allSame){same+=product;if(first===t)hit+=product;else miss+=product;}
   const d=BigInt(S-target),bm=BigInt(m),bn=BigInt(n),bs=BigInt(S),bQ=BigInt(Q);
   if(625n*bn*d*d<=2401n*bs*(bn-bs))covers.iid_wald+=product;
   if(625n*BigInt(m-1)*d*d<=2401n*(bm*bQ-bs*bs))covers.cluster_corrected_wald+=product;
   const il=iidLimits(n,S);if(il[0]<=target&&target<=il[1])covers.iid_percentile+=product;
   const cl=clusterLimits(ks.slice().sort((a,b)=>a-b));if(cl[0]<=target&&target<=cl[1])covers.cluster_percentile+=product;
  }
  assert(total===den&&same===miss+hit,"source partition");
  assert(equal(same,den,w.probability_of_identical_cluster_counts_and_zero_cluster_variance),"archived zero variance");
  const mr=main.all_worlds.find(x=>x.m===m&&x.true_p===w.true_p&&x.source===w.source);
  assert(!!mr,"main world");
  for(const [n,d,v] of [[miss,den,mr.degenerate_miss_mass],[hit,den,mr.degenerate_hit_mass],[same,den,mr.identical_mass],[den-miss,den,mr.cluster_coverage_ceiling]])
   assert(equal(n,d,v),"independent bound mismatch");
  for(const key of Object.keys(covers)){assert(equal(covers[key],den,w.exact_interval_frequentist_coverages[key]),"archived coverage "+key);parities++;}
  rows.push({m,source:w.source,true_p:w.true_p,enumerated_samples:count,exact_mass_denominator:String(den),
   same_numerator:String(same),miss_numerator:String(miss),hit_numerator:String(hit),
   all_four_interval_coverage_parity:true});
 }
 assert(paths===7750&&parities===120&&clusterCache.size===120,"audit coverage");
 const tests=[
  equal(0n,1n,"0"),equal(1n,1n,"1"),
  (()=>{const t=[1,1,1];return clusterLimits(t)[0]===3&&clusterLimits(t)[1]===3;})(),
  (()=>{const t=[0,0,0];return clusterLimits(t)[0]===0&&clusterLimits(t)[1]===0;})()
 ];
 assert(tests.every(Boolean),"negative controls");
 return {study:"R180_INDEPENDENT_CARTESIAN_INTEGER_AUDIT",status:"PASS_BOUNDED_INTERNAL_E1",
  original_source_git_blob_sha1:"b30bc0964a8ce89df6d723e32daad10521c538c5",
  worlds:30,ordered_sample_paths:paths,unique_conditional_cluster_profiles:clusterCache.size,
  archived_interval_coverage_exact_parities:parities,archived_zero_variance_parities:30,
  independent_new_bound_parities:120,negative_controls:tests.length,
  algorithm:"integer common denominator, base5 ordered sample enumeration, integer squared Wald comparisons, direct conditional binomial and m^m group resample quantiles",
  all_worlds:rows,new_E2:0,new_E3:0,external_independent_replication:0};
}
if(require.main===module){
 const root=path.resolve(__dirname,"../..");
 const a=JSON.parse(fs.readFileSync(path.join(root,"research/R180/R180_EXACT_RESULTS.json"),"utf8"));
 const b=JSON.parse(fs.readFileSync(path.join(root,"research/validation/R180_DEGENERATE_NONCOVERAGE_THIRD_METHOD_EXACT_RECEIPT_2026-10-26.json"),"utf8"));
 process.stdout.write(JSON.stringify(auditR180(a,b),null,2)+"\n");
}
module.exports={auditR180};
