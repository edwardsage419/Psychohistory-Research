#!/usr/bin/env node
"use strict";
// R159 E1 exact BigInt centered-cubic audit. Node 18+; input is the immutable R159 archive JSON.
function auditR159(doc){
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n};
  const Q=(n,d=1n)=>{if(typeof n==="string"){const p=n.split("/");return Q(BigInt(p[0]),p.length===2?BigInt(p[1]):1n)}if(typeof n==="number")n=BigInt(n);if(typeof d==="number")d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return[n/g,d/g]};
  const add=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const neg=x=>[-x[0],x[1]];
  const sub=(x,y)=>add(x,neg(y));
  const mul=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
  const div=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
  const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
  const cmp=(x,y)=>x[0]*y[1]<y[0]*x[1]?-1:x[0]*y[1]>y[0]*x[1]?1:0;
  const S=x=>x[1]===1n?x[0].toString():x[0]+"/"+x[1];
  const Z=Q(0),O=Q(1),T=Q(2),H=Q(1n,2n);
  const polynomial=p=>sub(mul(Q(3),mul(p,p)),mul(Q(2),mul(mul(p,p),p)));
  const step=(p,h,u)=>add(mul(sub(O,u),add(mul(sub(O,h),p),mul(h,polynomial(p)))),div(u,T));
  const gridH=["0","1/4","1/2","1"],gridU=["0","1/10","1/4"];
  const rows=[];
  for(const hs of gridH)for(const us of gridU){
    const h=Q(hs),u=Q(us),a=mul(sub(O,u),add(O,div(h,T))),b=mul(T,mul(sub(O,u),h)),delta=sub(a,O);
    const status=eq(h,Z)&&eq(u,Z)?"neutral_continuum":cmp(delta,Z)>0?"bistable":"central_only";
    const x2=status==="bistable"?div(delta,b):null;
    if(status==="bistable"){
      if(cmp(x2,Z)<=0||cmp(x2,Q(1n,4n))>0)throw Error("equilibrium outside [0,1]");
      if(cmp(a,O)<=0)throw Error("bistable center not unstable");
      const slope=sub(Q(3),mul(T,a));
      if(cmp(slope,Z)<0||cmp(slope,O)>=0)throw Error("outer fixed point not attracting");
    }
    if(status==="central_only"&&cmp(a,O)>=0)throw Error("center not strictly stable");
    for(let k=0;k<=100;k++){
      const p=Q(BigInt(k),100n),x=sub(p,H),xn=sub(step(p,h,u),H);
      const cubic=sub(mul(a,x),mul(b,mul(mul(x,x),x)));
      if(!eq(xn,cubic))throw Error("centered cubic identity failed");
    }
    rows.push({h:hs,u:us,a:S(a),b:S(b),critical_u:h[0]===0n?null:S(div(h,add(h,T))),regime:status,outer_x_squared:x2?S(x2):null,center_slope:S(a),outer_slope:status==="bistable"?S(sub(Q(3),mul(T,a))):null});
  }
  if(doc.research_id!=="R159"||doc.scenario_count!==48||doc.worlds.length!==48)throw Error("source ledger identity/count");
  const seen=new Set();let observations=0,transitions=0,majorityChecks=0,mutantReset=0,mutantCopy=0;
  const byId=new Map();
  for(const w of doc.worlds){
    if(seen.has(w.case_id))throw Error("duplicate world");seen.add(w.case_id);byId.set(w.case_id,w);
    const h=Q(w.conformity_fraction),u=Q(w.symmetric_innovation_reset);
    let p=Q(w.initial_frequency);
    if(w.points.length!==7)throw Error("unexpected horizon");
    for(let t=0;t<7;t++){
      const row=w.points[t],actual=Q(row.trait_A_frequency);
      if(row.t!==t||!eq(actual,p))throw Error("archive frequency mismatch "+w.case_id+" "+t);
      const c=Q(row.independent_three_demo_majority);
      if(!eq(c,polynomial(p)))throw Error("archive majority mismatch "+w.case_id+" "+t);
      observations++;majorityChecks++;
      if(t<6){
        const trueNext=step(p,h,u);
        const resetToCurrent=add(mul(sub(O,u),add(mul(sub(O,h),p),mul(h,polynomial(p)))),mul(u,p));
        const unbiased=add(mul(sub(O,u),p),div(u,T));
        if(!eq(resetToCurrent,trueNext))mutantReset++;
        if(!eq(unbiased,trueNext))mutantCopy++;
        p=trueNext;transitions++;
      }
    }
  }
  if(seen.size!==48||observations!==336||transitions!==288||majorityChecks!==336||mutantReset!==192||mutantCopy!==216)throw Error("predeclared counts not met "+[seen.size,observations,transitions,mutantReset,mutantCopy]);
  let mirrors=0;
  for(let hi=0;hi<4;hi++)for(let ui=0;ui<3;ui++){
    const l=byId.get(`p1_h${hi}_u${ui}`),r=byId.get(`p2_h${hi}_u${ui}`);
    for(let t=0;t<7;t++){if(!eq(add(Q(l.points[t].trait_A_frequency),Q(r.points[t].trait_A_frequency)),O))throw Error("mirror failure");mirrors++}
  }
  const counts={};for(const r of rows)counts[r.regime]=(counts[r.regime]||0)+1;
  if(counts.bistable!==7||counts.central_only!==4||counts.neutral_continuum!==1)throw Error("regime count");
  return {research:"R159",evidence:"E1_SYNTHETIC",source_archive_scenario_count:48,source_archive_observations_checked:observations,source_archive_transitions_checked:transitions,majority_polynomial_checks:majorityChecks,centered_identity_grid_checks:12*101,mirror_checks:mirrors,negative_reset_mutant_detected:mutantReset,negative_unbiased_copy_mutant_detected:mutantCopy,regime_counts:counts,parameter_rows:rows,source_model_unchanged:true,external_independent_replication:false};
}
const fs=require("node:fs");
if(process.argv.length!==3){console.error("Usage: node r159_centered_cubic_exact.js R159_EXACT_RESULTS.json");process.exit(2)}
console.log(JSON.stringify(auditR159(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));
