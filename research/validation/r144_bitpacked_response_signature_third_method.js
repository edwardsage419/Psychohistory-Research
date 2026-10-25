#!/usr/bin/env node
'use strict';
// R144 E1 frozen bit-packed third method. Node.js standard library only.
// Usage: node r144_bitpacked_response_signature_third_method.js > result.json
const EVENTS = ['O','M','A','E','B','W'];
function encode(r,c,w,e) { return (r&1) | ((c&1)<<1) | ((w&3)<<2) | ((e&1)<<4); }
function decode(s) { return {r:s&1,c:(s>>1)&1,w:(s>>2)&3,e:(s>>4)&1}; }
function step(state, event) {
  let {r,c,w,e}=decode(state);
  if(event==='O') { if(e===0) w=2; }
  else {
    if(event==='M' && w>0) c=1;
    if(event==='A' && w>0 && c===1) r=1;
    if(event==='E' && r===1) e=1;
    if(event==='B' && e===0) { r=0; c=0; }
    if(w>0) w--;
  }
  if(e && !r) throw new Error('entrenched without reform');
  if(w<0 || w>2) throw new Error('invalid window');
  return encode(r,c,w,e);
}
function replay(events) { let s=0; for(const event of events) s=step(s,event); return s; }
function asWord(n) { let x=n; const word=[]; for(let j=0;j<5;j++){word.push(EVENTS[x%6]);x=Math.floor(x/6);}return word; }
function permutations(items) {
  if(!items.length) return [[]];
  const out=[];
  for(let i=0;i<items.length;i++) for(const rest of permutations(items.filter((_,j)=>i!==j))) out.push([items[i],...rest]);
  return out;
}
const histories=[];
const terminal={'r0e0':0,'r1e0':0,'r1e1':0,'r0e1':0};
const responseByR=[new Map(),new Map()];
const responseByB={'survive':0,'collapse':0};
for(let i=0;i<6**5;i++){
  const word=asWord(i),s=replay(word),{r,e}=decode(s);
  terminal[`r${r}e${e}`]++;
  const signature=EVENTS.map(event=>String(decode(step(s,event)).r)).join('');
  responseByR[r].set(signature,(responseByR[r].get(signature)||0)+1);
  if(r===1) responseByB[decode(step(s,'B')).r===1?'survive':'collapse']++;
  histories.push({word,s,r,e,signature});
}
const changes={r:0,e:0,any:0,both:0};
for(const {word,r,e} of histories){
  for(let j=0;j<5;j++){
    const counter=word.slice();counter[j]='W';
    const s=replay(counter),d=decode(s);
    const rdiff=r!==d.r,ediff=e!==d.e;
    if(rdiff) changes.r++;
    if(ediff) changes.e++;
    if(rdiff||ediff) changes.any++;
    if(rdiff&&ediff) changes.both++;
  }
}
const orders=permutations(['O','M','A','E','B']);
const orderReform=orders.filter(x=>decode(replay(x)).r===1).length;
const choose2=n=>n*(n-1)/2;
const signatureStats=responseByR.map((map,r)=>{
  const entries=Object.fromEntries([...map].sort((a,b)=>a[0].localeCompare(b[0])));
  const total=[terminal.r0e0+terminal.r0e1,terminal.r1e0+terminal.r1e1][r];
  const distinctPairs=choose2(total)-[...map.values()].reduce((v,n)=>v+choose2(n),0);
  return {observed_reform:r,counts:entries,total,signature_count:map.size,indistinguishable_observation_but_different_one_step_pairs:distinctPairs};
});
const witnessA=decode(replay(['O','M','A','W','W']));
const witnessB=decode(replay(['O','M','A','E','W']));
const afterA=decode(step(replay(['O','M','A','W','W']),'B'));
const afterB=decode(step(replay(['O','M','A','E','W']),'B'));
const controls={
  event_order_matter:orderReform>0 && orderReform<120,
  reform_not_necessarily_entrenched:witnessA.r===1 && witnessA.e===0 && witnessB.r===1 && witnessB.e===1 && afterA.r===0 && afterB.r===1
};
if(JSON.stringify(terminal)!==JSON.stringify({r0e0:7663,r1e0:96,r1e1:17,r0e1:0}))throw new Error('terminal regression');
if(JSON.stringify(changes)!==JSON.stringify({r:373,e:69,any:388,both:54}))throw new Error('do-W regression');
if(orderReform!==4||orders.length!==120)throw new Error('permutation regression');
if(!Object.values(controls).every(Boolean))throw new Error('negative control failed');
if(signatureStats[0].total!==7663||signatureStats[1].total!==113)throw new Error('signature total');
if(responseByB.survive!==17||responseByB.collapse!==96)throw new Error('B probe');
const result={research_id:'R144',evidence:'E1',source_histories:7776,paired_do_W:38880,terminal,changes,orders:120,order_reformed:orderReform,response_signature_event_order:'OMAEBW',signatureStats,responseByB,B_probe_opposite_unordered_pairs:responseByB.survive*responseByB.collapse,negative_controls:controls,new_E2:0,new_E3:0,external_replication:false};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
