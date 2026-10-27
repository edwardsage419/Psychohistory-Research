"use strict";
const fs=typeof require==="function"?require("fs"):null;
function run(csv,receipt){
 let checks=0;function assert(x,m){checks++;if(!x)throw Error(m)}
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a||1n};
 class F{
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(!d)throw Error("zero");let g=gcd(n,d);this.n=n/g;this.d=d/g}
  static of(s){let x=String(s).split("/");return new F(x[0],x[1]||"1")}
  add(y){return new F(this.n*y.d+y.n*this.d,this.d*y.d)}
  sub(y){return new F(this.n*y.d-y.n*this.d,this.d*y.d)}
  mul(y){return new F(this.n*y.n,this.d*y.d)}
  div(y){return new F(this.n*y.d,this.d*y.n)}
  abs(){return new F(this.n<0n?-this.n:this.n,this.d)}
  eq(y){return this.n===y.n&&this.d===y.d}
  ge(y){return this.n*y.d>=y.n*this.d}
  toString(){return this.d===1n?""+this.n:this.n+"/"+this.d}
 }
 const O=new F(1),Z=new F(0);
 const lines=csv.trim().split(/\r?\n/),keys=lines.shift().split(","),groups=new Map();
 for(let line of lines){
  const fields=line.split(",");assert(fields.length===keys.length,"CSV width");
  const r=Object.fromEntries(keys.map((k,i)=>[k,fields[i]])),z=+r.instrument_assignment_Z,d=+r.observed_actual_D;
  assert(d===+r[z?"potential_D_if_Z1":"potential_D_if_Z0"],"source D");
  assert(+r.observed_actual_Y_exact===+r[d?"potential_Y_if_D1_without_direct_Z_exact":"potential_Y_if_D0_without_direct_Z_exact"]+z*(+r.direct_outcome_effect_of_Z_exact),"source Y");
  const q=F.of(r.person_specific_instrument_propensity_exact);
  assert(F.of(r.joint_source_probability_exact).eq((z?q:O.sub(q)).div(new F(8))),"source weight");
  if(!groups.has(r.world))groups.set(r.world,new Map());
  const people=groups.get(r.world),i=+r.latent_source_person_i;
  if(!people.has(i))people.set(i,{});
  assert(!people.get(i)[z],"unique source");people.get(i)[z]=r;
 }
 assert(lines.length===128&&groups.size===8,"source size");
 const fields=["assignment_count","assignment_probability_sum_exact","empty_arm_count","empty_arm_probability_exact","zero_sample_first_stage_count","zero_sample_first_stage_probability_exact","defined_count","defined_probability_exact","wald_mean_conditional_defined_exact","max_absolute_defined_wald_exact","absolute_wald_at_least_10_unconditional_probability_exact","absolute_wald_at_least_10_conditional_defined_probability_exact","absolute_wald_minus_late_at_least_2_unconditional_probability_exact","absolute_wald_minus_late_at_least_2_conditional_defined_probability_exact"];
 let matches=0;const summary={};
 for(let [world,people] of groups){
  assert(people.size===8,"eight people");
  const pairs=Array.from({length:8},(_,i)=>{const p=people.get(i);assert(p&&p[0]&&p[1],"source pair");return p});
  const comp=pairs.filter(p=>p[0].principal_stratum_type==="COMPLIER");
  const late=comp.length?comp.reduce((s,p)=>s.add(F.of(p[0].source_unit_treatment_effect_exact)),Z).div(new F(comp.length)):null;
  let counts=[0,0,0],masses=[Z,Z,Z],sum=Z,mean=Z,tail=Z,gap=Z,max=Z;
  for(let bits=0;bits<256;bits++){
   let n1=0,d1=0,d0=0,y1=0,y0=0,p=O;
   for(let i=0;i<8;i++){
    const z=(bits>>i)&1,row=pairs[i][z],q=F.of(pairs[i][0].person_specific_instrument_propensity_exact);
    p=p.mul(z?q:O.sub(q));
    if(z){n1++;d1+=+row.observed_actual_D;y1+=+row.observed_actual_Y_exact}
    else{d0+=+row.observed_actual_D;y0+=+row.observed_actual_Y_exact}
   }
   sum=sum.add(p);const n0=8-n1,den=d1*n0-d0*n1;
   let state=0;
   if(n1&&n0){
    if(!den)state=1;
    else{
     state=2;const ratio=new F(y1*n0-y0*n1,den);
     mean=mean.add(p.mul(ratio));if(ratio.abs().ge(new F(10)))tail=tail.add(p);
     if(late&&ratio.sub(late).abs().ge(new F(2)))gap=gap.add(p);
     if(ratio.abs().ge(max))max=ratio.abs();
    }
   }
   counts[state]++;masses[state]=masses[state].add(p);
  }
  assert(sum.eq(O),"prob mass");assert(counts.reduce((a,b)=>a+b,0)===256,"assignment partition");
  assert(masses.reduce((a,b)=>a.add(b),Z).eq(O),"mass partition");
  const v={
   assignment_count:256,assignment_probability_sum_exact:sum.toString(),
   empty_arm_count:counts[0],empty_arm_probability_exact:masses[0].toString(),
   zero_sample_first_stage_count:counts[1],zero_sample_first_stage_probability_exact:masses[1].toString(),
   defined_count:counts[2],defined_probability_exact:masses[2].toString(),
   wald_mean_conditional_defined_exact:mean.div(masses[2]).toString(),max_absolute_defined_wald_exact:max.toString(),
   absolute_wald_at_least_10_unconditional_probability_exact:tail.toString(),
   absolute_wald_at_least_10_conditional_defined_probability_exact:tail.div(masses[2]).toString(),
   absolute_wald_minus_late_at_least_2_unconditional_probability_exact:late?gap.toString():"NOT_APPLICABLE_NO_COMPLIERS",
   absolute_wald_minus_late_at_least_2_conditional_defined_probability_exact:late?gap.div(masses[2]).toString():"NOT_APPLICABLE"
  };
  const old=receipt.summary_worlds.find(w=>w.world===world);assert(!!old,"receipt world");
  for(let k of fields){assert(String(v[k])===String(old[k]),world+" "+k);matches++}
  summary[world]={empty:counts[0],zero:counts[1],defined:counts[2],conditional_mean:v.wald_mean_conditional_defined_exact};
 }
 assert(receipt.summary_worlds.length===8,"world count");
 return {checks,failed:0,source_rows:lines.length,worlds:8,assignments:2048,exact_receipt_fields:matches,summary};
}
if(fs&&typeof require!=="undefined"&&require.main===module){
 if(process.argv.length!==4)throw Error("Usage: node script.js SOURCE.csv R_RECEIPT.json");
 console.log(JSON.stringify(run(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));
}