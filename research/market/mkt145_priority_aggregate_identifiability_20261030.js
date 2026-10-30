"use strict";
// Artificial minute-level illustration. This is NOT an implementation of Health Connect.
const SEGMENTS=[
 {minutes:10,appA:100,appB:80},
 {minutes:10,appA:50,appB:0}
];
function validate(segments){
 if(!Array.isArray(segments)||segments.length===0)throw Error("empty segments");
 for(const s of segments){
  if(!Number.isSafeInteger(s.minutes)||s.minutes<=0)throw Error("invalid minutes");
  for(const k of ["appA","appB"])if(!Number.isSafeInteger(s[k])||s[k]<0)throw Error("invalid counts");
 }
}
function aggregateToy(segments,priority){
 validate(segments);
 if(!["appA","appB"].includes(priority))throw Error("unknown priority");
 let total=0;
 for(const s of segments){
  const both=s.appA>0&&s.appB>0;
  total+=s.minutes*(both?s[priority]:s.appA+s.appB);
 }
 return total;
}
function rawSum(segments){
 validate(segments);return segments.reduce((n,s)=>n+s.minutes*(s.appA+s.appB),0);
}
function priorityInterval(segments){
 return {lower:Math.min(aggregateToy(segments,"appA"),aggregateToy(segments,"appB")),
 upper:Math.max(aggregateToy(segments,"appA"),aggregateToy(segments,"appB")),
 status:"PRIORITY_UNVERIFIED"};
}
function assert(ok,name){if(!ok)throw Error("ASSERT "+name);}
function expectReject(fn,name){let rejected=false;try{fn();}catch(e){rejected=true;}assert(rejected,name);}
function runTests(){
 let passed=0;
 function check(ok,name){assert(ok,name);passed++;}
 function bad(fn,name){expectReject(fn,name);passed++;}
 check(rawSum(SEGMENTS)===2300,"raw sum");
 check(aggregateToy(SEGMENTS,"appA")===1500,"A priority");
 check(aggregateToy(SEGMENTS,"appB")===1300,"B priority");
 check(priorityInterval(SEGMENTS).lower===1300,"lower");
 check(priorityInterval(SEGMENTS).upper===1500,"upper");
 check(priorityInterval(SEGMENTS).status==="PRIORITY_UNVERIFIED","unknown status");
 check(aggregateToy(SEGMENTS,"appA")-aggregateToy(SEGMENTS,"appB")===200,"priority difference");
 check(SEGMENTS.reduce((n,s)=>n+s.minutes*s.appA,0)===1500,"origin A");
 check(SEGMENTS.reduce((n,s)=>n+s.minutes*s.appB,0)===800,"origin B");
 check(rawSum([{minutes:1,appA:1,appB:0}])===1,"single source");
 check(aggregateToy([{minutes:1,appA:0,appB:7}],"appA")===7,"missing priority source");
 bad(()=>aggregateToy(SEGMENTS,"appC"),"unknown priority rejected");
 bad(()=>aggregateToy([],"appA"),"empty rejected");
 bad(()=>aggregateToy([{minutes:0,appA:1,appB:1}],"appA"),"zero minutes rejected");
 bad(()=>rawSum([{minutes:1,appA:-1,appB:2}]),"negative rejected");
 bad(()=>rawSum([{minutes:1,appA:1.5,appB:2}]),"fraction rejected");
 return {passed,raw:rawSum(SEGMENTS),priorityA:aggregateToy(SEGMENTS,"appA"),
 priorityB:aggregateToy(SEGMENTS,"appB"),unverified:priorityInterval(SEGMENTS)};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(runTests()));
