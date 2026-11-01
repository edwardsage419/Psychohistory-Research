#!/usr/bin/env node
'use strict';
/* R257 S53 source lineage audit. Internal nonblind artificial E1 only.
 * No audited Python implementation imported. Run:
 * node research/validation/r257_s53_original225_source_link_gate_20261102.js --repo-root .
 */
const f=s=>{if(typeof s!=='string'||!(/^-?\d+(?:\/[1-9]\d*)?$/).test(s))throw Error('rational');let [n,d='1']=s.split('/');return [BigInt(n),BigInt(d)]};
const eq=(x,y)=>x[0]*y[1]===y[0]*x[1];
const add=(x,y)=>[x[0]*y[1]+y[0]*x[1],x[1]*y[1]];
const sub=(x,y)=>[x[0]*y[1]-y[0]*x[1],x[1]*y[1]];
const mul=(x,y)=>[x[0]*y[0],x[1]*y[1]];
const le=(x,y)=>x[0]*y[1]<=y[0]*x[1];
const two=f('2'),grid=['0','1/4','1/2','3/4','1'],nonconvex='NONCONVEX_KKT_NOT_SUFFICIENT';
const header='world,original_candidate_x,original_candidate_y,frozen_capacity_C,original_candidate_feasible,original_objective_value,original_grad_fx,original_grad_fy,original_capacity_slack,original_uniform_grid_design_mass,actual_math_world_is_convex';
function check(d){
const rr=JSON.parse(d.original),sr=JSON.parse(d.receipt),lines=d.csv.trim().split(/\r?\n/);
if(lines[0]!==header)throw Error('CSV header');
const keys=lines[0].split(','),r=lines.slice(1).map(s=>Object.fromEntries(s.split(',').map((v,i)=>[keys[i],v])));
if(r.length!==225||rr.world_results.length!==9||sr.worlds.length!==8)throw Error('universe');
const rm=new Map(rr.world_results.map(w=>[w.world,w])),sm=new Map(sr.worlds.map(w=>[w.world,w]));
const m=d.s53.match(/WORLDS = \{([\s\S]*?)\n\}/);if(!m)throw Error('S53 source');
const mm=new Map([...m[1].matchAll(/^\s*'([A-Z0-9_]+)':\s*\('([^']+)',\s*'([^']+)',\s*'([^']+)'\),?\s*$/gm)].map(x=>[x[1],[x[2],x[3],x[4]]]));
if(rm.size!==9||sm.size!==8||mm.size!==8||sm.has(nonconvex))throw Error('world universe');
const groups=new Map([...rm.keys()].map(k=>[k,new Set()]));let convex=0,non=0,feasible=0;
for(const row of r){
if(Object.keys(row).length!==11)throw Error('CSV fields');
const w=rm.get(row.world);if(!w)throw Error('unknown world');
const x=f(row.original_candidate_x),y=f(row.original_candidate_y),C=f(row.frozen_capacity_C);
const gx=grid.find(z=>eq(f(z),x)),gy=grid.find(z=>eq(f(z),y));if(gx===undefined||gy===undefined)throw Error('grid');
const k=gx+'|'+gy,g=groups.get(row.world);if(g.has(k))throw Error('duplicate grid');g.add(k);
if(!eq(C,f(w.capacity)))throw Error('capacity');
const ok=le(add(x,y),C);if(row.original_candidate_feasible!==(ok?'1':'0'))throw Error('feasible');
if(ok)feasible++;
if(!eq(f(row.original_capacity_slack),sub(C,add(x,y))))throw Error('slack');
if(!eq(f(row.original_uniform_grid_design_mass),f('1/25')))throw Error('mass');
const cv=w.globally_convex_and_strictly_positive_definite===true;
if(row.actual_math_world_is_convex!==(cv?'1':'0'))throw Error('convex label');
if(cv){
const dx=sub(x,f(w.target_a)),dy=sub(y,f(w.target_b));
if(!eq(f(row.original_grad_fx),mul(two,dx))||!eq(f(row.original_grad_fy),mul(two,dy)))throw Error('gradient');
if(!eq(f(row.original_objective_value),add(mul(dx,dx),mul(dy,dy))))throw Error('objective');
convex++;
}else{if(row.world!==nonconvex)throw Error('nonconvex identity');non++;}
}
for(const [k,v] of groups)if(v.size!==25)throw Error('grid completeness '+k);
for(const [id,w] of rm){if(id===nonconvex)continue;
const x=mm.get(id),s=sm.get(id);if(!x||!s)throw Error('missing S53 world');
if(!eq(f(x[0]),f(w.capacity))||!eq(f(x[1]),f(w.target_a))||!eq(f(x[2]),f(w.target_b)))throw Error('S53 code source binding');
if(!eq(f(s.baseline_capacity),f(w.capacity))||!eq(f(s.baseline_minimum),f(w.exact_continuous_global_optimum_value))||!eq(f(s.baseline_lambda),f(w.exact_convex_KKT_primal_dual_complementary_certificate.lambda_capacity)))throw Error('S53 baseline binding');
const zero=s.perturbations.filter(z=>eq(f(z.delta),f('0')));
if(zero.length!==1||!eq(f(zero[0].minimum),f(w.exact_continuous_global_optimum_value))||!zero[0].point.every((v,i)=>eq(f(v),f(w.exact_continuous_global_optimum[i]))))throw Error('S53 delta zero');
}
if(convex!==200||non!==25||feasible!==145)throw Error('partitions '+convex+' '+non+' '+feasible);
return {status:'PASS_SOURCE_LINK_INTERNAL_E1_ONLY',original_rows:225,convex_rows:convex,nonconvex_rows_structure_only:non,feasible_grid_rows:feasible,linked_worlds:8,blind_order:'FAIL',formal_scientific_acceptance:'PARTIAL'};
}
module.exports={check};
if(require.main===module){
 const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
 const pins={
 csv:['research/R257/R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv','63dc333cf4c4206fa466e0c0f33e3b079f4dc01b'],
 original:['research/R257/R257_EXACT_RESULTS.json','55c00defa893ba3ed36cc5d3a6b0144953f16301'],
 s53:['research/validation/r257_s53_capacity_shadow_20261029.py','4026c2111eed6d64dd21d100ab9961c00a6fa71e'],
 receipt:['research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json','37f33083b45435e18c66641ef693c6f0c779a680']};
 try{
  if(process.argv.length!==4||process.argv[2]!=='--repo-root')throw Error('usage: --repo-root PATH');
  const root=path.resolve(process.argv[3]),data={};
  for(const [k,[rel,pin]] of Object.entries(pins)){
   const file=path.join(root,rel),stat=fs.lstatSync(file);
   if(!stat.isFile()||stat.isSymbolicLink())throw Error('unsafe input '+rel);
   const b=fs.readFileSync(file);
   const hash=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+String.fromCharCode(0))).update(b).digest('hex');
   if(hash!==pin)throw Error('Git blob mismatch '+rel);
   data[k]=b.toString('utf8');
  }
  console.log(JSON.stringify(check(data)));
 }catch(e){console.error('SOURCE_LINK_FAIL: '+e.message);process.exitCode=1;}
}
