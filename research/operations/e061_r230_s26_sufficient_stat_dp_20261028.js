#!/usr/bin/env node
'use strict';
// E061: independently convolve first/second-moment sufficient statistics.
// Usage: node research/operations/e061_r230_s26_sufficient_stat_dp_20261028.js
const fs=require('fs'),path=require('path');
const analyze=function analyze(csv, receipt) {
  const rows=csv.trim().split(/\r?\n/); const cols=rows.shift().split(",");
  const idx=Object.fromEntries(cols.map((x,i)=>[x,i]));
  const worlds=new Map();
  for(const line of rows){
    const a=line.split(","), w=a[idx.world], x=[+a[idx.observed_X1],+a[idx.observed_X2],+a[idx.observed_X3]];
    if(!worlds.has(w))worlds.set(w,[]);
    worlds.get(w).push({x,p:a[idx.original_source_probability]});
  }
  let checks=0; const ok=(v,msg)=>{checks++;if(!v)throw Error(msg)};
  ok(worlds.size===8,"eight worlds");ok(rows.length===256,"256 sources");
  const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
  const fraction=(a,b)=>{a=BigInt(a);b=BigInt(b);const d=gcd(a,b);a/=d;b/=d;return b===1n?String(a):`${a}/${b}`};
  const keys=[[0,0],[0,1],[0,2],[1,1],[1,2],[2,2]];
  const result={};
  for(const [world,source] of worlds){
    ok(source.length===32,world+" source rows");
    ok(source.every(r=>r.p==="1/32"),world+" source weight");
    const hist=new Map();
    for(const {x} of source){const key=x.join(",");const prev=hist.get(key);if(prev)prev.count++;else hist.set(key,{x,count:1});}
    result[world]={};
    for(const n of [2,3]){
      // Convolve sufficient statistics (first moments + six second moments).
      // This aggregates equivalent states at every draw, rather than enumerating ordered tuples.
      let states=new Map([["0,0,0,0,0,0,0,0,0",{s:Array(9).fill(0),weight:1}]]);
      for(let draw=0;draw<n;draw++){
        const next=new Map();
        for(const {s,weight} of states.values())for(const {x,count} of hist.values()){
          const ns=s.slice();
          for(let i=0;i<3;i++)ns[i]+=x[i];
          for(let k=0;k<6;k++){const [i,j]=keys[k];ns[3+k]+=x[i]*x[j];}
          const key=ns.join(",");
          const prev=next.get(key);
          if(prev)prev.weight+=weight*count;else next.set(key,{s:ns,weight:weight*count});
        }
        states=next;
      }
      const rank=[0,0,0], sign=Array.from({length:3},()=>[0,0,0]);
      const sum=Array.from({length:3},()=>Array(3).fill(0));
      let mass=0;
      for(const {s,weight} of states.values()){
        mass+=weight;
        const C=Array.from({length:3},()=>Array(3).fill(0));
        for(let k=0;k<6;k++){const [i,j]=keys[k],v=n*s[3+k]-s[i]*s[j];C[i][j]=v;C[j][i]=v;}
        let r=0;
        if(C.some(a=>a.some(v=>v!==0))){
          r=1;
          for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(C[i][i]*C[j][j]-C[i][j]*C[i][j]>0)r=2;
        }
        rank[r]+=weight;
        for(let i=0;i<3;i++)for(let j=0;j<3;j++)sum[i][j]+=weight*C[i][j];
        for(let k=0;k<3;k++){const [i,j]=[[0,1],[0,2],[1,2]][k],v=C[i][j];sign[k][v<0?0:v>0?2:1]+=weight;}
      }
      const target=receipt.results[world]["n"+n], expected=target.expected_covariance;
      ok(mass===32**n,world+n+" mass");
      for(let k=0;k<3;k++){ok(rank[k]===target.rank_counts[k],world+n+" rank"+k);
        for(let j=0;j<3;j++)ok(sign[k][j]===target.offdiag_sign_counts[k][j],world+n+" sign"+k+j);
      }
      for(let i=0;i<3;i++)for(let j=0;j<3;j++)ok(fraction(sum[i][j],mass*n*n)===expected[i][j],world+n+" moment"+i+j);
      result[world]["n"+n]={mass,rank,sign,unique_sufficient_states:states.size};
    }
  }
  for(const [a,b] of [["ONE_COMMON_TRAIT","COMMON_METHOD_ALIAS"],["CROSS_LOADING","ROTATED_CROSS_ALIAS"]])for(const n of [2,3]){
    ok(JSON.stringify(result[a]["n"+n])===JSON.stringify(result[b]["n"+n]),"alias "+a+n);
  }
  ok(result.NO_COMMON_FACTOR.n2.sign[0][0]===128&&result.NO_COMMON_FACTOR.n2.sign[0][2]===128,"negative control n2");
  ok(result.NO_COMMON_FACTOR.n3.sign[0][0]===9216&&result.NO_COMMON_FACTOR.n3.sign[0][2]===9216,"negative control n3");
  return {checks,failed:0,worlds:worlds.size,source_rows:rows.length,ordered_draws:8*(32**2+32**3),no_common_factor:result.NO_COMMON_FACTOR,method:"dynamic_programming_sufficient_statistic_convolution"};
};
const root=path.resolve(__dirname,'../..');
const csv=fs.readFileSync(path.join(root,'research/R230/R230_ALL_256_ORIGINAL_FACTOR_EXOGENOUS_SOURCES.csv'),'utf8');
const receipt=JSON.parse(fs.readFileSync(path.join(root,'research/validation/R230_S26_FINITE_SAMPLE_EXACT_RECEIPT_2026-10-28.json'),'utf8'));
console.log(JSON.stringify(analyze(csv,receipt),null,2));
