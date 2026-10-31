"use strict";
// R307 S103 exact synthetic model. All arithmetic uses reduced BigInt fractions.
function gcd(a,b){while(b){let q=a%b;a=b;b=q;}return a<0n?-a:a;}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];}
function add(x,y){return f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function sub(x,y){return add(x,[-y[0],y[1]]);}
function mul(x,y){return f(x[0]*y[0],x[1]*y[1]);}
function div(x,y){return f(x[0]*y[1],x[1]*y[0]);}
function pow(x,t){let a=f(1);for(let i=0;i<t;i++)a=mul(a,x);return a;}
function fmt(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1];}
const Z=f(0),H=f(1,2),O=f(1),SIX=f(6),LEVELS=[Z,H,O];
const DESIGNS=["D0_T0_JOINT_M1","D1_PRIVATE_M1","D2_PUBLIC_M1","D3_PUBLIC_M1_M2","D4_JOINT_M1","D5_JOINT_M1_M2"];
function predict(t,c,k,n,m){
 const odds=pow(add(O,mul(c,k)),t);
 const b=div(odds,add(O,odds));
 const retention=sub(O,mul(n,div(f(6-m),SIX)));
 return {b,public:add(H,mul(retention,sub(b,H)))};
}
function signature(t,c,k,n,d){
 const x=predict(t,c,k,n,1),y=predict(t,c,k,n,2);
 if(d===0){let z=predict(0,c,k,n,1);return [fmt(z.b),fmt(z.public)];}
 if(d===1)return [fmt(x.b)];
 if(d===2)return [fmt(x.public)];
 if(d===3)return [fmt(x.public),fmt(y.public)];
 if(d===4)return [fmt(x.b),fmt(x.public)];
 if(d===5)return [fmt(x.b),fmt(x.public),fmt(y.b),fmt(y.public)];
 throw Error("unknown design");
}
function run(){
 const rows=[],tables=[];
 for(const t of [1,2,3]){
  const groups=DESIGNS.map(()=>new Map());
  for(const c of LEVELS)for(const k of LEVELS)for(const n of LEVELS){
   const x=predict(t,c,k,n,1),y=predict(t,c,k,n,2);
   const key=[fmt(c),fmt(k),fmt(n)].join("|");
   rows.push({t,c:fmt(c),k:fmt(k),n:fmt(n),private:fmt(x.b),public_m1:fmt(x.public),public_m2:fmt(y.public)});
   DESIGNS.forEach((_,i)=>{let s=JSON.stringify(signature(t,c,k,n,i));if(!groups[i].has(s))groups[i].set(s,[]);groups[i].get(s).push(key);});
  }
  DESIGNS.forEach((name,i)=>{
   const partitions=[...groups[i]].map(([signature,triples])=>({signature:JSON.parse(signature),triples}));
   const hist={};for(const g of partitions){let k=String(g.triples.length);hist[k]=(hist[k]||0)+1;}
   if(partitions.reduce((a,g)=>a+g.triples.length,0)!==27)throw Error("coverage failed");
   tables.push({t,design:name,classes:partitions.length,class_size_histogram:hist,singleton_worlds:partitions.filter(g=>g.triples.length===1).length,max_class_size:Math.max(...partitions.map(g=>g.triples.length)),uniform_prior_optimal_accuracy:fmt(f(partitions.length,27)),partitions});
  });
 }
 if(rows.length!==81||new Set(rows.map(x=>[x.t,x.c,x.k,x.n].join("|"))).size!==81||tables.length!==18)throw Error("universe failed");
 const fields=["t","c","k","n","private","public_m1","public_m2"];
 const csv=fields.join(",")+"\n"+rows.map(x=>fields.map(k=>x[k]).join(",")).join("\n")+"\n";
 const json=JSON.stringify({research_id:"R307",extension:"S103",evidence:"E1_ARTIFICIAL",prior:"1/2",confirmatory_t:[1,2,3],candidate_triples_per_t:27,world_count:81,designs:DESIGNS,results:tables,real_human_E2:0,historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"},null,2)+"\n";
 return {csv,json,rows,tables};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),out=run();
 fs.writeFileSync("R307_S103_ALL_81_CONFIRMATORY_WORLDS.csv",out.csv);
 fs.writeFileSync("R307_S103_EXACT_PARTITIONS.json",out.json);
 console.log(JSON.stringify(out.tables.map(({t,design,classes,singleton_worlds,max_class_size,uniform_prior_optimal_accuracy})=>({t,design,classes,singleton_worlds,max_class_size,uniform_prior_optimal_accuracy})),null,2));
}
