#!/usr/bin/env node
'use strict';
// Synthetic as-of datapoint revisions. This does not implement Beeminder billing.
const assert = require('node:assert/strict');
const threshold = 2;
const histories = {
  A: [{at:0,value:2,kind:'initial'}, {at:2,value:1,kind:'correction'}, {at:3,value:2,kind:'correction'}],
  B: [{at:0,value:1,kind:'initial'}, {at:2,value:2,kind:'correction'}]
};
function asOf(events,time){
  const visible=events.filter(e=>e.at<=time);
  return visible.length?visible.at(-1).value:null;
}
function status(events,time){const v=asOf(events,time);return v===null?'UNKNOWN':v>=threshold?'SAFE':'SHORT';}
const output={research:'MKT153',evidence:'INTERNAL_NONBLIND_ARTIFICIAL_E1',threshold,
  deadline_time:1,final_time:3,worlds:{}};
for(const [name,events] of Object.entries(histories)){
  output.worlds[name]={at_deadline:asOf(events,1),status_at_deadline:status(events,1),
    after_first_revision:asOf(events,2),status_after_first_revision:status(events,2),
    final:asOf(events,3),final_status:status(events,3)};
}
let tests=0;function check(cond,label){assert.ok(cond,label);tests++;}
check(output.worlds.A.at_deadline===2,'A original');
check(output.worlds.B.at_deadline===1,'B original');
check(output.worlds.A.status_at_deadline==='SAFE','A safe');
check(output.worlds.B.status_at_deadline==='SHORT','B short');
check(output.worlds.A.after_first_revision===1,'A corrected down');
check(output.worlds.B.after_first_revision===2,'B corrected up');
check(output.worlds.A.status_after_first_revision==='SHORT','A retro short');
check(output.worlds.B.status_after_first_revision==='SAFE','B retro safe');
check(output.worlds.A.final===output.worlds.B.final,'same final snapshot');
check(output.worlds.A.final_status===output.worlds.B.final_status,'same final status');
check(output.worlds.A.status_at_deadline!==output.worlds.B.status_at_deadline,'history nonidentification');
check(asOf(histories.A,-1)===null,'unknown pre-collection');
check(asOf(histories.B,-1)===null,'unknown pre-collection B');
check(1+7===8,'illustrative 7 day delay');
check(histories.A.every((e,i)=>i===0||e.at>histories.A[i-1].at),'A monotone event time');
check(histories.B.every((e,i)=>i===0||e.at>histories.B[i-1].at),'B monotone event time');
output.assertions_passed=tests;
if(require.main===module)console.log(JSON.stringify(output,null,2));
module.exports={asOf,status,histories,output};
