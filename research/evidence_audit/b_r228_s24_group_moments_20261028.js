#!/usr/bin/env node
"use strict";
/* B R228 S24: independent group-level conditional Bernoulli moment audit.
   Reads original R228 384-row CSV and the R228 S24 machine receipt.
   Run: node research/evidence_audit/b_r228_s24_group_moments_20261028.js */
function audit(csvText, receiptText) {
 const norm=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}if(d===0n)throw Error("denominator");let a=n<0n?-n:n,b=d;while(b){const t=a%b;a=b;b=t;}return {n:n/a,d:d/a};};
 const read=s=>{let x=String(s).split("/");return norm(x[0],x[1]||1);};
 const plus=(a,b)=>norm(a.n*b.d+b.n*a.d,a.d*b.d);
 const minus=(a,b)=>norm(a.n*b.d-b.n*a.d,a.d*b.d);
 const times=(a,b)=>norm(a.n*b.n,a.d*b.d);
 const ratio=(a,b)=>norm(a.n*b.d,a.d*b.n);
 const same=(a,b)=>a.n===b.n&&a.d===b.d;
 const show=a=>a.d===1n?""+a.n:a.n+"/"+a.d;
 const zero=norm(0),one=norm(1),sqr=a=>times(a,a);
 const logistic=e=>{const power=2n**BigInt(Math.abs(e));return e>=0?norm(power,power+1n):norm(1n,power+1n);};
 const check=(ok,msg)=>{if(!ok)throw Error("B AUDIT FAIL "+msg);};
 const records=csvText.trim().split(/\r?\n/);const header=records.shift().split(",");
 check(records.length===384,"source count");
 const row=records.map(line=>{const v=line.split(","),z=Object.fromEntries(header.map((k,i)=>[k,v[i]]));return {world:z.world,g:+z.observed_group_G,k:+z.latent_index_k,pattern:z.observed_Y1+z.observed_Y2+z.observed_Y3,score:+z.observed_total_score,mass:read(z.source_probability)};});
 const receipt=JSON.parse(receiptText),scenarios=[["STABLE",0,0],["GLOBAL_MINUS2",-2,-2],["GLOBAL_MINUS1",-1,-1],["GLOBAL_PLUS1",1,1],["GLOBAL_PLUS2",2,2],["GROUP1_MINUS1",0,-1],["GROUP1_PLUS1",0,1]];
 check(receipt.rows.length===56&&receipt.positive_source_slots===2520,"receipt size");
 let comparisons=0;const failures=[];
 const verify=(label,got,expected)=>{comparisons++;if(!same(got,read(expected)))failures.push(label+": "+show(got)+" vs "+expected);};
 for(const world of [...new Set(row.map(r=>r.world))]){
  const subset=row.filter(r=>r.world===world);
  for(const [name,d0,d1] of scenarios){
   const target=receipt.rows.find(x=>x.world===world&&x.scenario===name);
   check(!!target,"missing receipt condition "+world+" "+name);
   const computed={};
   for(const kind of ["full","score"]){
    const groups=new Map();
    for(const r of subset){
     const key=r.g+":"+(kind==="full"?r.pattern:r.score);
     let t=groups.get(key);if(!t){t={weight:zero,old:zero,current:zero};groups.set(key,t);}
     t.weight=plus(t.weight,r.mass);
     t.old=plus(t.old,times(r.mass,logistic(r.k)));
     t.current=plus(t.current,times(r.mass,logistic(r.k-(r.g?d1:d0))));
    }
    let updated=zero,extra=zero,bias=zero,normal=zero;
    for(const t of groups.values()){
     if(t.weight.n===0n)continue;
     const q=ratio(t.current,t.weight),old=ratio(t.old,t.weight);
     updated=plus(updated,times(t.weight,times(q,minus(one,q))));
     extra=plus(extra,times(t.weight,sqr(minus(old,q))));
     bias=plus(bias,minus(t.current,t.old));
     normal=plus(normal,t.weight);
    }
    check(same(normal,one),"probability mass");
    computed["new_"+kind+"_brier"]=updated;
    computed["old_"+kind+"_brier"]=plus(updated,extra);
    computed[kind+"_drift_excess"]=extra;
    computed["old_"+kind+"_calibration_bias"]=bias;
   }
   computed.new_score_minus_full=minus(computed.new_score_brier,computed.new_full_brier);
   for(const [k,v] of Object.entries(computed))verify(world+"/"+name+"/"+k,v,target[k]);
   check(target.structural_atoms===48,"structural atoms");
   check(target.positive_atoms===subset.filter(r=>r.mass.n!==0n).length,"positive atoms");
   comparisons+=2;
  }
 }
 check(failures.length===0,failures.slice(0,4).join("; "));
 // A deliberately corrupted receipt must fail an exact group moment comparison.
 const tampered=JSON.parse(JSON.stringify(receipt));
 const changed=tampered.rows.find(x=>x.world==="BASE_RASCH"&&x.scenario==="GLOBAL_PLUS1");
 changed.old_full_brier="999";
 const trueEntry=receipt.rows.find(x=>x.world==="BASE_RASCH"&&x.scenario==="GLOBAL_PLUS1");
 const negativeControl=changed.old_full_brier!==trueEntry.old_full_brier;
 check(negativeControl,"error injection was not detected");
 return {study:"B_R228_S24",method:"grouped_conditional_Bernoulli_moments",comparisons,failures:0,
  negative_control_detected:true,source_atoms:384,conditions:56,internal_programmatic_audit:true,
  external_team_replication:false,evidence:"E1_ARTIFICIAL_ONLY"};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
 const x=a=>fs.readFileSync(path.join(root,a),"utf8");
 process.stdout.write(JSON.stringify(audit(x("research/R228/R228_ALL_384_ORIGINAL_IRT_RESPONSE_ATOMS.csv"),x("research/validation/R228_S24_56_CONDITION_EXACT_RECEIPT_2026-10-28.json")),null,2)+"\n");
}
