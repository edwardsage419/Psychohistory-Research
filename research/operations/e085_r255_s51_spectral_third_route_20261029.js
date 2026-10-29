"use strict";
// E085 third-route spectral closed form for R255 S51.
// Run in a repository checkout:
// node research/operations/e085_r255_s51_spectral_third_route_20261029.js
function runE085(receipt,csvText){
  let checks=0;function ok(v,msg){checks++;if(!v)throw new Error("CHECK_"+checks+" "+msg);}
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
  function frac(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
  function plus(x,y){return frac(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
  function minus(x,y){return frac(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
  function fstr(x){return x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);}
  const edges=[[0,1],[0,2],[1,2]];
  function spectral(mask,seed,t){
    const x=seed.map(BigInt),n=BigInt(t),pow4=4n**n,sum=x[0]+x[1]+x[2];
    const degree=[0,0,0],open=[];
    edges.forEach(([a,b],i)=>{if(mask&(1<<i)){degree[a]++;degree[b]++;open.push([a,b]);}});
    let num=[0n,0n,0n];
    if(open.length===0){num=x.map(z=>6n*pow4*z);}
    else if(open.length===1){
      const [a,b]=open[0],k=[0,1,2].find(i=>i!==a&&i!==b);
      num[a]=3n*pow4*(x[a]+x[b])+3n*(2n**n)*(x[a]-x[b]);
      num[b]=3n*pow4*(x[a]+x[b])-3n*(2n**n)*(x[a]-x[b]);
      num[k]=6n*pow4*x[k];
    }else if(open.length===2){
      const c=degree.indexOf(2),leaves=[0,1,2].filter(i=>i!==c);
      const [a,b]=leaves,d=x[a]-x[b],q=x[a]+x[b]-2n*x[c];
      num[a]=2n*pow4*sum+3n*(3n**n)*d+q;
      num[b]=2n*pow4*sum-3n*(3n**n)*d+q;
      num[c]=2n*pow4*sum-2n*q;
    }else{num=x.map(z=>2n*pow4*sum+6n*z-2n*sum);}
    return num.map(z=>frac(z,6n*pow4));
  }
  function row(mask,seed){
    return Array.from({length:4},(_,t)=>spectral(mask,seed,t));
  }
  const states=[];
  for(let mask=0;mask<8;mask++)for(let seedCode=0;seedCode<8;seedCode++){
    const seed=[(seedCode>>2)&1,(seedCode>>1)&1,seedCode&1],path=row(mask,seed);
    states.push({mask,seed,path,target:((mask&1)+((mask>>1)&1)+((mask>>2)&1))>=2?1:0});
  }
  ok(states.length===64,"64 graph seed states");
  ok(states.reduce((s,r)=>s+r.target,0)===32,"half connected");
  const expected=receipt.risk_by_world,real=expected.ER_TRIANGLE_P_HALF,alias=expected.STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF;
  function riskAt(horizon,isAlias){
    const groups=new Map();
    for(const r of states){
      const key=r.path.slice(0,horizon+1).flat().map(fstr).join("|");
      const g=groups.get(key)||{n:0,s:0};g.n++;g.s+=isAlias?0:r.target;groups.set(key,g);
    }
    let total=frac(0),mixed=0,max=0;
    for(const {n,s} of groups.values()){
      total=plus(total,frac(BigInt(s*(n-s)),BigInt(n*64)));
      if(s>0&&s<n)mixed++;if(n>max)max=n;
    }
    return {groups:groups.size,mixed_label_groups:mixed,max_group_size:max*8,risk:fstr(total)};
  }
  let totalGroups=0;
  for(const [name,record,isAlias] of [["ER_TRIANGLE_P_HALF",real,false],["STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF",alias,true]]){
    const risks=[];
    for(let t=0;t<4;t++){
      const f="F"+t,computed=riskAt(t,isAlias),detail=record.group_details[f];
      ok(computed.risk===record[f],name+" "+f+" risk");
      for(const field of ["groups","mixed_label_groups","max_group_size","risk"])
        ok(computed[field]===detail[field],name+" "+f+" "+field);
      risks.push(frac(...computed.risk.split("/").map(BigInt)));
      totalGroups+=computed.groups;
    }
    for(let i=0;i<3;i++)ok(fstr(minus(risks[i],risks[i+1]))===record.improvements[i],name+" improvement "+i);
  }
  const lines=csvText.trimEnd().split(/\r?\n/);
  const header=lines[0].split(","),rows=lines.slice(1);
  ok(rows.length===512,"512 reconstructed rows");
  const wanted=["edge_bits","seed_bits","reported_edge_mask","x0","x1","x2","x3","ER_observed_connected","ALIAS_true_connected","mass"];
  ok(JSON.stringify(header)===JSON.stringify(wanted),"exact CSV header");
  const seen=new Set();
  for(const line of rows){
    const fields=line.split(","),r=Object.fromEntries(header.map((h,i)=>[h,fields[i]]));
    const bits=r.edge_bits,seedbits=r.seed_bits;
    ok(bits.length===6&&/^[01]+$/.test(bits),"six binary bits");
    ok(seedbits.length===3&&/^[01]+$/.test(seedbits),"three binary seed");
    const mask=[0,2,4].reduce((m,i,k)=>m+(bits[i]==="0"?(1<<k):0),0);
    const seed=seedbits.split("").map(Number);
    const key=bits+":"+seedbits;ok(!seen.has(key),"unique source");seen.add(key);
    const path=row(mask,seed);
    const expectedMask=edges.map((_,i)=>mask&(1<<i)?"1":"0").join("");
    ok(r.reported_edge_mask===expectedMask,"reported mask");
    for(let t=0;t<4;t++)for(let i=0;i<3;i++){
      ok(r["x"+t].split(";")[i]===fstr(path[t][i]),"spectral CSV opinion "+t+" "+i);
    }
    const connected=((mask&1)+((mask>>1)&1)+((mask>>2)&1))>=2?1:0;
    ok(Number(r.ER_observed_connected)===connected,"observed connectivity");
    ok(r.ALIAS_true_connected==="0","hidden empty");
    ok(r.mass==="1/512","source mass");
  }
  ok(seen.size===512,"complete nine-bit combinations");
  const changed=JSON.parse(JSON.stringify(receipt));changed.risk_by_world.ER_TRIANGLE_P_HALF.F2="999";
  ok(riskAt(2,false).risk!==changed.risk_by_world.ER_TRIANGLE_P_HALF.F2,"mutated receipt rejected");
  return {checks,failures:0,source_rows:rows.length,source_opinion_coordinates:rows.length*12,
    independent_graph_seed_states:64,total_prefix_group_counts_across_worlds:totalGroups,
    real_risks:[0,1,2,3].map(t=>riskAt(t,false).risk),
    alias_risks:[0,1,2,3].map(t=>riskAt(t,true).risk),
    mixed_groups:[0,1,2,3].map(t=>riskAt(t,false).mixed_label_groups),
    route:"SPECTRAL_CLOSED_FORM_NOT_MATRIX_ITERATION_OR_PATH_ENUMERATION",
    original_R255_18432_CSV_audited:false};
}
if(typeof module!=="undefined"&&require.main===module){
  const fs=require("fs");
  const receipt=JSON.parse(fs.readFileSync("research/validation/R255_S51_EXACT_RECEIPT_2026-10-29.json","utf8"));
  const csv=fs.readFileSync("research/validation/R255_S51_SOURCE_RECONSTRUCTION_2026-10-29.csv","utf8");
  console.log(JSON.stringify(runE085(receipt,csv),null,2));
}
