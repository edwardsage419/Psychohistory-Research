#!/usr/bin/env node
// Independent Markov transition enumeration and cross entropy/KL audit for R209.
// Node.js >=18; no dependencies. Run from repository root or any directory.
const fs=require("fs"),path=require("path");
const original=JSON.parse(fs.readFileSync(path.resolve(__dirname,"../R209/R209_EXACT_RESULTS.json"),"utf8"));
const main=JSON.parse(fs.readFileSync(path.resolve(__dirname,"../validation/R209_GRAPH_SEED_TRANSPORT_432_WORLD_RECEIPT_2026-10-27.json"),"utf8"));
function audit(original,main){
 const graphs={STAR:[[0,1],[0,2],[0,3]],PATH:[[0,1],[1,2],[2,3]],CYCLE:[[0,1],[1,2],[2,3],[0,3]]},models=["BASE","SIMPLE","COMPLEX"];
 function distribution(graph,seed,model){
  const adj=[[],[],[],[]];for(let [a,b] of graphs[graph]){adj[a].push(b);adj[b].push(a);}
  let init=[3,3,3,3];init[seed]=0;let states=[{mask:1<<seed,t:init,p:1}];
  for(let r=1;r<=2;r++){
   let next=[];
   for(let s of states){
    let remain=[0,1,2,3].filter(i=>!(s.mask&(1<<i)));
    for(let choices=0;choices<(1<<remain.length);choices++){
     let t=s.t.slice(),mask=s.mask,p=s.p;
     remain.forEach((i,k)=>{
      let exposure=adj[i].filter(j=>s.mask&(1<<j)).length;
      let hazard=((model==="SIMPLE"&&exposure>=1)||(model==="COMPLEX"&&exposure>=2))?0.75:0.25;
      if(choices&(1<<k)){p*=hazard;t[i]=r;mask|=1<<i;}else p*=1-hazard;
     });
     next.push({mask,t,p});
    }
   }
   states=next;
  }
  let out=new Map();for(let s of states){let key=s.t.join(",");if(out.has(key))throw Error("duplicate Markov path");out.set(key,s.p);}
  let sum=[...out.values()].reduce((a,b)=>a+b,0);
  if(out.size!==27||Math.abs(sum-1)>1e-13||[...out.values()].some(x=>x<=0))throw Error("Markov probability");
  return out;
 }
 const dists={};for(let g of Object.keys(graphs))for(let seed=0;seed<4;seed++){let x={};for(let m of models)x[m]=distribution(g,seed,m);dists[g+seed]=x;}
 const event=m=>[...m].reduce((s,[key,p])=>s+(key.split(",").filter(x=>x==="1"||x==="2").length>=2?p:0),0);
 const cross=(p,q)=>[...p].reduce((s,[k,v])=>s-v*Math.log(q.get(k)),0);
 const parse=s=>{let v=String(s).split("/");return Number(v[0])/Number(v[1]||1);};
 const brier=(p,q)=>p*(1-p)+(q-p)**2;
 let selected={},checks={independent_training_model_weights:0,transfer_logloss_fields:0,transfer_Brier_fields:0,transfer_event_probability:0,KL_decomposition:0,Brier_variance_decomposition:0,oracle_nonnegative_regret:0};
 for(let w of original.worlds){
  let d=dists[w.graph+w.seed],weights={BASE:0,SIMPLE:0,COMPLEX:0};
  for(let [key,p] of d[w.true_model]){
   let chosen=models[0],best=-1;
   for(let m of models){let v=d[m].get(key);if(v>best){best=v;chosen=m;}}
   weights[chosen]+=p;
  }
  for(let m of models){if(Math.abs(weights[m]-parse(w.selected_model_probabilities_exact[m]))>1e-14)throw Error("training model probability mismatch");checks.independent_training_model_weights++;}
  selected[w.graph+"|"+w.seed+"|"+w.true_model]=weights;
 }
 let negatives={wrong_graph_logloss_changed:0,wrong_graph_Brier_changed:0,wrong_seed_zero_support:0,oracle_leakage_strict_improvement:0};
 let maxDiff=0,rows=[];
 for(let w of main.worlds){
  let weights=selected[w.train_graph+"|"+w.train_seed+"|"+w.true_model],d=dists[w.test_graph+w.test_seed],truth=d[w.true_model],p=event(truth);
  let L={},B={},q={};
  for(let m of models){L[m]=cross(truth,d[m]);q[m]=event(d[m]);B[m]=brier(p,q[m]);}
  let sl=models.reduce((s,m)=>s+weights[m]*L[m],0),sb=models.reduce((s,m)=>s+weights[m]*B[m],0);
  let entropy=L[w.true_model],oracleB=brier(p,p),kl=models.reduce((s,m)=>s+weights[m]*[...truth].reduce((z,[k,v])=>z+v*Math.log(v/d[m].get(k)),0),0);
  if(Math.abs((sl-entropy)-kl)>1e-12)throw Error("KL identity");checks.KL_decomposition++;
  if(Math.abs((sb-oracleB)-models.reduce((s,m)=>s+weights[m]*(q[m]-p)**2,0))>1e-12)throw Error("variance identity");checks.Brier_variance_decomposition++;
  if(sl<entropy-1e-12||sb<oracleB-1e-12)throw Error("oracle bound");checks.oracle_nonnegative_regret++;
  let logs=[["selected_future_logloss",sl],["fixed_BASE_future_logloss",L.BASE],["oracle_future_logloss",entropy],["excess_logloss_vs_BASE",sl-L.BASE],["excess_logloss_vs_oracle",sl-entropy]];
  let bs=[["selected_future_Brier_exact",sb],["fixed_BASE_future_Brier_exact",B.BASE],["oracle_future_Brier_exact",oracleB],["excess_Brier_vs_BASE_exact",sb-B.BASE],["excess_Brier_vs_oracle_exact",sb-oracleB]];
  for(let [k,v] of logs){let diff=Math.abs(w[k]-v);maxDiff=Math.max(maxDiff,diff);if(diff>1.1e-10)throw Error("logscore mismatch "+k+" "+diff);checks.transfer_logloss_fields++;}
  for(let [k,v] of bs){let diff=Math.abs(parse(w[k])-v);maxDiff=Math.max(maxDiff,diff);if(diff>1e-12)throw Error("Brier mismatch "+k+" "+diff);checks.transfer_Brier_fields++;}
  if(Math.abs(parse(w.true_test_event_probability_exact)-p)>1e-12)throw Error("event probability");checks.transfer_event_probability++;
  if(w.test_graph!==w.train_graph){
    let wrong=dists[w.train_graph+w.test_seed],wl=models.reduce((s,m)=>s+weights[m]*cross(truth,wrong[m]),0),wb=models.reduce((s,m)=>s+weights[m]*brier(p,event(wrong[m])),0);
    if(Math.abs(wl-sl)>1e-9)negatives.wrong_graph_logloss_changed++;
    if(Math.abs(wb-sb)>1e-9)negatives.wrong_graph_Brier_changed++;
  }
  if(w.test_seed!==w.train_seed){
    let wrong=dists[w.test_graph+w.train_seed];let support=[...truth.keys()].some(k=>!wrong.BASE.has(k));
    if(support)negatives.wrong_seed_zero_support++;
  }
  if(sl>entropy+1e-10)negatives.oracle_leakage_strict_improvement++;
  rows.push({train_graph:w.train_graph,train_seed:w.train_seed,true_model:w.true_model,test_graph:w.test_graph,test_seed:w.test_seed,logloss_diff:+(sl-w.selected_future_logloss).toExponential(4),Brier_diff:+(sb-parse(w.selected_future_Brier_exact)).toExponential(4)});
 }
 if(main.worlds.length!==432||checks.independent_training_model_weights!==108||checks.transfer_logloss_fields!==2160||checks.transfer_Brier_fields!==2160||checks.transfer_event_probability!==432||negatives.wrong_seed_zero_support!==324||negatives.wrong_graph_logloss_changed===0||negatives.oracle_leakage_strict_improvement===0)throw Error("audit check count/negative");
 return {audit:"B_R209_INDEPENDENT_MARKOV_PATH_ENUMERATION",evidence:"E1_INTERNAL_ALGORITHMIC_ONLY",main_receipt_blob:"ce0d7c7769dfddda344d8c197312f78b3037b15b",original_blob:"427244c57607a599867d129be238dc33f1afc008",checks,negatives,max_abs_difference:maxDiff,worlds:432,rows};
}
process.stdout.write(JSON.stringify(audit(original,main),null,2)+"\n");
