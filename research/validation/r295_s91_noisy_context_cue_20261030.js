#!/usr/bin/env node
"use strict";
/* R295 S91 fixed E1 artificial cue measurement study. Standard library only. */
const ORIGINAL_BLOB="c8400ce907e2f09734bbdf5f018074ce73d0b130";
const FREEZE="4b67e0dd172f6633a37c4ba65f12e7b5269856b2";
const ALPHAS=["0","1/2","1"], LAMBDAS=["0","1/2","1"], VALUES=["0","1"], STAGES=[0,1,2,3,4], ERRORS=[0,1,2];
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return Math.abs(a);}
function rat(n,d){if(d<=0)throw Error("bad denominator");let g=gcd(Math.abs(n),d);return g===0?"0":(d/g===1?String(n/g):String(n/g)+"/"+String(d/g));}
function parseCSV(s){
 const lines=s.trimEnd().split(/\r?\n/),head=lines.shift().split(",");
 return lines.map(line=>{let v=line.split(",");if(v.length!==head.length)throw Error("invalid original CSV");return Object.fromEntries(head.map((k,i)=>[k,v[i]]));});
}
function compute(originalCSV){
 const original=parseCSV(originalCSV);
 if(original.length!==180)throw Error("original source universe length");
 const lookup=new Map();
 for(const r of original){
  const k=[r.alpha,r.habit_share_lambda,r.current_outcome_value,r.training_repetitions_n,r.same_context_cue].join("|");
  if(lookup.has(k))throw Error("duplicate original source");
  if(!["A","B"].includes(r.selected))throw Error("invalid action");
  lookup.set(k,r.selected==="A"?1:0);
 }
 if(lookup.size!==180)throw Error("original unique source universe");
 const header=["alpha","lambda","V","n","error_rate","true_cue","observed_cue","source_probability","action_A","q_no_cue","q_noisy_cue","q_true_cue","weighted_brier_no_cue","weighted_brier_noisy_cue","weighted_brier_true_cue"];
 const atoms=[header.join(",")],worlds=[],totals=new Map(),lambdaTotals=new Map();
 for(const a of ALPHAS)for(const l of LAMBDAS)for(const v of VALUES)for(const n of STAGES){
  const y=[0,1].map(c=>{let k=[a,l,v,String(n),String(c)].join("|");if(!lookup.has(k))throw Error("missing original source "+k);return lookup.get(k);});
  for(const e4 of ERRORS){
   const sensitive=y[0]!==y[1], e=rat(e4,4), key=[a,l,v,n,e].join("|");
   let sum0=0,sumz=0,sumc=0,mass=0;
   for(let c=0;c<2;c++)for(let z=0;z<2;z++){
    const p8=(c===z?4-e4:e4),q04=2*(y[0]+y[1]),qz4=(4-e4)*y[z]+e4*y[1-z],qc4=4*y[c];
    const b0=p8*(4*y[c]-q04)**2,bz=p8*(4*y[c]-qz4)**2,bc=p8*(4*y[c]-qc4)**2;
    mass+=p8;sum0+=b0;sumz+=bz;sumc+=bc;
    atoms.push([a,l,v,n,e,c,z,rat(p8,8),y[c],rat(q04,4),rat(qz4,4),rat(qc4,4),rat(b0,128),rat(bz,128),rat(bc,128)].join(","));
   }
   if(mass!==8||sumc!==0||sum0<sumz||sumz<0)throw Error("mass/risk failure "+key);
   if(sensitive){
    if(sum0!==32||sumz!==8*e4*(4-e4)||sum0-sumz!==8*(2-e4)**2)throw Error("sensitive formula "+key);
   }else if(sum0!==0||sumz!==0)throw Error("negative control "+key);
   const row={alpha:a,lambda:l,V:v,n,error_rate:e,cue_sensitive:sensitive,baseline_brier:rat(sum0,128),noisy_brier:rat(sumz,128),oracle_brier:rat(sumc,128),information_gain:rat(sum0-sumz,128)};
   worlds.push(row);
   for(const [map,k] of [[totals,e],[lambdaTotals,l+"|"+e]]){
    const t=map.get(k)||{worlds:0,sensitive:0,baseline_n128:0,noisy_n128:0,oracle_n128:0,delta_n128:0};
    t.worlds++;t.sensitive+=Number(sensitive);t.baseline_n128+=sum0;t.noisy_n128+=sumz;t.oracle_n128+=sumc;t.delta_n128+=sum0-sumz;map.set(k,t);
   }
  }
 }
 if(worlds.length!==270||atoms.length!==1081)throw Error("S91 universe incomplete");
 const summary=(map)=>[...map].map(([key,t])=>({key,worlds:t.worlds,cue_sensitive:t.sensitive,total_baseline_brier:rat(t.baseline_n128,128),total_noisy_brier:rat(t.noisy_n128,128),total_oracle_brier:rat(t.oracle_n128,128),total_information_gain:rat(t.delta_n128,128)}));
 const result={research_id:"R295_S91",freeze_commit:FREEZE,original_source_blob:ORIGINAL_BLOB,evidence:"E1_SYNTHETIC_ONLY",settings:270,source_atoms:1080,zero_mass_atoms:atoms.slice(1).filter(s=>s.split(",")[7]==="0").length,worlds,by_error:summary(totals),by_lambda_error:summary(lambdaTotals),R073:"FROZEN",PESEN_v0_1:"FROZEN",new_human_E2:0,new_historical_E3:0,external_independent_replication:"NOT_RUN"};
 return {csv:atoms.join("\n")+"\n",json:JSON.stringify(result,null,2)+"\n",result};
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),crypto=require("crypto");
 const originalPath=path.resolve(__dirname,"../R295/R295_ALL_180_ORIGINAL_HABIT_CUE_REVALUATION_STATES.csv");
 const buf=fs.readFileSync(originalPath);
 const blob=crypto.createHash("sha1").update("blob "+buf.length+"\0").update(buf).digest("hex");
 if(blob!==ORIGINAL_BLOB)throw Error("original Git blob identity mismatch "+blob);
 const out=compute(buf.toString("utf8")),mode=process.argv[2]||"--check";
 for(const [name,content] of [["R295_S91_ALL_1080_NOISY_CUE_ATOMS.csv",out.csv],["R295_S91_EXACT_RESULTS.json",out.json]]){
  const file=path.join(__dirname,name);
  if(mode==="--emit")fs.writeFileSync(file,content);
  else if(mode==="--check"){if(fs.readFileSync(file,"utf8")!==content)throw Error("persisted bytes mismatch "+name);}
  else throw Error("usage: --emit or --check");
 }
 console.log(JSON.stringify({status:"PASS",mode,source_blob:blob,settings:270,atoms:1080,by_error:out.result.by_error}));
}
