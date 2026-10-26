// MKT065: synthetic version-bounded snapshot retrieval. Run: node research/market/mkt065_asof_snapshot_synthetic_20261027.js
"use strict";
const events=[{v:1,d:5},{v:2,d:7},{v:3,d:-3},{v:4,d:2}];
const snapshots=[{v:2,s:12,b:"A"},{v:4,s:11,b:"A"}];
function replay(t,ss,branch="A",checkBranch=false){
 const s=ss.filter(x=>x.v<=t).sort((a,b)=>b.v-a.v)[0];
 if(s&&checkBranch&&s.b!==branch)throw Error("BRANCH_MISMATCH");
 let state=s?s.s:0,base=s?s.v:0;
 for(const e of events)if(e.v>base&&e.v<=t)state+=e.d;
 return {value:state,selected:base};
}
function run(){
 let n=0;const ok=(x,m)=>{n++;if(!x)throw Error(m);};
 const expected=[0,5,12,9,11];
 for(let t=0;t<=4;t++){let x=replay(t,snapshots);ok(x.value===expected[t],"asof");ok(x.selected<=t,"future");}
 ok(snapshots[1].s!==expected[1],"naive v1");ok(snapshots[1].s!==expected[3],"naive v3");
 ok(replay(3,[]).value===9,"no snapshot");
 ok(replay(4,[{v:9,s:999,b:"A"}]).value===11,"ignore future");
 ok(replay(4,[{v:2,s:99,b:"A"}]).value===98,"bad same-version state");
 ok(replay(4,[{v:2,s:-8,b:"B"}]).value===-9,"bad branch");
 let blocked=false;try{replay(4,[{v:2,s:-8,b:"B"}],"A",true);}catch(e){blocked=e.message==="BRANCH_MISMATCH";}
 ok(blocked,"candidate branch check");
 ok(replay(3,[{v:2,s:12,b:"A"}]).value===9,"correct prefix");
 ok(replay(3,[{v:4,s:11,b:"A"}]).value===9,"exclude future snapshot");
 return {checks:n,failures:0,asof_v3:replay(3,snapshots),naive_v3:11,corrupt_v4:98};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run,replay};
