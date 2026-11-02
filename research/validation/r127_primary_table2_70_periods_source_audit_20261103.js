#!/usr/bin/env node
"use strict";
/*
 R127 source-table audit. Counts manually transcribed from the 1990 AER
 scan, printed pp.240-241, Table 2, Treatment A, seven experiments.
 Rows are efforts 7,6,5,4,3,2,1; columns are periods 1..10.
 This does not reconstruct participant trajectories or independently
 authenticate every cell against a second scan reader.
*/
const TABLES = {
1:[[8,1,1,0,0,0,0,0,0,1],[3,2,1,0,0,0,0,0,0,0],[2,3,2,1,0,0,1,0,0,0],[1,6,5,4,1,1,1,0,0,0],[1,2,5,5,4,1,1,1,0,1],[1,2,2,4,8,7,8,6,4,1],[0,0,0,2,3,7,5,9,12,13]],
2:[[4,0,1,0,0,0,0,0,0,1],[1,0,1,0,0,1,0,0,0,0],[3,3,2,1,0,0,1,1,0,1],[4,6,2,3,3,0,0,0,0,0],[1,4,2,5,0,1,1,0,1,0],[3,2,6,5,5,9,3,4,3,1],[0,1,2,2,8,5,11,11,12,13]],
3:[[4,4,1,0,1,1,1,0,0,2],[2,0,2,0,0,0,0,0,0,0],[5,6,1,1,1,0,0,0,0,0],[3,3,2,1,2,1,0,0,0,1],[0,0,7,6,0,2,3,0,0,0],[0,1,1,4,5,3,6,3,2,2],[0,0,0,2,5,7,4,11,12,9]],
4:[[6,0,1,1,0,0,1,0,0,0],[0,6,2,0,0,1,0,0,0,0],[8,5,5,5,0,1,0,0,0,0],[1,1,4,6,7,1,2,1,1,0],[0,2,3,2,4,3,2,2,1,0],[0,1,0,0,2,3,7,4,2,2],[0,0,0,1,2,6,3,8,11,13]],
5:[[2,2,3,1,1,1,1,0,0,0],[1,3,1,0,0,0,0,0,0,0],[9,3,0,4,1,0,2,0,0,0],[3,4,6,2,1,2,0,2,1,1],[1,2,2,4,6,0,0,0,0,1],[0,2,2,3,4,6,5,2,5,3],[0,0,2,2,3,7,8,12,10,11]],
6:[[5,3,1,1,1,1,2,2,2,3],[2,0,0,0,1,0,0,0,0,0],[5,1,0,0,0,1,0,0,0,0],[2,3,4,0,0,0,0,0,0,0],[1,5,4,2,2,2,1,0,2,0],[0,2,4,5,3,3,6,4,5,5],[1,2,3,8,9,9,7,10,7,8]],
7:[[4,3,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0],[4,0,1,2,1,0,0,0,0,0],[1,3,2,1,1,0,0,0,0,0],[1,3,2,2,4,4,4,4,5,3],[1,2,8,8,7,9,9,9,8,10]]
};
const SIZES = [16,16,14,15,16,16,14];
const ENDPOINTS = {
1:[[8,3,2,1,1,1,0],[1,0,0,0,1,1,13]],
2:[[4,1,3,4,1,3,0],[1,0,1,0,0,1,13]],
3:[[4,2,5,3,0,0,0],[2,0,0,1,0,2,9]],
4:[[6,0,8,1,0,0,0],[0,0,0,0,0,2,13]],
5:[[2,1,9,3,1,0,0],[0,0,0,1,1,3,11]],
6:[[5,2,5,2,1,0,1],[3,0,0,0,0,5,8]],
7:[[4,1,2,4,1,1,1],[1,0,0,0,0,3,10]]
};
const PRINTED_MINIMUMS = {
1:[2,2,2,1,1,1,1,1,1,1],
2:[2,1,1,1,1,1,1,1,1,1],
3:[4,2,2,1,1,1,1,1,1,1],
4:[4,2,3,1,1,1,1,1,1,1],
5:[3,2,1,1,1,1,1,1,1,1],
6:[1,1,1,1,1,1,1,1,1,1],
7:[1,1,1,1,1,1,1,1,1,1]
};
function insist(condition, message) {
  if (!condition) throw new Error(message);
}
function audit(tables=TABLES, sizes=SIZES, endpoints=ENDPOINTS, minimums=PRINTED_MINIMUMS) {
  insist(Object.keys(tables).length === 7, "experiment universe");
  let period1_sevens=0, period1_ones=0, period10_ones=0;
  let period_ones=Array(10).fill(0), period_weighted_effort=Array(10).fill(0);
  for (let experiment=1; experiment<=7; experiment++) {
    const rows=tables[experiment], n=sizes[experiment-1];
    insist(Number.isInteger(n) && n>=2, "group size");
    insist(Array.isArray(rows) && rows.length===7, "effort universe");
    insist(rows.every(r=>Array.isArray(r)&&r.length===10), "period universe");
    for(let period=0;period<10;period++){
      const col=rows.map(r=>r[period]);
      insist(col.every(v=>Number.isSafeInteger(v)&&v>=0), "nonnegative integer count");
      insist(col.reduce((a,b)=>a+b,0)===n, "group-period count");
      const min=7-col.findLastIndex(v=>v>0);
      insist(min===minimums[experiment][period], "printed minimum mismatch");
      if(period===0||period===9){
        const expected=endpoints[experiment][period===0?0:1];
        insist(JSON.stringify(col)===JSON.stringify(expected), "frozen endpoint mismatch");
      }
      period_ones[period]+=col[6];
      period_weighted_effort[period]+=col.reduce((a,b,i)=>a+b*(7-i),0);
    }
    period1_sevens+=rows[0][0];period1_ones+=rows[6][0];period10_ones+=rows[6][9];
  }
  insist(sizes.reduce((a,b)=>a+b,0)===107, "total subjects");
  insist(period1_sevens===33 && period1_ones===2 && period10_ones===77, "published text margins");
  return {
    status:"PASS_BOUNDED_SOURCE_TRANSCRIPTION_CONSISTENCY",
    source:"Van Huyck et al. AER 1990 printed pp.240-241 Table 2",
    printed_cells:490, session_period_columns:70,
    group_period_sum_checks:70, printed_minimum_checks:70,
    frozen_endpoint_vectors_checked:14,
    new_middle_period_columns:56,
    published_subjects:107, first_period_7:period1_sevens,
    first_period_1:period1_ones, tenth_period_1:period10_ones,
    count_effort1_by_period:period_ones,
    effort_sum_by_period:period_weighted_effort,
    individual_transitions_identified:false,
    independent_second_reader:false, new_E2:0, new_E3:0
  };
}
function run(){
  const positive=audit();
  let rejects=0;
  for(let case_id=0;case_id<6;case_id++){
    const x=JSON.parse(JSON.stringify(TABLES));
    const sizes=SIZES.slice();
    const mins=JSON.parse(JSON.stringify(PRINTED_MINIMUMS));
    if(case_id===0)x[1][0][0]=-1;
    if(case_id===1)x[1][0].pop();
    if(case_id===2)x[1][0][3]+=1;
    if(case_id===3){x[1][0][0]--;x[1][1][0]++;}
    if(case_id===4)mins[1][0]=1;
    if(case_id===5)sizes[1]=17;
    try{audit(x,sizes,ENDPOINTS,mins);}catch(error){rejects++;}
  }
  insist(rejects===6,"negative controls must all reject");
  return {...positive,negative_controls_rejected:rejects,
    execution:"deterministic JavaScript integer sums",
    random_seed:"N/A"};
}
if(typeof process!=="undefined" && typeof require!=="undefined" && require.main===module){
  console.log(JSON.stringify(run(),null,2));
}
