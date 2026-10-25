"use strict";
// Exact E1 kernel sufficiency replay; node thisfile.js R168_EXACT_RESULTS.json
const fs=require("fs");
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){[a,b]=[b,a%b]}return a};
const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]};
const P=x=>{const z=String(x).split("/");return Q(z[0],z[1]||1)};
const S=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
const A=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const M=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
const D=(x,y)=>A(x,Q(-y[0],y[1]));
const E=(x,n)=>Q(x[0]**BigInt(n),x[1]**BigInt(n));
const Z=Q(0),O=Q(1),ID=x=>[x.N,x.f,x.u,x.mode||x.access_mode].join("|");
function main(doc){
 if(doc.kernels.length!==32||doc.worlds.length!==64)throw Error("frozen dimensions");
 const byAB=new Map(),byMatrix=new Map(),kernel=new Map(),paths=new Set();let cell=0,worldCell=0;
 for(const k of doc.kernels){
  const n=k.mode==="full_pool"?k.N:1, a=E(D(O,P(k.u)),n),b=E(D(O,P(k.f)),n);
  const rows=[[a,D(O,a),Z],[M(a,b),M(a,D(O,b)),D(O,a)],[Z,b,D(O,b)]];
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){if(S(rows[i][j])!==S(P(k.kernel[i][j])))throw Error("kernel "+ID(k));cell++}
  const matrix=rows.map(r=>r.map(S).join(",")).join(";"),ab=S(a)+"|"+S(b);
  for(const [map,key] of [[byAB,ab],[byMatrix,matrix]]){if(!map.has(key))map.set(key,[]);map.get(key).push(ID(k))}
  kernel.set(ID(k),rows);
 }
 const classes=m=>[...m.values()].map(x=>x.slice().sort()).sort((a,b)=>b.length-a.length||a[0].localeCompare(b[0]));
 if(JSON.stringify(classes(byAB))!==JSON.stringify(classes(byMatrix)))throw Error("sufficiency failed");
 for(const w of doc.worlds){
  const k=kernel.get(ID(w));if(!k)throw Error("world key");
  let v=[0,1,2].map(i=>Q(i===w.initial_frontier?1:0)),sig=[];
  for(let t=0;t<w.points.length;t++){
   const now=v.map(S);sig.push(now.join(","));
   for(let j=0;j<3;j++){if(now[j]!==S(P(w.points[t].frontier_0_1_2_probabilities[j])))throw Error("path "+w.id+" "+t);worldCell++}
   v=[0,1,2].map(j=>[0,1,2].reduce((s,i)=>A(s,M(v[i],k[i][j])),Z));
  }
  paths.add(sig.join(";"));
 }
 const get=(n,f,u,mode)=>kernel.get([n,f,u,mode].join("|")).map(r=>r.map(S).join(",")).join(";");
 if(get(2,"1/2","0","full_pool")!==get(2,"3/4","0","single_channel"))throw Error("negative counterfactual");
 if(get(2,"1/2","1/8","full_pool")===get(2,"1/2","1/8","single_channel"))throw Error("positive counterfactual");
 const c=classes(byAB);
 return {id:"R168_EFFECTIVE_KERNEL_THIRD_METHOD",evidence:"E1_SYNTHETIC_ONLY",original_kernel_count:32,original_world_count:64,kernel_cells_verified:cell,path_cells_verified:worldCell,distinct_kernels:byMatrix.size,distinct_effective_pairs:byAB.size,ambiguous_rows:c.filter(x=>x.length>1).reduce((s,x)=>s+x.length,0),singletons:c.filter(x=>x.length===1).length,class_sizes:c.map(x=>x.length),classes:c,distinct_five_time_paths:paths.size,counterfactuals:"PASS",new_E2:0,new_E3:0,external_replications:0};
}
if(require.main===module){console.log(JSON.stringify(main(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}
module.exports={main};