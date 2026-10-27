"use strict";
// E045 closed-form independent audit of R212 misclassified binary confounder.
// Run: node e045_r212_closed_form_20261027.js <receipt.json>. Node 18+.
const fs=require("fs");
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n}
function f(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]}
const plus=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const minus=(a,b)=>f(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const times=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
const over=(a,b)=>f(a[0]*b[1],a[1]*b[0]);
const equal=(a,b)=>a[0]*b[1]===b[0]*a[1];
const parse=s=>{const x=String(s).split("/");return f(x[0],x[1]||1)};
function audit(data){
 let checks=0;const failures=[];
 const check=(v,label)=>{checks++;if(!v)failures.push(label)};
 check(data.worlds.length===9,"nine worlds");
 check(data.augmented_source_rows===288,"288 rows");
 check(data.original_source_rows_per_world===8,"original 8");
 check(data.independent_measurement_slots===4,"four slots");
 for(const w of ["CONFOUND","DIRECT","COMBINED"])for(const qstr of ["0/4","1/4","2/4"]){
  const r=data.worlds.find(z=>z.world===w&&z.q===qstr);
  check(!!r,"exists "+w+qstr);if(!r)continue;
  const q=parse(qstr),one=f(1);
  // Independent elimination of latent C yields this rational residual bias.
  const bias=over(times(f(8),times(q,minus(one,q))),times(minus(f(3),times(f(2),q)),plus(one,times(f(2),q))));
  const truth=w==="CONFOUND"?f(0):w==="DIRECT"?one:f(1,2);
  const obs=w==="CONFOUND"?f(1,2):w==="DIRECT"?one:f(3,4);
  const adj=w==="CONFOUND"?bias:w==="DIRECT"?one:plus(f(1,2),over(bias,f(2)));
  check(r.source_rows===32,"source rows "+w+qstr);
  for(const [key,expected] of Object.entries({observational_difference:obs,proxy_adjusted_difference:adj,true_do_effect:truth,proxy_adjustment_bias:minus(adj,truth)}))
   check(equal(parse(r[key]),expected),key+" "+w+qstr);
  check(r.support.length===4,"support cells "+w+qstr);
  for(let s=0;s<2;s++)for(let t=0;t<2;t++){
   const cell=r.support.find(z=>z.cstar===s&&z.t===t);
   check(!!cell,"cell "+w+qstr+s+t);if(!cell)continue;
   const n=s===t?minus(f(12),times(f(8),q)):plus(f(4),times(f(8),q));
   const y=w==="DIRECT"?(t?n:f(0)):
     w==="CONFOUND"?(s===0?(t?times(f(12),q):times(f(4),q)):(t?times(f(12),minus(one,q)):times(f(4),minus(one,q)))):
     (t?n:(s===0?times(f(4),q):times(f(4),minus(one,q))));
   check(equal(f(cell.n),n),"support count "+w+qstr+s+t);
   check(equal(f(cell.y),y),"outcome sum "+w+qstr+s+t);
   check(cell.n>0,"positivity "+w+qstr+s+t);
  }
  if(qstr==="0/4")check(equal(adj,truth),"perfect measurement "+w);
  if(qstr==="2/4")check(equal(adj,obs),"uninformative proxy "+w);
  if(w==="DIRECT")check(equal(adj,one),"direct control "+qstr);
 }
 let last=f(-1);
 for(let k=0;k<=4;k++){
  const q=f(k,8),one=f(1);
  const b=over(times(f(8),times(q,minus(one,q))),times(minus(f(3),times(f(2),q)),plus(one,times(f(2),q))));
  check(b[0]>=0n,"nonnegative "+k);
  check(last[0]<0n||b[0]*last[1]>=last[0]*b[1],"monotonic "+k);
  last=b;
 }
 const mutant=data.worlds.find(z=>z.world==="CONFOUND"&&z.q==="1/4");
 check(!!mutant&&!equal(parse(mutant.proxy_adjusted_difference),f(0)),"mutant q=0 detected");
 return {checks,failures,worlds:data.worlds.length,method:"closed-form latent elimination and support moments"};
}
if(require.main===module){if(process.argv.length<3)throw Error("receipt path required");const r=audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8")));console.log(JSON.stringify(r));if(r.failures.length)process.exitCode=1}
module.exports={audit};
