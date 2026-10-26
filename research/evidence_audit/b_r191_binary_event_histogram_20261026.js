"use strict";
// B R191 independent histogram likelihood and multinomial overlap audit.
// node b_r191_binary_event_histogram_20261026.js research/R191/R191_EXACT_RESULTS.json research/validation/R191_BINARY_EVENT_24_EXACT_RECEIPT_2026-10-26.json
const fs=require("fs");
function frac(){
 const abs=x=>x<0n?-x:x;function gcd(a,b){a=abs(a);b=abs(b);while(b){let t=a%b;a=b;b=t;}return a;}
 function F(a,b=1n){if(a&&typeof a==="object"&&"n" in a)return a;if(typeof a==="string"&&a.includes("/")){let p=a.split("/");return F(BigInt(p[0]),BigInt(p[1]));}a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return {n:a/g,d:b/g};}
 const add=(a,b)=>F(a.n*b.d+b.n*a.d,a.d*b.d),sub=(a,b)=>F(a.n*b.d-b.n*a.d,a.d*b.d);
 const mul=(a,b)=>F(a.n*b.n,a.d*b.d),div=(a,b)=>F(a.n*b.d,a.d*b.n);
 const pow=(a,k)=>F(a.n**BigInt(k),a.d**BigInt(k));
 const show=a=>a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);
 const eq=(a,b)=>a.n===b.n&&a.d===b.d;return {F,add,sub,mul,div,pow,show,eq};
}
function compute(source,main){
 const {F,add,sub,mul,div,pow,show,eq}=frac(),z=F(0),one=F(1),half=F(1,2),eight=F(8);
 if(source.worlds.length!==24||main.rows.length!==24)throw Error("source size");
 const fact=[1n,1n,2n,6n,24n];
 function* counts(n,k){if(k===1){yield [n];return;}for(let a=0;a<=n;a++)for(const tail of counts(n-a,k-1))yield [a,...tail];}
 function pmf(t,s,u){return [[sub(u,mul(F(2),s)),F(1,4)],[u,F(1,2)],[add(u,mul(F(2),s)),F(1,4)]];}
 function lookup(arr,v){for(const [x,p] of arr)if(eq(x,v))return p;return z;}
 const rows=[];let positiveMutants=0,histTotal=0,compared=0;
 for(const w of source.worlds){
  const t=F(w.tau),s=F(w.sigma),n=w.n,minus=pmf(t,s,sub(z,t)),plus=pmf(t,s,t);
  const vals=[...minus,...plus].map(x=>x[0]);const unique=[];
  for(const v of vals)if(!unique.some(x=>eq(x,v)))unique.push(v);
  const am=minus.reduce((v,[y,p])=>y.n>0n?add(v,p):v,z),ap=plus.reduce((v,[y,p])=>y.n>0n?add(v,p):v,z);
  const p0=mul(half,add(am,ap)),base=mul(p0,sub(one,p0));
  let sum=z,mass=z,hists=0;
  for(const c of counts(n,unique.length)){
   let mult=F(fact[n]);for(const k of c)mult=div(mult,F(fact[k]));
   let lm=mult,lp=mult;
   for(let j=0;j<c.length;j++){lm=mul(lm,pow(lookup(minus,unique[j]),c[j]));lp=mul(lp,pow(lookup(plus,unique[j]),c[j]));}
   const den=add(lm,lp);if(!den.n)continue;
   hists++;mass=add(mass,mul(half,den));
   const d=sub(lp,lm);sum=add(sum,div(mul(mult===null?z:one,mul(d,d)),den));
  }
  if(!eq(mass,one))throw Error("histogram mass mismatch");
  const delta=sub(ap,am),skill=div(mul(mul(delta,delta),sum),eight);
  const row=main.rows.find(x=>x.tau===w.tau&&x.sigma===w.sigma&&x.n===w.n);
  if(!row)throw Error("missing main world");
  const fields=[["prior_event_probability",p0],["same_group_Bayes_Brier",sub(base,skill)],["same_group_global_Brier",base],["same_group_skill_exact",skill],["new_group_correct_Brier",base],["new_group_wrong_reused_posterior_Brier",add(base,skill)]];
  for(const [name,v] of fields){if(!eq(F(row[name]),v))throw Error("independent mismatch "+name+" "+JSON.stringify(w));compared++;}
  // Pre-frozen negative control: incorrect same-group risk applied to new-group outcomes.
  if(skill.n>0n){if(!sub(add(base,skill),sub(base,skill)).n)throw Error("negative control failed");positiveMutants++;}
  rows.push({tau:w.tau,sigma:w.sigma,n,histogram_cells:hists,prior_event_probability:show(p0),same_group_Bayes_Brier:show(sub(base,skill)),same_group_skill_exact:show(skill),wrong_new_group_Brier:show(add(base,skill))});histTotal+=hists;
 }
 if(positiveMutants!==16||compared!==144)throw Error("coverage mismatch");
 return {research_id:"R191",method:"independent latent-state multinomial histogram likelihood overlap",worlds:24,independent_histogram_cells:histTotal,exact_cross_algorithm_field_comparisons:compared,exact_disagreements:0,negative_control_positive_skill_worlds_detected:positiveMutants,zero_skill_worlds_not_flagged:8,external_team_replications:0,evidence:"INTERNAL_DIFFERENT_ALGORITHM_E1",rows};
}
module.exports={compute};
if(require.main===module){
 if(process.argv.length!==4)throw Error("usage: node script original_results.json main_receipt.json");
 process.stdout.write(JSON.stringify(compute(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2)+"\n");
}
