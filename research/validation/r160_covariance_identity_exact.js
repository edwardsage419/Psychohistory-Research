#!/usr/bin/env node
"use strict";
// R160 exact BigInt audit of frozen joint frequency archive. Node 18+.
function auditR160(doc){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a||1n};
 const q=(n,d=1n)=>{if(typeof n==="string"){let x=n.split("/");return q(BigInt(x[0]),x[1]?BigInt(x[1]):1n)}if(typeof n==="number")n=BigInt(n);if(typeof d==="number")d=BigInt(d);if(d===0n)throw Error("zero denom");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return[n/g,d/g]};
 const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const sub=(a,b)=>q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]);
 const div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const str=a=>a[1]===1n?a[0].toString():a[0]+"/"+a[1];
 const Z=q(0),O=q(1),totals=new Map();
 if(doc.research_id!=="R160"||doc.main_worlds!==60||doc.worlds.length!==60)throw Error("wrong source");
 let tables=0,transitions=0,dChecks=0,gChecks=0,mutantOneZ=0,mutantNoSelection=0;
 for(const w of doc.worlds){
   const s=q(w.s),u=q(w.u);
   if(w.points.length!==5)throw Error("bad horizon");
   for(let i=0;i<5;i++){
     const pt=w.points[i],cells=pt.joint_00_01_10_11.map(q);
     const sum=cells.reduce(add,Z);
     if(!eq(sum,O)||cells.some(x=>x[0]<0n))throw Error("probability mass");
     const [p00,p01,p10,p11]=cells,G=add(p10,p11),C=add(p01,p11),D=sub(p11,mul(G,C));
     if(!eq(q(pt.G1_fraction),G)||!eq(q(pt.C1_fraction),C)||!eq(q(pt.gene_culture_association_D),D))throw Error("archive marginal mismatch");
     tables++;
     if(i===0){
       const key=w.id.replace(/_h\d+/,"");
       const a=totals.get(key)||[];
       a.push({h:w.h,d:q(w.points[1].gene_culture_association_D),c:q(w.points[1].C1_fraction)});
       totals.set(key,a);
     }
     if(i<4){
       const norm=add(O,mul(s,p11));
       const numerator=add(D,mul(s,mul(p00,p11)));
       const nextD=mul(sub(O,u),div(numerator,mul(norm,norm)));
       const nextG=div(add(G,mul(s,p11)),norm);
       const actualD=q(w.points[i+1].gene_culture_association_D);
       const actualG=q(w.points[i+1].G1_fraction);
       if(!eq(nextD,actualD)||!eq(nextG,actualG))throw Error("exact identity mismatch "+w.id+" "+i);
       const mutantZ=mul(sub(O,u),div(numerator,norm));
       const mutantNoSel=mul(sub(O,u),D);
       if(!eq(mutantZ,actualD))mutantOneZ++;
       if(!eq(mutantNoSel,actualD))mutantNoSelection++;
       dChecks++;gChecks++;transitions++;
     }
   }
 }
 let invariantGroups=0,invariantPairs=0,cultureSensitiveGroups=0;
 for(const [key,rows] of totals){
   if(rows.length!==3)throw Error("missing h group "+key);
   if(!eq(rows[0].d,rows[1].d)||!eq(rows[1].d,rows[2].d))throw Error("h dependence of D "+key);
   invariantGroups++;invariantPairs+=2;
   if(!eq(rows[0].c,rows[2].c))cultureSensitiveGroups++;
 }
 if(tables!==300||transitions!==240||invariantGroups!==20||invariantPairs!==40)throw Error("count mismatch");
 return {research:"R160",source:"frozen_60_world_archive",evidence:"E1_SYNTHETIC",joint_tables_mass_and_marginal_checks:tables,covariance_identity_exact_transitions:dChecks,gene_marginal_identity_exact_transitions:gChecks,independent_h_groups:invariantGroups,h_pairwise_covariance_equalities:invariantPairs,h_sensitive_first_step_culture_groups:cultureSensitiveGroups,wrong_single_Z_mutant_detected:mutantOneZ,omitted_selection_term_mutant_detected:mutantNoSelection,representative_s_half_u_quarter_uniform_D:"1/54",original_author_equations_reproduced:false,real_human_genetics_used:false,external_independent_replication:false};
}
const fs=require("node:fs");
if(process.argv.length!==3){console.error("Usage: node r160_covariance_identity_exact.js R160_EXACT_RESULTS.json");process.exit(2)}
console.log(JSON.stringify(auditR160(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));
