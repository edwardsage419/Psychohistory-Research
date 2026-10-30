#!/usr/bin/env node
'use strict';
const fs=require('fs');
const {audit}=require('./b_r292_s88_independent_grouped_conditional_oracle_20261030.js');
const tests=function tests(audit,csv,json,old){
 let variants={
 duplicate:()=>{let a=csv.split("\n");a[2]=a[1];return [a.join("\n"),json,old]},
 missing:()=>{let a=csv.split("\n");a.splice(2,1);return [a.join("\n"),json,old]},
 source_mass:()=>{let a=csv.split("\n"),x=a[2].split(",");x[11]="1/2";a[2]=x.join(",");return [a.join("\n"),json,old]},
 behavior:()=>{let a=csv.split("\n"),x=a[2].split(",");x[10]=x[10]==="0"?"1":"0";a[2]=x.join(",");return [a.join("\n"),json,old]},
 forecast:()=>{let a=csv.split("\n"),x=a[2].split(",");x[16]="1/2";a[2]=x.join(",");return [a.join("\n"),json,old]},
 epsilon:()=>{let a=csv.split("\n"),x=a[2].split(",");x[3]="1/2";a[2]=x.join(",");return [a.join("\n"),json,old]},
 summary:()=>{let o=JSON.parse(json);o.worlds[0].TRA_minus_FULL_ANZ="1/2";return [csv,JSON.stringify(o),old]},
 evidence_upgrade:()=>{let o=JSON.parse(json);o.scope="E2_HUMAN";return [csv,JSON.stringify(o),old]}
 };
 let base=audit(csv,json,old);let out={};
 for(let [name,fn] of Object.entries(variants)){try{audit(...fn());throw Error("FAIL_OPEN "+name)}catch(e){if(String(e.message).startsWith("FAIL_OPEN"))throw e;out[name]=e.message}}
 return {status:"PASS",positive:base,mutations:out,mutations_rejected:Object.keys(out).length};
};
if(require.main===module){if(process.argv.length!==5)throw Error('usage: node test.js sources.csv results.json original_R292.json');console.log(JSON.stringify(tests(audit,...process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'))),null,2));}
module.exports={tests};
