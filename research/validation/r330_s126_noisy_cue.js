// R330 S126 exact finite noisy-cue calculation. Constructed E1 only.
const F=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}let x=a<0n?-a:a,y=b;while(y){const t=x%y;x=y;y=t}return [a/x,b/x]};
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const ge=(a,b)=>a[0]*b[1]>=b[0]*a[1];
const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
const ONE=F(1),ZERO=F(0),HALF=F(1,2),ERRORS=[ZERO,F(1,4),HALF];
const MEM=[[1,"A",0],[2,"B",1],[3,"A",1],[4,"B",0]];
function components(h,z,d,a){
 let num=ZERO,den=ZERO;
 MEM.forEach(([t,action,c],i)=>{if(action!==a)return;
  const sim=c===z?ONE:HALF;
  const rec=d?F(1,5-t):ONE;
  const w=mul(sim,rec);
  num=add(num,mul(w,F(h[i])));den=add(den,w);
 });return [num,den];
}
const choose=(a,b)=>ge(a,b)?"A":"B";
function solve(h,d,o,e){
 const comps=[{},{}],scores=[{},{}];
 for(let z=0;z<2;z++)for(const a of ["A","B"]){
  comps[z][a]=components(h,z,d,a);
  scores[z][a]=div(comps[z][a][0],comps[z][a][1]);
 }
 const post=[o===0?add(ONE,mul(F(-1),e)):e,o===1?add(ONE,mul(F(-1),e)):e];
 const marginal={},pooled={};
 for(const a of ["A","B"]){
  marginal[a]=add(mul(post[0],scores[0][a]),mul(post[1],scores[1][a]));
  pooled[a]=div(add(mul(post[0],comps[0][a][0]),mul(post[1],comps[1][a][0])),
                add(mul(post[0],comps[0][a][1]),mul(post[1],comps[1][a][1])));
 }
 const naive=choose(scores[o].A,scores[o].B),mc=choose(marginal.A,marginal.B),pc=choose(pooled.A,pooled.B);
 return {history:h.join(""),decay:d,observed_cue:o,error:fmt(e),
  score_a_cue0:fmt(scores[0].A),score_b_cue0:fmt(scores[0].B),
  score_a_cue1:fmt(scores[1].A),score_b_cue1:fmt(scores[1].B),
  marginal_a:fmt(marginal.A),marginal_b:fmt(marginal.B),
  pooled_a:fmt(pooled.A),pooled_b:fmt(pooled.B),
  naive_choice:naive,marginal_choice:mc,pooled_choice:pc,
  marginal_vs_naive:Number(mc!==naive),pooled_vs_marginal:Number(pc!==mc),
  score_noncommutation:Number(!eq(marginal.A,pooled.A)||!eq(marginal.B,pooled.B))};
}
function generate(){
 const worlds=[];
 for(let n=0;n<16;n++){const h=[(n>>3)&1,(n>>2)&1,(n>>1)&1,n&1];
  for(const d of [0,1])for(const o of [0,1])for(const e of ERRORS)worlds.push(solve(h,d,o,e));
 }
 const groups=[];
 for(const d of [0,1])for(const e of ERRORS){
  const subset=worlds.filter(r=>r.decay===d&&r.error===fmt(e));
  groups.push({decay:d,error:fmt(e),n:subset.length,
   marginal_A:subset.filter(r=>r.marginal_choice==="A").length,
   naive_disagreements:subset.reduce((s,r)=>s+r.marginal_vs_naive,0),
   pooled_choice_disagreements:subset.reduce((s,r)=>s+r.pooled_vs_marginal,0),
   score_noncommutations:subset.reduce((s,r)=>s+r.score_noncommutation,0)});
 }
 return {model:"R330_S126_CONSTRUCTED_NOISY_CUE_E1",evidence:"E1_CONSTRUCTED_ONLY",
  original_protocol:"R330_FOUR_INSTANCE_CUE_RECENCY",world_count:192,groups,worlds};
}
function canonical(o){if(Array.isArray(o))return o.map(canonical);
 if(o&&typeof o==="object")return Object.fromEntries(Object.keys(o).sort().map(k=>[k,canonical(o[k])]));
 return o}
function serialized(){return JSON.stringify(canonical(generate()))+"\n"}
if(typeof module!=="undefined"&&module.exports)module.exports={generate,serialized};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");const out=process.argv[2];
 if(out)fs.writeFileSync(out,serialized());else process.stdout.write(serialized());
}
