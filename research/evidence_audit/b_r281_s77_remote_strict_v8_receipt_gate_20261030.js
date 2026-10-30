"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);const g=gcd(a,b);if(!g||b===0n)throw Error("invalid fraction");if(b<0n){a=-a;b=-b;}return {n:a/g,d:b/g};}
function read(s){const x=String(s).split("/");return f(x[0],x[1]||1);}
function st(x){return x.d===1n?String(x.n):String(x.n)+"/"+String(x.d);}
function add(a,b){return f(a.n*b.d+b.n*a.d,a.d*b.d);}
function mul(a,b){return f(a.n*b.n,a.d*b.d);}
function sub(a,b){return add(a,f(-b.n,b.d));}
function div(a,b){return f(a.n*b.d,a.d*b.n);}
function pow(a,n){return f(a.n**BigInt(n),a.d**BigInt(n));}
function eq(a,b){return a.n*b.d===b.n*a.d;}
function greater(a,b){return a.n*b.d>b.n*a.d;}
const one=f(1),zero=f(0),comb=[1,4,6,4,1];
function sym(q,y){const table={"1/16":[[4,-1,-1],[4,0,0]],"15/16":[[4,0,0],[4,-1,-1]],"1/4":[[2,-1,0],[2,0,0]],"3/4":[[2,0,0],[2,-1,0]],"1/2":[[1,0,0],[1,0,0]]};return table[st(q)][y].map(fv=>f(fv));}
function verify(csv,json){
 const obj=JSON.parse(json);
 if(obj.evidence!=="E1_INTERNAL_NONBLIND_EXPLORATORY"||obj.world_count!==12||obj.source_count!==192)throw Error("evidence");
 const lines=csv.trimEnd().split("\n"),header=lines.shift().split(",");
 if(lines.length!==192)throw Error("source count");
 const seen=new Set(),counts=new Map(),massSum=new Map();
 for(const line of lines){
  const cells=line.split(",");if(cells.length!==header.length)throw Error("csv width");
  const r=Object.fromEntries(header.map((h,i)=>[h,cells[i]]));
  const key=r.p+"|"+r.boundary+"|"+r.epsilon,source=key+"|"+r.bits;
  if(seen.has(source))throw Error("duplicate");seen.add(source);
  if(!["1/4","1/2","3/4"].includes(r.p)||!["0","1"].includes(r.boundary)||!["1/16","1/4"].includes(r.epsilon))throw Error("world");
  if(!/^[01]{4}$/.test(r.bits))throw Error("bits");
  const p=read(r.p),e=read(r.epsilon),q=r.boundary==="0"?e:sub(one,e),k=r.bits.split("1").length-1;
  const mass=mul(pow(p,k),pow(sub(one,p),4-k));
  const c0=sym(q,0),c1=sym(q,1);
  const sc=c0.map((x,i)=>div(add(mul(f(4-k),x),mul(f(k),c1[i])),f(4)));
  const lq=mul(pow(q,k),pow(sub(one,q),4-k)),lp=mul(pow(p,k),pow(sub(one,p),4-k));
  const expected={q:st(q),k:String(k),mass:st(mass),ln2:st(sc[0]),ln3:st(sc[1]),ln5:st(sc[2]),strict_win:greater(lq,lp)?"1":"0",tie:eq(lq,lp)?"1":"0"};
  if(Object.entries(expected).some(([k,v])=>r[k]!==v))throw Error("source mismatch "+source);
  counts.set(key,(counts.get(key)||0)+1);massSum.set(key,add(massSum.get(key)||zero,mass));
 }
 if(counts.size!==12||[...counts].some(([key,n])=>n!==16||!eq(massSum.get(key),one)))throw Error("coverage");
 if(obj.worlds.length!==12)throw Error("worlds");
 const worldSeen=new Set();
 for(const w of obj.worlds){
  const key=w.p+"|"+w.boundary+"|"+w.epsilon;if(worldSeen.has(key)||!counts.has(key))throw Error("world duplicate");worldSeen.add(key);
  const p=read(w.p),e=read(w.epsilon),q=w.boundary==="0"?e:sub(one,e);
  const c0=sym(q,0),c1=sym(q,1),risk=c0.map((x,i)=>add(mul(sub(one,p),x),mul(p,c1[i])));
  let win=zero,tie=zero;
  for(let k=0;k<=4;k++){
   const weight=mul(f(comb[k]),mul(pow(p,k),pow(sub(one,p),4-k)));
   const lq=mul(pow(q,k),pow(sub(one,q),4-k)),lp=mul(pow(p,k),pow(sub(one,p),4-k));
   if(greater(lq,lp))win=add(win,weight);
   if(eq(lq,lp))tie=add(tie,weight);
  }
  const inf=w.boundary==="0"?sub(one,pow(sub(one,p),4)):sub(one,pow(p,4));
  if(JSON.stringify(w.risk_coefficients)!==JSON.stringify(risk.map(st))||w.strict_win_probability!==st(win)||w.tie_probability!==st(tie)||w.original_unclipped_infinite_probability!==st(inf)||w.original_unclipped_expected_risk!=="INF")throw Error("analytic world mismatch "+key);
 }
 if(obj.frozen_no_tie_when_q_differs_status!=="FAIL"||obj.frozen_no_tie_counterexample.tie_probability!=="27/128")throw Error("frozen negative evidence");
 return {status:"PASS",rows:lines.length,worlds:worldSeen.size,independent_binomial_cells:60};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");const csv=fs.readFileSync(process.argv[2],"utf8"),json=fs.readFileSync(process.argv[3],"utf8");console.log(JSON.stringify(verify(csv,json)));
}
