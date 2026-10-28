#!/usr/bin/env node
"use strict";
// R237 S33: frozen E1 exact three-class Brier risk; Node standard library only.
// Usage: node research/validation/r237_s33_prefix_brier_exact_20261028.js
const fs = require("fs");
const input = "research/R237/R237_EXACT_RESULTS.json";
const source = JSON.parse(fs.readFileSync(input, "utf8"));
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a;}
function F(v){if(typeof v==="object")return v;const s=String(v).split("/");let a=BigInt(s[0]),b=BigInt(s[1]||"1");if(b===0n)throw Error("zero denominator");let g=gcd(a,b);return {n:a/g,d:b/g};}
function calc(a,b,op){a=F(a);b=F(b);let n,d;if(op==="+"){n=a.n*b.d+b.n*a.d;d=a.d*b.d;}else if(op==="-"){n=a.n*b.d-b.n*a.d;d=a.d*b.d;}else if(op==="*"){n=a.n*b.n;d=a.d*b.d;}else{n=a.n*b.d;d=a.d*b.n;}if(d===0n)throw Error("division by zero");let g=gcd(n,d);if(d<0n)g=-g;return {n:n/g,d:d/g};}
const A=(a,b)=>calc(a,b,"+"),S=(a,b)=>calc(a,b,"-"),M=(a,b)=>calc(a,b,"*"),D=(a,b)=>calc(a,b,"/"),Z=F(0),O=F(1),T=F("1/3"),txt=v=>v.d===1n?String(v.n):v.n+"/"+v.d;
function assert(cond,msg){if(!cond)throw Error(msg);}
const worlds=[];
for(const world of source.world_results){
  const joint=Object.fromEntries(Object.entries(world.exact_observable_three_position_word_joint).map(([k,v])=>[k,F(v)]));
  assert(Object.keys(joint).length===27, "27 cells");
  assert(txt(Object.values(joint).reduce(A,Z))==="1","joint mass");
  const cells={},unigram=[Z,Z,Z],oracle={};
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){
    const prefix=""+i+j;cells[prefix]=[joint[prefix+"0"],joint[prefix+"1"],joint[prefix+"2"]];
    for(let k=0;k<3;k++)unigram[k]=A(unigram[k],cells[prefix][k]);
  }
  for(const [p,arr] of Object.entries(cells)){
    const mass=arr.reduce(A,Z);assert(mass.n>0n,"positive prefix");
    oracle[p]=arr.map(x=>D(x,mass));
    assert(txt(oracle[p].reduce(A,Z))==="1","oracle normalized");
  }
  const q={
    ORACLE_PREFIX:oracle,
    UNIGRAM:Object.fromEntries(Object.keys(cells).map(p=>[p,unigram])),
    UNIFORM:Object.fromEntries(Object.keys(cells).map(p=>[p,[T,T,T]]))
  };
  const risk={};
  for(const [name,model] of Object.entries(q)){
    let total=Z;
    for(const [p,arr] of Object.entries(cells))for(let k=0;k<3;k++){
      let loss=Z;
      for(let j=0;j<3;j++){const e=S(model[p][j],j===k?O:Z);loss=A(loss,M(e,e));}
      total=A(total,M(arr[k],loss));
    }
    assert(total.n>=0n,"risk nonnegative");risk[name]=txt(total);
  }
  worlds.push({world:world.world,risks:risk,regrets:{
    UNIGRAM:txt(S(F(risk.UNIGRAM),F(risk.ORACLE_PREFIX))),
    UNIFORM:txt(S(F(risk.UNIFORM),F(risk.ORACLE_PREFIX)))
  }});
}
const by=Object.fromEntries(worlds.map(x=>[x.world,x]));
for(const [a,b] of [["BASE_TOPICS","LABEL_SWAP_ALIAS"],["DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B"]])
  assert(JSON.stringify(by[a].risks)===JSON.stringify(by[b].risks),"observable alias");
for(const name of ["DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B","UNIFORM_WORDS"])
  assert(by[name].regrets.UNIGRAM==="0","iid negative control");
assert(by.BASE_TOPICS.regrets.UNIGRAM!=="0","base strict gain");
assert(by.UNIFORM_WORDS.regrets.UNIFORM==="0","uniform negative control");
console.log(JSON.stringify({research_id:"R237_S33",evidence:"E1_ONLY",source_blob_sha1:"01af9a479bd6aca2f2555b5e5127039f8bb89728",world_count:worlds.length,worlds,new_E2:0,new_E3:0},null,2));
