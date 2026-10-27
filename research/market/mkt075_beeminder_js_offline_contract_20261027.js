'use strict';
// Run: node research/market/mkt075_beeminder_js_offline_contract_20261027.js
// Exact MIT-licensed source fixture and LICENSE are stored in research/market/fixtures.
const fs=require('fs'),vm=require('vm'),crypto=require('crypto'),assert=require('assert'),path=require('path');
const sourceFile=process.argv[2]||path.join(__dirname,'fixtures','mkt075_beeminder_js_pinned_20261027.js');
const bytes=fs.readFileSync(sourceFile);
const sha=crypto.createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
assert.strictEqual(sha,'2a0f29c5ac34e76a90131b7bc860c54c70c9cdb8');
let checks=1,calls=[],mockData=[],failure=null;
const http={};
for(const verb of ['get','post','put','delete'])http[verb]=async(...args)=>{
 calls.push({verb,args});if(failure){const e=failure;failure=null;throw e;}
 if(verb==='post')return {data:{id:'created-id'}};
 return {data:verb==='get'?mockData:{id:'old-id',value:25}};
};
const qs={stringify:o=>new URLSearchParams(Object.entries(o).map(([k,v])=>[k,String(v)])).toString()};
const mod={exports:{}};
vm.runInNewContext(bytes.toString('utf8'),{module:mod,exports:mod.exports,require:n=>n==='axios'?http:n==='qs'?qs:(()=>{throw Error(n)})(),Error,URLSearchParams},{filename:sourceFile});
const Goal=mod.exports.Goal;
function eq(a,b){assert.strictEqual(a,b);checks++}
function ok(a){assert.ok(a);checks++}
function last(){return calls[calls.length-1]}
(async()=>{
 const token='FAKE_TOKEN_NOT_A_SECRET',g=new Goal('fictional-user',token,'fictional-goal');
 mockData=Array.from({length:51},(_,i)=>({id:String(i+1),value:i+1}));
 const got=await g.datapoints();
 eq(got.length,51);eq(last().verb,'get');
 const getUrl=last().args[0],u=new URL(getUrl);
 eq(u.protocol,'https:');eq(u.hostname,'www.beeminder.com');eq(u.searchParams.get('auth_token'),token);
 ok(getUrl.includes(token));ok(!u.searchParams.has('page'));ok(!u.searchParams.has('per'));ok(!u.searchParams.has('count'));ok(!u.searchParams.has('sort'));
 eq(got[0].id,'1');eq(got[50].id,'51');
 ok(('GET '+getUrl+' 200').includes(token));
 await g.deleteDatapoint('point-7');eq(last().verb,'delete');
 const du=last().args[0];eq(new URL(du).searchParams.get('auth_token'),token);
 ok(du.includes('/datapoints/point-7.json'));ok(du.includes(token));
 const id=await g.createDatapoint({value:25,daystamp:'20261027',requestid:'local-001'});
 eq(id,'created-id');eq(last().verb,'post');ok(!last().args[0].includes(token));
 const pb=new URLSearchParams(last().args[1]);eq(pb.get('auth_token'),token);eq(pb.get('value'),'25');
 eq(pb.get('daystamp'),'20261027');eq(pb.get('requestid'),'local-001');
 eq(last().args[2].headers['Content-Type'],'application/x-www-form-urlencoded');
 await g.updateDatapoint({id:'point-7',value:25});
 eq(last().verb,'put');ok(!last().args[0].includes(token));
 const ub=new URLSearchParams(last().args[1]);eq(ub.get('auth_token'),token);eq(ub.get('value'),'25');eq(ub.get('id'),'point-7');
 failure={response:{status:401,data:{errors:'denied'}},config:{url:getUrl},message:'denied'};
 let caught=null;try{await g.datapoints()}catch(e){caught=e}
 ok(caught!==null);eq(caught.name,'AuthError');ok(!caught.message.includes(token));ok(caught.cause.config.url.includes(token));
 failure=new Error('offline failure');let other=null;
 try{await g.datapoints()}catch(e){other=e}
 ok(other!==null);ok(other.message.includes('Failed to fetch datapoints'));
 ok(!other.message.includes(token));ok(other.cause.message==='offline failure');
 eq(typeof g.createMultipleDatapoints,'undefined');eq(g.datapoints.length,0);
 eq(typeof g.deleteDatapoint,'function');eq(typeof g.createDatapoint,'function');
 assert.strictEqual(checks,43);
 console.log(JSON.stringify({checks,failures:0,source_blob_sha:sha,real_server_called:false},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
