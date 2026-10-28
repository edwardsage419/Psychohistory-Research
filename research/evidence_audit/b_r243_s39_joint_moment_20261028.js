"use strict";
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a;}
function frac(a,b=1n){a=BigInt(a);b=BigInt(b);let k=gcd(a<0n?-a:a,b);return [a/k,b/k];}
function add(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function subtract(a,b){return frac(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function format(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1];}
function parse(s){let x=String(s).split("/");return frac(x[0],x[1]||"1");}
function compute(raw){
 let worlds=JSON.parse(raw).world_results,results=[],cells=0,terms=0;
 if(worlds.length!==9)throw Error("worlds");
 for(let w of worlds){
  let atoms=[],mass=0n;
  for(let [path,prob] of Object.entries(w.exact_full_observed_five_point_path_joint)){
   let v=path.split(","),f=parse(prob);if(v.length!==5||(f[0]*16n)%f[1]!==0n)throw Error("atom");
   let m=f[0]*16n/f[1],d=subtract(parse(v[4]),parse(v[3]));atoms.push({v,m,z:d[0]>0n});mass+=m;cells++;
  }
  if(mass!==16n||atoms.reduce((s,a)=>s+(a.z?a.m:0n),0n)!==8n)throw Error("mass");
  for(let n=0;n<=4;n++){
   let groups=new Map();
   for(let a of atoms){let key=a.v.slice(0,n+1).join(",");if(!groups.has(key))groups.set(key,{yes:0n,no:0n});let c=groups.get(key);if(a.z)c.yes+=a.m;else c.no+=a.m;}
   let risk=frac(0n),values=new Set();
   for(let c of groups.values()){let size=c.yes+c.no;values.add(format(frac(c.yes,size)));risk=add(risk,frac(c.yes*c.no,16n*size));terms++;}
   if(n===4){if(risk[0]!==0n)throw Error("leak");continue;}
   results.push({world:w.world,n,prefix_support:groups.size,probabilities:[...values].sort(),oracle_brier:format(risk),baseline_brier:"1/4",gain:format(subtract(frac(1n,4n),risk))});
  }
 }
 return {study:"R243_S39",method:"independent_joint_mass_second_moment",input_blob:"c9ad714d688104b1e6fc663cef24fafaf2e3f7f4",worlds:worlds.length,conditions:results.length,observed_path_cells:cells,conditional_moment_terms:terms,leaked_Y4_control:"ALL_9_ZERO_INVALID",rows:results};
}
if(typeof module!=="undefined"){module.exports={compute};if(require.main===module){let fs=require("fs");console.log(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2));}}
