"use strict";
// Synthetic preference identification counterexample. Node.js standard library only.
const assert = require("node:assert/strict");
let checks = 0;
const check = (condition, message) => { checks++; assert.ok(condition, message); };
const p = (model, time, context) => model === "TIME" ? (time === 0 ? 0.9 : 0.1) : model === "CONTEXT" ? (context === 0 ? 0.9 : 0.1) : 0.5;
const likelihood = (model, observations) => observations.reduce((v, o) => v * (o.y === 1 ? p(model, o.t, o.c) : 1 - p(model, o.t, o.c)), 1);
const initial = [{t:0,c:0,y:1},{t:1,c:1,y:0}];
const probes = [{t:0,c:1,y:1},{t:1,c:0,y:0}];
const full = initial.concat(probes);
check(Math.abs(likelihood("TIME",initial)-0.81)<1e-12,"initial time");
check(Math.abs(likelihood("CONTEXT",initial)-0.81)<1e-12,"initial context");
check(Math.abs(likelihood("STATIC",initial)-0.25)<1e-12,"initial static");
check(Math.abs(likelihood("TIME",full)-0.6561)<1e-12,"crossed time");
check(Math.abs(likelihood("CONTEXT",full)-0.0081)<1e-12,"crossed context");
check(Math.abs(likelihood("TIME",full)/likelihood("CONTEXT",full)-81)<1e-9,"bayes factor");
for(const model of ["TIME","CONTEXT","STATIC"]){
 for(const t of [0,1])for(const c of [0,1]){
  const q=p(model,t,c);check(q>0&&q<1,"probability support");
  const yes={t,c,y:1},no={t,c,y:0};
  check(Math.abs(likelihood(model,[yes,no])-q*(1-q))<1e-12,"contradictory repeats are possible");
 }
}
for(const y0 of [0,1])for(const y1 of [0,1]){
 const a=[{t:0,c:0,y:y0},{t:1,c:1,y:y1}];
 check(Math.abs(likelihood("TIME",a)-likelihood("CONTEXT",a))<1e-12,"nonidentifiability");
}
const ledger=[];
const approve=(id)=>ledger.push({type:"APPROVE",id});
const revoke=(id)=>ledger.push({type:"REVOKE",id});
const active=()=>{const last=ledger.at(-1);return last&&last.type==="APPROVE"?last.id:null;};
approve("A");check(active()==="A","initial approval");
approve("C");check(active()==="C","new approval");
revoke("C");check(active()===null,"no stale fallback");
ledger.push({type:"ABSTAIN"});check(active()===null,"abstain does not authorize");
console.log(JSON.stringify({checks,failures:0,initial_likelihood:{time:likelihood("TIME",initial),context:likelihood("CONTEXT",initial),static:likelihood("STATIC",initial)},crossed_likelihood:{time:likelihood("TIME",full),context:likelihood("CONTEXT",full)},likelihood_ratio:likelihood("TIME",full)/likelihood("CONTEXT",full),approval_state:"NO_ACTIVE_PREFERENCE"},null,2));
