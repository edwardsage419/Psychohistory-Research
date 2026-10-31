#!/usr/bin/env node
"use strict";
// Independent nonblind R318 S114 exact Fraction-style oracle. No imports from R scorer.
const fs=require("node:fs"),path=require("node:path");
const audit=function audit(csv,summary){
  const assert=(ok,m)=>{if(!ok)throw Error(m)};
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a};
  const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);assert(b!==0n,"zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
  const parse=s=>{let [a,b]=String(s).split("/");return Q(a,b===undefined?1:b)};
  const add=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),mul=(x,y)=>Q(x[0]*y[0],x[1]*y[1]),neg=x=>Q(-x[0],x[1]),sub=(x,y)=>add(x,neg(y)),div=(x,y)=>Q(x[0]*y[1],x[1]*y[0]),cmp=(x,y)=>x[0]*y[1]>y[0]*x[1]?1:x[0]*y[1]<y[0]*x[1]?-1:0,st=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
  const one=Q(1),zero=Q(0),X=[-2,-1,1,2],p=[Q(1,4),Q(1,2),Q(3,4)],lot=[];
  for(let i=0;i<X.length;i++)for(let j=i+1;j<X.length;j++)for(let z of p)lot.push({a:X[i],b:X[j],p:z});
  const W=(x,k)=>{if(k==="identity")return x;assert(k==="quadratic_asymmetric_noncanonical","unknown transform");const n=x[0],d=x[1];return Q(n*n,n*n+2n*(d-n)*(d-n))};
  const value=x=>Q(x>0?x:2*x);
  const score=(l,k,norm=false)=>{let low,high;if(l.b<0){low=W(l.p,k);high=sub(one,low)}else if(l.a>0){high=W(sub(one,l.p),k);low=sub(one,high)}else{low=W(l.p,k);high=W(sub(one,l.p),k)}let s=add(mul(low,value(l.a)),mul(high,value(l.b)));return norm&&l.a<0&&l.b>0?div(s,add(low,high)):s};
  const tail=(l,t)=>add(l.a>t?l.p:zero,l.b>t?sub(one,l.p):zero);
  const dominates=(x,y)=>X.every(t=>cmp(tail(x,t),tail(y,t))>=0)&&X.some(t=>cmp(tail(x,t),tail(y,t))>0);
  const cols=["transform","lottery_a","lottery_b","a_low","a_high","a_p_low","b_low","b_high","b_p_low","fosd_a_over_b","cpt_value_a","cpt_value_b","cpt_delta","normalized_value_a","normalized_value_b","normalized_delta","normalized_fosd_violation"];
  const lines=csv.trimEnd().split("\n");assert(lines[0]===cols.join(","),"header");assert(lines.length===613,"row count");
  const seen=new Set(),stat={},signs={},witnesses=[];
  for(let i=1;i<lines.length;i++){
    const cells=lines[i].split(",");assert(cells.length===17,"width");const row=Object.fromEntries(cols.map((c,j)=>[c,cells[j]]));
    const k=row.transform,ai=Number(row.lottery_a),bi=Number(row.lottery_b);
    assert(["identity","quadratic_asymmetric_noncanonical"].includes(k),"transform");assert(Number.isInteger(ai)&&ai>=0&&ai<18&&Number.isInteger(bi)&&bi>=0&&bi<18&&ai!==bi,"indices");
    const key=k+":"+ai+":"+bi;assert(!seen.has(key),"duplicate");seen.add(key);
    const la=lot[ai],lb=lot[bi];
    assert(row.a_low===String(la.a)&&row.a_high===String(la.b)&&row.a_p_low===st(la.p)&&row.b_low===String(lb.a)&&row.b_high===String(lb.b)&&row.b_p_low===st(lb.p),"source keys");
    const dom=dominates(la,lb),va=score(la,k),vb=score(lb,k),na=score(la,k,true),nb=score(lb,k,true),d=sub(va,vb),nd=sub(na,nb),bad=dom&&cmp(nd,zero)<=0;
    const expected=[Number(dom),st(va),st(vb),st(d),st(na),st(nb),st(nd),Number(bad)].map(String);
    const actual=["fosd_a_over_b","cpt_value_a","cpt_value_b","cpt_delta","normalized_value_a","normalized_value_b","normalized_delta","normalized_fosd_violation"].map(c=>row[c]);
    assert(JSON.stringify(actual)===JSON.stringify(expected),"arithmetic "+key);
    if(!stat[k])stat[k]={rows:0,fosd:0,cpt_fosd_violations:0,normalized_fosd_violations:0,normalized_sign_differences_ordered:0};
    const s=stat[k];s.rows++;if(dom){s.fosd++;if(cmp(d,zero)<=0)s.cpt_fosd_violations++;if(bad){s.normalized_fosd_violations++;witnesses.push({transform:k,lottery_a:ai,lottery_b:bi,actual_delta:st(d),normalized_delta:st(nd)})}}
    if(cmp(d,zero)!==cmp(nd,zero))s.normalized_sign_differences_ordered++;
    if(ai<bi)signs[key]=cmp(d,zero);
  }
  assert(seen.size===612,"coverage");
  for(const k of ["identity","quadratic_asymmetric_noncanonical"])for(let i=0;i<18;i++)for(let j=0;j<18;j++)if(i!==j)assert(seen.has(k+":"+i+":"+j),"missing key");
  const rank={unordered_pairs:153,strict_reversals:0,ties_any:0,sign_disagreement:0};
  for(let i=0;i<18;i++)for(let j=i+1;j<18;j++){let x=signs["identity:"+i+":"+j],y=signs["quadratic_asymmetric_noncanonical:"+i+":"+j];if(x*y===-1)rank.strict_reversals++;if(x===0||y===0)rank.ties_any++;if(x!==y)rank.sign_disagreement++}
  assert(summary.schema==="r318_s114_fosd_exact_v1"&&summary.prescore_commit==="c12d3c90d447bd43963332be3f6d3e076a47bf78"&&summary.evidence==="E1_SYNTHETIC_ONLY"&&summary.real_E2===0&&summary.historical_E3===0&&summary.external_independent_replication==="NOT_RUN"&&summary.original_R318_status==="UNCHANGED","metadata");
  assert(summary.lotteries===18&&summary.ordered_comparisons===612,"size summary");
  assert(JSON.stringify(summary.per_transform)===JSON.stringify(stat),"stats");
  assert(JSON.stringify(summary.rank_comparison)===JSON.stringify(rank),"ranks");
  assert(JSON.stringify(summary.normalization_negative_control_witnesses)===JSON.stringify(witnesses),"witnesses");
  return {status:"PASS",rows:612,source_identities:18,stat,rank,witnesses};
};
const root=path.resolve(__dirname,"../validation");
const csv=fs.readFileSync(path.join(root,"R318_S114_ALL_612_ORDERED_COMPARISONS.csv"),"utf8");
const summary=JSON.parse(fs.readFileSync(path.join(root,"R318_S114_EXACT_SUMMARY.json"),"utf8"));
const r=audit(csv,summary);
if(process.argv.includes("--mutations")){
 const tests=[
 ["remove_row",()=>csv.trimEnd().split("\n").slice(0,-1).join("\n")+"\n",()=>summary],
 ["duplicate_row",()=>csv+csv.split("\n")[1]+"\n",()=>summary],
 ["change_cpt_delta",()=>{let z=csv.split("\n"),f=z[1].split(",");f[12]="999";z[1]=f.join(",");return z.join("\n")},()=>summary],
 ["flip_fosd",()=>{let z=csv.split("\n"),f=z[2].split(",");f[9]=f[9]==="1"?"0":"1";z[2]=f.join(",");return z.join("\n")},()=>summary],
 ["flip_negative_control",()=>{let z=csv.split("\n"),f=z[5].split(",");f[16]=f[16]==="1"?"0":"1";z[5]=f.join(",");return z.join("\n")},()=>summary],
 ["swap_transform",()=>{let z=csv.split("\n"),f=z[5].split(",");f[0]="quadratic_asymmetric_noncanonical";z[5]=f.join(",");return z.join("\n")},()=>summary],
 ["tamper_aggregate",()=>csv,()=>({...summary,rank_comparison:{...summary.rank_comparison,strict_reversals:0}})],
 ["promote_e2",()=>csv,()=>({...summary,real_E2:1})]
 ];
 for(const [name,cfn,sfn] of tests){let failed=false;try{audit(cfn(),sfn())}catch(e){failed=true}if(!failed)throw Error("mutation escaped "+name)}
 console.log("PASS 8/8 mutation controls");
}
console.log("PASS independent exact 612 rows "+JSON.stringify(r.rank));
