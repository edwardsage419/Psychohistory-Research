// MKT142 artificial finite-universe and Health Connect-inspired delta contract.
// Standard JavaScript. No network or personal data.
"use strict";
const gcd=(a,b)=>{while(b)[a,b]=[b,a%b];return a};
const f=(n,d)=>{n=BigInt(n);d=BigInt(d);const g=gcd(n,d);return n/g+"/"+d/g};
function bounds(s,t,cap=null){
 if(!Number.isSafeInteger(s)||!Number.isSafeInteger(t)||s<0||t<0)throw Error("bad counts");
 if(cap===null)return {seen:s+t,lower:"0/1",upper:"1/1",closed:false};
 if(!Number.isSafeInteger(cap)||cap<s+t||cap===0)throw Error("bad cap");
 return {seen:s+t,lower:f(s,cap),upper:f(cap-t,cap),closed:true};
}
function sync(rows,pages,valid=true,permission=true){
 if(!Array.isArray(rows)||!Array.isArray(pages))throw Error("bad input");
 if(!permission)return {status:"PERMISSION_REVOKED",checkpoint:null};
 if(!valid)return {status:"TOKEN_EXPIRED_RECONCILE",checkpoint:null};
 const m=new Map(rows.map(x=>[x.id,{...x}]));let checkpoint=null,complete=false;
 for(let i=0;i<pages.length;i++){
  const p=pages[i];
  if(!p||!Array.isArray(p.changes)||typeof p.next!=="string"||typeof p.more!=="boolean")throw Error("bad page");
  for(const c of p.changes){
   if(!c||typeof c.id!=="string"||!["upsert","delete"].includes(c.kind))throw Error("bad change");
   if(c.kind==="delete"){if(!m.has(c.id))return {status:"UNKNOWN_DELETE_ID",checkpoint:null};m.delete(c.id);}
   else {if(!Number.isSafeInteger(c.version)||c.version<0)throw Error("bad version");
    if(!m.has(c.id)||c.version>m.get(c.id).version)m.set(c.id,{id:c.id,version:c.version,value:c.value});}
  }
  checkpoint=p.next;
  if(!p.more){if(i!==pages.length-1)throw Error("trailing page");complete=true;}
 }
 if(!complete)return {status:"INCOMPLETE_PAGINATION",checkpoint:null};
 return {status:"APPLIED_ARTIFICIAL_ONLY",checkpoint,rows:[...m.values()].sort((a,b)=>a.id.localeCompare(b.id))};
}
function run(){
 let checks=0,rejections=0;const ok=(x)=>{if(!x)throw Error("assert "+checks);checks++};
 const a=bounds(4,2),b=bounds(4,2,6),c=bounds(4,2,12),d=bounds(4,2,20);
 ok(a.lower==="0/1"&&a.upper==="1/1"&&!a.closed);
 ok(b.lower==="2/3"&&b.upper==="2/3");
 ok(c.lower==="1/3"&&c.upper==="5/6");
 ok(d.lower==="1/5"&&d.upper==="9/10");
 ok(4/12<.5&&10/12>.5);
 const initial=[{id:"a",version:1,value:0},{id:"b",version:1,value:1}];
 const pages=[{changes:[{kind:"upsert",id:"a",version:2,value:1}],next:"t1",more:true},{changes:[{kind:"delete",id:"b"}],next:"t2",more:false}];
 const good=sync(initial,pages);
 ok(good.status==="APPLIED_ARTIFICIAL_ONLY"&&good.checkpoint==="t2");
 ok(good.rows.length===1&&good.rows[0].value===1);
 ok(sync(initial,pages.slice(0,1)).status==="INCOMPLETE_PAGINATION");
 ok(sync(initial,pages,false).status==="TOKEN_EXPIRED_RECONCILE");
 ok(sync(initial,pages,true,false).status==="PERMISSION_REVOKED");
 ok(sync(initial,[{changes:[{kind:"delete",id:"unknown"}],next:"t3",more:false}]).status==="UNKNOWN_DELETE_ID");
 ok(sync(initial,[{changes:[{kind:"upsert",id:"a",version:0,value:9}],next:"t3",more:false}]).rows[0].value===0);
 const bad=[()=>bounds(-1,2),()=>bounds(1,2,2),()=>bounds(0,0,0),()=>sync(initial,[{}]),()=>sync(initial,[{changes:[{kind:"upsert",id:"a",version:-1}],next:"t",more:false}]),()=>sync(initial,[{changes:[],next:"a",more:false},{changes:[],next:"b",more:false}])];
 for(const fn of bad){let rejected=false;try{fn()}catch(e){rejected=true}if(!rejected)throw Error("negative");rejections++;}
 return {checks,rejections,unbounded:a,cap12:c,cap20:d,delta:good.status};
}
if(typeof module!=="undefined")module.exports={bounds,sync,run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
