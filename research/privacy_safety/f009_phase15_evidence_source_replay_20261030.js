'use strict';
// Boolean evidence gate only. No signature, issuer, nonce or cryptographic verification is performed.
const assert=require('node:assert/strict');
const fields=['payloadIntegrity','trustedIssuer','verifiedSignature','freshNonce','accountBound'];
function gate(e){
 if(Object.keys(e).sort().join('|')!==fields.slice().sort().join('|')) throw Error('schema');
 if(fields.some(k=>typeof e[k]!=='boolean')) throw Error('types');
 return fields.every(k=>e[k])?'REVIEWABLE_SOURCE_CLAIM':'QUARANTINE_UNKNOWN';
}
let checks=0, accepted=0;
for(let mask=0;mask<32;mask++){
 const e=Object.fromEntries(fields.map((f,i)=>[f,Boolean(mask&(1<<i))]));
 const verdict=gate(e);
 assert.equal(verdict,mask===31?'REVIEWABLE_SOURCE_CLAIM':'QUARANTINE_UNKNOWN');
 accepted+=Number(verdict==='REVIEWABLE_SOURCE_CLAIM');checks++;
}
assert.equal(accepted,1);checks++;
for(const [k,v] of [['payloadIntegrity','yes'],['trustedIssuer',null],['verifiedSignature',1],['freshNonce',undefined]]){
 const e=Object.fromEntries(fields.map(f=>[f,true]));e[k]=v;
 assert.throws(()=>gate(e));checks++;
}
const old=Object.fromEntries(fields.map(f=>[f,true]));old.freshNonce=false;
assert.equal(gate(old),'QUARANTINE_UNKNOWN');checks++;
const wrongAccount=Object.fromEntries(fields.map(f=>[f,true]));wrongAccount.accountBound=false;
assert.equal(gate(wrongAccount),'QUARANTINE_UNKNOWN');checks++;
const extra=Object.fromEntries(fields.map(f=>[f,true]));extra.email='private@example.invalid';
assert.throws(()=>gate(extra));checks++;
console.log(JSON.stringify({status:'PASS',checks,worlds:32,eligible:accepted,rejected:31,scope:'BOOLEAN_ORACLE_TOY_NO_CRYPTOGRAPHY'}));
