'use strict';
// E076: third internal route. Run at the repository root using Node.js standard library.
const fs = require('node:fs');
const root = process.cwd();
const read = p => JSON.parse(fs.readFileSync(root + '/' + p, 'utf8'));
const pmf = read('research/R246/R246_EXACT_RESULTS.json');
const r = read('research/validation/R246_S42_HISTORY_FORECAST_EXACT_RECEIPT_2026-10-28.json');
const b = read('research/evidence_audit/B_R246_S42_SOURCE_COUNT_AUDIT_RECEIPT_2026-10-28.json');
const gcd = (a,b) => b === 0n ? (a < 0n ? -a : a) : gcd(b,a%b);
const norm = (n,d=1n) => { if (d === 0n) throw Error('zero denominator'); if (d < 0n) {n=-n;d=-d;} const g=gcd(n,d);return [n/g,d/g]; };
const parse = s => {const [a,d='1']=String(s).split('/');return norm(BigInt(a),BigInt(d));};
const add = (a,b) => norm(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub = (a,b) => norm(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul = (a,b) => norm(a[0]*b[0],a[1]*b[1]);
const div = (a,b) => norm(a[0]*b[1],a[1]*b[0]);
const eq = (a,b) => a[0]===b[0] && a[1]===b[1];
const keys=['F0','F3','F23','F123'];
const prefix = (s,k) => k==='F0'?'':k==='F3'?s[2]:k==='F23'?s.slice(1,3):s.slice(0,3);
let checks=0;
const check = (c,m) => {checks++;if(!c)throw Error('E076 failed: '+m);};
function compute(world) {
  const rows=Object.entries(world.complete_observed_four_bin_event_joint).map(([s,p])=>({s,p:parse(p),z:s[3]==='1'}));
  const out={};
  for(const k of keys) {
    const groups=new Map();
    for(const row of rows) {const x=prefix(row.s,k);if(!groups.has(x))groups.set(x,[]);groups.get(x).push(row);}
    let risk=norm(0n);
    for(const arr of groups.values()) {
      let pos=norm(0n),neg=norm(0n);
      for(const x of arr) {if(x.z)pos=add(pos,x.p);else neg=add(neg,x.p);}
      const m=add(pos,neg);
      if(m[0]!==0n)risk=add(risk,div(mul(pos,neg),m));
    }
    out[k]={risk,support:[...groups.values()].filter(arr=>arr.some(x=>x.p[0]!==0n)).length};
  }
  return out;
}
for(const w of pmf.world_results) {
  const source=Object.entries(w.complete_observed_four_bin_event_joint);
  check(source.length===Number(w.observed_full_four_bin_path_support_size),w.world+' support size');
  check(eq(source.reduce((a,[,p])=>add(a,parse(p)),norm(0n)),norm(1n)),w.world+' PMF sum');
  const x=compute(w),rw=r.worlds.find(v=>v.world===w.world),bw=b.worlds.find(v=>v.world===w.world);
  check(!!rw&&!!bw,w.world+' receipts');
  for(const k of keys) {
    check(eq(x[k].risk,parse(rw.risks[k])),w.world+' R '+k);
    check(eq(x[k].risk,parse(bw.risks[k])),w.world+' B '+k);
    check(x[k].support===bw.positive_support_prefix_groups[k],w.world+' support '+k);
    check(x[k].risk[0]>=0n,w.world+' nonnegative '+k);
    check(x[k].risk[0]*4n<=x[k].risk[1],w.world+' max risk '+k);
  }
  for(let j=1;j<keys.length;j++) {
    const name=keys[j-1]+'_to_'+keys[j],gain=sub(x[keys[j-1]].risk,x[keys[j]].risk);
    check(eq(gain,parse(rw.history_gains[name])),w.world+' R gain '+name);
    check(eq(gain,parse(bw.history_gains[name])),w.world+' B gain '+name);
    check(gain[0]>=0n,w.world+' monotonic '+name);
  }
}
const bad=JSON.parse(JSON.stringify(b));
bad.worlds[0].risks.F0='999';
check(!eq(compute(pmf.world_results[0]).F0.risk,parse(bad.worlds[0].risks.F0)),'mutation detected');
check(pmf.world_results.length===9,'world count');
check(b.source_rows===4608,'source row metadata');
check(b.source_blob==='f817b78f833cf13ea589bc5ab732bc6947d66a3a','source blob identity');
console.log(JSON.stringify({study:'E076_R246_S42',checks,failures:0,risks_compared:72,gains_compared:54,source:'frozen observed PMF',external_replication:0}));
