#!/usr/bin/env node
'use strict';
const build=function build(){
 const profiles={BALANCED:[1,1,1],CONTROL_HEAVY:[1,1,2],CONTROL_NULL:[1,1,0],NORM_HEAVY:[1,2,1]},eps=[0,1,2],names=["ORACLE_ANC","FULL_ANZ","TRA_AN","CONSTANT"];
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r}return a}
 function q(n,d){n=BigInt(n);d=BigInt(d);if(d<=0n)throw Error("denom");let g=gcd(n,d);return String(n/g)+(d/g===1n?"":"/"+String(d/g))}
 let cols=["world","profile","kappa","epsilon","A","N","C","I","F","Z","B","source_mass","p_intention","p_feasibility","p_Z_given_C","forecast_ORACLE_ANC","forecast_FULL_ANZ","forecast_TRA_AN","forecast_CONSTANT"];
 let rows=[],worlds=[];
 for(let [profile,[a,n,c]] of Object.entries(profiles))for(let k of [0,1])for(let e4 of eps){
  let id=profile+"__K"+k+"__E"+e4,seen=new Set(),mass=0n,positive=0,risk=Object.fromEntries(names.map(x=>[x,0n]));
  for(let A of [-1,1])for(let N of [-1,1])for(let C of [-1,1])for(let I of [0,1])for(let F of [0,1])for(let Z of [-1,1]){
   let s=a*A+n*N+c*C,pi=8+s,pf=2+k*C,pz=Z===C?4-e4:e4;
   let m=(I?pi:16-pi)*(F?pf:4-pf)*pz,B=I*F;
   let tra=64+4*c*k+8*(a*A+n*N),con=64+4*c*k,h=4*(c+4*k)+2*k*(a*A+n*N);
   let p={ORACLE_ANC:tra+2*C*h,FULL_ANZ:tra+(2-e4)*Z*h,TRA_AN:tra,CONSTANT:con};
   if(m<0||Object.values(p).some(x=>x<0||x>256||!Number.isInteger(x)))throw Error("bad probability");
   let key=[A,N,C,I,F,Z].join(":");if(seen.has(key))throw Error("duplicate");seen.add(key);
   mass+=BigInt(m);if(m)positive++;
   for(let f of names)risk[f]+=BigInt(m)*BigInt((256*B-p[f])**2);
   rows.push([id,profile,k,q(e4,4),A,N,C,I,F,Z,B,q(m,2048),q(pi,16),q(pf,4),q(pz,4),...names.map(f=>q(p[f],256))]);
  }
  if(mass!==2048n||seen.size!==64)throw Error("source universe");
  let vnum=BigInt(4*(c+4*k)**2+k*k*(a*a+n*n)),t=2-e4,den=134217728n;
  let gain=risk.TRA_AN-risk.FULL_ANZ,loss=risk.FULL_ANZ-risk.ORACLE_ANC;
  if(gain<0n||loss<0n||risk.CONSTANT<risk.TRA_AN)throw Error("risk order");
  if(gain*16384n!==BigInt(t*t)*vnum*den)throw Error("gain formula");
  if(loss*16384n!==BigInt(4-t*t)*vnum*den)throw Error("loss formula");
  if((risk.CONSTANT-risk.TRA_AN)*1024n!==BigInt(a*a+n*n)*den)throw Error("AN formula");
  if(e4===0&&loss!==0n||e4===2&&gain!==0n||profile==="CONTROL_NULL"&&k===0&&gain!==0n)throw Error("negative controls");
  worlds.push({world:id,profile,kappa:k,epsilon:q(e4,4),cells:64,positive_cells:positive,mass:"1",risk:Object.fromEntries(names.map(f=>[f,q(risk[f],den)])),TRA_minus_FULL_ANZ:q(gain,den),FULL_ANZ_minus_ORACLE:q(loss,den),analytic_control_information:q(vnum,4096)});
 }
 if(rows.length!==1536||worlds.length!==24)throw Error("universe size");
 let nl=String.fromCharCode(10);
 return {csv:cols.join(",")+nl+rows.map(x=>x.join(",")).join(nl)+nl,json:JSON.stringify({research:"R292_S88",scope:"E1_ARTIFICIAL_INTERNAL_NONBLIND",prescore:"R292_S88_NOISY_PERCEIVED_CONTROL_PRESCORE_FREEZE_2026-10-30.md",original_R292:"UNCHANGED_CLOSED_BOUNDED_E1",R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0,world_count:24,source_cells:1536,worlds},null,2)+nl,worlds};
};
if(require.main===module){const fs=require('fs'),path=require('path');let dir=process.argv[2]||process.cwd(),r=build();fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'R292_S88_ALL_1536_NOISY_CONTROL_SOURCE_CELLS.csv'),r.csv);fs.writeFileSync(path.join(dir,'R292_S88_EXACT_RESULTS.json'),r.json);console.log(JSON.stringify({worlds:r.worlds.length,cells:1536,first:r.worlds[0]},null,2));}
module.exports={build};
