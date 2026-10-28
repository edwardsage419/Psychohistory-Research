#!/usr/bin/env node
'use strict';
// R230 S26: exact integer enumeration, independent histogram and pairwise-difference audit.
// Usage: node research/validation/r230_s26_finite_sample_exact_20261028.js
const fs=require('fs'),path=require('path');
function analyze(csv,original){
  const rows=csv.trim().split(/\r?\n/),fields=rows.shift().split(",");
  const data=rows.map(s=>{const p=s.split(",");const o=Object.fromEntries(fields.map((f,i)=>[f,p[i]]));return {w:o.world,x:[+o.observed_X1,+o.observed_X2,+o.observed_X3],p:o.original_source_probability}});
  const worlds=[...new Set(data.map(x=>x.w))], out={};
  if(data.length!==256||worlds.length!==8)throw Error("source universe changed");
  const org=new Map(original.world_results.map(x=>[x.world,x]));
  let checks=0;
  function ok(test,msg){checks++;if(!test)throw Error("check "+msg);}
  const gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a);
  function frac(a,b){const d=gcd(a,b);return (a/d)+(b/d===1?"":"/"+b/d)}
  function statR(x,n){let s=[0,0,0],p=Array.from({length:3},()=>[0,0,0]);for(const v of x){for(let i=0;i<3;i++){s[i]+=v[i];for(let j=0;j<3;j++)p[i][j]+=v[i]*v[j]}}
    let c=p.map((r,i)=>r.map((v,j)=>n*v-s[i]*s[j]));let rank=0;
    if(n===2){rank=x[0].some((v,i)=>v!==x[1][i])?1:0}
    else{const a=x[1].map((v,i)=>v-x[0][i]),b=x[2].map((v,i)=>v-x[0][i]);const cross=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];rank=cross.some(v=>v!==0)?2:(a.some(v=>v!==0)||b.some(v=>v!==0)?1:0)}
    return {c,rank};
  }
  function statB(x,n){let c=Array.from({length:3},()=>[0,0,0]);for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let i=0;i<3;i++)for(let j=0;j<3;j++)c[i][j]+=(x[a][i]-x[b][i])*(x[a][j]-x[b][j]);
    let rank=0;if(c.some(r=>r.some(v=>v!==0))){rank=1;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(c[i][i]*c[j][j]-c[i][j]*c[j][i]>0)rank=2;}
    return {c,rank};
  }
  function fresh(){return {rank:[0,0,0],sign:Array.from({length:3},()=>[0,0,0]),sum:Array.from({length:3},()=>[0,0,0]),mass:0}}
  function add(a,st,weight){a.mass+=weight;a.rank[st.rank]+=weight;for(let i=0;i<3;i++)for(let j=0;j<3;j++)a.sum[i][j]+=st.c[i][j]*weight;for(let k=0;k<3;k++){const [i,j]=[[0,1],[0,2],[1,2]][k],v=st.c[i][j];a.sign[k][v<0?0:v===0?1:2]+=weight}}
  for(const w of worlds){const src=data.filter(x=>x.w===w);ok(src.length===32,w+" size");ok(src.every(x=>x.p==="1/32"),w+" weights");const o=org.get(w);ok(!!o,w+" original receipt");
    const hist=new Map();for(const s of src){let k=s.x.join(",");let h=hist.get(k);if(h)h.freq++;else hist.set(k,{x:s.x,freq:1})}
    const u=[...hist.values()];
    out[w]={unique_observed_vectors:u.length};
    for(const n of [2,3]){
      const a=fresh(),b=fresh(),mass=32**n;
      for(let i=0;i<32;i++)for(let j=0;j<32;j++){if(n===2)add(a,statR([src[i].x,src[j].x],n),1);else for(let k=0;k<32;k++)add(a,statR([src[i].x,src[j].x,src[k].x],n),1)}
      for(let i=0;i<u.length;i++)for(let j=i;j<u.length;j++){if(n===2){add(b,statB([u[i].x,u[j].x],n),u[i].freq*u[j].freq*(i===j?1:2))}else for(let k=j;k<u.length;k++){const mult=i===j&&j===k?1:(i===j||j===k?3:6);add(b,statB([u[i].x,u[j].x,u[k].x],n),u[i].freq*u[j].freq*u[k].freq*mult)}}
      ok(a.mass===mass,w+n+" R mass");ok(b.mass===mass,w+n+" B mass");
      for(let i=0;i<3;i++){ok(a.rank[i]===b.rank[i],w+n+" rank"+i);for(let j=0;j<3;j++){ok(a.sum[i][j]===b.sum[i][j],w+n+" moment"+i+j);const sigma=Number(o.exact_population_covariance[i][j]);ok(a.sum[i][j]*n===sigma*(n-1)*mass*n*n,w+n+" covariance identity"+i+j);ok(a.sign[i][j]===b.sign[i][j],w+n+" sign"+i+j)}}
      ok(a.rank.slice(n).every(v=>v===0),w+n+" rank bound");
      out[w]["n"+n]={ordered_draws:mass,rank_counts:a.rank,offdiag_sign_counts:a.sign,expected_covariance:a.sum.map(r=>r.map(v=>frac(v,mass*n*n)))};
    }
  }
  for(const [w,v] of [["ONE_COMMON_TRAIT","COMMON_METHOD_ALIAS"],["CROSS_LOADING","ROTATED_CROSS_ALIAS"]])for(const n of [2,3]){ok(JSON.stringify(out[w]["n"+n])===JSON.stringify(out[v]["n"+n]),"alias "+w+n)}
  ok(out.NO_COMMON_FACTOR.n2.offdiag_sign_counts.some(s=>s[0]>0&&s[2]>0),"negative control");
  const receipt={research_id:"R230_S26",scope:"E1_FINITE_ARTIFICIAL_ONLY",source_rows:256,worlds:8,sample_sizes:[2,3],ordered_source_sequences:8*(32**2+32**3),method_R:"ordered_original_source_enumeration_integer_centering",method_B:"unordered_observed_histogram_multinomial_pairwise_difference",checks_passed:checks,checks_failed:0,external_replications:0,E2:0,E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",results:out};
  return receipt;
}
const root=path.resolve(__dirname,'../..');
const csv=fs.readFileSync(path.join(root,'research/R230/R230_ALL_256_ORIGINAL_FACTOR_EXOGENOUS_SOURCES.csv'),'utf8');
const original=JSON.parse(fs.readFileSync(path.join(root,'research/R230/R230_EXACT_RESULTS.json'),'utf8'));
console.log(JSON.stringify(analyze(csv,original),null,2));
