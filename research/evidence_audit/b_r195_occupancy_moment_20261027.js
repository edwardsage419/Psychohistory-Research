"use strict";
// Independent B algorithm: propagate raw occupancy-count moments across Markov states.
function gcdB(a,b){while(b!==0n){const r=a%b;a=b;b=r}return a<0n?-a:a}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero");if(d<0n){n=-n;d=-d}const g=gcdB(n<0n?-n:n,d);return {n:n/g,d:d/g}}
function parse(s){let a=String(s).split("/");return F(a[0],a.length===1?1:a[1])}
function add(a,b){return F(a.n*b.d+b.n*a.d,a.d*b.d)}
function minus(a,b){return F(a.n*b.d-b.n*a.d,a.d*b.d)}
function multiply(a,b){return F(a.n*b.n,a.d*b.d)}
function divide(a,b){return F(a.n*b.d,a.d*b.n)}
function display(a){return a.n+"/"+a.d}
const zero=F(0),one=F(1),two=F(2),n64=F(64),n4096=F(4096);
function evaluate(kernel,j){
 const T=kernel.transition_exact_matrix.map(row=>row.map(parse));
 const pi=kernel.target_exact_pi.map(parse);
 let mass=pi.slice(),first=pi.map((p,i)=>i===j?p:zero),second=first.slice(),normalization_checks=0;
 for(let t=1;t<64;t++){
  const nm=[zero,zero,zero],nf=[zero,zero,zero],ns=[zero,zero,zero];
  for(let i=0;i<3;i++)for(let h=0;h<3;h++){
   const transition=T[i][h],indicator=h===j?one:zero;
   nm[h]=add(nm[h],multiply(mass[i],transition));
   nf[h]=add(nf[h],multiply(add(first[i],multiply(mass[i],indicator)),transition));
   const update=add(add(second[i],multiply(two,multiply(indicator,first[i]))),multiply(mass[i],indicator));
   ns[h]=add(ns[h],multiply(update,transition));
  }
  mass=nm;first=nf;second=ns;
  if(display(mass.reduce(add,zero))!=="1/1")throw Error("mass not normalized");
  normalization_checks++;
 }
 const ES=first.reduce(add,zero),ES2=second.reduce(add,zero);
 const variance=divide(minus(ES2,multiply(ES,ES)),n4096);
 const V=multiply(pi[j],minus(one,pi[j]));
 if(display(ES)!==display(multiply(n64,pi[j])))throw Error("occupancy expectation drift");
 return {variance:display(variance),ESS:display(divide(V,variance)),normalization_checks,ES:display(ES),ES2:display(ES2)};
}
function audit(source,main){
 let compared=0,normalization=0,records=[];
 for(const kernel of source.kernels)for(let j=0;j<3;j++){
  const r=main.rows.find(x=>x.target===kernel.target&&x.q===kernel.proposal_edge_probability_q&&x.indicator_state===j);
  if(!r)throw Error("missing main receipt case");
  const b=evaluate(kernel,j);
  if(b.variance!==r.sample_mean_variance||b.ESS!==r.ESS_N64)throw Error("independent moment mismatch");
  compared+=2;normalization+=b.normalization_checks;
  records.push({target:kernel.target,q:kernel.proposal_edge_probability_q,j,variance:b.variance,ESS:b.ESS});
 }
 const skew=source.kernels.find(k=>k.target==="SKEW"&&k.proposal_edge_probability_q==="1/8");
 const e0=evaluate(skew,0);
 const pi2=parse(skew.target_exact_pi[2]),pi0=parse(skew.target_exact_pi[0]);
 const wrong=minus(parse(e0.ES2),multiply(multiply(n64,pi2),multiply(n64,pi2)));
 const wrongVar=divide(wrong,n4096);
 if(display(wrongVar)===e0.variance||display(pi0)===display(pi2))throw Error("wrong mean negative control failed");
 return {status:"PASS_BOUNDED_INTERNAL_E1_DIFFERENT_ALGORITHM",new_indicator_cases:16,original_indicator_rechecked:8,exact_variance_and_ESS_fields_compared:compared,mass_normalization_checks:normalization,negative_controls_rejected:1,method:"state-occupancy first/second moment recursion, no covariance arrays",new_E2:0,new_E3:0,external_replication:0};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");if(process.argv.length!==4)throw Error("usage: node b_r195_moment.js original_kernels.json r195_receipt.json");console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2))}
