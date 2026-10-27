'use strict';
// R214-S10 main enumeration. Node >=18. No external packages.
// Input: frozen R214-S9 original 576-row CSV. All arithmetic exact BigInt fractions.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
class Q{
  constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error('zero denominator');if(b<0n){a=-a;b=-b;}let g=gcd(a,b);this.n=a/g;this.d=b/g;}
  static of(x){let s=String(x).split('/');return new Q(s[0],s[1]||1);}
  add(b){b=Q.of(b);return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  sub(b){b=Q.of(b);return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
  mul(b){b=Q.of(b);return new Q(this.n*b.n,this.d*b.d);}
  div(b){b=Q.of(b);return new Q(this.n*b.d,this.d*b.n);}
  eq(b){b=Q.of(b);return this.n===b.n&&this.d===b.d;}
  toString(){return this.d===1n?String(this.n):String(this.n)+'/'+String(this.d);}
}
function compute(csv){
  let lines=csv.trim().split(/\r?\n/), cols=lines.shift().split(',');
  const rows=lines.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[cols[i],v])));
  if(rows.length!==576)throw Error('source row count mismatch');
  const worlds=[...new Set(rows.map(r=>r.world))];
  if(worlds.length!==9||worlds.some(w=>rows.filter(r=>r.world===w).length!==64))throw Error('world count mismatch');
  const z=[Q.of('-1/8'),Q.of('0'),Q.of('1/8')];
  const qs=['0','1/4','1/2'], target=Q.of('1/8');
  let results=[];
  for(let w of worlds){
    const group=rows.filter(r=>r.world===w);
    const taus=[...new Set(group.map(r=>r.oracle_true_tau_at_R))];
    // Tau(r) can vary with r; cutoff tau0 from original S9 model: only LINEAR_EFFECT_SLOPE
    // and DIFFERENTIAL_CURVATURE vary, both equal 2 at r=0.
    const tau=w==='PLACEBO_JUMP_NO_TREATMENT'?Q.of(0):Q.of(2);
    for(let qtext of qs){
      const q=Q.of(qtext), probs=[q,Q.of(1).sub(q.mul(2)),q];
      let mass=Q.of(0), zero=Q.of(0), zeroD=Q.of(0), wrong=Q.of(0);
      let plus=Q.of(0),minus=Q.of(0),plusY=Q.of(0),minusY=Q.of(0);
      let positiveSlots=0;
      for(let row of group){
        const r=Q.of(row.observed_R), y=Q.of(row.observed_Y), p=Q.of(row.source_probability), d=Number(row.assigned_D);
        if(d!==(r.n>0n?1:0))throw Error('source treatment mismatch');
        for(let j=0;j<3;j++){
          let weight=p.mul(probs[j]), obs=r.add(z[j]);
          mass=mass.add(weight);
          if(weight.n!==0n)positiveSlots++;
          if(obs.eq(0)){zero=zero.add(weight);if(d)zeroD=zeroD.add(weight);}
          if(d!==(obs.n>0n?1:0))wrong=wrong.add(weight);
          if(obs.eq(target)){plus=plus.add(weight);plusY=plusY.add(weight.mul(y));}
          if(obs.eq(Q.of('-1/8'))){minus=minus.add(weight);minusY=minusY.add(weight.mul(y));}
        }
      }
      if(!mass.eq(1)||plus.n===0n||minus.n===0n)throw Error('support or probability failure');
      const gap=plusY.div(plus).sub(minusY.div(minus));
      const record={world:w,q:qtext,source_slots:192,positive_probability_slots:positiveSlots,
        probability_sum:String(mass),w0_mass:String(zero),w0_treated_share:zero.n===0n?null:String(zeroD.div(zero)),
        assignment_mismatch_mass:String(wrong),w_plus_mass:String(plus),w_minus_mass:String(minus),
        y_plus_mean:String(plusY.div(plus)),y_minus_mean:String(minusY.div(minus)),
        observed_gap:String(gap),oracle_cutoff_tau:String(tau),gap_minus_oracle:String(gap.sub(tau))};
      if(!zero.eq(q.div(8)))throw Error('zero support invariant');
      const expectedWrong=q.mul(w==='DENSITY_JUMP_ONLY'?Q.of('3/32'):Q.of('1/16'));
      if(!wrong.eq(expectedWrong))throw Error('mismatch invariant');
      if(zero.n>0n&&!zeroD.div(zero).eq(w==='DENSITY_JUMP_ONLY'?Q.of('3/4'):Q.of('1/2')))throw Error('zero treatment invariant');
      results.push(record);
    }
  }
  const linear=results.filter(x=>x.world==='LINEAR_CONSTANT').map(x=>x.observed_gap);
  if(JSON.stringify(linear)!==JSON.stringify(['9/4','7/3','5/2']))throw Error('linear frozen control');
  return {research_id:'R214-S10',catalogue_id:'09-005',evidence:'E1_ARTIFICIAL_FINITE_ONLY',
    source_path:'research/R214/R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv',
    source_blob_sha1:'27de4f8239c25c4946f050c68691c3793b8b09af',
    q_values:qs,worlds:worlds.length,source_rows:rows.length,enumerated_slots:5184,
    positive_probability_slots:results.reduce((a,r)=>a+r.positive_probability_slots,0),
    conditions:results.length,results,new_E2:0,new_E3:0};
}
if(typeof module!=='undefined'&&require.main===module){
 const fs=require('fs'),crypto=require('crypto');
 const path=process.argv[2]||'research/R214/R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv';
 const buf=fs.readFileSync(path);
 const blob=crypto.createHash('sha1').update('blob '+buf.length+'\0').update(buf).digest('hex');
 if(blob!=='27de4f8239c25c4946f050c68691c3793b8b09af')throw Error('source blob changed');
 process.stdout.write(JSON.stringify(compute(buf.toString('utf8')),null,2)+'\n');
}
