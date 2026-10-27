#!/usr/bin/env node
// R219 S15: exact pilot x held-out assignment enumeration, Node >=18.
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

const conditional=[],conditions=[];
let validSlots=0,blockedSlots=0,pilotMutation=false,outcomeMutation=false;
for(const world of worlds){
 const wr=rows.filter(r=>r.world===world);
 const first=wr[0],p=first.oracle_all_eight_true_individual_propensity_NOT_ESTIMATOR_INPUT.split("|").map(F);
 const publicE=first.public_observed_X_propensity.split("|").map(F);
 const valid=publicE.every(q=>q.n>0n&&q.n<q.d);
 const evalRows=wr.map(r=>({z:r.all_eight_Z.split("|").map(Number),y:r.all_eight_actual_observed_Y.split("|").map(F),w:F(r.original_source_probability_exact),old:r.PUBLIC_HT_X_exact}));
 if(!eq(evalRows.reduce((s,r)=>A(s,r.w),zero),one))throw Error("future source mass");
 const pilotRows=Array.from({length:16},(_,bits)=>({bits,w:probability(bits,p)}));
 if(!eq(pilotRows.reduce((s,r)=>A(s,r.w),zero),one))throw Error("pilot source mass");
 let base=null;
 if(valid){
  const baseMean=evalRows.reduce((s,r)=>A(s,M(r.w,F(r.old))),zero);
  const baseVar=evalRows.reduce((s,r)=>A(s,M(r.w,M(N(F(r.old),baseMean),N(F(r.old),baseMean)))),zero);
  base={mean:S(baseMean),variance:S(baseVar),mse:S(A(baseVar,M(N(baseMean,two),N(baseMean,two))))};
 }
 for(const alpha of alphas){
  let sumMean=zero,sumSecond=zero;
  for(const pilot of pilotRows){
   const q=propensity(pilot.bits,alpha);
   if(!pilotMutation&&pilot.bits===0){pilotMutation=!eq(q[0],propensity(1,alpha)[0])}
   if(!valid){
    conditional.push({world,alpha,pilot_bits:pilot.bits,pilot_probability:S(pilot.w),e_hat_X0:S(q[0]),e_hat_X1:S(q[1]),status:"NO_ORIGINAL_OVERLAP",mean:null,variance:null,mse:null});
    blockedSlots++;
    continue;
   }
   let mean=zero,second=zero;
   for(const er of evalRows){
    let t=zero;
    for(let i=0;i<8;i++){
     const qi=q[i<4?0:1];
     const v=er.z[i]===1?D(er.y[i],qi):M(F(-1),D(er.y[i],N(one,qi)));
     t=A(t,v);
    }
    t=D(t,eight);
    mean=A(mean,M(er.w,t));
    second=A(second,M(er.w,M(t,t)));
    validSlots++;
   }
   const variance=N(second,M(mean,mean)),mse=A(variance,M(N(mean,two),N(mean,two)));
   if(variance.n<0n)throw Error("negative conditional variance");
   conditional.push({world,alpha,pilot_bits:pilot.bits,pilot_probability:S(pilot.w),e_hat_X0:S(q[0]),e_hat_X1:S(q[1]),status:"OK",mean:S(mean),variance:S(variance),mse:S(mse)});
   sumMean=A(sumMean,M(pilot.w,mean));sumSecond=A(sumSecond,M(pilot.w,second));
   if(!outcomeMutation){const test=evalRows.find(r=>r.w.n>0n);const idx=0;const delta=D(one,M(eight,test.z[idx]===1?q[0]:N(one,q[0])));outcomeMutation=delta.n!==0n;}
  }
  if(!valid){conditions.push({world,alpha,status:"NO_ORIGINAL_OVERLAP",pilot_mass:"1",future_source_count:wr.length,mean:null,bias:null,variance:null,mse:null,original_public_HT_baseline:null});continue}
  const variance=N(sumSecond,M(sumMean,sumMean)),bias=N(sumMean,two),mse=A(variance,M(bias,bias));
  conditions.push({world,alpha,status:"OK",pilot_mass:"1",future_source_count:wr.length,mean:S(sumMean),bias:S(bias),variance:S(variance),mse:S(mse),original_public_HT_baseline:base});
 }
}
if(validSlots!==40960||blockedSlots!==32||!pilotMutation||!outcomeMutation)throw Error("frozen slot/control mismatch "+[validSlots,blockedSlots,pilotMutation,outcomeMutation]);
return {research:"R219_S15",evidence:"E1_ARTIFICIAL",original_source_blob:"fa14af5a46694c6cc23717f8e9ee9fa2acb9501d",original_assignment_rows:1281,pilot_patterns_per_world:16,pilot_indices:[0,2,4,6],alphas,valid_future_pilot_slots:validSlots,blocked_pilot_slots:blockedSlots,conditions,conditional,checks:{pilot_bit_mutation_detected:pilotMutation,outcome_mutation_detected:outcomeMutation},new_E2:0,new_E3:0};

}
if(require.main===module){if(!process.argv[2])throw Error("usage: node script.js R219_original.csv");process.stdout.write(JSON.stringify(compute(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}
module.exports={compute};
