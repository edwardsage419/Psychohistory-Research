// MKT069 Eventide checkpoint and identifier synthetic boundary tests.
// Node 18+ standard library only; no database or upstream package executed.
"use strict";
function test(){
 let checks=0;
 function yes(ok,label){checks++;if(!ok)throw Error("CHECK "+checks+": "+label);}
 const store=new Map();
 const positionName=(category,id)=>category+"+position"+(id?"-"+id:"");
 function processBatch(category,id,interval,positions,effects,fail){
  const name=positionName(category,id);let counter=0,processed=[];
  for(const pos of positions){
   effects.push("first:"+pos);
   if(pos===fail)throw Error("synthetic second handler failure at "+pos);
   effects.push("second:"+pos);processed.push(pos);counter++;
   if(counter>=interval){store.set(name,pos);counter=0;}
  }
  return {checkpoint:store.get(name)||0,processed,counter};
 }
 yes(positionName("account:command",null)==="account:command+position","default checkpoint stream");
 yes(positionName("account:command","A")==="account:command+position-A","qualified checkpoint stream");
 yes(positionName("account:command","A")!==positionName("account:command","B"),"distinct identifiers");
 let effects=[];
 let a=processBatch("demo","A",5,[1,2,3,4,5,6,7],effects);
 yes(a.checkpoint===5,"checkpoint every five");
 yes(a.counter===2,"unpersisted two");
 yes(effects.length===14,"all two handlers completed");
 let restarted=[1,2,3,4,5,6,7].filter(p=>p>a.checkpoint);
 yes(restarted.join(",")==="6,7","replay after restart");
 yes(restarted.every(p=>effects.includes("second:"+p)),"duplicate side effects possible");
 let immediate=processBatch("fast","A",1,[1,2,3],[]);
 yes(immediate.checkpoint===3,"interval one");
 let slow=processBatch("slow","A",100,Array.from({length:99},(_,i)=>i+1),[]);
 yes(slow.checkpoint===0,"default interval 100 leaves no checkpoint after 99");
 yes(slow.counter===99,"99 pending updates");
 let failEffects=[];
 try{processBatch("failed","A",1,[1,2,3],failEffects,2);yes(false,"expected handler failure");}catch(e){yes(/second handler failure/.test(e.message),"failure propagates");}
 yes(store.get(positionName("failed","A"))===1,"failed second handler does not advance checkpoint");
 yes(failEffects.includes("first:2")&&!failEffects.includes("second:2"),"first handler side effect may duplicate");
 let sharedA=processBatch("shared",null,1,[1,2,3,4,5],[]);
 let sharedB=processBatch("shared",null,1,[6,7,8,9,10],[]);
 yes(sharedA.checkpoint===5,"first shared consumer checkpoint");
 yes(sharedB.checkpoint===10,"second overwrites shared position");
 yes(store.get(positionName("shared",null))===10,"shared position latest");
 yes([6,7,8,9,10].filter(x=>x>(store.get(positionName("shared",null))||0)).length===0,"restart A skips its unprocessed messages");
 processBatch("isolated","A",1,[1,2,3],[]);
 processBatch("isolated","B",1,[1,2,3,4,5],[]);
 yes(store.get(positionName("isolated","A"))===3,"isolated A checkpoint");
 yes(store.get(positionName("isolated","B"))===5,"isolated B checkpoint");
 const assign=(hash,size)=>hash%size;
 yes(assign(3,2)===1&&assign(3,3)===0,"resizing moves synthetic stream hash3 to member0");
 yes(assign(6,2)===0&&assign(6,3)===0,"stream hash6 remains member0");
 const oldMember0Checkpoint=20;
 const movedMessage={hash:3,position:9};
 yes(assign(movedMessage.hash,2)!==0,"moved message originally outside member0");
 yes(assign(movedMessage.hash,3)===0,"moved message now member0");
 yes(movedMessage.position<oldMember0Checkpoint,"reusing old checkpoint skips moved message");
 let separated=[{category:"alpha",pos:1},{category:"beta",pos:2}];
 yes(separated.filter(x=>x.category==="alpha").map(x=>x.pos).join()==="1","category isolation");
 yes(separated.filter(x=>x.category==="beta").map(x=>x.pos).join()==="2","other category independent");
 yes(store.size===6,"six distinct checkpoint streams");
 return {checks,status:"PASS",synthetic_only:true,default_interval:100,observed_replay:2,checkpoint_collision:true,resize_risk_conditional:true};
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(test(),null,2));