'use strict';
const fs=require('node:fs');
function calculate(csv,reference){
 let checks=0;function ok(v,m){checks++;if(!v)throw Error(m)}
 function gcd(a,b){while(b){let c=a%b;a=b;b=c}return a<0n?-a:a}
 function q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<=0n)throw Error('denom');let g=gcd(n,d);return [n/g,d/g]}
 function plus(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
 function sub(a,b){return q(a[0]*b[1]-b[0]*a[1],a[1]*b[1])}
 function fmt(a){return a[1]===1n?String(a[0]):a[0]+'/'+a[1]}
 function parse(s){let a=String(s).split('/');return q(a[0],a[1]||1)}
 const rows=csv.trim().split(/\r?\n/),headers=rows.shift().split(','),idx=Object.fromEntries(headers.map((x,i)=>[x,i]));
 const cols=['world','oracle_hidden_U','original_exogenous_source_probability',...Array.from({length:4},(_,i)=>'observed_event_Y'+(i+1)),...Array.from({length:4},(_,i)=>'observed_accumulated_count_N'+(i+1)),...Array.from({length:4},(_,i)=>'oracle_exogenous_R'+(i+1)+'1'),...Array.from({length:4},(_,i)=>'oracle_exogenous_R'+(i+1)+'2')];
 for(const c of cols)ok(Number.isInteger(idx[c]),'missing '+c);
 const worlds=new Map(),ids=new Map(),alias=new Map();
 for(const line of rows){
  let v=line.split(','),w=v[idx.world];ok(v.length===headers.length,'width');
  if(!worlds.has(w)){worlds.set(w,[]);ids.set(w,new Set());alias.set(w,new Map())}
  let bits=v[idx.oracle_hidden_U]+[1,2,3,4].map(i=>v[idx['oracle_exogenous_R'+i+'1']]+v[idx['oracle_exogenous_R'+i+'2']]).join('');
  ok(/^[01]{9}$/.test(bits)&&!ids.get(w).has(bits),'unique source');ids.get(w).add(bits);
  ok(v[idx.original_exogenous_source_probability]==='1/512','source probability');
  let y=[1,2,3,4].map(i=>v[idx['observed_event_Y'+i]]);ok(y.every(x=>x==='0'||x==='1'),'binary');
  let total=0;for(let i=1;i<=4;i++){total+=Number(y[i-1]);ok(v[idx['observed_accumulated_count_N'+i]]===String(total),'cumulative')}
  worlds.get(w).push(y);alias.get(w).set(bits,y.join(''));
 }
 ok(rows.length===4608&&worlds.size===9,'complete universe');
 for(const [w,arr] of worlds)ok(arr.length===512&&ids.get(w).size===512,'512 per world '+w);
 const a=alias.get('SELF_EXCITING_LAG1'),b=alias.get('STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS');
 for(const [key,value] of a)ok(b.get(key)===value,'sourcewise alias');
 const fields={F0:[],F3:[2],F23:[1,2],F123:[0,1,2]};
 let out=[];
 for(const [w,arr] of worlds){
  let risks={},support={};
  for(const [label,indices] of Object.entries(fields)){
   let groups=new Map();
   for(const y of arr){let key=indices.map(i=>y[i]).join('')||'*',g=groups.get(key)||{m:0,s:0};g.m++;g.s+=Number(y[3]);groups.set(key,g)}
   let risk=q(0);
   for(const {m,s} of groups.values()){ok(m>0&&s>=0&&s<=m,'count');risk=plus(risk,q(BigInt(s*(m-s)),BigInt(512*m)))}
   risks[label]=fmt(risk);support[label]=groups.size;
  }
  let ref=reference.worlds.find(x=>x.world===w);ok(!!ref,'reference world');
  for(const k of Object.keys(fields)){ok(ref.risks[k]===risks[k],'risk parity '+w+' '+k);ok(ref.positive_support_prefix_groups[k]===support[k],'support parity')}
  let gains={F0_to_F3:fmt(sub(parse(risks.F0),parse(risks.F3))),F3_to_F23:fmt(sub(parse(risks.F3),parse(risks.F23))),F23_to_F123:fmt(sub(parse(risks.F23),parse(risks.F123)))};
  for(const k of Object.keys(gains))ok(ref.history_gains[k]===gains[k],'gain parity');
  let s=arr.reduce((n,y)=>n+Number(y[3]),0);ok(fmt(q(BigInt(s*(512-s)),BigInt(512*512)))===risks.F0,'marginal');
  out.push({world:w,risks,history_gains:gains,positive_support_prefix_groups:support});
 }
 // Illegal future-target feature: every (Y4) group has a constant target, hence exact risk zero.
 let leakageWorlds=0;
 for(const arr of worlds.values()){
   const groups=new Map();
   for(const y of arr){const k=y[3],g=groups.get(k)||{m:0,s:0};g.m++;g.s+=Number(y[3]);groups.set(k,g)}
   for(const {m,s} of groups.values())ok(s===0||s===m,'future-target group must be pure');
   leakageWorlds++;
 }
 ok(leakageWorlds===9,'leakage negative control world count');
 const mutant=JSON.parse(JSON.stringify(reference));mutant.worlds.find(x=>x.world==='IID_LOW').risks.F0='999';
 ok(mutant.worlds.find(x=>x.world==='IID_LOW').risks.F0!==out.find(x=>x.world==='IID_LOW').risks.F0,'mutant rejection');
 return {research_id:'B_R246_S42',scope:'INTERNAL_INDEPENDENT_INTEGER_SOURCE_COUNTS_E1',source:'research/R246/R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv',source_blob:'f817b78f833cf13ea589bc5ab732bc6947d66a3a',source_rows:rows.length,world_count:worlds.size,checks,failures:0,compared_risks:36,compared_gains:27,mutation_detection:true,future_outcome_leakage_risk:'0',worlds:out,external_replication:0};
}
if(require.main===module){let p=process.argv;console.log(JSON.stringify(calculate(fs.readFileSync(p[2]||'research/R246/R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv','utf8'),JSON.parse(fs.readFileSync(p[3]||'research/validation/R246_S42_HISTORY_FORECAST_EXACT_RECEIPT_2026-10-28.json','utf8'))),null,2))}
module.exports={calculate};
