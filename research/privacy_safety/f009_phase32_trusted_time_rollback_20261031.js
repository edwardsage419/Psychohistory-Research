"use strict";
let checks=0;function check(v,m){checks++;if(!v)throw Error(m);}
const expiry=110,rev=2;
function naive(s){return s.signature&&s.local_now<expiry?"ACCEPT":"REJECT";}
function guarded(s){
if(!s.signature)return "REJECT";
if(s.trusted_now!==null&&s.trusted_now>=expiry)return "REJECT";
if(s.trusted_now===null||s.trusted_now<s.last_trusted||s.cached_rev<rev||!s.online||!s.witness_current)return "UNKNOWN";
return "REVIEW";
}
function run(){
const counts={REVIEW:0,UNKNOWN:0,REJECT:0},naiveCounts={ACCEPT:0,REJECT:0};let states=0,naiveOnly=0;
for(const trusted_now of [null,90,100,115])
for(const last_trusted of [95,105])
for(const cached_rev of [1,2])
for(const local_now of [95,105])
for(const online of [false,true])
for(const witness_current of [false,true])
for(const signature of [false,true]){
let s={trusted_now,last_trusted,cached_rev,local_now,online,witness_current,signature},n=naive(s),g=guarded(s);
states++;counts[g]++;naiveCounts[n]++;
check(["REVIEW","UNKNOWN","REJECT"].includes(g),"state");
check(g!=="REVIEW"||(signature&&trusted_now!==null&&trusted_now>=last_trusted&&trusted_now<expiry&&cached_rev===rev&&online&&witness_current),"review invariant");
if(n==="ACCEPT"&&g!=="REVIEW")naiveOnly++;
}
check(states===256,"coverage");check(counts.REVIEW===2&&counts.UNKNOWN===94&&counts.REJECT===160,"histogram");
check(naiveCounts.ACCEPT===128&&naiveOnly===126,"naive gap");
const s={trusted_now:100,last_trusted:95,cached_rev:2,local_now:95,online:true,witness_current:true,signature:true};
check(guarded(s)==="REVIEW","clean");
check(guarded({...s,trusted_now:90})==="UNKNOWN","rollback");
check(guarded({...s,trusted_now:null})==="UNKNOWN","no anchor");
check(guarded({...s,cached_rev:1})==="UNKNOWN","stale rev");
check(guarded({...s,online:false})==="UNKNOWN","offline");
check(guarded({...s,witness_current:false})==="UNKNOWN","witness");
check(guarded({...s,trusted_now:115})==="REJECT","expired");
check(guarded({...s,signature:false})==="REJECT","invalid signature");
return {states,checks,counts,naiveCounts,naiveOnly,evidence:"synthetic E1, no real clock/signatures"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));