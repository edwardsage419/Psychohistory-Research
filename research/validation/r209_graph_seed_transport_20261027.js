#!/usr/bin/env node
// R209 synthetic graph/seed transfer. Node 18+ standard library only.
// node research/validation/r209_graph_seed_transport_20261027.js > /tmp/r209.json
const fs=require("fs"),path=require("path");
const original=JSON.parse(fs.readFileSync(path.resolve(__dirname,"../R209/R209_EXACT_RESULTS.json"),"utf8"));
function compute(original){
const graphs={STAR:[[0,1],[0,2],[0,3]],PATH:[[0,1],[1,2],[2,3]],CYCLE:[[0,1],[1,2],[2,3],[0,3]]},models=["BASE","SIMPLE","COMPLEX"],D=4096;
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;};
const rat=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}let d=gcd(a,b);return[a/d,b/d];};
const add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1]),mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
const parse=s=>{let a=String(s).split("/");return rat(a[0],a[1]||1);},str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1],num=a=>Number(a[0])/Number(a[1]);
function distribution(graph,seed,model){
let adj=[[],[],[],[]];for(let [u,v] of graphs[graph]){adj[u].push(v);adj[v].push(u);}
let others=[0,1,2,3].filter(x=>x!==seed),out=[];
for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)for(let c=1;c<=3;c++){
let t=[0,0,0,0];[a,b,c].forEach((x,j)=>t[others[j]]=x);
let n=1,attempts=0;for(let round=1;round<=2;round++)for(let i=0;i<4;i++){
if(i===seed||t[i]<round)continue;
let k=adj[i].filter(j=>t[j]<round).length;
let high=(model==="SIMPLE"&&k>=1)||(model==="COMPLEX"&&k>=2);
let h=high?3:1;n*=t[i]===round?h:4-h;attempts++;
}
out.push({n:n*4**(6-attempts),y:Number(t.filter(v=>v===1||v===2).length>=2)});
}
if(out.length!==27||out.some(x=>x.n<=0)||out.reduce((s,x)=>s+x.n,0)!==D)throw Error("probability normalization");
return out;
}
const cache={};for(let g of Object.keys(graphs))for(let seed=0;seed<4;seed++){let x={};for(let m of models)x[m]=distribution(g,seed,m);cache[g+seed]=x;}
if(JSON.stringify(cache.STAR0.BASE)!==JSON.stringify(cache.STAR0.COMPLEX))throw Error("equivalence");
const event=p=>p.reduce((s,x)=>s+x.y*x.n,0);
const brier=(p,q)=>rat(BigInt(p)*BigInt(D-q)**2n+BigInt(D-p)*BigInt(q)**2n,BigInt(D)**3n);
const logloss=(p,q)=>p.reduce((s,x,i)=>s+x.n/D*(-Math.log(q[i].n/D)),0);
const worlds=[],checks={same_design_brier_exact:0,same_design_logscore:0,oracle_brier:0,oracle_logloss:0,training_weights:0};
if(original.worlds.length!==36)throw Error("original world count");
for(let train of original.worlds){
let w=models.map(m=>parse(train.selected_model_probabilities_exact[m]));if(str(w.reduce(add,rat(0)))!=="1")throw Error("train weights");checks.training_weights++;
for(let tg of Object.keys(graphs))for(let ts=0;ts<4;ts++){
let d=cache[tg+ts],p=d[train.true_model],P=event(p),L=models.map(m=>logloss(p,d[m])),B=models.map(m=>brier(P,event(d[m])));
let sl=w.reduce((s,x,i)=>s+num(x)*L[i],0),sb=w.reduce((s,x,i)=>add(s,mul(x,B[i])),rat(0)),ob=brier(P,P),ol=L[models.indexOf(train.true_model)];
if(num(sub(sb,ob)) < -1e-12||sl<ol-1e-11)throw Error("oracle bound");checks.oracle_brier++;checks.oracle_logloss++;
if(tg===train.graph&&ts===train.seed){
if(str(sb)!==str(parse(train.full_independent_future_binary_Brier_exact)))throw Error("original Brier mismatch");
if(Math.abs(sl-train.full_independent_future_trajectory_logscore)>1e-10)throw Error("original logscore mismatch");
checks.same_design_brier_exact++;checks.same_design_logscore++;
}
worlds.push({train_graph:train.graph,train_seed:train.seed,true_model:train.true_model,test_graph:tg,test_seed:ts,
category:(train.graph===tg?"same_graph":"changed_graph")+"_"+(train.seed===ts?"same_seed":"changed_seed"),
training_selected_probabilities:train.selected_model_probabilities_exact,
true_test_event_probability_exact:str(rat(P,D)),
selected_future_logloss:+sl.toFixed(12),fixed_BASE_future_logloss:+L[0].toFixed(12),oracle_future_logloss:+ol.toFixed(12),
selected_future_Brier_exact:str(sb),fixed_BASE_future_Brier_exact:str(B[0]),oracle_future_Brier_exact:str(ob),
excess_logloss_vs_BASE:+(sl-L[0]).toFixed(12),excess_logloss_vs_oracle:+(sl-ol).toFixed(12),
excess_Brier_vs_BASE_exact:str(sub(sb,B[0])),excess_Brier_vs_oracle_exact:str(sub(sb,ob))});
}}
if(worlds.length!==432||checks.same_design_brier_exact!==36)throw Error("world count");
let categories={};for(let x of worlds){let c=categories[x.category]??={n:0,log_better:0,log_worse:0,brier_better:0,brier_worse:0};c.n++;if(x.excess_logloss_vs_BASE < -1e-10)c.log_better++;if(x.excess_logloss_vs_BASE>1e-10)c.log_worse++;let v=num(parse(x.excess_Brier_vs_BASE_exact));if(v<0)c.brier_better++;if(v>0)c.brier_worse++;}
let ordered=[...worlds].sort((a,b)=>a.excess_logloss_vs_BASE-b.excess_logloss_vs_BASE);
return {research_id:"R209",method:"THIRD_METHOD_GRAPH_SEED_TRANSPORT",evidence:"E1_SYNTHETIC_ONLY",frozen_protocol_commit:"287dffd0b92bfc95e2d34c181a833d021878b663",original_results_blob:"427244c57607a599867d129be238dc33f1afc008",training_worlds:36,target_designs:12,transfer_worlds:432,independent_future_paths_per_world:27,checks,categories,best_vs_BASE:ordered[0],worst_vs_BASE:ordered[ordered.length-1],worlds};
}
process.stdout.write(JSON.stringify(compute(original),null,2)+"\n");
