// R300 S96 exact finite HMM forecast risk. Frozen e7d5d6e7f9a82210fb5151c77a492303e1b20110.
// All probabilities are exact reduced BigInt rationals. Synthetic E1 only.
"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
class F{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 static of(x){if(x instanceof F)return x;let p=String(x).split("/");return new F(p[0],p[1]||1);}
 add(b){b=F.of(b);return new F(this.n*b.d+b.n*this.d,this.d*b.d);}
 sub(b){b=F.of(b);return new F(this.n*b.d-b.n*this.d,this.d*b.d);}
 mul(b){b=F.of(b);return new F(this.n*b.n,this.d*b.d);}
 div(b){b=F.of(b);return new F(this.n*b.d,this.d*b.n);}
 eq(b){b=F.of(b);return this.n===b.n&&this.d===b.d;}
 toString(){return this.d===1n?String(this.n):this.n+"/"+this.d;}
}
const z=F.of(0),one=F.of(1),half=F.of("1/2");
const stays=["1/4","1/2","3/4"],emissions=["1/2","3/4","1"];
const trueStays=["1/2","3/4"],bits=Array.from({length:16},(_,i)=>i.toString(2).padStart(4,"0"));
function filt(a,q,history){
 a=F.of(a);q=F.of(q);
 let w0=half,w1=half;
 for(let t=0;t<history.length;t++){
   if(t){let x=w0.mul(a).add(w1.mul(one.sub(a)));let y=w1.mul(a).add(w0.mul(one.sub(a)));w0=x;w1=y;}
   if(history[t]==="0"){w0=w0.mul(q);w1=w1.mul(one.sub(q));}
   else {w0=w0.mul(one.sub(q));w1=w1.mul(q);}
 }
 let evidence=w0.add(w1);if(evidence.eq(z))throw Error("zero evidence");
 let posterior=w1.div(evidence);
 let nextHidden=posterior.mul(a).add(one.sub(posterior).mul(one.sub(a)));
 let nextObserved=nextHidden.mul(q).add(one.sub(nextHidden).mul(one.sub(q)));
 return {evidence,posterior,nextObserved};
}
function run(){
 const rows=[],groups=[];
 for(let aTrue of trueStays){
  const world=aTrue==="1/2"?"IID_HIDDEN_NEGATIVE_CONTROL":"PERSISTENT_HMM";
  const trueInfo=bits.map(prefix=>({prefix,...filt(aTrue,"3/4",prefix)}));
  if(!trueInfo.reduce((v,x)=>v.add(x.evidence),z).eq(one))throw Error("mass");
  const oracle=trueInfo.reduce((v,x)=>v.add(x.evidence.mul(x.nextObserved).mul(one.sub(x.nextObserved))),z);
  for(let a of stays)for(let q of emissions){
   let risk=z,excess=z;
   for(let info of trueInfo){
    const c=filt(a,q,info.prefix),p=info.nextObserved,f=c.nextObserved;
    const conditional=p.mul(one.sub(f).mul(one.sub(f))).add(one.sub(p).mul(f.mul(f)));
    const weighted=info.evidence.mul(conditional);
    const ex=info.evidence.mul(f.sub(p).mul(f.sub(p)));
    risk=risk.add(weighted);excess=excess.add(ex);
    rows.push({world,true_stay:aTrue,true_emission:"3/4",prefix:info.prefix,candidate_stay:a,candidate_emission:q,true_prefix_mass:info.evidence.toString(),true_next1:p.toString(),candidate_prefix_evidence:c.evidence.toString(),candidate_next1:f.toString(),conditional_brier:conditional.toString(),weighted_brier:weighted.toString(),weighted_excess:ex.toString()});
   }
   if(!risk.sub(oracle).eq(excess))throw Error("Brier decomposition");
   if(a===aTrue&&q==="3/4"&&!excess.eq(z))throw Error("oracle mismatch");
   if(aTrue==="1/2"&&!oracle.eq(F.of("1/4")))throw Error("iid oracle");
   groups.push({world,true_stay:aTrue,candidate_stay:a,candidate_emission:q,prefixes:16,expected_brier:risk.toString(),oracle_brier:oracle.toString(),excess_brier:excess.toString(),fixed_half_brier:"1/4"});
  }
 }
 if(rows.length!==288||groups.length!==18)throw Error("cardinality");
 if(new Set(rows.map(r=>[r.world,r.prefix,r.candidate_stay,r.candidate_emission].join("|"))).size!==288)throw Error("duplicate");
 for(let r of rows){if(r.world==="IID_HIDDEN_NEGATIVE_CONTROL"&&r.true_next1!=="1/2")throw Error("IID truth");if((r.candidate_stay==="1/2"||r.candidate_emission==="1/2")&&r.candidate_next1!=="1/2")throw Error("uninformative candidate");}
 const columns=["world","true_stay","true_emission","prefix","candidate_stay","candidate_emission","true_prefix_mass","true_next1","candidate_prefix_evidence","candidate_next1","conditional_brier","weighted_brier","weighted_excess"];
 const csv=columns.join(",")+"\n"+rows.map(r=>columns.map(k=>r[k]).join(",")).join("\n")+"\n";
 const result={research_id:"R300",extension:"S96-v1",freeze_commit:"e7d5d6e7f9a82210fb5151c77a492303e1b20110",B_plan_commit:"cd0eb73dd9b52b9a98a0a40d9f9628257bc44752",scope:"E1_EXACT_KNOWN_PARAMETER_MISSPECIFIED_HMM_FORECAST_RISK",source_rows:288,distinct_true_prefixes:32,group_count:18,results:groups,original_R300_acceptance:"UNCHANGED",R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0,external_replication:"NOT_RUN"};
 return {rows,groups,csv,json:JSON.stringify(result,null,2)+"\n"};
}
if(typeof module!=="undefined")module.exports={run,filt,F};
