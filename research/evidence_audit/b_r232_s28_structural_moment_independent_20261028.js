#!/usr/bin/env node
'use strict';
// Independent coefficient-vector covariance oracle; no CSV/source enumeration.
// Run at repo root: node research/evidence_audit/b_r232_s28_structural_moment_independent_20261028.js research/validation/R232_S28_PROXY_NOISE_RECEIPT_2026-10-28.json
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const WORLDS={
 RANDOMIZED_MEDIATED:['R',1,0,1,0,0,0],RANDOMIZED_NULL:['R',0,1,1,0,0,0],
 LATENT_CAUSAL_ALIAS:['U',1,0,1,0,0,0],LATENT_COMMON_ALIAS:['U',0,1,1,0,0,0],
 RANDOMIZED_DIRECT_AND_MEDIATED:['R',1,0,1,1,0,0],
 RANDOMIZED_MEDIATOR_CONFOUNDED:['R',1,1,1,0,1,0],
 RANDOMIZED_DIRECT_ONLY:['R',0,1,1,1,0,0],
 RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR:['R',1,0,1,0,0,1]
};
const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}
 let a=n<0n?-n:n,b=d;while(b){let t=a%b;a=b;b=t;}return [n/a,d/a];};
const add=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const sub=(x,y)=>F(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>F(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>F(x[0]*y[1],x[1]*y[0]);
const str=x=>x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1]);
function assertEqual(actual,expected,label){if(actual!==expected)throw Error('AUDIT_MISMATCH '+label+' expected='+expected+' actual='+actual);}
function independent(world,lambda){let p=WORLDS[world];if(!p)throw Error('unknown world');
 const e=(i)=>Array.from({length:7},(_,j)=>Number(i===j));
 const u=e(0),r=e(1),em=e(2),ey=e(3),ew=e(4),ez1=e(5),ez2=e(6);
 const A=p[0]==='R'?r:u;
 const plus=(...terms)=>Array.from({length:7},(_,j)=>terms.reduce((s,[v,x])=>s+v*x[j],0));
 const M=plus([p[1],A],[p[2],u],[1,em]);
 const Y=plus([p[3],M],[p[4],A],[p[5],u],[1,ey]);
 const W=plus([1,M],[p[6]+lambda,ew]);
 const X=[A,W,Y,plus([1,u],[1,ez1]),plus([1,u],[1,ez2])];
 const C=X.map(x=>X.map(y=>x.reduce((s,v,i)=>s+v*y[i],0)));
 const va=F(C[0][0]),vw=F(C[1][1]),aw=F(C[0][1]),ay=F(C[0][2]),wy=F(C[1][2]);
 const det=sub(mul(va,vw),mul(aw,aw));
 const total=div(ay,va),a_to_w=div(aw,va),bw=div(sub(mul(wy,va),mul(ay,aw)),det),ba=div(sub(mul(ay,vw),mul(wy,aw)),det),prod=mul(a_to_w,bw);
 return {covariance:C.map(row=>row.map(String)),paths:{total:str(total),a_to_w:str(a_to_w),y_on_w_given_a:str(bw),y_on_a_given_w:str(ba),proxy_indirect:str(prod),proxy_bias:str(sub(prod,F(p[3]*p[1])))},truth:{total:String(p[4]+p[3]*p[1]),direct:String(p[4]),indirect:String(p[3]*p[1])}};
}
function audit(receipt){assertEqual(receipt.research,'R232_S28','research');assertEqual(receipt.rows.length,32,'conditions');let comparisons=0;
 for(let row of receipt.rows){let ref=independent(row.world,row.lambda);
  for(let i=0;i<5;i++)for(let j=0;j<5;j++){assertEqual(row.covariance[i][j],ref.covariance[i][j],row.world+'/'+row.lambda+'/cov/'+i+'/'+j);comparisons++;}
  for(let [k,v] of Object.entries(ref.paths)){assertEqual(row.paths[k],v,row.world+'/'+row.lambda+'/'+k);comparisons++;}
  for(let [k,v] of Object.entries(ref.truth)){assertEqual(row.truth[k],v,row.world+'/'+row.lambda+'/truth/'+k);comparisons++;}
 }
 return comparisons;
}
function main(){let input=process.argv[2]||'research/validation/R232_S28_PROXY_NOISE_RECEIPT_2026-10-28.json';
 let receipt=JSON.parse(fs.readFileSync(path.resolve(ROOT,input),'utf8'));
 let comparisons=audit(receipt),tampered=JSON.parse(JSON.stringify(receipt));tampered.rows[0].paths.proxy_indirect='999';let detected=false;
 try{audit(tampered);}catch(e){detected=/AUDIT_MISMATCH/.test(e.message);}if(!detected)throw Error('negative control failed');
 process.stdout.write(JSON.stringify({research:'R232_S28',evidence:'E1_ARTIFICIAL',independent_method:'SEVEN_EXOGENOUS_COEFFICIENT_DOT_PRODUCTS',conditions:32,exact_comparisons:comparisons,failures:0,mutation_detected:true,external_replication:0,CI:'NOT_RUN'},null,2)+'\n');
}
if(require.main===module)main();module.exports={audit,independent};
