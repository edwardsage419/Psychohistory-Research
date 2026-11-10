#!/usr/bin/env node
// Read-only adapter: evaluate original bytes, append an export binding, never edit them.
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),crypto=require('node:crypto');
if(process.argv.length!==3)throw Error('usage: export_js_states.js original_script.js');
const raw=fs.readFileSync(process.argv[2]),context={};
vm.runInNewContext(raw.toString('utf8')+
 '\nglobalThis.__codex={graphs,starts,noises,modes,path,mainKernel};',context,{timeout:10000});
const api=context.__codex,records=[];
for(const [graph,edges] of api.graphs)for(const [initial,start] of api.starts)
for(const nu of api.noises)for(const mode of api.modes){
 const snapshots=api.path(edges,start,nu,mode,api.mainKernel);
 for(let t=0;t<4;t++)records.push({graph,initial,nu:String(nu),mode,t,
  law:Object.fromEntries([...snapshots[t]].sort((a,b)=>a[0].localeCompare(b[0])).map(([s,p])=>[s,String(p)]))});
}
console.log(JSON.stringify({route:'archived_JS_directed_delivered_mixture',
 source_sha256:crypto.createHash('sha256').update(raw).digest('hex'),records},null,2));
