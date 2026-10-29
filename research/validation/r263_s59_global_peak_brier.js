#!/usr/bin/env node
// R263 S59: exact E1 conditional Brier scores from the original frozen CSV.
// Usage: node r263_s59_global_peak_brier.js ORIGINAL.csv > RESULTS.json
const fs=require('fs');
const raw=fs.readFileSync(process.argv[2],'utf8').trimEnd().split('\n');
const columns=raw.shift().split(',');
const rows=raw.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[columns[i],v])));
const worlds=[...new Set(rows.map(r=>r.world))];
function gcd(a,b){while(b)[a,b]=[b,a%b];return a}
function add([a,b],[c,d]){let n=a*d+c*b,m=b*d,g=gcd(n,m);return[n/g,m/g]}
function fraction([a,b]){return b===1n?String(a):a+'/'+b}
function fit(g,obj){return obj==='TRAP'&&g==='000'?4:[...g].filter(x=>x==='1').length}
function independentMask(r){
  let a=parseInt(r.observed_parent0_threebit_genome,2),b=parseInt(r.observed_parent1_threebit_genome,2);
  const bits=Array.from({length:4},(_,i)=>Number(r['oracle_original_bit_'+(6+i)]));
  const [flag,cut,m0,m1]=bits;
  const cross=Number(r.frozen_crossover_enabled),mut=Number(r.frozen_mutation_enabled),elite=Number(r.frozen_elite_survival);
  let c=a,d=b;
  if(cross&&flag){const low=cut?1:3;c=(a&~low)|(b&low);d=(b&~low)|(a&low)}
  if(mut&&m0)c^=4;
  if(mut&&m1)d^=1;
  const score=x=>r.frozen_objective==='TRAP'&&x===0?4:x.toString(2).split('1').length-1;
  if(elite){const ranked=[a,b,c,d].map((v,i)=>({v,i,s:score(v)})).sort((x,y)=>y.s-x.s||x.v-y.v||x.i-y.i);c=ranked[0].v;d=ranked[1].v}
  return Number(Math.max(score(c),score(d))===(r.frozen_objective==='TRAP'?4:3));
}
const results=[];
for(const world of worlds){
  const subset=rows.filter(r=>r.world===world),ids=new Set(),groups=Array.from({length:5},()=>new Map());
  let positives=0;
  for(const r of subset){
    const bits=Array.from({length:10},(_,i)=>r['oracle_original_bit_'+i]).join('');
    if(ids.has(bits))throw Error('duplicate original source '+world+bits);
    ids.add(bits);
    const a=r.observed_parent0_threebit_genome,b=r.observed_parent1_threebit_genome;
    if(a!==bits.slice(0,3)||b!==bits.slice(3,6)||r.original_complete_tenbit_source_mass!=='1/1024')throw Error('source mismatch');
    const y=Number(Number(r.observed_next_survivor_best_fitness)===(r.frozen_objective==='TRAP'?4:3));
    if(y!==independentMask(r))throw Error('independent offspring oracle mismatch '+world+bits);
    positives+=y;
    const keys=['all',String(Math.max(fit(a,r.frozen_objective),fit(b,r.frozen_objective))),a+b,a+b+bits[6],bits];
    keys.forEach((key,i)=>{let z=groups[i].get(key)||[0,0];z[0]++;z[1]+=y;groups[i].set(key,z)});
  }
  if(ids.size!==1024||subset.length!==1024)throw Error('incomplete world '+world);
  const risks=groups.map(g=>{
    let sum=[0n,1n],mixed=0;
    for(const [n,k] of g.values())if(k&&k<n){mixed++;sum=add(sum,[BigInt(k*(n-k)),BigInt(n*1024)])}
    return {risk:fraction(sum),groups:g.size,mixed_groups:mixed};
  });
  const [F0,FB,FP,FPC,FF]=risks;
  if(FF.risk!=='0')throw Error('full information not deterministic');
  results.push({world,source_atoms:1024,global_peak_positive:positives,F0,FB,FP,FPC,FF});
}
if(results.length!==9||rows.length!==9216)throw Error('incomplete universe');
const output={research:'R263 S59',evidence:'E1',protocol:'protocols/R263_S59_PARTIAL_PARENT_INFORMATION_GLOBAL_PEAK_BRIER_FREEZE_2026-10-29.md',all_atoms:9216,exact_risks:45,independent_oracle:'original CSV versus integer-mask offspring',results,R073:'FROZEN',PESEN_v0_1:'FROZEN',E2_new:0,E3_new:0};
process.stdout.write(JSON.stringify(output,null,2)+'\n');
