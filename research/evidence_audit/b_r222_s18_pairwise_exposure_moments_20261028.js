#!/usr/bin/env node
"use strict";
// Independent R222 S18 B audit: combinatorial cell probabilities and pairwise moments.
const fs=require('fs'),path=require('path');

function abs(a){return a<0n?-a:a;}
function gcf(a,b){a=abs(a);b=abs(b);while(b){const r=a%b;a=b;b=r;}return a;}
class Rational{
 constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("denominator zero");if(b<0n){a=-a;b=-b;}const k=gcf(a,b);this.a=a/k;this.b=b/k;}
 plus(v){v=F(v);return new Rational(this.a*v.b+v.a*this.b,this.b*v.b);}
 times(v){v=F(v);return new Rational(this.a*v.a,this.b*v.b);}
 minus(v){v=F(v);return new Rational(this.a*v.b-v.a*this.b,this.b*v.b);}
 over(v){v=F(v);return new Rational(this.a*v.b,this.b*v.a);}
 show(){return this.b===1n?this.a.toString():this.a.toString()+"/"+this.b.toString();}
}
function F(v){if(v instanceof Rational)return v;const p=String(v).split("/");return new Rational(p[0],p[1]??1);}
const zero=F(0),one=F(1);
function load(csv){
 const lines=csv.trim().split(/\r?\n/);const header=lines.shift().split(",");const rows=lines.map(line=>{const p=line.split(",");if(p.length!==12)throw Error("csv structure");const obj={};header.forEach((h,i)=>obj[h]=p[i]);return {graph:obj.graph,mechanism:obj.mechanism,policy:obj.random_policy,edge:obj.graph_edges,z:obj.source_assignment_z.split("|").map(Number),y:obj.actual_four_individual_results.split("|").map(F),prob:F(obj.source_assignment_probability_exact)};});
 if(rows.length!==198)throw Error("expected 198 source rows");const groups=new Map();for(const r of rows){const key=[r.graph,r.mechanism,r.policy].join("|");if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r);}if(groups.size!==18)throw Error("expected 18 worlds");return groups;
}
const pairOrder=["01","02","03","12","13","23"];
function adjacency(original,regime){
 const trueEdges=original.split("|"),observed=new Set(trueEdges);
 if(regime==="DROP_FIRST_EDGE")observed.delete(trueEdges[0]);
 if(regime==="ADD_FIRST_NONEDGE"){const missing=pairOrder.find(e=>!observed.has(e));if(!missing)throw Error("missing nonedge");observed.add(missing);}
 const A=Array.from({length:4},()=>Array(4).fill(0));
 for(const edge of observed){let i=Number(edge[0]),j=Number(edge[1]);A[i][j]=1;A[j][i]=1;}
 return {A,edges:[...observed].join("|")};
}
function exposure(A,z,i){let n=0;for(let j=0;j<4;j++)n+=A[i][j]*z[j];return n;}
function assignments(policy){
 let all=[];for(let mask=0;mask<16;mask++){const z=Array.from({length:4},(_,i)=>(mask>>i)&1);if(policy==="BERNOULLI_HALF"||z.reduce((a,b)=>a+b,0)===2)all.push(z);}
 return all;
}
function calculate(csv){
 const worlds=load(csv),results=[];let sourceChecked=0;
 for(const [key,rows] of worlds){
  const [graph,mechanism,policy]=key.split("|");
  const possible=assignments(policy),expectedWeight=F(1).over(possible.length);
  const actual=new Set(rows.map(r=>r.z.join("")));
  if(rows.length!==possible.length||actual.size!==possible.length||possible.some(z=>!actual.has(z.join(""))))throw Error("incomplete source support");
  for(const r of rows){if(r.prob.show()!==expectedWeight.show())throw Error("weight mismatch");}
  sourceChecked+=rows.length;
  for(const regime of ["TRUE_GRAPH","DROP_FIRST_EDGE","ADD_FIRST_NONEDGE"]){
   const obs=adjacency(rows[0].edge,regime);
   // Compute design cell probabilities using all combinatorial assignments, independent of CSV outcome rows.
   const cells=Array.from({length:4},()=>[zero,zero]);
   for(const z of possible){for(let i=0;i<4;i++){if(exposure(obs.A,z,i)===0)cells[i][z[i]]=cells[i][z[i]].plus(expectedWeight);}}
   const valid=[0,1,2,3].filter(i=>cells[i][0].a>0n&&cells[i][1].a>0n);
   const excluded=[0,1,2,3].filter(i=>!valid.includes(i));
   let expected=null,variance=null,bias=null,mse=null;
   if(valid.length){
    // Each contribution is a design-weighted observed cell, with sign determined by own treatment.
    // Compute E(H) from individual conditional cell means; compute E(H^2) from ordered
    // pairwise cross moments, never from a per-assignment aggregate H squared.
    const contrib=rows.map(row=>valid.map(i=>{
     if(exposure(obs.A,row.z,i)!==0)return zero;
     const v=row.y[i].over(cells[i][row.z[i]]);
     return row.z[i]===1?v:zero.minus(v);
    }));
    const first=valid.map((i,a)=>rows.reduce((s,row,r)=>s.plus(row.prob.times(contrib[r][a])),zero));
    let pairSecond=zero;
    for(let a=0;a<valid.length;a++)for(let b=0;b<valid.length;b++){
     let moment=zero;
     for(let r=0;r<rows.length;r++)moment=moment.plus(rows[r].prob.times(contrib[r][a]).times(contrib[r][b]));
     pairSecond=pairSecond.plus(moment);
    }
    expected=first.reduce((s,x)=>s.plus(x),zero).over(valid.length);
    const second=pairSecond.over(valid.length*valid.length);
    variance=second.minus(expected.times(expected));
    if(variance.a<0n)throw Error("negative exact variance");
    bias=expected.minus(2);
    mse=variance.plus(bias.times(bias));
   }
   results.push({graph,mechanism,policy,observed_graph_regime:regime,observed_graph_edges:obs.edges,eligible_units:valid,excluded_units:excluded,eligible_unit_count:valid.length,zero_exposure_cell_probabilities:cells.map((x,i)=>({unit:i,p_control:x[0].show(),p_treated:x[1].show()})),expected_estimator_exact:expected?.show()??null,variance_exact:variance?.show()??null,bias_exact:bias?.show()??null,mse_exact:mse?.show()??null});
  }
 }
 return {source_worlds:worlds.size,source_rows_checked:sourceChecked,condition_count:results.length,conditions:results};
}
function audit(csv,original){
 const res=calculate(csv),index=new Map(original.conditions.map(x=>[[x.graph,x.mechanism,x.policy,x.observed_graph_regime].join("|"),x]));
 let checks=0;const errors=[];
 for(const row of res.conditions){
  const key=[row.graph,row.mechanism,row.policy,row.observed_graph_regime].join("|");
  const target=index.get(key);if(!target){errors.push("missing condition "+key);continue;}
  for(const field of ["eligible_unit_count","expected_estimator_exact","variance_exact","bias_exact","mse_exact","observed_graph_edges"]){
   checks++;if(row[field]!==target[field])errors.push(key+" "+field);
  }
  for(const field of ["eligible_units","excluded_units"]){checks++;if(JSON.stringify(row[field])!==JSON.stringify(target[field]))errors.push(key+" "+field);}
  for(let i=0;i<4;i++)for(const field of ["p_control","p_treated"]){checks++;if(row.zero_exposure_cell_probabilities[i][field]!==target.zero_exposure_cell_probabilities[i][field])errors.push(key+" unit"+i+" "+field);}
 }
 if(res.condition_count!==54||res.source_rows_checked!==198)errors.push("source count");
 return {comparison_count:checks,errors,conditions_checked:res.condition_count,source_rows_checked:res.source_rows_checked,results:res};
}

const csv=fs.readFileSync(path.resolve(__dirname,'../R222/R222_ALL_198_ORIGINAL_NETWORK_ASSIGNMENT_SOURCES.csv'),'utf8');
const original=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../validation/R222_S18_NETWORK_EDGE_ERROR_54_CONDITION_EXACT_RECEIPT_2026-10-28.json'),'utf8'));
const result=audit(csv,original);
if(result.errors.length)throw Error('independent mismatch: '+result.errors.slice(0,8).join('; '));
process.stdout.write(JSON.stringify({status:'PASS',comparison_count:result.comparison_count,conditions_checked:result.conditions_checked,source_rows_checked:result.source_rows_checked},null,2)+'\n');
