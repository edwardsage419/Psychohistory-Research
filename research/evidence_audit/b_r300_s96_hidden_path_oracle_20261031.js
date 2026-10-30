// Independent R300 S96 audit. Full latent-path enumeration; does not import R source.
// Frozen audit plan cd0eb73dd9b52b9a98a0a40d9f9628257bc44752. Nonblind E1.
"use strict";
function frac(s){let a=String(s).split("/"),n=BigInt(a[0]),d=BigInt(a[1]||"1");if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let x=n<0n?-n:n,y=d;while(y){let z=x%y;x=y;y=z;}return {n:n/x,d:d/x};}
const Z=frac("0"),O=frac("1"),H=frac("1/2");
function plus(a,b){return frac((a.n*b.d+b.n*a.d)+"/"+(a.d*b.d));}
function neg(a){return {n:-a.n,d:a.d};}
function minus(a,b){return plus(a,neg(b));}
function times(a,b){return frac(a.n*b.n+"/"+(a.d*b.d));}
function over(a,b){return frac(a.n*b.d+"/"+(a.d*b.n));}
function same(a,b){return a.n===b.n&&a.d===b.d;}
function fmt(a){return a.d===1n?String(a.n):a.n+"/"+a.d;}
function paths(n){return Array.from({length:2**n},(_,v)=>v.toString(2).padStart(n,"0"));}
function joint(hidden,observed,stay,quality){
 let p=H;
 for(let i=0;i<hidden.length;i++){
  if(i>0)p=times(p,hidden[i]===hidden[i-1]?stay:minus(O,stay));
  p=times(p,hidden[i]===observed[i]?quality:minus(O,quality));
 }
 return p;
}
function evidence(obs,stay,quality){
 let p=Z;for(let h of paths(obs.length))p=plus(p,joint(h,obs,stay,quality));return p;
}
function predict(obs,stay,quality){
 let den=evidence(obs,stay,quality),num=Z;
 if(same(den,Z))throw Error("zero candidate evidence");
 for(let h of paths(obs.length+1))num=plus(num,joint(h,obs+"1",stay,quality));
 return {den,forecast:over(num,den)};
}
function audit(csv,results){
 let lines=csv.trimEnd().split("\n"),header=lines.shift().split(",");
 const columns=["world","true_stay","true_emission","prefix","candidate_stay","candidate_emission","true_prefix_mass","true_next1","candidate_prefix_evidence","candidate_next1","conditional_brier","weighted_brier","weighted_excess"];
 if(JSON.stringify(header)!==JSON.stringify(columns))throw Error("header mismatch");
 if(lines.length!==288)throw Error("missing or excess source");
 if(results.scope!=="E1_EXACT_KNOWN_PARAMETER_MISSPECIFIED_HMM_FORECAST_RISK"||results.new_E2!==0||results.new_E3!==0||results.external_replication!=="NOT_RUN")throw Error("evidence promotion");
 if(results.source_rows!==288||results.distinct_true_prefixes!==32||results.group_count!==18||results.results.length!==18)throw Error("result cardinality");
 let keys=new Set(),sums=new Map(),prefixMass=new Map(),comparisons=0;
 const allStays=["1/4","1/2","3/4"],allQ=["1/2","3/4","1"],trueStays=["1/2","3/4"];
 for(let line of lines){
  let vals=line.split(",");if(vals.length!==columns.length)throw Error("column count");
  let r=Object.fromEntries(columns.map((k,i)=>[k,vals[i]]));
  let world=r.true_stay==="1/2"?"IID_HIDDEN_NEGATIVE_CONTROL":"PERSISTENT_HMM";
  if(r.world!==world||!trueStays.includes(r.true_stay)||r.true_emission!=="3/4"||!/^[01]{4}$/.test(r.prefix)||!allStays.includes(r.candidate_stay)||!allQ.includes(r.candidate_emission))throw Error("source identity");
  let key=[r.world,r.prefix,r.candidate_stay,r.candidate_emission].join("|");
  if(keys.has(key))throw Error("duplicate source");keys.add(key);
  let ta=frac(r.true_stay),tq=frac(r.true_emission),a=frac(r.candidate_stay),q=frac(r.candidate_emission);
  let tr=predict(r.prefix,ta,tq),cr=predict(r.prefix,a,q);
  let p=tr.forecast,f=cr.forecast;
  let conditional=plus(times(p,times(minus(O,f),minus(O,f))),times(minus(O,p),times(f,f)));
  let weighted=times(tr.den,conditional),ex=times(tr.den,times(minus(f,p),minus(f,p)));
  for(let [field,val] of Object.entries({true_prefix_mass:tr.den,true_next1:p,candidate_prefix_evidence:cr.den,candidate_next1:f,conditional_brier:conditional,weighted_brier:weighted,weighted_excess:ex})){
   if(!same(frac(r[field]),val))throw Error("source mismatch "+field+" "+key);
   comparisons++;
  }
  let group=[r.world,r.candidate_stay,r.candidate_emission].join("|");
  sums.set(group,plus(sums.get(group)||Z,weighted));
  if(r.candidate_stay==="1/4"&&r.candidate_emission==="1/2")prefixMass.set(r.world,plus(prefixMass.get(r.world)||Z,tr.den));
 }
 if(keys.size!==288||sums.size!==18)throw Error("coverage");
 for(let w of ["IID_HIDDEN_NEGATIVE_CONTROL","PERSISTENT_HMM"])if(!same(prefixMass.get(w),O))throw Error("mass normalization");
 let checked=0;
 for(let g of results.results){
  let world=g.true_stay==="1/2"?"IID_HIDDEN_NEGATIVE_CONTROL":"PERSISTENT_HMM",key=[world,g.candidate_stay,g.candidate_emission].join("|");
  if(g.world!==world||g.prefixes!==16||!sums.has(key))throw Error("group identity");
  let risk=sums.get(key);
  let ta=frac(g.true_stay),oracle=Z;
  for(let obs of paths(4)){let x=predict(obs,ta,frac("3/4"));oracle=plus(oracle,times(x.den,times(x.forecast,minus(O,x.forecast))));}
  if(!same(frac(g.expected_brier),risk)||!same(frac(g.oracle_brier),oracle)||!same(frac(g.excess_brier),minus(risk,oracle))||g.fixed_half_brier!=="1/4")throw Error("group risk");
  checked++;
 }
 return {status:"PASS",rows:lines.length,groups:checked,exact_source_fields:comparisons,method:"full hidden-path 4/5 state enumeration",blind:"NONBLIND",external_replication:"NOT_RUN"};
}
if(typeof module!=="undefined")module.exports={audit};
