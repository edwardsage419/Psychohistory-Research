// F009 phase55: synthetic common-operator witness dependence. No real credentials.
const assert = require('node:assert/strict');
const slots = [{id:'W1',domain:'OP_X'},{id:'W2',domain:'OP_X'},{id:'W3',domain:'OP_Y'}];
const replies = ['VALID','REVOKED','MISSING'];
function naive(x) {
  const valid=x.filter(v=>v==='VALID').length;
  const revoked=x.filter(v=>v==='REVOKED').length;
  return valid>=2?'REVIEW_ONLY':revoked>=2?'REJECT':'UNKNOWN';
}
function cautious(x) {
  const visible=x.filter(v=>v!=='MISSING');
  if (visible.includes('VALID') && visible.includes('REVOKED')) return 'CONFLICT_QUARANTINE';
  const domains=new Set(slots.filter((s,i)=>x[i]!=='MISSING').map(s=>s.domain));
  if(domains.size<2) return 'UNKNOWN_QUARANTINE';
  return visible[0]==='REVOKED'?'REJECT':'REVIEW_ONLY';
}
const counts={REVIEW_ONLY:0,REJECT:0,CONFLICT_QUARANTINE:0,UNKNOWN_QUARANTINE:0};
let naiveFalseIndependent=0;
for(const a of replies)for(const b of replies)for(const c of replies){
  const x=[a,b,c], v=cautious(x);
  counts[v]++;
  if(naive(x)==='REVIEW_ONLY' && v!=='REVIEW_ONLY')naiveFalseIndependent++;
}
assert.equal(Object.values(counts).reduce((a,b)=>a+b,0),27);
assert.equal(naive(['VALID','VALID','MISSING']),'REVIEW_ONLY');
assert.equal(cautious(['VALID','VALID','MISSING']),'UNKNOWN_QUARANTINE');
assert.equal(cautious(['VALID','MISSING','VALID']),'REVIEW_ONLY');
assert.equal(cautious(['VALID','VALID','REVOKED']),'CONFLICT_QUARANTINE');
assert.equal(cautious(['REVOKED','REVOKED','MISSING']),'UNKNOWN_QUARANTINE');
assert.equal(cautious(['REVOKED','MISSING','REVOKED']),'REJECT');
assert.equal(cautious(['MISSING','MISSING','MISSING']),'UNKNOWN_QUARANTINE');
assert.equal(naiveFalseIndependent>0,true);
console.log(JSON.stringify({status:'PASS',cases:27,assertions:9,counts,naiveFalseIndependent,automaticHighImpactRestore:0,scope:'E1 synthetic; operator labels assumed authentic'}));
