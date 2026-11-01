#!/usr/bin/env node
'use strict';
// R179 independent finite E1 verification. No imports from R177 or R179.
function audit(d){
const check=(v,m)=>{if(!v)throw Error(m)};
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n};
const q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);check(b!==0n,'zero denominator');if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]};
const parse=s=>{check(typeof s==='string'&&/^-?\d+(?:\/[1-9]\d*)?$/.test(s),'invalid rational');let t=s.split('/');return q(t[0],t[1]||1)};
const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>add(a,[-b[0],b[1]]);
const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]),div=(a,b)=>{check(b[0]!==0n,'divide zero');return q(a[0]*b[1],a[1]*b[0])};
const pow=(a,n)=>q(a[0]**BigInt(n),a[1]**BigInt(n)),eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],le=(a,b)=>a[0]*b[1]<=b[0]*a[1],num=a=>Number(a[0])/Number(a[1]);
const choose=(n,k)=>{let v=1n;for(let j=1;j<=k;j++)v=v*BigInt(n-j+1)/BigInt(j);return v};
const rising=(a,n)=>{let v=q(1);for(let i=0;i<n;i++)v=mul(v,add(a,q(i)));return v};
const priors={U:[1,1],S:[2,2],A:[1,3]},srcs=['IID_BIN','CLUSTERED_BB_C2','CLUSTERED_BB_C8','INACTIVE_ZIB_Z1_8','INACTIVE_ZIB_Z1_4'];
const expected=new Set();for(let n of [4,8,12])for(let p of ['1/4','1/2'])for(let s of srcs)for(let pr of Object.keys(priors))expected.add([n,p,s,pr].join('|'));
check(d.research_id==='R179'&&d.status==='E1_ARTIFICIAL_EXACT_IID_WORKING_BETA_POSTERIOR','root status');
check(d.source_frozen_python_git_blob==='2d032513ce84141214b6b3f84df9c0ed9976a02b'&&d.source_frozen_result_sha256==='57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535','source identity');
check(d.source_count_mechanism_worlds===30&&d.prior_by_source_worlds===90&&d.full_source_count_PMF_cells===810&&d.new_E2===0&&d.new_E3===0&&d.true_real_human_or_historical_data_scored===false,'counts and evidence');
check(d.all_central_credible_interval_frequentist_coverages_exact===true&&d.all_two_independent_posterior_Beta_integral_and_CDF_routes_equal===true,'root verification flags');
check(JSON.stringify(d.prior_grid)==='[{"a":1,"b":3,"label":"A"},{"a":2,"b":2,"label":"S"},{"a":1,"b":1,"label":"U"}]'||
      Array.isArray(d.prior_grid)&&d.prior_grid.length===3&&new Set(d.prior_grid.map(p=>p.label+':'+p.a+':'+p.b)).size===3&&d.prior_grid.every(p=>['U:1:1','S:2:2','A:1:3'].includes(p.label+':'+p.a+':'+p.b)),'prior grid');
