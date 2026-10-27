#!/usr/bin/env node
/* E057 source-first exact R226 S22 check, no dependencies or network calls.
Usage: node e057_r226_s22_source_1250_20261028.js original.csv receipt.json */
'use strict';
const fs=require('node:fs');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}if(d===0n)return null;const g=gcd(n,d);return d/g===1n?String(n/g):String(n/g)+'/'+String(d/g);}
function verify(csv,receipt){
 let checks=0,cellChecks=0;
 function check(ok,why){checks++;if(!ok)throw new Error('FAIL '+why);}
 const lines=csv.trim().split(/\r?\n/),header=lines.shift().split(','),worlds=new Map();
 for(const line of lines){const p=line.split(','),row=Object.fromEntries(header.map((h,i)=>[h,p[i]]));check(row.original_probability==='1/16','source mass');if(!worlds.has(row.world))worlds.set(row.world,[]);worlds.get(row.world).push(row);}
 check(worlds.size===8,'world count');check(receipt.rows.length===40,'receipt count');
 for(const r of receipt.rows){
  const original=worlds.get(r.world);check(!!original&&original.length===16,'world source count');
  const [num,den]=r.p.includes('/')?r.p.split('/').map(BigInt):[BigInt(r.p),1n],k=Number(8n*num/den);
  check(8n*num%den===0n,'eighths');check([0,1,2,3,4].includes(k),'p grid');
  const mass=new Map();let total=0n,edge=0n,discord=0n,doAll=0n,doEdge=0n;
  const gm=[0n,0n],gy=[0n,0n],rm=[0n,0n],ry=[0n,0n];
  for(const src of original){
   const E=Number(src.observed_edge_E),A=Number(src.observed_sender_A0),B0=Number(src.observed_receiver_B0),B1=Number(src.observed_receiver_B1),R=Number(src.external_random_R),eff=Number(src.oracle_B1_doA1)-Number(src.oracle_B1_doA0);
   doAll+=BigInt(eff)*8n;
   for(let t=0;t<2;t++){
    const w=BigInt(t?k:8-k),as=A^t,key=''+E+as+B0+B1;
    mass.set(key,(mass.get(key)||0n)+w);total+=w;
    if(E){edge+=w;if(as!==B0)discord+=w;gm[as]+=w;gy[as]+=w*BigInt(B1);rm[R]+=w;ry[R]+=w*BigInt(B1);doEdge+=w*BigInt(eff);}
   }
  }
  check(total===128n,'total mass');check(r.source_slots===32,'slots');
  check(frac(edge,128n)===r.connected_probability,'edge');
  check(frac(discord,edge)===r.observed_discordance_given_edge,'discordance');
  const contrast=gm[0]&&gm[1]?frac(gy[1]*gm[0]-gy[0]*gm[1],gm[1]*gm[0]):null;
  check(contrast===r.observed_peer_contrast,'contrast');
  check(frac(doAll,128n)===r.true_population_doA_effect,'population oracle');
  check(frac(doEdge,edge)===r.true_connected_doA_effect,'connected oracle');
  if(contrast!==null){const [n1,d1=1n]=contrast.split('/').map(BigInt),[n2,d2=1n]=r.true_connected_doA_effect.split('/').map(BigInt);check(frac(n1*d2-n2*d1,d1*d2)===r.observed_minus_true_connected,'bias');}
  else check(r.observed_minus_true_connected===null,'null bias');
  const randomized=['RANDOMIZED_PEER_COPY','RANDOMIZED_NO_COPY','RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK'].includes(r.world);
  const rc=randomized&&rm[0]&&rm[1]?frac(ry[1]*rm[0]-ry[0]*rm[1],rm[1]*rm[0]):null;
  check(rc===r.randomized_assignment_contrast,'randomization');
  for(let i=0;i<16;i++){const key=i.toString(2).padStart(4,'0');check(frac(mass.get(key)||0n,128n)===(r.observation_signature[key]??'0'),'joint '+r.world+' '+r.p+' '+key);cellChecks++;}
 }
 return {status:'PASS',checks,source_rows:lines.length,receipt_rows:receipt.rows.length,joint_cell_checks:cellChecks,failures:0};
}
if(require.main===module){if(process.argv.length!==4){console.error('Usage: node e057_r226_s22_source_1250_20261028.js original.csv receipt.json');process.exit(2);}console.log(JSON.stringify(verify(fs.readFileSync(process.argv[2],'utf8'),JSON.parse(fs.readFileSync(process.argv[3],'utf8')))));}
module.exports={verify};
