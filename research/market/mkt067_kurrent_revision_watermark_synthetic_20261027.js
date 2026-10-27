"use strict";
// Synthetic state machine inspired by documented KurrentDB API semantics.
// This does not run a KurrentDB server or its official client.
function run(){
  let checks=0;
  function ok(x,m){checks++;if(!x)throw Error("MKT067 check "+checks+": "+m);}
  class Ledger {
    constructor(){this.streams=new Map();this.commit=99;}
    get(name){return this.streams.get(name)||[];}
    append(name,expected,id,payload){
      const arr=this.get(name),current=arr.length-1;
      const eligible=expected==="ANY"||(expected==="EXISTS"&&arr.length>0)||(expected==="NO_STREAM"&&arr.length===0)||(Number.isInteger(expected)&&expected===current);
      if(!eligible){
        // An idempotent retry is modeled only for the original expected position.
        const old=arr.find((e,i)=>e.id===id&&((expected==="NO_STREAM"&&i===0)||(Number.isInteger(expected)&&i===expected+1)));
        return old?{status:"RETRY",event:old}:{status:"CONFLICT"};
      }
      const event={stream:name,id,payload,revision:arr.length,commit:++this.commit};
      this.streams.set(name,arr.concat(event));
      return {status:"APPENDED",event};
    }
  }
  const db=new Ledger();
  let a=db.append("life","NO_STREAM","evt-A",{value:1});
  ok(a.status==="APPENDED","initial append");ok(a.event.revision===0,"initial revision");ok(a.event.commit===100,"commit position");
  let retry=db.append("life","NO_STREAM","evt-A",{value:1});
  ok(retry.status==="RETRY","same request retry");ok(retry.event.commit===100,"retry stable commit");
  ok(db.get("life").length===1,"retry no duplicate");
  ok(db.append("life","NO_STREAM","evt-B",{}).status==="CONFLICT","new id no stream conflict");
  let b=db.append("life",0,"evt-B",{value:2});
  ok(b.status==="APPENDED","revision0 succeeds");ok(b.event.revision===1,"revision1");
  ok(db.append("life",0,"evt-B",{value:2}).status==="RETRY","idempotent revision0 retry");
  ok(db.append("life",0,"evt-C",{}).status==="CONFLICT","stale expected revision");
  let c=db.append("life",1,"evt-C",{value:3});
  ok(c.status==="APPENDED","fresh expected revision");
  ok(c.event.commit===102,"third commit");
  let repeated=db.append("life",2,"evt-C",{value:3});
  ok(repeated.status==="APPENDED","same id with new expected position allowed in synthetic");
  ok(db.get("life").filter(e=>e.id==="evt-C").length===2,"event id alone not unique");
  let other=db.append("other","NO_STREAM","evt-C",{value:8});
  ok(other.status==="APPENDED","same id other stream");
  ok(db.get("other").length===1,"other stream persisted");
  let any=db.append("life","ANY","evt-X",{value:4});
  ok(any.status==="APPENDED","ANY accepts without version check");
  ok(any.event.revision===4,"ANY appends next revision");
  ok(db.append("missing","EXISTS","evt-Y",{}).status==="CONFLICT","EXISTS requires stream");
  ok(db.append("life","EXISTS","evt-Y",{}).status==="APPENDED","EXISTS accepts stream");
  // A commit position is a watermark. A projection may lag even after commit.
  const committed=any.event.commit;let projectionPosition=committed-2;
  ok(projectionPosition<committed,"projection can lag");
  ok(!(projectionPosition>=committed),"cannot claim read model current");
  projectionPosition=committed;
  ok(projectionPosition>=committed,"caught-up projection may serve snapshot");
  // Acknowledge after side effect. If crash before ack, delivery may repeat.
  let deliveries=0,sideEffects=0,acked=false,seen=new Set();
  function consume(e,crashBeforeAck){
    deliveries++;const key=e.stream+"|"+e.id;
    if(!seen.has(key)){sideEffects++;seen.add(key);}
    if(!crashBeforeAck)acked=true;
  }
  consume(a.event,true);
  ok(sideEffects===1&&!acked,"side effect before ack crash");
  consume(a.event,false);
  ok(deliveries===2,"at least once delivery modeled");
  ok(sideEffects===1,"consumer dedupe suppresses duplicate effect");
  ok(acked,"ack after success");
  const bad={acked:false,effect:false};bad.acked=true;
  ok(bad.acked&&!bad.effect,"ack before effect risks missing effect");
  const expectedPair={stream:"life",revision:db.get("life").at(-1).revision};
  ok(expectedPair.revision===5,"revision current");
  ok(db.append("life",expectedPair.revision,"evt-Z",{}).status==="APPENDED","fresh version append");
  ok(db.append("life",expectedPair.revision,"evt-Q",{}).status==="CONFLICT","concurrent writer rejected");
  return {assertions:checks,failures:0,synthetic_only:true,events_in_life:db.get("life").length,duplicate_id_within_stream:2,projection_lag_example:2};
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
