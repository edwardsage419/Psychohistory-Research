"use strict";
const fs=require("fs");
const csv=fs.readFileSync(process.argv[2]||"research/R237/R237_ALL_1944_ORIGINAL_LATENT_TOPIC_WORD_ATOMS.csv","utf8").trim();
const source=JSON.parse(fs.readFileSync(process.argv[3]||"research/R237/R237_EXACT_RESULTS.json","utf8"));
const receipt=JSON.parse(fs.readFileSync(process.argv[4]||"research/validation/R237_S33_PREFIX_BRIER_EXACT_RECEIPT_2026-10-28.json","utf8"));
let checks=0;
function check(c,msg){checks++;if(!c)throw Error("CHECK_FAILED "+msg);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function rat(n,d=1n){if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function f(s){let p=String(s).split("/");return rat(BigInt(p[0]),p.length>1?BigInt(p[1]):1n);}
function add(a,b){return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return rat(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return rat(a[0]*b[1],a[1]*b[0]);}
function sub(a,b){return add(a,[-b[0],b[1]]);}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
function str(a){return a[1]===1n?String(a[0]):a[0]+"/"+a[1];}
const Z=f("0"),O=f("1"),TWO=f("2"),THREE=f("3");
const lines=csv.split(/\r?\n/),header=lines.shift().split(",");
const expected=["world","oracle_z1","oracle_z2","oracle_z3","observed_word1","observed_word2","observed_word3","oracle_topic0_count","oracle_topic1_count","full_dirichlet_collapsed_topic_sequence_probability","conditional_emission_probability","full_original_latent_word_atom_probability"];
check(header.join("|")===expected.join("|"),"CSV schema");
check(lines.length===1944,"source rows");
const worlds=new Map(),keys=new Set();
for(const [i,line] of lines.entries()){
 const x=line.split(",");check(x.length===12,"columns "+i);
 const [world,z1,z2,z3,w1,w2,w3,n0,n1,dir,em,atom]=x;
 for(const v of [z1,z2,z3,w1,w2,w3,n0,n1])check(/^\d+$/.test(v),"integer "+i);
 for(const v of [z1,z2,z3])check(Number(v)<2,"topic "+i);
 for(const v of [w1,w2,w3])check(Number(v)<3,"word "+i);
 check(Number(n0)+Number(n1)===3,"topic count "+i);
 check(Number(n0)===[z1,z2,z3].filter(v=>v==="0").length,"topic0 count "+i);
 const p=f(atom);check(eq(mul(f(dir),f(em)),p),"atom factorization "+i);
 check(p[0]>0n,"positive atom "+i);
 const key=[world,z1,z2,z3,w1,w2,w3].join(":");check(!keys.has(key),"duplicate "+i);keys.add(key);
 if(!worlds.has(world))worlds.set(world,{rows:0,atoms:Z,joint:new Map()});
 const o=worlds.get(world),wkey=w1+w2+w3;
 o.rows++;o.atoms=add(o.atoms,p);o.joint.set(wkey,add(o.joint.get(wkey)||Z,p));
}
check(worlds.size===9,"world count");
const results=[];
for(const w of source.world_results){
 const o=worlds.get(w.world);check(!!o,"world "+w.world);check(o.rows===216,"atoms "+w.world);
 check(eq(o.atoms,O),"atom mass "+w.world);check(o.joint.size===27,"27 cells "+w.world);
 const j=w.exact_observable_three_position_word_joint;check(Object.keys(j).length===27,"frozen support "+w.world);
 for(const [key,v] of Object.entries(j))check(eq(o.joint.get(key)||Z,f(v)),"source-to-frozen "+w.world+" "+key);
 const prefixes=new Map(),marg=[Z,Z,Z];
 for(const [key,p] of o.joint){
   const x=key.slice(0,2),y=Number(key[2]);
   if(!prefixes.has(x))prefixes.set(x,[Z,Z,Z]);
   const a=prefixes.get(x);a[y]=add(a[y],p);marg[y]=add(marg[y],p);
 }
 check(prefixes.size===9,"prefix count "+w.world);
 check(eq(marg.reduce(add,Z),O),"marginal total "+w.world);
 let oracle=Z;
 for(const [prefix,a] of prefixes){
   const mass=a.reduce(add,Z);check(mass[0]>0n,"prefix positive "+w.world+" "+prefix);
   let cross=Z;
   for(let i=0;i<3;i++)for(let k=i+1;k<3;k++)cross=add(cross,mul(a[i],a[k]));
   oracle=add(oracle,div(mul(TWO,cross),mass));
 }
 let mcross=Z;
 for(let i=0;i<3;i++)for(let k=i+1;k<3;k++)mcross=add(mcross,mul(marg[i],marg[k]));
 const uni=mul(TWO,mcross),uniform=div(TWO,THREE);
 const regrets={UNIGRAM:sub(uni,oracle),UNIFORM:sub(uniform,oracle)};
 const rr=receipt.worlds.find(v=>v.world===w.world);check(!!rr,"receipt world "+w.world);
 for(const [k,val] of Object.entries({ORACLE_PREFIX:oracle,UNIGRAM:uni,UNIFORM:uniform}))check(eq(val,f(rr.risks[k])),"risk "+w.world+" "+k);
 for(const [k,val] of Object.entries(regrets)){check(eq(val,f(rr.regrets[k])),"regret "+w.world+" "+k);check(val[0]>=0n,"nonnegative "+w.world+" "+k);}
 results.push({world:w.world,ORACLE_PREFIX:str(oracle),UNIGRAM:str(uni),UNIFORM:str(uniform),REGRET_UNIGRAM:str(regrets.UNIGRAM),REGRET_UNIFORM:str(regrets.UNIFORM)});
}
check(results.length===9,"all worlds");
function find(name){return results.find(x=>x.world===name);}
for(const [a,b] of [["BASE_TOPICS","LABEL_SWAP_ALIAS"],["DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B"]])check(JSON.stringify(find(a)).replace(a,"")===JSON.stringify(find(b)).replace(b,""),"alias "+a);
for(const n of ["DUPLICATE_TOPICS_A","DUPLICATE_TOPICS_B","UNIFORM_WORDS"])check(find(n).REGRET_UNIGRAM==="0","zero regret "+n);
check(find("UNIFORM_WORDS").REGRET_UNIFORM==="0","uniform zero");
check(f(find("BASE_TOPICS").REGRET_UNIGRAM)[0]>0n,"base strictly positive");
const altered=JSON.parse(JSON.stringify(receipt));altered.worlds[0].risks.ORACLE_PREFIX="999";
check(!eq(f(altered.worlds[0].risks.ORACLE_PREFIX),f(find(altered.worlds[0].world).ORACLE_PREFIX)),"mutation rejected");
console.log(JSON.stringify({status:"PASS",checks,source_rows:lines.length,worlds:results,mutation_detected:true}));
