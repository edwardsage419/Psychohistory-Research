"use strict";
// Candidate-only offline recovery code guard. Binary cases are not incident probabilities.
function decide(b,strict) {
  const [restore,present,stolen,reused,bound,notice,reviewer,revoked,ledger,anchor]=b;
  if(!restore)return "NO_RESTORE";
  if(!present)return "UNKNOWN_QUARANTINE";
  if(strict&&(stolen||reused||!bound))return "REJECT";
  if(!notice||!reviewer||!revoked||!ledger||!anchor)return "UNKNOWN_QUARANTINE";
  return "REVIEW_ONLY";
}
function run(){
  const out={},weak={},counts={};let strictReview=0,weakReview=0;
  for(let mask=0;mask<1024;mask++){
    const b=Array.from({length:10},(_,i)=>(mask>>i)&1);
    const s=decide(b,true),w=decide(b,false);
    out[s]=(out[s]||0)+1;weak[w]=(weak[w]||0)+1;
    if(s==="REVIEW_ONLY")strictReview++;
    if(w==="REVIEW_ONLY")weakReview++;
    if(s==="REVIEW_ONLY"&&(b[2]||b[3]||!b[4]))throw Error("compromised code passed");
    if(s==="REVIEW_ONLY"&&w!=="REVIEW_ONLY")throw Error("non-subset");
  }
  if(out.NO_RESTORE!==512||out.UNKNOWN_QUARANTINE!==287||out.REJECT!==224||out.REVIEW_ONLY!==1||weakReview!==8)throw Error("unexpected exact count");
  if(Object.keys(out).some(k=>k.startsWith("AUTO")))throw Error("automatic recovery");
  return {total:1024,strict:out,weak,strict_review:strictReview,weak_review:weakReview,automatic_restore:0,guard_families:4};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
