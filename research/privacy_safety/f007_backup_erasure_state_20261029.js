#!/usr/bin/env node
'use strict';
/* Synthetic reference graph for backup erasure evidence. Never runs restic. */
let checks=0;
function ok(v,m){checks++;if(!v)throw Error(m);}
function model(){return {
  snapshots:new Map([['S1',new Set(['P','Q'])],['S2',new Set(['P','R'])]]),
  blobs:new Set(['P','Q','R']), keys:new Set(['K1','K2']),
  externalCopies:'UNKNOWN',mediaErasure:'UNVERIFIED'
};}
function forget(state,id){return state.snapshots.delete(id);}
function prune(state){
  const referenced=new Set([...state.snapshots.values()].flatMap(x=>[...x]));
  for(const blob of [...state.blobs])if(!referenced.has(blob))state.blobs.delete(blob);
}
function canRead(state,blob){return state.blobs.has(blob)&&state.keys.size>0;}
function evidence(state,blob){return {
  localBlobPresent:state.blobs.has(blob),localKeys:state.keys.size,
  externalCopies:state.externalCopies,mediaErasure:state.mediaErasure,
  globallyErased:'UNVERIFIED'
};}
function run(){
  const s=model();
  ok(canRead(s,'P'),'initial P readable');
  ok(s.snapshots.size===2,'two snapshots');
  ok(forget(s,'S1'),'forget S1');
  ok(s.snapshots.size===1,'one snapshot');
  ok(s.blobs.has('Q'),'forget alone leaves blob Q');
  ok(s.blobs.has('P'),'forget alone leaves shared P');
  prune(s);
  ok(!s.blobs.has('Q'),'prune removes Q');
  ok(s.blobs.has('P'),'shared P retained');
  ok(s.blobs.has('R'),'R retained');
  s.keys.delete('K1');
  ok(s.keys.has('K2'),'second key remains');
  ok(canRead(s,'P'),'removing one key leaves access');
  ok(evidence(s,'P').globallyErased==='UNVERIFIED','no global erasure claim');
  ok(forget(s,'S2'),'forget S2');
  ok(s.blobs.has('P'),'forget S2 alone leaves P');
  prune(s);
  ok(!s.blobs.has('P'),'prune removes local P');
  ok(s.blobs.size===0,'all local blobs gone');
  ok(evidence(s,'P').externalCopies==='UNKNOWN','external copies unverified');
  ok(evidence(s,'P').mediaErasure==='UNVERIFIED','media erasure unverified');
  ok(evidence(s,'P').globallyErased==='UNVERIFIED','cannot assert complete deletion');
  const t=model();t.keys.clear();
  ok(!canRead(t,'P'),'no listed local key blocks model access');
  ok(t.blobs.has('P'),'no keys does not delete ciphertext');
  ok(evidence(t,'P').globallyErased==='UNVERIFIED','key absence insufficient');
  process.stdout.write(JSON.stringify({checks,failures:0,sharedBlobSurvivesFirstPrune:true,
    secondKeyPreservesAccess:true,localBlobRemovedAfterFinalPrune:true,
    globalErasure:'UNVERIFIED'})+'\n');
}
if(require.main===module)run();
module.exports={model,forget,prune,evidence,run};
