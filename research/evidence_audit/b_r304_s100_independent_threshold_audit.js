#!/usr/bin/env node
"use strict";
// Independent algebraic threshold oracle and eight mutation guards. Run: node research/evidence_audit/b_r304_s100_independent_threshold_audit.js
const fs=require("fs"),path=require("path");
const audit=function audit(rows,summary,originalWorlds){
 if(summary.scope!=="E1_PROJECT_CUSTOM_SYNTHETIC_ONLY"||summary.source_rows!==1296||rows.length!==1296)throw Error("scope or count");
 const menus=[["EQUAL_TOTAL_A_FAVORED",10,6],["EQUAL_TOTAL_B_FAVORED",6,10],["LOWER_TOTAL_A_FAVORED",9,3],["LOWER_TOTAL_B_FAVORED",3,9]],labels=["A_INGROUP","B_INGROUP"];
 const orig=originalWorlds?new Map(originalWorlds.map(w=>[w.world,w.chosen_option])):null;
 const lvl=x=>x===0?"0":x===1?"1/2":"1";
 const threshold=(s,d,e,l,m)=>{
  let favored=(l===0?m[1]>m[2]:m[2]>m[1]);
  if(!favored)return 0;
  if(m[1]+m[2]===16)return Number(s*d>2*e);
  return Number(6*s*d>16+12*e);
 };
 let i=0,sensitive=0,alternative=0;const totals={0:{prior:0,naive:0,bayes:0},1:{prior:0,naive:0,bayes:0},2:{prior:0,naive:0,bayes:0}};
 for(let s=0;s<=2;s++)for(let d=0;d<=2;d++)for(let e=0;e<=2;e++)for(let m of menus){
  let y=[threshold(s,d,e,0,m),threshold(s,d,e,1,m)];
  sensitive+=Number(y[0]!==y[1]);alternative+=y[0]+y[1];
  for(let l=0;l<2;l++){
   if(orig){let key=`salience=${lvl(s)}|differentiation=${lvl(d)}|inequity=${lvl(e)}|label=${labels[l]}|menu=${m[0]}`;if(orig.get(key)!==(y[l]?"ALTERNATIVE":"BASE"))throw Error("original archive mismatch")}
   for(let k=0;k<=2;k++)for(let o=0;o<2;o++){
    const r=rows[i++],weight=o===l?4-k:k,prior4=2*(y[0]+y[1]),naive4=4*y[o],bayes4=(4-k)*y[o]+k*y[1-o];
    if(r.s!==s||r.d!==d||r.e!==e||r.menu!==m[0]||r.true_label!==labels[l]||r.observed_label!==labels[o]||r.epsilon_quarters!==k||r.channel_weight_eighths!==weight||r.actual_alternative!==y[l]||r.prior_prob_quarters!==prior4||r.naive_prob_quarters!==naive4||r.bayes_prob_quarters!==bayes4)throw Error("atom mismatch "+i);
    for(let z of ["prior","naive","bayes"]){
     const q={prior:prior4,naive:naive4,bayes:bayes4}[z], loss=(q-4*y[l])**2;
     if(r[`${z}_brier_sixteenths`]!==loss)throw Error("loss mismatch");
     totals[k][z]+=weight*loss;
    }
   }
  }
 }
 if(i!==1296||summary.sensitive!==sensitive||summary.invariant!==108-sensitive||summary.alternativeWorlds!==alternative)throw Error("summary coverage mismatch");
 for(let k=0;k<=2;k++){
  let z=summary.by_epsilon[`${k}/4`];
  if(z.denominator!==13824||z.numerators.prior!==sensitive*32||z.numerators.naive!==sensitive*32*k||z.numerators.bayes!==sensitive*8*k*(4-k))throw Error("independent algebraic risk mismatch");
  for(let name of ["prior","naive","bayes"])if(totals[k][name]!==z.numerators[name])throw Error("row aggregate mismatch");
 }
 return {rows:i,sensitive,original_parity:orig?216:0,algebraic_risks:"PASS"};
};
const csvRows=(txt)=>{const lines=txt.trim().split(/\r?\n/),cols=lines.shift().split(",");return lines.map(line=>{let cells=line.split(","),r={};cols.forEach((k,i)=>r[k]=["s","d","e","epsilon_quarters","channel_weight_eighths","actual_alternative","prior_prob_quarters","naive_prob_quarters","bayes_prob_quarters","prior_brier_sixteenths","naive_brier_sixteenths","bayes_brier_sixteenths"].includes(k)?Number(cells[i]):cells[i]);return r})};
if(require.main===module){
 const v=path.join(__dirname,"..","validation"),o=path.join(__dirname,"..","R304");
 const rows=csvRows(fs.readFileSync(path.join(v,"R304_S100_ALL_1296_LABEL_CHANNEL_ATOMS.csv"),"utf8"));
 const summary=JSON.parse(fs.readFileSync(path.join(v,"R304_S100_EXACT_BRIER_RESULTS.json"),"utf8"));
 const original=JSON.parse(fs.readFileSync(path.join(o,"R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json"),"utf8")).worlds;
 const positive=audit(rows,summary,original),mutations=[];
 const tryMut=(name,fn)=>{let a=rows.slice(),b=JSON.parse(JSON.stringify(summary));fn(a,b);try{audit(a,b,original);mutations.push({name,rejected:false})}catch(e){mutations.push({name,rejected:true,error:e.message})}};
 tryMut("duplicate",a=>a.splice(1,0,{...a[0]}));tryMut("missing",a=>a.pop());
 tryMut("action",a=>a[0]={...a[0],actual_alternative:1});
 tryMut("posterior",a=>a[0]={...a[0],bayes_prob_quarters:3});
 tryMut("channel_weight",a=>a[0]={...a[0],channel_weight_eighths:3});
 tryMut("loss",a=>a[0]={...a[0],prior_brier_sixteenths:1});
 tryMut("aggregate",(_a,b)=>b.by_epsilon["1/4"].numerators.bayes++);
 tryMut("evidence",(_a,b)=>b.scope="E2_HUMAN");
 const receipt={status:mutations.every(m=>m.rejected)?"PASS":"FAIL",positive,mutations};
 process.stdout.write(JSON.stringify(receipt,null,2)+"\n");if(receipt.status!=="PASS")process.exitCode=1;
}
module.exports={audit};
