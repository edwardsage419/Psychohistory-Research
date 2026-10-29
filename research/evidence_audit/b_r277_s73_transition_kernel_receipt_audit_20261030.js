#!/usr/bin/env node
"use strict";
// Independent R277 S73 receipt validator. Analytic two-step Markov kernel.
const M=["ANTIPERSISTENT","IID_FAIR","PERSISTENT"],S=[1,2,3];
const W={A_ADJACENT:[0,1,2],B_ODD:[0,2,4],C_EVEN:[1,3,5]};
const Y=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0"));
function gcd(a,b){while(b){const t=a%b;a=b;b=t}return a}
function f(a,b){const g=gcd(a,b);return b/g===1?String(a/g):String(a/g)+"/"+String(b/g)}
function mass(w,m,y){
 const s=S[m],p=W[w];let n=1,d=2;
 for(let i=0;i<2;i++){
  const gap=p[i+1]-p[i],q=gap===1?s:s*s+(4-s)*(4-s),den=gap===1?4:16;
  n*=y[i]===y[i+1]?q:den-q;d*=den;
 }
 const z=2048*n/d;if(!Number.isInteger(z))throw Error("noninteger mass");return z;
}
function validate(r,csv){
 if(r.evidence!=="EXPLORATORY_E1_NONBLIND_INTERNAL"||r.E2_predictions!==0||r.E3_predictions!==0||r.external_replication!==false)throw Error("evidence");
 if(r.source_count!==192||r.observable_rows!==72||r.original_R277_freeze!=="923a161bbdc012c138e53f1fa316e6085ff2704e")throw Error("source identity");
 if(Object.keys(r.windows).join(",")!==Object.keys(W).join(","))throw Error("windows");
 for(const w of Object.keys(W)){
  const z=r.windows[w],map={};
  for(const y of Y){
   let winner=0;for(let j=1;j<3;j++)if(mass(w,j,y)>mass(w,winner,y))winner=j;
   map[y]=M[winner];if(z.map[y]!==map[y])throw Error("MAP");
  }
  for(let m=0;m<3;m++){
   let total=0;for(const y of Y){const v=mass(w,m,y);total+=v;if(z.observation_probability[M[m]][y]!==f(v,2048))throw Error("probability")}
   if(total!==2048)throw Error("normalization");
   for(let j=0;j<3;j++){const v=Y.filter(y=>map[y]===M[j]).reduce((a,y)=>a+mass(w,m,y),0);if(z.confusion[M[m]][M[j]]!==f(v,2048))throw Error("confusion")}
  }
  const correct=M.reduce((a,m,i)=>a+Y.filter(y=>map[y]===m).reduce((b,y)=>b+mass(w,i,y),0),0);
  if(z.macro_accuracy!==f(correct,6144))throw Error("macro");
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const v=Y.reduce((a,y)=>a+Math.abs(mass(w,i,y)-mass(w,j,y)),0);if(z.tv[M[i]+"|"+M[j]]!==f(v,4096))throw Error("TV")}
 }
 const lines=csv.trimEnd().split("\n");
 if(lines.length!==73||lines[0]!=="window,true_model,observed_three_bits,exact_mass,numerator_over_2048")throw Error("CSV coverage");
 const seen=new Set();
 for(const line of lines.slice(1)){
  const [w,m,y,p,n]=line.split(","),key=w+"|"+m+"|"+y;
  if(!W[w]||!M.includes(m)||!Y.includes(y)||seen.has(key))throw Error("CSV key");
  seen.add(key);const v=mass(w,M.indexOf(m),y);
  if(p!==f(v,2048)||n!==String(v))throw Error("CSV value");
 }
 if(seen.size!==72)throw Error("CSV incomplete");
 return {status:"PASS",probability_cells:72,confusion_cells:27,tv_cells:9,csv_rows:72};
}
function mutants(r,csv){
 const checks=[];
 function attempt(name,change,raw=csv){
  const copy=JSON.parse(JSON.stringify(r));change(copy);
  let rejected=false;try{validate(copy,raw)}catch(e){rejected=true}
  if(!rejected)throw Error("escaped mutation "+name);
  checks.push(name);
 }
 attempt("probability",x=>x.windows.B_ODD.observation_probability.ANTIPERSISTENT["000"]="0");
 attempt("confusion",x=>x.windows.A_ADJACENT.confusion.IID_FAIR.IID_FAIR="0");
 attempt("TV",x=>x.windows.B_ODD.tv["ANTIPERSISTENT|PERSISTENT"]="1/8");
 attempt("evidence",x=>x.evidence="E3");
 attempt("freeze",x=>x.original_R277_freeze="wrong");
 attempt("missing-window",x=>delete x.windows.C_EVEN);
 attempt("duplicate-CSV",x=>{},csv+csv.trimEnd().split("\n")[1]+"\n");
 attempt("missing-CSV",x=>{},csv.trimEnd().split("\n").slice(0,-1).join("\n")+"\n");
 return checks;
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),r=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),csv=fs.readFileSync(process.argv[3],"utf8");
 console.log(JSON.stringify({audit:validate(r,csv),mutations_rejected:mutants(r,csv)},null,2));
}
module.exports={validate,mutants};
