"use strict";
const outcome=[0,1,0,1,1,0,0,1,1,0,1,0];
const tags={
  exercise:[1,1,0,1,0,0,1,0,1,0,1,0],
  reading:[0,0,1,1,1,0,0,1,1,0,1,0],
  late_work:[1,0,0,1,0,1,0,1,1,0,0,1],
  rest:[0,1,1,0,0,1,1,0,0,1,0,1]
};
const windows={all:[0,12],early:[0,6],late:[6,12]};
function phi(a,b){
  if(!Array.isArray(a)||!Array.isArray(b)||a.length!==b.length||a.length<2)throw Error("invalid length");
  for(const v of [...a,...b])if(v!==0&&v!==1)throw Error("nonbinary");
  let n11=0,n10=0,n01=0,n00=0;
  for(let i=0;i<a.length;i++){
    if(a[i]===1&&b[i]===1)n11++;
    else if(a[i]===1)n10++;
    else if(b[i]===1)n01++;
    else n00++;
  }
  const den=Math.sqrt((n11+n10)*(n01+n00)*(n11+n01)*(n10+n00));
  return den===0?null:(n11*n00-n10*n01)/den;
}
function stats(y){
  const out=[];
  for(const [tag,values] of Object.entries(tags))
    for(const [window,[s,e]] of Object.entries(windows))
      out.push({tag,window,r:phi(values.slice(s,e),y.slice(s,e))});
  return out;
}
function study(){
  let tests=0;
  function ok(c,msg){tests++;if(!c)throw Error("assert "+msg);}
  const obs=stats(outcome);
  const finite=obs.filter(x=>x.r!==null);
  const selected=finite.reduce((a,b)=>Math.abs(b.r)>Math.abs(a.r)?b:a);
  ok(obs.length===12,"12 prespecified views");
  ok(selected.tag==="reading"&&selected.window==="late"&&selected.r===1,"selected report");
  const fixed=phi(tags.reading,outcome);
  ok(Math.abs(fixed-2/3)<1e-12,"full window");
  const alternateReading=[1,1,0,0,0,1,...tags.reading.slice(6)];
  ok(phi(alternateReading.slice(6),outcome.slice(6))===1,"same published window");
  ok(Math.abs(phi(alternateReading,outcome)-1/3)<1e-12,"different unreported history");
  let family=0,single=0,constant=0;
  for(let mask=0;mask<4096;mask++){
    const y=Array.from({length:12},(_,i)=>(mask>>i)&1);
    const results=stats(y);
    if(results.some(x=>x.r!==null&&Math.abs(x.r)>1-1e-12))family++;
    const r=phi(tags.reading.slice(6),y.slice(6));
    if(r!==null&&Math.abs(r)>1-1e-12)single++;
    if(results.some(x=>x.r===null))constant++;
  }
  ok(family===848,"exact family count");
  ok(single===128,"exact single count");
  ok(family>single,"selection inflation");
  ok(family/4096===0.20703125,"family probability");
  ok(single/4096===0.03125,"single probability");
  ok(phi([0,0,0],[1,0,1])===null,"constant predictor");
  ok(phi([0,1,0],[1,1,1])===null,"constant outcome");
  for(const f of [()=>phi([0],[1]),()=>phi([0,1],[1]),()=>phi([0,2],[1,0]),()=>phi(null,[0,1]),()=>phi([1,0],["1",0])]){
    let failed=false;try{f();}catch(_){failed=true;}ok(failed,"reject malformed input");
  }
  ok(outcome.length===12,"complete outcome");
  ok(Object.keys(tags).length===4,"four tag definitions");
  ok(Object.keys(windows).length===3,"three windows");
  return {status:"PASS",tests,observed_selected:selected,full_reading_correlation:fixed,alternate_full_reading_correlation:phi(alternateReading,outcome),null_worlds:4096,family_perfect_worlds:family,single_perfect_worlds:single,family_probability:family/4096,single_probability:single/4096,constant_worlds:constant};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(study(),null,2));
