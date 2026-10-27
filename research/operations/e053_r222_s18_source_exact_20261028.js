#!/usr/bin/env node
"use strict";
// E053 independent exact arithmetic audit. Requires Node.js standard library only.
// Usage: node e053_r222_s18_source_exact_20261028.js ORIGINAL.csv S18_RECEIPT.json
const fs = require("node:fs");
if (process.argv.length !== 4) {
  console.error("Usage: node e053_r222_s18_source_exact_20261028.js ORIGINAL.csv S18_RECEIPT.json");
  process.exit(2);
}
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;};
const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
const P=v=>{const [a,b="1"]=String(v).split("/");return Q(a,b);};
const plus=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const minus=(x,y)=>plus(x,[-y[0],y[1]]);
const times=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
const over=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
const equal=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const lines=fs.readFileSync(process.argv[2],"utf8").trim().split(/\r?\n/);
const header=lines.shift().split(",");
const rows=lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[header[i],v])));
const receipt=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));
const worlds=new Map();
for(const row of rows){const key=[row.graph,row.mechanism,row.random_policy].join("|");if(!worlds.has(key))worlds.set(key,[]);worlds.get(key).push(row);}
let checks=0;const failures=[];let nulls=0;
function check(ok,context){checks++;if(!ok&&failures.length<30)failures.push(context);}
for(const [key,world] of worlds){
  let mass=Q(0);
  for(const row of world){
    mass=plus(mass,P(row.source_assignment_probability_exact));
    const z=row.source_assignment_z.split("|").map(Number);
    const e=row.actual_four_neighbor_exposure_counts.split("|").map(Number);
    const y=row.actual_four_individual_results.split("|").map(Number);
    const m=row.mechanism,gamma=m==="LINEAR_SPILL"?2:m==="INTERACTION_SPILL"?1:0,delta=m==="INTERACTION_SPILL"?2:0;
    for(let i=0;i<4;i++)check(y[i]===i+2*z[i]+gamma*e[i]+delta*z[i]*e[i],"source "+key+" "+row.source_assignment_z+" i"+i);
  }
  check(equal(mass,Q(1)),"mass "+key);
}
for(const c of receipt.conditions){
  const label=[c.graph,c.mechanism,c.policy,c.observed_graph_regime].join("|");
  const world=worlds.get([c.graph,c.mechanism,c.policy].join("|"));
  check(world.length===c.original_assignment_count,"count "+label);
  const edges=c.observed_graph_edges.split("|").filter(Boolean).map(s=>[Number(s[0]),Number(s[1])]);
  const data=world.map(row=>{
    const z=row.source_assignment_z.split("|").map(Number),y=row.actual_four_individual_results.split("|").map(Number),e=[0,0,0,0];
    for(const [i,j] of edges){e[i]+=z[j];e[j]+=z[i];}
    return {z,y,e,p:P(row.source_assignment_probability_exact)};
  });
  const p=Array.from({length:4},()=>[Q(0),Q(0)]);
  for(const d of data)for(let i=0;i<4;i++)if(d.e[i]===0)p[i][d.z[i]]=plus(p[i][d.z[i]],d.p);
  const eligible=[0,1,2,3].filter(i=>p[i][0][0]>0n&&p[i][1][0]>0n);
  const excluded=[0,1,2,3].filter(i=>!eligible.includes(i));
  check(JSON.stringify(eligible)===JSON.stringify(c.eligible_units),"eligible "+label);
  check(JSON.stringify(excluded)===JSON.stringify(c.excluded_units),"excluded "+label);
  check(eligible.length===c.eligible_unit_count,"eligible count "+label);
  for(let i=0;i<4;i++){
    check(equal(p[i][0],P(c.zero_exposure_cell_probabilities[i].p_control)),"p0 "+label+" i"+i);
    check(equal(p[i][1],P(c.zero_exposure_cell_probabilities[i].p_treated)),"p1 "+label+" i"+i);
  }
  if(eligible.length===0){
    nulls++;
    for(const field of ["expected_estimator_exact","variance_exact","bias_exact","mse_exact"])check(c[field]===null,"null "+field+" "+label);
    continue;
  }
  let E=Q(0),E2=Q(0),MSE=Q(0);
  for(const d of data){
    let H=Q(0);
    for(const i of eligible){
      if(d.e[i]!==0)continue;
      const term=over(Q(d.y[i]),p[i][d.z[i]]);
      H=plus(H,d.z[i]===1?term:[-term[0],term[1]]);
    }
    H=over(H,Q(eligible.length));
    E=plus(E,times(d.p,H));
    E2=plus(E2,times(d.p,times(H,H)));
    const err=minus(H,Q(2));
    MSE=plus(MSE,times(d.p,times(err,err)));
  }
  const variance=minus(E2,times(E,E)),bias=minus(E,Q(2));
  for(const [field,val] of [["expected_estimator_exact",E],["variance_exact",variance],["bias_exact",bias],["mse_exact",MSE]])
    check(equal(P(c[field]),val),field+" "+label);
}
const output={checks,failures,source_rows:rows.length,worlds:worlds.size,conditions:receipt.conditions.length,zero_support:nulls,exact:true};
console.log(JSON.stringify(output,null,2));
if(failures.length||checks!==1674||rows.length!==198||worlds.size!==18||receipt.conditions.length!==54||nulls!==6)process.exit(1);
