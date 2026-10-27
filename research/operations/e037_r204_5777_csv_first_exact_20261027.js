"use strict";
// Run from repository root: node research/operations/e037_r204_5777_csv_first_exact_20261027.js
const fs=require("node:fs");
function audit(csv,receipt){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n};
 class Q{constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}const g=gcd(n,d);this.n=n/g;this.d=d/g}add(o){o=q(o);return new Q(this.n*o.d+o.n*this.d,this.d*o.d)}sub(o){o=q(o);return new Q(this.n*o.d-o.n*this.d,this.d*o.d)}mul(o){o=q(o);return new Q(this.n*o.n,this.d*o.d)}div(o){o=q(o);return new Q(this.n*o.d,this.d*o.n)}eq(o){o=q(o);return this.n===o.n&&this.d===o.d}str(){return this.d===1n?String(this.n):this.n+"/"+this.d}}
 const q=x=>x instanceof Q?x:typeof x==="string"&&x.includes("/")?new Q(...x.split("/")):new Q(x);
 const lines=csv.trim().split(/\r?\n/),heads=lines.shift().split(",");
 const rows=lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[heads[i],v])));
 const splits={EXTRAPOLATION:[[0,1,2],[3,4]],INTERPOLATION:[[0,2,4],[1,3]],GAP:[[0,1,4],[2,3]]};
 const features={IID:[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]],CONSTANT:[[1,1,1,1,1]],ALTERNATING:[[1,-1,1,-1,1]],LINEAR:[[-2,-1,0,1,2]]};
 const loss=(p,f)=>p.reduce((s,z,j)=>s.add(z.sub(f[j]).mul(z.sub(f[j]))),q(0)).div(2);
 const invert=a=>{const t=a.map((row,i)=>[...row,...[0,1,2].map(j=>q(i===j?1:0))]);for(let i=0;i<3;i++){let k=i;while(t[k][i].n===0n)k++;[t[k],t[i]]=[t[i],t[k]];const p=t[i][i];t[i]=t[i].map(z=>z.div(p));for(let j=0;j<3;j++)if(j!==i){const f=t[j][i];t[j]=t[j].map((z,h)=>z.sub(f.mul(t[i][h])))}}return t.map(row=>row.slice(3))};
 const predictors={};
 for(const [split,[train,test]] of Object.entries(splits))for(const [kernel,phi] of Object.entries(features)){
  const cov=(i,j)=>phi.reduce((s,v)=>s+v[i]*v[j],0);
  const inv=invert(train.map((i,h)=>train.map((j,l)=>q(cov(i,j)+(h===l?1:0)))));
  predictors[split+"|"+kernel]=test.map(i=>train.map((_,h)=>train.reduce((s,j,l)=>s.add(q(cov(i,j)).mul(inv[l][h])),q(0))));
 }
 const groups=new Map();let checks=0;
 const check=(ok,label)=>{checks++;if(!ok)throw Error("CHECK_FAILED "+label)};
 for(const row of rows){
  const split=row.split,kernel=row.true_kernel_source,phi=features[kernel],factors=row.true_source_latent_factors.split("|").map(Number),noise=row.true_observation_noise.split("|").map(Number);
  const [train,test]=splits[split];check(factors.length===phi.length&&noise.length===3,"factor");
  const f=Array.from({length:5},(_,i)=>phi.reduce((s,v,j)=>s+v[i]*factors[j],0));
  const y=train.map((i,j)=>f[i]+noise[j]),held=test.map(i=>f[i]);
  check(y.join("|")===row.observed_train_y,"train");check(held.join("|")===row.heldout_true_latent_f,"heldout");
  check(q(row.real_original_source_probability).eq(new Q(1n,BigInt(2**(factors.length+3)))),"mass");
  const predict=k=>predictors[split+"|"+k].map(w=>w.reduce((s,z,j)=>s.add(z.mul(y[j])),q(0)));
  const selected=predict(row.fitted_kernel_from_training_only);
  check(selected.map(z=>z.str()).join("|")===row.heldout_latent_predicted_mean,"pred");
  check(loss(selected,held.map(q)).eq(q(row.heldout_latent_MSE_two_sites_exact)),"loss");
  const key=split+"|"+kernel;if(!groups.has(key))groups.set(key,[]);
  groups.get(key).push({y:y.join("|"),f:held.map(q),pred:selected,trueGP:predict(kernel)});
 }
 for(const w of receipt.worlds){
  const atoms=groups.get(w.split+"|"+w.true_kernel);check(atoms.length===w.source_atoms,"count");
  const byY=new Map();for(const x of atoms){if(!byY.has(x.y))byY.set(x.y,[]);byY.get(x.y).push(x)}
  check(byY.size===w.distinct_observed_y,"support");
  let bayes=q(0),trueGP=q(0),selected=q(0),zero=q(0),excess=q(0);
  for(const arr of byY.values()){
   const mean=[0,1].map(j=>arr.reduce((s,x)=>s.add(x.f[j]),q(0)).div(arr.length));
   for(const x of arr){bayes=bayes.add(loss(mean,x.f).div(atoms.length));trueGP=trueGP.add(loss(x.trueGP,x.f).div(atoms.length));selected=selected.add(loss(x.pred,x.f).div(atoms.length));zero=zero.add(loss([q(0),q(0)],x.f).div(atoms.length));excess=excess.add(loss(x.pred,mean).div(atoms.length))}
   check(arr.every(x=>x.pred.every((z,j)=>z.eq(arr[0].pred[j]))),"same visible input");
  }
  check(bayes.eq(q(w.risk_exact.bayes)),"bayes");check(trueGP.eq(q(w.risk_exact.gp_true)),"trueGP");
  check(selected.eq(q(w.risk_exact.gp_selected)),"selectedGP");check(zero.eq(q(w.risk_exact.zero)),"zero");
  check(selected.sub(bayes).eq(excess),"orthogonality");
 }
 check(rows.length===912,"total rows");check(receipt.worlds.length===12,"world count");
 return {checks,rows:rows.length,worlds:receipt.worlds.length,all_passed:true};
}
if(typeof require==="function"&&require.main===module){
 const csv=fs.readFileSync("research/R204/R204_ALL_912_REAL_SOURCE_GP_TRAIN_AND_HELDOUT.csv","utf8");
 const receipt=JSON.parse(fs.readFileSync("research/validation/R204_DISCRETE_BAYES_ORACLE_12_WORLDS_EXACT_RECEIPT_2026-10-27.json","utf8"));
 console.log(JSON.stringify(audit(csv,receipt)));
}
