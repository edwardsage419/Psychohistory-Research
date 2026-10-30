'use strict';
// Artificial weighted sum only. This is not Dcider's undisclosed scoring algorithm.
const assert = require('node:assert/strict');
const A = [9,4], B = [6,8];
const score = (v,w) => w*v[0]+(1-w)*v[1];
const margin = w => score(A,w)-score(B,w);
const choose = w => margin(w)>0 ? 'A' : margin(w)<0 ? 'B' : 'TIE';
const historical = [
  {id:'d1',weightVersion:'v1',weight:0.65,choice:'A'},
  {id:'d2',weightVersion:'v2',weight:0.60,choice:'A'},
  {id:'d3',weightVersion:'v3',weight:0.50,choice:'B'},
];
let checks=0;
function ok(condition,msg){assert.ok(condition,msg);checks++}
ok(Math.abs(margin(0.65)-0.55)<1e-12,'old margin');
ok(Math.abs(margin(0.6)-0.2)<1e-12,'middle margin');
ok(Math.abs(margin(0.5)+0.5)<1e-12,'new margin');
ok(Math.abs(margin(4/7))<1e-12,'switch threshold');
for(const d of historical){ok(choose(d.weight)===d.choice,'as-of replay '+d.id);}
const currentWeight=0.5;
const currentReplayed=historical.map(d=>choose(currentWeight));
ok(currentReplayed.join(',')==='B,B,B','current recomputation');
ok(historical.filter(d=>choose(currentWeight)===d.choice).length===1,'one current agreement');
ok(historical.filter(d=>choose(d.weight)===d.choice).length===3,'three as-of agreements');
const altHistory=historical.map((d,i)=>({...d,weight:i===0?0.8:i===1?0.7:0.5}));
ok(altHistory.every((d,i)=>d.choice===historical[i].choice),'same observed choices');
ok(altHistory[0].weight!==historical[0].weight,'distinct hidden histories');
ok(altHistory[1].weight!==historical[1].weight,'distinct middle histories');
ok(choose(0.5)==='B','latest policy');
for(const w of [0,0.25,0.5,4/7,0.65,0.75,1]){
 ok(Math.abs(margin(w)-(7*w-4))<1e-12,'linear identity '+w);
}
for(const bad of [-0.1,1.1,NaN,Infinity]){ok(!(Number.isFinite(bad)&&bad>=0&&bad<=1),'invalid weight '+bad)}
console.log(JSON.stringify({status:'PASS',checks,as_of_choices:historical.map(d=>choose(d.weight)),current_choices:currentReplayed,as_of_agreements:3,current_agreements:1,threshold:'4/7',evidence:'ARTIFICIAL_NONBLIND_E1'}));
