#!/usr/bin/env node
"use strict";
const result=(function(){
const counts={},examples={};let assertions=0;
function check(x,msg){assertions++;if(!x)throw Error(msg);}
function classify(flags){
 const [stale,tomb,alias,approve,primaryComp,secondary,oldRevoked,fresh]=flags;
 if(!stale)return "NO_RESTORE_NEEDED";
 if(!tomb||!alias||!fresh||(primaryComp&&!secondary))return "UNKNOWN_QUARANTINE";
 if(!approve||!oldRevoked)return "REJECT_PENDING_AUTHORIZATION";
 return "REVIEW_ONLY";
}
for(let mask=0;mask<256;mask++){
 const flags=Array.from({length:8},(_,i)=>Boolean(mask&(1<<i)));
 const status=classify(flags);
 counts[status]=(counts[status]||0)+1;
 if(examples[status]===undefined)examples[status]=mask;
}
check(counts.NO_RESTORE_NEEDED===128,"no restore");
check(counts.UNKNOWN_QUARANTINE===116,"quarantine");
check(counts.REJECT_PENDING_AUTHORIZATION===9,"reject");
check(counts.REVIEW_ONLY===3,"review");
check(Object.values(counts).reduce((a,b)=>a+b,0)===256,"coverage");
check(classify([true,true,true,true,true,false,true,true])==="UNKNOWN_QUARANTINE","compromised primary without fallback");
check(classify([true,true,true,true,true,true,true,false])==="UNKNOWN_QUARANTINE","stale notice replay");
check(classify([true,true,true,true,true,true,true,true])==="REVIEW_ONLY","fallback with fresh notice review");
check(classify([true,true,true,false,false,false,true,true])==="REJECT_PENDING_AUTHORIZATION","notification cannot authorize");
check(!Object.hasOwn(counts,"AUTO_ALLOW"),"no auto restore");
return {counts,examples,assertions,synthetic:true};

})();
console.log(JSON.stringify(result,null,2));
