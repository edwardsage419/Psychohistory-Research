#!/usr/bin/env node
// Independent B: first and second inclusion moments; oracle potential outcomes for audit only.
const fs=require("fs");
function compute(csv){
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n};
const F=x=>{if(typeof x==="object"&&x.n!==undefined)return x;let s=String(x).split("/");let n=BigInt(s[0]),d=BigInt(s[1]||"1");if(d<0n){n=-n;d=-d;}if(d===0n)throw Error("zero denominator");let g=gcd(n,d);return {n:n/g,d:d/g}};
const A=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d+y.n*x.d)+"/"+(x.d*y.d))};
const N=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d-y.n*x.d)+"/"+(x.d*y.d))};
const M=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.n)+"/"+(x.d*y.d))};
const D=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d)+"/"+(x.d*y.n))};
const S=x=>{x=F(x);return x.d===1n?String(x.n):x.n+"/"+x.d};
const eq=(x,y)=>S(x)===S(y),zero=F(0),one=F(1);
const lines=csv.trim().split(/\r?\n/);const hdr=lines.shift().split(",");
const rows=lines.map(l=>Object.fromEntries(hdr.map((h,i)=>[h,l.split(",")[i]])));
const worlds=[...new Set(rows.map(r=>r.world))],clips=["0","1/3","1/2"],conditions=[];
let mutatedPairDetected=false;
for(const world of worlds){
 const wr=rows.filter(r=>r.world===world),p=Array.from({length:8},()=>zero),q=Array.from({length:8},()=>Array.from({length:8},()=>zero));
 const first=wr[0],x=first.observed_8_X.split("|").map(Number),y0=first.true_8_individual_Y0_ORACLE_ONLY.split("|").map(F),y1=first.true_8_individual_Y1_ORACLE_ONLY.split("|").map(F),e=first.observable_e_X0_e_X1.split("|").map(F);
 let mass=zero;
 for(const r of wr){
  const z=r.original_8_unit_treatment_assignment.split("|").map(Number),weight=F(r.original_assignment_true_probability_exact);mass=A(mass,weight);
  for(let i=0;i<8;i++)if(z[i]){p[i]=A(p[i],weight);for(let j=0;j<8;j++)if(z[j])q[i][j]=A(q[i][j],weight)}
 }
 if(!eq(mass,one))throw Error("mass");
 for(const clip of clips){
  const c=F(clip),overlap=e.every(v=>v.n>0n&&v.n<v.d);
  if(!overlap){conditions.push({world,clip,source_mass:S(mass),status:"NO_COMMON_SUPPORT",mean:null,bias:null,variance:null,mse:null});continue}
  const a=[],baseTerms=[];
  for(let i=0;i<8;i++){
   let ec=e[x[i]];
   if(ec.n*c.d<c.n*ec.d)ec=c;
   const upper=N(one,c);
   if(ec.n*upper.d>upper.n*ec.d)ec=upper;
   a.push(D(A(D(y1[i],ec),D(y0[i],N(one,ec))),F(8)));
   baseTerms.push(D(y0[i],M(F(-8),N(one,ec))));
  }
  const b=baseTerms.reduce(A,zero);
  const lin=a.reduce((s,ai,i)=>A(s,M(ai,p[i])),zero);
  const mean=A(b,lin);
  let second=A(M(b,b),M(F(2),M(b,lin)));
  for(let i=0;i<8;i++){second=A(second,M(M(a[i],a[i]),p[i]));for(let j=i+1;j<8;j++)second=A(second,M(F(2),M(M(a[i],a[j]),q[i][j])))}
  const variance=N(second,M(mean,mean)),bias=N(mean,F(2)),mse=A(variance,M(bias,bias));
  if(variance.n<0n)throw Error("negative variance");
  conditions.push({world,clip,source_mass:S(mass),status:"OK",mean:S(mean),bias:S(bias),variance:S(variance),mse:S(mse)});
  if(!mutatedPairDetected&&a[0].n!==0n&&a[1].n!==0n){
   const mutantSecond=A(second,M(F(2),M(M(a[0],a[1]),F("1/1000"))));
   mutatedPairDetected=!eq(mutantSecond,second);
  }
 }
}
if(!mutatedPairDetected)throw Error("pairwise mutation undetected");
return {research:"B_R218_S14",method:"independent first and second inclusion moment identity; no per-assignment observed outcome estimator",conditions,checks:{joint_inclusion_mutation_detected:mutatedPairDetected},evidence:"E1_ARTIFICIAL"};

}
if(require.main===module){if(!process.argv[2])throw Error("usage: node script.js original_R218.csv");process.stdout.write(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}
module.exports={compute};
