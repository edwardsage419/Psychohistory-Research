"use strict";
/* R288 S84, exact six-draw preference-sign audit; Node standard library only.
   CLI: node r288_s84_sign_error_20261030.js ORIGINAL_CSV OUTPUT_DIR
   This program never alters the original source. */
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){let t=a%b;a=b;b=t;}return a||1}
function frac(n,d=1){if(!Number.isInteger(n)||!Number.isInteger(d)||d===0)throw Error("bad rational");if(d<0){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]}
function parseF(s){let p=String(s).split("/");return frac(Number(p[0]),p.length===2?Number(p[1]):1)}
function same(a,b){return a[0]*b[1]===b[0]*a[1]}
function fmt(a){return a[1]===1?String(a[0]):a.join("/")}
function val(x,r,L){return x>=r?x-r:L*(x-r)}
function parseCSV(text){let lines=text.trimEnd().split(/\r?\n/),head=lines.shift().split(",");return lines.map(line=>{let cells=line.split(",");if(cells.length!==head.length)throw Error("column count");return Object.fromEntries(head.map((k,i)=>[k,cells[i]]))})}
function analyze(text){
 let rows=parseCSV(text),seen=new Set(),groups=new Map(),out=[];
 if(rows.length!==576)throw Error("source coverage: expected 576");
 for(let z of rows){
  let r=Number(z.reference),L=Number(z.loss_multiplier),bits=z.ordered_all_six_independent_fair_gamble_bits;
  if(![-2,0,2].includes(r)||![1,2,3].includes(L)||!/^[01]{6}$/.test(bits))throw Error("source keys");
  let world="REF_"+r+"_LOSS_"+L,key=world+"|"+bits;
  if(z.world!==world||seen.has(key))throw Error("duplicate/world");seen.add(key);
  if(z.source_probability!=="1/64")throw Error("source probability");
  let pay=bits.split("").map(x=>x==="1"?3:-2),scores=pay.map(x=>val(x,r,L)),sure=val(0,r,L);
  if(z.realized_gamble_payoffs!==pay.join(";")||z.realized_gamble_reference_values!==scores.join(";"))throw Error("source payoff/value");
  if(!same(parseF(z.sure_zero_reference_value),frac(sure)))throw Error("sure value");
  let sum=scores.reduce((a,b)=>a+b,0),diff=sum-6*sure;
  if(!same(parseF(z.realized_mean_gamble_reference_value),frac(sum,6)))throw Error("realized mean");
  if(!same(parseF(z.realized_mean_gamble_minus_sure),frac(diff,6)))throw Error("realized difference");
  let population=val(3,r,L)+val(-2,r,L)-2*sure;
  if(population===0)throw Error("population tie unhandled");
  let cls=diff===0?"TIE":Math.sign(diff)===Math.sign(population)?"CORRECT":"WRONG";
  let g=groups.get(world)||{reference:r,loss_multiplier:L,correct:0,wrong:0,tie:0,population_difference:fmt(frac(population,2))};
  g[cls.toLowerCase()]++;groups.set(world,g);
  out.push({world,reference:r,loss_multiplier:L,bits,source_probability:"1/64",realized_difference:fmt(frac(diff,6)),population_difference:fmt(frac(population,2)),classification:cls});
 }
 if(groups.size!==9||seen.size!==576)throw Error("missing world");
 let summary=[...groups.values()].sort((a,b)=>a.reference-b.reference||a.loss_multiplier-b.loss_multiplier).map(g=>{
   if(g.correct+g.wrong+g.tie!==64)throw Error("per-world coverage");
   return {reference:g.reference,loss_multiplier:g.loss_multiplier,population_difference:g.population_difference,correct:g.correct,wrong:g.wrong,tie:g.tie,p_correct:fmt(frac(g.correct,64)),p_wrong:fmt(frac(g.wrong,64)),p_tie:fmt(frac(g.tie,64)),p_wrong_given_non_tie:fmt(frac(g.wrong,64-g.tie))};
 });
 return {rows:out,summary};
}
function negativeControls(text){
 const lines=text.trimEnd().split("\n"),base=analyze(text);let failures=[];
 const muts=[
  ["duplicate",()=>[lines[0],lines[1],lines[1],...lines.slice(3)].join("\n")+"\n"],
  ["missing",()=>lines.slice(0,-1).join("\n")+"\n"],
  ["probability",()=>text.replace(",1/64,",",1/32,")],
  ["realized",()=>text.replace(/,(-?\d+(?:\/\d+)?)\n/,",999\n")],
  ["source_bits",()=>text.replace("000001","000000")]
 ];
 for(let [name,fn] of muts){let rejected=false;try{analyze(fn())}catch(e){rejected=true}if(!rejected)throw Error("mutant accepted: "+name);failures.push(name)}
 return failures;
}
function derivedCSV(rows){let h=["world","reference","loss_multiplier","bits","source_probability","realized_difference","population_difference","classification"];return h.join(",")+"\n"+rows.map(z=>h.map(k=>z[k]).join(",")).join("\n")+"\n"}
if(typeof module!=="undefined")module.exports={analyze,negativeControls,derivedCSV};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),args=process.argv.slice(2);
 if(args.length!==2)throw Error("Usage: node SCRIPT ORIGINAL_CSV OUTPUT_DIR");
 const text=fs.readFileSync(args[0],"utf8"),z=analyze(text),neg=negativeControls(text);
 fs.mkdirSync(args[1],{recursive:true});
 fs.writeFileSync(path.join(args[1],"R288_S84_ALL_576_SIGN_RECEIPTS.csv"),derivedCSV(z.rows));
 fs.writeFileSync(path.join(args[1],"R288_S84_EXACT_RESULTS.json"),JSON.stringify({research_id:"R288",substudy:"S84",evidence:"E1_ONLY",source_atoms:576,results:z.summary,negative_controls_rejected:neg,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0},null,2)+"\n");
 console.log(JSON.stringify({worlds:z.summary.length,rows:z.rows.length,negative_controls_rejected:neg},null,2));
}
