#!/usr/bin/env node
'use strict';
// R312 S108 two-step exact integer-grid generator; all opinion values in units 1/32.
const fs=require('fs');
const PROFILES={"A":[0,0,0,0],"B":[0,0,0,16],"C":[0,0,16,32],"D":[0,16,16,32],"E":[0,0,32,32],"F":[0,16,32,32],"G":[16,16,16,32],"H":[32,32,32,32]};
const EPS=[0,16,32],MUS=[1,2],PAIRS=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b];}return a||1;}
function frac(n,d=1){if(!Number.isInteger(n)||!Number.isInteger(d)||d<=0)throw Error('noninteger rational');const g=gcd(n,d);n/=g;d/=g;return d===1?String(n):`${n}/${d}`;}
function opinion(x){return frac(x,32);}
function Dnum(x){const s=x.reduce((a,b)=>a+b,0);return 4*x.reduce((a,b)=>a+b*b,0)-s*s;}
function step(x,eps,mu,p){const y=x.slice(),[i,j]=p;if(Math.abs(x[i]-x[j])<=eps){const di=mu*(x[j]-x[i]),dj=mu*(x[i]-x[j]);if(di%4||dj%4)throw Error('grid not exact');y[i]+=di/4;y[j]+=dj/4;}if(y.reduce((a,b)=>a+b,0)!==x.reduce((a,b)=>a+b,0))throw Error('mean changed');return y;}
function generate(){
 const header='world,profile,epsilon,mu,first_i,first_j,second_i,second_j,first_eligible,second_eligible,initial_opinions,after_first,after_second,D0,D1_path,D2_path';
 const rows=[header],summaries=[];
 let totalOrders=0,changedOrders=0,strict1=0,strict2=0,zero2=0,distinctMin=100,distinctMax=0,strictExample=null,orderExample=null;
 for(const [name,initial] of Object.entries(PROFILES))for(const eps of EPS)for(const mu of MUS){
  const wid=`profile=${name}|eps=${frac(eps,32)}|mu=${frac(mu,4)}`;
  const d0=Dnum(initial),one=PAIRS.map(p=>step(initial,eps,mu,p)),d1sum=one.reduce((s,x)=>s+Dnum(x),0);
  let d2sum=0,states=new Set(),worldOrder=0;
  for(let a=0;a<6;a++)for(let b=0;b<6;b++){
   const x1=one[a],x2=step(x1,eps,mu,PAIRS[b]);d2sum+=Dnum(x2);states.add(x2.join(';'));
   rows.push([wid,name,frac(eps,32),frac(mu,4),...PAIRS[a],...PAIRS[b],Math.abs(initial[PAIRS[a][0]]-initial[PAIRS[a][1]])<=eps,Math.abs(x1[PAIRS[b][0]]-x1[PAIRS[b][1]])<=eps,initial.map(opinion).join(';'),x1.map(opinion).join(';'),x2.map(opinion).join(';'),frac(d0,4096),frac(Dnum(x1),4096),frac(Dnum(x2),4096)].join(','));
  }
  if(6*d0<d1sum||6*d1sum<d2sum)throw Error('expected dispersion increased');
  if(6*d0>d1sum)strict1++;if(6*d1sum>d2sum)strict2++;else zero2++;
  for(let a=0;a<6;a++)for(let b=a+1;b<6;b++){
   totalOrders++;const ab=step(one[a],eps,mu,PAIRS[b]),ba=step(one[b],eps,mu,PAIRS[a]);
   if(ab.join(';')!==ba.join(';')){worldOrder++;changedOrders++;if(!orderExample)orderExample={world:wid,first_then_second:[PAIRS[a],PAIRS[b]],result_ab:ab.map(opinion),result_ba:ba.map(opinion)};}
  }
  if(!strictExample&&6*d1sum>d2sum)strictExample={world:wid,D0:frac(d0,4096),E_D1:frac(d1sum,24576),E_D2:frac(d2sum,147456)};
  distinctMin=Math.min(distinctMin,states.size);distinctMax=Math.max(distinctMax,states.size);
  summaries.push({world:wid,profile:name,epsilon:frac(eps,32),mu:frac(mu,4),D0:frac(d0,4096),E_D1:frac(d1sum,24576),E_D2:frac(d2sum,147456),reduction_01:frac(6*d0-d1sum,24576),reduction_12:frac(6*d1sum-d2sum,147456),distinct_terminal_states:states.size,order_sensitive_of_15:worldOrder});
 }
 if(rows.length!==1729||summaries.length!==48||totalOrders!==720)throw Error('coverage failure');
 const summary={research_id:'R312',extension:'S108',freeze_commit:'8e8e0c06deb5a8e122bfcfe8c7312d679f93a98c',scope:'E1_ARTIFICIAL_TWO_INDEPENDENT_UNIFORM_DYADS',artificial_worlds:48,ordered_paths:1728,paths_per_world:36,ordered_pair_contrasts:720,order_sensitive_contrasts:changedOrders,strict_reduction_step1_worlds:strict1,strict_reduction_step2_worlds:strict2,zero_reduction_step2_worlds:zero2,distinct_terminal_min:distinctMin,distinct_terminal_max:distinctMax,strict_example:strictExample,order_example:orderExample,worlds:summaries,new_human_E2:0,new_historical_E3:0,R073:'FROZEN',PESEN_v0_1:'FROZEN'};
 return {csv:rows.join('\n')+'\n',json:JSON.stringify(summary,null,2)+'\n',summary};
}
if(require.main===module){const r=generate();if(process.argv[2]==='--emit'){fs.writeFileSync(process.argv[3],r.csv);fs.writeFileSync(process.argv[4],r.json);}else if(process.argv[2]==='--test'){console.log(JSON.stringify(r.summary));}else throw Error('usage: --emit CSV JSON or --test');}
module.exports={generate};
