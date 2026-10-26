"use strict";
// R191 third method. Node 18+ standard library only.
// node r191_binary_event_24_20261026.js research/R191/R191_ALL_OBSERVABLE_POSTERIOR_PROFILES.json research/R191/R191_EXACT_RESULTS.json
const fs=require("fs");
function rational(){
 const abs=x=>x<0n?-x:x;
 function gcd(a,b){a=abs(a);b=abs(b);while(b){const t=a%b;a=b;b=t;}return a;}
 function F(a,b=1n){if(a&&typeof a==="object"&&"n" in a)return a;
  if(typeof a==="string"&&a.includes("/")){let [x,y]=a.split("/");return F(BigInt(x),BigInt(y));}
  a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");
  if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return {n:a/g,d:b/g};
 }
 const add=(a,b)=>F(a.n*b.d+b.n*a.d,a.d*b.d);
 const neg=a=>F(-a.n,a.d),sub=(a,b)=>add(a,neg(b));
 const mul=(a,b)=>F(a.n*b.n,a.d*b.d),div=(a,b)=>F(a.n*b.d,a.d*b.n);
 const sq=a=>mul(a,a),eq=(a,b)=>a.n===b.n&&a.d===b.d;
 const show=a=>a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);
 return {F,add,sub,mul,div,sq,eq,show};
}
function compute(profiles,source){
 const {F,add,sub,mul,div,sq,eq,show}=rational(),zero=F(0),one=F(1),half=F(1,2);
 if(profiles.observable_profile_count!==1136||profiles.profiles.length!==1136||source.world_count!==24||source.worlds.length!==24)throw Error("frozen source shape changed");
 const key=(t,s,n)=>[t,s,n].join("|");
 const groups=new Map();
 for(const w of source.worlds)groups.set(key(w.tau,w.sigma,w.n),{w,weight:zero,mean:zero,skill:zero,risk:zero,count:0});
 for(const p of profiles.profiles){
  const k=key(p.tau,p.sigma,p.n),g=groups.get(k);if(!g)throw Error("unknown world "+k);
  const tau=F(p.tau),sigma=F(p.sigma),lm=F(p.posterior_hidden_U_minus_state_likelihood),lp=F(p.posterior_hidden_U_plus_state_likelihood),sum=add(lm,lp);
  if(!sum.n)throw Error("zero profile likelihood");
  const w=F(p.true_training_observation_probability);
  if(!eq(w,mul(half,sum)))throw Error("source probability mismatch");
  if(!eq(F(p.posterior_expected_hidden_U),mul(tau,div(sub(lp,lm),sum))))throw Error("posterior U mismatch");
  function event(u){let ans=zero;for(const [eps,prob] of [[mul(F(-2),sigma),F(1,4)],[zero,F(1,2)],[mul(F(2),sigma),F(1,4)]])if(add(u,eps).n>0n)ans=add(ans,prob);return ans;}
  const am=event(sub(zero,tau)),ap=event(tau),p0=mul(half,add(am,ap));
  const q=div(add(mul(lm,am),mul(lp,ap)),sum);
  if(q.n<0n||sub(q,one).n>0n)throw Error("invalid conditional probability");
  g.weight=add(g.weight,w);g.mean=add(g.mean,mul(w,q));
  g.risk=add(g.risk,mul(w,mul(q,sub(one,q))));
  g.skill=add(g.skill,mul(w,sq(sub(q,p0))));g.count++;
 }
 const rows=[];let positive=0,zeroWorlds=0,total=0;
 for(const w of source.worlds){
  const g=groups.get(key(w.tau,w.sigma,w.n)),tau=F(w.tau),sigma=F(w.sigma);
  function event(u){let ans=zero;for(const [eps,prob] of [[mul(F(-2),sigma),F(1,4)],[zero,F(1,2)],[mul(F(2),sigma),F(1,4)]])if(add(u,eps).n>0n)ans=add(ans,prob);return ans;}
  const p0=mul(half,add(event(sub(zero,tau)),event(tau))),base=mul(p0,sub(one,p0));
  if(!eq(g.weight,one)||!eq(g.mean,p0)||!eq(add(g.risk,g.skill),base)||g.count!==w.distinct_observable_training_vectors)throw Error("calibration/risk/count identity "+JSON.stringify(w));
  if(g.skill.n<0n)throw Error("negative skill");
  if(g.skill.n>0n)positive++;else zeroWorlds++;
  rows.push({tau:w.tau,sigma:w.sigma,n:w.n,visible_profiles:g.count,prior_event_probability:show(p0),same_group_Bayes_Brier:show(g.risk),same_group_global_Brier:show(base),same_group_skill_exact:show(g.skill),new_group_correct_Brier:show(base),new_group_wrong_reused_posterior_Brier:show(add(base,g.skill))});total+=g.count;
 }
 if(total!==1136||positive!==16||zeroWorlds!==8)throw Error("unexpected world distribution");
 let monotonicChecks=0;for(const t of ["0","1/2","1"])for(const s of ["1/2","1"]){let a=rows.filter(x=>x.tau===t&&x.sigma===s).sort((a,b)=>a.n-b.n);for(let i=1;i<a.length;i++){if(sub(F(a[i].same_group_skill_exact),F(a[i-1].same_group_skill_exact)).n<0n)throw Error("learning monotonicity");monotonicChecks++;}}
 return {research_id:"R191",method:"source 1136 observable profiles exact conditional event Brier",frozen_source_results_blob:"31f3cb89bbe502640f78407bb68c564d4701f95a",frozen_source_profiles_blob:"f174d4c37c3559073252ce5b14020a93c0592ce6",worlds:24,profiles:total,strict_positive_skill_worlds:positive,zero_skill_worlds:zeroWorlds,nondecreasing_n_skill_checks:monotonicChecks,all_profile_mass_and_conditional_calibration_exact:true,all_cross_group_reuse_penalties_equal_skill_exact:true,evidence:"E1_ARTIFICIAL_POSTSCORE",new_E2:0,new_E3:0,external_independent_team_replications:0,R073_and_PESEN_unchanged:true,rows};
}
module.exports={compute};
if(require.main===module){
 if(process.argv.length!==4)throw Error("usage: node script posterior_profiles.json original_results.json");
 process.stdout.write(JSON.stringify(compute(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2)+"\n");
}
