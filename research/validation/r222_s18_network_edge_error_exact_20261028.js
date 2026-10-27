#!/usr/bin/env node
"use strict";
// R222 S18. Node.js standard library only. Exact rational arithmetic; original CSV is immutable.
const fs=require('fs'),path=require('path');

function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
class Q{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(b){b=q(b);return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
 sub(b){b=q(b);return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
 mul(b){b=q(b);return new Q(this.n*b.n,this.d*b.d);}
 div(b){b=q(b);return new Q(this.n*b.d,this.d*b.n);}
 eq(b){b=q(b);return this.n===b.n&&this.d===b.d;}
 str(){return this.d===1n?String(this.n):String(this.n)+"/"+String(this.d);}
}
function q(x){if(x instanceof Q)return x;let s=String(x).split("/");return new Q(BigInt(s[0]),s.length===2?BigInt(s[1]):1n);}
const ZERO=q(0),ONE=q(1),TWO=q(2);
function parse(csv){
 const lines=csv.trim().split(/\r?\n/),header=lines.shift().split(",");
 if(lines.length!==198)throw Error("source count "+lines.length);
 const out=lines.map(line=>{const fields=line.split(",");if(fields.length!==header.length)throw Error("csv fields");const o={};header.forEach((h,i)=>o[h]=fields[i]);o.z=o.source_assignment_z.split("|").map(Number);o.y=o.actual_four_individual_results.split("|").map(q);o.w=q(o.source_assignment_probability_exact);return o;});
 const groups={};for(const row of out){let key=[row.graph,row.mechanism,row.random_policy].join("|");(groups[key]??=[]).push(row);}
 if(Object.keys(groups).length!==18)throw Error("world count");return groups;
}
const pairs=["01","02","03","12","13","23"];
function edges(original,regime){let es=original.split("|");if(regime==="DROP_FIRST_EDGE")es=es.slice(1);else if(regime==="ADD_FIRST_NONEDGE"){const e=pairs.find(x=>!es.includes(x));if(!e)throw Error("no missing edge");es.push(e);}else if(regime!=="TRUE_GRAPH")throw Error("regime");return es;}
function exposures(z,es){let e=[0,0,0,0];for(const edge of es){const a=+edge[0],b=+edge[1];e[a]+=z[b];e[b]+=z[a];}return e;}
function compute(csv){
 const groups=parse(csv),conditions=[],controls={no_spill:0,add_or_true:0,linear_bernoulli_drop:0,interaction_bernoulli_drop_positive:0,zero_support_conditions:0,source_rows:0};
 for(const [key,rows] of Object.entries(groups)){
  const [graph,mechanism,policy]=key.split("|");const nExpected=policy==="BERNOULLI_HALF"?16:6;
  if(rows.length!==nExpected)throw Error("world row count "+key);
  let mass=ZERO;const seen=new Set();
  for(const r of rows){mass=mass.add(r.w);let z=r.z.join("");if(seen.has(z))throw Error("duplicate assignment");seen.add(z);if(!r.w.eq(q(1).div(nExpected)))throw Error("source probability");}
  if(!mass.eq(ONE))throw Error("mass");controls.source_rows+=rows.length;
  for(const regime of ["TRUE_GRAPH","DROP_FIRST_EDGE","ADD_FIRST_NONEDGE"]){
   const observedEdges=edges(rows[0].graph_edges,regime),p=Array.from({length:4},()=>[ZERO,ZERO]);
   for(const r of rows){const e=exposures(r.z,observedEdges);for(let i=0;i<4;i++)if(e[i]===0)p[i][r.z[i]]=p[i][r.z[i]].add(r.w);}
   const eligible=[0,1,2,3].filter(i=>p[i][0].n>0n&&p[i][1].n>0n);
   const excluded=[0,1,2,3].filter(i=>!eligible.includes(i));
   let mean=null,variance=null,bias=null,mse=null;
   if(eligible.length){
    const scores=rows.map(r=>{const e=exposures(r.z,observedEdges);let h=ZERO;for(const i of eligible){if(e[i]===0){const t=r.z[i];h=h.add((t===1?r.y[i]:ZERO.sub(r.y[i])).div(p[i][t]));}}return [r.w,h.div(eligible.length)];});
    mean=scores.reduce((s,[w,h])=>s.add(w.mul(h)),ZERO);
    variance=scores.reduce((s,[w,h])=>s.add(w.mul(h.sub(mean).mul(h.sub(mean)))),ZERO);
    bias=mean.sub(TWO);
    mse=scores.reduce((s,[w,h])=>s.add(w.mul(h.sub(TWO).mul(h.sub(TWO)))),ZERO);
    if(!mse.eq(variance.add(bias.mul(bias))))throw Error("MSE identity");
    if(mechanism==="NO_SPILL"){if(!bias.eq(ZERO))throw Error("no spill control");controls.no_spill++;}
    if(regime!=="DROP_FIRST_EDGE"){if(!bias.eq(ZERO))throw Error("observed supergraph control");controls.add_or_true++;}
    if(mechanism==="LINEAR_SPILL"&&policy==="BERNOULLI_HALF"&&regime==="DROP_FIRST_EDGE"){if(!bias.eq(ZERO))throw Error("linear Bernoulli control");controls.linear_bernoulli_drop++;}
    if(mechanism==="INTERACTION_SPILL"&&policy==="BERNOULLI_HALF"&&regime==="DROP_FIRST_EDGE"&&bias.n>0n)controls.interaction_bernoulli_drop_positive++;
   }else controls.zero_support_conditions++;
   conditions.push({graph,mechanism,policy,observed_graph_regime:regime,observed_graph_edges:observedEdges.join("|"),original_assignment_count:rows.length,eligible_units:eligible,excluded_units:excluded,eligible_unit_count:eligible.length,zero_exposure_cell_probabilities:p.map((v,i)=>({unit:i,p_control:v[0].str(),p_treated:v[1].str()})),true_no_treated_neighbor_direct_effect:"2",expected_estimator_exact:mean?.str()??null,variance_exact:variance?.str()??null,bias_exact:bias?.str()??null,mse_exact:mse?.str()??null});
  }
 }
 if(conditions.length!==54||controls.source_rows!==198||controls.no_spill===0||controls.add_or_true===0||controls.linear_bernoulli_drop===0||controls.interaction_bernoulli_drop_positive===0)throw Error("frozen controls incomplete");
 return {research_id:"R222_S18",evidence_class:"E1_ARTIFICIAL",source_path:"research/R222/R222_ALL_198_ORIGINAL_NETWORK_ASSIGNMENT_SOURCES.csv",source_git_blob:"5100af6615ff5a8fe8e9ad2702dfa4227aa6c0bc",source_worlds:18,source_assignment_rows:198,condition_count:54,control_checks:controls,scoring_target:"true graph zero treated neighbor controlled direct effect tau=2; supported units only",conditions};
}

const input=path.resolve(__dirname,'../R222/R222_ALL_198_ORIGINAL_NETWORK_ASSIGNMENT_SOURCES.csv');
const result=compute(fs.readFileSync(input,'utf8'));
process.stdout.write(JSON.stringify(result,null,2)+'\n');
