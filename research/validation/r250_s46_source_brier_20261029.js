"use strict";
// R250 S46 exact source-first Brier risk. Node.js >=18; no dependencies.
// Usage: node research/validation/r250_s46_source_brier_20261029.js [original_csv]
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a||1n}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}if(!b)throw Error("denominator zero");let g=gcd(a<0n?-a:a,b);return [a/g,b/g]}
function plus(x,y){return f(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
function minus(x,y){return f(x[0]*y[1]-y[0]*x[1],x[1]*y[1])}
function repr(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1]}
function parse(s){let a=s.split("/");return f(a[0],a[1]||1)}
function cluster(e){let seen=new Set([0]),edges=[[0,1],[0,2],[1,2]],old=0;while(old!==seen.size){old=seen.size;edges.forEach(([a,b],i)=>{if(e[i]&&(seen.has(a)||seen.has(b))){seen.add(a);seen.add(b)}})}return seen.size}
function risk(rows,fields){let groups=new Map();for(let r of rows){let k=fields.map(x=>r[x]).join(":");let v=groups.get(k)||[0,0];v[0]++;v[1]+=Number(r.observed_root_component_size==="3");groups.set(k,v)}let sum=f(0);for(let [n,k] of groups.values())sum=plus(sum,f(k*(n-k),64*n));return [repr(sum),groups.size]}
function run(csv){
 let lines=csv.trim().split(/\r?\n/),keys=lines.shift().split(",");
 if(lines.length!==576)throw Error("source count");
 let rows=lines.map(line=>{let v=line.split(",");if(v.length!==keys.length)throw Error("columns");return Object.fromEntries(keys.map((k,i)=>[k,v[i]]))});
 let names=["CHAIN_P_QUARTER","CHAIN_P_HALF","CHAIN_P_THREE_QUARTER","TRIANGLE_P_ZERO","TRIANGLE_P_QUARTER","TRIANGLE_P_HALF","TRIANGLE_P_THREE_QUARTER","TRIANGLE_P_ONE","TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS"];
 let worlds=[],checks=0;
 for(let name of names){
  let rr=rows.filter(x=>x.world===name);if(rr.length!==64)throw Error("world count");checks++;
  let keys6=new Set(),chain=name.startsWith("CHAIN"),alias=name.endsWith("ALIAS"),p=name.includes("QUARTER")?(name.includes("THREE")?3:1):name.includes("ZERO")?0:name.endsWith("_ONE")?4:2;
  let obs=0,tru=0;
  for(let r of rr){
   let bits=["01","02","12"].flatMap(e=>["a","b"].map(s=>Number(r["oracle_original_edge_R"+e+s])));
   if(bits.some(x=>x!==0&&x!==1))throw Error("bit");let id=bits.join("");if(keys6.has(id))throw Error("duplicate");keys6.add(id);checks++;
   if(r.original_full_edge_source_probability!=="1/64")throw Error("weight");checks++;
   let edges=["01","02","12"].map(e=>Number(r["observed_reported_edge_Y"+e]));
   let pred=[0,1,2].map(i=>chain&&i===1?0:Number(2*bits[2*i]+bits[2*i+1]<p));
   for(let i=0;i<3;i++){if(edges[i]!==pred[i])throw Error("observed edge");checks++}
   let s=cluster(edges);if(s!==Number(r.observed_root_component_size))throw Error("observed cluster");checks++;
   let hidden=["01","02","12"].map(e=>Number(r["oracle_true_hidden_edge_H"+e]));
   for(let i=0;i<3;i++){if(hidden[i]!== (alias?0:edges[i]))throw Error("hidden edge");checks++}
   let t=cluster(hidden);if(t!==Number(r.oracle_true_root_component_size))throw Error("true cluster");checks++;
   obs+=Number(s===3);tru+=Number(t===3);
  }
  if(keys6.size!==64)throw Error("universe");checks++;
  let a=risk(rr,[]),b=risk(rr,["observed_reported_edge_Y01"]),c=risk(rr,["observed_reported_edge_Y01","observed_reported_edge_Y02","observed_reported_edge_Y12"]);
  if(c[0]!=="0")throw Error("full edges insufficient");checks++;
  worlds.push({world:name,source_rows:64,target_rate:repr(f(obs,64)),oracle_true_target_rate:repr(f(tru,64)),f0:a[0],f01:b[0],fall:c[0],gain:repr(minus(parse(a[0]),parse(b[0]))),remaining:b[0],support_f0:a[1],support_f01:b[1],support_fall:c[1]});
 }
 return {research_id:"R250_S46",method:"source_first_integer_grouped_Brier",source_rows:rows.length,source_checks:checks,failed_checks:0,worlds};
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require==="function"&&require.main===module){const fs=require("fs"),path=require("path");const file=process.argv[2]||path.join(__dirname,"..","R250","R250_ALL_576_ORIGINAL_THREE_NODE_EDGE_SOURCE_ATOMS.csv");console.log(JSON.stringify(run(fs.readFileSync(file,"utf8")),null,2));}
