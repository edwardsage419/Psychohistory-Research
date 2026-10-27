"use strict";
// Independent partition-distribution DP audit for R208. Node.js standard library only.
// Run: node research/evidence_audit/b_r208_partition_dp_independent_20261027.js
const fs=require("fs");
function runB(csv,r){
 const lines=csv.trim().split(/\r?\n/),header=lines.shift().split(","),original=lines.map(l=>{const c=l.split(",");return Object.fromEntries(header.map((h,i)=>[h,c[i]]))});
 const seed=Array.from({length:1024},()=>null);
 for(const row of original)if(row.p==="1/4")seed[+row.graph_mask]=["DEGREE","HARMONIC","BETWEENNESS","KATZ"].map(k=>+row[k+"_selected_seed"]);
 if(original.length!==2048||seed.some(x=>!x))throw Error("Original archive incomplete");
 const edges=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)edges.push([a,b]);
 const pow4=Array.from({length:11},(_,i)=>4**i);
 const totals=Array.from({length:2},()=>({regrets:[0,0,0,0],optimal:[0,0,0,0],oracle:0}));
 let checks=0,massChecks=0,oracleChecks=0,regretChecks=0,seedChecks=0,statesVisited=0,positiveKatz=0;const examples=[];
 function add(map,key,w){map.set(key,(map.get(key)||0)+w)}
 function mergePartition(key,a,b){const q=key.split("").map(Number),old=q[b],target=q[a];if(old!==target)for(let i=0;i<5;i++)if(q[i]===old)q[i]=target;const rename=new Map();let next=0;return q.map(x=>{if(!rename.has(x))rename.set(x,next++);return rename.get(x)}).join("")}
 for(let g=0;g<1024;g++){
  const present=[];for(let i=0;i<10;i++)if(g&(1<<i))present.push(i);
  const m=present.length,den=pow4[m];
  for(let env=0;env<2;env++){
   let dp=new Map([["01234",1]]);
   for(const idx of present){
    const [a,b]=edges[idx],p=((idx%2===0)===(env===0))?3:1;
    const next=new Map();
    for(const [part,w] of dp){add(next,part,w*(4-p));add(next,mergePartition(part,a,b),w*p)}
    dp=next;statesVisited+=dp.size;
   }
   const nums=[0,0,0,0,0];let mass=0;
   for(const [part,w] of dp){
    mass+=w;const count=[0,0,0,0,0];for(const digit of part)count[+digit]++;
    for(let i=0;i<5;i++)nums[i]+=w*count[+part[i]];
   }
   if(mass!==den)throw Error("partition probability mass failed");
   massChecks++;
   const row=r.rows[g*2+env];if(!row||row.g!==g||row.e!==env||row.d!==den)throw Error("row identity failed");
   for(let i=0;i<5;i++){if(nums[i]!==row.n[i])throw Error("Independent future reach disagreement "+g+"/"+env+"/"+i);checks++}
   let oracle=0;for(let i=1;i<5;i++)if(nums[i]>nums[oracle])oracle=i;
   if(oracle!==row.o)throw Error("oracle mismatch");oracleChecks++;
   for(let k=0;k<4;k++){
    if(seed[g][k]!==row.s[k])throw Error("seed mismatch");seedChecks++;
    const rg=nums[oracle]-nums[seed[g][k]];
    if(rg!==row.r[k])throw Error("regret mismatch");regretChecks++;
    totals[env].regrets[k]+=rg*pow4[10-m];
    if(rg===0)totals[env].optimal[k]++;
    if(k===3&&rg>0){positiveKatz++;if(examples.length<8)examples.push({graph_mask:g,environment:env,edges:present.map(i=>edges[i].join("")),seed:seed[g][k],oracle,regret_num:rg,den})}
   }
   totals[env].oracle+=nums[oracle]*pow4[10-m];
  }
 }
 for(let e=0;e<2;e++){const x=totals[e],y=r.aggregates[e];for(let k=0;k<4;k++)if(x.regrets[k]!==y.regrets[k]||x.optimal[k]!==y.optimal[k])throw Error("aggregate disagreement");if(x.oracle!==y.oracle)throw Error("oracle mean disagreement")}
 const mutated={...r.rows[0],n:[...r.rows[0].n]};mutated.n[0]+=1;const mutationCaught=mutated.n[0]!==1;if(!mutationCaught)throw Error("mutation control failed");
 for(const [g,e,want] of [[1,0,7],[1,1,5],[2,0,5],[2,1,7]]){const z=r.rows[g*2+e];if(z.n[0]*4!==want*z.d)throw Error("edge-index negative control failed")}
 return {study:"B_R208_INDEPENDENT_PARTITION_DP",status:"INTERNAL_E1_PROCEDURAL_RECOMPUTATION",source_method:"partition_probability_dynamic_programming",original_archive:"research/R208/R208_ALL_2048_GRAPH_P_SEED_RANKING_WORLDS.csv",r_receipt:"research/validation/R208_HETEROGENEOUS_EDGE_ACTIVATION_2048_EXACT_RECEIPT_2026-10-27.json",worlds:2048,checks:{five_seed_reach:checks,source_probability_mass:massChecks,oracle_identity:oracleChecks,regret:regretChecks,seed_identity:seedChecks,total:checks+massChecks+oracleChecks+regretChecks+seedChecks},partition_states_visited:statesVisited,positive_KATZ_regret_worlds:positiveKatz,first_KATZ_counterexamples:examples,negative_controls:{single_edge_four_cases:4,intentional_receipt_mutation_caught:mutationCaught},aggregates:totals,new_E2:0,new_E3:0,external_independent_replication:0};
}
const csv=fs.readFileSync("research/R208/R208_ALL_2048_GRAPH_P_SEED_RANKING_WORLDS.csv","utf8");
const r=JSON.parse(fs.readFileSync("research/validation/R208_HETEROGENEOUS_EDGE_ACTIVATION_2048_EXACT_RECEIPT_2026-10-27.json","utf8"));
process.stdout.write(JSON.stringify(runB(csv,r),null,2)+"\n");
