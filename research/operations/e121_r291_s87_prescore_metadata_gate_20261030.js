#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const paths={
 checker:'evidence_audit/b_r291_s87_independent_conditional_variance_20261030.js',
 csv:'validation/R291_S87_ALL_768_PROXY_SOURCE_CELLS.csv',
 json:'validation/R291_S87_EXACT_RESULTS.json'
};
const expected={
 checker:'53148a6e4c15f7983ace3648bd896f5cfb401df4',
 csv:'d04ce3b99d37f4433e0251190324304de3df19c6',
 json:'ecd62fab3b63f5398abe2cda6e086c4819ce1a0a'
};
const contents={};
for(const [key,relative] of Object.entries(paths)){
 const bytes=fs.readFileSync(path.join(root,relative));
 const h=crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
 assert.equal(h,expected[key],'archived blob identity: '+key);
 contents[key]=bytes.toString('utf8');
}
const start=contents.checker.indexOf('const check=function check');
const end=contents.checker.indexOf('const root=',start);
assert.ok(start>=0&&end>start,'original checker function extraction');
const check=vm.runInNewContext(contents.checker.slice(start,end)+';check',Object.create(null),{timeout:10000});
const original=check(contents.csv,contents.json);
assert.equal(original.status,'PASS');assert.equal(original.source_rows,768);
const mutate=[
 ['parent_commit_replace',o=>{o.parent_R291_freeze='UNVERIFIED_FROZEN_PROTOCOL'}],
 ['parent_commit_delete',o=>{delete o.parent_R291_freeze}],
 ['prescore_commit_replace',o=>{o.S87_prescore_commit='NOT_FROZEN'}],
 ['prescore_commit_delete',o=>{delete o.S87_prescore_commit}],
 ['E2_type_change',o=>{o.new_human_E2='0'}],
 ['R073_status_change',o=>{o.R073='UNFROZEN'}]
];
const results=[];
for(const [name,edit] of mutate){
 const o=JSON.parse(contents.json);edit(o);
 let accepted=false;
 try{accepted=check(contents.csv,JSON.stringify(o)).status==='PASS'}catch(_e){}
 results.push({name,accepted});
}
assert.deepEqual(results.map(x=>x.accepted),[true,true,true,true,false,false]);
console.log(JSON.stringify({status:'PASS',original,results,original_blob_shas:expected,scope:'original persisted CSV/JSON and original B checker function; not original B CLI or blind replication'}));
