#!/usr/bin/env node
"use strict";
const WORLDS=[{name:"dread_weighted",a:3,b:1},{name:"unknown_weighted",a:1,b:3},{name:"balanced",a:1,b:1},{name:"scaled_balanced",a:2,b:2}];
const POLICIES=["state_only","exact_score","threshold_ge_4","compare_dread","compare_unknown","compare_both"];
const STATES=Array.from({length:16},(_,i)=>[i>>3&1,i>>2&1,i>>1&1,i&1]);
const score=(s,w)=>w.a*(s[0]+s[1])+w.b*(s[2]+s[3]);
const sign=x=>x>0?1:x<0?-1:0;
const gcd=(a,b)=>b?gcd(b,a%b):a;
const frac=(a,b)=>{let d=gcd(a,b);return b/d===1?String(a/d):a/d+"/"+b/d;};
function atom(i,s){const w=WORLDS[i],v=score(s,w);return {world_id:i,state:s.join(""),D:s[0]+s[1],U:s[2]+s[3],score:v,threshold_ge_4:Number(v>=4),compare_dread:sign(v-score([1,1,0,0],w)),compare_unknown:sign(v-score([0,0,1,1],w))};}
function observation(p,r){switch(p){case "state_only":return [];case "exact_score":return [r.score];case "threshold_ge_4":return [r.threshold_ge_4];case "compare_dread":return [r.compare_dread];case "compare_unknown":return [r.compare_unknown];case "compare_both":return [r.compare_dread,r.compare_unknown];default:throw Error("unknown policy");}}
function rankProfile(w){const v=STATES.map(s=>score(s,w));return v.flatMap(x=>v.map(y=>sign(x-y))).join(",");}
function generate(){
 const rows=WORLDS.flatMap((_,i)=>STATES.map(s=>atom(i,s)));
 if(rows.length!==64||new Set(rows.map(r=>r.world_id+":"+r.state)).size!==64)throw Error("bad atom universe");
 const policies=POLICIES.map(p=>{const groups=new Map();for(const r of rows){const k=JSON.stringify([r.state,observation(p,r)]);if(!groups.has(k))groups.set(k,[0,0,0,0]);groups.get(k)[r.world_id]++;}const n=[...groups.values()].reduce((s,c)=>s+Math.max(...c),0);return {policy:p,observation_groups:groups.size,accuracy:frac(n,64),accuracy_numerator:n,accuracy_denominator:64};});
 const profiles=WORLDS.map(rankProfile),distinct=new Set(profiles).size;
 const result={schema:"r324_s120_ordinal_observation_e1_v1",evidence:"E1_SYNTHETIC_ONLY",source_original_blob:"1b0062eeea020606a3d510d566da43db03ace8d9",frozen_protocol_commit:"dc2bc2ad22a0130984cf0ecb497c2c54f04803f8",original_catalogue_id:"01-017",world_count:4,state_count:16,atom_count:64,atom_mass:"1/64",policies,full_ordinal_profile:{distinct_profiles:distinct,accuracy:frac(distinct,4),profile_groups:[0,1,2,2]},witnesses:{w2_w3_identical_weak_rank:profiles[2]===profiles[3],w2_w3_exact_score_differ_count:STATES.filter(s=>score(s,WORLDS[2])!==score(s,WORLDS[3])).length},human_E2:"NOT_ESTABLISHED",historical_E3:"NOT_ESTABLISHED",external_independent_replication:"NOT_RUN"};
 return {rows,result};
}
const FIELDS=["world_id","state","D","U","score","threshold_ge_4","compare_dread","compare_unknown"];
const csvText=rows=>FIELDS.join(",")+"\n"+rows.map(r=>FIELDS.map(k=>r[k]).join(",")).join("\n")+"\n";
const jsonText=obj=>JSON.stringify(obj,null,2)+"\n";
function originalCsvExpected(){const h="world_id,policy,dread1,dread2,unknown1,unknown2,weight,D,U,score\n";const a=WORLDS.flatMap((w,i)=>STATES.map(s=>[i,w.name,...s,"1/16",s[0]+s[1],s[2]+s[3],score(s,w)].join(",")));return h+a.join("\n")+"\n";}
function verify(original,csv,json){if(original!==originalCsvExpected())throw Error("original R324 CSV mismatch");const g=generate();if(csv!==csvText(g.rows))throw Error("S120 CSV mismatch");if(json!==jsonText(g.result))throw Error("S120 JSON mismatch");return true;}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),args=process.argv.slice(2),mode=args[0],dest=args[1],root=path.resolve(__dirname,"../..");
 const orig=fs.readFileSync(path.join(root,"research/R324/R324_ALL_64_ARTIFICIAL_RISK_STATES.csv"),"utf8");
 if(orig!==originalCsvExpected())throw Error("original R324 source identity mismatch");
 const g=generate();
 if(mode==="--emit"&&dest){fs.mkdirSync(dest,{recursive:true});fs.writeFileSync(path.join(dest,"R324_S120_64_ATOM_ORDINAL_OBSERVATIONS.csv"),csvText(g.rows));fs.writeFileSync(path.join(dest,"R324_S120_EXACT_OBSERVATION_RESULTS.json"),jsonText(g.result));console.log("R324_S120_EMIT_PASS",g.rows.length,g.result.policies.length);}
 else if(mode==="--check"&&dest){verify(orig,fs.readFileSync(path.join(dest,"R324_S120_64_ATOM_ORDINAL_OBSERVATIONS.csv"),"utf8"),fs.readFileSync(path.join(dest,"R324_S120_EXACT_OBSERVATION_RESULTS.json"),"utf8"));console.log("R324_S120_CHECK_PASS");}
 else if(mode==="--selftest"){verify(orig,csvText(g.rows),jsonText(g.result));let failures=0;for(const [c,j] of [[csvText(g.rows).replace(",0,0,0,0\n",",0,0,0,1\n"),jsonText(g.result)],[csvText(g.rows),jsonText(g.result).replace('"atom_count": 64','"atom_count": 65')]]){try{verify(orig,c,j);}catch(e){failures++;}}if(failures!==2)throw Error("mutation accepted");console.log("R324_S120_SELFTEST_PASS",g.rows.length,failures);}
 else throw Error("usage: --emit DIR | --check DIR | --selftest");
}