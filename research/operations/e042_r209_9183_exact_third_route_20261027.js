#!/usr/bin/env node
// E042 read-only R209 third route, Node 18+ standard library, no network.
'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const R=JSON.parse(fs.readFileSync(path.join(root,'research/validation/R209_GRAPH_SEED_TRANSPORT_432_WORLD_RECEIPT_2026-10-27.json'),'utf8'));
const O=JSON.parse(fs.readFileSync(path.join(root,'research/R209/R209_EXACT_RESULTS.json'),'utf8'));
function audit(R,O){
 const edges={STAR:[[0,1],[0,2],[0,3]],PATH:[[0,1],[1,2],[2,3]],CYCLE:[[0,1],[1,2],[2,3],[0,3]]},models=["BASE","SIMPLE","COMPLEX"];
 const gcd=(a,b)=>{while(b){let t=a%b;a=b;b=t;}return a<0n?-a:a;};
 const rat=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}if(!d)throw Error("zero denom");let g=gcd(n<0n?-n:n,d);return[n/g,d/g];};
 const parse=s=>{let z=String(s).split("/");return rat(z[0],z[1]||"1");};
 const add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1]),mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],toNum=a=>Number(a[0])/Number(a[1]);
 const zero=rat(0),one=rat(1);
 const cache={};let assertions=0,failures=[],maxLogError=0;
 function check(ok,tag){assertions++;if(!ok&&failures.length<20)failures.push(tag);}
 function distribution(g,seed,model){
  const k=[g,seed,model].join(":");if(cache[k])return cache[k];
  const others=[0,1,2,3].filter(x=>x!==seed), e=edges[g];
  let dist=[],sum=zero,q=zero;
  for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)for(let c=1;c<=3;c++){
   let t=[3,3,3,3];t[seed]=0;[a,b,c].forEach((x,i)=>t[others[i]]=x);
   let n=1n,d=1n;
   for(let round=1;round<=2;round++)for(let i of others){
    if(t[i]<round)continue;
    let exposure=e.reduce((v,[u,w])=>v+((u===i&&t[w]<round)||(w===i&&t[u]<round)?1:0),0);
    let high=model==="SIMPLE"?exposure>=1:model==="COMPLEX"?exposure>=2:false;
    let h=high?3n:1n, adopt=t[i]===round;
    n*=adopt?h:4n-h;d*=4n;
   }
   let p=rat(n,d);dist.push(p);sum=add(sum,p);
   if(others.filter(i=>t[i]<=2).length>=2)q=add(q,p);
  }
  check(eq(sum,one),"path sum "+k);check(dist.length===27,"path length "+k);
  return cache[k]={dist,q};
 }
 const orig=new Map(O.worlds.map(w=>[[w.graph,w.seed,w.true_model].join(":"),w]));
 const seen=new Set(),categories={},weightsSeen=new Map(),modelEffects={};
 for(const w of R.worlds){
  let tr=[w.train_graph,w.train_seed,w.true_model].join(":"),tk=[w.test_graph,w.test_seed].join(":");
  check(!seen.has(tr+":"+tk),"duplicate "+tr+":"+tk);seen.add(tr+":"+tk);
  let expected=w.train_graph===w.test_graph?(w.train_seed===w.test_seed?"same_graph_same_seed":"same_graph_changed_seed"):(w.train_seed===w.test_seed?"changed_graph_same_seed":"changed_graph_changed_seed");
  check(w.category===expected,"category "+tr+":"+tk);
  const original=orig.get(tr);check(!!original,"original "+tr);
  let weights=Object.fromEntries(models.map(m=>[m,parse(w.training_selected_probabilities[m])]));
  for(const m of models)check(eq(weights[m],parse(original.selected_model_probabilities_exact[m])),"weight original "+tr+":"+m);
  check(eq(models.reduce((a,m)=>add(a,weights[m]),zero),one),"weights sum "+tr);
  let previous=weightsSeen.get(tr),sig=models.map(m=>w.training_selected_probabilities[m]).join("|");
  if(previous)check(previous===sig,"training weights leak "+tr);else weightsSeen.set(tr,sig);
  let truth=distribution(w.test_graph,w.test_seed,w.true_model),base=distribution(w.test_graph,w.test_seed,"BASE");
  check(eq(truth.q,parse(w.true_test_event_probability_exact)),"q "+tr+":"+tk);
  let oracle=mul(truth.q,sub(one,truth.q));
  let baseB=add(oracle,mul(sub(base.q,truth.q),sub(base.q,truth.q)));
  let selected=oracle;
  for(const m of models){let q=distribution(w.test_graph,w.test_seed,m).q;let e=sub(q,truth.q);selected=add(selected,mul(weights[m],mul(e,e)));}
  check(eq(oracle,parse(w.oracle_future_Brier_exact)),"oracle B "+tr+":"+tk);
  check(eq(baseB,parse(w.fixed_BASE_future_Brier_exact)),"base B "+tr+":"+tk);
  check(eq(selected,parse(w.selected_future_Brier_exact)),"selected B "+tr+":"+tk);
  check(eq(sub(selected,baseB),parse(w.excess_Brier_vs_BASE_exact)),"excess base B "+tr+":"+tk);
  check(eq(sub(selected,oracle),parse(w.excess_Brier_vs_oracle_exact)),"excess oracle B "+tr+":"+tk);
  function crossEntropy(model){let d=distribution(w.test_graph,w.test_seed,model).dist;let total=0;for(let i=0;i<27;i++)total-=toNum(truth.dist[i])*Math.log(toNum(d[i]));return total;}
  let trueL=crossEntropy(w.true_model),baseL=crossEntropy("BASE"),selL=models.reduce((v,m)=>v+toNum(weights[m])*crossEntropy(m),0);
  for(const [key,v] of [["oracle_future_logloss",trueL],["fixed_BASE_future_logloss",baseL],["selected_future_logloss",selL],["excess_logloss_vs_BASE",selL-baseL],["excess_logloss_vs_oracle",selL-trueL]]){
   let delta=Math.abs(w[key]-v);maxLogError=Math.max(maxLogError,delta);check(delta<=1e-10,"logloss "+key+" "+tr+":"+tk+" "+delta);
  }
  check(toNum(sub(selected,oracle))>=-1e-13,"Brier oracle lower "+tr+":"+tk);
  check(selL>=trueL-1e-10,"log oracle lower "+tr+":"+tk);
  if(w.train_graph===w.test_graph&&w.train_seed===w.test_seed){
   check(eq(parse(original.full_independent_future_binary_Brier_exact),selected),"orig B "+tr);
   check(Math.abs(original.full_independent_future_trajectory_logscore-selL)<1e-10,"orig L "+tr);
  }
  const c=categories[w.category]??={n:0,logBetter:0,logWorse:0,brierBetter:0,brierWorse:0};c.n++;
  if(selL<baseL-1e-10)c.logBetter++;if(selL>baseL+1e-10)c.logWorse++;
  let bs=sub(selected,baseB);if(bs[0]<0n)c.brierBetter++;if(bs[0]>0n)c.brierWorse++;
  const z=modelEffects[w.true_model]??={n:0,logBetter:0,logWorse:0};z.n++;if(selL<baseL-1e-10)z.logBetter++;if(selL>baseL+1e-10)z.logWorse++;
 }
 check(seen.size===432,"world count");check(weightsSeen.size===36,"train count");
 check(Object.keys(cache).length===36,"distributions count");
 return {assertions,failures,maxLogError,categories,modelEffects,distinctTrain:weightsSeen.size,distinctDistributions:Object.keys(cache).length};
}
const result=audit(R,O);
console.log(JSON.stringify(result,null,2));
if(result.failures.length||result.assertions!==9183)process.exitCode=1;
