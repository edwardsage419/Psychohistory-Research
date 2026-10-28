"use strict";
const fs=require("fs"),path=require("path");
function gcd(a,b){return b===0n?(a<0n?-a:a):gcd(b,a%b)}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");let g=gcd(n,d);return [n/g,d/g]}
function plus(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function minus(a,b){return frac(a[0]*b[1]-b[0]*a[1],a[1]*b[1])}
function show(a){return a[1]===1n?String(a[0]):a.join("/")}
const FEATURE={F0:[0],F1:[1],F2:[2],F12:[1,2],LEAK:[3]};
function compute(csv){let lines=csv.trim().split(/\r?\n/),header=lines.shift().split(","),ix=Array.from({length:4},(_,i)=>header.indexOf("observed_y"+i)),wi=header.indexOf("world"),pi=header.indexOf("original_source_probability");
 if([...ix,wi,pi].some(x=>x<0))throw Error("missing observed field");let worlds=new Map();
 for(let line of lines){let f=line.split(",");if(f[pi]!=="1/128")throw Error("unexpected original source mass");let name=f[wi],y=ix.map(i=>f[i]);if(y.some(x=>x!=="0"&&x!=="1")||y[0]!=="0")throw Error("invalid observed state");let rows=worlds.get(name)||[];rows.push(y);worlds.set(name,rows)}
 if(worlds.size!==9||lines.length!==1152)throw Error("wrong original source universe");
 let result=[];for(let [name,rows] of worlds){if(rows.length!==128)throw Error("wrong world source count");let risks={},support={};
 for(let [label,idx] of Object.entries(FEATURE)){let bins=new Map();for(let y of rows){let k=idx.map(i=>y[i]).join(""),g=bins.get(k)||{t:0n,n:0n};g.t++;if(y[3]==="1")g.n++;bins.set(k,g)}
 let value=frac(0);for(let {t,n} of bins.values())value=plus(value,frac(n*(t-n),128n*t));risks[label]=show(value);support[label]=bins.size}
 let gain=show(minus((x=>{let [n,d="1"]=x.split("/");return frac(n,d)})(risks.F2),(x=>{let [n,d="1"]=x.split("/");return frac(n,d)})(risks.F12)));
 result.push({world:name,risks,history_gain:gain,support})}
 return {source_rows:lines.length,worlds:result}}
function audit(csv,receipt){let x=compute(csv),ref=new Map(receipt.worlds.map(w=>[w.world,w])),checks=0;for(let w of x.worlds){let y=ref.get(w.world);if(!y)throw Error("missing world");for(let k of Object.keys(FEATURE)){if(w.risks[k]!==y.risks[k]||w.support[k]!==y.support[k])throw Error("risk mismatch "+w.world+" "+k);checks+=2}if(w.history_gain!==y.history_gain)throw Error("gain mismatch "+w.world);checks++}return {source_rows:x.source_rows,compared_fields:checks,failures:0,route:"CSV_source_counts_vs_PMF_fraction"}}
if(require.main===module){let csv=fs.readFileSync(path.join(__dirname,"../R244/R244_ALL_1152_ORIGINAL_BINARY_MARKOV_SOURCE_PATHS.csv"),"utf8"),receipt=JSON.parse(fs.readFileSync(path.join(__dirname,"../validation/R244_S40_HISTORY_BRIER_RECEIPT_2026-10-28.json"),"utf8"));console.log(JSON.stringify(audit(csv,receipt),null,2))}
module.exports={compute,audit};
