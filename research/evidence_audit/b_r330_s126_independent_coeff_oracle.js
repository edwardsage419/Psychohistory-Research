// R330 S126 independent nonblind oracle: fixed closed-form coefficient pairs; no primary imports.
const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let x=a<0n?-a:a,y=b;while(y){[x,y]=[y,x%y]}return [a/x,b/x]};
const plus=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const times=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const over=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const geq=(a,b)=>a[0]*b[1]>=b[0]*a[1];
const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
const COEFF={
 0:[{A:[Q(1),Q(1,2)],B:[Q(1,2),Q(1)]},{A:[Q(1,2),Q(1)],B:[Q(1),Q(1,2)]}],
 1:[{A:[Q(1,4),Q(1,4)],B:[Q(1,6),Q(1)]},{A:[Q(1,8),Q(1,2)],B:[Q(1,3),Q(1,2)]}]
};
const errors=[Q(0),Q(1,4),Q(1,2)];
const action=(a,b)=>geq(a,b)?"A":"B";
function expected(){
 const worlds=[];
 for(let n=0;n<16;n++){const bits=[n>>3&1,n>>2&1,n>>1&1,n&1],history=bits.join("");
 for(const decay of [0,1])for(const observed_cue of [0,1])for(const error of errors){
 const scores=[{},{}],weighted=[{},{}];
 for(const z of [0,1])for(const a of ["A","B"]){
  const w=COEFF[decay][z][a],indices=a==="A"?[0,2]:[1,3];
  const numerator=plus(times(w[0],Q(bits[indices[0]])),times(w[1],Q(bits[indices[1]])));
  const denominator=plus(w[0],w[1]);
  weighted[z][a]=[numerator,denominator];scores[z][a]=over(numerator,denominator);
 }
 const posterior=[observed_cue===0?Q(error[1]-error[0],error[1]):error,
                  observed_cue===1?Q(error[1]-error[0],error[1]):error];
 const m={},p={};
 for(const a of ["A","B"]){
  m[a]=plus(times(posterior[0],scores[0][a]),times(posterior[1],scores[1][a]));
  p[a]=over(plus(times(posterior[0],weighted[0][a][0]),times(posterior[1],weighted[1][a][0])),
             plus(times(posterior[0],weighted[0][a][1]),times(posterior[1],weighted[1][a][1])));
 }
 const naive=action(scores[observed_cue].A,scores[observed_cue].B),mc=action(m.A,m.B),pc=action(p.A,p.B);
 worlds.push({history,decay,observed_cue,error:fmt(error),
  score_a_cue0:fmt(scores[0].A),score_b_cue0:fmt(scores[0].B),
  score_a_cue1:fmt(scores[1].A),score_b_cue1:fmt(scores[1].B),
  marginal_a:fmt(m.A),marginal_b:fmt(m.B),pooled_a:fmt(p.A),pooled_b:fmt(p.B),
  naive_choice:naive,marginal_choice:mc,pooled_choice:pc,
  marginal_vs_naive:Number(mc!==naive),pooled_vs_marginal:Number(pc!==mc),
  score_noncommutation:Number(fmt(m.A)!==fmt(p.A)||fmt(m.B)!==fmt(p.B))});
 }}
 const groups=[];
 for(const decay of [0,1])for(const error of errors){
  const rows=worlds.filter(r=>r.decay===decay&&r.error===fmt(error));
  groups.push({decay,error:fmt(error),n:rows.length,
   marginal_A:rows.filter(r=>r.marginal_choice==="A").length,
   naive_disagreements:rows.reduce((s,r)=>s+r.marginal_vs_naive,0),
   pooled_choice_disagreements:rows.reduce((s,r)=>s+r.pooled_vs_marginal,0),
   score_noncommutations:rows.reduce((s,r)=>s+r.score_noncommutation,0)});
 }
 return {model:"R330_S126_CONSTRUCTED_NOISY_CUE_E1",evidence:"E1_CONSTRUCTED_ONLY",
  original_protocol:"R330_FOUR_INSTANCE_CUE_RECENCY",world_count:192,groups,worlds};
}
function same(a,b){if(Array.isArray(a)||Array.isArray(b))return Array.isArray(a)&&Array.isArray(b)&&a.length===b.length&&a.every((v,i)=>same(v,b[i]));
 if(a&&b&&typeof a==="object"&&typeof b==="object"){const ak=Object.keys(a).sort(),bk=Object.keys(b).sort();
  return ak.join("|")===bk.join("|")&&ak.every(k=>same(a[k],b[k]));}
 return a===b}
function audit(receipt){if(!same(receipt,expected()))throw Error("receipt arithmetic, identity, source or coverage mismatch");return true}
function mutationTests(original){
 const mods=[x=>x.worlds.pop(),x=>x.worlds[1]=x.worlds[0],
  x=>x.worlds[1].marginal_a="999",x=>x.worlds[1].pooled_b="999",
  x=>x.worlds[1].marginal_choice=x.worlds[1].marginal_choice==="A"?"B":"A",
  x=>x.worlds[1].error="3/8",x=>x.original_protocol="R073",x=>x.evidence="E2"];
 let rejected=0;
 for(const mod of mods){const v=JSON.parse(JSON.stringify(original));mod(v);
  try{audit(v)}catch(e){rejected++}}
 if(rejected!==mods.length)throw Error("negative controls failed "+rejected);
 return rejected;
}
if(typeof module!=="undefined"&&module.exports)module.exports={audit,mutationTests};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");const receipt=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 audit(receipt);console.log("PASS 192 worlds; rejected "+mutationTests(receipt)+" mutations");
}
