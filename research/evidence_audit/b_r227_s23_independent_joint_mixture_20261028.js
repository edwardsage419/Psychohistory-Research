"use strict";
/* B track: independent frozen-joint mixture, never invokes R track source enumerator.
   node research/evidence_audit/b_r227_s23_independent_joint_mixture_20261028.js */
const frac=s=>{const p=String(s).split("/");return reduce(BigInt(p[0]),BigInt(p[1]||1));};
function reduce(n,d){if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let a=n<0n?-n:n,b=d;while(b){const t=a%b;a=b;b=t;}return [n/a,d/a];}
const sum=(a,b)=>reduce(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const product=(a,b)=>reduce(a[0]*b[0],a[1]*b[1]);
const minus=(a,b)=>sum(a,[-b[0],b[1]]);
const divide=(a,b)=>reduce(a[0]*b[1],a[1]*b[0]);
const equal=(a,b)=>a[0]*b[1]===b[0]*a[1];
const out=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
const zero=[0n,1n],one=[1n,1n];
function audit(original,receipt){
  let checks=0;
  function assert(ok,msg){checks++;if(!ok)throw Error("audit mismatch "+msg);}
  assert(original.world_results.length===8,"original worlds");
  assert(receipt.conditions===40,"R condition count");
  assert(receipt.weighted_source_slots===5120,"R slots");
  const resultByKey=new Map(receipt.results.map(x=>[x.world+"|"+x.rho,x]));
  const jointBy={};
  for(const world of original.world_results){
    const marg=new Map();
    for(const [key,v] of Object.entries(world.single_observation_joint)){
      const [x,y]=key.split(",").map(Number),s=String(x+y);
      marg.set(s,sum(marg.get(s)||zero,frac(v)));
    }
    const base=new Map(Object.entries(world.retest_sum_joint).map(([k,v])=>[k,frac(v)]));
    const vScore=frac(world.variance_sum),trueVar=frac(world.true_score_variance);
    const alpha=frac(world.two_item_alpha),trueRel=frac(world.true_reliability_conditional_stable_trait);
    assert(equal(Array.from(marg.values()).reduce(sum,zero),one),world.world+" single normalization");
    for(const rho of ["0","1/8","1/4","1/2","1"]){
      const r=resultByKey.get(world.world+"|"+rho);
      assert(!!r,world.world+" "+rho+" present");
      const p=frac(rho),complement=minus(one,p);
      const keys=new Set([...base.keys(),...Array.from(marg.keys()).map(s=>s+","+s),...Object.keys(r.retest_joint)]);
      const j=new Map();
      for(const key of keys){
        const [s1,s2]=key.split(",");
        const expected=sum(product(complement,base.get(key)||zero),s1===s2?product(p,marg.get(s1)||zero):zero);
        const actual=frac(r.retest_joint[key]||"0");
        assert(equal(expected,actual),world.world+" "+rho+" joint "+key);
        if(expected[0]!==0n)j.set(key,expected);
      }
      const total=Array.from(j.values()).reduce(sum,zero);
      assert(equal(total,one),world.world+" "+rho+" normalization");
      const m1=new Map(),m2=new Map();
      let cross=zero;
      for(const [key,w] of j){
        const [s1,s2]=key.split(",").map(Number);
        m1.set(String(s1),sum(m1.get(String(s1))||zero,w));
        m2.set(String(s2),sum(m2.get(String(s2))||zero,w));
        cross=sum(cross,product(w,frac(s1*s2)));
      }
      for(const [s,w] of marg){assert(equal(m1.get(s)||zero,w),world.world+" "+rho+" first marginal "+s);assert(equal(m2.get(s)||zero,w),world.world+" "+rho+" second marginal "+s);}
      const mean=Array.from(marg).reduce((a,[s,w])=>sum(a,product(frac(Number(s)),w)),zero);
      const cov=minus(cross,product(mean,mean));
      const predictedCov=sum(product(complement,trueVar),product(p,vScore));
      const retest=divide(cov,vScore);
      const predictedR=sum(product(complement,trueRel),p);
      const bias=minus(retest,trueRel);
      assert(equal(cov,predictedCov),world.world+" "+rho+" covariance identity");
      assert(equal(retest,predictedR),world.world+" "+rho+" retest identity");
      for(const [key,value] of [["two_item_alpha",alpha],["true_reliability",trueRel],["cross_occasion_covariance",cov],["retest_correlation",retest],["retest_minus_true",bias],["single_score_variance",vScore],["total_probability",one]]){
        assert(equal(frac(r[key]),value),world.world+" "+rho+" "+key);
      }
      assert(r.positive_source_slots===(rho==="1"?16:128),world.world+" "+rho+" support");
      jointBy[world.world+"|"+rho]=j;
    }
  }
  const trait=jointBy["PERFECT_TRAIT|1"],method=jointBy["PERFECT_METHOD|1"];
  assert(trait.size===method.size,"two-occasion alias size");
  for(const [k,v] of trait)assert(equal(v,method.get(k)||zero),"two-occasion alias "+k);
  const changed=JSON.parse(JSON.stringify(receipt));
  const x=changed.results.find(r=>r.world==="PERFECT_METHOD"&&r.rho==="1/2");
  x.retest_joint["-2,-2"]="999";
  let mutationDetected=false;
  try{auditWithoutMutation(original,changed);}catch(e){mutationDetected=/audit mismatch/.test(String(e));}
  assert(mutationDetected,"mutated joint cell detected");
  return {audit:"B_R227_S23",date:"2026-10-28",status:"INTERNAL_INDEPENDENT_ALGORITHM_PASS",algorithm:"frozen baseline retest joint plus same-occasion diagonal marginal mixture",worlds:8,conditions:40,checks_passed:checks,checks_failed:0,mutation_test_detected:true,external_independent_reproduction:0,evidence:"E1_ARTIFICIAL_ONLY",new_E2:0,new_E3:0};
}
function auditWithoutMutation(original,receipt){
  const w=original.world_results.find(x=>x.world==="PERFECT_METHOD");
  const r=receipt.results.find(x=>x.world==="PERFECT_METHOD"&&x.rho==="1/2");
  const base=frac(w.retest_sum_joint["-2,-2"]),p=frac("1/2");
  const single=frac(w.single_observation_joint["-1,-1"]);
  const expected=sum(product(frac("1/2"),base),product(p,single));
  if(!equal(expected,frac(r.retest_joint["-2,-2"])))throw Error("audit mismatch injected cell");
}
if(typeof module!=="undefined"){module.exports={audit};if(require.main===module){
 const fs=require("fs"),path=require("path");
 const orig=JSON.parse(fs.readFileSync(path.join(__dirname,"../R227/R227_EXACT_RESULTS.json"),"utf8"));
 const rec=JSON.parse(fs.readFileSync(path.join(__dirname,"../validation/R227_S23_40_CONDITION_EXACT_RECEIPT_2026-10-28.json"),"utf8"));
 process.stdout.write(JSON.stringify(audit(orig,rec),null,2)+"\n");
}}
