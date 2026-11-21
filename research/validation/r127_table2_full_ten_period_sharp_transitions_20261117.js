#!/usr/bin/env node
"use strict";
/*
 R127 secondary sharp partial-identification audit.
 Input is the existing archived seven-session, ten-period Table 2 transcription.
 This script does not infer real participant trajectories. All constructed paths
 are synthetic witnesses of bounds consistent with published aggregate marginals.
 Standard Node.js only. From repository root:
 node research/validation/r127_table2_full_ten_period_sharp_transitions_20261117.js
*/
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const ROOT=path.resolve(__dirname,"../../");
const SOURCE=path.join(ROOT,"research/validation/r127_primary_table2_70_periods_source_audit_20261103.js");
const EXPECTED_BLOB="aa575a803e5547afe24eabc1f232f2b539ef1709";
const raw=fs.readFileSync(SOURCE);
const blob=crypto.createHash("sha1").update(Buffer.concat([
 Buffer.from("blob "+raw.length+"\0"),raw
])).digest("hex");
if(blob!==EXPECTED_BLOB)throw Error("SOURCE_BLOB_MISMATCH");
const code=raw.toString("utf8");
const match=code.match(/const TABLES = (\{[\s\S]*?\});\nconst SIZES/);
if(!match)throw Error("TABLE_SOURCE_FORMAT_CHANGED");
const TABLES=JSON.parse(match[1].replace(/(?<!")\b([1-7]):(?=\[)/g,'"$1":'));
function analyze(TABLES) {
  const sizes=[16,16,14,15,16,16,14],group=[],byStep=Array.from({length:9},(_,t)=>({t:t+1,minimum_changes:0,maximum_changes:0,minimum_absolute_effort_distance:0,minimum_enter_effort1:0,minimum_exit_effort1:0}));
  const sum=arr=>arr.reduce((s,x)=>s+x,0);
  const require=(v,msg)=>{if(v!==true)throw Error(msg)};
  function minCost(a,b,maximize) {
    const N=16,source=14,sink=15,G=Array.from({length:N},()=>[]);
    function edge(u,v,cap,cost) {
      G[u].push({v,cap,cost,rev:G[v].length,original:cap});
      G[v].push({v:u,cap:0,cost:-cost,rev:G[u].length-1,original:0});
    }
    for(let i=0;i<7;i++)edge(source,i,a[i],0);
    for(let i=0;i<7;i++)for(let j=0;j<7;j++)edge(i,7+j,Math.min(a[i],b[j]),i===j?0:(maximize?-1:1));
    for(let j=0;j<7;j++)edge(7+j,sink,b[j],0);
    let sent=0,cost=0,iterations=0,n=sum(a);
    while(sent<n) {
      const dist=Array(N).fill(Infinity),prev=Array(N).fill(null);dist[source]=0;
      for(let k=0;k<N-1;k++) {
        let changed=false;
        for(let u=0;u<N;u++)if(Number.isFinite(dist[u]))for(let j=0;j<G[u].length;j++){
          const e=G[u][j];
          if(e.cap>0&&dist[e.v]>dist[u]+e.cost){dist[e.v]=dist[u]+e.cost;prev[e.v]=[u,j];changed=true;}
        }
        if(!changed)break;
      }
      require(prev[sink]!==null,"FLOW_PATH_MISSING");
      let inc=Infinity;
      for(let v=sink;v!==source;){const [u,j]=prev[v];inc=Math.min(inc,G[u][j].cap);v=u;}
      for(let v=sink;v!==source;){const [u,j]=prev[v],e=G[u][j];e.cap-=inc;G[v][e.rev].cap+=inc;cost+=inc*e.cost;v=u;}
      sent+=inc;iterations++;
      require(iterations<=500,"FLOW_ITERATION_LIMIT");
    }
    const matrix=Array.from({length:7},(_,i)=>Array.from({length:7},(_,j)=>{
      const e=G[i].find(e=>e.v===j+7);
      return e?e.original-e.cap:0;
    }));
    for(let i=0;i<7;i++){
      require(sum(matrix[i])===a[i],"FLOW_ROW_MARGINAL");
      require(sum(matrix.map(row=>row[i]))===b[i],"FLOW_COL_MARGINAL");
    }
    const switches=matrix.reduce((s,row,i)=>s+row.reduce((v,x,j)=>v+(i===j?0:x),0),0);
    require(switches===Math.abs(cost),"FLOW_COST_AUDIT");
    return {matrix,switches};
  }
  function earth(a,b) {
    const aa=a.flatMap((v,i)=>Array(v).fill(i)),bb=b.flatMap((v,i)=>Array(v).fill(i));
    require(aa.length===bb.length,"EARTH_SIZE");
    const matrix=Array.from({length:7},()=>Array(7).fill(0));
    let dist=0;for(let k=0;k<aa.length;k++){matrix[aa[k]][bb[k]]++;dist+=Math.abs(aa[k]-bb[k]);}
    let prefix=0,oracle=0;for(let i=0;i<6;i++){prefix+=a[i]-b[i];oracle+=Math.abs(prefix);}
    require(dist===oracle,"EARTH_PREFIX_MISMATCH");
    return {matrix,dist};
  }
  function compose(matrices,initialCounts) {
    const agents=initialCounts.flatMap((v,i)=>Array.from({length:v},()=>[i]));
    let switches=0,distance=0;
    for(const matrix of matrices) {
      const lookup=Array.from({length:7},()=>[]);
      agents.forEach((p,id)=>lookup[p.at(-1)].push(id));
      const next=Array(agents.length).fill(null);
      for(let i=0;i<7;i++){let off=0;for(let j=0;j<7;j++){
        for(let k=0;k<matrix[i][j];k++) {const id=lookup[i][off++];require(id!==undefined,"PATH_ASSIGNMENT");next[id]=j;}
      }require(off===lookup[i].length,"PATH_ROW_CONSERVATION");}
      for(let id=0;id<agents.length;id++){
        require(next[id]!==null,"PATH_UNASSIGNED");
        const previous=agents[id].at(-1);if(previous!==next[id])switches++;
        distance+=Math.abs(previous-next[id]);agents[id].push(next[id]);
      }
    }
    require(agents.every(p=>p.length===matrices.length+1),"PATH_LENGTH");
    return {switches,distance,agents};
  }
  require(Object.keys(TABLES).length===7,"SESSION_COUNT");
  let minTotal=0,maxTotal=0,earthTotal=0,endpointTotal=0,pairChecks=0,sourceCells=0;
  for(let g=1;g<=7;g++) {
    const T=TABLES[g],n=sizes[g-1];
    require(Array.isArray(T)&&T.length===7&&T.every(row=>Array.isArray(row)&&row.length===10),"MATRIX_SHAPE");
    const minFlows=[],maxFlows=[],earthFlows=[],d={session:g,n,minimum_changes:0,maximum_changes:0,minimum_absolute_effort_distance:0,endpoint_minimum_changes:0};
    for(let t=0;t<10;t++){
      const counts=T.map(row=>row[t]);
      require(counts.every(x=>Number.isInteger(x)&&x>=0)&&sum(counts)===n,"MARGIN_INVALID");
      sourceCells+=7;
    }
    for(let t=0;t<9;t++) {
      const a=T.map(row=>row[t]),b=T.map(row=>row[t+1]);
      const lo=sum(a.map((v,i)=>Math.max(0,v-b[i])));
      const hi=n-Math.max(0,...a.map((v,i)=>v+b[i]-n));
      const min=minCost(a,b,false),max=minCost(a,b,true),transport=earth(a,b);
      require(min.switches===lo&&max.switches===hi&&lo<=hi,"SHARP_CHANGED_BOUNDS");
      minFlows.push(min.matrix);maxFlows.push(max.matrix);earthFlows.push(transport.matrix);
      d.minimum_changes+=lo;d.maximum_changes+=hi;d.minimum_absolute_effort_distance+=transport.dist;
      byStep[t].minimum_changes+=lo;byStep[t].maximum_changes+=hi;
      byStep[t].minimum_absolute_effort_distance+=transport.dist;
      byStep[t].minimum_enter_effort1+=Math.max(0,b[6]-a[6]);
      byStep[t].minimum_exit_effort1+=Math.max(0,a[6]-b[6]);
      pairChecks++;
    }
    const first=T.map(row=>row[0]),last=T.map(row=>row[9]);
    d.endpoint_minimum_changes=sum(first.map((v,i)=>Math.max(0,v-last[i])));
    const minPaths=compose(minFlows,first),maxPaths=compose(maxFlows,first),earthPaths=compose(earthFlows,first);
    require(minPaths.switches===d.minimum_changes,"MINIMUM_PATH_CERTIFICATE");
    require(maxPaths.switches===d.maximum_changes,"MAXIMUM_PATH_CERTIFICATE");
    require(earthPaths.distance===d.minimum_absolute_effort_distance,"EARTH_PATH_CERTIFICATE");
    for(const paths of [minPaths,maxPaths,earthPaths])for(let t=0;t<10;t++)for(let action=0;action<7;action++)
      require(paths.agents.filter(p=>p[t]===action).length===T[action][t],"LONGITUDINAL_MARGINS");
    group.push(d);
    minTotal+=d.minimum_changes;maxTotal+=d.maximum_changes;earthTotal+=d.minimum_absolute_effort_distance;endpointTotal+=d.endpoint_minimum_changes;
  }
  const summed=(key)=>byStep.reduce((s,e)=>s+e[key],0);
  require(sourceCells===490&&pairChecks===63,"SOURCE_COVERAGE");
  require(minTotal===262&&maxTotal===857&&earthTotal===552&&endpointTotal===89,"FROZEN_SCOPE_RECEIPT_MISMATCH");
  require(summed("minimum_enter_effort1")===98&&summed("minimum_exit_effort1")===23,"EFFORT1_FLUX");
  return {status:"PASS_BOUNDED_SHARP_AGGREGATE_IDENTIFICATION",data_scope:"7_PUBLISHED_HUMAN_GROUP_AGGREGATE_SESSIONS_10_PERIODS",source_cells:sourceCells,independent_adjacent_pairs:pairChecks,participant_round_transitions:107*9,minimum_total_switches:minTotal,maximum_total_switches:maxTotal,minimum_absolute_effort_distance:earthTotal,endpoint_only_minimum_switches:endpointTotal,minimum_enter_effort1:summed("minimum_enter_effort1"),minimum_exit_effort1:summed("minimum_exit_effort1"),sharpness:"EXPLICIT_INTEGER_FLOW_AND_FULL_SYNTHETIC_PATH_DECOMPOSITION",session_rows:group,adjacent_period_rows:byStep,individual_real_actions_identified:false,new_E2_predictions:0,new_E3_predictions:0};
}
const result=analyze(TABLES);
const corrupted=JSON.parse(JSON.stringify(TABLES));
corrupted[1][0][1]++;
try {analyze(corrupted);throw Error("BAD_MARGINAL_ACCEPTED");}
catch (error) {if(error.message==="BAD_MARGINAL_ACCEPTED")throw error;}
result.input_git_blob_sha1=blob;
result.negative_controls=["nonconserving_count_REJECTED","source_blob_pin_REJECTS_EDITED_SOURCE"];
console.log(JSON.stringify(result,null,2));
