'use strict';
const fs=require('node:fs');
function calculate(raw){
 const data=JSON.parse(raw), Z=[0n,1n];let checks=0;
 function ok(v,m){checks++;if(!v)throw Error(m)}
 function gcd(a,b){while(b){[a,b]=[b,a%b]}return a<0n?-a:a}
 function q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<=0n)throw Error('denom');let g=gcd(a,b);return [a/g,b/g]}
 function add(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
 function sub(a,b){return q(a[0]*b[1]-b[0]*a[1],a[1]*b[1])}
 function mul(a,b){return q(a[0]*b[0],a[1]*b[1])}
 function div(a,b){return q(a[0]*b[1],a[1]*b[0])}
 function cmp(a,b){let x=a[0]*b[1]-b[0]*a[1];return x<0n?-1:x>0n?1:0}
 function parse(s){let a=String(s).split('/');return q(a[0],a[1]||1)}
 function str(a){return a[1]===1n?String(a[0]):a[0]+'/'+a[1]}
 const fields={F0:[],F3:[2],F23:[1,2],F123:[0,1,2]};
 ok(data.research_id==='R246'&&data.frozen_worlds===9,'input identity');
 let worlds=[];
 for(const w of data.world_results){
  const entries=Object.entries(w.complete_observed_four_bin_event_joint);
  let total=q(0),positive=q(0);
  for(const [bits,weight] of entries){ok(/^[01]{4}$/.test(bits),'path bits');let p=parse(weight);ok(cmp(p,q(0))>0,'positive mass');total=add(total,p);if(bits[3]==='1')positive=add(positive,p)}
  ok(cmp(total,q(1))===0,'mass sum');
  let risks={},support={};
  for(const [name,indices] of Object.entries(fields)){
   const g=new Map();
   for(const [bits,weight] of entries){let key=indices.map(i=>bits[i]).join('')||'*',old=g.get(key)||{m:q(0),s:q(0)};old.m=add(old.m,parse(weight));if(bits[3]==='1')old.s=add(old.s,parse(weight));g.set(key,old)}
   let risk=q(0);for(const {m,s} of g.values()){ok(cmp(m,q(0))>0,'positive group');risk=add(risk,div(mul(s,sub(m,s)),m))}
   risks[name]=str(risk);support[name]=g.size;ok(cmp(risk,q(0))>=0&&cmp(risk,q(1,4))<=0,'range');
  }
  let a=Object.values(risks).map(parse);ok(cmp(a[0],mul(positive,sub(q(1),positive)))===0,'marginal risk');
  ok(a.every((v,i)=>i===0||cmp(a[i-1],v)>=0),'nested risks');
  let gains={F0_to_F3:str(sub(a[0],a[1])),F3_to_F23:str(sub(a[1],a[2])),F23_to_F123:str(sub(a[2],a[3]))};
  worlds.push({world:w.world,risks,history_gains:gains,positive_support_prefix_groups:support});
 }
 ok(worlds.length===9,'world count');
 const get=n=>worlds.find(x=>x.world===n).risks;
 for(const n of ['IID_LOW','IID_HIGH','ALTERNATING_EXOGENOUS_RATE']){let a=get(n);ok(a.F0===a.F3&&a.F3===a.F23&&a.F23===a.F123,'iid '+n)}
 let a=get('SELF_EXCITING_LAG1');ok(a.F3===a.F23&&a.F23===a.F123,'lag1 sufficient');
 let b=get('SELF_EXCITING_TWO_LAG');ok(cmp(parse(b.F3),parse(b.F23))>0,'lag2 gain');
 ok(JSON.stringify(a)===JSON.stringify(get('STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS')),'alias');
 return {research_id:'R246_S42',scope:'E1_SYNTHETIC_FOUR_BIN_BERNOULLI_NOT_CONTINUOUS_POISSON_HAWKES',source:'research/R246/R246_EXACT_RESULTS.json',source_blob:'8aec1fd3f6dba6073f03e74f8f854f7d6a46a6c3',world_count:9,target:'Y4',checks,failures:0,worlds,real_E2:0,historical_E3:0,external_replication:0};
}
if(require.main===module){console.log(JSON.stringify(calculate(fs.readFileSync(process.argv[2]||'research/R246/R246_EXACT_RESULTS.json','utf8')),null,2))}
module.exports={calculate};
