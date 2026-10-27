#!/usr/bin/env node
// Independent B: conditional Bernoulli HT moments plus pilot mixture.
const fs=require("fs");
function compute(csv){
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n};
const F=x=>{if(x&&typeof x==="object"&&x.n!==undefined)return x;const s=String(x).split("/");let n=BigInt(s[0]),d=BigInt(s[1]||"1");if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return {n:n/g,d:d/g}};
const A=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d+y.n*x.d)+"/"+(x.d*y.d))};
const N=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d-y.n*x.d)+"/"+(x.d*y.d))};
const M=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.n)+"/"+(x.d*y.d))};
const D=(x,y)=>{x=F(x);y=F(y);return F((x.n*y.d)+"/"+(x.d*y.n))};
const S=x=>{x=F(x);return x.d===1n?String(x.n):x.n+"/"+x.d};
const eq=(x,y)=>S(x)===S(y),zero=F(0),one=F(1),two=F(2),eight=F(8);
const lines=csv.trim().split(/\r?\n/),hdr=lines.shift().split(",");
const rows=lines.map(l=>{const parts=l.split(",");if(parts.length!==hdr.length)throw Error("CSV columns mismatch");return Object.fromEntries(hdr.map((h,i)=>[h,parts[i]]))});
if(rows.length!==1281)throw Error("1281 original assignments required");
const worlds=[...new Set(rows.map(r=>r.world))];if(worlds.length!==6)throw Error("six worlds");
const alphas=["1/2","1"],pilots=[0,2,4,6];
const probability=(bit,p)=>{let mass=one;for(let k=0;k<4;k++)mass=M(mass,bit&(1<<k)?p[pilots[k]]:N(one,p[pilots[k]]));return mass};
const propensity=(bit,alpha)=>{const a=F(alpha),den=A(two,M(two,a));const k0=(bit&1?1:0)+(bit&2?1:0),k1=(bit&4?1:0)+(bit&8?1:0);return [D(A(F(k0),a),den),D(A(F(k1),a),den)]};

const conditions=[],conditional=[];let probMutation=false;
for(const world of worlds){
 const wr=rows.filter(r=>r.world===world),first=wr[0];
 const p=first.oracle_all_eight_true_individual_propensity_NOT_ESTIMATOR_INPUT.split("|").map(F);
 const publicE=first.public_observed_X_propensity.split("|").map(F);
 const y0=first.auditor_all_eight_Y0_NOT_ESTIMATOR_INPUT.split("|").map(F);
 const y1=first.auditor_all_eight_Y1_NOT_ESTIMATOR_INPUT.split("|").map(F);
 const valid=publicE.every(q=>q.n>0n&&q.n<q.d);
 const pilotRows=Array.from({length:16},(_,bits)=>({bits,w:probability(bits,p)}));
 if(!eq(pilotRows.reduce((s,r)=>A(s,r.w),zero),one))throw Error("pilot mass");
 let baseline=null;
 if(valid){
  const mean=Array.from({length:8},(_,i)=>A(M(p[i],D(y1[i],publicE[i])),M(F(-1),M(N(one,p[i]),D(y0[i],N(one,publicE[i])))))).reduce(A,zero);
  const bm=D(mean,eight);
  const bv=D(Array.from({length:8},(_,i)=>M(M(p[i],N(one,p[i])),M(A(D(y1[i],publicE[i]),D(y0[i],N(one,publicE[i]))),A(D(y1[i],publicE[i]),D(y0[i],N(one,publicE[i])))))).reduce(A,zero),F(64));
  baseline={mean:S(bm),variance:S(bv),mse:S(A(bv,M(N(bm,two),N(bm,two))))};
 }
 for(const alpha of alphas){
  let aggregateMean=zero,aggregateSecond=zero;
  for(const pilot of pilotRows){
   const q=propensity(pilot.bits,alpha);
   if(!valid){conditional.push({world,alpha,pilot_bits:pilot.bits,pilot_probability:S(pilot.w),e_hat_X0:S(q[0]),e_hat_X1:S(q[1]),status:"NO_ORIGINAL_OVERLAP",mean:null,variance:null,mse:null});continue}
   const meanTerms=[],varTerms=[];
   for(let i=0;i<8;i++){
    const qi=q[i<4?0:1];
    meanTerms.push(N(M(p[i],D(y1[i],qi)),M(N(one,p[i]),D(y0[i],N(one,qi)))));
    const influence=A(D(y1[i],qi),D(y0[i],N(one,qi)));
    varTerms.push(M(M(p[i],N(one,p[i])),M(influence,influence)));
   }
   const mean=D(meanTerms.reduce(A,zero),eight);
   const variance=D(varTerms.reduce(A,zero),F(64));
   const mse=A(variance,M(N(mean,two),N(mean,two)));
   conditional.push({world,alpha,pilot_bits:pilot.bits,pilot_probability:S(pilot.w),e_hat_X0:S(q[0]),e_hat_X1:S(q[1]),status:"OK",mean:S(mean),variance:S(variance),mse:S(mse)});
   aggregateMean=A(aggregateMean,M(pilot.w,mean));
   aggregateSecond=A(aggregateSecond,M(pilot.w,A(variance,M(mean,mean))));
   if(!probMutation&&pilot.bits===0&&world==="CORRECT_X"){
    const old=varTerms[0],pi=p[0],mutated=A(pi,F("1/1000")),q0=q[0];
    const inf=A(D(y1[0],q0),D(y0[0],N(one,q0)));
    const changed=M(M(mutated,N(one,mutated)),M(inf,inf));
    probMutation=!eq(old,changed);
   }
  }
  if(!valid){conditions.push({world,alpha,status:"NO_ORIGINAL_OVERLAP",pilot_mass:"1",future_source_count:wr.length,mean:null,bias:null,variance:null,mse:null,original_public_HT_baseline:null});continue}
  const variance=N(aggregateSecond,M(aggregateMean,aggregateMean)),bias=N(aggregateMean,two),mse=A(variance,M(bias,bias));
  conditions.push({world,alpha,status:"OK",pilot_mass:"1",future_source_count:wr.length,mean:S(aggregateMean),bias:S(bias),variance:S(variance),mse:S(mse),original_public_HT_baseline:baseline});
 }
}
if(!probMutation)throw Error("p mutation failed");
return {research:"B_R219_S15",method:"independent Bernoulli conditional moments and law of total variance",conditions,conditional,checks:{true_probability_mutation_detected:probMutation},evidence:"E1_ARTIFICIAL"};

}
if(require.main===module){if(!process.argv[2])throw Error("usage: node script.js R219_original.csv");process.stdout.write(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}
module.exports={compute};
