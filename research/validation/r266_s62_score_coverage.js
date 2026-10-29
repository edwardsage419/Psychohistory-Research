#!/usr/bin/env node
"use strict";
const EXPECTED_SOURCE_SHA = "5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a";
const FREEZE = "6cdc35c36bdf6d2f06761dff5b04a8af8aa1bd8b";
function gcd(a,b){while(b){const r=a%b;a=b;b=r;}return a<0n?-a:a;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function P(s){const a=String(s).split("/");if(a.length>2)throw Error("invalid fraction");return F(BigInt(a[0]),a.length===2?BigInt(a[1]):1n);}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function div(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function audit(csvText,baseline){
 if(baseline.research_id!=="R266"||baseline.original_complete_total_source_types!==5328||baseline.worlds.length!==9)throw Error("wrong baseline");
 const header=["world","function","evaluations","design","primitive_independent_draws","original_source_tuple","exact_source_mass","event_success_count","estimate","true_integral","squared_error"].join(",");
 const lines=csvText.trimEnd().split(/\r?\n/);
 if(lines[0]!==header||lines.length!==5329)throw Error("source header or total mismatch");
 const ref=new Map(baseline.worlds.map(w=>[w.world,w]));
 if(ref.size!==9)throw Error("duplicate world in baseline");
 const groups=new Map();
 for(let i=1;i<lines.length;i++){
  const c=lines[i].split(",");if(c.length!==11)throw Error("invalid CSV row "+i);
  const [world,fn,nstr,design,kstr,tuple,massstr,hitstr,estimate,truth,squared]=c;
  const w=ref.get(world),n=Number(nstr),k=Number(hitstr),ind=Number(kstr);
  if(!w||w.function!==fn||w.evaluations!==n||!["IID","ANTITHETIC"].includes(design)||!Number.isSafeInteger(k)||k<0||k>n)throw Error("wrong row identity");
  const draws=design==="IID"?n:n/2;
  if(ind!==draws||tuple.split(";").length!==draws||!tuple.split(";").every(x=>/^[0-3]$/.test(x)))throw Error("wrong primitive source");
  if(!eq(P(massstr),F(1n,4n**BigInt(draws))))throw Error("wrong mass");
  const p=P(w.true_integral),est=F(BigInt(k),BigInt(n)),err=sub(est,p);
  if(!eq(P(truth),p)||!eq(P(estimate),est)||!eq(P(squared),mul(err,err)))throw Error("wrong source calculation");
  const key=world+"|"+design;
  if(!groups.has(key))groups.set(key,{w,n,design,p,seen:new Set(),covered:0,sumPluginNumerator:0n,total:0});
  const g=groups.get(key);
  if(g.seen.has(tuple))throw Error("duplicate primitive tuple");
  g.seen.add(tuple);g.total++;
  const N=BigInt(n),K=BigInt(k),a=p[0],b=p[1];
  if((b*K-a*N)**2n<=4n*N*a*(b-a))g.covered++;
  g.sumPluginNumerator+=K*(N-K);
 }
 if(groups.size!==18)throw Error("missing group");
 const results=[];
 for(const w of baseline.worlds){
  for(const design of ["IID","ANTITHETIC"]){
   const g=groups.get(w.world+"|"+design);if(!g)throw Error("missing row");
   const expected=4**(design==="IID"?g.n:g.n/2);
   if(g.total!==expected||g.total!==w.designs[design].source_atoms)throw Error("missing source atoms");
   const p=g.p,n=F(BigInt(g.n)),q=sub(F(1),p),cov=P(w.antithetic_pair_covariance);
   const formula=div(design==="IID"?mul(p,q):add(mul(p,q),cov),n);
   const actual=P(w.designs[design].exact_variance);
   if(!eq(actual,formula))throw Error("tampered variance reference");
   const plugin=F(g.sumPluginNumerator,BigInt(g.total)*BigInt(g.n)**3n);
   const coverage=F(g.covered,g.total);
   results.push({world:w.world,design,evaluations:g.n,source_atoms:g.total,covered_atoms:g.covered,
    exact_score_z2_coverage:fmt(coverage),exact_score_z2_miscoverage:fmt(sub(F(1),coverage)),
    expected_naive_IID_plugin_variance:fmt(plugin),actual_estimator_variance:fmt(actual),
    naive_plugin_over_actual_variance:actual[0]===0n?null:fmt(div(plugin,actual))});
  }
 }
 const i=results.find(x=>x.world==="SYMMETRIC_EXTREMES_N6"&&x.design==="IID");
 const a=results.find(x=>x.world==="SYMMETRIC_EXTREMES_N6"&&x.design==="ANTITHETIC");
 if(i.exact_score_z2_coverage!=="31/32"||a.exact_score_z2_coverage!=="3/4")throw Error("frozen counterexample failed");
 return {research_id:"R266_S62",protocol_freeze_commit:FREEZE,original_R266_source_sha256:EXPECTED_SOURCE_SHA,
  original_complete_source_types:5328,worlds:9,design_combinations:18,
  score_interval:"Wilson score inversion, z=2, evaluated as if n function calls IID",
  nominal_normal_reference:"about 95.45%, not exact finite coverage",
  evidence:"E1_EXHAUSTIVE_ARTIFICIAL_ONLY",new_real_human_E2:0,new_real_historical_E3:0,
  R073:"FROZEN",PESEN_v0_1:"FROZEN",results};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto"),path=require("path");
 const base=path.join(__dirname,"../R266");
 const csv=fs.readFileSync(path.join(base,"R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv"));
 if(crypto.createHash("sha256").update(csv).digest("hex")!==EXPECTED_SOURCE_SHA)throw Error("source SHA mismatch");
 const b=JSON.parse(fs.readFileSync(path.join(base,"R266_EXACT_FINITE_MC_RESULTS.json"),"utf8"));
 process.stdout.write(JSON.stringify(audit(csv.toString("utf8"),b),null,2)+"\n");
}
if(typeof module!=="undefined")module.exports={audit};
