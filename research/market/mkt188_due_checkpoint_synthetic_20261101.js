'use strict';
const decisions=[1,2,3,4].map(id=>({id,p:0.8,outcome:id<=2?1:0}));
const horizons=[30,90,180],now=120;
const all=decisions.flatMap(d=>horizons.map(h=>({id:d.id,h,p:d.p,due:h<=now,
  y:h<=now?d.outcome:null,reviewed:h===30&&d.id<=2})));
const due=all.filter(x=>x.due),reviewed=due.filter(x=>x.reviewed),future=all.filter(x=>!x.due);
const loss=x=>(x.p-x.y)**2;
const sum=a=>a.reduce((s,x)=>s+x,0),near=(a,b)=>Math.abs(a-b)<1e-12;
const observed=sum(reviewed.map(loss))/reviewed.length;
const oracle=sum(due.map(loss))/due.length;
const missing=due.filter(x=>!x.reviewed);
const lower=(sum(reviewed.map(loss))+sum(missing.map(x=>Math.min(x.p**2,(1-x.p)**2))))/due.length;
const upper=(sum(reviewed.map(loss))+sum(missing.map(x=>Math.max(x.p**2,(1-x.p)**2))))/due.length;
let tests=0;function check(x){if(!x)throw Error('assertion '+tests);tests++;}
check(all.length===12);check(due.length===8);check(future.length===4);
check(reviewed.length===2);check(missing.length===6);
check(near(observed,0.04));check(near(oracle,0.34));
check(near(lower,0.04));check(near(upper,0.49));
check(near(reviewed.length/due.length,0.25));
check(near(reviewed.length/all.length,1/6));
check(due.filter(x=>x.h===90&&x.reviewed).length===0);
check(future.every(x=>x.y===null&&!x.reviewed));
check(lower<=oracle&&oracle<=upper);
console.log(JSON.stringify({tests,planned:all.length,due:due.length,notYetDue:future.length,
 reviewed:reviewed.length,dueCoverage:reviewed.length/due.length,
 allPlannedCoverage:reviewed.length/all.length,reviewedBrier:observed,
 oracleBrier:oracle,possibleDueBrier:[lower,upper],
 horizonCoverage:horizons.map(h=>({h,due:due.filter(x=>x.h===h).length,
 reviewed:reviewed.filter(x=>x.h===h).length}))},null,2));
