"use strict";
/* R158 independent exact rational conditional Poisson likelihood-ratio audit.
   Run: node r158_exact_poisson_ratio.js path/to/R158_EXACT_RESULTS.json */
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a||1n};
const q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(!d)throw Error("zero");let g=gcd(n,d);return [n/g,d/g]};
const parse=s=>{let p=String(s).split("/");return q(p[0],p[1]||"1")};
const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
const add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const div=(x,y)=>q(x[0]*y[1],x[1]*y[0]);
const pow=(x,n)=>{let z=q(1);for(let i=0;i<n;i++)z=mul(z,x);return z};
const num=x=>Number(x[0])/Number(x[1]);
const fmt=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
function audit(archive){
  if(archive.research_id!=="R158"||archive.worlds.length!==60)throw Error("wrong frozen archive");
  const baseline=new Map();
  for(const w of archive.worlds)if(w.alpha==="0")baseline.set(w.history_id+"|"+w.mu,w.total_log_score);
  if(baseline.size!==12)throw Error("missing baseline");
  let matches=0, nonzero=0, h0=0, alpha0=0,maxdiff=0,first=null;
  for(const w of archive.worlds){
    const mu=parse(w.mu),alpha=parse(w.alpha),hist=w.observed_artificial_counts;
    let prev=0,S=0,R=q(1),logR=0;
    for(const n of hist){
      const factor=div(add(mu,mul(alpha,q(prev))),mu);
      R=mul(R,pow(factor,n));
      logR+=n*Math.log(num(factor));
      S+=prev;prev=n;
    }
    const logRatio=logR-num(alpha)*S;
    const archived=w.total_log_score-baseline.get(w.history_id+"|"+w.mu);
    const diff=Math.abs(logRatio-archived);
    if(diff>2e-11)throw Error("likelihood ratio mismatch "+w.case_id+" "+diff);
    maxdiff=Math.max(maxdiff,diff);matches++;
    if(w.alpha==="0"){alpha0++;if(fmt(R)!=="1"||S<0)throw Error("alpha=0 wrong")}
    else nonzero++;
    if(w.history_id===0){h0++;if(fmt(R)!=="1"||logRatio!==0)throw Error("H0 alpha wrong")}
    if(w.history_id===1&&w.mu==="1"&&w.alpha==="1/2")first={history:"H1",mu:"1",alpha:"1/2",rational_R:fmt(R),lag_exposure_S:S,log_ratio:logRatio,archived_log_ratio:archived};
  }
  if(matches!==60||nonzero!==48||alpha0!==12||h0!==15||!first)throw Error("wrong count");
  const H1=[1,0,2,0,3,0,2,1],mu=q(1),alpha=q(1,2);
  let prev=0,lagR=q(1),sameR=q(1),S=0;
  for(const n of H1){
    lagR=mul(lagR,pow(div(add(mu,mul(alpha,q(prev))),mu),n));
    sameR=mul(sameR,pow(div(add(mu,mul(alpha,q(n))),mu),n));
    S+=prev;prev=n;
  }
  const correct=Math.log(num(lagR))-num(alpha)*S;
  if(Math.abs(correct-Math.log(num(lagR)))<1e-9)throw Error("missing exposure not rejected");
  if(fmt(lagR)===fmt(sameR))throw Error("same-time leakage not rejected");
  return {status:"PASS_BOUNDED_INTERNAL_E1",archive_worlds:60,exact_rational_ratio_worlds:matches,nonzero_alpha_worlds:nonzero,zero_alpha_worlds:alpha0,H0_alpha_invariance_worlds:h0,max_absolute_log_ratio_rounding_diff:maxdiff,example:first,negative_controls:{omitted_exponential_exposure:"REJECTED",contemporaneous_count_instead_of_lag:"REJECTED",causal_claim:"NOT_AUTHORIZED"},E2_new:0,E3_new:0,external_replication:false};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==3)throw Error("archive path required");
 process.stdout.write(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2)+"\n");
}
