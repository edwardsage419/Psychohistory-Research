'use strict';
// F009 phase 8: synthetic relying-party registration and manager-copy separation.
const assert=require('node:assert/strict');
let checks=0;
const eq=(a,b)=>{assert.deepEqual(a,b);checks++;};
const reject=(fn)=>{assert.throws(fn,TypeError);checks++;};
function authorize(state,rp,credential,epoch){
  if (!state || !state[rp] || !state[rp][credential] || !Number.isSafeInteger(epoch) || epoch<0)
    throw new TypeError('invalid RP/credential/epoch');
  const c=state[rp][credential];
  return c.active && c.epoch===epoch && c.signatureVerified===true;
}
const state={
  rpA:{passA:{active:true,epoch:1,signatureVerified:true}},
  rpB:{passB:{active:true,epoch:2,signatureVerified:true}}
};
const manager={passA:true,passB:true};
eq(authorize(state,'rpA','passA',1),true);
eq(authorize(state,'rpB','passB',2),true);
state.rpA.passA.active=false;
eq(authorize(state,'rpA','passA',1),false);
eq(manager.passA,true); // RP revocation does not prove private-key deletion.
eq(authorize(state,'rpB','passB',2),true);
manager.passA=false;
eq(authorize(state,'rpA','passA',1),false);
eq(manager.passB,true);
state.rpA.passNew={active:true,epoch:2,signatureVerified:true};
eq(authorize(state,'rpA','passNew',1),false);
eq(authorize(state,'rpA','passNew',2),true);
state.rpA.passNew.signatureVerified=false;
eq(authorize(state,'rpA','passNew',2),false);
reject(()=>authorize(state,'rpC','passA',1));
reject(()=>authorize(state,'rpA','passB',2));
reject(()=>authorize(state,'rpA','passA',-1));
reject(()=>authorize(state,'rpA','passA',1.5));
reject(()=>authorize(null,'rpA','passA',1));
console.log(JSON.stringify({evidence:'E1_ARTIFICIAL_NONBLIND',checks,
  rpA_old_revoked:true,manager_copy_after_rp_revoke:true,rpB_unchanged:true,
  actual_signatures_verified:false}));
