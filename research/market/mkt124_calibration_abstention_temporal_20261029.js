#!/usr/bin/env node
"use strict";
// MKT124: synthetic calibration and abstention under subject/time holdouts.
// Standard-library only. No user data, network requests, payments or API calls.
const assert = require("node:assert/strict");
let checks = 0;
function ok(condition, message) { checks++; assert.ok(condition, message); }
function records(users, periods) {
  const out = [];
  for (const u of users) for (const t of periods) for (let k=0;k<2;k++) {
    const stable = u % 2;
    const label = t === 3 && u < 4 ? 1-stable : stable;
    const p = u >= 8 ? 0.5 : stable ? 0.9 : 0.1;
    out.push({u,t,k,label,p,session: u+":"+t});
  }
  return out;
}
function metric(rows, transform = r => r.p) {
  ok(rows.length>0,"nonempty metric group");
  let brier=0, correct=0;
  const bins = new Map();
  for (const r of rows) {
    const p=transform(r);
    ok(p>=0 && p<=1,"probability range");
    brier+=(p-r.label)**2;
    correct+=Number((p>=0.5)===Boolean(r.label));
    const key=p.toFixed(8);
    const g=bins.get(key)||{n:0, y:0, p:0};
    g.n++;g.y+=r.label;g.p+=p;bins.set(key,g);
  }
  const ece=[...bins.values()].reduce((a,g)=>a+g.n/rows.length*Math.abs(g.y/g.n-g.p/g.n),0);
  return {n:rows.length, accuracy:correct/rows.length, brier:brier/rows.length, ece};
}
function selection(rows, threshold, validThrough=Infinity) {
  const accepted=rows.filter(r=>r.t<=validThrough && Math.max(r.p,1-r.p)>=threshold);
  const errors=accepted.filter(r=>(r.p>=0.5)!==Boolean(r.label)).length;
  return {accepted:accepted.length, coverage:accepted.length/rows.length,
    error_rate:accepted.length?errors/accepted.length:null};
}
function checkDisjoint(train, test, mode) {
  if(mode==="new_user") {
    const a=new Set(train.map(r=>r.u));
    if(test.some(r=>a.has(r.u))) throw Error("subject leakage");
  } else if(mode==="forward") {
    if(Math.max(...train.map(r=>r.t))>=Math.min(...test.map(r=>r.t))) throw Error("temporal leakage");
  } else throw Error("unknown split");
}
function mustReject(f) { let rejected=false; try { f(); } catch(e) {rejected=true;}
  ok(rejected,"negative control should reject"); }
function close(a,b){ok(Math.abs(a-b)<1e-10,"unexpected exact metric "+a+" versus "+b);}
function run() {
  const train=records([0,1,2,3,4,5,6,7],[0,1]);
  const calibration=records([0,1,2,3,4,5,6,7],[2]);
  const future=records([0,1,2,3,4,5,6,7],[3]);
  const newUsers=records([8,9,10,11],[2]);
  checkDisjoint(train,calibration,"forward");
  checkDisjoint(calibration,future,"forward");
  checkDisjoint(train,newUsers,"new_user");
  mustReject(()=>checkDisjoint(train,records([0],[2]),"new_user"));
  mustReject(()=>checkDisjoint(records([0],[3]),calibration,"forward"));
  const calibrationBins=new Map();
  for(const r of calibration) {
    const key=r.p.toFixed(8);
    const g=calibrationBins.get(key)||{n:0,y:0};
    g.n++;g.y+=r.label;calibrationBins.set(key,g);
  }
  const mapped=r=>calibrationBins.get(r.p.toFixed(8))?.y/calibrationBins.get(r.p.toFixed(8))?.n ?? 0.5;
  const stable=metric(calibration), drift=metric(future), newUser=metric(newUsers);
  const stableMapped=metric(calibration,mapped), driftMapped=metric(future,mapped);
  const stableSelect=selection(calibration,0.8);
  const driftSelect=selection(future,0.8);
  const driftHorizon=selection(future,0.8,2);
  const newSelect=selection(newUsers,0.8);
  close(stable.accuracy,1);close(stable.brier,0.01);close(stable.ece,0.1);
  close(drift.accuracy,0.5);close(drift.brier,0.41);close(drift.ece,0.4);
  close(newUser.accuracy,0.5);close(newUser.brier,0.25);close(newUser.ece,0);
  close(stableMapped.brier,0);close(driftMapped.brier,0.5);
  close(stableSelect.coverage,1);close(stableSelect.error_rate,0);
  close(driftSelect.coverage,1);close(driftSelect.error_rate,0.5);
  close(driftHorizon.coverage,0);ok(driftHorizon.error_rate===null,"empty abstention");
  close(newSelect.coverage,0);ok(newSelect.error_rate===null,"unknown user abstention");
  ok(train.length===32 && calibration.length===16 && future.length===16 && newUsers.length===8,"sample sizes");
  return {evidence:"E1_SYNTHETIC",checks,train:train.length,calibration:stable,
    future:drift,new_user:newUser,calibrated_stable:stableMapped,
    calibrated_future:driftMapped,selection:{stable:stableSelect,future:driftSelect,
    horizon_block:driftHorizon,new_user:newSelect},negative_controls:2};
}
if (require.main===module) console.log(JSON.stringify(run(),null,2));
module.exports={run};
