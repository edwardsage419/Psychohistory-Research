"use strict";
let checks=0;function check(v,m){checks++;if(!v)throw Error(m);}
function clean(s){return s.trim().toLowerCase().replace(/[^a-z0-9_-]+/g,"_").replace(/^_+|_+$/g,"")||"unknown";}
function dest(p,bound){let base=p.bucket.split("-synced-from-")[0];return bound?p.device_id+"::"+base:base+"-synced-from-"+clean(p.hostname);}
function simulate(peers,bound){let buckets=new Map();for(const p of peers){let key=dest(p,bound),rows=buckets.get(key)||[],cursor=rows.length?Math.max(...rows.map(x=>x.t)):-Infinity;for(const e of p.events)if(e.t>cursor)rows.push({id:e.id,t:e.t,device_id:p.device_id});buckets.set(key,rows);}return {buckets,events:[...buckets.values()].flat().map(x=>x.id).sort()};}
function run(){
const a={device_id:"device_A",hostname:"Office Laptop",bucket:"aw-watcher-window",events:[{id:"A1",t:1},{id:"A3",t:3}]},b={device_id:"device_B",hostname:"office_laptop",bucket:"aw-watcher-window",events:[{id:"B2",t:2},{id:"B4",t:4}]};
check(a.device_id!==b.device_id,"two devices");check(clean(a.hostname)===clean(b.hostname),"same normalized host");check(dest(a,false)===dest(b,false),"legacy collision");check(dest(a,true)!==dest(b,true),"bound separation");
const ab=simulate([a,b],false),ba=simulate([b,a],false),x=simulate([a,b],true),y=simulate([b,a],true);
check(ab.buckets.size===1,"legacy AB buckets");check(ba.buckets.size===1,"legacy BA buckets");
check(ab.events.join(",")==="A1,A3,B4","AB skipped B2");check(ba.events.join(",")==="B2,B4","BA skipped A");
check(!ab.events.includes("B2"),"missing B2");check(!ba.events.includes("A1"),"missing A1");
check(x.buckets.size===2,"bound AB buckets");check(y.buckets.size===2,"bound BA buckets");
check(x.events.join(",")==="A1,A3,B2,B4","bound AB complete");check(y.events.join(",")==="A1,A3,B2,B4","bound BA complete");
check(x.buckets.get(dest(a,true)).every(e=>e.device_id==="device_A"),"A source");check(x.buckets.get(dest(b,true)).every(e=>e.device_id==="device_B"),"B source");
check(dest({...a,hostname:"unknown"},true)===dest(a,true),"device key rename stable");
check(dest({...a,hostname:"other"},false)!==dest(a,false),"legacy rename fork");
return {checks,legacy_AB:ab.events,legacy_BA:ba.events,device_bound_AB:x.events,device_bound_BA:y.events,evidence:"synthetic E1; Rust and devices NOT_RUN"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));