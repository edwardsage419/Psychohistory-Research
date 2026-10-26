// E034: independent prefix-cylinder masks for R200. Run:
// node research/operations/e034_r200_prefix_mask_20261027.js research/validation/R200_SEQUENTIAL_PREFIX_18_EXACT_RECEIPT_2026-10-27.json
"use strict";
const fs=require("node:fs");
const names=["LOW","HIGH","MID","UP2","UP3","DOWN2","DOWN3","SPIKE2","SPIKE3"];
const alts=["UP2","UP3","DOWN2","DOWN3"];
function q(s,t){if(s==="LOW")return 1n;if(s==="HIGH")return 3n;if(s==="MID")return 2n;
 if(s.startsWith("UP"))return t>=Number(s.slice(2))?3n:1n;
 if(s.startsWith("DOWN"))return t>=Number(s.slice(4))?1n:3n;
 if(s.startsWith("SPIKE"))return t===Number(s.slice(5))?3n:1n;
 throw Error("unknown source");}
function bits(i,t){return Array.from({length:t},(_,j)=>(i>>(t-j-1))&1);}
function mass(s,b){return b.reduce((v,x,i)=>{const p=q(s,i+1);return v*(x?p:4n-p);},1n);}
function alarm(b,mode){return (mode==="scan"?alts:["UP2"]).some(s=>mass(s,b)>=4n*2n**BigInt(b.length));}
function gcd(a,b){while(b){const x=a%b;a=b;b=x;}return a;}
function f(n,d){const g=gcd(n,d);return String(n/g)+"/"+String(d/g);}
function run(){
 const masks={};
 for(const T of [4,5])for(const mode of ["scan","single"]){
  masks[T+mode]=Array.from({length:2**T},(_,i)=>{
   const b=bits(i,T);let first=0;
   for(let t=3;t<=T;t++)if(alarm(b.slice(0,t),mode)){first=t;break;}
   return {b,first,last:alarm(b,mode)};
  });
 }
 const worlds=[];let normalized=0;
 for(const T of [4,5])for(const source of names){
  const den=4n**BigInt(T),row={source,T,modes:{}};
  for(const mode of ["scan","single"]){
   let total=0n,last=0n,ever=0n;const first={};
   for(let t=3;t<=T;t++)first["t"+t]=0n;
   for(const m of masks[T+mode]){const w=mass(source,m.b);total+=w;
    if(m.last)last+=w;if(m.first){ever+=w;first["t"+m.first]+=w;}}
   if(total!==den||ever<last)throw Error("mass or inclusion");normalized++;
   const firstExact={};for(let t=3;t<=T;t++)firstExact["t"+t]=f(first["t"+t],den);
   row.modes[mode]={terminal:f(last,den),ever:f(ever,den),first_alarm:firstExact,
    never:f(den-ever,den),excess_ever_over_terminal:f(ever-last,den)};
  }worlds.push(row);
 }
 return {worlds,normalized,scan_t4_first:masks["4scan"].filter(x=>x.first===4).length,
  scan_t5_first:masks["5scan"].filter(x=>x.first===5).length};
}
function compare(x,receipt){
 let n=0;for(const row of x.worlds){
  const ref=receipt.worlds.find(y=>y.source===row.source&&y.T===row.T);
  if(!ref)throw Error("missing world");
  for(const mode of ["scan","single"]){
   for(const key of ["terminal","ever","never","excess_ever_over_terminal"]){
    n++;if(row.modes[mode][key]!==ref.modes[mode][key])throw Error("mismatch "+key);
   }
   for(const key of Object.keys(row.modes[mode].first_alarm)){
    n++;if(row.modes[mode].first_alarm[key]!==ref.modes[mode].first_alarm[key])throw Error("mismatch "+key);
   }
  }
 }return n;
}
if(require.main===module){
 const x=run(),n=process.argv[2]?compare(x,JSON.parse(fs.readFileSync(process.argv[2],"utf8"))):null;
 console.log(JSON.stringify({worlds:x.worlds.length,normalized:x.normalized,exactMatches:n,
  scan_t4_first:x.scan_t4_first,scan_t5_first:x.scan_t5_first,
  mid5:x.worlds.find(y=>y.source==="MID"&&y.T===5)},null,2));
}
module.exports={run,compare};
