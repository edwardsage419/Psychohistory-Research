#!/usr/bin/env node
// E049 independent frozen-world exact replay, Node.js standard library.
// Usage: node e049_r216_s12_600_world_replay_20261027.js RECEIPT.json
// Selftest: node e049_r216_s12_600_world_replay_20261027.js --selftest
const fs=require('node:fs'),assert=require('node:assert/strict');
const worlds=['VALID_CONSTANT','VALID_HETEROGENEOUS','VALID_DYNAMIC','POST_EVENT_SHOCK_MIMIC','DIFFERENTIAL_PRETREND','LATE_ANTICIPATION'];
const thresholds=[0,1,2,4,'ALL'], names=['E_k1_clean','L_k0_clean','E_k1_BAD_L_ALREADY_TREATED'];
const targets={VALID_CONSTANT:[2,2,2],VALID_HETEROGENEOUS:[1,3,1],VALID_DYNAMIC:[4,1,4],POST_EVENT_SHOCK_MIMIC:[0,0,0],DIFFERENTIAL_PRETREND:[0,0,0],LATE_ANTICIPATION:[2,3,2]};
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function f(n,d=1n){n=BigInt(n);d=BigInt(d);assert(d!==0n);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);n/=g;d/=g;return d===1n?String(n):String(n)+'/'+String(d);}
function baseline(world){
 const a=[];for(const g of ['E','L','N'])for(let t=0;t<4;t++){
  let v={E:1,L:-1,N:0}[g]+t;
  if(world==='DIFFERENTIAL_PRETREND'&&g==='E')v+=t;
  if(world==='LATE_ANTICIPATION'&&g==='L'&&t===2)v++;
  if(world==='POST_EVENT_SHOCK_MIMIC'){
   if(g==='E'&&t===2)v+=2;if(g==='E'&&t===3)v+=4;if(g==='L'&&t===3)v++;
  }else if(world==='VALID_CONSTANT'){
   if((g==='E'&&t>=2)||(g==='L'&&t===3))v+=2;
  }else if(world==='VALID_HETEROGENEOUS'){
   if(g==='E'&&t>=2)v++;if(g==='L'&&t===3)v+=3;
  }else if(world==='VALID_DYNAMIC'){
   if(g==='E'&&t===2)v+=2;if(g==='E'&&t===3)v+=4;if(g==='L'&&t===3)v++;
  }else if(world==='LATE_ANTICIPATION'){
   if(g==='E'&&t===2)v++;if(g==='E'&&t===3)v+=2;if(g==='L'&&t===3)v+=3;
  }
  a.push(v);
 }return a;
}
function calculate(){
 const out=[];for(const world of worlds){
  const base=baseline(world),source=[];
  for(let mask=0;mask<4096;mask++){
   const y=base.map((v,i)=>v+((mask&(1<<i))?1:-1));
   source.push({preE:y[1]-y[0]-y[9]+y[8],preL:y[6]-y[5]-y[10]+y[9],
    est:[y[3]-y[1]-y[11]+y[9],y[7]-y[6]-y[11]+y[10],y[3]-y[1]-y[7]+y[5]]});
  }
  for(const h of thresholds){
   const sel=source.filter(x=>h==='ALL'||Math.max(Math.abs(x.preE),Math.abs(x.preL))<=h);
   const n=BigInt(sel.length),sums=k=>sel.reduce((a,x)=>a+BigInt(x[k]),0n);
   const row={world,threshold:h,accepted:sel.length,source_count:4096,acceptance_probability:f(n,4096n),
    pre_E_mean:n?f(sums('preE'),n):null,pre_L_mean:n?f(sums('preL'),n):null,estimators:{}};
   names.forEach((name,j)=>{
    const v=sel.map(x=>BigInt(x.est[j])),s=v.reduce((a,x)=>a+x,0n),sq=v.reduce((a,x)=>a+x*x,0n),tar=BigInt(targets[world][j]);
    const loss=v.reduce((a,x)=>a+(x-tar)**2n,0n);
    row.estimators[name]={target:Number(tar),mean:n?f(s,n):null,variance:n?f(sq*n-s*s,n*n):null,
     bias:n?f(s-n*tar,n):null,mse:n?f(loss,n):null};
   });
   out.push(row);
  }
 }return out;
}
const got=calculate();assert.equal(got.length,30);
assert.deepEqual(baseline('VALID_DYNAMIC'),baseline('POST_EVENT_SHOCK_MIMIC'));
assert.equal(got.filter(x=>x.accepted===0).length,2);
if(process.argv[2]==='--selftest'){
 const row=(w,h)=>got.find(x=>x.world===w&&x.threshold===h);
 assert.equal(row('VALID_CONSTANT',0).accepted,576);
 assert.equal(row('VALID_DYNAMIC',0).estimators.E_k1_clean.mse,'10/3');
 assert.equal(row('POST_EVENT_SHOCK_MIMIC',0).estimators.E_k1_clean.mse,'58/3');
 assert.equal(row('POST_EVENT_SHOCK_MIMIC','ALL').estimators.E_k1_clean.mse,'20');
 console.log(JSON.stringify({status:'PASS',selftestAssertions:7,worlds:6,sourceSlots:24576,rows:30}));
}else{
 assert(process.argv[2],'receipt path required');
 const ref=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));assert.equal(ref.rows.length,30);
 let checks=0;for(const row of got){
  const orig=ref.rows.find(x=>x.world===row.world&&x.threshold===row.threshold);assert(orig,'missing row');
  for(const key of ['accepted','source_count','acceptance_probability','pre_E_mean','pre_L_mean']){
   assert.deepEqual(row[key],orig[key],row.world+'/'+row.threshold+'/'+key);checks++;
  }
  for(const name of names)for(const key of ['target','mean','variance','bias','mse']){
   assert.deepEqual(row.estimators[name][key],orig.estimators[name][key],row.world+'/'+row.threshold+'/'+name+'/'+key);checks++;
  }
 }
 assert.equal(checks,600);
 console.log(JSON.stringify({status:'PASS',exactFieldChecks:checks,worlds:6,sourceSlots:24576,rows:30,zeroAcceptance:2,observationalAlias:true}));
}
