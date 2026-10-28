#!/usr/bin/env node
'use strict';
// R232 S28 exact E1 source-level measurement channel sensitivity.
// Run at repository root: node research/validation/r232_s28_proxy_noise_exact_20261028.js > receipt.json
const fs=require('fs'),crypto=require('crypto'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const SOURCE=path.join(ROOT,'research/R232/R232_ALL_1024_ORIGINAL_SEM_EXOGENOUS_SOURCES.csv');
const SOURCE_SHA='86add6aeacc8c4b34bdc7d82738fb0382e1e2e627ef31bb30a5d2ac9ada1d38f';
const SOURCE_BLOB='97be4f33d8c31c1a36541a9e50afd13447a942ec';
const FREEZE='e21b7c3f394afeceacb6a92882075b71c6a4d7c1';
const WORLDS={
 RANDOMIZED_MEDIATED:['R',1,0,1,0,0,0],RANDOMIZED_NULL:['R',0,1,1,0,0,0],
 LATENT_CAUSAL_ALIAS:['U',1,0,1,0,0,0],LATENT_COMMON_ALIAS:['U',0,1,1,0,0,0],
 RANDOMIZED_DIRECT_AND_MEDIATED:['R',1,0,1,1,0,0],
 RANDOMIZED_MEDIATOR_CONFOUNDED:['R',1,1,1,0,1,0],
 RANDOMIZED_DIRECT_ONLY:['R',0,1,1,1,0,0],
 RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR:['R',1,0,1,0,0,1]
};
const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');
 if(d<0n){n=-n;d=-d;}let a=n<0n?-n:n,b=d;while(b){let t=a%b;a=b;b=t;}return [n/a,d/a];};
const add=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const sub=(x,y)=>F(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>F(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>F(x[0]*y[1],x[1]*y[0]);
const str=x=>x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1]);
function assert(ok,msg){if(!ok)throw Error(msg);}
function readRows(){let bytes=fs.readFileSync(SOURCE),sha=crypto.createHash('sha256').update(bytes).digest('hex');
 assert(sha===SOURCE_SHA,'original source SHA256 mismatch');let lines=bytes.toString('utf8').trimEnd().split(/\r?\n/),keys=lines.shift().split(',');
 const out={};for(let w of Object.keys(WORLDS))out[w]=[];
 for(let line of lines){let vals=line.split(',');assert(vals.length===keys.length,'CSV width');let r=Object.fromEntries(keys.map((k,i)=>[k,vals[i]]));
 assert(Object.hasOwn(out,r.world),'unknown original world');assert(r.original_source_probability==='1/128','original source weight');out[r.world].push(r);}
 for(let [w,rows] of Object.entries(out)){assert(rows.length===128,'source count '+w);
  let seen=new Set(rows.map(r=>['U','R','EM','EY','EW','EZ1','EZ2'].map(k=>r['oracle_original_'+k]).join(',')));
  assert(seen.size===128,'source identity duplicates '+w);}
 return out;
}
function run(){let sources=readRows(),results=[],aliases={};
 for(let [world,p] of Object.entries(WORLDS))for(let lambda of [0,1,2,3]){
  let obs=[],joint=new Map();for(let r of sources[world]){
   let a=Number(r.observed_A),w=Number(r.observed_W)+lambda*Number(r.oracle_original_EW),
       y=Number(r.observed_Y),z1=Number(r.observed_Z1),z2=Number(r.observed_Z2);
   let x=[a,w,y,z1,z2];obs.push(x);let key=x.join(',');joint.set(key,(joint.get(key)||0)+1);
  }
  assert(obs.length===128,'source length');assert([...joint.values()].reduce((a,b)=>a+b,0)===128,'probability mass');
  let means=Array.from({length:5},(_,i)=>obs.reduce((s,x)=>s+BigInt(x[i]),0n));
  assert(means.every(x=>x===0n),'symmetry means changed');
  let c=Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>F(obs.reduce((s,x)=>s+BigInt(x[i])*BigInt(x[j]),0n),128n)));
  let va=c[0][0],vw=c[1][1],aw=c[0][1],ay=c[0][2],wy=c[1][2];
  let det=sub(mul(va,vw),mul(aw,aw));assert(det[0]>0n,'singular observable projection');
  let total=div(ay,va),a_to_w=div(aw,va),b_w=div(sub(mul(wy,va),mul(ay,aw)),det),
      b_a=div(sub(mul(ay,vw),mul(wy,aw)),det),prod=mul(a_to_w,b_w);
  assert(str(add(b_a,prod))===str(total),'OLS decomposition');
  let truth={total:String(p[4]+p[3]*p[1]),direct:String(p[4]),indirect:String(p[3]*p[1])};
  let keys=[...joint.keys()].sort(),canonical=keys.map(k=>k+':'+joint.get(k)).join('\n');
  let joint_sha256=crypto.createHash('sha256').update(canonical).digest('hex');
  let result={world,lambda,source_atoms:128,observed_joint_support:joint.size,joint_sha256,
   covariance:c.map(row=>row.map(str)),
   paths:{total:str(total),a_to_w:str(a_to_w),y_on_w_given_a:str(b_w),y_on_a_given_w:str(b_a),proxy_indirect:str(prod),proxy_bias:str(sub(prod,F(truth.indirect)))},truth};
  if(world==='LATENT_CAUSAL_ALIAS'||world==='LATENT_COMMON_ALIAS')aliases[world+':'+lambda]=canonical;
  if(world==='RANDOMIZED_MEDIATED')assert(str(prod)==={0:'1',1:'1/2',2:'1/5',3:'1/10'}[lambda],'mediated preset');
  if(world==='RANDOMIZED_MEDIATOR_CONFOUNDED')assert(str(prod)==={0:'3/2',1:'1',2:'1/2',3:'3/11'}[lambda],'confounded preset');
  results.push(result);
 }
 for(let lambda of [0,1,2,3])assert(aliases['LATENT_CAUSAL_ALIAS:'+lambda]===aliases['LATENT_COMMON_ALIAS:'+lambda],'alias distribution');
 assert(results.length===32,'grid size');
 return {research:'R232_S28',evidence:'E1_ARTIFICIAL',freeze_commit:FREEZE,
 original_source_blob:SOURCE_BLOB,original_source_sha256:SOURCE_SHA,world_count:8,
 lambda_grid:[0,1,2,3],conditions:32,weighted_source_slots:4096,
 observed_joint_alias_preserved:true,rows:results,
 new_human_E2:0,new_historical_E3:0,external_replication:0,CI:'NOT_RUN'};
}
if(require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+'\n');
module.exports={run};
