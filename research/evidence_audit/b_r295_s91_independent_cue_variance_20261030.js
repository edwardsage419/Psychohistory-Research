#!/usr/bin/env node
"use strict";
/* Independent nonblind B audit. No import from R295 S91 primary generator. */
const A=["0","1/2","1"],L=["0","1/2","1"],V=["0","1"],N=[0,1,2,3,4],E=["0","1/4","1/2"];
function parseCSV(s){const lines=s.trimEnd().split(/\r?\n/),head=lines.shift().split(",");return {head,rows:lines.map(line=>{let v=line.split(",");if(v.length!==head.length)throw Error("CSV width");return Object.fromEntries(head.map((k,i)=>[k,v[i]]));})};}
function number(s){if(typeof s!=="string"||!/^-?\d+(\/\d+)?$/.test(s))throw Error("invalid fraction "+s);let [a,b="1"]=s.split("/").map(Number);if(!b)throw Error("zero denominator");return a/b;}
function expect(test,why){if(!test)throw Error(why);}
function choice(a,l,v,n,c){
 let alpha16={"0":0,"1/2":8,"1":16}[a],lambda2={"0":0,"1/2":1,"1":2}[l];
 expect(alpha16!==undefined&&lambda2!==undefined,"bad factor");
 let H16=0;for(let i=0;i<n;i++)H16+=alpha16*(16-H16)/16;
 const score32=(2-lambda2)*Number(v)*16+lambda2*c*H16;
 return Number(score32>16);
}
function audit(csv,json){
 const data=parseCSV(csv),results=JSON.parse(json);
 const expectedHead=["alpha","lambda","V","n","error_rate","true_cue","observed_cue","source_probability","action_A","q_no_cue","q_noisy_cue","q_true_cue","weighted_brier_no_cue","weighted_brier_noisy_cue","weighted_brier_true_cue"];
 expect(JSON.stringify(data.head)===JSON.stringify(expectedHead),"header");
 expect(data.rows.length===1080,"source count");
 expect(results.research_id==="R295_S91"&&results.evidence==="E1_SYNTHETIC_ONLY"&&results.new_human_E2===0&&results.new_historical_E3===0&&results.R073==="FROZEN"&&results.PESEN_v0_1==="FROZEN"&&results.external_independent_replication==="NOT_RUN","evidence scope");
 expect(results.settings===270&&results.source_atoms===1080&&results.worlds.length===270,"result universe");
 const map=new Map();
 for(const r of data.rows){const k=[r.alpha,r.lambda,r.V,r.n,r.error_rate,r.true_cue,r.observed_cue].join("|");expect(!map.has(k),"duplicate source");map.set(k,r);}
 let checked=0,zeros=0,sensitive=0,summary=new Map(),worlds=new Map();
 for(const a of A)for(const l of L)for(const v of V)for(const n of N){
  const y0=choice(a,l,v,n,0),y1=choice(a,l,v,n,1);
  for(const e of E){
   const ep=number(e),k=[a,l,v,n,e].join("|"),sens=y0!==y1;
   if(sens)sensitive++;
   let r0=0,rz=0,rc=0,mass=0;
   for(let c=0;c<2;c++)for(let z=0;z<2;z++){
    const key=k+"|"+c+"|"+z,r=map.get(key);expect(!!r,"missing atom "+key);
    const p=(c===z?1-ep:ep)/2,y=c?y1:y0,q0=(y0+y1)/2,qz=(z?y1:y0)*(1-ep)+(z?y0:y1)*ep;
    const want={source_probability:p,action_A:y,q_no_cue:q0,q_noisy_cue:qz,q_true_cue:y,weighted_brier_no_cue:p*(y-q0)**2,weighted_brier_noisy_cue:p*(y-qz)**2,weighted_brier_true_cue:0};
    for(const [field,x] of Object.entries(want))expect(number(r[field])===x,"wrong "+field+" "+key);
    mass+=p;r0+=want.weighted_brier_no_cue;rz+=want.weighted_brier_noisy_cue;rc+=want.weighted_brier_true_cue;checked++;if(p===0)zeros++;
   }
   expect(mass===1&&rc===0,"mass and oracle");
   const w=results.worlds.find(x=>[x.alpha,x.lambda,x.V,x.n,x.error_rate].join("|")===k);
   expect(!!w,"missing result world");
   expect(w.cue_sensitive===sens,"sensitivity "+k);
   for(const [field,val] of [["baseline_brier",r0],["noisy_brier",rz],["oracle_brier",rc],["information_gain",r0-rz]])expect(Math.abs(number(w[field])-val)<1e-12,"world result "+field+" "+k);
   worlds.set(k,true);
   const ag=summary.get(e)||{worlds:0,sensitive:0,base:0,noisy:0,gain:0};
   ag.worlds++;ag.sensitive+=Number(sens);ag.base+=r0;ag.noisy+=rz;ag.gain+=r0-rz;summary.set(e,ag);
  }
 }
 expect(checked===1080&&map.size===1080&&worlds.size===270&&zeros===180&&results.zero_mass_atoms===180,"full coverage");
 expect(results.by_error.length===3&&results.by_lambda_error.length===9,"summary coverage");
 for(const [e,s] of summary){const r=results.by_error.find(x=>x.key===e);expect(!!r&&r.worlds===s.worlds&&r.cue_sensitive===s.sensitive,"summary key");for(const [field,x] of [["total_baseline_brier",s.base],["total_noisy_brier",s.noisy],["total_information_gain",s.gain]])expect(Math.abs(number(r[field])-x)<1e-12,"summary "+field);}
 const byL=new Map();for(const w of results.worlds){const k=w.lambda+"|"+w.error_rate,t=byL.get(k)||{worlds:0,sensitive:0,base:0,noisy:0,gain:0};t.worlds++;t.sensitive+=Number(w.cue_sensitive);t.base+=number(w.baseline_brier);t.noisy+=number(w.noisy_brier);t.gain+=number(w.information_gain);byL.set(k,t);}
 for(const [k,s] of byL){const r=results.by_lambda_error.find(x=>x.key===k);expect(!!r&&r.worlds===s.worlds&&r.cue_sensitive===s.sensitive,"lambda summary key");for(const [field,x] of [["total_baseline_brier",s.base],["total_noisy_brier",s.noisy],["total_information_gain",s.gain]])expect(Math.abs(number(r[field])-x)<1e-12,"lambda summary "+field);}
 expect(sensitive===66,"sensitive 22 per error");
 return {status:"PASS",checked_atoms:checked,settings:270,zero_mass_atoms:zeros,sensitive_per_error:sensitive/3,independent_method:"fixed integer habit strength and direct conditional Bernoulli variance"};
}
function mutationTests(csv,json){
 const d=parseCSV(csv),head=d.head,lines=csv.trimEnd().split("\n");
 const modify=(row,field,value)=>{const j=head.indexOf(field),cells=lines[row].split(",");cells[j]=value;const copy=lines.slice();copy[row]=cells.join(",");return copy.join("\n")+"\n";};
 const tests=[
  ["duplicate",()=>{let x=lines.slice();x[2]=x[1];return [x.join("\n")+"\n",json];}],
  ["missing",()=>[lines.slice(0,-1).join("\n")+"\n",json]],
  ["probability",()=>[modify(2,"source_probability","1/3"),json]],
  ["action",()=>[modify(2,"action_A","7"),json]],
  ["predictor",()=>[modify(2,"q_noisy_cue","1/3"),json]],
  ["weighted_loss",()=>[modify(2,"weighted_brier_noisy_cue","999"),json]],
  ["summary",()=>{const o=JSON.parse(json);o.by_error[0].cue_sensitive=999;return [csv,JSON.stringify(o)];}],
  ["evidence_inflation",()=>{const o=JSON.parse(json);o.evidence="E2_REAL_HUMAN";return [csv,JSON.stringify(o)];}]
 ];
 const observed=[];for(const [name,make] of tests){const [c,j]=make();let rejected=false;try{audit(c,j);}catch(e){rejected=true;}expect(rejected,"mutation escaped "+name);observed.push({name,rejected});}
 return observed;
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../validation");
 const csv=fs.readFileSync(path.join(root,"R295_S91_ALL_1080_NOISY_CUE_ATOMS.csv"),"utf8"),json=fs.readFileSync(path.join(root,"R295_S91_EXACT_RESULTS.json"),"utf8");
 console.log(JSON.stringify({audit:audit(csv,json),mutations:mutationTests(csv,json)}));
}
