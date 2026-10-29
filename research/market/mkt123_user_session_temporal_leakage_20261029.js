#!/usr/bin/env node
// MKT123 synthetic only; requires Node.js; no dependencies or personal data.
console.log(JSON.stringify((function(){
"use strict";
const records=[];
for(let user=0;user<8;user++)for(let period=0;period<4;period++)
 for(let repeat=0;repeat<2;repeat++)
  records.push({user,period,session:user+":"+period,repeat,label:(user%2)^(period===3?1:0)});
let checks=0;
function check(ok,message){checks++;if(!ok)throw Error(message);}
function validate(train,test,mode){
 check(train.every(r=>!test.some(s=>s.session===r.session&&s.repeat===r.repeat)),"row overlap");
 if(mode==="new_user"){
  const users=new Set(train.map(r=>r.user));
  check(test.every(r=>!users.has(r.user)),"user leakage");
 }else if(mode==="new_session"){
  const sessions=new Set(train.map(r=>r.session));
  check(test.every(r=>!sessions.has(r.session)),"session leakage");
 }else if(mode==="forward"){
  check(Math.max(...train.map(r=>r.period))<Math.min(...test.map(r=>r.period)),"future leakage");
 }
}
function predict(train,row){
 const history=train.filter(r=>r.user===row.user);
 if(!history.length)return 0;
 const labels=new Set(history.map(r=>r.label));
 check(labels.size===1,"training label drift mixed");
 return history[0].label;
}
function score(train,test,mode){
 validate(train,test,mode);
 const errors=test.filter(r=>predict(train,r)!==r.label).length;
 return {correct:test.length-errors,total:test.length,errors,accuracy:(test.length-errors)/test.length};
}
check(records.length===64,"record count");
for(let r of records)check(r.label===((r.user%2)^(r.period===3?1:0)),"label generator");
const retrospective=score(records.filter(r=>r.period===0||r.period===2),records.filter(r=>r.period===1),"new_session");
const newUser=score(records.filter(r=>r.user<6&&r.period<3),records.filter(r=>r.user>=6&&r.period===1),"new_user");
const forwardStable=score(records.filter(r=>r.period<=1),records.filter(r=>r.period===2),"forward");
const forwardDrift=score(records.filter(r=>r.period<=2),records.filter(r=>r.period===3),"forward");
check(retrospective.accuracy===1,"retrospective");
check(newUser.accuracy===0.5,"new user");
check(forwardStable.accuracy===1,"forward stable");
check(forwardDrift.accuracy===0,"forward drift");
let negatives=0;
for(let [train,test,mode] of [
 [records.filter(r=>r.user<6),records.filter(r=>r.user===0),"new_user"],
 [records.filter(r=>r.period<=2),records.filter(r=>r.period===2),"forward"],
 [records.filter(r=>r.period<=2),records.filter(r=>r.period===0),"new_session"]
]){
 try{validate(train,test,mode)}catch(e){negatives++;continue}
 throw Error("negative control accepted: "+mode);
}
check(negatives===3,"negative controls");
return {checks,negatives,records:records.length,retrospective,newUser,forwardStable,forwardDrift};
})(),null,2));
