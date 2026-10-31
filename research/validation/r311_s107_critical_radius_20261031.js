#!/usr/bin/env node
"use strict";
// R311 S107 finite E1. Opinion units are exact quarters.
const OP=[0,2,4],EPS=[0,1,2,4],fmt={0:"0",1:"1/4",2:"1/2",4:"1"};
function check(ok,message){if(!ok)throw Error(message);}
function csv(rows,cols){return [cols.join(","),...rows.map(r=>cols.map(k=>String(r[k])).join(","))].join("\n")+"\n";}
function allVectors(){const a=[];for(const i of OP)for(const j of OP)for(const k of OP)for(const l of OP)a.push([i,j,k,l]);return a;}
function generate(){
 const profiles=[],grid=[];
 for(const x of allVectors()){
  const s=x.slice().sort((a,b)=>a-b),c=Math.max(s[1]-s[0],s[2]-s[1],s[3]-s[2]),q=s[3]-s[0],g=q-c;
  const v=x.map(z=>fmt[z]).join(";");
  check(c<=q&&g>=0&&EPS.includes(c)&&EPS.includes(q),"invalid critical radius");
  profiles.push({vector:v,critical_connected:fmt[c],critical_clique:fmt[q],critical_gap:fmt[g],grid_connected:fmt[EPS.find(e=>e>=c)],grid_clique:fmt[EPS.find(e=>e>=q)]});
  for(const e of EPS)grid.push({vector:v,epsilon:fmt[e],connected_formula:e>=c?"True":"False",clique_formula:e>=q?"True":"False"});
 }
 check(profiles.length===81&&grid.length===324,"incomplete universe");
 const freq=(k)=>{const o={};for(const r of profiles)o[r[k]]=(o[r[k]]||0)+1;return Object.fromEntries(Object.entries(o).sort());};
 const positive=profiles.filter(r=>r.critical_gap!=="0").length;
 const falsePositive=grid.filter(r=>r.connected_formula==="True"&&r.clique_formula==="False").length;
 const summary={research:"R311",stage:"S107",scope:"E1_FINITE_ARTIFICIAL",vectors:81,grid_worlds:324,
  original_source_rows_expected:1944,critical_connected_counts:freq("critical_connected"),
  critical_clique_counts:freq("critical_clique"),gap_counts:freq("critical_gap"),
  positive_gap_vectors:positive,connected_not_clique_worlds:falsePositive,
  naive_connected_as_clique_false_positives:falsePositive,
  naive_connected_as_clique_false_positive_rate:String(falsePositive)+"/324",naive_connected_as_clique_correct:324-falsePositive,
  source_identity_status:"TO_BE_AUDITED_SEPARATELY",new_real_E2:0,new_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 check(profiles.find(r=>r.vector==="0;1/2;1;1").critical_connected==="1/2","chain critical");
 check(profiles.find(r=>r.vector==="0;1/2;1;1").critical_clique==="1","chain clique");
 check(profiles.find(r=>r.vector==="0;0;0;0").critical_gap==="0","equal vector");
 return {profiles,grid,summary,
  profilesCsv:csv(profiles,["vector","critical_connected","critical_clique","critical_gap","grid_connected","grid_clique"]),
  gridCsv:csv(grid,["vector","epsilon","connected_formula","clique_formula"])};
}
if(typeof module!=="undefined")module.exports={generate,allVectors};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),d=generate();
 if(process.argv.includes("--test")){console.log(JSON.stringify(d.summary,null,2));process.exit(0);}
 const ix=process.argv.indexOf("--emit");
 if(ix<0||!process.argv[ix+1])throw Error("use --test or --emit OUTPUT_DIR");
 const out=process.argv[ix+1];fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,"R311_S107_ALL_81_CRITICAL_RADII.csv"),d.profilesCsv);
 fs.writeFileSync(path.join(out,"R311_S107_ALL_324_THRESHOLD_PREDICTIONS.csv"),d.gridCsv);
 fs.writeFileSync(path.join(out,"R311_S107_SUMMARY.json"),JSON.stringify(d.summary,null,2)+"\n");
 console.log(JSON.stringify({status:"PASS",vectors:81,grid_worlds:324,output:out}));
}