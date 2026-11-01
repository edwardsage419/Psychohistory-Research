"use strict";
// MKT189: synthetic decision outcome verification. Node.js standard library only.
const assert=require("node:assert/strict");
const rows=[
 {id:"D1",p:0.8,owner:1,verified:1},
 {id:"D2",p:0.8,owner:1,verified:0},
 {id:"D3",p:0.2,owner:0,verified:null},
 {id:"D4",p:0.2,owner:0,verified:null}
];
const sq=(p,y)=>(p-y)**2,close=(a,b)=>Math.abs(a-b)<1e-12;
const owner=rows.reduce((s,r)=>s+sq(r.p,r.owner),0)/4;
const oracle=[1,0,1,0];
const full=rows.reduce((s,r,i)=>s+sq(r.p,oracle[i]),0)/4;
const known=rows.filter(r=>r.verified!==null).length;
const lo=rows.reduce((s,r)=>s+(r.verified===null?Math.min(sq(r.p,0),sq(r.p,1)):sq(r.p,r.verified)),0)/4;
const hi=rows.reduce((s,r)=>s+(r.verified===null?Math.max(sq(r.p,0),sq(r.p,1)):sq(r.p,r.verified)),0)/4;
const flow={encrypted_at_rest:true,server_decrypts:true,external_inference_data:true,model_training:false,ai_opt_out:true};
let tests=0;function check(v,msg){assert.ok(v,msg);tests++;}
check(rows.length===4,"rows");check(rows.every(r=>r.owner!==null),"owner complete");
check(close(owner,.04),"owner brier");check(close(full,.34),"oracle brier");
check(known===2,"verified count");check(close(lo,.19),"lower");
check(close(hi,.49),"upper");check(full>=lo&&full<=hi,"oracle in bounds");
check(owner<lo,"self report optimism");check(rows[1].owner!==rows[1].verified,"disagreement");
check(flow.server_decrypts&&flow.external_inference_data,"inference data flow");
check(flow.model_training===false&&flow.external_inference_data,"training vs inference");
check(flow.encrypted_at_rest&&flow.server_decrypts,"at rest distinction");
check(flow.ai_opt_out,"vendor opt out claim");
console.log(JSON.stringify({tests,owner_brier:owner,oracle_brier:full,verified_coverage:known/4,bounds:[lo,hi],scope:"artificial E1; vendor flow fields are official-document claims"}));
