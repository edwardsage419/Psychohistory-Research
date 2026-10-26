"use strict";
// B R189: independent two latent-state product enumeration, no use of frozen PMF endpoints.
// node research/evidence_audit/b_r189_latent_extreme_20261026.js
function audit(original,receipt){
 const abs=x=>x<0n?-x:x;
 function gcd(a,b){a=abs(a);b=abs(b);while(b){let z=a%b;a=b;b=z;}return a||1n;}
 function R(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
 const add=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>add(a,[-b[0],b[1]]),mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]),div=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
 const parse=s=>{let p=String(s).split("/");return R(p[0],p[1]||1);};
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
 const pow=(a,n)=>R(a[0]**BigInt(n),a[1]**BigInt(n));
 const one=R(1),two=R(2);
 const success=odds=>div(odds,add(one,odds));
 if(receipt.cases.length!==48||original.all_worlds.length!==24)throw Error("source size");
 let checks=0,mutation=0,negative=0;
 for(const row of receipt.cases){
  const w=original.all_worlds[row.world],n=w.n_per_cluster,o=parse(w.source_base_odds_o),t=parse(w.source_conditional_odds_multiplier_t),h=R(w.source_latent_odds_multiplier_h);
  const odds=mul(o,row.x===0?one:t),p1=success(mul(odds,h)),p2=success(div(odds,h));
  const mu=div(add(p1,p2),two),true0=div(add(pow(sub(one,p1),n),pow(sub(one,p2),n)),two);
  const truen=div(add(pow(p1,n),pow(p2,n)),two),ind0=pow(sub(one,mu),n),indn=pow(mu,n);
  const target={mu,true_zero:true0,independent_zero:ind0,zero_excess:sub(true0,ind0),true_all_success:truen,independent_all_success:indn,all_success_excess:sub(truen,indn),total_extreme_excess:add(sub(true0,ind0),sub(truen,indn))};
  for(const [k,v] of Object.entries(target)){if(!eq(v,parse(row[k])))throw Error("B mismatch "+row.world+" "+row.x+" "+k);checks++;}
 }
 // Deliberate corrupted independent marginal baseline: use mu + 1/100.
 const row=receipt.cases.find(x=>x.h===3),bad=pow(sub(one,add(parse(row.mu),R(1,100))),row.n);
 if(!eq(bad,parse(row.independent_zero)))mutation++;
 if(mutation!==1)throw Error("mutation not detected");
 return {status:"PASS_INTERNAL_METHOD_INDEPENDENT_E1",source_worlds:24,conditions:48,exact_field_identities:checks,latent_state_enumeration:"two symmetric odds multipliers independently calculated",bad_marginal_mutation_detected:mutation,real_human_E2:0,historical_E3:0,external_independent_replication:false};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
 const o=JSON.parse(fs.readFileSync(path.join(root,"research/R189/R189_EXACT_RESULTS.json"),"utf8"));
 const r=JSON.parse(fs.readFileSync(path.join(root,"research/validation/R189_CLUSTER_EXTREME_TAIL_48_EXACT_RECEIPT_2026-10-26.json"),"utf8"));
 process.stdout.write(JSON.stringify(audit(o,r),null,2)+"\n");
}
