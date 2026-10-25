"use strict";
// R163 exact Bernoulli-product distinguishability for two synthetic copying rules.
// Node usage: node r163_finite_choice_identifiability.js research/R163/R163_EXACT_RESULTS.json
function gcd(a,b){while(b){const t=a%b;a=b;b=t}return a}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}if(!b)throw Error("zero denom");const g=gcd(a<0n?-a:a,b);return [a/g,b/g]}
function add(x,y){return f(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
function mul(x,y){return f(x[0]*y[0],x[1]*y[1])}
function sub(x,y){return f(x[0]*y[1]-y[0]*x[1],x[1]*y[1])}
function abs(x){return [x[0]<0n?-x[0]:x[0],x[1]]}
function cmp(x,y){const z=x[0]*y[1]-y[0]*x[1];return z<0n?-1:z>0n?1:0}
function str(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1]}
function parse(s){const a=String(s).split("/");return f(BigInt(a[0]),BigInt(a[1]||1))}
function pow(x,n){return f(x[0]**BigInt(n),x[1]**BigInt(n))}
function binom(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-i+1)/BigInt(i);return v}
function error(p,q,n){
 let overlap=f(0n);
 for(let k=0;k<=n;k++){
  const a=mul(f(binom(n,k)),mul(pow(p,k),pow(sub(f(1n),p),n-k)));
  const b=mul(f(binom(n,k)),mul(pow(q,k),pow(sub(f(1n),q),n-k)));
  overlap=add(overlap,cmp(a,b)<=0?a:b);
 }
 return mul(overlap,f(1n,2n));
}
function direct(w){
 const a=w.demonstrator_actions,s=w.displayed_payoffs;
 if(w.copying_strategy==="best"){
  const max=Math.max(...s),indices=s.map((v,i)=>v===max?i:-1).filter(i=>i>=0);
  return f(BigInt(indices.reduce((sum,i)=>sum+a[i],0)),BigInt(indices.length));
 }
 const sum1=s.reduce((t,v,i)=>t+(a[i]===1?v:0),0),num1=a.reduce((x,y)=>x+y,0);
 const sum0=s.reduce((t,v,i)=>t+(a[i]===0?v:0),0),num0=3-num1;
 const d=sum1*num0-sum0*num1;
 return d>0?f(1n):d<0?f(0n):f(1n,2n);
}
function compute(input){
 if(input.research_id!=="R163"||input.world_count!==72||input.worlds.length!==72)throw Error("source identity");
 const profiles=["A_outlier","B_outlier","A_agreement","B_agreement","best_tie","mean_tie"];
 const transforms=["raw","reverse","flat"];
 const buckets=new Map(),ids=new Set();
 for(const w of input.worlds){
  if(ids.has(w.id))throw Error("duplicate ID");ids.add(w.id);
  if(!profiles.includes(w.profile_name)||!transforms.includes(w.transformation))throw Error("unexpected world");
  const p=direct(w);
  if(cmp(p,parse(w.probability_copy_A))!==0)throw Error("source probability mismatch "+w.id);
  const key=w.profile_name+"|"+w.transformation;
  if(!buckets.has(key))buckets.set(key,[]);
  buckets.get(key).push({strategy:w.copying_strategy,c:w.synthetic_correct_action,p});
 }
 if(ids.size!==72||buckets.size!==18)throw Error("incomplete 72-world design");
 const contexts=[];let identical=0,distinguishable=0,zeroAt1=0,zeroAt8=0,mutantDetected=0;
 for(const profile of profiles)for(const transform of transforms){
  const key=profile+"|"+transform,rows=buckets.get(key);
  if(!rows||rows.length!==4)throw Error("missing context");
  const get=(strategy,c)=>{const a=rows.filter(r=>r.strategy===strategy&&r.c===c);if(a.length!==1)throw Error("bad design");return a[0].p};
  const p=get("best",0),q=get("means",0);
  if(cmp(p,get("best",1))||cmp(q,get("means",1)))throw Error("truth leakage into copying");
  const errors=[1,2,4,8].map(n=>error(p,q,n));
  for(let i=0;i<errors.length;i++){
   if(cmp(errors[i],f(0n))<0||cmp(errors[i],f(1n,2n))>0||i>0&&cmp(errors[i],errors[i-1])>0)throw Error("error monotonicity/bounds");
  }
  const tv=abs(sub(p,q)),same=cmp(p,q)===0;
  if(same){identical++;if(errors.some(e=>cmp(e,f(1n,2n))!==0))throw Error("identical context should be nonidentifiable")}
  else {distinguishable++;if(cmp(errors[0],f(1n,2n))>=0)throw Error("mutant sentinel");mutantDetected++}
  if(cmp(errors[0],f(0n))===0)zeroAt1++;
  if(cmp(errors[3],f(0n))===0)zeroAt8++;
  contexts.push({profile,transform,p_best:str(p),p_means:str(q),tv_one_choice:str(tv),equal_prior_error:Object.fromEntries([1,2,4,8].map((n,i)=>[String(n),str(errors[i])]))});
 }
 return {research_id:"R163",evidence:"E1_SYNTHETIC_ONLY",input_blob_sha1:"1f1dba0e64d8540695544bcde50e3df5ebcbf5e6",
  verified_worlds:ids.size,contexts:contexts.length,identical_contexts:identical,distinguishable_contexts:distinguishable,
  zero_error_at_n1:zeroAt1,zero_error_at_n8:zeroAt8,neutralized_strategy_mutant_detected_contexts:mutantDetected,
  context_results:contexts,E2:0,E3:0,external_reproduction:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const input=process.argv[2]||path.join(__dirname,"..","R163","R163_EXACT_RESULTS.json");
 console.log(JSON.stringify(compute(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
}
if(typeof module!=="undefined")module.exports={compute};
