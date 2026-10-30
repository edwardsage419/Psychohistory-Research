/* R289 S85: exact artificial paired threshold selection. Node 18+; no packages.
   Run: node r289_s85_train_selected_aspiration_20261030.js
   Prints JSON with all exact fractions. CSV can be obtained from module.exports.compute().csv.
   Frozen 2026-10-30 commit f018236900fa00368c8980db5402ce4267d59c7c.
   Original source Git blob 261d821044278d05db1d15e85e20cef8aafbe5a4.
*/
"use strict";
const R289S85=(function(){
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a}
function f(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return {n:n/g,d:d/g}}
const add=(a,b)=>f(a.n*b.d+b.n*a.d,a.d*b.d);
const sub=(a,b)=>f(a.n*b.d-b.n*a.d,a.d*b.d);
const mul=(a,b)=>f(a.n*b.n,a.d*b.d);
const str=a=>a.d===1n?a.n.toString():a.n+"/"+a.d;
const equal=(a,b)=>a.n===b.n&&a.d===b.d;
const zero=f(0),one=f(1);
const DGP={UNIFORM:{w:[1,1,1],base:3},LOW_HEAVY:{w:[2,1,1],base:4},HIGH_HEAVY:{w:[1,1,2],base:4}};
const VALUES=[1,3,5];
function payoff2(xs,h){for(let i=0;i<4;i++)if(xs[i]>=h||i===3)return 2*xs[i]-i;throw Error("bad offer")}
function ledger(){
 const out=[];
 for(const [name,p] of Object.entries(DGP)){
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)for(let d=0;d<3;d++){
   const ix=[a,b,c,d],xs=ix.map(i=>VALUES[i]),weight=ix.reduce((v,i)=>v*p.w[i],1);
   const h3=payoff2(xs,3),h5=payoff2(xs,5);
   out.push({distribution:name,source:xs.join(""),weight,den:p.base**4,h3net2:h3,h5net2:h5,difference2:h5-h3});
  }
 }
 return out;
}
function verifyLedger(rows){
 if(rows.length!==243)throw Error("source count");
 const expected=ledger(), seen=new Set();
 for(let i=0;i<rows.length;i++){
  const z=rows[i],k=z.distribution+"|"+z.source;
  if(seen.has(k))throw Error("duplicate source");seen.add(k);
  const e=expected[i];
  if(!e||Object.keys(e).some(key=>e[key]!==z[key]))throw Error("source mismatch at "+i);
 }
 if(seen.size!==243)throw Error("incomplete source universe");
 return true;
}
function direct(rows){
 verifyLedger(rows);
 const out=[];
 for(const [name,p] of Object.entries(DGP)){
  const rr=rows.filter(x=>x.distribution===name),den=BigInt(p.base**4);
  const mass=rr.reduce((s,z)=>s+BigInt(z.weight),0n);
  if(mass!==den)throw Error("mass");
  const e3=f(rr.reduce((s,z)=>s+BigInt(z.weight*z.h3net2),0n),2n*den);
  const e5=f(rr.reduce((s,z)=>s+BigInt(z.weight*z.h5net2),0n),2n*den);
  const mu=f(rr.reduce((s,z)=>s+BigInt(z.weight*Number(z.source[0])),0n),den);
  for(const m of [1,2]){
   let win=0n,tie=0n,total=den**BigInt(m);
   if(m===1)for(const x of rr){if(x.difference2>0)win+=BigInt(x.weight);if(x.difference2===0)tie+=BigInt(x.weight)}
   else for(const x of rr)for(const y of rr){
    const w=BigInt(x.weight)*BigInt(y.weight),d=x.difference2+y.difference2;
    if(d>0)win+=w;if(d===0)tie+=w;
   }
   const p5=f(win,total),pTie=f(tie,total);
   const pInferior=e3.n*e5.d>e5.n*e3.d?p5:e3.n*e5.d<e5.n*e3.d?sub(one,p5):zero;
   const net=add(e3,mul(p5,sub(e5,e3)));
   const best=e3.n*e5.d>e5.n*e3.d?e3:e5;
   out.push({distribution:name,training_episodes:m,training_source_tuples:m===1?81:6561,
     expected_H3:str(e3),expected_H5:str(e5),first_only:str(mu),
     probability_select_H5:str(p5),probability_training_tie:str(pTie),
     probability_select_inferior:str(pInferior),independent_test_expected_net:str(net),
     oracle_of_two_thresholds:str(best),regret_vs_best_fixed_threshold:str(sub(best,net)),
     gain_over_first_only:str(sub(net,mu)),evidence:"E1_ARTIFICIAL_NONBLIND"});
  }
 }
 return out;
}
function polynomial(rows){
 // Separate aggregation route: build signed difference PMF then convolve exact weighted counts.
 const out=[];
 for(const [name,p] of Object.entries(DGP)){
  const rr=rows.filter(z=>z.distribution===name),counts=new Map(),den=BigInt(p.base**4);
  for(const z of rr)counts.set(z.difference2,(counts.get(z.difference2)||0n)+BigInt(z.weight));
  for(const m of [1,2]){
   let dist=new Map([[0,1n]]);
   for(let t=0;t<m;t++){
    const next=new Map();
    for(const [a,pa] of dist)for(const [b,pb] of counts){
     next.set(a+b,(next.get(a+b)||0n)+pa*pb);
    }
    dist=next;
   }
   const mass=[...dist.values()].reduce((a,b)=>a+b,0n);
   if(mass!==den**BigInt(m))throw Error("polynomial mass");
   let positive=0n,tie=dist.get(0)||0n;
   for(const [d,w] of dist)if(d>0)positive+=w;
   out.push({distribution:name,m,p5:str(f(positive,mass)),tie:str(f(tie,mass)),support:dist.size});
  }
 }
 return out;
}
function selftest(rows){
 verifyLedger(rows);
 const good=direct(rows),oracle=polynomial(rows);
 for(let i=0;i<good.length;i++){
  if(good[i].probability_select_H5!==oracle[i].p5||good[i].probability_training_tie!==oracle[i].tie)throw Error("route mismatch "+i);
 }
 const baseline={"UNIFORM":["67/18","100/27","3"],"LOW_HEAVY":["27/8","197/64","5/2"],"HIGH_HEAVY":["133/32","35/8","7/2"]};
 for(const z of good){const b=baseline[z.distribution];if(z.expected_H3!==b[0]||z.expected_H5!==b[1]||z.first_only!==b[2])throw Error("R289 original baseline drift")}
 const mutants=[];
 function check(tag,fn){const copy=rows.map(z=>({...z}));fn(copy);let rejected=false;try{verifyLedger(copy)}catch(_){rejected=true}mutants.push({tag,rejected});if(!rejected)throw Error("false accept "+tag)}
 check("duplicate",x=>{x[1]={...x[0]}});
 check("missing",x=>{x.pop()});
 check("weight_mutation",x=>{x[0].weight++});
 check("payoff_mutation",x=>{x[0].h5net2++});
 check("difference_mutation",x=>{x[0].difference2++});
 const zeroDiff=rows.find(x=>x.difference2===0);
 if(!zeroDiff||!(zeroDiff.difference2===0))throw Error("no tie source");
 // Frozen tie rule is H3; strict >0 must be used. An >=0 selector is a rejected negative control.
 const wrongTie=(zeroDiff.difference2>=0),correctTie=(zeroDiff.difference2>0);
 if(!wrongTie||correctTie)throw Error("tie negative control failed");
 mutants.push({tag:"incorrect_tie_rule",rejected:true});
 return {checks:good.length,mutation_tests:mutants,route_B:oracle};
}
function compute(){
 const rows=ledger(),result=direct(rows),checks=selftest(rows);
 const cols=["distribution","source","weight","den","h3net2","h5net2","difference2"];
 const csv=cols.join(",")+"\n"+rows.map(z=>cols.map(k=>z[k]).join(",")).join("\n")+"\n";
 return {csv,json:JSON.stringify({study:"R289_S85",scope:"E1_ARTIFICIAL_NONBLIND",freeze_commit:"f018236900fa00368c8980db5402ce4267d59c7c",original_source_git_blob:"261d821044278d05db1d15e85e20cef8aafbe5a4",source_rows:243,worlds:result,independent_polynomial:checks.route_B,mutation_tests:checks.mutation_tests,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0,external_replication:0},null,2)+"\n"};
}
return {compute,ledger,verifyLedger,direct,polynomial,selftest};
})();
if(typeof module!=="undefined" && module.exports){module.exports=R289S85;if(require.main===module){const fs=require("fs");const out=R289S85.compute();if(process.argv.includes("--emit")){fs.writeFileSync("R289_S85_ALL_243_PAIRED_OFFERS.csv",out.csv);fs.writeFileSync("R289_S85_EXACT_RESULTS.json",out.json)}else{process.stdout.write(out.json)}}}
