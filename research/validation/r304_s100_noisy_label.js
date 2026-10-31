#!/usr/bin/env node
"use strict";
// Exact synthetic enumeration. Run: node research/validation/r304_s100_noisy_label.js
const fs=require("fs"),path=require("path");
const generate=function generate(originalWorlds){
 const levels=[0,1,2],menus=[["EQUAL_TOTAL_A_FAVORED",10,6],["EQUAL_TOTAL_B_FAVORED",6,10],["LOWER_TOTAL_A_FAVORED",9,3],["LOWER_TOTAL_B_FAVORED",3,9]],labels=["A_INGROUP","B_INGROUP"],rates=[0,1,2];
 const alt=(s,d,e,l,m)=>{let a=m[1],b=m[2],g=l===0?a-b:b-a;return Number(4*(a+b-16)+s*d*g-2*e*Math.abs(a-b)>0)};
 const fracLevel=v=>v===0?"0":v===1?"1/2":"1";
 const gcd=(a,b)=>b?gcd(b,a%b):a, frac=(n,d)=>{let g=gcd(n,d);return `${n/g}/${d/g}`};
 const accum={0:{prior:0,naive:0,bayes:0},1:{prior:0,naive:0,bayes:0},2:{prior:0,naive:0,bayes:0}},rows=[];
 const orig=originalWorlds?new Map(originalWorlds.map(w=>[w.world,w.chosen_option])):null;
 let sensitive=0,invariant=0,alternativeWorlds=0,originalCheck=0;
 for(let s of levels)for(let d of levels)for(let e of levels)for(let m of menus){
  const ys=labels.map((_,l)=>alt(s,d,e,l,m));
  sensitive+=Number(ys[0]!==ys[1]);invariant+=Number(ys[0]===ys[1]);alternativeWorlds+=ys[0]+ys[1];
  for(let l=0;l<2;l++){
   if(orig){let world=`salience=${fracLevel(s)}|differentiation=${fracLevel(d)}|inequity=${fracLevel(e)}|label=${labels[l]}|menu=${m[0]}`;if(orig.get(world)!==(ys[l]?"ALTERNATIVE":"BASE"))throw Error(`Original R304 parity FAIL ${world}`);originalCheck++}
   for(let k of rates)for(let o=0;o<2;o++){
    const weight=o===l?4-k:k;
    const prior4=2*(ys[0]+ys[1]),naive4=4*ys[o],bayes4=(4-k)*ys[o]+k*ys[1-o],y4=4*ys[l];
    const losses={prior:(prior4-y4)**2,naive:(naive4-y4)**2,bayes:(bayes4-y4)**2};
    for(let z of Object.keys(losses))accum[k][z]+=weight*losses[z];
    rows.push({s,d,e,menu:m[0],true_label:labels[l],observed_label:labels[o],epsilon_quarters:k,channel_weight_eighths:weight,actual_alternative:ys[l],prior_prob_quarters:prior4,naive_prob_quarters:naive4,bayes_prob_quarters:bayes4,prior_brier_sixteenths:losses.prior,naive_brier_sixteenths:losses.naive,bayes_brier_sixteenths:losses.bayes});
   }
  }
 }
 if(rows.length!==1296||sensitive+invariant!==108||alternativeWorlds!==12)throw Error("Coverage fail");
 if(orig&&originalCheck!==216)throw Error("Archive parity incomplete");
 const summary={scope:"E1_PROJECT_CUSTOM_SYNTHETIC_ONLY",model:"R304",extension:"S100-v1",original_freeze:"60f6406cede7eb5bb7cea9dc622835d8fe3f4c41",prescore_freeze:"04424fe2798d8b03efe90d582ac6a29ed0ccdbfd",source_rows:rows.length,label_free_configurations:108,sensitive,invariant,alternativeWorlds,originalCheck,by_epsilon:{}};
 for(let k of rates){let a=accum[k],n=13824;summary.by_epsilon[`${k}/4`]={prior:frac(a.prior,n),naive:frac(a.naive,n),bayes:frac(a.bayes,n),numerators:a,denominator:n}}
 const cols=Object.keys(rows[0]),csv=cols.join(",")+"\n"+rows.map(r=>cols.map(k=>r[k]).join(",")).join("\n")+"\n";
 return {summary,csv,rows};
};
if(require.main===module){
 const root=path.join(__dirname,"..","R304");
 const orig=JSON.parse(fs.readFileSync(path.join(root,"R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json"),"utf8")).worlds;
 const out=generate(orig);
 fs.writeFileSync(path.join(__dirname,"R304_S100_ALL_1296_LABEL_CHANNEL_ATOMS.csv"),out.csv);
 fs.writeFileSync(path.join(__dirname,"R304_S100_EXACT_BRIER_RESULTS.json"),JSON.stringify(out.summary,null,2)+"\n");
 process.stdout.write(JSON.stringify(out.summary)+"\n");
}
module.exports={generate};
