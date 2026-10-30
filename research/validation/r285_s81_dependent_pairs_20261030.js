#!/usr/bin/env node
"use strict";
// R285 S81 exact E1 enumeration; prescore freeze b2ba179a and erratum 1f10fb34.
const regimes={BOTH_NULL:[4,4],ONE_SIGNAL:[6,4]},modes=["INDEPENDENT","COMONOTONE","COUNTERMONOTONE"],policies=["RAW_UNADJUSTED","HOLM_FWER","BH_FDR"],p=[16,15,11,5,1];
function gcd(a,b){while(b){let c=a%b;a=b;b=c;}return a;}
function F(a,b=1){if(!a)return"0";let g=gcd(a,b);return b===g?String(a/g):a/g+"/"+b/g;}
function q(reg,mode){let[a,b]=regimes[reg],both=mode==="INDEPENDENT"?a*b/8:mode==="COMONOTONE"?Math.min(a,b):Math.max(0,a+b-8);return[8-a-b+both,b-both,a-both,both];}
function choice(k,l,policy){
 if(policy==="RAW_UNADJUSTED")return[+(k>=3),+(l>=3)];
 if(policy==="HOLM_FWER"){let both=(k===4&&l>=3)||(l===4&&k>=3);return[both?1:+(k===4),both?1:+(l===4)];}
 if(policy==="BH_FDR"){let both=k>=3&&l>=3;return[both?1:+(k===4),both?1:+(l===4)];}
 throw Error("policy");
}
function atom(reg,mode,policy,i){
 let weights=q(reg,mode),n=i,w=1,k=0,l=0,seq=[];
 for(let t=0;t<4;t++){let d=n%4;n=Math.floor(n/4);k+=(d>>1)&1;l+=d&1;w*=weights[d];seq.push(((d>>1)&1)+""+(d&1));}
 let mask=choice(k,l,policy),R=mask[0]+mask[1],V=(reg==="BOTH_NULL"?mask[0]:0)+mask[1],S=R-V;
 return {regime:reg,coupling:mode,policy,source_index:i,four_ordered_pairs:seq.join(" "),K1:k,K2:l,weight_num:w,weight_den:4096,pvalue_H1:F(p[k],16),pvalue_H2:F(p[l],16),reject_H1:mask[0],reject_H2:mask[1],R,V,S,FDP:F(V,Math.max(R,1)),FWER:+(V>0)};
}
function aggregate(rows){
 let mass=0,fw=0,fd2=0,v=0,s=0,r=0,z=0;
 for(let x of rows){let w=x.weight_num;mass+=w;fw+=w*x.FWER;fd2+=w*(x.R?2*x.V/x.R:0);v+=w*x.V;s+=w*x.S;r+=w*x.R;z+=w*+(x.R===0);}
 if(mass!==4096||!Number.isInteger(fd2))throw Error("source mass");
 return {FWER:F(fw,4096),FDR:F(fd2,8192),EV:F(v,4096),ES:F(s,4096),ER:F(r,4096),P_R0:F(z,4096)};
}
const baseline={
"BOTH_NULL|RAW_UNADJUSTED":"135/256|135/256|5/8|0|5/8",
"BOTH_NULL|HOLM_FWER":"31/256|31/256|5/32|0|5/32",
"BOTH_NULL|BH_FDR":"47/256|47/256|9/32|0|9/32",
"ONE_SIGNAL|RAW_UNADJUSTED":"5/16|1615/8192|5/16|189/256|269/256",
"ONE_SIGNAL|HOLM_FWER":"145/1024|647/8192|145/1024|351/1024|31/64",
"ONE_SIGNAL|BH_FDR":"253/1024|1079/8192|253/1024|459/1024|89/128"};
const columns=["regime","coupling","policy","source_index","four_ordered_pairs","K1","K2","weight_num","weight_den","pvalue_H1","pvalue_H2","reject_H1","reject_H2","R","V","S","FDP","FWER"];
function compute(){
 let rows=[],results=[];
 for(let reg of Object.keys(regimes))for(let mode of modes)for(let pol of policies){
  let group=Array.from({length:256},(_,i)=>atom(reg,mode,pol,i)),a=aggregate(group);
  if(mode==="INDEPENDENT"&&[a.FWER,a.FDR,a.EV,a.ES,a.ER].join("|")!==baseline[reg+"|"+pol])throw Error("R285 original baseline");
  if(reg==="BOTH_NULL"&&a.FWER!==a.FDR)throw Error("all null");
  rows.push(...group);results.push({regime:reg,coupling:mode,policy:pol,...a});
 }
 let receipt={research:"R285_S81",scope:"E1_ARTIFICIAL_NONBLIND",freeze_commit:"b2ba179ae4bc6fe24c45e2e1dc963d25e7aa82e8",prescore_erratum_commit:"1f10fb34fae9185cca20cbcfe64f6b0de6c409a2",original_R285:"UNCHANGED",source_rows:4608,world_policy_groups:18,zero_mass_rows:rows.filter(x=>!x.weight_num).length,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0,original_independent_baseline_match:true,results};
 let csv=columns.join(",")+"\n"+rows.map(x=>columns.map(k=>String(x[k])).join(",")).join("\n")+"\n";
 return {rows,receipt,csv,json:JSON.stringify(receipt,null,2)+"\n"};
}
function validate(rows,receipt){
 if(receipt.scope!=="E1_ARTIFICIAL_NONBLIND"||receipt.R073!=="FROZEN"||receipt.PESEN_v0_1!=="FROZEN"||rows.length!==4608||receipt.results.length!==18)throw Error("scope/count");
 let pos=0,g=0;
 for(let reg of Object.keys(regimes))for(let mode of modes)for(let pol of policies){
  let group=[];
  for(let i=0;i<256;i++){let expected=atom(reg,mode,pol,i),actual=rows[pos++];if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error("row "+pos);group.push(actual);}
  let expected={regime:reg,coupling:mode,policy:pol,...aggregate(group)};
  if(JSON.stringify(expected)!==JSON.stringify(receipt.results[g++]))throw Error("receipt");
 }
 return true;
}
function mutationTests(base){
 let tests=[];
 function reject(name,change){let rows=base.rows.map(x=>({...x})),rec=JSON.parse(JSON.stringify(base.receipt));change(rows,rec);let bad=false;try{validate(rows,rec);}catch(e){bad=true;}if(!bad)throw Error("accepted mutant "+name);tests.push(name);}
 reject("duplicate",r=>r.push({...r[0]}));reject("missing",r=>r.pop());
 reject("weight",r=>r[0].weight_num++);reject("decision",r=>r[0].reject_H1=1-r[0].reject_H1);
 reject("FDP",r=>r[0].FDP="999");reject("scope",(r,o)=>o.scope="E3_HISTORICAL");
 reject("aggregate",(r,o)=>o.results[0].FWER="999");
 reject("zero_mass_omission",r=>r.splice(r.findIndex(x=>x.weight_num===0),1));
 return tests;
}
if(typeof module!=="undefined")module.exports={compute,validate,mutationTests};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 let fs=require("fs"),path=require("path"),out=compute();validate(out.rows,out.receipt);mutationTests(out);
 if(process.argv[2]==="--emit"){let dir=process.argv[3]||".";fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,"R285_S81_ALL_4608_SOURCES.csv"),out.csv);fs.writeFileSync(path.join(dir,"R285_S81_EXACT_RESULTS.json"),out.json);}
 console.log(JSON.stringify({rows:out.rows.length,groups:out.receipt.results.length,mutants:8}));
}
