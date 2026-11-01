#!/usr/bin/env node
"use strict";
function produce(){
  const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}let a=n<0n?-n:n,b=d;while(b){const t=a%b;a=b;b=t}return [n/a,d/a]};
  const add=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const sub=(x,y)=>F(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const mul=(x,y)=>F(x[0]*y[0],x[1]*y[1]);
  const cmp=(x,y)=>{const v=x[0]*y[1]-y[0]*x[1];return v<0n?-1:v>0n?1:0};
  const max=(x,y)=>cmp(x,y)>=0?x:y;
  const s=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
  const one=F(1n),half=F(1n,2n),qualities=[[1n,2n],[5n,8n],[3n,4n],[7n,8n],[1n,1n]],costs=[0n,1n,2n,3n,4n].map(n=>F(n,16n)),worlds=[];
  for(const qq of qualities){const q=F(...qq);for(const c of costs){for(let k=0;k<=8;k++){const b=F(BigInt(k),8n),pb=sub(one,b),nq=sub(one,q);
    const p00=mul(pb,q),p01=mul(pb,nq),p10=mul(b,nq),p11=mul(b,q);
    if(cmp(add(add(p00,p01),add(p10,p11)),one)!==0)throw Error("mass");
    const m=max(b,pb),u=add(max(p00,p10),max(p01,p11)),sense=sub(u,c),gross=sub(u,m),v=max(m,sense);
    const action=cmp(sense,m)>0?"SENSE":cmp(b,half)>0?"GUESS_1":"GUESS_0";
    worlds.push({belief:s(b),accuracy:s(q),cost:s(c),immediate_value:s(m),uncosted_sense_value:s(u),sense_value:s(sense),gross_information_value:s(gross),optimal_value:s(v),chosen_action:action});
  }}}
  return {model:"R327_S123_FINITE_SENSOR_QUALITY_COST_E1",evidence_grade:"E1_SYNTHETIC_ONLY",freeze_commit:"5bfd3c13e4ee9d4b6af1defc17469c33bd538c4c",world_count:225,worlds};
}
if (typeof require !== 'undefined' && require.main === module) process.stdout.write(JSON.stringify(produce())+'\n');
