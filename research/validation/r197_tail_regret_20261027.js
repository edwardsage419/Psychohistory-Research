// Exact R197 third-method E1 artificial risk. Node.js >=18.\nconst fs=require("fs"),path=require("path");\nfunction analyze(csv,baseline){
 const F=x=>{const [a,b="1"]=String(x).split("/");let n=BigInt(a),d=BigInt(b);if(d<0n){n=-n;d=-d}let p=n<0n?-n:n,q=d;while(q){const t=p%q;p=q;q=t}const g=p||1n;return [n/g,d/g]};
 const add=(x,y)=>F((x[0]*y[1]+y[0]*x[1])+"/"+(x[1]*y[1]));
 const sub=(x,y)=>F((x[0]*y[1]-y[0]*x[1])+"/"+(x[1]*y[1]));
 const mul=(x,y)=>F((x[0]*y[0])+"/"+(x[1]*y[1]));
 const div=(x,y)=>F((x[0]*y[1])+"/"+(x[1]*y[0]));
 const eq=(x,y)=>x[0]*y[1]===y[0]*x[1];
 const gt=(x,y)=>x[0]*y[1]>y[0]*x[1];
 const lt=(x,y)=>x[0]*y[1]<y[0]*x[1];
 const str=x=>x[1]===1n?""+x[0]:x[0]+"/"+x[1];
 const Z=F(0),O=F(1),Q=F("1/4");
 const S=["WHITE","AR1","RW","DRIFT","DIFF_AR1","DIFF_MA1"];
 function cells(line){let out=[],v="",inside=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(inside&&line[i+1]==='"'){v+='"';i++}else inside=!inside}else if(c===','&&!inside){out.push(v);v=""}else v+=c}out.push(v);return out}
 const ls=csv.trim().split(/\r?\n/),header=cells(ls.shift()),old=JSON.parse(baseline),worlds=new Map();
 let candidateChecks=0,selectedChecks=0;
 for(const line of ls){const row=cells(line);if(row.length!==header.length)throw Error("csv width");const r=Object.fromEntries(header.map((h,i)=>[h,row[i]]));
  const key=[r.source,r.training_time_steps_T,r.future_horizon_h].join("|");
  if(!worlds.has(key))worlds.set(key,{source:r.source,T:+r.training_time_steps_T,h:+r.future_horizon_h,n:0,mass:Z,q:Z,rw:Z,d:Z,tail25:Z,tail1:Z,worse:Z,better:Z,tie:Z,models:Object.fromEntries(S.map(s=>[s,{mass:Z,q:Z,d:Z,n:0}]))});
  const w=worlds.get(key),p=F(r.true_original_training_mass),mu=F(r.true_conditional_test_mean_oracle),v=F(r.true_conditional_test_variance_oracle);
  const f=F(r["candidate_"+r.selected_prequential_model+"_forecast"]),frw=F(r.candidate_RW_forecast);
  const q=mul(sub(mu,f),sub(mu,f)),qrw=mul(sub(mu,frw),sub(mu,frw)),d=sub(q,qrw);
  if(!eq(add(v,q),F(r.fitted_model_true_independent_future_MSE)))throw Error("selected mismatch "+key);
  if(!eq(add(v,qrw),F(r.candidate_RW_true_independent_future_MSE)))throw Error("RW mismatch "+key);selectedChecks+=2;
  for(const s of S){const ff=F(r["candidate_"+s+"_forecast"]),rr=add(v,mul(sub(mu,ff),sub(mu,ff)));if(!eq(rr,F(r["candidate_"+s+"_true_independent_future_MSE"])))throw Error("candidate mismatch "+key+" "+s);candidateChecks++}
  w.n++;w.mass=add(w.mass,p);w.q=add(w.q,mul(p,q));w.rw=add(w.rw,mul(p,qrw));w.d=add(w.d,mul(p,d));
  if(gt(q,Q))w.tail25=add(w.tail25,p);if(gt(q,O))w.tail1=add(w.tail1,p);
  if(gt(d,Z))w.worse=add(w.worse,p);else if(lt(d,Z))w.better=add(w.better,p);else w.tie=add(w.tie,p);
  const m=w.models[r.selected_prequential_model];m.mass=add(m.mass,p);m.q=add(m.q,mul(p,q));m.d=add(m.d,mul(p,d));m.n++;
 }
 if(ls.length!==3888||worlds.size!==24)throw Error("row count");
 let archiveChecks=0;const rows=[];
 for(const w of worlds.values()){
  if(w.n!==3**w.T||!eq(w.mass,O)||!eq(add(add(w.worse,w.better),w.tie),O))throw Error("mass");
  const oldRow=old.all_24_original_worlds.find(x=>x.original_source===w.source&&x.training_T===w.T&&x.future_test_horizon_h===w.h);
  if(!oldRow)throw Error("archive row missing");
  const oracle=F(oldRow.oracle_true_source_expected_independent_future_MSE);
  for(const [a,b] of [[w.q,F(oldRow.selected_model_expected_excess_MSE_over_oracle)],[add(w.q,oracle),F(oldRow.selected_model_expected_independent_future_MSE)],[add(w.rw,oracle),F(oldRow.always_RW_expected_independent_future_MSE)]]){if(!eq(a,b))throw Error("archive aggregate");archiveChecks++}
  const m={};for(const s of S){const x=w.models[s];if(!eq(x.mass,F(oldRow.candidate_prequential_selection_probability[s])))throw Error("selection archive");archiveChecks++;m[s]={probability:str(x.mass),paths:x.n,conditional_excess:x.mass[0]===0n?null:str(div(x.q,x.mass)),conditional_vs_RW:x.mass[0]===0n?null:str(div(x.d,x.mass))}}
  rows.push({source:w.source,T:w.T,h:w.h,paths:w.n,probability_mass:str(w.mass),selected_excess:str(w.q),RW_excess:str(w.rw),selected_minus_RW:str(w.d),P_excess_gt_quarter:str(w.tail25),P_excess_gt_one:str(w.tail1),P_worse_than_RW:str(w.worse),P_better_than_RW:str(w.better),P_equal_RW:str(w.tie),by_selected_model:m});
 }
 rows.sort((a,b)=>S.indexOf(a.source)-S.indexOf(b.source)||a.T-b.T||a.h-b.h);
 const find=(s,t,h)=>rows.find(x=>x.source===s&&x.T===t&&x.h===h);
 if(!gt(F(find("RW",5,1).selected_minus_RW),Z)||!gt(F(find("RW",5,2).selected_minus_RW),Z)||!lt(F(find("DRIFT",5,2).selected_minus_RW),Z))throw Error("prelocked contrasts");
 for(const s of S)for(const T of [4,5]){const a=find(s,T,1),b=find(s,T,2);for(const m of S)if(a.by_selected_model[m].probability!==b.by_selected_model[m].probability)throw Error("future leakage in model selection")}
 return {schema:"R197_selection_tail_regret_v1",source_csv_blob:"ed8b150677dd5213e4798154162135245e1aa18a",source_original_blob:"53b47a5096243812551d3b38fe07bb17bddfe5fa",counts:{rows:ls.length,worlds:rows.length,candidateChecks,selectedChecks,archiveChecks},worlds:rows,evidence:"E1_INTERNAL_ARTIFICIAL",new_E2:0,new_E3:0,external_replication:0};
}\nif(require.main===module){const root=process.argv[2]||path.resolve(__dirname,"../..");process.stdout.write(JSON.stringify(analyze(fs.readFileSync(path.join(root,"research/R197/R197_ALL_3888_INDEPENDENT_HELDOUT_RISK_PROFILES.csv"),"utf8"),fs.readFileSync(path.join(root,"research/R197/R197_EXACT_RESULTS.json"),"utf8")),null,2)+"\\n")}\nmodule.exports={analyze};\n