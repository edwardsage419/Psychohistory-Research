"use strict";
function g(a,b){while(b){let t=a%b;a=b;b=t;}return a;}
function rat(a,b=1n){a=BigInt(a);b=BigInt(b);let z=g(a<0n?-a:a,b);return [a/z,b/z];}
function add(a,b){return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return rat(a[0]*b[0],a[1]*b[1]);}
function out(a){return a[1]===1n?String(a[0]):a[0]+"/"+a[1];}
function read(s){let a=String(s).split("/");return rat(a[0],a[1]||"1");}
function compute(csv){
 let lines=csv.trim().split(/\r?\n/),head=lines.shift().split(",");
 let rows=lines.map(line=>{let v=line.split(",");if(v.length!==head.length)throw Error("width");return Object.fromEntries(head.map((k,i)=>[k,v[i]]));});
 let worlds=[...new Set(rows.map(x=>x.world))],results=[],checks=0;
 if(rows.length!==144||worlds.length!==9)throw Error("universe");
 for(let world of worlds){
  let data=rows.filter(x=>x.world===world);if(data.length!==16)throw Error("world source count");
  let keys=new Set(),z=[];
  for(let x of data){
   let e=[1,2,3,4].map(i=>x["oracle_original_epsilon_"+i]);keys.add(e.join(","));
   if(x.original_path_probability!=="1/16"||e.some(t=>t!=="1"&&t!=="-1"))throw Error("source");
   let d=sub(read(x.observed_y4),read(x.observed_y3));if(out(d)!==out(read(x.observed_increment4)))throw Error("increment");
   z.push(d[0]>0n?1:0);checks+=3;
  }
  if(keys.size!==16||z.reduce((a,b)=>a+b,0)!==8)throw Error("closure");
  let base=rat(1n,4n);
  for(let n=0;n<=4;n++){
   let bins=new Map();
   for(let i=0;i<16;i++){let key=data[i]["observed_y0"];for(let k=1;k<=n;k++)key+=","+data[i]["observed_y"+k];if(!bins.has(key))bins.set(key,[]);bins.get(key).push(i);}
   let risk=rat(0n),ps=new Set();
   for(let ix of bins.values()){
    let p=rat(ix.reduce((s,i)=>s+z[i],0),ix.length);ps.add(out(p));
    for(let i of ix){let diff=sub(p,rat(z[i]));risk=add(risk,mul(diff,diff));checks++;}
   }
   risk=mul(risk,rat(1n,16n));
   if(n===4){if(risk[0]!==0n)throw Error("leak control");continue;}
   results.push({world,n,prefix_support:bins.size,probabilities:[...ps].sort(),oracle_brier:out(risk),baseline_brier:out(base),gain:out(sub(base,risk))});
  }
 }
 return {study:"R243_S39",method:"source_level_squared_brier",input_blob:"1bb098387d25654bcf3d52a8dde63ca42184a9f1",source_rows:rows.length,worlds:worlds.length,conditions:results.length,checks,leaked_Y4_control:"ALL_9_ZERO_INVALID",rows:results};
}
if(typeof module!=="undefined"){module.exports={compute};if(require.main===module){let fs=require("fs");console.log(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2));}}
