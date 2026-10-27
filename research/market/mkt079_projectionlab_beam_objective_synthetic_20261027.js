#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
let checks=0;
function check(condition,message){checks++;assert.ok(condition,message);}
const firstStage=[{id:'A',preliminary:8},{id:'B',preliminary:7}];
const outcomes=[
{id:'A1',root:'A',tax:5,legacy:7},
{id:'A2',root:'A',tax:6,legacy:9},
{id:'B1',root:'B',tax:3,legacy:3},
{id:'B2',root:'B',tax:4,legacy:4}];
function choose(options,objective){
 const sorted=[...options].sort((x,y)=>objective==='tax'?x.tax-y.tax||x.id.localeCompare(y.id):y.legacy-x.legacy||x.id.localeCompare(y.id));
 return sorted[0];
}
function beam(width,objective){
 const roots=[...firstStage].sort((x,y)=>y.preliminary-x.preliminary).slice(0,width);
 return choose(outcomes.filter(p=>roots.some(r=>r.id===p.root)),objective);
}
function dominates(a,b){return a.tax<=b.tax&&a.legacy>=b.legacy&&(a.tax<b.tax||a.legacy>b.legacy);}
check(firstStage.length===2,'two roots');
check(outcomes.length===4,'four options');
check(new Set(outcomes.map(x=>x.id)).size===4,'unique options');
check(beam(1,'tax').id==='A1','narrow tax');
check(beam(2,'tax').id==='B1','wide tax');
check(beam(1,'tax').tax>beam(2,'tax').tax,'missed optimum');
check(beam(2,'legacy').id==='A2','legacy winner');
check(beam(1,'legacy').id==='A2','narrow legacy');
check(beam(2,'tax').id!==beam(2,'legacy').id,'objective conflict');
check(outcomes.every(x=>x.tax>=0&&x.legacy>=0),'nonnegative');
check(outcomes.every(x=>!outcomes.some(y=>dominates(y,x))),'all nondominated');
check(outcomes.filter(x=>x.tax<=4).length===2,'tax ceiling');
check(outcomes.filter(x=>x.legacy>=7).length===2,'legacy floor');
check(outcomes.filter(x=>x.tax<=4&&x.legacy>=7).length===0,'infeasible intersection');
for(const x of outcomes){
 check(Number.isInteger(x.tax),'tax integer');
 check(Number.isInteger(x.legacy),'legacy integer');
 check(firstStage.some(y=>y.id===x.root),'root exists');
 check(!dominates(x,x),'irreflexive');
}
for(const objective of ['tax','legacy']){
 check(choose(outcomes,objective).id===beam(2,objective).id,'full width');
 check(outcomes.some(x=>x.id===beam(1,objective).id),'narrow valid');
}
check(checks===34,'count before final assertion');
console.log(JSON.stringify({checks,failed:0,beam1_tax:beam(1,'tax'),beam2_tax:beam(2,'tax'),beam2_legacy:beam(2,'legacy'),pareto_options:outcomes.length}));
