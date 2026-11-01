'use strict';
// R178: independent 30-world exact rational PMF and risk audit (Node.js stdlib).
// Scope: archived artificial E1, no original Python imports or empirical scoring.
const PIN='3b4a5abeaa14b5be32fb258a15aa6bf502b2756c';
const NAMES=['IID_BIN','CLUSTERED_BB_C2','CLUSTERED_BB_C8','INACTIVE_ZIB_Z1_8','INACTIVE_ZIB_Z1_4'];
function req(ok,msg){if(!ok)throw Error(msg)}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);req(b!==0n,'zero denominator');if(b<0n){a=-a;b=-b}let d=gcd(a,b);return [a/d,b/d]}
function P(s){let x=String(s).split('/');return F(x[0],x[1]||1)}
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>add(a,[-b[0],b[1]]),
mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]),
eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],le=(a,b)=>a[0]*b[1]<=b[0]*a[1],
pow=(a,n)=>F(a[0]**BigInt(n),a[1]**BigInt(n)),num=a=>Number(a[0])/Number(a[1]),
fmt=a=>a[1]===1n?String(a[0]):a.map(String).join('/');
const Z=F(0),ONE=F(1);
function choose(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-i+1)/BigInt(i);return F(v)}
function rise(a,k){let v=ONE;for(let i=0;i<k;i++)v=mul(v,add(a,F(i)));return v}
function pmf(n,p,name){return Array.from({length:n+1},(_,k)=>{
 let c=choose(n,k);
 if(name==='IID_BIN')return mul(c,mul(pow(p,k),pow(sub(ONE,p),n-k)));
 if(name.startsWith('CLUSTERED')){let t=F(name.endsWith('C2')?2:8);
   return div(mul(c,mul(rise(mul(p,t),k),rise(mul(sub(ONE,p),t),n-k))),rise(t,n))}
 let z=F(name.endsWith('Z1_8')?1:1,name.endsWith('Z1_8')?8:4),q=div(p,sub(ONE,z));
 let b=mul(c,mul(pow(q,k),pow(sub(ONE,q),n-k)));
 return k===0?add(z,mul(sub(ONE,z),b)):mul(sub(ONE,z),b);
})}
function audit(data){
 req(data.research_id==='R178'&&data.stage==='E1_ARTIFICIAL_EXACT_FINITE_SAMPLE_MLE_RISK','identity');
 req(data.world_count===30&&data.full_count_probability_cells===270&&data.source_distributions===5,'totals');
 req(data.real_human_or_history_tested===false&&data.new_E2===0&&data.new_E3===0,'grade');
 req(Array.isArray(data.source_worlds)&&data.source_worlds.length===30,'universe');
 let worlds=0,cells=0,checks=0,maxError=0;
 const check=(got,expected,label)=>{checks++;req(eq(got,P(expected)),label+' mismatch '+fmt(got)+' vs '+expected)};
 for(let n of [4,8,12])for(let ps of ['1/4','1/2'])for(let name of NAMES){
  let key=n+'|'+ps+'|'+name;
  let matches=data.source_worlds.filter(r=>r.sample_size===n&&r.true_marginal_p===ps&&r.training_mechanism===name);
  req(matches.length===1,'duplicate or missing '+key);
  let r=matches[0],p=P(ps),w=pmf(n,p,name);
  req(r.full_training_count_pmf.length===n+1,'support '+key);
  w.forEach((v,k)=>{check(v,r.full_training_count_pmf[k],'PMF '+key+' '+k);cells++});
  check(w.reduce(add,Z),'1','normalization '+key);
  check(w.reduce((a,b,k)=>add(a,mul(b,F(k))),Z),fmt(mul(p,F(n))),'mean '+key);
  let bias=w.reduce((a,b,k)=>add(a,mul(b,sub(F(k,n),p))),Z);
  let mse=w.reduce((a,b,k)=>add(a,mul(b,pow(sub(F(k,n),p),2))),Z);
  let naive=div(mul(p,sub(ONE,p)),F(n));
  let cov=w.reduce((a,b,k)=>{let q=F(k,n);return le(pow(sub(p,q),2),div(mul(pow(F(49,25),2),mul(q,sub(ONE,q))),F(n)))?add(a,b):a},Z);
  let boundary=add(w[0],w[n]);
  let lb=w.reduce((a,b,k)=>add(a,mul(b,sub(F(k+1,n+2),p))),Z);
  let lm=w.reduce((a,b,k)=>add(a,mul(b,pow(sub(F(k+1,n+2),p),2))),Z);
  for(let [v,f] of [[bias,'mle_expected_bias'],[mse,'mle_expected_squared_error'],
    [naive,'iid_model_claimed_theoretical_mse'],[div(mse,naive),'true_over_naive_mle_variance_ratio'],
    [cov,'wald_nominal_95_actual_coverage'],[boundary,'boundary_mle_0_or_1_probability'],
    [lb,'laplace_bias'],[lm,'laplace_expected_squared_error']])check(v,r[f],f+' '+key);
  req(num(boundary)>0&&r.unsmoothed_mle_independent_test_expected_logloss==='INF','infinite loss '+key);
  let score=w.reduce((a,b,k)=>{let q=(k+1)/(n+2);return a+num(b)*(-num(p)*Math.log(q)-(1-num(p))*Math.log(1-q))},0);
  let error=Math.abs(score-Number(r.laplace_expected_independent_test_logloss));
  maxError=Math.max(maxError,error);req(error<=1e-12,'Laplace score '+key);
  worlds++;
 }
 req(data.source_worlds.every(r=>[4,8,12].includes(r.sample_size)&&['1/4','1/2'].includes(r.true_marginal_p)&&NAMES.includes(r.training_mechanism)),'unexpected world');
 req(JSON.stringify(data.fixed_n8_p_quarter_comparison)===JSON.stringify(data.source_worlds.filter(r=>r.sample_size===8&&r.true_marginal_p==='1/4')),'illustration identity');
 return {status:'PASS_INTERNAL_NONBLIND_E1',worlds,cells,exact_checks:checks,max_laplace_error:maxError,new_E2:0,new_E3:0};
}
function negatives(d){let rejected=0;
 for(let change of [x=>x.source_worlds[0].full_training_count_pmf[0]='999',
                    x=>x.source_worlds[0].mle_expected_squared_error='999',
                    x=>x.source_worlds[1]=JSON.parse(JSON.stringify(x.source_worlds[0]))]){
  let x=JSON.parse(JSON.stringify(d));change(x);try{audit(x)}catch(e){rejected++}
 }req(rejected===3,'mutation test');return rejected}
if(typeof module!=='undefined')module.exports={audit,negatives};
if(typeof require!=='undefined'&&require.main===module){
 try{const fs=require('node:fs'),crypto=require('node:crypto');
 req(process.argv.length===3,'usage: node audit.js R178_EXACT_RESULTS.json');
 let raw=fs.readFileSync(process.argv[2]);
 let hash=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
 req(hash===PIN,'archive Git blob mismatch');
 let d=JSON.parse(raw.toString('utf8'));let out=audit(d);out.mutations_rejected=negatives(d);out.source_blob=hash;
 console.log(JSON.stringify(out,null,2));
 }catch(e){console.error('R178_E1_AUDIT_FAIL: '+e.message);process.exitCode=1}
}