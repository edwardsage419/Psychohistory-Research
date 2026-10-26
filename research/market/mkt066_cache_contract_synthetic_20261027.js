'use strict';
const assert = require('node:assert/strict');
let checks=0; const check=(a,b)=>{assert.deepEqual(a,b);checks++};
class Repo {
  constructor({fastforward=true,fastforwardSkipping=false,deepcopy=true}={}) {
    this.events=[{version:1,delta:5},{version:2,delta:7}];
    this.cache=null;this.lockBusy=false;this.fastforward=fastforward;
    this.fastforwardSkipping=fastforwardSkipping;this.deepcopy=deepcopy;
  }
  append(delta){this.events.push({version:this.events.length+1,delta})}
  reconstruct(version){
    const events=this.events.filter(e=>version===undefined||e.version<=version);
    if(!events.length)throw Error('no events');
    return {version:events.at(-1).version,value:events.reduce((s,e)=>s+e.delta,0)}
  }
  get({version,fastforwardSkipping=false,deepcopy=true}={}){
    if(version!==undefined)return this.reconstruct(version);
    if(!this.cache)this.cache=this.reconstruct();
    else if(this.fastforward&&(!this.lockBusy||!(fastforwardSkipping||this.fastforwardSkipping))){
      for(const e of this.events.filter(e=>e.version>this.cache.version)){
        this.cache.value+=e.delta;this.cache.version=e.version;
      }
    }
    return deepcopy&&this.deepcopy?structuredClone(this.cache):this.cache;
  }
}
const d=new Repo();
check(d.get(),{version:2,value:12});check(d.cache.version,2);
d.append(3);check(d.cache.version,2);check(d.get(),{version:3,value:15});
check(d.get({version:1}),{version:1,value:5});
check(d.get({version:2}),{version:2,value:12});check(d.cache.version,3);
const stale=new Repo({fastforward:false});
check(stale.get(),{version:2,value:12});stale.append(3);
check(stale.get(),{version:2,value:12});check(stale.get({version:3}),{version:3,value:15});
const skip=new Repo({fastforwardSkipping:true});
check(skip.get(),{version:2,value:12});skip.append(3);skip.lockBusy=true;
check(skip.get(),{version:2,value:12});check(skip.get({version:3}),{version:3,value:15});
skip.lockBusy=false;check(skip.get(),{version:3,value:15});
const per=new Repo();check(per.get(),{version:2,value:12});
per.append(3);per.lockBusy=true;
check(per.get({fastforwardSkipping:true}),{version:2,value:12});
check(per.get({version:3}),{version:3,value:15});
const copy=new Repo();const external=copy.get();external.value=999;
check(copy.cache.value,12);const shared=copy.get({deepcopy:false});shared.value=999;
check(copy.cache.value,999);check(copy.get({version:2}).value,12);
const noCopy=new Repo({deepcopy:false});noCopy.get().value=101;
check(noCopy.cache.value,101);
check(new Repo().get({version:1}),{version:1,value:5});
check(new Repo().get({version:2}),{version:2,value:12});
assert.equal(checks,23);
console.log(JSON.stringify({checks,failures:0,evidence:'synthetic only'}));
