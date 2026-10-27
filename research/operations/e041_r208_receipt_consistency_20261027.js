#!/usr/bin/env node
"use strict";
const fs=require("node:fs");
const file=process.argv[2]||"research/validation/R208_HETEROGENEOUS_EDGE_ACTIVATION_2048_EXACT_RECEIPT_2026-10-27.json";
function audit(d){
let n=0,errors=[],agg=[{count:0,reg:[0,0,0,0],opt:[0,0,0,0]},{count:0,reg:[0,0,0,0],opt:[0,0,0,0]}];
const ck=(v,m)=>{n++;if(!v&&errors.length<12)errors.push(m)};
for(const r of d.rows){
 const m=r.g.toString(2).split("1").length-1,best=Math.max(...r.n);
 ck(r.m===m,"m "+r.g);ck(r.d===4**m,"d "+r.g);
 ck(r.n.length===5,"n length");ck(r.s.length===4,"s length");ck(r.r.length===4,"r length");
 ck(r.o===r.n.indexOf(best),"oracle "+r.g+","+r.e);
 for(let k=0;k<5;k++)ck(r.n[k]>=r.d&&r.n[k]<=5*r.d,"reach "+r.g+","+r.e+","+k);
 for(let k=0;k<4;k++){
  ck(Number.isInteger(r.s[k])&&r.s[k]>=0&&r.s[k]<5,"seed "+r.g+","+r.e+","+k);
  ck(r.r[k]===best-r.n[r.s[k]],"regret "+r.g+","+r.e+","+k);
  agg[r.e].reg[k]+=r.r[k]*4**(10-m);
  agg[r.e].opt[k]+=r.r[k]===0?1:0;
 }
 agg[r.e].count++;
}
ck(d.rows.length===2048,"rows");
for(let e=0;e<2;e++){
 ck(agg[e].count===1024,"env count");
 for(let k=0;k<4;k++){
  ck(agg[e].reg[k]===d.aggregates[e].regrets[k],"aggregate regret "+e+","+k);
  ck(agg[e].opt[k]===d.aggregates[e].optimal[k],"aggregate opt "+e+","+k);
 }
}
const edges=[[0,1],[0,2],[1,2]],prob=[[3,1,3],[1,3,1]];
for(let e=0;e<2;e++){
 let mass=0,sums=[0,0,0,0,0];
 for(let mask=0;mask<8;mask++){
  let w=1,parent=[0,1,2,3,4];
  const root=x=>{while(parent[x]!==x)x=parent[x];return x};
  for(let i=0;i<3;i++){
   const on=(mask>>i)&1,p=prob[e][i];w*=on?p:4-p;
   if(on){const [a,b]=edges[i];parent[root(a)]=root(b)}
  }
  mass+=w;
  for(let i=0;i<5;i++){let size=0;for(let j=0;j<5;j++)if(root(i)===root(j))size++;sums[i]+=w*size}
 }
 const r=d.rows.find(x=>x.g===19&&x.e===e);
 ck(mass===64,"triangle mass "+e);
 ck(r.n.every((x,i)=>x===sums[i]),"triangle reach "+e);
 ck(r.o===sums.indexOf(Math.max(...sums)),"triangle oracle "+e);
 ck(r.r[3]===Math.max(...sums)-sums[r.s[3]],"triangle regret "+e);
}
return {checks:n,failures:errors.length,errors,reg:agg.map(x=>x.reg),optimal:agg.map(x=>x.opt)};
}
const result=audit(JSON.parse(fs.readFileSync(file,"utf8")));
console.log(JSON.stringify({file,...result}));
if(result.failures)process.exitCode=1;
