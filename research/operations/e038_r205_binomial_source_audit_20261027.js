// E038 independent R205 audit, Node 18+; no third-party dependencies.
// Usage: node e038_r205_binomial_source_audit_20261027.js TRAIN.csv RECEIPT.json
"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
function P(x){let s=String(x).trim().split("/");return F(s[0],s[1]||1);}
function A(x,y){return F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function D(x,y){return F(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function M(x,y){return F(x[0]*y[0],x[1]*y[1]);}
function V(x,y){return F(x[0]*y[1],x[1]*y[0]);}
function C(x,y){let d=x[0]*y[1]-y[0]*x[1];return d<0n?-1:d>0n?1:0;}
function S(x){return x[1]===1n?String(x[0]):x[0]+"/"+x[1];}
function choose(n,k){let z=1n;for(let i=1;i<=k;i++)z=z*BigInt(n-i+1)/BigInt(i);return z;}
function audit(csv,receipt){
 let checks=0,regressions=0,worldChecks=0,negativeControls=0;
 function yes(v,label){checks++;if(!v)throw Error("CHECK "+checks+": "+label);}
 function same(actual,expected,label){yes(C(P(actual),expected)===0,label+" got="+actual+" expected="+S(expected));}
 const lines=csv.trim().split(/\r?\n/),h=lines.shift().split(",");
 const rows=lines.map((line,i)=>{const cells=line.split(",");yes(cells.length===h.length,"row width "+i);return Object.fromEntries(h.map((k,j)=>[k,cells[j]]));});
 yes(rows.length===240,"training row count");
 yes(receipt.training_history_rows===240,"receipt row count");
 yes(receipt.shifted_evaluation_worlds===36,"receipt world count");
 yes(receipt.weighted_heldout_event_evaluations===2880,"receipt weighted evaluations");
 const byWorld=new Map();
 for(const [i,r] of rows.entries()){
  let a=Number(r.true_a),b=Number(r.true_b),m=Number(r.independent_training_pair_count);
  let axes=r.ordered_training_pair_axes.split("|").map(Number),k=axes.filter(x=>x===1).length;
  yes(axes.length===m&&axes.every(x=>x===1||x===2),"training axes "+i);
  let x=BigInt(k*a*a),y=BigInt((m-k)*b*b),axis=x>=y?1:2;
  let v1=F(x,BigInt(m)),v2=F(y,BigInt(m)),total=A(v1,v2);
  let larger=C(v1,v2)>=0?v1:v2,smaller=C(v1,v2)>=0?v2:v1;
  let future=axis===1?F(b*b,2):F(a*a,2);
  let futureVar=F(a*a+b*b,2);
  same(r.source_train_probability,F(1,2**m),"train probability "+i);
  same(r.full_sample_mean_x1,F(0),"mean1 "+i);
  same(r.full_sample_mean_x2,F(0),"mean2 "+i);
  same(r.source_empirical_cov_x1x1,v1,"cov11 "+i);
  same(r.source_empirical_cov_x1x2,F(0),"cov12 "+i);
  same(r.source_empirical_cov_x2x2,v2,"cov22 "+i);
  yes(Number(r.training_selected_PC_axis)===axis,"axis "+i);
  same(r.training_explained_ratio_exact,V(larger,total),"training ratio "+i);
  same(r.training_reconstruction_mse_exact,smaller,"training recon "+i);
  same(r.true_independent_new_event_recon_mse_exact,future,"original future recon "+i);
  same(r.true_independent_new_event_retained_ratio_exact,D(F(1),V(future,futureVar)),"original retained "+i);
  same(r.true_independent_new_event_target1_mse_exact,axis===1?F(0):F(1,2),"original target1 "+i);
  same(r.true_independent_new_event_target2_mse_exact,axis===1?F(1,2):F(0),"original target2 "+i);
  regressions+=13;
  let key=[a,b,m].join("|");if(!byWorld.has(key))byWorld.set(key,{axes:new Set(),e1:0,rows:0});
  let group=byWorld.get(key);yes(!group.axes.has(r.ordered_training_pair_axes),"unique history "+i);
  group.axes.add(r.ordered_training_pair_axes);group.rows++;if(axis===1)group.e1++;
 }
 yes(byWorld.size===12,"12 training worlds");
 let positive=0,zero=0;
 for(const w of receipt.worlds){
  let {a,b,m}=w,q=P(w.q),key=[a,b,m].join("|"),group=byWorld.get(key);
  yes(!!group,"world exists "+key);yes(group.rows===2**m,"complete histories "+key);
  let e1Count=0n;for(let k=0;k<=m;k++)if(k*a*a>=(m-k)*b*b)e1Count+=choose(m,k);
  yes(group.e1===Number(e1Count),"binomial count "+key);
  let p=F(e1Count,BigInt(2**m)),one=F(1),notP=D(one,p),notQ=D(one,q);
  let axis1=M(q,F(a*a)),axis2=M(notQ,F(b*b)),energy=A(axis1,axis2);
  let mse=A(M(p,axis2),M(notP,axis1));
  let ratio=D(one,V(mse,energy));
  let target1=M(notP,q),target2=M(p,notQ);
  let oldAxis=a*a>=b*b?1:2,oldMse=oldAxis===1?axis2:axis1;
  let oracleAxis=C(axis1,axis2)>=0?1:2,oracleMse=oracleAxis===1?axis2:axis1;
  let regret=D(mse,oracleMse),oldRegret=D(oldMse,oracleMse);
  yes(w.ordered_train_histories===2**m,"world history count "+key);worldChecks++;
  for(const [field,value] of Object.entries({
   probability_select_e1:p,heldout_variance:energy,
   selected_pca_reconstruction_mse:mse,selected_pca_retained_energy_ratio:ratio,
   target1_mse:target1,target2_mse:target2,
   old_population_pca_reconstruction_mse:oldMse,
   test_distribution_oracle_reconstruction_mse:oracleMse,
   selected_pca_oracle_regret:regret,old_population_pca_oracle_regret:oldRegret
  })){same(w[field],value,key+" "+w.q+" "+field);worldChecks++;}
  yes(w.old_population_pca_axis===oldAxis,"old axis "+key);worldChecks++;
  yes(w.test_distribution_oracle_axis===oracleAxis,"oracle axis "+key);worldChecks++;
  if(C(regret,F(0))>0)positive++;else if(C(regret,F(0))===0)zero++;else throw Error("negative oracle regret");
  if(a===3&&b===1&&m===5&&w.q==="1/20"){
   yes(C(mse,A(M(p,F(b*b,2)),M(notP,F(a*a,2))))!==0,"negative control: stale q=1/2 differs");negativeControls++;
   yes(C(mse,oracleMse)>0,"negative control: future oracle leakage");negativeControls++;
  }
 }
 yes(receipt.worlds.length===36,"36 receipt worlds");
 yes(positive===32&&zero===4,"oracle regret sign count");
 return {checks,training_rows:rows.length,training_regressions:regressions,worlds:receipt.worlds.length,world_field_checks:worldChecks,positive_regret:positive,zero_regret:zero,negative_controls:negativeControls,status:"PASS"};
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==4)throw Error("Usage: node SCRIPT TRAIN.csv RECEIPT.json");
 console.log(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));
}