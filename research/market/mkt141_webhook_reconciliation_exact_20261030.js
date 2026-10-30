"use strict";
// MKT141: artificial E1, no real user data, no network or paid services.
const assert=(x,m)=>{if(!x)throw Error("assertion: "+m);};
const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){const t=a%b;a=b;b=t;}return a||1;};
const frac=(a,b)=>{if(!Number.isInteger(a)||!Number.isInteger(b)||b<=0)throw Error("fraction");const g=gcd(a,b);return (b/g===1)?String(a/g):a/g+"/"+b/g;};
const source=[
 ["A1","before",1],["A2","before",1],["A3","before",1],
 ["A4","before",1],["A5","before",1],["A6","before",0],
 ["B1","after",1],["B2","after",1],["B3","after",1],
 ["B4","after",0],["B5","after",0],["B6","after",0]
];
const index=new Map(source.map(x=>[x[0],{group:x[1],value:x[2]}]));
function evaluate(observed){
 if(!(observed instanceof Map))throw Error("map required");
 const groups={before:{known:0,success:0},after:{known:0,success:0}};
 for(const [id,value] of observed){
   const ref=index.get(id);
   if(!ref||!(value===0||value===1))throw Error("invalid event");
   groups[ref.group].known++;groups[ref.group].success+=value;
 }
 for(const name of ["before","after"]){
   const g=groups[name];if(g.known>6)throw Error("duplicate event");
   g.unknown=6-g.known;
   g.observed_rate=g.known?frac(g.success,g.known):null;
   g.lower=frac(g.success,6);g.upper=frac(g.success+g.unknown,6);
 }
 const a=groups.before,b=groups.after;
 return {before:groups.before,after:groups.after,
   observed_change:(a.known&&b.known)?frac(b.success*a.known-a.success*b.known,b.known*a.known):null,
   change_lower:frac(b.success-a.success-a.unknown,6),
   change_upper:frac(b.success+b.unknown-a.success,6),
   completeness:(a.unknown+b.unknown===0)?"COMPLETE_SNAPSHOT":"PARTIAL_UNKNOWN"};
}
function fullMap(){return new Map(source.map(x=>[x[0],x[2]]));}
function run(){
 let tests=0;const check=(x,m)=>{tests++;assert(x,m);};
 const delivered=new Map(["A1","A6","B1","B2","B3","B4"].map(id=>[id,index.get(id).value]));
 const s0=evaluate(delivered);
 check(s0.observed_change==="1/4","webhook apparent gain");
 check(s0.change_lower==="-1/3"&&s0.change_upper==="2/3","unknown bounds");
 check(s0.completeness==="PARTIAL_UNKNOWN","partial status");
 check(s0.before.known===2&&s0.after.known===4,"webhook counts");
 const s1=evaluate(fullMap());
 check(s1.observed_change==="-1/3","full reconciliation reverses sign");
 check(s1.completeness==="COMPLETE_SNAPSHOT","complete only with all slots");
 const sourceRevised=fullMap();sourceRevised.set("B1",0);
 const stale=evaluate(fullMap());const revised=evaluate(sourceRevised);
 check(stale.observed_change==="-1/3"&&revised.observed_change==="-1/2","silent update");
 const incremental=fullMap();incremental.set("B1",0);
 check(evaluate(incremental).observed_change==="-1/2","updated-at reconciliation");
 const deleted=new Map(incremental);deleted.delete("A6");
 const s4=evaluate(deleted);
 check(s4.change_lower==="-2/3"&&s4.change_upper==="-1/2","deletion unknown bounds");
 check(s4.completeness==="PARTIAL_UNKNOWN","deleted slot not zero");
 check(s4.before.unknown===1,"deleted slot unknown");
 const bad=[()=>evaluate(null),()=>evaluate(new Map([["UNKNOWN",1]])),()=>evaluate(new Map([["A1",2]])),()=>frac(1,0)];
 let rejected=0;for(const f of bad){try{f();}catch(e){rejected++;}}
 check(rejected===4,"invalid inputs rejected");
 return {status:"PASS",tests,invalid_rejected:rejected,
   snapshots:{webhook:s0,full:s1,revision_stale:stale,revision_source:revised,
     after_incremental:evaluate(incremental),after_delete_full:s4},
   source_event_count:12,webhook_event_count:6,
   evidence:"ARTIFICIAL_E1_INTERNAL_NONBLIND",E2:0,E3:0};
}
if(typeof module!=="undefined")module.exports={run,evaluate};
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(run(),null,2));
