#!/usr/bin/env node
"use strict";
// Independent B oracle: reconstruct original 1944 dyads. Does not import R generator.
function gate(ok,why){if(!ok)throw Error(why);}
function parseCsv(t){
 const lines=t.trimEnd().split(/\r?\n/);
 function fields(line){const a=[];let v="",q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){v+='"';i++;}else q=!q;}else if(c===","&&!q){a.push(v);v="";}else v+=c;}gate(!q,"unterminated CSV quote");a.push(v);return a;}
 const h=fields(lines.shift());return lines.map((l,i)=>{const f=fields(l);gate(f.length===h.length,"CSV width at "+i);return Object.fromEntries(h.map((k,j)=>[k,f[j]]));});
}
const E=["0","1/4","1/2","1"], quarter={"0":0,"1/4":1,"1/2":2,"1":4};
function audit(original,profiles,grid,summary){
 gate(original.length===1944,"original source count");
 gate(profiles.length===81,"profile count");
 gate(grid.length===324,"grid count");
 const worlds=new Map(), profileMap=new Map(),gridMap=new Map();
 for(const r of original){
  const k=r.world, ij=r.source_i+","+r.source_j;
  gate(r.source_i!==r.source_j&&+r.source_i<+r.source_j&&+r.source_i>=0&&+r.source_j<4,"bad dyad identity");
  if(!worlds.has(k))worlds.set(k,{rows:new Map(),vector:r.initial_opinions,epsilon:r.confidence_radius});
  const w=worlds.get(k);gate(w.vector===r.initial_opinions&&w.epsilon===r.confidence_radius,"inconsistent world");
  gate(!w.rows.has(ij),"duplicate original dyad");
  w.rows.set(ij,r);
 }
 gate(worlds.size===324,"original world universe");
 const truth=new Map();
 for(const [key,w] of worlds){
  gate(w.rows.size===6,"missing original dyad");
  const x=w.vector.split(";").map(s=>quarter[s]),e=quarter[w.epsilon];
  gate(x.length===4&&x.every(v=>Number.isInteger(v))&&e!==undefined,"bad vector/epsilon");
  gate(key==="opinion="+x.map(z=>Object.keys(quarter).find(k=>quarter[k]===z)).join(",")+"|epsilon="+w.epsilon,"world key mismatch");
  const adj=Array.from({length:4},()=>[]);let edges=0;
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
   const row=w.rows.get(i+","+j);gate(!!row,"missing pair "+i+","+j);
   const edge=Math.abs(x[i]-x[j])<=e,dist=Math.abs(x[i]-x[j]);
   gate(row.is_confidence_dyad===(edge?"True":"False"),"original edge mismatch");
   gate(quarter[row.absolute_distance]===dist,"original distance mismatch");
   gate(quarter[row.opinion_i]===x[i]&&quarter[row.opinion_j]===x[j],"opinion mismatch");
   if(edge){adj[i].push(j);adj[j].push(i);edges++;}
  }
  const visited=new Set(),components=[];
  for(let i=0;i<4;i++)if(!visited.has(i)){
   const q=[i],c=[];visited.add(i);
   while(q.length){const a=q.shift();c.push(a);for(const b of adj[a])if(!visited.has(b)){visited.add(b);q.push(b);}}
   components.push(c);
  }
  const connected=components.length===1,clique=edges===6;
  for(const row of w.rows.values()){
   gate(+row.confidence_edge_count===edges,"original edge count mismatch");
   gate(+row.connected_component_count===components.length,"original component count mismatch");
   gate(row.graph_connected===(connected?"True":"False"),"original connected mismatch");
   gate(row.fully_pairwise_confident===(clique?"True":"False"),"original clique mismatch");
   const i=+row.source_i,j=+row.source_j;
   gate(+row.component_of_i===Math.min(...components.find(c=>c.includes(i))),"component_i mismatch");
   gate(+row.component_of_j===Math.min(...components.find(c=>c.includes(j))),"component_j mismatch");
  }
  truth.set(w.vector+"|"+w.epsilon,{connected,clique});
 }
 for(const r of grid){
  const key=r.vector+"|"+r.epsilon,t=truth.get(key);
  gate(t&&!gridMap.has(key),"duplicate/missing grid world");
  gate(r.connected_formula===(t.connected?"True":"False"),"connected prediction error");
  gate(r.clique_formula===(t.clique?"True":"False"),"clique prediction error");
  gridMap.set(key,r);
 }
 gate(gridMap.size===324,"grid identity missing");
 let positive=0,falsePositive=0;const counts={critical_connected:{},critical_clique:{},critical_gap:{}};
 for(const r of profiles){
  gate(!profileMap.has(r.vector),"duplicate profile");
  const states=E.map(e=>truth.get(r.vector+"|"+e));gate(states.every(Boolean),"missing profile states");
  const ci=states.findIndex(s=>s.connected),qi=states.findIndex(s=>s.clique);
  gate(ci>=0&&qi>=0,"unreachable complete graph");
  const c=E[ci],q=E[qi],gap=Object.keys(quarter).find(k=>quarter[k]===quarter[q]-quarter[c]);
  gate(r.critical_connected===c&&r.critical_clique===q&&r.critical_gap===gap,"critical radius mismatch");
  gate(r.grid_connected===c&&r.grid_clique===q,"grid radius mismatch");
  for(const [k,v] of Object.entries({critical_connected:c,critical_clique:q,critical_gap:gap}))counts[k][v]=(counts[k][v]||0)+1;
  if(gap!=="0")positive++;
  profileMap.set(r.vector,r);
 }
 gate(profileMap.size===81,"profile universe missing");
 for(const t of truth.values())if(t.connected&&!t.clique)falsePositive++;
 for(const k of Object.keys(counts))gate(Object.keys(counts[k]).length===Object.keys(summary[k+"_counts"]).length&&Object.keys(counts[k]).every(z=>counts[k][z]===summary[k+"_counts"][z]),"summary distribution mismatch");
 gate(summary.vectors===81&&summary.grid_worlds===324&&summary.original_source_rows_expected===1944,"summary universe mismatch");
 gate(summary.positive_gap_vectors===positive,"summary positive gap mismatch");
 gate(summary.connected_not_clique_worlds===falsePositive&&summary.naive_connected_as_clique_false_positives===falsePositive,"summary false positives mismatch");
 gate(summary.naive_connected_as_clique_correct===324-falsePositive&&summary.naive_connected_as_clique_false_positive_rate===falsePositive+"/324","summary baseline mismatch");
 gate(summary.scope==="E1_FINITE_ARTIFICIAL"&&summary.new_real_E2===0&&summary.new_historical_E3===0&&summary.R073==="FROZEN"&&summary.PESEN_v0_1==="FROZEN","evidence scope promotion");
 return {status:"PASS",original_rows:original.length,original_worlds:worlds.size,profile_rows:profileMap.size,grid_rows:gridMap.size,critical_distribution:counts,positive_gap:positive,false_positive: falsePositive};
}
function mutations(o,p,g,s){
 const copy=x=>JSON.parse(JSON.stringify(x)),mutants=[
  x=>x.o.push(copy(x.o[0])),
  x=>x.o.pop(),
  x=>x.o[0].is_confidence_dyad="False",
  x=>x.o[0].connected_component_count="4",
  x=>x.g[0].clique_formula="False",
  x=>x.p[0].critical_clique="1/2",
  x=>x.s.naive_connected_as_clique_correct=999,
  x=>x.s.new_real_E2=1
 ];let rejected=0;
 for(let i=0;i<mutants.length;i++){
  const x={o:copy(o),p:copy(p),g:copy(g),s:copy(s)};mutants[i](x);
  try{audit(x.o,x.p,x.g,x.s);}catch(e){rejected++;continue;}
  throw Error("mutation escaped "+i);
 }
 return {rejected,total:mutants.length};
}
if(typeof module!=="undefined")module.exports={parseCsv,audit,mutations};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 gate(process.argv.length>=6,"usage: node B.js ORIGINAL.csv PROFILES.csv GRID.csv SUMMARY.json [--mutations]");
 const o=parseCsv(fs.readFileSync(process.argv[2],"utf8")),p=parseCsv(fs.readFileSync(process.argv[3],"utf8")),
  g=parseCsv(fs.readFileSync(process.argv[4],"utf8")),s=JSON.parse(fs.readFileSync(process.argv[5],"utf8"));
 const result=audit(o,p,g,s);if(process.argv.includes("--mutations"))result.mutations=mutations(o,p,g,s);
 console.log(JSON.stringify(result,null,2));
}