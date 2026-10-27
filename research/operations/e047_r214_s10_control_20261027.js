'use strict';
// E047: exact independent audit of R214-S10 frozen negative control.
// Node 18+, no external packages. Run from repository root.
const fs=require('fs'),crypto=require('crypto');
const paths=['research/R214/R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv','research/validation/R214_S10_RUNNING_VARIABLE_COARSENING_EXACT_RECEIPT_2026-10-27.json'];
const expected=['27de4f8239c25c4946f050c68691c3793b8b09af','4af13379e2f14b9d35380aef4bcd1f559f395c29'];
function sha(b){return crypto.createHash('sha1').update('blob '+b.length+String.fromCharCode(0)).update(b).digest('hex');}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
class F{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 static p(x){let a=String(x).split('/');return new F(a[0],a[1]||1);}
 add(x){x=F.p(x);return new F(this.n*x.d+x.n*this.d,this.d*x.d);}
 sub(x){x=F.p(x);return new F(this.n*x.d-x.n*this.d,this.d*x.d);}
 mul(x){x=F.p(x);return new F(this.n*x.n,this.d*x.d);}
 div(x){x=F.p(x);return new F(this.n*x.d,this.d*x.n);}
 eq(x){x=F.p(x);return this.n===x.n&&this.d===x.d;}
 toString(){return this.d===1n?String(this.n):this.n+'/'+this.d;}
}
function run(){
 let checks=0;function ok(b,msg){checks++;if(!b)throw Error('assertion '+checks+' '+msg);}
 const bufs=paths.map(p=>fs.readFileSync(p));for(let i=0;i<2;i++)ok(sha(bufs[i])===expected[i],'Git blob');
 const lines=bufs[0].toString('utf8').trim().split(String.fromCharCode(10)),cols=lines.shift().trim().split(',');
 const rows=lines.map(s=>Object.fromEntries(s.trim().split(',').map((v,i)=>[cols[i],v])));
 const rec=JSON.parse(bufs[1].toString('utf8')),z=F.p(0),one=F.p(1);
 ok(rows.length===576,'rows');let worlds=[...new Set(rows.map(x=>x.world))];ok(worlds.length===9,'worlds');
 let fails=0,passes=0,receiptChecks=0,disagreementCases=0,positiveSlots=0,exceptions=[];
 for(let world of worlds){
  let group=rows.filter(x=>x.world===world),sourceMass=z;ok(group.length===64,'group size');
  for(let r of group){sourceMass=sourceMass.add(F.p(r.source_probability));ok(Number(r.assigned_D)===(F.p(r.observed_R).n>0n?1:0),'source treatment');}
  ok(sourceMass.eq(one),'source probability');
  for(let qs of ['0','1/4','1/2']){
   let q=F.p(qs),old=z,alt=z,m0=z,m0d=z,dis=z,mass=z;
   for(let r of group)for(let [dz,pz] of [['-1/8',q],['0',one.sub(q.mul(2))],['1/8',q]]){
    let w=F.p(r.observed_R).add(F.p(dz)),p=F.p(r.source_probability).mul(pz),d=Number(r.assigned_D);
    mass=mass.add(p);if(p.n!==0n)positiveSlots++;
    let a=w.n>0n?1:0,b=w.n>=0n?1:0;
    if(a!==d)old=old.add(p);if(b!==d)alt=alt.add(p);if(a!==b)dis=dis.add(p);
    if(w.eq(z)){m0=m0.add(p);if(d)m0d=m0d.add(p);}
   }
   let rr=rec.results.find(x=>x.world===world&&x.q===qs);
   ok(!!rr,'receipt present');ok(mass.eq(one),'probability normalized');
   ok(old.eq(rr.assignment_mismatch_mass),'old mismatch receipt');receiptChecks++;
   ok(m0.eq(rr.w0_mass),'zero mass receipt');receiptChecks++;
   ok(m0.eq(q.div(8)),'zero mass invariant');ok(dis.eq(m0),'changed label mass');
   ok(alt.sub(old).eq(m0.sub(m0d.mul(2))),'identity');
   if(q.n!==0n){
    ok(m0d.div(m0).eq(world==='DENSITY_JUMP_ONLY'?'3/4':'1/2'),'conditional treatment');
    ok(dis.n>0n,'positive source label disagreement');disagreementCases++;
    if(alt.eq(old))fails++;else{passes++;exceptions.push({world,q:qs,old:String(old),alt:String(alt),delta:String(alt.sub(old))});}
   }
  }
 }
 return {checks,failures:0,source_rows:rows.length,worlds:worlds.length,conditions:27,
  positive_probability_slots:positiveSlots,receiptChecks,disagreementCases,
  original_control_failures:fails,original_control_passes:passes,exceptions};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};
