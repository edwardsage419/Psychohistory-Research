#!/usr/bin/env node
"use strict";
const assert=(p,m)=>{if(!p)throw Error(m||"assertion")};
const gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a);
const F=(n,d=1)=>{assert(Number.isInteger(n)&&Number.isInteger(d)&&d!==0);if(d<0){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]};
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
const gt=(a,b)=>a[0]*b[1]>b[0]*a[1];
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const fmt=a=>a[1]===1?String(a[0]):a[0]+"/"+a[1];
const levels=[0,1,2],cats={P:[0,0,1,1],Q:[0,1,0,1]};
function fit(k,cat){
  assert(k>=0&&k<=4&&Number.isInteger(k));const x=[0,4+3*k,16-3*k,20],lab=cats[cat];assert(lab,"category");
  let within=0,across=0,w=0,b=0;
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
    const d=Math.abs(x[i]-x[j]);
    if(lab[i]===lab[j]){within+=d;w++}else{across+=d;b++}
  }
  assert(w===2&&b===4&&within>0,"pair universe");
  return F(across,2*within);
}
function decision(k,r,np,nq,t){
  const p=mul(F(r*np,4),fit(k,"P")),q=mul(F(r*nq,4),fit(k,"Q")),base=F(t);
  return {p,q,choice:gt(p,q)&&gt(p,base)?"P":gt(q,p)&&gt(q,base)?"Q":"PERSONAL"};
}
function generate(){
  const header=["lambda","features","readiness","norm_P","norm_Q","personal_threshold","MC_P","MC_Q","score_P","score_Q","choice"];
  const rows=[],counts={},hist={0:0,1:0,2:0,3:0,4:0},paths=[];
  let changes=0;
  for(let k=0;k<5;k++)counts[fmt(F(k,4))]={P:0,Q:0,PERSONAL:0};
  for(const r of levels)for(const np of levels)for(const nq of levels)for(const t of levels){
    const path=[];
    for(let k=0;k<5;k++){
      const a=decision(k,r,np,nq,t),lam=fmt(F(k,4)),features=[0,4+3*k,16-3*k,20].map(v=>fmt(F(v,4))).join(";");
      rows.push([lam,features,fmt(F(r,2)),fmt(F(np,2)),fmt(F(nq,2)),String(t),fmt(fit(k,"P")),fmt(fit(k,"Q")),fmt(a.p),fmt(a.q),a.choice]);
      counts[lam][a.choice]++;path.push(a.choice);
      if(r===0||(np===0&&nq===0))assert(a.choice==="PERSONAL","negative control");
    }
    const n=path.slice(1).reduce((acc,v,i)=>acc+(v!==path[i]),0);hist[n]++;changes+=n;
    paths.push({readiness:fmt(F(r,2)),norm_P:fmt(F(np,2)),norm_Q:fmt(F(nq,2)),personal_threshold:t,path,adjacent_changes:n});
  }
  assert(rows.length===405&&paths.length===81&&Object.values(hist).reduce((a,b)=>a+b,0)===81);
  assert(eq(fit(0,"P"),F(4))&&eq(fit(0,"Q"),F(5,8))&&eq(fit(2,"P"),F(1))&&eq(fit(2,"Q"),F(1))&&eq(fit(4,"P"),F(5,8))&&eq(fit(4,"Q"),F(4)));
  const csv=header.join(",")+"\n"+rows.map(row=>row.map(x=>'"'+String(x).replaceAll('"','""')+'"').join(",")).join("\n")+"\n";
  const summary={research_id:"R305",stage:"S101",grade:"E1_SYNTHETIC_ONLY",original_frozen_model_unchanged:true,worlds:405,candidate_source_cells:810,configurations:81,adjacent_comparisons:324,metacontrast:[0,1,2,3,4].map(k=>({lambda:fmt(F(k,4)),P:fmt(fit(k,"P")),Q:fmt(fit(k,"Q"))})),choice_counts:counts,trajectory_change_histogram:hist,total_adjacent_changes:changes,first_change_witness:paths.find(p=>p.adjacent_changes>0)||null,all_trajectories:paths,original_R305_endpoint_midpoint_parity:"CHECKED_EXTERNALLY",human_E2:0,historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",scientific_acceptance:"PARTIAL"};
  return {csv,summary,rows};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){
  const fs=require("node:fs"),path=require("node:path"),r=generate();
  if(process.argv.includes("--emit")){
    const dir=process.argv[process.argv.indexOf("--emit")+1]||".";
    fs.mkdirSync(dir,{recursive:true});
    fs.writeFileSync(path.join(dir,"R305_S101_ALL_405_CONTEXT_WORLDS.csv"),r.csv);
    fs.writeFileSync(path.join(dir,"R305_S101_EXACT_RESULTS.json"),JSON.stringify(r.summary,null,2)+"\n");
  }
  console.log(JSON.stringify({worlds:r.summary.worlds,changes:r.summary.total_adjacent_changes,hist:r.summary.trajectory_change_histogram,counts:r.summary.choice_counts}));
}
