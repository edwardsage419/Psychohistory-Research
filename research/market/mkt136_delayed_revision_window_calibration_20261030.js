"use strict";
// MKT136: finite artificial delayed-label and revision replay.
// All scores use integer numerators over 25; no external dependencies.
const records=[
 {id:"A",at:0,p5:1,truth:0,first:1,label:0},
 {id:"B",at:0,p5:1,truth:0,first:5,label:0},
 {id:"C",at:1,p5:1,truth:1,first:6,label:0,rev:9,newLabel:1},
 {id:"D",at:1,p5:1,truth:0,first:2,label:0},
 {id:"E",at:2,p5:4,truth:1,first:3,label:1},
 {id:"F",at:2,p5:4,truth:1,first:7,label:0,rev:10,newLabel:1},
 {id:"G",at:3,p5:4,truth:0,first:8,label:0},
 {id:"H",at:3,p5:4,truth:1,first:4,label:1}
];
function requireValid(rows) {
 const ids=new Set();
 for(const r of rows){
  if(ids.has(r.id)) throw Error("duplicate ID");
  ids.add(r.id);
  if(!Number.isInteger(r.at)||r.at<0||!Number.isInteger(r.p5)||r.p5<0||r.p5>5) throw Error("bad prediction");
  if(!Number.isInteger(r.first)||r.first<r.at) throw Error("bad first availability");
  if(![0,1].includes(r.label)||![0,1].includes(r.truth)) throw Error("bad label");
  if(r.rev!==undefined && (!Number.isInteger(r.rev)||r.rev<=r.first||![0,1].includes(r.newLabel))) throw Error("bad revision");
  if(r.rev===undefined && r.newLabel!==undefined) throw Error("orphan revision label");
 }
}
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a;}
function frac(n,d){if(!Number.isInteger(n)||!Number.isInteger(d)||d<=0)throw Error("bad fraction");const g=gcd(n,d);return (n/g)+"/"+(d/g);}
function error25(r,y){return (r.p5-5*y)**2;}
function asof(r,t){if(r.first>t)return null;return r.rev!==undefined&&r.rev<=t?r.newLabel:r.label;}
function evaluate(t,rows=records,horizon=3){
 requireValid(rows);
 if(!Number.isInteger(t)||t<0||!Number.isInteger(horizon)||horizon<0)throw Error("bad cutoff");
 const mature=rows.filter(r=>r.at+horizon<=t);
 if(!mature.length)return {cutoff:t,mature:0,status:"ABSTAIN"};
 const observed=mature.map(r=>({r,y:asof(r,t)})).filter(x=>x.y!==null);
 const missing=mature.length-observed.length;
 const sum=observed.reduce((a,x)=>a+error25(x.r,x.y),0);
 const min=mature.filter(r=>asof(r,t)===null).reduce((a,r)=>a+Math.min(error25(r,0),error25(r,1)),0);
 const max=mature.filter(r=>asof(r,t)===null).reduce((a,r)=>a+Math.max(error25(r,0),error25(r,1)),0);
 const oracle=mature.reduce((a,r)=>a+error25(r,r.truth),0);
 let ece="ABSTAIN";
 if(!missing){
  let total=0;
  for(const p5 of [...new Set(mature.map(r=>r.p5))]){
   const bin=mature.filter(r=>r.p5===p5);
   const positives=bin.reduce((a,r)=>a+asof(r,t),0);
   total+=Math.abs(5*positives-p5*bin.length);
  }
  ece=frac(total,5*mature.length);
 }
 return {cutoff:t,mature:mature.length,observed:observed.length,missing,
  observedBrier:observed.length?frac(sum,25*observed.length):"ABSTAIN",
  riskLower:frac(sum+min,25*mature.length),riskUpper:frac(sum+max,25*mature.length),
  finalOracleBrier:frac(oracle,25*mature.length),ece};
}
function check(cond,msg){if(!cond)throw Error("ASSERT "+msg);}
function rejects(fn){let yes=false;try{fn();}catch(e){yes=true;}check(yes,"expected rejection");}
function run(){
 const a=[4,6,8,10].map(t=>evaluate(t));
 check(a[0].mature===4&&a[0].observed===2&&a[0].riskUpper==="17/50","cutoff4");
 check(a[0].riskLower==="1/25"&&a[0].finalOracleBrier==="19/100","cutoff4 oracle");
 check(a[1].mature===8&&a[1].observed===6&&a[1].riskUpper==="19/100","cutoff6");
 check(a[1].observedBrier==="1/25"&&a[1].riskLower==="1/25","cutoff6 observed");
 check(a[2].observed===8&&a[2].observedBrier==="19/100"&&a[2].ece==="1/4","cutoff8");
 check(a[3].observed===8&&a[3].observedBrier==="19/100"&&a[3].ece==="1/20","cutoff10");
 check(a[2].observedBrier===a[3].observedBrier&&a[2].ece!==a[3].ece,"aggregate masking");
 check(evaluate(2).status==="ABSTAIN","immature");
 rejects(()=>evaluate(4,[records[0],records[0]]));
 rejects(()=>evaluate(4,[{...records[0],p5:6}]));
 rejects(()=>evaluate(4,[{...records[0],first:-1}]));
 rejects(()=>evaluate(4,[{...records[0],label:2}]));
 rejects(()=>evaluate(4,[{...records[2],rev:5}]));
 rejects(()=>evaluate(4,[{...records[0],newLabel:1}]));
 rejects(()=>evaluate(4.5));
 return {status:"PASS",positiveAssertions:8,negativeControls:7,cutoffs:a};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
