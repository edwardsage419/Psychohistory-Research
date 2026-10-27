// R217 S13, finite artificial E1 donor-pool sensitivity. Node.js standard library only.
"use strict";
const WORLDS=["VALID_TAU2","VALID_ZERO","VALID_MINUS2","VALID_DYNAMIC","DONOR_POST_CONTAMINATION","UNTREATED_POST_SHOCK_MIMIC","UNTREATED_POST_DRIFT","PRE_FIT_MISMATCH"];
const POOLS=[[0,1,2],[0,1],[0,2],[1,2],[0],[1],[2]];
const DPRE=[[0,0,0],[0,2,4],[2,1,0]], DPOST=[[0,0],[6,8],[-2,-2]];
const ALLW=[];for(let a=0;a<=4;a++)for(let b=0;b<=4-a;b++){let c=4-a-b;ALLW.push([a,b,c]);}
const name=p=>p.map(i=>"D"+i).join("");
const signed=(bits,i)=>((bits>>i)&1)?4:-4; // outcome scale 16
const preBase=(world)=>world==="PRE_FIT_MISMATCH"?[0,1,3]:[0,1,2];
const y0=(world)=>world==="UNTREATED_POST_SHOCK_MIMIC"?[5,6]:world==="UNTREATED_POST_DRIFT"?[4,6]:[3,4];
const tau=(world)=>["VALID_ZERO","UNTREATED_POST_SHOCK_MIMIC","UNTREATED_POST_DRIFT","PRE_FIT_MISMATCH"].includes(world)?[0,0]:world==="VALID_MINUS2"?[-2,-2]:world==="VALID_DYNAMIC"?[1,3]:[2,2];
const postD=(world)=>world==="DONOR_POST_CONTAMINATION"?[[0,0],[8,10],[-2,-2]]:DPOST;
function fit(world,pool,bits){
 const obs=preBase(world).map((v,k)=>16*v+signed(bits,k));
 let best=null, bestLoss=Infinity;
 for(const w of ALLW){if(w.some((v,i)=>v&&!pool.includes(i)))continue;
  let loss=0;for(let t=0;t<3;t++){const pred=4*w.reduce((s,v,i)=>s+v*DPRE[i][t],0);loss+=(obs[t]-pred)**2;}
  if(loss<bestLoss){bestLoss=loss;best=w;}
 }
 if(!best)throw Error("no candidates");return {w:best,loss:bestLoss};
}
function futurePairError(world,w,bits){
 const yy=y0(world),tt=tau(world),d=postD(world);
 let total=0;
 for(let t=0;t<2;t++){
   const actualT16=16*(yy[t]+tt[t])+signed(bits,t);
   const donor16=d.map((row,j)=>16*row[t]+(j===1?signed(bits,2+t):0));
   const pred16=w.reduce((s,v,j)=>s+v*donor16[j],0)/4;
   if(!Number.isInteger(pred16))throw Error("quarter scale failure");
   const err16=actualT16-pred16-16*tt[t];total+=err16**2;
 }
 return total; // future two-period MSE = total/512
}
function gcd(a,b){while(b){const x=a%b;a=b;b=x;}return a;}
function frac(n,d){if(!Number.isSafeInteger(n)||!Number.isSafeInteger(d))throw Error("noninteger");const g=gcd(Math.abs(n),d);return (d/g===1)?String(n/g):n/g+"/"+d/g;}
function run(){
 const conditions=[],summary=[];
 for(const world of WORLDS)for(const pool of POOLS){
   let trainSSE256=0,riskNum=0;const weights={};let probZero=0;
   for(let pre=0;pre<8;pre++){
     const f=fit(world,pool,pre);trainSSE256+=f.loss;
     if(f.loss===0)probZero++;
     const wk=f.w.map(v=>v+"/4").join("|");weights[wk]=(weights[wk]||0)+1;
     let errTotal=0;for(let post=0;post<16;post++)errTotal+=futurePairError(world,f.w,post);
     if(errTotal%16!==0)throw Error("future expectation not integer");
     const conditional512=errTotal/16;
     riskNum+=conditional512;
     conditions.push({world,pool:name(pool),pre_bits:pre,weights_quarters:f.w.join("|"),training_sse_num256:f.loss,conditional_future_mse_num512:conditional512});
   }
   summary.push({world,pool:name(pool),pool_size:pool.length,training_mean_sse_exact:frac(trainSSE256,2048),future_effect_mse_exact:frac(riskNum,4096),future_effect_mse_num4096:riskNum,selected_weight_histogram:weights,zero_training_sse_paths:probZero});
 }
 if(conditions.length!==448||summary.length!==56)throw Error("incomplete finite grid");
 const full={"VALID_TAU2":"9/64","VALID_ZERO":"9/64","VALID_MINUS2":"9/64","VALID_DYNAMIC":"9/64","DONOR_POST_CONTAMINATION":"57/64","UNTREATED_POST_SHOCK_MIMIC":"297/64","UNTREATED_POST_DRIFT":"193/64","PRE_FIT_MISMATCH":"825/256"};
 for(const r of summary.filter(r=>r.pool==="D0D1D2"))if(r.future_effect_mse_exact!==full[r.world])throw Error("R217 original baseline regression "+r.world);
 for(const p of POOLS){const a=summary.find(x=>x.world==="VALID_TAU2"&&x.pool===name(p)),b=summary.find(x=>x.world==="UNTREATED_POST_SHOCK_MIMIC"&&x.pool===name(p));if(JSON.stringify(a.selected_weight_histogram)!==JSON.stringify(b.selected_weight_histogram))throw Error("observational alias violated");}
 return {study:"R217_S13",evidence:"E1_ARTIFICIAL",world_count:8,pools:POOLS.map(name),training_paths:8,future_paths:16,source_slots:7168,conditional_rows:conditions.length,summary_rows:summary.length,original_R217_full_pool_regression:"PASS_8_OF_8",conditions,summary};
}
if(typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
