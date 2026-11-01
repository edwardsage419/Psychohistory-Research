'use strict';
// F009 phase51 artificial offline revocation freshness, no cryptography.
function decide(s,r){
 if(!r.request)return 'NO_REQUEST';
 if(!s||s.signature!=='valid'||s.account!==r.account||s.issued>r.now||s.ttl<0)return 'UNKNOWN_QUARANTINE';
 if(s.status==='revoked')return 'REJECT';
 if(s.status!=='active'||r.now-s.issued>s.ttl||r.now-s.issued>r.maxAge)return 'UNKNOWN_QUARANTINE';
 if(r.highImpact&&!r.online)return 'UNKNOWN_QUARANTINE';
 if(r.online==='revoked')return 'REJECT';
 if(r.online&&r.online!=='active')return 'UNKNOWN_QUARANTINE';
 return 'REVIEW_ONLY';
}
function run(){
 let n=0;const a=(v,s)=>{if(!v)throw Error(s);n++};
 const s={signature:'valid',account:'test',issued:0,ttl:24,status:'active'};
 const r={request:true,account:'test',now:6,maxAge:8,highImpact:true,online:null};
 const A={cached:s,revokedAt:null},B={cached:s,revokedAt:3};
 a(JSON.stringify(A.cached)===JSON.stringify(B.cached),'same evidence');
 a(decide(A.cached,r)==='UNKNOWN_QUARANTINE','A offline');
 a(decide(B.cached,r)==='UNKNOWN_QUARANTINE','B offline');
 a(decide(s,{...r,highImpact:false})==='REVIEW_ONLY','low impact');
 a(decide(s,{...r,highImpact:false,maxAge:2})==='UNKNOWN_QUARANTINE','max age');
 a(decide(s,{...r,highImpact:false,now:25,maxAge:30})==='UNKNOWN_QUARANTINE','ttl');
 a(decide(s,{...r,online:'revoked'})==='REJECT','online revoked');
 a(decide(s,{...r,online:'active'})==='REVIEW_ONLY','online active');
 a(decide({...s,signature:'bad'},r)==='UNKNOWN_QUARANTINE','signature');
 a(decide({...s,status:'revoked'},r)==='REJECT','cached revoked');
 a(decide({...s,account:'other'},r)==='UNKNOWN_QUARANTINE','binding');
 a(decide({...s,issued:7},r)==='UNKNOWN_QUARANTINE','future');
 a(decide(s,{...r,request:false})==='NO_REQUEST','no request');
 return {tests:n,pass:true,indistinguishable_offline_worlds:true,automatic_high_impact_restores:0,scope:'ARTIFICIAL_NONBLIND_E1'};
}
module.exports={decide,run};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
