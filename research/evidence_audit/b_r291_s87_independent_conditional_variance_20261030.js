#!/usr/bin/env node
"use strict";
const fs=require("fs"),path=require("path");
const check=function check(csv,jtext){
 const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("denom");if(b<0n){a=-a;b=-b}let x=a<0n?-a:a,y=b;while(y){let t=x%y;x=y;y=t}return [a/x,b/x]};
 const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>add(a,[-b[0],b[1]]),mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]),div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]),str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1],eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],parse=s=>{let z=s.split("/");return Q(z[0],z[1]||1)};
 const zero=Q(0),one=Q(1),keys=["FULL_ANJ","AJ","AN","A"],profs=[["BALANCED",1,1],["ATTITUDE_HEAVY",2,1],["NORM_HEAVY",1,2],["NORM_NULL",2,0]],modes=[["MEDIATED",0],["DIRECT_NORM_STRESS",1]];
 const hdr="world,profile,mode,error_rate,A,N,I,B,J,source_probability,forecast_FULL_ANJ,forecast_AJ,forecast_AN,forecast_A",lines=csv.trimEnd().split("\n");
 if(lines.length!==769||lines[0]!==hdr)throw Error("csv coverage");
 const data=JSON.parse(jtext);if(data.research_id!=="R291_S87"||data.scope!=="INTERNAL_NONBLIND_E1_ARTIFICIAL"||data.source_cells!==768||data.worlds!==24||data.results.length!==24||data.new_human_E2!==0||data.new_historical_E3!==0||data.external_independent_replication!==0||data.R073!=="FROZEN"||data.PESEN_v0_1!=="FROZEN")throw Error("scope");
 const tag=(k,A,N,J)=>k==="FULL_ANJ"?`${A},${N},${J}`:k==="AJ"?`${A},${J}`:k==="AN"?`${A},${N}`:""+A;
 let pos=1,zeros=0,worlds=0;
 for(const [profile,a,n] of profs)for(const [mode,d] of modes)for(const es of ["0","1/4","1/2"]){
  const e=parse(es),world=profile+"__"+mode,maps=Object.fromEntries(keys.map(k=>[k,new Map()]));
  for(const A of [-1,1])for(const N of [-1,1])for(const J of [0,1]){
   const pI=add(Q(1,2),Q(a*A+n*N,8));let mass=zero,success=zero;
   for(const I of [0,1]){
    const w=mul(Q(1,4),mul(I?pI:sub(one,pI),J===I?sub(one,e):e));
    const pB=add(add(Q(1,4),Q(I,2)),Q(d*N,8));
    mass=add(mass,w);success=add(success,mul(w,pB));
   }
   for(const k of keys){const t=tag(k,A,N,J),old=maps[k].get(t)||{m:zero,s:zero};old.m=add(old.m,mass);old.s=add(old.s,success);maps[k].set(t,old)}
  }
  const risks={};for(const k of keys){let r=zero;for(const t of maps[k].values())if(t.m[0]!==0n){const q=div(t.s,t.m);r=add(r,mul(t.m,mul(q,sub(one,q))))}risks[k]=r}
  const seen=new Set();let mass=zero,localZeros=0;
  for(let i=0;i<32;i++){
   const f=lines[pos++].split(",");if(f.length!==14)throw Error("width");
   const [w,p,m,ee,sa,sn,si,sb,sj,sp,...qs]=f;
   const A=Number(sa),N=Number(sn),I=Number(si),B=Number(sb),J=Number(sj);
   if(w!==world||p!==profile||m!==mode||ee!==es||![-1,1].includes(A)||![-1,1].includes(N)||![0,1].includes(I)||![0,1].includes(B)||![0,1].includes(J))throw Error("identity");
   const ident=`${A},${N},${I},${B},${J}`;if(seen.has(ident))throw Error("duplicate");seen.add(ident);
   const pi=add(Q(1,2),Q(a*A+n*N,8)),pb=add(add(Q(1,4),Q(I,2)),Q(d*N,8)),pj=I===J?sub(one,e):e;
   const expect=mul(Q(1,4),mul(I?pi:sub(one,pi),mul(B?pb:sub(one,pb),pj)));
   if(!eq(expect,parse(sp)))throw Error("source mass mismatch");
   mass=add(mass,expect);if(expect[0]===0n)localZeros++;
   for(let k=0;k<4;k++){const t=maps[keys[k]].get(tag(keys[k],A,N,J));const q=t.m[0]===0n?"NA":str(div(t.s,t.m));if(qs[k]!==q)throw Error("forecast mismatch")}
  }
  if(seen.size!==32||!eq(mass,one))throw Error("mass");
  const res=data.results[worlds++];
  if(res.world!==world||res.proxy_flip_rate!==es||res.source_cells!==32||res.source_mass!=="1"||res.zero_mass_cells!==localZeros)throw Error("world metadata");
  for(const k of keys)if(res.risk_brier[k]!==str(risks[k]))throw Error("Brier mismatch");
  for(const [k,r] of [["norm_omission_gap",sub(risks.AJ,risks.FULL_ANJ)],["ignore_proxy_gap",sub(risks.AN,risks.FULL_ANJ)],["ignore_proxy_and_norm_gap",sub(risks.A,risks.FULL_ANJ)]])if(res[k]!==str(r))throw Error("regret mismatch");
  zeros+=localZeros;
 }
 if(pos!==lines.length)throw Error("trailing rows");
 return {status:"PASS",worlds,source_rows:pos-1,zero_mass_rows:zeros,method:"independent conditional variance from 8 by 3 observation kernels"};
};
const root=path.resolve(__dirname,"../validation");
const csv=fs.readFileSync(path.join(root,"R291_S87_ALL_768_PROXY_SOURCE_CELLS.csv"),"utf8");
const json=fs.readFileSync(path.join(root,"R291_S87_EXACT_RESULTS.json"),"utf8");
const modCell=(text,col,val)=>{let lines=text.trimEnd().split("\n");let f=lines[1].split(",");f[col]=val;lines[1]=f.join(",");return lines.join("\n")+"\n"};
const changed=JSON.parse(json);changed.results[1].norm_omission_gap="0";
const controls=[
 ["duplicate",csv.trimEnd()+"\n"+csv.split("\n")[1]+"\n",json],
 ["missing",csv.split("\n").slice(0,-2).join("\n")+"\n",json],
 ["probability",modCell(csv,9,"1/100"),json],
 ["forecast",modCell(csv,10,"0"),json],
 ["result",csv,JSON.stringify(changed)]
];
const out=check(csv,json);
for(const [name,a,b] of controls){let rejected=false;try{check(a,b)}catch(e){rejected=true}if(!rejected)throw Error("mutation survived: "+name)}
console.log(JSON.stringify({...out,mutation_controls:controls.length}));
