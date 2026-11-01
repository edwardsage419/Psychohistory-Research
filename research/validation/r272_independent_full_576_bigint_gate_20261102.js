'use strict';
// Independent BigInt oracle for frozen R272 artificial E1. No original Python import.
const CSV_BLOB='8fbbc73d239765f5c66395af1bcf9cf7a8df1f41';
const JSON_BLOB='db3ca11ae224af52c2caf385c898e24aaa0cc54b';
const PS=['1/4','1/2','3/4'],MODELS=['CONSTANT_HALF','TRAIN_MLE','LAPLACE_BETA11'];
const HEADER='world,true_p,predictor,original_full_sixbit_source,original_training_four_bits,original_future_test_two_bits,train_successes,test_successes,exact_original_source_probability,forecast_trained_on_four_bits_only,original_train_brier_per_row,original_test_brier_per_row,exact_train_mean_brier,exact_independent_test_mean_brier,unfloored_future_log_loss_is_infinite';
function need(x,msg){if(!x)throw Error(msg);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);need(d!==0n,'zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function parse(s){const z=String(s).split('/');return frac(z[0],z[1]||'1');}
function add(x,y){return frac(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function sub(x,y){return frac(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function mul(x,y){return frac(x[0]*y[0],x[1]*y[1]);}
function div(x,y){return frac(x[0]*y[1],x[1]*y[0]);}
function pow(x,n){return frac(x[0]**BigInt(n),x[1]**BigInt(n));}
function repr(x){return x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1]);}
function eq(x,y){return x[0]===y[0]&&x[1]===y[1];}
const ZERO=frac(0),ONE=frac(1);
function verify(csv,obj){
 const lines=csv.trimEnd().split(/\r?\n/);
 need(lines.length===577&&lines[0]===HEADER,'CSV header/universe');
 need(obj.research_id==='R272'&&obj.original_catalogue_id==='12-002','research identity');
 need(obj.prescore_freeze_commit==='52f84dbfbe8563cf5c9a491e67d5e320223e0a56','freeze');
 need(obj.artificial_worlds===9&&obj.complete_source_types===576&&obj.training_bit_count===4&&obj.strictly_heldout_test_bit_count===2,'universe');
 need(obj.no_real_human_E2===0&&obj.no_real_historical_E3===0&&obj.R073==='FROZEN'&&obj.PESEN_v0_1==='FROZEN','grade/freeze');
 need(obj.all_nine_analytical_binomial_scores_verified===true&&obj.zero_probability_log_loss_failure_separately_recorded===true,'receipt scope');
 need(Array.isArray(obj.world_results)&&obj.world_results.length===9,'nine world receipts');
 const groups=[];let fields=0;
 for(let i=0;i<3;i++)for(let j=0;j<3;j++){
  const p=parse(PS[i]),model=MODELS[j],world='TRUE_P'+PS[i].replace('/','OF')+'_'+model;
  let mass=ZERO,train=ZERO,test=ZERO,inf=ZERO;
  for(let k=0;k<64;k++){
   const row=lines[1+(i*3+j)*64+k].split(',');
   const bits=k.toString(2).padStart(6,'0'),a=bits.slice(0,4),b=bits.slice(4);
   const K=[...a].reduce((v,c)=>v+Number(c),0),J=[...b].reduce((v,c)=>v+Number(c),0),T=K+J;
   const q=model==='CONSTANT_HALF'?frac(1,2):model==='TRAIN_MLE'?frac(K,4):frac(K+1,6);
   const weight=mul(pow(p,T),pow(sub(ONE,p),6-T));
   const loss=c=>pow(sub(frac(Number(c)),q),2);
   const tl=[...a].map(loss),fl=[...b].map(loss);
   const mean=z=>div(z.reduce(add,ZERO),frac(z.length));
   const trainLoss=mean(tl),testLoss=mean(fl);
   const bad=Number((eq(q,ZERO)&&J>0)||(eq(q,ONE)&&J<2));
   const expected=[world,PS[i],model,bits,a,b,String(K),String(J),repr(weight),repr(q),tl.map(repr).join(';'),fl.map(repr).join(';'),repr(trainLoss),repr(testLoss),String(bad)];
   need(row.length===15,'row column count');
   for(let z=0;z<15;z++){fields++;need(row[z]===expected[z],'row '+(1+(i*3+j)*64+k)+' field '+z);}
   mass=add(mass,weight);train=add(train,mul(weight,trainLoss));test=add(test,mul(weight,testLoss));inf=add(inf,mul(weight,frac(bad)));
  }
  need(eq(mass,ONE),'probability mass '+world);
  const r=obj.world_results[i*3+j];
  need(r.world===world&&r.true_p===PS[i]&&r.predictor===model&&r.full_ordered_source_types===64,'world receipt identity');
  need(r.exact_design_expected_train_mean_Brier===repr(train)&&r.exact_design_expected_independent_future_mean_Brier===repr(test)&&r.exact_unfloored_infinite_test_log_loss_event_probability===repr(inf),'world score '+world);
  need(r.source_enumeration_equals_independent_binomial_theory===true,'analytic claim '+world);
  groups.push({world,train:repr(train),future:repr(test),infinite_event:repr(inf)});
 }
 return {status:'PASS_BOUNDED_E1_INDEPENDENT_FULL_SOURCE',rows:576,fields_checked:fields,worlds:groups.length,evidence:'E1_ARTIFICIAL_ONLY',new_E2:0,new_E3:0,external_replication:'NOT_RUN'};
}
function selftest(csv,obj){
 const lines=csv.trimEnd().split(/\r?\n/);
 const tests=[['source_mass',1,8,'1/2'],['test_split',2,5,'11'],['forecast',80,9,'1/3'],['test_loss',400,13,'0'],['source_identity',5,3,'000011']];
 let rejected=0;
 for(const [name,index,column,replacement] of tests){
  const modified=lines.slice(),r=modified[index].split(',');
  r[column]=replacement;modified[index]=r.join(',');
  try{verify(modified.join('\n')+'\n',obj);}catch(e){rejected++;continue;}
  throw Error('false acceptance: '+name);
 }
 try{verify(csv,{...obj,no_real_human_E2:1});}catch(e){rejected++;}
 try{verify(csv,{...obj,world_results:obj.world_results.map((r,i)=>i===4?{...r,exact_design_expected_independent_future_mean_Brier:'1/4'}:r)});}catch(e){rejected++;}
 need(rejected===7,'false acceptance in metadata/score mutants');
 return {mutation_rejections:rejected,mutation_total:7};
}
module.exports={verify,selftest,CSV_BLOB,JSON_BLOB};
if(require.main===module){
 const fs=require('node:fs'),crypto=require('node:crypto');
 const args=process.argv.slice(2);
 try{
  need(args.length>=2&&args.length<=3&&(args.length===2||args[2]==='--selftest'),'usage: gate CSV JSON [--selftest]');
  const cb=fs.readFileSync(args[0]),jb=fs.readFileSync(args[1]);
  const blob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
  need(blob(cb)===CSV_BLOB&&blob(jb)===JSON_BLOB,'historical Git blob identity');
  const c=cb.toString('utf8'),o=JSON.parse(jb.toString('utf8'));
  const result=verify(c,o);
  if(args[2]==='--selftest')result.negative_controls=selftest(c,o);
  console.log(JSON.stringify(result));
 }catch(e){console.error('R272_BIGINT_GATE_FAIL: '+e.message);process.exitCode=1;}
}
