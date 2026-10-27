#!/usr/bin/env node
"use strict";
// MKT081 pinned pymoo PI-NSGA-II failed-fit fallback contract.
// Isolated source-branch simulation. No full optimizer or user data.
const EXPECTED_BLOB="207726ffba920eca75f739b2d0cccaf0c23d92b8";
function assert(x,m){if(!x)throw Error(m)}
function perms(a){return a.length===1?[a]:a.flatMap((v,i)=>perms(a.filter((_,j)=>j!==i)).map(t=>[v,...t]))}
function sourceFallback(r){const cut=r[1],ids=r.map((_,i)=>i);ids.splice(cut-1,1);return {ids,ranks:[r[0],...r.slice(2)].map(x=>x>cut?x-1:x),deletedIndex:cut-1}}
function correctedFallback(r){const cutIndex=r.indexOf(2),ids=r.map((_,i)=>i);ids.splice(cutIndex,1);return {ids,ranks:ids.map(i=>r[i]>2?r[i]-1:r[i]),deletedIndex:cutIndex}}
function run(source){
 let checks=0;const ck=(x,m)=>{checks++;assert(x,m)};
 if(source!==undefined){
  const lines=["rank_to_remove = dm_ranks[1]","eta_F = np.delete(eta_F, rank_to_remove - 1, axis=0)","dm_ranks = np.concatenate(([dm_ranks[0]], dm_ranks[2:]))","dm_ranks[dm_ranks > rank_to_remove] = dm_ranks[dm_ranks > rank_to_remove] - 1"];
  for(const s of lines)ck(source.includes(s),"pinned branch source missing: "+s);
 }
 const summary={};
 for(const n of [3,4,5]){let removedWrong=0,misaligned=0,rankStillPermutation=0;
  const arr=perms(Array.from({length:n},(_,i)=>i+1));
  for(const r of arr){
   const a=sourceFallback(r),b=correctedFallback(r);
   ck(a.ids.length===n-1&&a.ranks.length===n-1,"source length");
   ck(b.ids.length===n-1&&b.ranks.length===n-1,"corrected length");
   ck(b.ids.every((id,i)=>b.ranks[i]===(r[id]>2?r[id]-1:r[id])),"corrected identity");
   if(a.deletedIndex!==b.deletedIndex)removedWrong++;
   const retained=a.ids.map(id=>r[id]);
   const expected=retained.map(v=>retained.filter(x=>x<=v).length);
   if(a.ranks.some((v,i)=>v!==expected[i]))misaligned++;
   if(a.ranks.slice().sort((x,y)=>x-y).every((v,i)=>v===i+1))rankStillPermutation++;
  }
  summary[n]={permutations:arr.length,wrongSecondBestRemoval:removedWrong,retainedPreferenceOrderChanged:misaligned,sourceStillPassesPermutationValidation:rankStillPermutation};
 }
 ck(summary[3].wrongSecondBestRemoval===2&&summary[4].wrongSecondBestRemoval===12&&summary[5].wrongSecondBestRemoval===72,"removal counts");
 ck(summary[3].retainedPreferenceOrderChanged===2&&summary[4].retainedPreferenceOrderChanged===11&&summary[5].retainedPreferenceOrderChanged===75,"order counts");
 const example=[3,1,4,2],a=sourceFallback(example),b=correctedFallback(example);
 ck(a.deletedIndex===0&&a.ids.join("|")==="1|2|3"&&a.ranks.join("|")==="2|3|1","source example");
 ck(b.deletedIndex===3&&b.ids.join("|")==="0|1|2"&&b.ranks.join("|")==="2|1|3","corrected example");
 return {status:"PASS",checks,summary,example:{ranks:example,source:a,corrected:b},scope:"pinned failed-fit branch simulation; no full scipy fit or user effect"}
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto");let source;
 if(process.argv[2]){const b=fs.readFileSync(process.argv[2]);const sha=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");assert(sha===EXPECTED_BLOB,"pinned blob mismatch");source=b.toString("utf8")}
 console.log(JSON.stringify(run(source)));
}