check(Array.isArray(d.worlds)&&d.worlds.length===90,'world count');
const seen=new Set();let cells=0,maxlog=0;
for(const w of d.worlds){
const n=w.sample_size,p=parse(w.true_marginal_p),s=w.training_mechanism,pr=w.prior_label,key=[n,w.true_marginal_p,s,pr].join('|');
check(expected.has(key)&&!seen.has(key),'duplicate or unknown world '+key);seen.add(key);
const [a,b]=priors[pr];check(w.prior_a===a&&w.prior_b===b&&w.working_iid_beta_posterior_under_misspecification===true,'prior identity');
check(Array.isArray(w.source_PMF)&&w.source_PMF.length===n+1&&Array.isArray(w.training_count_posteriors)&&w.training_count_posteriors.length===n+1,'row count');
const c=s==='CLUSTERED_BB_C2'?2:s==='CLUSTERED_BB_C8'?8:0,z=s==='INACTIVE_ZIB_Z1_8'?q(1,8):s==='INACTIVE_ZIB_Z1_4'?q(1,4):q(0);
check((s==='IID_BIN'&&w.source_R177_family==='BIN'&&w.source_R177_regime===0)||
(c>0&&w.source_R177_family==='BB'&&w.source_R177_regime===(c===2?0:2))||
(z[0]!==0n&&w.source_R177_family==='ZIB'&&w.source_R177_regime===(s.endsWith('1_8')?0:1)),'source family');
let total=q(0),mean=q(0),mse=q(0),varsum=q(0),cover=q(0),loss=0;
for(let k=0;k<=n;k++){
const wt=parse(w.source_PMF[k]),row=w.training_count_posteriors[k];
let pmf;
if(s==='IID_BIN')pmf=mul(q(choose(n,k)),mul(pow(p,k),pow(sub(q(1),p),n-k)));
else if(c>0){let C=q(c);pmf=mul(q(choose(n,k)),div(mul(rising(mul(C,p),k),rising(mul(C,sub(q(1),p)),n-k)),rising(C,n)))}
else {let active=div(p,sub(q(1),z));pmf=mul(sub(q(1),z),mul(q(choose(n,k)),mul(pow(active,k),pow(sub(q(1),active),n-k))));if(k===0)pmf=add(z,pmf)}
check(eq(wt,pmf),'source PMF '+key+' k='+k);
const A=a+k,B=b+n-k,D=A+B,mu=q(A,D),variance=q(A*B,D*D*(D+1));
let cdf=q(0);for(let j=A;j<D;j++)cdf=add(cdf,mul(q(choose(D-1,j)),mul(pow(p,j),pow(sub(q(1),p),D-1-j))));
const inside=le(q(1,40),cdf)&&le(cdf,q(39,40));
check(row.success_count===k&&eq(parse(row.source_weight),wt)&&row.posterior_shape_A===A&&row.posterior_shape_B===B,'row identity');
check(eq(parse(row.posterior_predictive_mean),mu)&&eq(parse(row.posterior_parameter_variance),variance)&&eq(parse(row.exact_posterior_cdf_at_true_p),cdf),'posterior math '+key+' k='+k);
check(row.truth_inside_central_95_credible_interval===inside&&row.independent_posterior_integral_parity===true,'coverage flag');
total=add(total,wt);mean=add(mean,mul(wt,mu));mse=add(mse,mul(wt,pow(sub(mu,p),2)));varsum=add(varsum,mul(wt,variance));if(inside)cover=add(cover,wt);
loss+=num(wt)*(-num(p)*Math.log(num(mu))-(1-num(p))*Math.log(1-num(mu)));cells++;
}
check(eq(total,q(1)),'PMF normalization');
for(let [name,val] of [['expected_posterior_predictive_mean',mean],['expected_bias_to_true_marginal',sub(mean,p)],['true_expected_posterior_predictive_mean_MSE',mse],['expected_working_posterior_parameter_variance',varsum],['true_MSE_over_expected_working_variance',div(mse,varsum)],['central_95_Beta_credible_interval_true_frequentist_coverage',cover]])check(eq(parse(w[name]),val),'aggregate '+key+' '+name);
let err=Math.max(Math.abs(loss-Number(w.expected_independent_future_event_logloss_numeric)),Math.abs(loss-Number(w.independent_decimal_future_event_logloss)));
check(err<1e-12,'logloss '+key);maxlog=Math.max(maxlog,err);
}
check(seen.size===90&&cells===810,'universe closure');
const illustration=d.fixed_n8_p_quarter_15_cases;check(Array.isArray(illustration)&&illustration.length===15,'illustration count');
const keys=illustration.map(w=>[w.sample_size,w.true_marginal_p,w.training_mechanism,w.prior_label].join('|'));
check(new Set(keys).size===15&&keys.every(k=>k.startsWith('8|1/4|')&&seen.has(k)),'illustration identity');
const byKey=new Map(d.worlds.map(w=>[[w.sample_size,w.true_marginal_p,w.training_mechanism,w.prior_label].join('|'),w]));
const canonical=v=>Array.isArray(v)?v.map(canonical):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):v;
for(let i=0;i<15;i++)check(JSON.stringify(canonical(illustration[i]))===JSON.stringify(canonical(byKey.get(keys[i]))),'illustration content '+keys[i]);
return {status:'PASS_INDEPENDENT_R179_EXACT_E1',worlds:90,source_cells:810,posterior_cells:810,maximum_logloss_absolute_difference:maxlog,evidence:'INTERNAL_NONBLIND_ARTIFICIAL_E1'};
}
if(typeof module!=='undefined'&&require.main===module){
const fs=require('node:fs'),crypto=require('node:crypto'),path=require('node:path');
try{const file=process.argv[2]||path.join(__dirname,'..','R179','R179_EXACT_RESULTS.json');const raw=fs.readFileSync(file);
const blob=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
if(blob!=='bce1490a8178b996b5a7322c0f9a15257feb5187')throw Error('original results blob mismatch');
console.log(JSON.stringify(audit(JSON.parse(raw.toString('utf8')))));}
catch(e){console.error('R179_AUDIT_FAIL: '+e.message);process.exitCode=1}
}
if(typeof module!=='undefined')module.exports={audit};
