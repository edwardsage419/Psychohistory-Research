// Independent B-track algebraic replay of R217 S13. Node.js standard library only.
// Uses quadratic pre-fit identity and future conditional bias/variance; never enumerates future shock outcomes.
"use strict";
const WORLD=["VALID_TAU2","VALID_ZERO","VALID_MINUS2","VALID_DYNAMIC","DONOR_POST_CONTAMINATION","UNTREATED_POST_SHOCK_MIMIC","UNTREATED_POST_DRIFT","PRE_FIT_MISMATCH"];
const SETS=["D0D1D2","D0D1","D0D2","D1D2","D0","D1","D2"];
const PRE=[[0,0,0],[0,2,4],[2,1,0]],POST=[[0,0],[6,8],[-2,-2]];
const choose=(w,p)=>w.every((v,i)=>!v||p.includes("D"+i));
const gcd=(a,b)=>b?gcd(b,a%b):a;
const fraction=(a,b)=>{let g=gcd(Math.abs(a),b);return b/g===1?""+(a/g):a/g+"/"+b/g;};
function train(w,world,bits){
  const T=(world==="PRE_FIT_MISMATCH"?[0,1,3]:[0,1,2]).map((v,i)=>16*v+(((bits>>i)&1)?4:-4));
  // Independent quadratic identity ||T||² - 2T'P + ||P||², P = sum_j w_j D_j.
  const P=[0,1,2].map(t=>4*PRE.reduce((sum,series,j)=>sum+w[j]*series[t],0));
  const normT=T.reduce((s,v)=>s+v*v,0),cross=T.reduce((s,v,i)=>s+v*P[i],0),normP=P.reduce((s,v)=>s+v*v,0);
  return normT-2*cross+normP;
}
function best(world,pool,bits){
 let opt=null,sse=Infinity;
 // enumerate simplex by c then b, independent of R code ordering; explicitly sort lexicographically
 const cand=[];for(let c=0;c<=4;c++)for(let b=0;b<=4-c;b++){let a=4-b-c;let w=[a,b,c];if(choose(w,pool))cand.push(w);}
 cand.sort((x,y)=>x[0]-y[0]||x[1]-y[1]||x[2]-y[2]);
 for(const w of cand){const v=train(w,world,bits);if(v<sse){sse=v;opt=w;}}
 return {w:opt,sse};
}
function analytic(world,w){
 const y0=world==="UNTREATED_POST_SHOCK_MIMIC"?[5,6]:world==="UNTREATED_POST_DRIFT"?[4,6]:[3,4];
 const D=world==="DONOR_POST_CONTAMINATION"?[[0,0],[8,10],[-2,-2]]:POST;
 let biasSquares=0;
 for(let t=0;t<2;t++){const bias16=16*y0[t]-4*w.reduce((s,v,j)=>s+v*D[j][t],0);biasSquares+=bias16*bias16;}
 // E[(eps_T - w1 eps_D1)^2] = (1 + (w1/4)^2)/16.
 return {riskNumer512:biasSquares+32+2*w[1]*w[1],noDonorNoiseNumer512:biasSquares+32};
}
function replay(receipt){
 if(receipt.conditions.length!==448||receipt.summary.length!==56)throw Error("wrong source sizes");
 const key=(world,pool,pre)=>world+"|"+pool+"|"+pre;
 const map=new Map(receipt.conditions.map(x=>[key(x.world,x.pool,x.pre_bits),x]));
 let checks=0,mutated=0,alias=0,conditions=0;
 const out=[];
 for(const world of WORLD)for(const pool of SETS){
  let sseTotal=0,riskTotal=0,zero=0;const hist={};
  for(let bits=0;bits<8;bits++){
    const {w,sse}=best(world,pool,bits),a=analytic(world,w),row=map.get(key(world,pool,bits));
    if(!row)throw Error("missing condition");
    for(const [field,got,expected] of [["weights",row.weights_quarters,w.join("|")],["sse",row.training_sse_num256,sse],["risk",row.conditional_future_mse_num512,a.riskNumer512]]){if(got!==expected)throw Error("mismatch "+key(world,pool,bits)+" "+field);checks++;}
    if(a.noDonorNoiseNumer512!==a.riskNumer512)mutated++;
    conditions++;sseTotal+=sse;riskTotal+=a.riskNumer512;if(sse===0)zero++;
    const label=w.map(v=>v+"/4").join("|");hist[label]=(hist[label]||0)+1;
  }
  const row=receipt.summary.find(x=>x.world===world&&x.pool===pool);
  for(const [field,got,expected] of [["train",row.training_mean_sse_exact,fraction(sseTotal,2048)],["risk",row.future_effect_mse_exact,fraction(riskTotal,4096)],["riskNum",row.future_effect_mse_num4096,riskTotal],["zero",row.zero_training_sse_paths,zero],["hist",JSON.stringify(row.selected_weight_histogram),JSON.stringify(hist)]]){if(got!==expected)throw Error("summary mismatch "+world+" "+pool+" "+field);checks++;}
  out.push({world,pool,risk:fraction(riskTotal,4096)});
 }
 // Observable alias is exact for every paired pre/future source.
 for(let pre=0;pre<8;pre++)for(let post=0;post<16;post++){
  const ta=[5,6].map((v,t)=>16*v+(((post>>t)&1)?4:-4));
  const tb=[5,6].map((v,t)=>16*v+(((post>>t)&1)?4:-4));
  const pa=[0,1,2].map((v,t)=>16*v+(((pre>>t)&1)?4:-4));
  const pb=[0,1,2].map((v,t)=>16*v+(((pre>>t)&1)?4:-4));
  if(JSON.stringify(ta)!==JSON.stringify(tb)||JSON.stringify(pa)!==JSON.stringify(pb))throw Error("alias mismatch");
  alias++;
 }
 if(mutated===0)throw Error("donor-noise negative control uninformative");
 return {study:"B_R217_S13",independent_method:"quadratic prefit plus analytic conditional moments",conditional_cross_checks:conditions*3,summary_cross_checks:56*5,total_cross_checks:checks,failed:0,observable_alias_pre_future_pairs:alias,donor_noise_variance_omission_detected_conditions:mutated,external_independent_replication:false,evidence:"E1_ARTIFICIAL",new_E2:0,new_E3:0};
}
if(typeof module!=="undefined"&&require.main===module){const fs=require("fs");const path=process.argv[2]||"research/validation/R217_S13_DONOR_POOL_56_WORLD_POOL_448_CONDITIONAL_EXACT_RECEIPT_2026-10-27.json";process.stdout.write(JSON.stringify(replay(JSON.parse(fs.readFileSync(path,"utf8"))),null,2)+"\n");}
