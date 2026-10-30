#!/usr/bin/env node
"use strict";
/* R293 S89: exact synthetic source enumeration. No third-party dependencies. */
const fs=require("fs"), path=require("path"), assert=require("assert");
const MODES=["INDEPENDENT","OPPOSED_PAIRS"];
const STYLES=["ANCHOR_PLUS","ANCHOR_MINUS"];
const FREEZE="a0a862befbf99ad5e350cdd2ae83aec02df6c2c4";
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){const t=a%b;a=b;b=t;}return a||1;}
function frac(a,b=1){assert(Number.isSafeInteger(a)&&Number.isSafeInteger(b)&&b>0);const g=gcd(a,b);a/=g;b/=g;return b===1?String(a):a+"/"+b;}
function build(){
 const lines=["mode,mechanism,latent_bits,source_probability,shift,latent_values,raw_scores,centered_scores"];
 const worlds=[];
 for(const mode of MODES){
  const n=mode==="INDEPENDENT"?10:5,N=2**n;
  for(const mechanism of STYLES){
   const sr=Array(10).fill(0),sc=Array(10).fill(0);
   const pr=Array.from({length:10},()=>Array(10).fill(0));
   const pc=Array.from({length:10},()=>Array(10).fill(0));
   for(let k=0;k<N;k++){
    const label=k.toString(2).padStart(n,"0");
    const bits=Array.from(label,Number);
    const latent=n===10?bits:bits.concat(bits.map(x=>1-x));
    const shift=mechanism==="ANCHOR_PLUS"?2*bits[0]:2*(1-bits[0]);
    const raw=latent.map(x=>x+shift);
    const total=latent.reduce((a,b)=>a+b,0);
    const cn=latent.map(x=>10*x-total);
    const centered=cn.map(x=>frac(x,10));
    lines.push([mode,mechanism,label,"1/"+N,shift,latent.join(";"),raw.join(";"),centered.join(";")].join(","));
    for(let i=0;i<10;i++){
     sr[i]+=raw[i];sc[i]+=cn[i];
     for(let j=0;j<10;j++){pr[i][j]+=raw[i]*raw[j];pc[i][j]+=cn[i]*cn[j];}
    }
    assert(cn.reduce((a,b)=>a+b,0)===0);
    assert(raw[0]-raw[5]===latent[0]-latent[5]);
   }
   const rawCovNumer=pr.map((row,i)=>row.map((v,j)=>N*v-sr[i]*sr[j]));
   const cenCovNumer=pc.map((row,i)=>row.map((v,j)=>N*v-sc[i]*sc[j]));
   const rawCov=rawCovNumer.map(row=>row.map(v=>frac(v,N*N)));
   const cenCov=cenCovNumer.map(row=>row.map(v=>frac(v,100*N*N)));
   const sq=frac(rawCovNumer[0][5]**2,rawCovNumer[0][0]*rawCovNumer[5][5]);
   const expected=mode==="INDEPENDENT"?"4/5":"1";
   assert.strictEqual(sq,expected);
   for(let i=0;i<10;i++)for(let j=0;j<10;j++){
    const c=mode==="INDEPENDENT"?(i===j?"9/40":"-1/40"):
      (i===j?"1/4":(Math.abs(i-j)===5?"-1/4":"0"));
    assert.strictEqual(cenCov[i][j],c);
   }
   worlds.push({mode,mechanism,source_rows:N,source_mass:"1",
    raw_mean:sr.map(x=>frac(x,N)),centered_mean:sc.map(x=>frac(x,10*N)),
    raw_covariance:rawCov,centered_covariance:cenCov,
    pair_0_5_raw_correlation_squared:sq,pair_0_5_raw_correlation_sign:"positive"});
  }
 }
 const result={research_id:"R293",increment:"S89",freeze_commit:FREEZE,
  scope:"SYNTHETIC_E1_ENDOGENOUS_SHARED_STYLE_NOT_HUMAN_ESS_PVQ21",
  original_R293_baseline:"CLOSED_BOUNDED_E1_UNCHANGED",new_source_rows:2112,
  worlds,empirical_circle_validated:false,new_human_E2:0,new_historical_E3:0,
  R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 return {csv:lines.join("\n")+"\n",json:JSON.stringify(result,null,2)+"\n",result};
}
function check(){
 const o=build();
 assert.strictEqual(o.csv.trimEnd().split("\n").length,2113);
 assert.strictEqual(o.result.worlds.length,4);
 assert(o.result.worlds.every(w=>w.centered_mean.every(x=>x==="0")));
 return o;
}
if(require.main===module){
 const flag=process.argv[2];
 if(flag==="--test"){check();console.log("R293 S89 synthetic exact checks PASS");}
 else if(flag==="--emit"||flag==="--check"){
  const o=check(),dir=__dirname;
  const files=[["R293_S89_ALL_2112_ENDOGENOUS_STYLE_SOURCES.csv",o.csv],["R293_S89_EXACT_RESULTS.json",o.json]];
  if(flag==="--emit"){for(const [name,content] of files)fs.writeFileSync(path.join(dir,name),content,"utf8");}
  else{for(const [name,content] of files)assert.strictEqual(fs.readFileSync(path.join(dir,name),"utf8"),content);}
  console.log("R293 S89 "+flag+" PASS");
 }else{throw new Error("Use --test, --emit or --check");}
}
module.exports={build,check};