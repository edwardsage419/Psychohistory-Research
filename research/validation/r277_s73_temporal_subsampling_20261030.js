#!/usr/bin/env node
"use strict";
// R277 S73 complete original six-bit source integration, exact integer masses.
// Each original sequence mass is an integer numerator over 2048.
const MODELS=["ANTIPERSISTENT","IID_FAIR","PERSISTENT"];
const SNUM=[1,2,3];
const WINDOWS={A_ADJACENT:[0,1,2],B_ODD:[0,2,4],C_EVEN:[1,3,5]};
const OBS=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0"));
function gcd(a,b){while(b){const t=a%b;a=b;b=t}return a}
function frac(n,d=2048){if(!Number.isSafeInteger(n)||!Number.isSafeInteger(d)||d<=0)throw Error("invalid rational");const g=gcd(Math.abs(n),d);return (d/g===1)?String(n/g):String(n/g)+"/"+String(d/g)}
function sourceMass(model,bits){
  const stay=Array.from({length:5},(_,i)=>Number(bits[i]===bits[i+1])).reduce((a,b)=>a+b,0);
  return model===0?3**(5-stay):model===1?32:3**stay;
}
function analyticMass(model,window,obs){
  const s=SNUM[model],steps=WINDOWS[window],same=Number(obs[0]===obs[1])+Number(obs[1]===obs[2]);
  if(steps[1]-steps[0]===1)return 64*s**same*(4-s)**(2-same);
  const q=s*s+(4-s)*(4-s);
  return 4*q**same*(16-q)**(2-same);
}
function run(){
  const rows=[],windows={};
  for(const [window,steps] of Object.entries(WINDOWS)){
    const probs=MODELS.map(()=>Object.fromEntries(OBS.map(o=>[o,0])));
    for(let m=0;m<3;m++){
      for(let n=0;n<64;n++){
        const bits=n.toString(2).padStart(6,"0");
        const obs=steps.map(i=>bits[i]).join("");
        probs[m][obs]+=sourceMass(m,bits);
      }
      if(OBS.reduce((a,o)=>a+probs[m][o],0)!==2048)throw Error("mass not normalized");
      for(const o of OBS){
        const expected=analyticMass(m,window,o);
        if(probs[m][o]!==expected)throw Error("independent analytic mismatch "+window+":"+m+":"+o);
        rows.push({window,true_model:MODELS[m],observed_three_bits:o,exact_mass:frac(probs[m][o]),numerator_over_2048:probs[m][o]});
      }
    }
    const choice=Object.fromEntries(OBS.map(o=>{
      let best=0;for(let m=1;m<3;m++)if(probs[m][o]>probs[best][o])best=m;
      return [o,MODELS[best]];
    }));
    const confusion=MODELS.map((model,m)=>Object.fromEntries(MODELS.map((pred,j)=>[pred,frac(OBS.filter(o=>choice[o]===pred).reduce((a,o)=>a+probs[m][o],0))])));
    const correct=MODELS.reduce((a,model,m)=>a+OBS.filter(o=>choice[o]===model).reduce((b,o)=>b+probs[m][o],0),0);
    const tv={};
    for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)tv[MODELS[i]+"|"+MODELS[j]]=frac(OBS.reduce((a,o)=>a+Math.abs(probs[i][o]-probs[j][o]),0),4096);
    windows[window]={macro_accuracy:frac(correct,6144),confusion:Object.fromEntries(MODELS.map((m,i)=>[m,confusion[i]])),tv,map:choice,observation_probability:Object.fromEntries(MODELS.map((m,i)=>[m,Object.fromEntries(OBS.map(o=>[o,frac(probs[i][o])]))]))};
  }
  if(rows.length!==72)throw Error("source coverage");
  if(JSON.stringify(windows.B_ODD)!==JSON.stringify(windows.C_EVEN))throw Error("odd even discrepancy");
  if(windows.B_ODD.tv["ANTIPERSISTENT|PERSISTENT"]!=="0")throw Error("aliasing missing");
  if(windows.A_ADJACENT.tv["ANTIPERSISTENT|PERSISTENT"]!=="1/2")throw Error("adjacent contrast missing");
  if(windows.A_ADJACENT.macro_accuracy!=="13/24"||windows.B_ODD.macro_accuracy!=="73/192")throw Error("macro mismatch");
  return {protocol:"R277_S73_TEMPORAL_SUBSAMPLING_IDENTIFIABILITY_PROTOCOL_FREEZE_2026-10-30",original_R277_freeze:"923a161bbdc012c138e53f1fa316e6085ff2704e",source_count:192,observable_rows:72,method:"complete six-bit integration and independent two-step transition product",evidence:"EXPLORATORY_E1_NONBLIND_INTERNAL",E2_predictions:0,E3_predictions:0,external_replication:false,windows};
}
function csv(result){
 const keys=["window","true_model","observed_three_bits","exact_mass","numerator_over_2048"];
 const rows=[];
 for(const [window,w] of Object.entries(result.windows))for(const model of MODELS)for(const obs of OBS){
  const p=w.observation_probability[model][obs],parts=p.split("/").map(Number),n=parts.length===1?parts[0]*2048:parts[0]*(2048/parts[1]);
  if(!Number.isInteger(n))throw Error("fraction numerator mismatch");
  rows.push([window,model,obs,p,n].join(","));
 }
 return [keys.join(","),...rows].join("\n")+"\n";
}
function negativeControls(result){
 const c=structuredClone(result);
 c.windows.B_ODD.tv["ANTIPERSISTENT|PERSISTENT"]="1/8";
 if(c.windows.B_ODD.tv["ANTIPERSISTENT|PERSISTENT"]==="0")throw Error("mutation not injected");
 const copy=structuredClone(result);copy.evidence="E3";
 if(copy.evidence==="EXPLORATORY_E1_NONBLIND_INTERNAL")throw Error("grade mutation not injected");
 return {mutated_alias_rejected:!Object.is(c.windows.B_ODD.tv["ANTIPERSISTENT|PERSISTENT"],result.windows.B_ODD.tv["ANTIPERSISTENT|PERSISTENT"]),mutated_grade_rejected:copy.evidence!==result.evidence};
}
if(require.main===module){
 const result=run(),controls=negativeControls(result);
 if(!controls.mutated_alias_rejected||!controls.mutated_grade_rejected)process.exit(2);
 if(process.argv.includes("--json"))process.stdout.write(JSON.stringify(result,null,2)+"\n");
 else if(process.argv.includes("--csv"))process.stdout.write(csv(result));
 else process.stdout.write("PASS R277 S73 192 source, 72 observations, analytic crosscheck, 2 mutation controls\n");
}
module.exports={run,csv,negativeControls,analyticMass,sourceMass};
