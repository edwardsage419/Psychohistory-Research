#!/usr/bin/env node
// Free standard-library synthetic or nonblind archival audit.
function audit(inputs){
"use strict";
const assert=(v,m)=>{if(!v)throw Error(m)};
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a};
const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);assert(b!==0n,"zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
const parse=s=>{const z=String(s).split("/");return q(z[0],z.length>1?z[1]:1)};
const st=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]);
const sub=(a,b)=>add(a,q(-b[0],b[1]));
const div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
const eq=(a,b)=>a[0]*b[1]===b[0]*a[1];
const one=q(1),two=q(2);
const weight=(p,k)=>k==="identity"?p:div(mul(p,p),add(mul(p,p),mul(two,mul(sub(one,p),sub(one,p)))));
const parseCsv=s=>{const lines=s.trimEnd().split("\n"),h=lines.shift().split(",");return lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[h[i],v])))};
function audit(atomText,original,comparisonText){
 const atoms=parseCsv(atomText),rows=parseCsv(comparisonText);
 assert(atoms.length===72&&rows.length===612&&original.outcomes.length===36,"row counts");
 const X=[-2,-1,1,2],P=[q(1,4),q(1,2),q(3,4)],lot=[];
 for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)for(const p of P)lot.push({low:X[i],high:X[j],p});
 const vals={};let checked=0;
 for(const k of ["identity","quadratic_asymmetric_noncanonical"]){
  for(let id=0;id<18;id++){
   const l=lot[id],world=id+(k==="identity"?0:18);
   const domain=l.low>0?"gain":l.high<0?"loss":"mixed";
   const lowW=domain==="gain"?sub(one,weight(sub(one,l.p),k)):weight(l.p,k);
   const highW=domain==="loss"?sub(one,lowW):weight(sub(one,l.p),k);
   const vLow=q(l.low<0?2*l.low:l.low),vHigh=q(l.high<0?2*l.high:l.high);
   const contrib=[mul(lowW,vLow),mul(highW,vHigh)],total=add(contrib[0],contrib[1]);
   const expected={world:String(world),transform:k,x_low:String(l.low),x_high:String(l.high),p_low:st(l.p),domain,lottery_value:st(total)};
   for(let idx=0;idx<2;idx++){
    const a=atoms[world*2+idx];
    const extra={outcome_index:String(idx),outcome:String(idx?l.high:l.low),outcome_probability:st(idx?sub(one,l.p):l.p),decision_weight:st(idx?highW:lowW),reference_value:st(idx?vHigh:vLow),weighted_contribution:st(contrib[idx])};
    for(const [field,val] of Object.entries({...expected,...extra})){assert(a[field]===val,"atom "+world+" "+idx+" "+field);checked++}
   }
   const o=original.outcomes[world];
   for(const [field,val] of Object.entries({transform:k,x_low:l.low,x_high:l.high,p_low:st(l.p),lottery_value:st(total)})){assert(String(o[field])===String(val),"original JSON "+world+" "+field);checked++}
   vals[k+":"+id]={...l,value:st(total)};
  }
 }
 const seen=new Set();
 for(const r of rows){
  const ai=Number(r.lottery_a),bi=Number(r.lottery_b),k=r.transform;
  assert(Number.isInteger(ai)&&ai>=0&&ai<18&&Number.isInteger(bi)&&bi>=0&&bi<18&&ai!==bi,"IDs");
  const key=k+":"+ai+":"+bi;assert(!seen.has(key),"duplicate");seen.add(key);
  const a=vals[k+":"+ai],b=vals[k+":"+bi];assert(a&&b,"transform");
  for(const [field,val] of Object.entries({a_low:String(a.low),a_high:String(a.high),a_p_low:st(a.p),b_low:String(b.low),b_high:String(b.high),b_p_low:st(b.p),cpt_value_a:a.value,cpt_value_b:b.value})){assert(r[field]===val,"comparison "+key+" "+field);checked++}
 }
 assert(seen.size===612,"complete");
 return {status:"PASS",sourceAtoms:72,originalValuations:36,orderedComparisons:612,fieldChecks:checked};
}
const good=audit(inputs.atoms,inputs.original,inputs.comparisons);
let rejected=0;
for(const mutation of ["atom_weight","comparison_value","duplicate_comparison"]){
 let a=inputs.atoms,c=inputs.comparisons;
 if(mutation==="atom_weight"){const lines=a.split("\n"),cells=lines[1].split(",");cells[9]="999";lines[1]=cells.join(",");a=lines.join("\n")}
 if(mutation==="comparison_value"){const lines=c.split("\n"),cells=lines[1].split(",");cells[10]="999";lines[1]=cells.join(",");c=lines.join("\n")}
 if(mutation==="duplicate_comparison"){const lines=c.trimEnd().split("\n");lines[2]=lines[1];c=lines.join("\n")+"\n"}
 try{audit(a,inputs.original,c)}catch(e){rejected++}
}
assert(rejected===3,"mutation escaped");
return {...good,mutationRejected:rejected,scope:"INTERNAL_NONBLIND_SOURCE_CHAIN_E1"};
}
const fs=require("node:fs"),path=require("node:path");
const read=p=>fs.readFileSync(path.resolve(__dirname,p),"utf8");
const inputs={atoms:read("../R318/R318_ALL_72_ORIGINAL_RANK_SIGN_OUTCOME_SOURCE_ATOMS.csv"),original:JSON.parse(read("../R318/R318_EXACT_36_TWO_OUTCOME_CPT_VALUES.json")),comparisons:read("../validation/R318_S114_ALL_612_ORDERED_COMPARISONS.csv")};
console.log(JSON.stringify(audit(inputs),null,2));
