"use strict";
/* Exact R167 one-step reversal threshold. Node.js 18+, standard library only. */
const fs=require("node:fs");
const path=require("node:path");
function compute(raw){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;};
 const f=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(!b)throw Error("zero denom");let g=gcd(a,b);return [a/g,b/g];};
 const p=s=>{let z=String(s).split("/");return f(z[0],z[1]||"1");};
 const a=(x,y)=>f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const n=(x)=>f(-x[0],x[1]);
 const s=(x,y)=>a(x,n(y));
 const m=(x,y)=>f(x[0]*y[0],x[1]*y[1]);
 const d=(x,y)=>f(x[0]*y[1],x[1]*y[0]);
 const cmp=(x,y)=>{let q=x[0]*y[1]-y[0]*x[1];return q>0n?1:q<0n?-1:0;};
 const st=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
 const z=f(0),o=f(1),two=f(2),deltaPos=p("1/4");
 const calc=(a0,b0,x,y,delta,kappa)=>{
   const q0=s(a0,m(delta,m(a0,s(o,a0)))),q1=s(b0,m(delta,m(b0,s(o,b0))));
   const r0=a(o,m(kappa,a0)),r1=a(o,m(kappa,b0)),den=a(m(x,r0),m(y,r1));
   const nx=d(m(x,r0),den),ny=d(m(y,r1),den);
   const mean0=a(m(x,a0),m(y,b0)),mean1=a(m(nx,q0),m(ny,q1));
   return {q0,q1,nx,ny,mean0,mean1,within:a(m(x,s(q0,a0)),m(y,s(q1,b0))),between:s(mean1,a(m(x,q0),m(y,q1))),total:s(mean1,mean0)};
 };
 let comparisons=0,thresholdTests=0,deltaPositive=0,finiteThresholdWorlds=0,impossibleThresholdWorlds=0,reversalWorlds=0,zeroWorlds=0,positiveCases=[],records=[],boundaryTests=0,controls=0;
 for(const w of raw.worlds){
  let [aa,bb]=w.initial_fractions.map(p),y=p(w.initial_high_group_weight),x=s(o,y),delta=p(w.within_delta),kappa=f(w.between_kappa);
  let S=a(m(x,m(aa,s(o,aa))),m(y,m(bb,s(o,bb)))),mean=a(m(x,aa),m(y,bb)),C=s(o,m(delta,s(o,a(aa,bb)))),gap=s(bb,aa);
  let W=n(m(delta,S)), B=d(m(m(m(m(x,y),kappa),m(gap,gap)),C),a(o,m(kappa,mean))),T=a(W,B);
  let dr=calc(aa,bb,x,y,delta,kappa),orig=w.points[1];
  const pairs=[[W,dr.within],[B,dr.between],[T,dr.total],[dr.mean1,p(orig.overall_A)],[dr.q0,p(orig.A_in_lower_group)],[dr.q1,p(orig.A_in_higher_group)],[dr.nx,p(orig.group_low_weight)],[dr.ny,p(orig.group_high_weight)],[W,p(orig.within_component)],[B,p(orig.between_component)],[T,p(orig.total_change)]];
  for(const [left,right] of pairs){comparisons++;if(cmp(left,right))throw Error("archival mismatch "+w.id+" "+st(left)+" "+st(right));}
  if(w.between_kappa===0){controls++;if(cmp(B,z))throw Error("kappa zero B");}
  if(cmp(aa,bb)===0){controls++;if(cmp(B,z))throw Error("equal frequency B");}
  let threshold=null, status="NOT_APPLICABLE_DELTA_NONPOSITIVE";
  if(cmp(delta,z)>0){
    deltaPositive++;
    const D=s(m(m(m(x,y),m(gap,gap)),C),m(m(delta,S),mean));
    if(cmp(D,z)>0){
      finiteThresholdWorlds++;let critical=d(m(delta,S),D);threshold=st(critical);
      let predicted=cmp(kappa,critical);let actual=cmp(T,z);thresholdTests++;
      if(predicted!==actual)throw Error("threshold sign mismatch "+w.id);
      if(actual>0){reversalWorlds++;positiveCases.push(w.id);}
      if(actual===0)zeroWorlds++;
      for(const [tag,kk] of [["below",d(critical,two)],["equal",critical],["above",a(critical,o)]]){
        let r=calc(aa,bb,x,y,delta,kk);let actual2=cmp(r.total,z);let expected=tag==="below"?-1:tag==="equal"?0:1;
        if(actual2!==expected)throw Error("independent boundary mismatch "+w.id+" "+tag+" "+st(r.total));
        boundaryTests++;
      }
      status="FINITE_CRITICAL_KAPPA";
    }else{
      impossibleThresholdWorlds++;thresholdTests++;
      if(cmp(T,z)>=0)throw Error("impossible threshold sign mismatch "+w.id);
      status="NO_FINITE_NONNEGATIVE_KAPPA_REVERSAL";
    }
  }
  records.push({id:w.id,delta:w.within_delta,kappa:w.between_kappa,within:st(W),between:st(B),net:st(T),critical_kappa:threshold,threshold_status:status});
 }
 if(raw.worlds.length!==72||comparisons!==72*11||deltaPositive!==24||thresholdTests!==24)throw Error("unexpected fixed grid size");
 let aa=p("1/4"),bb=p("3/4"),x=p("1/2"),y=p("1/2"),del=p("1/4");
 const example=["1","6/5","2"].map(k=>({kappa:k,net:st(calc(aa,bb,x,y,del,p(k)).total)}));
 if(example.map(e=>e.net).join(",")!=="-1/192,0,1/64")throw Error("prespecified example mismatch "+JSON.stringify(example));
 return {research_id:"R167",date:"2026-10-26",protocol:"protocols/R167_KAPPA_REVERSAL_CRITICAL_THRESHOLD_THIRD_METHOD_FREEZE_2026-10-26.md",evidence:"E1_SYNTHETIC_ONLY",original_frozen_R167_blob:"86839d8d473e4aee2f450d8c598797299ec1cf41",worlds:72,exact_archival_scalar_comparisons:comparisons,delta_positive_worlds:deltaPositive,threshold_sign_tests:thresholdTests,finite_threshold_worlds:finiteThresholdWorlds,impossible_threshold_worlds:impossibleThresholdWorlds,strict_reversal_worlds:reversalWorlds,zero_net_worlds:zeroWorlds,independent_direct_weight_boundary_tests:boundaryTests,negative_controls:controls,example,positive_world_ids:positiveCases,records,claim_limit:"conditional exact one-step two-group toy theorem; no E2/E3; no external independent replication"};
}
const input=path.join(__dirname,"../R167/R167_EXACT_RESULTS.json");
const raw=JSON.parse(fs.readFileSync(input,"utf8"));
console.log(JSON.stringify(compute(raw),null,2));
