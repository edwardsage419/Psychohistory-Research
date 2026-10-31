#!/usr/bin/env node
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const audit=function audit(archive,receipt){
  const zero=()=>[0n,1n],unit=()=>[1n,1n];
  function g(a,b){a=a<0n?-a:a;while(b){const c=a%b;a=b;b=c;}return a;}
  function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<=0n)throw Error("bad denominator");let z=g(n,d);return [n/z,d/z];}
  function read(s){if(s===null)throw Error("null fraction");const a=String(s).split("/");if(a.length>2)throw Error("bad fraction");return q(a[0],a[1]??1);}
  function plus(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
  function times(a,b){return q(a[0]*b[0],a[1]*b[1]);}
  function over(a,b){if(b[0]===0n)throw Error("zero divide");let n=a[0]*b[1],d=a[1]*b[0];return d<0n?q(-n,-d):q(n,d);}
  function eq(a,b){return a[0]*b[1]===b[0]*a[1];}
  function higher(a,b){return a[0]*b[1]>b[0]*a[1];}
  function print(a){return a[1]===1n?String(a[0]):a[0]+"/"+a[1];}
  function edge(a,b){if(a===b)throw Error("self edge");return Math.min(a,b)+"-"+Math.max(a,b);}
  function ring(n){let x=new Set();for(let i=0;i<n;i++)for(let d of [1,2])x.add(edge(i,(i+d)%n));return x;}
  function serialize(edges){return [...edges].sort((a,b)=>{let [i,j]=a.split("-").map(Number),[k,l]=b.split("-").map(Number);return i-k||j-l;}).join(";");}
  function neigh(edges,n){let a=Array.from({length:n},()=>new Set());for(let s of edges){let [u,v]=s.split("-").map(Number);if(u===v||u<0||v>=n)throw Error("invalid graph");a[u].add(v);a[v].add(u);}return a;}
  function opts(edges,n,active,old){if(!edges.has(edge(active,old)))throw Error("missing original edge");let a=neigh(edges,n)[active];return [-1,...Array.from({length:n},(_,i)=>i).filter(i=>i!==active&&!a.has(i))];}
  function update(edges,active,old,target){let next=new Set(edges);if(target!==-1){next.delete(edge(active,old));next.add(edge(active,target));}return next;}
  function metric(edges,n){
    let a=neigh(edges,n),c=zero();
    for(let v=0;v<n;v++){let ns=[...a[v]],t=0;for(let i=0;i<ns.length;i++)for(let j=i+1;j<ns.length;j++)if(edges.has(edge(ns[i],ns[j])))t++;if(ns.length>1)c=plus(c,q(2*t,ns.length*(ns.length-1)));}
    c=over(c,q(n));
    let all=0,components=0,visited=new Set();
    for(let start=0;start<n;start++){
      let dist=new Map([[start,0]]),queue=[start];for(let v of queue)for(let u of a[v])if(!dist.has(u)){dist.set(u,dist.get(v)+1);queue.push(u);}
      if(!visited.has(start)){components++;for(let v of dist.keys())visited.add(v);}
      if(dist.size===n)for(let j=start+1;j<n;j++)all+=dist.get(j);
    }
    return {C:print(c),L:components===1?print(q(all,n*(n-1)/2)):null,components};
  }
  if(archive.schema!=="r315_ws_first_two_clockwise_edges_exact_e1_v1"||archive.source_scope!=="FINITE_ARTIFICIAL_E1_ONLY"||archive.source_atom_count!==210||archive.full_path_count!==180||archive.parameter_worlds.length!==6)throw Error("original source identity");
  if(receipt.schema!=="r315_s111_three_p_classification_exact_v1"||receipt.grade!=="E1_SYNTHETIC_NONBLIND"||receipt.freeze_commit!=="ec4fb603e3dccb1f35e8cf6b9d31f0c6e1ae5c40"||receipt.source_blob!=="5abbcdbf01e8b31e54671e83d033ab0f1985bd78")throw Error("receipt provenance/grade");
  const maps=["full_labeled_graph","joint_C_L_components","C","L","components"];
  if(JSON.stringify(receipt.observation_order)!==JSON.stringify(maps)||receipt.classifications.length!==10||receipt.worlds.length!==6)throw Error("receipt coverage");
  let checked=0,metrics=0,conditional=0;
  for(let n of [8,10]){
    let base=ring(n),m0=metric(base,n);if(base.size!==2*n)throw Error("baseline edges");
    let distributions=Object.fromEntries(maps.map(k=>[k,new Map()]));
    for(let [i,p] of ["0","1/2","1"].entries()){
      let w=archive.parameter_worlds.find(x=>x.N===n&&x.p===p);
      if(!w||w.complete_paths.length!==(n===8?19:41))throw Error("missing/duplicated path");
      if(w.baseline_edges!==serialize(base)||w.baseline_clustering!==m0.C||w.baseline_mean_shortest_path!==m0.L||w.baseline_components!==1)throw Error("baseline metrics");
      let first=opts(base,n,0,1),seen=new Set(),mass=zero(),ec=zero(),conn=zero(),dis=zero(),el=zero(),positive=0;
      for(let row of w.complete_paths){
        let a=row.first_action==="keep"?-1:row.first_action==="rewire"?row.first_target:null;
        if(a===null||!first.includes(a)||row.first_target!==a)throw Error("first action invalid");
        let mid=update(base,0,1,a),second=opts(mid,n,1,2);
        let b=row.second_action==="keep"?-1:row.second_action==="rewire"?row.second_target:null;
        if(b===null||!second.includes(b)||row.second_target!==b)throw Error("second action invalid");
        let key=a+"|"+b;if(seen.has(key))throw Error("duplicate path");seen.add(key);
        let fin=update(mid,1,2,b);
        if(fin.size!==2*n||serialize(fin)!==row.final_edges)throw Error("final graph invalid");
        let prob=times(a===-1?plus(unit(),times(q(-1),read(p))):over(read(p),q(first.length-1)),b===-1?plus(unit(),times(q(-1),read(p))):over(read(p),q(second.length-1)));
        if(!eq(prob,read(row.probability)))throw Error("wrong path probability");
        let mm=metric(fin,n);metrics++;
        if(!eq(read(mm.C),read(row.clustering))||mm.L!==row.mean_shortest_path||mm.components!==row.components)throw Error("graph metric mismatch");
        mass=plus(mass,prob);checked++;
        if(prob[0]===0n)continue;
        positive++;ec=plus(ec,times(prob,read(mm.C)));
        if(mm.components===1){conn=plus(conn,prob);el=plus(el,times(prob,read(mm.L)));}else dis=plus(dis,prob);
        const obs={full_labeled_graph:serialize(fin),joint_C_L_components:[mm.C,mm.L??"NULL",mm.components].join("|"),C:mm.C,L:mm.L??"NULL",components:String(mm.components)};
        for(let k of maps){let table=distributions[k];if(!table.has(obs[k]))table.set(obs[k],[zero(),zero(),zero()]);let v=table.get(obs[k]);v[i]=plus(v[i],prob);}
      }
      if(seen.size!==w.complete_paths.length||!eq(mass,unit()))throw Error("coverage/mass");
      let rw=receipt.worlds.find(x=>x.N===n&&x.p===p);
      if(!rw||rw.total_paths!==w.complete_paths.length||rw.positive_paths!==positive||rw.mass!=="1"||!eq(read(rw.expected_C),ec)||!eq(read(rw.connected_probability),conn)||!eq(read(rw.disconnected_probability),dis)||rw.conditional_expected_L!==(conn[0]===0n?null:print(over(el,conn))))throw Error("world receipt mismatch");
    }
    for(let k of maps){
      let table=distributions[k],maxsum=zero(),ties=0;
      for(let arr of table.values()){let m=arr[0];for(let v of arr)if(higher(v,m))m=v;if(arr.filter(v=>eq(v,m)).length>1)ties++;maxsum=plus(maxsum,m);}
      let accuracy=over(maxsum,q(3));
      let rr=receipt.classifications.find(x=>x.N===n&&x.observation===k);
      if(!rr||rr.positive_bins!==table.size||rr.bins_with_tied_max!==ties||!eq(read(rr.equal_prior_optimal_accuracy),accuracy))throw Error("classification receipt mismatch "+n+" "+k);
    }
  }
  if(checked!==180||metrics!==180)throw Error("audit coverage");
  return {status:"PASS",source_paths:checked,independent_graph_metric_checks:metrics,classification_cells:10,world_receipts:6,method:"independent event enumeration + BFS + BigInt rational",grade:"E1_INTERNAL_NONBLIND"};
};
const root=path.resolve(__dirname,"../..");
const orig=path.join(root,"research/R315/R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json");
const summary=path.join(root,"research/validation/R315_S111_THREE_P_CLASSIFICATION_EXACT.json");
const bytes=fs.readFileSync(orig);
const blob=crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\\0")).update(bytes).digest("hex");
if(blob!=="5abbcdbf01e8b31e54671e83d033ab0f1985bd78")throw Error("original Git blob changed: "+blob);
const source=JSON.parse(bytes.toString("utf8")),receipt=JSON.parse(fs.readFileSync(summary,"utf8"));
const verified=audit(source,receipt);
if(process.argv.includes("--mutations")){
 const tests=[
  ["duplicate_path",d=>d.parameter_worlds[0].complete_paths.push({...d.parameter_worlds[0].complete_paths[0]})],
  ["missing_path",d=>d.parameter_worlds[0].complete_paths.pop()],
  ["wrong_probability",d=>d.parameter_worlds[1].complete_paths[0].probability="1/5"],
  ["wrong_clustering",d=>d.parameter_worlds[1].complete_paths[0].clustering="999"],
  ["wrong_distance",d=>d.parameter_worlds[4].complete_paths[0].mean_shortest_path="999"],
  ["wrong_component",d=>d.parameter_worlds[2].complete_paths[0].components=2],
  ["wrong_final_graph",d=>d.parameter_worlds[1].complete_paths[0].final_edges="0-1"],
  ["wrong_source_scope",d=>d.source_scope="E2_REAL_HUMAN"]
 ];
 for(const [name,fn] of tests){
  const mutated=structuredClone(source);fn(mutated);
  let rejected=false;try{audit(mutated,receipt)}catch(e){rejected=true}
  if(!rejected)throw Error("mutation escaped: "+name);
 }
 const corrupted=structuredClone(receipt);corrupted.classifications[0].equal_prior_optimal_accuracy="1";
 let rejected=false;try{audit(source,corrupted)}catch(e){rejected=true}
 if(!rejected)throw Error("mutation escaped: wrong_receipt_accuracy");
 verified.mutations_rejected=9;
}
process.stdout.write(JSON.stringify(verified,null,2)+"\n");
