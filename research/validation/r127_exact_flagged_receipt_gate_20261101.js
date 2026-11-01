#!/usr/bin/env node
'use strict';
// R127 finite E1: independent integer oracle and exact two-CSV identity gate.
const fs=require('node:fs'),crypto=require('node:crypto'),path=require('node:path');
const SHA=['2a6706dcb047a5bf64f91651a8217d1d8009aa2c','07021ecb761de86d9ae71061dbd17f2f0f40dc8d'];
const HEAD='group_size,efforts,minimum,payoff_numerators';
function failIf(b,msg){if(b)throw Error(msg)}
function blob(x){return crypto.createHash('sha1').update(Buffer.from('blob '+x.length+'\0')).update(x).digest('hex')}
function expected(){const out=[];for(let n=2;n<=4;n++)for(let k=0;k<7**n;k++){
  let v=k,e=Array(n).fill(1);for(let j=n-1;j>=0;j--){e[j]=v%7+1;v=Math.floor(v/7)}
  const m=Math.min(...e);out.push([n,e.join('|'),m,e.map(z=>6+2*m-z).join('|')].join(','));
}return out}
function check(a,b,requirePinned=true){
  if(requirePinned){failIf(blob(a)!==SHA[0],'raw Git blob');failIf(blob(b)!==SHA[1],'flagged Git blob')}
  const split=x=>{const s=x.toString('utf8');failIf(!s.endsWith('\n')||s.includes('\r'),'line endings');return s.slice(0,-1).split('\n')};
  const x=split(a),y=split(b),want=expected();
  failIf(x[0]!==HEAD||y[0]!==HEAD+',exact_comparison_flag','header');
  failIf(x.length!==2794||y.length!==2794,'universe length');
  for(let i=0;i<want.length;i++)failIf(x[i+1]!==want[i]||y[i+1]!==want[i]+',PASS','row '+(i+1));
  return {status:'PASS_BOUNDED_E1',rows:2793,person_payoff_cells:10731,
    group_counts:{2:49,3:343,4:2401},raw_blob:blob(a),flag_blob:blob(b),
    evidence:'E1_ARTIFICIAL_ONLY',protocol_archive_deviation:'OPEN',new_E2:0,new_E3:0};
}
function selftest(){const r=expected(),a=Buffer.from(HEAD+'\n'+r.join('\n')+'\n'),
 b=Buffer.from(HEAD+',exact_comparison_flag\n'+r.map(z=>z+',PASS').join('\n')+'\n');
 failIf(blob(a)!==SHA[0]||blob(b)!==SHA[1],'independent full-byte reconstruction');check(a,b);
 const cases=[[Buffer.from(a.toString().replace('2,1|1,1,7|7','2,1|1,1,7|8')),b],
 [a,Buffer.from(b.toString().replace(',PASS',',FAIL'))],
 [a,Buffer.from(b.toString().replace('2,1|1,1,7|7,PASS\n',''))],
 [a,Buffer.from(b.toString().replace('2,1|2,1,7|6,PASS','2,1|1,1,7|7,PASS'))],
 [a,Buffer.from(b.toString().replace('exact_comparison_flag','flag'))],
 [a,Buffer.from(b.toString().slice(0,-1))]];
 for(let i=0;i<cases.length;i++){let rejected=false;try{check(...cases[i],false)}catch{rejected=true}failIf(!rejected,'mutation '+i+' accepted')}
 console.log(JSON.stringify({status:'PASS',full_byte_reconstruction:2,negative_controls:6,node:process.version}));
}
try{if(process.argv[2]==='--selftest')selftest();else{
 const dir=__dirname,a=process.argv[2]||path.join(dir,'R127_INTEGER_TENT_2793_PROFILES_2026-10-24.csv'),
 b=process.argv[3]||path.join(dir,'R127_INTEGER_TENT_2793_PROFILES_CI_FLAG_SUPPLEMENT_2026-10-24.csv');
 console.log(JSON.stringify(check(fs.readFileSync(a),fs.readFileSync(b))));
}}catch(e){console.error('R127_GATE_FAIL '+e.message);process.exitCode=1}
