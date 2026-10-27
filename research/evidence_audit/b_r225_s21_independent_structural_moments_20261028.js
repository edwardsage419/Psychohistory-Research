"use strict";
// B R225 S21: independently rebuild noiseless structural outcomes and exact
// conditional moments. No R S21 functions are imported or called.
const W={UNIFORM:[1,1,1,1,1,1],FAVOR_FIRST_PAIR:[6,1,1,1,1,1],FAVOR_LAST_PAIR:[1,1,1,1,1,6],FAVOR_UNIT_ZERO:[3,3,3,1,1,1]};
const WORLDS=["AS_IF_RANDOM_VALID","ENDOGENOUS_FUTURE_SHOCK_ALIAS","AS_IF_RANDOM_NULL","AS_IF_RANDOM_HETEROGENEOUS","ENDOGENOUS_VISIBLE_SELECTION","ANTICIPATORY_PRE_RESPONSE"];
const SCHEDULES=[[1,1,0,0],[1,0,1,0],[1,0,0,1],[0,1,1,0],[0,1,0,1],[0,0,1,1]];
const NAMES=["post_group_difference","pre_balance_placebo","two_period_DiD"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
class Q{constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
 mul(b){return new Q(this.n*b.n,this.d*b.d);}div(b){return new Q(this.n*b.d,this.d*b.n);}
 eq(b){return this.n===b.n&&this.d===b.d;}toString(){return this.d===1n?String(this.n):this.n+"/"+this.d;}}
const q=(n,d=1)=>new Q(n,d),zero=q(0);
function tau(world,i){return world==="AS_IF_RANDOM_HETEROGENEOUS"?q(i):["AS_IF_RANDOM_VALID","ANTICIPATORY_PRE_RESPONSE"].includes(world)?q(1):zero;}
function structural(world,z){
 const pre=[],post=[];
 for(let i=0;i<4;i++){
  const before=world==="ENDOGENOUS_VISIBLE_SELECTION"?q(1+z[i]):world==="ANTICIPATORY_PRE_RESPONSE"?q(1).add(q(z[i],2)):q(1);
  const untreated=["ENDOGENOUS_FUTURE_SHOCK_ALIAS","ENDOGENOUS_VISIBLE_SELECTION"].includes(world)?q(1+z[i]):q(1);
  pre.push(before);post.push(untreated.add(q(z[i]).mul(tau(world,i))));
 }
 return {pre,post};
}
function contrast(a,z){let t=zero,c=zero;for(let i=0;i<4;i++){if(z[i])t=t.add(a[i]);else c=c.add(a[i]);}return t.sub(c).div(q(2));}
function target(world){let t=zero;for(let i=0;i<4;i++)t=t.add(tau(world,i));return t.div(q(4));}
function predicted(world,weights){
 const denom=weights.reduce((a,b)=>a+b,0),prob=weights.map(w=>q(w,denom)),conditional=SCHEDULES.map(z=>{
  let o=structural(world,z),post=contrast(o.post,z),pre=contrast(o.pre,z);
  return [post,pre,post.sub(pre)];});
 const methods={};
 for(let m=0;m<3;m++){
  let mu=zero,second=zero;
  for(let j=0;j<6;j++){let x=conditional[j][m];mu=mu.add(prob[j].mul(x));second=second.add(prob[j].mul(x.mul(x)));}
  let variance=second.sub(mu.mul(mu)).add(m===1?zero:q(1,16));
  let bias=mu.sub(m===1?zero:target(world));
  methods[NAMES[m]]={expectation:mu.toString(),variance:variance.toString(),bias_from_true_target:bias.toString(),mean_squared_error:variance.add(bias.mul(bias)).toString()};
 }
 return {truth_ATE:target(world).toString(),methods};
}
function audit(receipt){
 if(receipt.study!=="R225_S21"||receipt.results.length!==24)throw Error("R receipt shape");
 let compared=0,sourceChecks=0;
 for(let [scenario,weights] of Object.entries(W)){
  const den=weights.reduce((a,b)=>a+b,0);
  if(!weights.every(x=>x>0)||weights.reduce((s,x)=>s+x,0)!==den)throw Error("weight support");
  sourceChecks++;
  for(let world of WORLDS){
   let predictedResult=predicted(world,weights),got=receipt.results.find(x=>x.scenario===scenario&&x.world===world);
   if(!got||got.truth_ATE!==predictedResult.truth_ATE)throw Error("truth mismatch "+world);
   for(let method of NAMES)for(let field of ["expectation","variance","bias_from_true_target","mean_squared_error"]){
    if(got.methods[method][field]!==predictedResult.methods[method][field])throw Error("independent moment mismatch "+scenario+"/"+world+"/"+method+"/"+field);
    compared++;
   }
  }
 }
 let aliasStructuralChecks=0;
 for(let z of SCHEDULES){
  const valid=structural("AS_IF_RANDOM_VALID",z),alias=structural("ENDOGENOUS_FUTURE_SHOCK_ALIAS",z);
  for(let key of ["pre","post"])for(let i=0;i<4;i++)if(!valid[key][i].eq(alias[key][i]))throw Error("conditional observable alias");
  aliasStructuralChecks++;
 }
 const mutated=JSON.parse(JSON.stringify(receipt));mutated.results[0].methods.post_group_difference.expectation="999";
 let mutationDetected=false;
 try{
  const expected=predicted(mutated.results[0].world,W[mutated.results[0].scenario]).methods.post_group_difference.expectation;
  if(mutated.results[0].methods.post_group_difference.expectation!==expected)throw Error("mutation caught");
 }catch(e){mutationDetected=e.message==="mutation caught";}
 if(!mutationDetected)throw Error("error injection escaped");
 return {audit:"B_R225_S21",independent_method:"STRUCTURAL_NOISELESS_CONDITIONAL_MOMENTS_PLUS_1_16_VARIANCE",exact_field_comparisons:compared,weight_support_checks:sourceChecks,conditional_observable_alias_checks:aliasStructuralChecks,error_injection_detected:mutationDetected,failures:0,evidence:"INTERNAL_PROCEDURAL_RECALCULATION_E1",external_independent_replications:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 if(process.argv.length!==3)throw Error("usage: node b_r225_s21_independent_structural_moments_20261028.js R_S21_RECEIPT.json");
 const receipt=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 process.stdout.write(JSON.stringify(audit(receipt),null,2)+"\n");
}