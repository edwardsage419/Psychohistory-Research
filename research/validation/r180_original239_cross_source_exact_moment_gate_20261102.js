"use strict";
// Independent R180 E1 exact moment audit. Node.js standard library only.
const BLOB_R177="2d032513ce84141214b6b3f84df9c0ed9976a02b";
const SHA_R177="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535";
const BLOB_R180="b30bc0964a8ce89df6d723e32daad10521c538c5";
const BLOB_FREEZE="96fc3fd28ca61719231a33cf5f6507b751ea1ecd";
const SOURCES={IID_BIN:["BIN",0],CLUSTERED_BB_C2:["BB",0],
  CLUSTERED_BB_C8:["BB",2],INACTIVE_ZIB_Z1_8:["ZIB",0],INACTIVE_ZIB_Z1_4:["ZIB",1]};
function need(x,m){if(!x)throw Error(m)}
function gcd(a,b){while(b){let c=a%b;a=b;b=c}return a<0n?-a:a}
function norm(a,b){need(b>0n,"denominator");let g=gcd(a,b);return [a/g,b/g]}
function F(s){s=String(s);need(/^-?\d+(\/[1-9]\d*)?$/.test(s),"fraction");let p=s.split("/");return norm(BigInt(p[0]),BigInt(p[1]||"1"))}
function add(a,b){return norm(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function neg(a){return [-a[0],a[1]]}
function sub(a,b){return add(a,neg(b))}
function mul(a,b){return norm(a[0]*b[0],a[1]*b[1])}
function div(a,b){need(b[0]!==0n,"zero divisor");return norm(a[0]*b[1],a[1]*b[0])}
function pow(a,n){return norm(a[0]**BigInt(n),a[1]**BigInt(n))}
function str(a){return String(a[0])+(a[1]===1n?"":"/"+String(a[1]))}
function audit(r177,r180){
 need(r177.research_id==="R177"&&r180.research_id==="R180","research IDs");
 need(r180.source_R177_git_blob===BLOB_R177&&r180.source_R177_results_sha256===SHA_R177,"upstream pins");
 need(r180.world_count===30&&r180.complete_ordered_sample_count===7750,"sample counts");
 need(r180.new_E2===0&&r180.new_E3===0&&r180.human_or_historical_data_scored===false,"evidence grades");
 need(Array.isArray(r180.all_worlds)&&r180.all_worlds.length===30,"world count");
 let expected=new Set(),seen=new Set(),checks=0,sourceChecks=0;
 for(let m of [2,3,4])for(let p of ["1/4","1/2"])for(let src of Object.keys(SOURCES))expected.add(m+"|"+p+"|"+src);
 for(let w of r180.all_worlds){
   let key=w.m+"|"+w.true_p+"|"+w.source, meta=SOURCES[w.source];
   need(expected.has(key)&&!seen.has(key),"duplicate/missing/extra world "+key);seen.add(key);
   need(w.n_per_cluster===4&&w.source_family===meta[0]&&w.source_regime===meta[1]&&w.ordered_dataset_count===5**w.m,"world metadata "+key);
   let matches=r177.world_data.filter(x=>x.n===4&&x.p===w.true_p&&x.family===meta[0]&&x.regime===meta[1]);
   need(matches.length===1&&JSON.stringify(matches[0].full_PMF)===JSON.stringify(w.source_count_pmf),"upstream PMF "+key);sourceChecks++;
   let p=F(w.true_p),q=w.source_count_pmf.map(F),mass=F(0),mean=F(0),second=F(0),identical=F(0);
   need(q.length===5,"PMF length");
   for(let k=0;k<5;k++){mass=add(mass,q[k]);mean=add(mean,mul(F(k),q[k]));second=add(second,mul(F(k*k),q[k]));identical=add(identical,pow(q[k],w.m))}
   need(str(mass)==="1"&&str(mean)===str(mul(F(4),p)),"mass/mean "+key);
   let varK=sub(second,mul(mean,mean)),trueVar=div(varK,F(16*w.m));
   need(varK[0]>0n,"positive variance");
   let iid=div(sub(mul(p,sub(F(1),p)),trueVar),F(4*w.m));
   let cluster=mul(trueVar,div(F(w.m-1),F(w.m)));
   let values={true_sampling_variance_of_p_hat:trueVar,true_MSE_of_p_hat:trueVar,
    expected_iid_bootstrap_variance:iid,expected_cluster_bootstrap_variance:cluster,
    expected_corrected_cluster_bootstrap_variance:trueVar,
    probability_of_identical_cluster_counts_and_zero_cluster_variance:identical,
    ratio_expected_iid_bootstrap_variance_to_true_variance:div(iid,trueVar)};
   for(let [name,v] of Object.entries(values)){need(w[name]===str(v),"field "+key+" "+name);checks++}
 }
 need(seen.size===expected.size,"incomplete coverage");
 return {status:"PASS",scope:"INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1",worlds:seen.size,
    upstream_PMF_matches:sourceChecks,exact_moment_checks:checks,negative_controls:7,
    interval_coverage:"NOT_RECOMPUTED",bootstrap_PMF:"NOT_RECOMPUTED",E2:0,E3:0};
}
function negatives(r177,r180){
 let copy=x=>JSON.parse(JSON.stringify(x));
 let changes=[
  x=>x.all_worlds[1]=copy(x.all_worlds[0]),x=>x.all_worlds.pop(),
  x=>x.all_worlds[0].source_count_pmf[0]="0",
  x=>x.all_worlds[0].true_sampling_variance_of_p_hat="999",
  x=>x.source_R177_git_blob="0".repeat(40),x=>x.new_E2=1,
  x=>x.all_worlds[0].source_regime=99];
 for(let i=0;i<changes.length;i++){let x=copy(r180);changes[i](x);let rejected=false;try{audit(r177,x)}catch(e){rejected=true}need(rejected,"mutation accepted "+i)}
 return changes.length;
}
if(typeof require==="function"&&typeof process!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
 const root=path.resolve(process.argv[2]||".");
 const read=p=>fs.readFileSync(path.join(root,p));
 const blob=b=>crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");
 const src=read("research/R177/r177_four_finite_count_families_exact.py");
 const freeze=read("protocols/R180_CLUSTER_BOOTSTRAP_30_WORLDS_7750_SAMPLES_PRESCORE_FREEZE_2026-10-21.md");
 const a=read("research/R177/R177_EXACT_RESULTS.json"),b=read("research/R180/R180_EXACT_RESULTS.json");
 need(blob(src)===BLOB_R177&&blob(freeze)===BLOB_FREEZE&&blob(b)===BLOB_R180,"Git blob pins");
 need(crypto.createHash("sha256").update(a).digest("hex")===SHA_R177,"upstream result SHA256");
 let x=JSON.parse(a),y=JSON.parse(b),out=audit(x,y);
 out.negative_controls=negatives(x,y);out.byte_pins="PASS";
 console.log(JSON.stringify(out));
}
