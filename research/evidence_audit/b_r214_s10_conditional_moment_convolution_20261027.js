'use strict';
// B route: convolution of R-level sufficient moments, independent of R's row x noise enumerator.
// Node >=18, no dependencies. Reads frozen original CSV and frozen S9 oracle summary.
function gc(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a||1n;}
class V{
 constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error('bad denominator');if(b<0n){a=-a;b=-b;}let g=gc(a,b);this.a=a/g;this.b=b/g;}
 static p(x){let s=String(x).split('/');return new V(s[0],s[1]||1);}
 plus(x){x=V.p(x);return new V(this.a*x.b+x.a*this.b,this.b*x.b);}
 neg(){return new V(-this.a,this.b);}
 minus(x){return this.plus(V.p(x).neg());}
 times(x){x=V.p(x);return new V(this.a*x.a,this.b*x.b);}
 over(x){x=V.p(x);return new V(this.a*x.b,this.b*x.a);}
 toString(){return this.b===1n?''+this.a:this.a+'/'+this.b;}
}
function audit(csv,s9text,receiptText){
 const source=csv.trim().split(/\r?\n/), cols=source.shift().split(',');
 const rows=source.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[cols[i],v])));
 const s9=JSON.parse(s9text),r=JSON.parse(receiptText);
 if(rows.length!==576||r.results.length!==27||s9.worlds.length!==9)throw Error('source/receipt shape');
 const expected=new Map(r.results.map(v=>[v.world+'|'+v.q,v]));
 const get=(m,key)=>m.get(key)||V.p(0);
 const del=V.p('1/8');
 let fields=0, baseline=0, masses=0, counter=0, falseFrozen=0, failures=[];
 let examples=[];
 for(let sw of s9.worlds){
  const world=sw.world, group=rows.filter(x=>x.world===world);
  const p=new Map(),py=new Map();
  for(let row of group){
   let k=row.observed_R,weight=V.p(row.source_probability),y=V.p(row.observed_Y);
   p.set(k,get(p,k).plus(weight));
   py.set(k,get(py,k).plus(weight.times(y)));
  }
  let total=[...p.values()].reduce((a,b)=>a.plus(b),V.p(0));
  if(total.toString()!=='1')failures.push('probability '+world);else masses++;
  for(let qstr of ['0','1/4','1/2']){
   let q=V.p(qstr),middle=V.p(1).minus(q.times(2));
   function massAt(w,table){
    let wv=V.p(w),left=wv.minus(del).toString(),right=wv.plus(del).toString();
    return get(table,w).times(middle).plus(get(table,left).times(q)).plus(get(table,right).times(q));
   }
   const pm=massAt('-1/8',p),pp=massAt('1/8',p),zm=massAt('0',p);
   const ym=massAt('-1/8',py).over(pm),yp=massAt('1/8',py).over(pp);
   const g=yp.minus(ym),tau=V.p(sw.oracle_tau_cutoff);
   const treatedAtZero=get(p,'1/8').times(q);
   const mismatch=treatedAtZero;
   const obj={world,q:qstr,source_slots:192,positive_probability_slots:group.length*(qstr==='0'?1:qstr==='1/4'?3:2),
    probability_sum:total.toString(),w0_mass:zm.toString(),w0_treated_share:zm.a===0n?null:treatedAtZero.over(zm).toString(),
    assignment_mismatch_mass:mismatch.toString(),w_plus_mass:pp.toString(),w_minus_mass:pm.toString(),
    y_plus_mean:yp.toString(),y_minus_mean:ym.toString(),observed_gap:g.toString(),
    oracle_cutoff_tau:tau.toString(),gap_minus_oracle:g.minus(tau).toString()};
   const original=expected.get(world+'|'+qstr);
   if(!original){failures.push('missing '+world+qstr);continue;}
   for(let [k,v] of Object.entries(obj)){fields++;if(original[k]!==v)failures.push(world+'|'+qstr+'|'+k);}
   if(qstr==='0'){
    const near=sw.observed_mean_R_near_cutoff;
    for(let [x,y] of [[ym,near[0]],[yp,near[1]]]){baseline++;if(x.toString()!==y)failures.push('S9 baseline '+world);}
   }
   if(qstr!=='0'){
    // Original frozen negative-control expectation is false in eight symmetric worlds.
    const wrongGreaterEqual=get(p,'-1/8').times(q);
    const labelDisagreement=zm;
    if(labelDisagreement.a<=0n)failures.push('label mutation not detectable');
    if(wrongGreaterEqual.toString()===mismatch.toString())falseFrozen++;
    else counter++;
    if(world==='DENSITY_JUMP_ONLY'&&wrongGreaterEqual.toString()===mismatch.toString())failures.push('density asymmetry missing');
   }
   if(world==='LINEAR_CONSTANT')examples.push({q:qstr,gap:g.toString(),bias:g.minus(tau).toString()});
  }
 }
 if(failures.length)throw Error('B audit failed: '+failures.slice(0,10).join(';'));
 return {research_id:'B_R214_S10',route:'R_CONDITIONAL_MOMENT_CONVOLUTION',status:'INTERNAL_PROGRAMMATIC_E1_ONLY',
  source_rows:rows.length,worlds:s9.worlds.length,conditions:r.results.length,
  exact_receipt_fields_compared:fields,original_s9_near_cutoff_means_compared:baseline,
  source_world_mass_checks:masses,postexecution_label_mutation_detected_conditions:18,
  original_frozen_aggregate_mutation_expectation_false_conditions:falseFrozen,
  aggregate_mutation_detected_conditions:counter,failures:failures.length,
  linear_examples:examples,new_E2:0,new_E3:0,external_independent_replications:0};
}
if(typeof module!=='undefined'&&require.main===module){
 const fs=require('fs');
 const a=process.argv[2]||'research/R214/R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv';
 const b=process.argv[3]||'research/R214/R214_S9_EXACT_RESULTS.json';
 const c=process.argv[4]||'research/validation/R214_S10_RUNNING_VARIABLE_COARSENING_EXACT_RECEIPT_2026-10-27.json';
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(a,'utf8'),fs.readFileSync(b,'utf8'),fs.readFileSync(c,'utf8')),null,2)+'\n');
}
