#!/usr/bin/env node
'use strict';
/* R253 S49 exact prefix Brier risk, original 4608 artificial sources only.
   Run: node research/validation/r253_s49_prefix_theta_brier_source_20261029.js
   Optional: node <script> <path/to/original/R253_ALL_4608_...csv>
   Node builtins only; no network, external packages or paid compute.
*/
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const WORLDS = [
 'BAYESIAN_CASCADE_Q34','PRIVATE_ONLY_Q34','FIRST_ACTION_IMITATION_Q34',
 'BAYESIAN_CASCADE_FAIR_Q12','HARD_CODED_CASCADE_ALIAS_Q34',
 'INVERTED_SIGNALS_Q14_BAYES','PERFECT_PRIVATE_Q1',
 'STATIC_TRUE_PRIVATE_CASCADE_REPORT_ALIAS_Q34','COMMON_SIGNAL_NO_SOCIAL_Q34'
];
const EXPECTED_SHA256='42e19a1d3f8a70ded77b3634d4b48eb8a3326eab0bda2f8b5a5ece3bf0b54d45';
function requireTrue(x,msg){if(!x)throw new Error(msg);}
function gcd(a,b){while(b){let c=a%b;a=b;b=c;}return a;}
function frac(a,b=1n){a=BigInt(a);b=BigInt(b);requireTrue(b!==0n,'zero denominator');if(b<0n){a=-a;b=-b;}let g=gcd(a<0n?-a:a,b);return [a/g,b/g];}
function plus(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function minus(a,b){return frac(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function repr(a){return a[1]===1n?String(a[0]):String(a[0])+'/'+String(a[1]);}
function compare(a,b){return a[0]*b[1]===b[0]*a[1];}
function expectedActions(w,s){
 if(w==='PRIVATE_ONLY_Q34'||w==='BAYESIAN_CASCADE_FAIR_Q12')return s;
 if(w==='FIRST_ACTION_IMITATION_Q34'||w==='COMMON_SIGNAL_NO_SOCIAL_Q34')return [s[0],s[0],s[0],s[0]];
 if(w==='INVERTED_SIGNALS_Q14_BAYES')s=s.map(v=>1-v);
 return s[0]===s[1]?[s[0],s[1],s[0],s[0]]:s;
}
function main(){
 const input=process.argv[2]||path.join(__dirname,'..','R253','R253_ALL_4608_ORIGINAL_FOUR_AGENT_SIGNAL_SOURCES.csv');
 const buf=fs.readFileSync(input), sha=crypto.createHash('sha256').update(buf).digest('hex');
 requireTrue(sha===EXPECTED_SHA256,'original R253 source SHA256 mismatch');
 const lines=buf.toString('utf8').trimEnd().split('\n'),headers=lines[0].split(',');
 requireTrue(lines.length===4609,'expected 4608 data records');
 const required=['world','oracle_true_state_theta','original_full_ninebit_source_probability'];
 for(let i=1;i<=4;i++)required.push('observed_public_action_Y'+i,'oracle_private_signal_S'+i,'oracle_true_hidden_action_H'+i,'oracle_original_signal_R'+i+'1','oracle_original_signal_R'+i+'2');
 for(const key of required)requireTrue(headers.includes(key),'missing field '+key);
 const records=new Map(WORLDS.map(w=>[w,[]]));
 for(const [lineNo,line] of lines.slice(1).entries()){
  const values=line.split(',');requireTrue(values.length===headers.length,'column width '+(lineNo+2));
  const r=Object.fromEntries(headers.map((h,i)=>[h,values[i]]));
  requireTrue(records.has(r.world),'unexpected world '+r.world);
  requireTrue(r.original_full_ninebit_source_probability==='1/512','source mass');
  const bits=[Number(r.oracle_true_state_theta)];
  for(let i=1;i<=4;i++)for(let j=1;j<=2;j++)bits.push(Number(r['oracle_original_signal_R'+i+j]));
  requireTrue(bits.length===9&&bits.every(v=>v===0||v===1),'invalid original bit');
  const theta=bits[0],q=r.world==='BAYESIAN_CASCADE_FAIR_Q12'?2:r.world==='INVERTED_SIGNALS_Q14_BAYES'?1:r.world==='PERFECT_PRIVATE_Q1'?4:3;
  const s=[];
  for(let i=0;i<4;i++){
   let b=2*bits[1+2*i]+bits[2+2*i];let sig=b<q?theta:1-theta;
   requireTrue(Number(r['oracle_private_signal_S'+(i+1)])===sig,'private signal mismatch');s.push(sig);
  }
  const a=expectedActions(r.world,s);
  for(let i=0;i<4;i++){
   requireTrue(Number(r['observed_public_action_Y'+(i+1)])===a[i],'public action mismatch');
   let hidden=r.world==='STATIC_TRUE_PRIVATE_CASCADE_REPORT_ALIAS_Q34'?s[i]:a[i];
   requireTrue(Number(r['oracle_true_hidden_action_H'+(i+1)])===hidden,'hidden action mismatch');
  }
  const key=bits.join('');records.get(r.world).push({key,theta,public:a});
 }
 const worldResults=[];
 for(const w of WORLDS){
  const rows=records.get(w);requireTrue(rows.length===512,'source count '+w);
  const unique=new Set(rows.map(r=>r.key));requireTrue(unique.size===512,'duplicate original source '+w);
  const risks=[];
  for(let k=0;k<=4;k++){
   const groups=new Map();
   for(const row of rows){let key=row.public.slice(0,k).join('');let n=groups.get(key)||[0,0];n[row.theta]++;groups.set(key,n);}
   let risk=frac(0n);
   for(const [n0,n1] of groups.values())risk=plus(risk,frac(BigInt(n0*n1),BigInt(512*(n0+n1))));
   risks.push(risk);
  }
  requireTrue(compare(risks[0],frac(1n,4n)),'wrong prior');
  const gains=risks.slice(1).map((v,i)=>minus(risks[i],v));
  requireTrue(gains.every(x=>x[0]>=0n),'negative information value');
  worldResults.push({world:w,risks:risks.map(repr),gains:gains.map(repr)});
 }
 for(const idx of [4,7])requireTrue(JSON.stringify(worldResults[idx].risks)===JSON.stringify(worldResults[0].risks),'Bayes alias mismatch');
 requireTrue(JSON.stringify(worldResults[2].risks)===JSON.stringify(worldResults[8].risks),'imitation alias mismatch');
 // The illegal oracle theta predictor is perfect by identity; never report it as a legal forecast.
 for(const rows of records.values())for(const r of rows)requireTrue((r.theta-r.theta)**2===0,'leakage negative');
 const out={research:'R253_S49',protocol:'protocols/R253_S49_PREFIX_THETA_BRIER_PRESCORE_FREEZE_2026-10-29.md',
  evidence:'E1_ONLY',original_source_sha256:sha,original_source_records:4608,
  worlds:9,risk_cells:45,gain_cells:36,leaked_theta_oracle_risk:'0',
  formal_R253_acceptance_unchanged:true,R073:'FROZEN',PESEN_v0_1:'FROZEN',world_results:worldResults};
 process.stdout.write(JSON.stringify(out,null,2)+'\n');
}
if(require.main===module)main();
