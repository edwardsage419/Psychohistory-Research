#!/usr/bin/env node
"use strict";
// E050 independent third route: original R217 CSV vs frozen R217 S13 receipt.
// Node.js standard library, artificial sources, no paid services.
const WORLDS=["VALID_TAU2","VALID_ZERO","VALID_MINUS2","VALID_DYNAMIC","DONOR_POST_CONTAMINATION","UNTREATED_POST_SHOCK_MIMIC","UNTREATED_POST_DRIFT","PRE_FIT_MISMATCH"];
const POOLS=[[0,1,2],[0,1],[0,2],[1,2],[0],[1],[2]];
const DPRE=[[0,0,0],[0,2,4],[2,1,0]], DPOST=[[0,0],[6,8],[-2,-2]];
const W=[];for(let a=0;a<=4;a++)for(let b=0;b<=4-a;b++)W.push([a,b,4-a-b]);
function assert(x,s){if(!x)throw Error(s)}
function g(a,b){a=Math.abs(a);while(b){const c=a%b;a=b;b=c}return a}
function frac(n,d){const q=g(n,d);return d/q===1?String(n/q):(n/q)+"/"+(d/q)}
function num16(s){const m=/^(-?\d+)(?:\/(\d+))?$/.exec(s);assert(m,"bad rational "+s);const n=Number(m[1]),d=Number(m[2]||1);assert(d>0&&(n*16)%d===0,"nonquarter source "+s);return n*16/d}
function str16(n){return frac(n,16)}
function bit(b,i){return ((b>>i)&1)?4:-4}
function name(p){return p.map(i=>"D"+i).join("")}
function preBase(w){return w==="PRE_FIT_MISMATCH"?[0,1,3]:[0,1,2]}
function y0(w){return w==="UNTREATED_POST_SHOCK_MIMIC"?[5,6]:w==="UNTREATED_POST_DRIFT"?[4,6]:[3,4]}
function tau(w){return ["VALID_ZERO","UNTREATED_POST_SHOCK_MIMIC","UNTREATED_POST_DRIFT","PRE_FIT_MISMATCH"].includes(w)?[0,0]:w==="VALID_MINUS2"?[-2,-2]:w==="VALID_DYNAMIC"?[1,3]:[2,2]}
function donors16(w,b){const d=DPOST.map(v=>v.map(x=>x*16));if(w==="DONOR_POST_CONTAMINATION")d[1]=[128,160];for(let t=0;t<2;t++)d[1][t]+=bit(b,t+2);return d}
function fit(obs,pool){let best=null,loss=Infinity;for(const w of W){if(w.some((x,i)=>x&&!pool.includes(i)))continue;let z=0;for(let t=0;t<3;t++){let pred=4*w.reduce((s,v,i)=>s+v*DPRE[i][t],0);z+=(obs[t]-pred)**2}if(z<loss){loss=z;best=w}}assert(best!==null,"no fit");return {w:best,loss}}
function run(csvText,receiptText){
 const receipt=JSON.parse(receiptText),lines=csvText.trim().split(/\r?\n/),heads=lines.shift().split(",");
 const by=new Map();let checks=0;const ck=(v,s)=>{checks++;assert(v,s)};
 ck(heads.length===18,"CSV column count");ck(lines.length===1024,"CSV rows");
 for(const line of lines){const vals=line.split(",");ck(vals.length===18,"CSV malformed");const row=Object.fromEntries(heads.map((h,i)=>[h,vals[i]]));
 const world=row.world,pre=Number(row.original_training_three_signs_bitmask),post=Number(row.independent_new_four_signs_bitmask);
 ck(WORLDS.includes(world)&&pre>=0&&pre<8&&post>=0&&post<16,"world bits");
 const key=world+"|"+pre+"|"+post;ck(!by.has(key),"duplicate source");by.set(key,row);
 ck(row.true_joint_train_independent_new_source_probability==="1/128","source probability");
 const obs=row.actual_pre_T_observed_three_values.split("|").map(num16);
 ck(obs.length===3&&obs.every((v,t)=>v===16*preBase(world)[t]+bit(pre,t)),"pre source mismatch");
 for(let j=0;j<3;j++)ck(row["fixed_pre_donor_D"+j]===DPRE[j].join("|"),"donor pre mismatch");
 const tt=row.independent_future_true_T_observed.split("|").map(num16), d=donors16(world,post), y=y0(world),effect=tau(world);
 ck(tt.length===2&&tt.every((v,t)=>v===16*(y[t]+effect[t])+bit(post,t)),"T future mismatch");
 ck(row.independent_future_actual_three_donor_series===d.map(x=>x.map(str16).join("/")).join("|"),"donor future mismatch");
 ck(row.independent_future_actual_true_causal_effect_ORACLE_ONLY===effect.join("|"),"effect mismatch");
 }
 ck(by.size===1024,"source coverage");
 const cmap=new Map(receipt.conditions.map(r=>[r.world+"|"+r.pool+"|"+r.pre_bits,r]));
 const smap=new Map(receipt.summary.map(r=>[r.world+"|"+r.pool,r]));
 ck(cmap.size===448&&smap.size===56,"receipt coverage");
 let compared=0;
 for(const world of WORLDS)for(const pool of POOLS){
  let sse=0,risk=0,zero=0,hist={};const p=name(pool);
  for(let pre=0;pre<8;pre++){
   const source=by.get(world+"|"+pre+"|0");ck(!!source,"source pre exists");
   const obs=source.actual_pre_T_observed_three_values.split("|").map(num16);
   const f=fit(obs,pool);sse+=f.loss;if(f.loss===0)zero++;
   const key=f.w.map(x=>x+"/4").join("|");hist[key]=(hist[key]||0)+1;
   let total=0;
   for(let post=0;post<16;post++){
    const row=by.get(world+"|"+pre+"|"+post);ck(!!row,"source future exists");
    const T=row.independent_future_true_T_observed.split("|").map(num16),D=donors16(world,post),e=row.independent_future_actual_true_causal_effect_ORACLE_ONLY.split("|").map(num16);
    let sum=0;for(let t=0;t<2;t++){const n=f.w.reduce((z,v,j)=>z+v*D[j][t],0);ck(n%4===0,"quarter predicted integer");const err=T[t]-n/4-e[t];sum+=err*err}total+=sum;
   }
   ck(total%16===0,"conditional risk integer");const cond=total/16;risk+=cond;
   const actual=cmap.get(world+"|"+p+"|"+pre);ck(!!actual,"missing receipt condition");
   for(const [k,v] of Object.entries({weights_quarters:f.w.join("|"),training_sse_num256:f.loss,conditional_future_mse_num512:cond})){ck(actual[k]===v,"condition "+world+" "+p+" "+pre+" "+k);compared++}
  }
  const sum=smap.get(world+"|"+p);ck(!!sum,"missing summary");
  const expected={training_mean_sse_exact:frac(sse,2048),future_effect_mse_exact:frac(risk,4096),future_effect_mse_num4096:risk,zero_training_sse_paths:zero,pool_size:pool.length};
  for(const [k,v] of Object.entries(expected)){ck(sum[k]===v,"summary "+world+" "+p+" "+k);compared++}
  ck(JSON.stringify(Object.entries(hist).sort())===JSON.stringify(Object.entries(sum.selected_weight_histogram).sort()),"hist "+world+" "+p);compared++;
 }
 ck(compared===1680,"compared fields");return {status:"PASS",checks,compared,sourceRows:by.size,conditions:cmap.size,summary:smap.size,scope:"independent original CSV source replay; artificial E1; no CI"}
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs");if(process.argv.length!==4)throw Error("usage: node script.js original_R217.csv S13_receipt.json");
 console.log(JSON.stringify(run(fs.readFileSync(process.argv[2],"utf8"),fs.readFileSync(process.argv[3],"utf8"))));
}
