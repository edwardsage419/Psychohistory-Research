"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function f(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}if(d===0n)throw Error("den0");const g=gcd(n,d);return {n:n/g,d:d/g};}
function add(a,b){return f(a.n*b.d+b.n*a.d,a.d*b.d);}
function mul(a,b){return f(a.n*b.n,a.d*b.d);}
function div(a,b){return f(a.n*b.d,a.d*b.n);}
function sub(a,b){return add(a,f(-b.n,b.d));}
function pow(a,n){return f(a.n**BigInt(n),a.d**BigInt(n));}
function cmp(a,b){const x=a.n*b.d-b.n*a.d;return x>0n?1:x<0n?-1:0;}
function st(a){return a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);}
const one=f(1),zero=f(0);
function coeff(q,y){const s=st(q);
const d={"1/16":[[4,-1,-1],[4,0,0]],"15/16":[[4,0,0],[4,-1,-1]],"1/4":[[2,-1,0],[2,0,0]],"3/4":[[2,0,0],[2,-1,0]],"1/2":[[1,0,0],[1,0,0]]};
if(!d[s])throw Error("unexpected q "+s);return d[s][y].map(x=>f(x));}
function build(){
 const rows=[],worlds=[],ps=[f(1,4),f(1,2),f(3,4)],epss=[f(1,16),f(1,4)];
 const cols=["p","boundary","epsilon","q","bits","k","mass","ln2","ln3","ln5","strict_win","tie"];
 for(const p of ps)for(const boundary of [0,1])for(const eps of epss){
  const q=boundary===0?eps:sub(one,eps);
  const c0=coeff(q,0),c1=coeff(q,1);
  let massSum=zero,win=zero,tie=zero,risk=[zero,zero,zero];
  for(let i=0;i<16;i++){
   const bits=i.toString(2).padStart(4,"0"),k=bits.split("").filter(x=>x==="1").length;
   const mass=mul(pow(p,k),pow(sub(one,p),4-k));
   const sample=c0.map((x,j)=>div(add(mul(f(4-k),x),mul(f(k),c1[j])),f(4)));
   const logq=mul(pow(q,k),pow(sub(one,q),4-k));
   const logp=mul(pow(p,k),pow(sub(one,p),4-k));
   const comparison=cmp(logq,logp),w=comparison>0?1:0,t=comparison===0?1:0;
   rows.push([st(p),String(boundary),st(eps),st(q),bits,String(k),st(mass),...sample.map(st),String(w),String(t)].join(","));
   massSum=add(massSum,mass);if(w)win=add(win,mass);if(t)tie=add(tie,mass);
   for(let j=0;j<3;j++)risk[j]=add(risk[j],mul(mass,sample[j]));
  }
  if(cmp(massSum,one)!==0)throw Error("bad mass");
  const analytic=c0.map((x,j)=>add(mul(sub(one,p),x),mul(p,c1[j])));
  if(risk.some((x,j)=>cmp(x,analytic[j])!==0))throw Error("risk mismatch");
  const inf=boundary===0?sub(one,pow(sub(one,p),4)):sub(one,pow(p,4));
  worlds.push({p:st(p),boundary:String(boundary),epsilon:st(eps),q:st(q),
   risk_coefficients:risk.map(st),strict_win_probability:st(win),tie_probability:st(tie),
   original_unclipped_infinite_probability:st(inf),original_unclipped_expected_risk:"INF"});
 }
 if(rows.length!==192||worlds.length!==12)throw Error("count");
 const w=(p,b,e)=>worlds.find(x=>x.p===p&&x.boundary===b&&x.epsilon===e);
 if(w("1/4","0","1/16").strict_win_probability!=="81/256")throw Error("control");
 if(w("1/4","1","1/4").tie_probability!=="27/128")throw Error("tie counterexample");
 if(JSON.stringify(w("1/4","0","1/16").risk_coefficients)!==JSON.stringify(w("3/4","1","1/16").risk_coefficients))throw Error("symmetry");
 const payload={schema:"r281_s77_epsilon_logscore_v1",evidence:"E1_INTERNAL_NONBLIND_EXPLORATORY",
  freeze_commit:"aab1a46ebf6ec9b14d904c1625411e90e15c0b28",world_count:12,source_count:192,
  frozen_no_tie_when_q_differs_status:"FAIL",frozen_no_tie_counterexample:{p:"1/4",boundary:"1",epsilon:"1/4",q:"3/4",tie_probability:"27/128"},
  worlds};
 return {csv:cols.join(",")+"\n"+rows.join("\n")+"\n",json:JSON.stringify(payload,null,2)+"\n",payload};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");const r=build();
 if(process.argv.includes("--selftest"))console.log("R_SELFTEST_PASS worlds=12 atoms=192, FROZEN_TIE_TEST_FAIL recorded");
 if(process.argv.includes("--emit")){const at=process.argv.indexOf("--emit"),out=process.argv[at+1];if(!out)throw Error("--emit requires directory");fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,"R281_S77_ALL_192_EPSILON_LOG_SCORE_SOURCE_ATOMS.csv"),r.csv);fs.writeFileSync(path.join(out,"R281_S77_EXACT_RESULTS.json"),r.json);}
}
