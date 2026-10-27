#!/usr/bin/env node
'use strict';
// Usage: node script.js R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv R215_S11_36_CONDITION_EXACT.csv
const fs=require('node:fs');
const [sourcePath,receiptPath]=process.argv.slice(2);
if(!sourcePath||!receiptPath){console.error('Two CSV paths required');process.exit(2);}
function rows(path){
 const lines=fs.readFileSync(path,'utf8').trim().split(/\r?\n/);
 const header=lines.shift().split(',');
 return lines.map(line=>{const vals=line.split(',');if(vals.length!==header.length)throw Error('CSV width');return Object.fromEntries(vals.map((v,i)=>[header[i],v]));});
}
const source=rows(sourcePath),receipt=rows(receiptPath);
const abs=n=>n<0n?-n:n;
const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b];}return a||1n;};
const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];};
const sub=(x,y)=>Q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
const eq=(x,y)=>x[0]*y[1]===y[0]*x[1];
const parse=v=>{const [n,d]=v.split('/');return Q(n,d||'1');};
const show=x=>x[1]===1n?x[0].toString():x[0]+'/'+x[1];
let checks=0;
function check(ok,label){checks++;if(!ok)throw Error('Failed '+label);}
const worlds={};
for(const row of source){
 const y=row.actual_six_observed_group_period_means.split('|').map(Number);
 check(y.length===6&&y.every(Number.isInteger),'six observed integers');
 const [tm,t0,tp,cm,c0,cp]=y;
 const D=(tp-cp)-(t0-c0),P=(t0-c0)-(tm-cm),C=D-P;
 const tau=Number(row.true_treated_post_ATT_FOR_AUDIT_ONLY);
 check(D===Number(row.STANDARD_DID_estimate),'D');
 check(P===Number(row.PRE_TREND_PLACEBO_estimate),'P');
 check(C===Number(row.LINEAR_PRETREND_CORRECTED_estimate),'C');
 check((D-tau)**2===Number(row.STANDARD_DID_squared_error_to_true_ATT),'D loss');
 check((C-tau)**2===Number(row.LINEAR_PRETREND_CORRECTED_squared_error_to_true_ATT),'C loss');
 check(row.original_source_probability==='1/64','source probability');
 (worlds[row.world]??=[]).push({D,P,C,tau});
}
const signs={increase:0,decrease:0,equal:0,meanShift:0},examples=[];
for(const row of receipt){
 const all=worlds[row.world],h=Number(row.h);
 const selected=all.filter(x=>Math.abs(x.P)<=h);
 check(all.length===64,'world size');
 check(selected.length===Number(row.accept_n),'accepted count');
 for(const name of ['D','C']){
  const n=BigInt(selected.length);
  const sum=selected.reduce((v,x)=>v+BigInt(x[name]),0n);
  const sumsq=selected.reduce((v,x)=>v+BigInt(x[name]*x[name]),0n);
  const loss=selected.reduce((v,x)=>v+BigInt((x[name]-x.tau)**2),0n);
  const mean=Q(sum,n),variance=sub(Q(sumsq,n),mul(mean,mean)),mse=Q(loss,n);
  const fullMse=Q(all.reduce((v,x)=>v+BigInt((x[name]-x.tau)**2),0n),64n);
  check(eq(mean,parse(row[name+'_mean'])),'mean');
  check(eq(variance,parse(row[name+'_var'])),'variance');
  check(eq(mse,parse(row[name+'_mse'])),'MSE');
  check(eq(sub(mse,fullMse),parse(row[name+'_mse_delta'])),'MSE delta');
  if(name==='D'){
   const delta=sub(mse,fullMse);
   if(delta[0]>0n)signs.increase++;else if(delta[0]<0n)signs.decrease++;else signs.equal++;
   const fullMean=Q(all.reduce((v,x)=>v+BigInt(x.D),0n),64n);
   if(!eq(mean,fullMean))signs.meanShift++;
   if(h===1&&['PARALLEL_NULL','DIFFERENTIAL_SLOPE_FALSE','LARGE_DIFF_SLOPE'].includes(row.world))examples.push({world:row.world,accepted:selected.length,mean:show(mean),mse:show(mse),delta:show(delta)});
  }
 }
}
if(source.length!==768||Object.keys(worlds).length!==12||receipt.length!==36)throw Error('Unexpected archive sizes');
if(checks!==5736)throw Error('Unexpected assertion count '+checks);
console.log(JSON.stringify({checks,failed:0,source_rows:source.length,receipt_rows:receipt.length,signs,examples}));
