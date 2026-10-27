#!/usr/bin/env node
// MKT073. Purely synthetic contract simulation. No network or real credentials.
'use strict';
const assert = require('node:assert/strict');
let checks = 0;
const verify = (condition, label) => { checks++; assert.ok(condition, label); };
const stable = (x) => JSON.stringify({value:x.value, daystamp:x.daystamp, comment:x.comment || ''});
class ToyBeeminder {
  constructor(){this.byGoal=new Map();this.sequence=0;}
  post(goal,point){
    let entries=this.byGoal.get(goal);if(!entries){entries=[];this.byGoal.set(goal,entries);}
    const existing=point.requestid?entries.find(x=>x.requestid===point.requestid):undefined;
    if(existing){
      if(stable(existing)===stable(point))return {status:'duplicate',id:existing.id};
      Object.assign(existing,point);return {status:'updated',id:existing.id};
    }
    const id='synthetic-'+(++this.sequence);entries.push({...point,id});
    return {status:'created',id};
  }
  value(goal,requestid){return this.byGoal.get(goal)?.find(x=>x.requestid===requestid)?.value;}
  count(goal){return (this.byGoal.get(goal)||[]).length;}
}
const date='20261027';
const base={requestid:'source-42',daystamp:date,comment:'recorded',value:100};
const corrected={...base,value:25};
const service=new ToyBeeminder();
let r=service.post('focus',base);
verify(r.status==='created','first write');verify(service.count('focus')===1,'one row');verify(service.value('focus',base.requestid)===100,'original value');
r=service.post('focus',{...base});
verify(r.status==='duplicate','same request and content');verify(service.count('focus')===1,'duplicate no new row');
r=service.post('focus',corrected);
verify(r.status==='updated','same requestid differing content updates');verify(service.value('focus',base.requestid)===25,'correction stored');
r=service.post('focus',base);
verify(r.status==='updated','stale retry upserts');verify(service.value('focus',base.requestid)===100,'stale retry reverts correction');verify(service.count('focus')===1,'still only one row');
r=service.post('health',base);
verify(r.status==='created','same requestid allowed on different goal');verify(service.value('health',base.requestid)===100,'other goal independent');
service.post('focus',{value:2,daystamp:date});service.post('focus',{value:2,daystamp:date});
verify(service.count('focus')===3,'missing requestid creates two rows');
const safe=new ToyBeeminder();let revision=1;safe.post('focus',base);
const pending={...base,revision:1};
revision=2;safe.post('focus',corrected);
const sendIfCurrent=(p)=>p.revision===revision?safe.post('focus',p):{status:'rejected_stale'};
r=sendIfCurrent(pending);
verify(r.status==='rejected_stale','local generation guard');verify(safe.value('focus',base.requestid)===25,'guard preserves correction');
// Batch partial-success model: official API documents successes and errors, not atomicity.
const batch=new ToyBeeminder();
const items=[{requestid:'a',value:10,daystamp:date},{requestid:'b',value:20,daystamp:date},{requestid:'c',value:30,daystamp:date}];
const successIds=new Set(['a','c']);for(const item of items)if(successIds.has(item.requestid))batch.post('batch',item);
verify(batch.count('batch')===2,'partial batch model');
batch.post('batch',{...items[0],value:7});
verify(batch.value('batch','a')===7,'external correction');
for(const item of items)batch.post('batch',item);
verify(batch.value('batch','a')===10,'full stale batch retry overwrites correction');
verify(batch.count('batch')===3,'batch eventually three points');
const selective=new ToyBeeminder();for(const item of items)if(successIds.has(item.requestid))selective.post('batch',item);
selective.post('batch',{...items[0],value:7});
for(const item of items)if(!successIds.has(item.requestid))selective.post('batch',item);
verify(selective.value('batch','a')===7,'retry failed only preserves correction');
verify(selective.value('batch','b')===20,'failed item added');
verify(selective.count('batch')===3,'selective count');
for(let i=0;i<16;i++){
 const toy=new ToyBeeminder(),goal='g'+i,id='r'+i,v=i+1;
 toy.post(goal,{requestid:id,value:v,daystamp:date});
 toy.post(goal,{requestid:id,value:v,daystamp:date});
 verify(toy.count(goal)===1,'idempotent '+i);
 toy.post(goal,{requestid:id,value:v+10,daystamp:date});
 verify(toy.value(goal,id)===v+10,'upsert '+i);
 toy.post(goal,{requestid:id,value:v,daystamp:date});
 verify(toy.value(goal,id)===v,'stale overwrite '+i);
}
// Official docs example: request IDs 929/930, response repeats 923.
const exampleRequest=['abcd182475929','abcd182475930'];
const exampleResponse=['abcd182475923','abcd182475923'];
verify(exampleRequest[0]!==exampleResponse[0],'published sample mismatch first');
verify(exampleRequest[1]!==exampleResponse[1],'published sample mismatch second');
verify(exampleResponse[0]===exampleResponse[1],'published sample response duplicate');
console.log(JSON.stringify({study:'MKT073',checks,failures:0,network:false,real_product_test:false,main_risk:'same requestid with changed payload is an upsert; stale retry can overwrite a correction'}));
