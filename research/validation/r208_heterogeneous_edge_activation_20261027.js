"use strict";
// R208 frozen heterogeneous-edge experiment, Node.js standard library only.
// Run: node research/validation/r208_heterogeneous_edge_activation_20261027.js > /tmp/r208_receipt.json
const fs=require("fs");
function runR(csv){
 const lines=csv.trim().split(/\r?\n/);const head=lines.shift().split(",");const rows=lines.map(l=>{const c=l.split(",");return Object.fromEntries(head.map((h,i)=>[h,c[i]]))});
 if(rows.length!==2048)throw Error("Expected 2048 original rows, got "+rows.length);
 const seeds={};for(const r of rows){const g=+r.graph_mask;if(!seeds[g])seeds[g]=[];const x=["DEGREE","HARMONIC","BETWEENNESS","KATZ"].map(k=>+r[k+"_selected_seed"]);seeds[g].push(x)}
 for(let g=0;g<1024;g++)if(seeds[g].length!==2||seeds[g][0].some((x,i)=>x!==seeds[g][1][i]))throw Error("original seed mismatch "+g);
 const edges=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)edges.push([i,j]);
 const pow4=Array.from({length:11},(_,i)=>4**i);const gcd=(a,b)=>b?gcd(b,a%b):a;
 const frac=(a,d)=>{const g=gcd(a,d);return d/g===1?String(a/g):a/g+"/"+d/g};
 const totals=Array.from({length:2},()=>({regrets:[0,0,0,0],oracle:0,selected:[0,0,0,0],optimal:[0,0,0,0],fixed0:0,uniform:0}));
 const out=[];let events=0;
 for(let g=0;g<1024;g++){
  const active=[];for(let i=0;i<10;i++)if(g&(1<<i))active.push(i);
  const m=active.length,den=pow4[m];events+=2*(1<<m);
  for(let env=0;env<2;env++){
   const pn=active.map(i=>((i%2===0)===(env===0))?3:1);let mass=0;const nums=[0,0,0,0,0];
   for(let s=0;s<(1<<m);s++){
    let w=1;const parent=[0,1,2,3,4];const root=i=>{while(parent[i]!==i)i=parent[i];return i};
    for(let j=0;j<m;j++){
     const on=!!(s&(1<<j));w*=on?pn[j]:4-pn[j];
     if(on){const [a,b]=edges[active[j]];const ra=root(a),rb=root(b);if(ra!==rb)parent[rb]=ra}
    }
    mass+=w;
    const sz=[0,0,0,0,0];for(let i=0;i<5;i++)sz[root(i)]++;
    for(let i=0;i<5;i++)nums[i]+=w*sz[root(i)];
   }
   if(mass!==den)throw Error("mass "+g+" "+env);
   let best=0;for(let i=1;i<5;i++)if(nums[i]>nums[best])best=i;
   const sd=seeds[g][0],rg=sd.map(i=>nums[best]-nums[i]);
   const t=totals[env],scale=pow4[10-m];
   t.oracle+=nums[best]*scale;t.fixed0+=nums[0]*scale;t.uniform+=nums.reduce((a,b)=>a+b,0)*scale;
   for(let k=0;k<4;k++){t.regrets[k]+=rg[k]*scale;t.selected[k]+=nums[sd[k]]*scale;if(rg[k]===0)t.optimal[k]++}
   out.push({g,e:env,m,d:den,n:nums,o:best,s:sd,r:rg});
  }
 }
 if(events!==118098||out.length!==2048)throw Error("source count mismatch");
 for(const [env,t] of totals.entries()){t.regret_fraction=t.regrets.map(v=>frac(v,pow4[10]*1024));t.optimal_rate=t.optimal.map(v=>frac(v,1024));t.oracle_mean=frac(t.oracle,pow4[10]*1024);t.fixed0_mean=frac(t.fixed0,pow4[10]*1024);t.uniform_mean=frac(t.uniform,pow4[10]*1024*5);t.env=env===0?"ENV_A":"ENV_B"}
 const r=(g,e)=>out.find(z=>z.g===g&&z.e===e);
 for(const [g,env,want] of [[1,0,7],[1,1,5],[2,0,5],[2,1,7]]){const z=r(g,env);const i=g===1?0:0;if(z.n[i]*4!==want*z.d)throw Error("single edge negative control "+g+" "+env+" got "+z.n[i]+"/"+z.d)}
 return {study:"R208_HETEROGENEOUS_EDGE_ACTIVATION",evidence:"E1_ARTIFICIAL",prescore_freeze_commit:"6e948f3d5ae92b715c802bc7e390c2ff4d568b87",original_archive:"research/R208/R208_ALL_2048_GRAPH_P_SEED_RANKING_WORLDS.csv",methods:["DEGREE","HARMONIC","BETWEENNESS","KATZ"],environment_definitions:["even=3/4,odd=1/4","even=1/4,odd=3/4"],worlds:out.length,source_events:events,aggregates:totals,rows:out};
}
const csv=fs.readFileSync("research/R208/R208_ALL_2048_GRAPH_P_SEED_RANKING_WORLDS.csv","utf8");
process.stdout.write(JSON.stringify(runR(csv),null,2)+"\n");
