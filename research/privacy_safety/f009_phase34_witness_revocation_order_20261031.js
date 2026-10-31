"use strict";
// Synthetic E1 only. Run: node research/privacy_safety/f009_phase34_witness_revocation_order_20261031.js
const keys=["receipt_new","witness_a_new","witness_b_new","witness_c_new","device_new","independent_root","signature_ok","ordering_proof","revocation_known"];
const out={REVIEW:0,UNKNOWN:0,REJECT:0,naiveAccept:0,naiveOutsideReview:0,staleNaive:0,correlatedNaive:0};let checks=0;
for(let i=0;i<512;i++){
 const x=Object.fromEntries(keys.map((k,j)=>[k,!!(i&(1<<j))]));
 const votes=[x.witness_a_new,x.witness_b_new,x.witness_c_new].filter(v=>v===x.receipt_new).length;
 const naive=x.signature_ok&&votes>=2;
 let strict="UNKNOWN";
 if(!x.signature_ok||(x.revocation_known&&!x.receipt_new))strict="REJECT";
 else if(keys.every(k=>x[k]))strict="REVIEW";
 out[strict]++;
 if(naive){out.naiveAccept++;if(strict!=="REVIEW")out.naiveOutsideReview++;if(!x.receipt_new)out.staleNaive++;if(!x.independent_root)out.correlatedNaive++;}
 if(strict==="REVIEW"&&!keys.every(k=>x[k]))throw Error("unsafe_review");
 if(x.revocation_known&&!x.receipt_new&&strict!=="REJECT")throw Error("revoked_old_receipt");
 if(!x.signature_ok&&strict!=="REJECT")throw Error("invalid_signature");
 checks+=3;
}
const expected={REVIEW:1,UNKNOWN:191,REJECT:320,naiveAccept:128,naiveOutsideReview:127,staleNaive:64,correlatedNaive:64};
for(const [k,v] of Object.entries(expected)){if(out[k]!==v)throw Error("wrong_"+k);checks++;}
console.log(JSON.stringify({artificial_states:512,assertions:checks,counts:out,evidence:"E1_SYNTHETIC",real_signatures:"NOT_RUN"},null,2));
