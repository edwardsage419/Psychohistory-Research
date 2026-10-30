"use strict";
/* F009 phase23 synthetic two-device acknowledgement replay and inventory gate.
 * Authenticated is an assumed boolean. No cryptography or actual erasure.
 */
function strictGate(s){
 return s.devices.every(x=>x==="FRESH")&&s.inventoryComplete&&s.backupsCleared&&s.authenticated&&!s.restorePending;
}
function naiveGate(s){return s.devices.every(x=>x!=="MISSING");}
function run(){
 const vals=["FRESH","STALE","MISSING"];let states=0,strict=0,naive=0,unsafeNaive=0,assertions=0;
 function ok(v,name){assertions++;if(!v)throw Error("FAIL "+name);}
 for(const a of vals)for(const b of vals)
 for(const inventoryComplete of [false,true])
 for(const backupsCleared of [false,true])
 for(const authenticated of [false,true])
 for(const restorePending of [false,true]){
  const s={devices:[a,b],inventoryComplete,backupsCleared,authenticated,restorePending};
  const x=strictGate(s),y=naiveGate(s);states++;strict+=Number(x);naive+=Number(y);
  unsafeNaive+=Number(y&&!x);
  ok(!x||(a==="FRESH"&&b==="FRESH"&&inventoryComplete&&backupsCleared&&authenticated&&!restorePending),"strict preconditions");
 }
 ok(states===144,"complete synthetic grid");
 ok(strict===1,"one strictly qualified state");
 ok(naive===64&&unsafeNaive===63,"naive overacceptance");
 const base={devices:["FRESH","FRESH"],inventoryComplete:true,backupsCleared:true,authenticated:true,restorePending:false};
 ok(strictGate(base),"qualified synthetic state");
 ok(!strictGate({...base,devices:["STALE","FRESH"]})&&naiveGate({...base,devices:["STALE","FRESH"]}),"old acknowledgement replay");
 ok(!strictGate({...base,inventoryComplete:false}),"unknown replica");
 ok(!strictGate({...base,authenticated:false}),"unauthenticated acknowledgement");
 ok(!strictGate({...base,restorePending:true}),"pending restore");
 return {states,strict,naive,unsafeNaive,assertions,synthetic:true};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
