#!/usr/bin/env node
'use strict';
// R319 S115: exact synthetic repeated-choice panels. No real human observations.
const fs = require('fs');
const path = require('path');
const gcd = (a,b) => { a=a<0n?-a:a; b=b<0n?-b:b; while(b){const t=a%b;a=b;b=t;}return a||1n; };
const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};};
const add=(a,b)=>F(a.n*b.d+b.n*a.d,a.d*b.d);
const neg=a=>F(-a.n,a.d);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>F(a.n*b.n,a.d*b.d);
const div=(a,b)=>F(a.n*b.d,a.d*b.n);
const abs=a=>F(a.n<0n?-a.n:a.n,a.d);
const sum=xs=>xs.reduce(add,F(0));
const str=a=>a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);
const power=x=>x>=0?F(2n**BigInt(x)):F(1n,2n**BigInt(-x));
const sets=[[0,1],[0,1,2],[0,1,1],[0,2,1],[0,2,2]];
const qs=[F(1,4),F(1,2),F(3,4)];
const conditional=(beta,xs)=>{const w=xs.map(x=>power(beta*x));const z=sum(w);return w.map(x=>div(x,z));};
function generate(){
  const rows=[],worlds=[];
  for(let s=0;s<sets.length;s++)for(let qi=0;qi<qs.length;qi++){
    const xs=sets[s],q=qs[qi],r=sub(F(1),q),wid=s*3+qi;
    const pp=conditional(1,xs),pm=conditional(-1,xs);
    const marg=xs.map((_,j)=>add(mul(q,pp[j]),mul(r,pm[j])));
    const joints={PERSISTENT:[],REDRAW:[]};
    for(const mechanism of ['PERSISTENT','REDRAW'])for(let j=0;j<xs.length;j++)for(let k=0;k<xs.length;k++){
      const p=mechanism==='PERSISTENT'?add(mul(q,mul(pp[j],pp[k])),mul(r,mul(pm[j],pm[k]))):mul(marg[j],marg[k]);
      joints[mechanism].push(p);
      rows.push([wid,"S"+s,xs.join('|'),str(q),mechanism,j,k,str(p)]);
    }
    if(str(sum(joints.PERSISTENT))!=='1'||str(sum(joints.REDRAW))!=='1')throw Error('joint mass');
    const diffs=joints.PERSISTENT.map((p,i)=>sub(p,joints.REDRAW[i]));
    const tv=div(sum(diffs.map(abs)),F(2));
    for(let j=0;j<xs.length;j++)for(let k=0;k<xs.length;k++){
      const identity=mul(mul(q,r),mul(sub(pp[j],pm[j]),sub(pp[k],pm[k])));
      if(str(identity)!==str(diffs[j*xs.length+k]))throw Error('covariance identity');
    }
    for(const mech of ['PERSISTENT','REDRAW'])for(let j=0;j<xs.length;j++){
      const a=sum(joints[mech].slice(j*xs.length,(j+1)*xs.length));
      const b=sum(joints[mech].filter((_,i)=>i%xs.length===j));
      if(str(a)!==str(marg[j])||str(b)!==str(marg[j]))throw Error('marginal mismatch');
    }
    worlds.push({world_id:wid,choice_set_id:"S"+s,features:xs,q_plus:str(q),marginal_probabilities:marg.map(str),tv_distance:str(tv),equal_prior_bayes_accuracy:str(div(add(F(1),tv),F(2)))});
  }
  if(rows.length!==240||worlds.length!==15)throw Error('universe size');
  const header='world_id,choice_set_id,features,q_plus,mechanism,choice_t1,choice_t2,joint_probability';
  const csv=header+'\n'+rows.map(row=>row.join(',')).join('\n')+'\n';
  const summary={schema:'r319_s115_two_occasion_persistence_e1_v1',original_model:'R319',original_catalogue_id:'01-007',synthetic_only:true,source_worlds:15,ordered_joint_cells:240,mechanisms:['PERSISTENT','REDRAW'],worlds};
  return {csv,json:JSON.stringify(summary,null,2)+'\n',summary};
}
function main(){
  const result=generate();
  if(process.argv.includes('--emit')){
    const i=process.argv.indexOf('--out-dir');
    if(i<0||!process.argv[i+1])throw Error('explicit --out-dir required');
    const out=process.argv[i+1];fs.mkdirSync(out,{recursive:true});
    fs.writeFileSync(path.join(out,'R319_S115_ALL_240_PANEL_JOINT_CELLS.csv'),result.csv);
    fs.writeFileSync(path.join(out,'R319_S115_EXACT_PANEL_SUMMARY.json'),result.json);
  }else if(process.argv.includes('--audit')){
    const root=path.resolve(__dirname);
    if(fs.readFileSync(path.join(root,'R319_S115_ALL_240_PANEL_JOINT_CELLS.csv'),'utf8')!==result.csv)throw Error('CSV byte mismatch');
    if(fs.readFileSync(path.join(root,'R319_S115_EXACT_PANEL_SUMMARY.json'),'utf8')!==result.json)throw Error('JSON byte mismatch');
  }
  const crypto=require('crypto');
  process.stdout.write(JSON.stringify({worlds:15,cells:240,sha256_csv:crypto.createHash('sha256').update(result.csv).digest('hex'),sha256_json:crypto.createHash('sha256').update(result.json).digest('hex'),s0_half:result.summary.worlds[1],s4_half:result.summary.worlds[13]})+'\n');
}
if(require.main===module)main();
module.exports={generate};
