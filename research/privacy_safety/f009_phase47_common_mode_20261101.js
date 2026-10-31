// F009 phase47 synthetic common-mode recovery, no user data.
function f47(){
 const keys=["stale","deletion","alias","revoked","fresh","notice1","notice2","reviewer","anchor","shared_admin","shared_device","offline"];
 const decide=(s,strict)=>!s.stale?"NO_RESTORE":(!s.deletion||!s.alias||!s.revoked||!s.fresh)?"UNKNOWN_QUARANTINE":(!s.notice1||!s.notice2||!s.reviewer||!s.anchor)?"REJECT_OR_REVIEW":(strict&&(s.shared_admin||s.shared_device)&&!s.offline)?"UNKNOWN_COMMON_MODE":"REVIEW_ONLY";
 const counts={},weak={};let changed=0;
 for(let i=0;i<4096;i++){const s=Object.fromEntries(keys.map((k,j)=>[k,(i>>j)&1])),x=decide(s,true),y=decide(s,false);counts[x]=(counts[x]||0)+1;weak[y]=(weak[y]||0)+1;if(x!==y)changed++}
 const tests=[Object.values(counts).reduce((a,b)=>a+b,0)===4096,counts.NO_RESTORE===2048,counts.UNKNOWN_QUARANTINE===1920,counts.REJECT_OR_REVIEW===120,counts.UNKNOWN_COMMON_MODE===3,counts.REVIEW_ONLY===5,weak.REVIEW_ONLY===8,changed===3,!counts.AUTO_RESTORE];
 if(tests.some(x=>!x))throw Error("common-mode test failed");
 return {scope:"synthetic states; no real attacks",states:4096,counts,weak,changed,automatic_restore:0,assertions:tests.length};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(f47(),null,2));
