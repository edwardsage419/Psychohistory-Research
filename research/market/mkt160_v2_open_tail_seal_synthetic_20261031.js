/* MKT160: synthetic ActivityWatch v2 writer abstraction. Run: node <this file>. No Rust/device test. */
function run(){let checks=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m)};const copy=x=>JSON.parse(JSON.stringify(x));
const s={generation:0,segments:[]};
function write(events){if(!events.length)return s.generation;let tail=s.segments.at(-1);
if(!tail||tail.sealed){tail={generation:++s.generation,sealed:false,replaces:null,events:[]};s.segments.push(tail)}
const byId=new Map(tail.events.map(e=>[e.id,e]));for(const e of events)byId.set(e.id,copy(e));
tail.events=[...byId.values()].sort((a,b)=>a.t-b.t);return s.generation;}
ok(write([{id:1,t:1,data:"old"}])===1,"first");const old=JSON.stringify(s.segments[0]);
ok(write([{id:1,t:1,data:"edited"}])===1,"tail gen");
ok(JSON.stringify(s.segments[0])!==old,"tail content changed");
ok(s.segments[0].events[0].data==="edited","edit reflected");s.segments[0].sealed=true;
ok(write([{id:2,t:2,data:"new"}])===2,"new gen");
ok(s.segments[0].events[0].data==="edited","sealed preserved");
const snap=JSON.stringify(s);ok(write([])===2,"empty");
ok(JSON.stringify(s)===snap,"no delete on empty");
ok(s.segments.every(x=>x.replaces===null),"replace null");
ok(s.segments.flatMap(x=>x.events).some(e=>e.id===1),"old event remains");
ok(copy(s).segments[0].events[0].id===1,"restore resurrection");
ok(s.segments[0].sealed,"sealed");ok(s.segments.length===2,"two generations");
return {assertions:checks,generations:s.generation,events:2,scope:"synthetic only"};}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
