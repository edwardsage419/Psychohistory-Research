#!/usr/bin/env node
'use strict';
const assert = require('node:assert/strict');
// Entirely fictional decisions. Reward is in [0,1]. Null means no follow-up.
const logs = Array.from({length:8}, (_, i) => ({
  id:i+1,valueVersion:i<4?'v1':'v2',
  firstCriterionWeight:i<4?0.65:0.50,
  chosen:i<4?'A':'B',
  observedReward:i<4?0.75:(i<6?1:null),
  feedbackStatus:i<6?'OBSERVED':'MISSING',
  loggingPropensity:null
}));
const observed=logs.filter(x=>x.observedReward!==null);
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const early=mean(observed.filter(x=>x.valueVersion==='v1').map(x=>x.observedReward));
const lateObserved=mean(observed.filter(x=>x.valueVersion==='v2').map(x=>x.observedReward));
const missingB=logs.filter(x=>x.chosen!=='B'||x.observedReward===null);
const worlds=[];
for(let mask=0;mask<(1<<missingB.length);mask++){
 const outcomes=Object.fromEntries(missingB.map((x,k)=>[x.id,(mask>>k)&1]));
 const b=logs.map(x=>x.chosen==='B'&&x.observedReward!==null?x.observedReward:outcomes[x.id]);
 worlds.push({targetB:mean(b),lateB:mean(b.slice(4)),difference:mean(b.slice(4))-early});
}
const range=k=>[Math.min(...worlds.map(w=>w[k])),Math.max(...worlds.map(w=>w[k]))];
let assertions=0;const t=(x,msg)=>{assert.ok(x,msg);assertions++};
t(logs.length===8,'eight logs');t(observed.length===6,'six observed');
t(missingB.length===6,'six unknown B outcomes');t(worlds.length===64,'64 completions');
t(early===0.75,'early selected reward');t(lateObserved===1,'late selected reward');
t(lateObserved-early===0.25,'naive observed gain');
t(range('targetB')[0]===0.25&&range('targetB')[1]===1,'target bounds');
t(range('lateB')[0]===0.5&&range('lateB')[1]===1,'late bounds');
t(range('difference')[0]===-0.25&&range('difference')[1]===0.25,'difference sign');
t(logs.every(x=>x.loggingPropensity===null),'propensities unknown');
t(logs.slice(0,4).every(x=>x.chosen==='A'),'early no B support');
t(logs.slice(4).every(x=>x.chosen==='B'),'late all B');
t(logs.every(x=>x.feedbackStatus===(x.observedReward===null?'MISSING':'OBSERVED')),'feedback status');
t(worlds.some(x=>x.difference<0)&&worlds.some(x=>x.difference>0),'opposite signs');
t(new Set(worlds.map(x=>x.targetB)).size===7,'seven target mean values');
console.log(JSON.stringify({status:'PASS',assertions,artificial:true,logged_decisions:8,observed_rewards:6,unobserved_B_potential_outcomes:6,completions:64,naive_observed_gain:0.25,target_B_mean_range:range('targetB'),late_B_mean_range:range('lateB'),late_B_minus_early_A_range:range('difference'),off_policy_ips_identified:false}));
