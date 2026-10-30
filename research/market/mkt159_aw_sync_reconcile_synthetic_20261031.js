"use strict";
/* MKT159 synthetic subset of ActivityWatch aw-sync reconciliation.
 * Pinned upstream: ActivityWatch/aw-server-rust fe353a66, aw-sync/src/sync.rs 942-1064.
 * No Rust runtime or real user data is exercised.
 */
function reconcile(source,destination,resumeDay,lookbackDays=7){
 const output=destination.map(e=>({...e}));
 const ids=new Set(source.filter(e=>e.t>=resumeDay-lookbackDays&&e.t<resumeDay).map(e=>e.t+"|"+e.d));
 for(const id of ids){
   const from=source.filter(e=>e.t+"|"+e.d===id);
   const indexes=output.map((e,i)=>e.t+"|"+e.d===id?i:-1).filter(i=>i>=0);
   if(!indexes.length)continue;
   for(let i=indexes.length-1;i>=0;i--)output.splice(indexes[i],1);
   output.push(...from.map(e=>({...e})));
 }
 return output.sort((a,b)=>a.t-b.t||a.d-b.d||a.data.localeCompare(b.data));
}
function run(){
 let checks=0;function ok(v,name){checks++;if(!v)throw Error("FAIL "+name);}
 const e=(t,d,data)=>({t,d,data});
 let got=reconcile([e(14,1,"edited")],[e(14,1,"old")],20);
 ok(got.length===1&&got[0].data==="edited","recent owner edit");
 got=reconcile([e(12,1,"edited")],[e(12,1,"old")],20);
 ok(got[0].data==="old","outside seven-day lookback");
 got=reconcile([],[e(14,1,"orphan")],20);
 ok(got.length===1&&got[0].data==="orphan","whole identity deletion not propagated");
 got=reconcile([e(14,1,"kept")],[e(14,1,"kept"),e(14,1,"removed")],20);
 ok(got.length===1&&got[0].data==="kept","same-identity sibling pruning");
 got=reconcile([e(14,1,"new")],[],20);
 ok(got.length===0,"source-only identity not copied by reconciliation");
 got=reconcile([e(14,2,"edited")],[e(14,1,"old")],20);
 ok(got.length===1&&got[0].data==="old","duration is part of identity");
 got=reconcile([e(14,1,"edited")],[e(14,1,"old")],30);
 ok(got[0].data==="old","window anchored to destination cursor");
 got=reconcile([e(14,1,"same")],[e(14,1,"same")],20);
 ok(got.length===1&&got[0].data==="same","idempotent matching payload");
 got=reconcile([e(20,1,"new")],[e(20,1,"old")],20);
 ok(got[0].data==="old","event at resume cursor excluded");
 return {checks,passed:checks,synthetic:true};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
