#!/usr/bin/env node
"use strict";
const fs=require("node:fs");
const path=require("node:path");
const score=function score(data){
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
  function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];}
  function P(s){let z=String(s).split("/");return F(z[0],z.length===2?z[1]:1);}
  function add(x,y){return F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
  function mul(x,y){return F(x[0]*y[0],x[1]*y[1]);}
  function div(x,y){return F(x[0]*y[1],x[1]*y[0]);}
  function gt(x,y){return x[0]*y[1]>y[0]*x[1];}
  function fmt(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1];}
  const zero=F(0),one=F(1),ps=["0","1/2","1"];
  if(data.schema!=="r315_ws_first_two_clockwise_edges_exact_e1_v1"||data.source_scope!=="FINITE_ARTIFICIAL_E1_ONLY"||data.source_atom_count!==210||data.full_path_count!==180)throw Error("source metadata mismatch");
  const out={schema:"r315_s111_three_p_classification_exact_v1",freeze_commit:"ec4fb603e3dccb1f35e8cf6b9d31f0c6e1ae5c40",source_blob:"5abbcdbf01e8b31e54671e83d033ab0f1985bd78",grade:"E1_SYNTHETIC_NONBLIND",observation_order:["full_labeled_graph","joint_C_L_components","C","L","components"],worlds:[],classifications:[]};
  for(let n of [8,10]){
    const worlds=ps.map(p=>data.parameter_worlds.find(w=>w.N===n&&w.p===p));
    if(worlds.some(w=>!w))throw Error("missing N/p world");
    for(let w of worlds){
      if(w.complete_paths.length!==(n===8?19:41))throw Error("path count mismatch");
      let mass=zero,ec=zero,connected=zero,el=zero,disconnected=zero,positive=0;
      for(let r of w.complete_paths){
        let prob=P(r.probability);if(prob[0]<0n)throw Error("negative mass");
        mass=add(mass,prob);if(prob[0]===0n)continue;positive++;
        ec=add(ec,mul(prob,P(r.clustering)));
        if(r.components===1){connected=add(connected,prob);el=add(el,mul(prob,P(r.mean_shortest_path)));}else{disconnected=add(disconnected,prob);if(r.mean_shortest_path!==null)throw Error("disconnected L must be null");}
      }
      if(fmt(mass)!=="1")throw Error("probability mass mismatch");
      out.worlds.push({N:n,p:w.p,total_paths:w.complete_paths.length,positive_paths:positive,mass:"1",expected_C:fmt(ec),connected_probability:fmt(connected),disconnected_probability:fmt(disconnected),conditional_expected_L:connected[0]===0n?null:fmt(div(el,connected))});
    }
    for(let observation of out.observation_order){
      let bins=new Map();
      for(let [i,w] of worlds.entries()){
        for(let r of w.complete_paths){
          let q=P(r.probability);if(q[0]===0n)continue;
          let key=observation==="full_labeled_graph"?r.final_edges:observation==="joint_C_L_components"?[r.clustering,r.mean_shortest_path??"NULL",r.components].join("|"):observation==="C"?r.clustering:observation==="L"?(r.mean_shortest_path??"NULL"):String(r.components);
          if(!bins.has(key))bins.set(key,[zero,zero,zero]);
          let a=bins.get(key);a[i]=add(a[i],q);
        }
      }
      let top=zero,ties=0;
      for(let a of bins.values()){
        let m=a[0];for(let v of a.slice(1))if(gt(v,m))m=v;
        if(a.filter(v=>fmt(v)===fmt(m)).length>1)ties++;
        top=add(top,m);
      }
      out.classifications.push({N:n,observation,positive_bins:bins.size,bins_with_tied_max:ties,equal_prior_optimal_accuracy:fmt(div(top,F(3)))});
    }
  }
  const a=(n,k)=>P(out.classifications.find(x=>x.N===n&&x.observation===k).equal_prior_optimal_accuracy);
  for(let n of [8,10]){let full=a(n,"full_labeled_graph"),joint=a(n,"joint_C_L_components");if(gt(joint,full))throw Error("coarsening violation full");for(let k of ["C","L","components"])if(gt(a(n,k),joint))throw Error("coarsening violation joint");}
  return out;
};
const root=path.resolve(__dirname,"../..");
const source=path.join(root,"research/R315/R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json");
const persisted=path.join(__dirname,"R315_S111_THREE_P_CLASSIFICATION_EXACT.json");
const result=score(JSON.parse(fs.readFileSync(source,"utf8")));
if(process.argv.includes("--check")){
 const expected=JSON.parse(fs.readFileSync(persisted,"utf8"));
 if(JSON.stringify(expected)!==JSON.stringify(result))throw Error("persisted result differs");
 process.stdout.write("PASS R315 S111 exact 180 paths, 10 classification cells, six p worlds\n");
}else process.stdout.write(JSON.stringify(result,null,2)+"\n");
