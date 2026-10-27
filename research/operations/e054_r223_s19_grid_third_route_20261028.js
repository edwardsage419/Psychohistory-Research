#!/usr/bin/env node
'use strict';
// Independent BigInt fraction replay of R223 S19, no third-party dependencies.
// Usage: node e054_r223_s19_grid_third_route_20261028.js R223_EXACT_RESULTS.json R223_S19_252_CONDITION_EXACT.csv
const fs = require('node:fs');
const assert = require('node:assert/strict');
if (process.argv.length !== 4) { console.error('Usage: node script.js input.json grid.csv'); process.exit(2); }
const worlds = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')).worlds;
const rows = fs.readFileSync(process.argv[3], 'utf8').trim().split(/\r?\n/).slice(1).map(x => {
  const c=x.split(',');
  assert.equal(c.length,7);
  return {w:c[0],e:BigInt(c[1]),d:BigInt(c[2]),B:c[3],L:c[4],nul:c[5],cover:c[6]};
});
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
const f=(n,d=1n)=>{if(d===0n)throw Error('zero denominator');const g=gcd(n,d);return [n/g,d/g]};
const parse=s=>{const z=s.split('/');return f(BigInt(z[0]),BigInt(z[1]??1))};
const fmt=x=>x[1]===1n?String(x[0]):x[0]+'/'+x[1];
const le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
let checks=0;
function ck(a,b,label){checks++;assert.equal(a,b,label)}
const per=[];
for(let i=0;i<worlds.length;i++){
  const w=worlds[i],rr=parse(w.observed_RR),truth=parse(w.true_causal_RR);
  const subset=rows.slice(i*36,(i+1)*36);
  let n=0,c=0;
  for(let j=0;j<36;j++){
    const x=subset[j],E=x.e,D=x.d,B=f(E*D,E+D-1n),L=f(rr[0]*B[1],rr[1]*B[0]);
    const nullOk=le(L,[1n,1n]);
    const covered=w.oracle_sensitivity_RR_EU===null?null:
      (E>=BigInt(w.oracle_sensitivity_RR_EU)&&D>=BigInt(w.oracle_sensitivity_RR_UD));
    ck(x.w,w.world,'world '+i+':'+j);
    ck(x.B,fmt(B),'bias factor '+i+':'+j);
    ck(x.L,fmt(L),'lower bound '+i+':'+j);
    ck(x.nul,String(nullOk),'null flag '+i+':'+j);
    ck(x.cover,String(covered),'oracle flag '+i+':'+j);
    if(covered===true)ck(le(L,truth),true,'oracle bound '+i+':'+j);
    if(nullOk)n++;
    if(covered)c++;
  }
  per.push({world:w.world,null_compatible:n,oracle_covered:c});
}
ck(rows.length,252,'row count');
ck(rows[0].w==='NULL_CONFOUNDED'&&rows[36].w==='CAUSAL_ALIAS',true,'ordering');
for(let j=0;j<36;j++){
  ck(rows[j].L,rows[36+j].L,'observational alias bound '+j);
  ck(rows[j].nul,rows[36+j].nul,'observational alias flag '+j);
}
console.log(JSON.stringify({checks,failures:0,conditions:rows.length,per_world:per}));
