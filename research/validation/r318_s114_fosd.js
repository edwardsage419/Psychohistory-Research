#!/usr/bin/env node
"use strict";
// R318 S114 finite exact rational FOSD audit. No packages, no floating point.
const fs=require("node:fs"),path=require("node:path");
const compute=function compute(){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a};
  const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}if(b===0n)throw Error("zero denominator");let g=gcd(a,b);return [a/g,b/g]};
  const add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const neg=x=>[-x[0],x[1]];
  const sub=(x,y)=>add(x,neg(y));
  const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
  const div=(x,y)=>q(x[0]*y[1],x[1]*y[0]);
  const cmp=(x,y)=>{let z=x[0]*y[1]-y[0]*x[1];return z>0n?1:z<0n?-1:0};
  const st=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
  const Z=q(0),O=q(1),T=q(2),P=[q(1,4),q(1,2),q(3,4)];
  const X=[-2,-1,1,2],L=[];
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)for(const p of P)L.push({id:L.length,a:X[i],b:X[j],p});
  const value=x=>q(x>0?x:2*x);
  const w=(p,k)=>k==="identity"?p:div(mul(p,p),add(mul(p,p),mul(T,mul(sub(O,p),sub(O,p)))));
  const weights=(l,k)=>l.a>0?[sub(O,w(sub(O,l.p),k)),w(sub(O,l.p),k)]:l.b<0?[w(l.p,k),sub(O,w(l.p,k))]:[w(l.p,k),w(sub(O,l.p),k)];
  const val=(l,k,normalize=false)=>{let [a,b]=weights(l,k),v=add(mul(a,value(l.a)),mul(b,value(l.b)));return normalize&&l.a<0&&l.b>0?div(v,add(a,b)):v};
  const cdf=(l,t)=>add(l.a<=t?l.p:Z,l.b<=t?sub(O,l.p):Z);
  const fosd=(a,b)=>X.every(t=>cmp(cdf(a,t),cdf(b,t))<=0)&&X.some(t=>cmp(cdf(a,t),cdf(b,t))<0);
  const kinds=["identity","quadratic_asymmetric_noncanonical"];
  const cols=["transform","lottery_a","lottery_b","a_low","a_high","a_p_low","b_low","b_high","b_p_low","fosd_a_over_b","cpt_value_a","cpt_value_b","cpt_delta","normalized_value_a","normalized_value_b","normalized_delta","normalized_fosd_violation"];
  const rows=[cols.join(",")], stats={}, signs={},witnesses=[],originalCheck=[];
  for(const k of kinds){
    let s={rows:0,fosd:0,cpt_fosd_violations:0,normalized_fosd_violations:0,normalized_sign_differences_ordered:0};
    for(const a of L)originalCheck.push({transform:k,x_low:a.a,x_high:a.b,p_low:st(a.p),lottery_value:st(val(a,k))});
    for(const a of L)for(const b of L){if(a.id===b.id)continue;
      let f=fosd(a,b),va=val(a,k),vb=val(b,k),d=sub(va,vb),na=val(a,k,true),nb=val(b,k,true),nd=sub(na,nb),bad=f&&cmp(nd,Z)<=0;
      rows.push([k,a.id,b.id,a.a,a.b,st(a.p),b.a,b.b,st(b.p),Number(f),st(va),st(vb),st(d),st(na),st(nb),st(nd),Number(bad)].join(","));
      s.rows++;if(f){s.fosd++;if(cmp(d,Z)<=0)s.cpt_fosd_violations++;if(bad){s.normalized_fosd_violations++;witnesses.push({transform:k,lottery_a:a.id,lottery_b:b.id,actual_delta:st(d),normalized_delta:st(nd)})}}
      if(cmp(d,Z)!==cmp(nd,Z))s.normalized_sign_differences_ordered++;
      if(a.id<b.id)signs[k+":"+a.id+":"+b.id]=cmp(d,Z);
    }
    stats[k]=s;
  }
  let ranks={unordered_pairs:153,strict_reversals:0,ties_any:0,sign_disagreement:0};
  for(let i=0;i<18;i++)for(let j=i+1;j<18;j++){
    let a=signs["identity:"+i+":"+j],b=signs["quadratic_asymmetric_noncanonical:"+i+":"+j];
    if(a*b===-1)ranks.strict_reversals++;if(a===0||b===0)ranks.ties_any++;if(a!==b)ranks.sign_disagreement++;
  }
  if(rows.length!==613||stats.identity.fosd!==117||stats.quadratic_asymmetric_noncanonical.fosd!==117||stats.quadratic_asymmetric_noncanonical.normalized_fosd_violations!==2||ranks.strict_reversals!==9)throw Error("independent crosscheck disagrees");
  const summary={schema:"r318_s114_fosd_exact_v1",prescore_commit:"c12d3c90d447bd43963332be3f6d3e076a47bf78",evidence:"E1_SYNTHETIC_ONLY",lotteries:18,ordered_comparisons:612,per_transform:stats,rank_comparison:ranks,normalization_negative_control_witnesses:witnesses,real_E2:0,historical_E3:0,external_independent_replication:"NOT_RUN",original_R318_status:"UNCHANGED"};
  return {csv:rows.join("\n")+"\n",summary,originalCheck};
};
const output=compute(),base=path.resolve(__dirname);
const csvPath=path.join(base,"R318_S114_ALL_612_ORDERED_COMPARISONS.csv");
const jsonPath=path.join(base,"R318_S114_EXACT_SUMMARY.json");
const original=JSON.parse(fs.readFileSync(path.resolve(base,"../R318/R318_EXACT_36_TWO_OUTCOME_CPT_VALUES.json"),"utf8"));
if(original.outcomes.length!==36)throw Error("original count");
for(let i=0;i<36;i++){
 const a=original.outcomes[i],b=output.originalCheck[i];
 for(const k of ["transform","x_low","x_high","p_low","lottery_value"])if(String(a[k])!==String(b[k]))throw Error("original source mismatch at "+i+" "+k);
}
const expectedJSON=JSON.stringify(output.summary,null,2)+"\n";
if(process.argv.includes("--check")){
 if(fs.readFileSync(csvPath,"utf8")!==output.csv)throw Error("CSV mismatch");
 if(fs.readFileSync(jsonPath,"utf8")!==expectedJSON)throw Error("JSON mismatch");
 console.log("PASS R318 S114 612 ordered comparisons, 117 FOSD per transform, 2 negative-control violations");
}else if(process.argv.includes("--emit")){
 fs.writeFileSync(csvPath,output.csv,{flag:"wx"});
 fs.writeFileSync(jsonPath,expectedJSON,{flag:"wx"});
 console.log("EMITTED");
}else console.log(expectedJSON);
