#!/usr/bin/env node
'use strict';
const audit=function audit(csv,results,original){
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r}return a}
 function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]}
 function parse(s){let p=String(s).split("/");return Q(p[0],p[1]||1)}
 function add(a,b){return Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
 function sub(a,b){return Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1])}
 function mul(a,b){return Q(a[0]*b[0],a[1]*b[1])}
 function div(a,b){return Q(a[0]*b[1],a[1]*b[0])}
 function eq(a,b){return a[0]===b[0]&&a[1]===b[1]}
 function must(x,msg){if(!x)throw Error(msg)}
 const prof={BALANCED:[1,1,1],CONTROL_HEAVY:[1,1,2],CONTROL_NULL:[1,1,0],NORM_HEAVY:[1,2,1]};
 let lines=csv.trimEnd().split("\n"),cols=lines.shift().split(","),rows=lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[cols[i],v])));
 must(rows.length===1536,"row count");let data=JSON.parse(results),prior=JSON.parse(original);
 must(data.world_count===24&&data.source_cells===1536&&data.scope==="E1_ARTIFICIAL_INTERNAL_NONBLIND","summary metadata");
 let seen=new Set(),grouped=new Map(),count=0;
 for(let r of rows){
  let profile=r.profile,k=Number(r.kappa),[a,n,cc]=prof[profile]||[], e=parse(r.epsilon), e4=Number(div(e,Q(1,4))[0]),A=Number(r.A),N=Number(r.N),C=Number(r.C),I=Number(r.I),F=Number(r.F),Z=Number(r.Z),B=Number(r.B);
  must(a!==undefined&&[0,1].includes(k)&&[0,1,2].includes(e4),"world configuration");
  must(r.world===profile+"__K"+k+"__E"+e4,"world label");
  must([A,N,C,Z].every(x=>x===1||x===-1)&&[I,F,B].every(x=>x===0||x===1),"binary fields");
  must(B===I*F,"behavior gate");
  let key=[r.world,A,N,C,I,F,Z].join("|");must(!seen.has(key),"duplicate source");seen.add(key);
  let pi=Q(8+a*A+n*N+cc*C,16),pf=Q(2+k*C,4),pz=Q(Z===C?4-e4:e4,4);
  must(eq(parse(r.p_intention),pi)&&eq(parse(r.p_feasibility),pf)&&eq(parse(r.p_Z_given_C),pz),"conditional factor");
  let expected=mul(mul(mul(Q(1,8),I?pi:sub(Q(1),pi)),F?pf:sub(Q(1),pf)),pz);
  must(eq(parse(r.source_mass),expected),"source factor");
  let m=div(expected,Q(1,2048));must(m[1]===1n,"noninteger source mass");
  if(!grouped.has(r.world))grouped.set(r.world,{rows:[],total:0n,positive:0});
  let g=grouped.get(r.world);g.rows.push({...r,A,N,C,I,F,Z,B,m:m[0]});g.total+=m[0];if(m[0])g.positive++;count++;
 }
 must(seen.size===1536&&grouped.size===24,"source coverage");
 let checked=0,control=0,summary=new Map(data.worlds.map(w=>[w.world,w]));must(summary.size===24,"summary duplicate");
 let originalMap=new Map(prior.worlds.map(w=>[w.world,w]));
 for(let [world,g] of grouped){
  must(g.rows.length===64&&g.total===2048n,"per-world mass");
  let w=summary.get(world);must(w&&w.cells===64&&w.positive_cells===g.positive&&w.mass==="1","world summary");
  let forecasts=[["ORACLE_ANC",r=>[r.A,r.N,r.C]],["FULL_ANZ",r=>[r.A,r.N,r.Z]],["TRA_AN",r=>[r.A,r.N]],["CONSTANT",r=>[]]];
  let calc={};
  for(let [name,fn] of forecasts){
   let bins=new Map();
   for(let r of g.rows){let key=fn(r).join(","),b=bins.get(key)||{m:0n,y:0n};b.m+=r.m;b.y+=r.m*BigInt(r.B);bins.set(key,b)}
   let loss=Q(0);
   for(let b of bins.values())if(b.m){loss=add(loss,sub(Q(b.y),Q(b.y*b.y,b.m)))}
   loss=div(loss,Q(2048));calc[name]=loss;
   for(let r of g.rows){let b=bins.get(fn(r).join(","));if(b.m){must(eq(parse(r["forecast_"+name]),Q(b.y,b.m)),"forecast conditional mismatch "+world+" "+name);checked++}}
   must(eq(loss,parse(w.risk[name])),"risk mismatch "+world+" "+name);
  }
  must(eq(sub(calc.TRA_AN,calc.FULL_ANZ),parse(w.TRA_minus_FULL_ANZ)),"gain mismatch");
  must(eq(sub(calc.FULL_ANZ,calc.ORACLE_ANC),parse(w.FULL_ANZ_minus_ORACLE)),"loss mismatch");
  let [profile,kstr,estr]=world.split("__"),k=Number(kstr.slice(1)),e4=Number(estr.slice(1)),[a,n,cc]=prof[profile];
  let V=add(Q((cc+4*k)**2,1024),Q(k*k*(a*a+n*n),4096));
  must(eq(V,parse(w.analytic_control_information)),"analytic info mismatch");
  must(eq(sub(calc.TRA_AN,calc.FULL_ANZ),mul(Q((2-e4)**2,4),V)),"analytic noisy gain mismatch");
  if(e4===0){
   let prev=originalMap.get(profile+"__"+(k?"INFORMATIVE":"UNINFORMATIVE"));
   must(prev&&eq(calc.ORACLE_ANC,parse(prev.Brier_risk.FULL_ANC))&&eq(calc.TRA_AN,parse(prev.Brier_risk.TRA_AN)),"original R292 baseline mismatch");control++;
  }
 }
 return {status:"PASS",cells:count,worlds:grouped.size,conditional_forecast_cells_checked:checked,original_R292_baselines:control,scope:"INTERNAL_NONBLIND_E1",new_E2:0,new_E3:0};
};
if(require.main===module){const fs=require('fs'),args=process.argv.slice(2);if(args.length!==3)throw Error('usage: node audit.js sources.csv results.json original_R292_results.json');console.log(JSON.stringify(audit(...args.map(p=>fs.readFileSync(p,'utf8'))),null,2));}
module.exports={audit};
