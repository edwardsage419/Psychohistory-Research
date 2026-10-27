// MKT070. Node.js 18+, standard library only. Synthetic Eventide control-flow model.
function runSynthetic(){
  let checks=0;const ok=(x,m)=>{checks++;if(!x)throw Error("assert "+checks+" "+m);};
  function make({interval=1,suppress=false,failAt=2}={}){
    const s={memory:1,durable:0,counter:0,effects:[],failures:[],positionWrites:[]};
    const dispatch=p=>{try{for(let i=1;i<=2;i++){if(i===2&&p===failAt)throw Error("handler2 failure");s.effects.push(`${p}:${i}`);}s.counter++;if(s.counter>=interval){s.durable=p;s.positionWrites.push(p);s.counter=0;}}catch(e){s.failures.push(p);if(!suppress)throw e;}};
    return{s,next:p=>{dispatch(p);s.memory=p+1;}};
  }
  const a=make({interval:1,suppress:true});a.next(1);a.next(2);a.next(3);
  ok(a.s.durable===3,"swallowed failure then durable advance");ok(a.s.memory===4,"memory advance");ok(a.s.failures.join(",")==="2","failure recorded");ok(a.s.effects.includes("2:1"),"earlier effect");ok(!a.s.effects.includes("2:2"),"failed handler");ok(a.s.positionWrites.join(",")==="1,3","checkpoint gap");ok(a.s.durable+1===4,"restart gap");ok(a.s.effects.includes("3:2"),"later completed");
  const b=make({interval:1,suppress:false});b.next(1);let thrown=false;try{b.next(2);}catch(e){thrown=true;}
  ok(thrown,"error rethrown");ok(b.s.memory===2,"no memory skip");ok(b.s.durable===1,"checkpoint stays");ok(b.s.effects.includes("2:1"),"partial side effect");ok(!b.s.effects.includes("2:2"),"failure");
  const c=make({interval:3,suppress:true});c.next(1);c.next(2);c.next(3);
  ok(c.s.durable===0,"interval3 no checkpoint");ok(c.s.counter===2,"success counter");c.next(4);ok(c.s.durable===4,"later checkpoint skips failed");ok(c.s.positionWrites.join(",")==="4","interval3 write");ok(c.s.memory===5,"memory moves");
  const d=make({interval:3,suppress:false});d.next(1);let stopped=false;try{d.next(2);}catch(e){stopped=true;}
  ok(stopped,"stopped");ok(d.s.durable===0,"durable unchanged");ok(d.s.memory===2,"memory unchanged");
  const e=make({interval:1,suppress:true,failAt:100});e.next(1);e.next(2);
  ok(e.s.failures.length===0,"normal no failures");ok(e.s.durable===2,"normal checkpoint");ok(e.s.effects.length===4,"normal effects");
  const f=make({interval:1,suppress:true,failAt:1});f.next(1);
  ok(f.s.memory===2,"first failure memory");ok(f.s.durable===0,"first failure durable");f.next(2);ok(f.s.durable===2,"first failure checkpoint skipped");ok(f.s.failures.join(",")==="1","first failure recorded");
  return {assertions:checks,failures:0,scenarios:6,scope:"standalone synthetic model"};
}
const result=runSynthetic();console.log(JSON.stringify(result));
