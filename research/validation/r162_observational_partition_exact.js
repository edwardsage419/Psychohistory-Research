"use strict";
// R162 third method, exact 72-world observable equivalence classes.
// Node usage: node r162_observational_partition_exact.js research/R162/R162_EXACT_RESULTS.json
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){const t=a%b;a=b;b=t;}return a||1}
function frac(n,d=1){if(d<=0)throw Error("denominator");const g=gcd(n,d);return [n/g,d/g]}
function fstr(v){return v[1]===1?String(v[0]):v[0]+"/"+v[1]}
function parse(s){const a=String(s).split("/").map(Number);return frac(a[0],a[1]||1)}
function eq(a,b){return a[0]*b[1]===b[0]*a[1]}
function sign(s){const n=parse(s)[0];return n<0?"negative":n>0?"positive":"zero"}
function compute(input){
 if(input.research_id!=="R162"||input.case_count!==72||input.worlds.length!==72)throw Error("frozen universe");
 const patterns=[[0,0,0],[1,0,0],[0,1,1],[1,1,1]], tickets=[0,1,3];
 const expected=new Set();
 for(let pi=0;pi<4;pi++)for(let j=0;j<3;j++)for(let li=0;li<3;li++)for(let c=0;c<2;c++)expected.add("p"+pi+"_j"+j+"_l"+li+"_c"+c);
 let nontrivialNeutral=0, flippedCorrect=0;
 const rows=[];
 for(const w of input.worlds){
  if(!expected.delete(w.id))throw Error("duplicate or extra world "+w.id);
  const y=w.demonstrator_actions,j=w.favored_demonstrator,l=w.additional_attention_tickets,c=w.artificial_correct_token;
  if(!patterns.some(p=>JSON.stringify(p)===JSON.stringify(y))||![0,1,2].includes(j)||!tickets.includes(l)||![0,1].includes(c))throw Error("world fields");
  const p=frac(y.reduce((a,b)=>a+b,0)+l*y[j],3+l),neutral=frac(y.reduce((a,b)=>a+b,0),3);
  const s=c===1?p:frac(p[1]-p[0],p[1]),s0=c===1?neutral:frac(neutral[1]-neutral[0],neutral[1]);
  const delta=frac(s[0]*s0[1]-s0[0]*s[1],s[1]*s0[1]);
  const checks=[["probability_copy_A",p],["neutral_probability_copy_A",neutral],["artificial_expected_accuracy",s],["neutral_expected_accuracy",s0],["advantage_over_neutral",delta]];
  for(const [name,value] of checks)if(!eq(parse(w[name]),value))throw Error("frozen mismatch "+w.id+" "+name);
  if(!eq(p,neutral))nontrivialNeutral++;
  if(!eq(delta,[0,1]))flippedCorrect++;
  rows.push({id:w.id,y:y.join(""),j,l,c,p:fstr(p),delta:fstr(delta)});
 }
 if(expected.size!==0)throw Error("missing frozen worlds "+expected.size);
 function partition(fields){
  const groups=new Map();
  for(const r of rows){const key=fields.map(f=>String(r[f])).join("|");if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r)}
  const hist={};let nonSingletonWorlds=0,max=0,mixedSignClasses=0,mixedSignWorlds=0;
  for(const group of groups.values()){
   const n=group.length;hist[n]=(hist[n]||0)+1;max=Math.max(max,n);
   if(n>1)nonSingletonWorlds+=n;
   if(new Set(group.map(r=>sign(r.delta))).size>1){mixedSignClasses++;mixedSignWorlds+=n}
  }
  return {class_count:groups.size,class_size_histogram:hist,maximum_class_size:max,non_singleton_worlds:nonSingletonWorlds,mixed_advantage_sign_classes:mixedSignClasses,mixed_advantage_sign_worlds:mixedSignWorlds}
 }
 const a=rows.find(r=>r.y==="100"&&r.j===0&&r.l===3&&r.c===1);
 const b=rows.find(r=>r.y==="011"&&r.l===0&&r.c===1);
 const c=rows.find(r=>r.y==="100"&&r.j===0&&r.l===3&&r.c===0);
 if(!a||!b||!c||a.p!=="2/3"||b.p!=="2/3"||c.p!=="2/3"||a.delta!=="1/3"||b.delta!=="0"||c.delta!=="-1/3")throw Error("predeclared counterexample failed");
 if(nontrivialNeutral===0||flippedCorrect===0)throw Error("mutants failed to trigger");
 return {research_id:"R162",evidence:"E1_SYNTHETIC_ONLY",frozen_blob_sha1:"aa6fd210a803d0914b5d18692f9a49c86f9b3009",verified_worlds:rows.length,
  partitions:{P0:partition(["p"]),P1:partition(["p","y"]),P2:partition(["p","y","c"]),P3:partition(["p","y","c","l"])},
  counterexamples:{prestige_A:a,neutral_other_composition:b,correct_token_reversal:c},
  executed_mutants:{replace_weighted_with_neutral_detected_worlds:nontrivialNeutral,reverse_correct_token_flips_nonzero_advantage_worlds:flippedCorrect},
  external_E2:0,external_E3:0,external_independent_reproduction:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const f=process.argv[2]||path.join(__dirname,"..","R162","R162_EXACT_RESULTS.json");
 console.log(JSON.stringify(compute(JSON.parse(fs.readFileSync(f,"utf8"))),null,2));
}
if(typeof module!=="undefined")module.exports={compute};
