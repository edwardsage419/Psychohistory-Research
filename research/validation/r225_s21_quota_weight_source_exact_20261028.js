"use strict";
// R225 S21 offline exact source reweighting; run with node and no dependencies.
const WORLDS=["AS_IF_RANDOM_VALID","ENDOGENOUS_FUTURE_SHOCK_ALIAS","AS_IF_RANDOM_NULL","AS_IF_RANDOM_HETEROGENEOUS","ENDOGENOUS_VISIBLE_SELECTION","ANTICIPATORY_PRE_RESPONSE"];
const W={UNIFORM:[1,1,1,1,1,1],FAVOR_FIRST_PAIR:[6,1,1,1,1,1],FAVOR_LAST_PAIR:[1,1,1,1,1,6],FAVOR_UNIT_ZERO:[3,3,3,1,1,1]};
const METHODS=["post_group_difference","pre_balance_placebo","two_period_DiD"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
class Q{constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
 mul(b){return new Q(this.n*b.n,this.d*b.d);}div(b){return new Q(this.n*b.d,this.d*b.n);}
 eq(b){return this.n===b.n&&this.d===b.d;}toString(){return this.d===1n?String(this.n):this.n+"/"+this.d;}}
const q=(a,b=1)=>new Q(a,b),zero=q(0);
function csvline(s){let out=[],v="",quote=false;for(let i=0;i<s.length;i++){let c=s[i];if(c==='"'){if(quote&&s[i+1]==='"'){v+='"';i++;}else quote=!quote;}else if(c===","&&!quote){out.push(v);v="";}else v+=c;}if(quote)throw Error("bad CSV");out.push(v);return out;}
function vec(s){let m=[...s.matchAll(/Fraction\((-?\d+),\s*(\d+)\)/g)];if(m.length!==4)throw Error("fraction vector invalid");return m.map(x=>q(x[1],x[2]));}
function parse(csv){let lines=csv.trimEnd().split(/\r?\n/),head=csvline(lines.shift());if(head.length!==12||head[0]!=="world"||head[11]!=="original_probability")throw Error("CSV schema drift");
 let rows=lines.map(line=>{let a=csvline(line);if(a.length!==12||a[11]!=="1/96")throw Error("CSV row invalid");
 let z=(a[4].match(/\d+/g)||[]).map(Number);if(z.length!==4||z.reduce((s,v)=>s+v,0)!==2||a[4]!==a[5])throw Error("assignment drift");
 return {world:a[0],j:+a[1],k:+a[2],z,pre:vec(a[6]),post:vec(a[7]),y0:vec(a[8]),y1:vec(a[9]),signature:a[4]+"|"+a[6]+"|"+a[7]};});
 if(rows.length!==576)throw Error("source count drift");
 for(let world of WORLDS){let r=rows.filter(x=>x.world===world);if(r.length!==96||new Set(r.map(x=>x.j+":"+x.k)).size!==96)throw Error("source support drift");}
 return rows;}
function contrast(v,z){let a=zero,b=zero;for(let i=0;i<4;i++){if(z[i])a=a.add(v[i]);else b=b.add(v[i]);}return a.sub(b).div(q(2));}
function ate(r){let a=zero;for(let i=0;i<4;i++)a=a.add(r.y1[i].sub(r.y0[i]));return a.div(q(4));}
function stats(vals,prob,target){let m=zero,s=zero;for(let i=0;i<vals.length;i++){m=m.add(vals[i].mul(prob[i]));s=s.add(vals[i].mul(vals[i]).mul(prob[i]));}let v=s.sub(m.mul(m)),b=m.sub(target);return {expectation:m.toString(),variance:v.toString(),bias_from_true_target:b.toString(),mean_squared_error:v.add(b.mul(b)).toString()};}
function compute(csv,baseline){
 const rows=parse(csv),base=typeof baseline==="string"?JSON.parse(baseline):baseline;let results=[],alias=[],regression=0,probChecks=0;
 for(let [scenario,weights] of Object.entries(W)){let den=weights.reduce((a,b)=>a+b,0);
  for(let world of WORLDS){let rr=rows.filter(r=>r.world===world),probs=rr.map(r=>q(weights[r.j],16*den)),mass=probs.reduce((a,b)=>a.add(b),zero);
   if(!mass.eq(q(1)))throw Error("mass");probChecks++;let truth=ate(rr[0]);if(rr.some(r=>!ate(r).eq(truth)))throw Error("ATE drift");
   let byMethod={};for(let k=0;k<3;k++){let vals=rr.map(r=>{let p=contrast(r.post,r.z),pre=contrast(r.pre,r.z);return [p,pre,p.sub(pre)][k];});
    let result=stats(vals,probs,k===1?zero:truth);byMethod[METHODS[k]]=result;
    if(scenario==="UNIFORM"){let original=base.world_results.find(x=>x.world===world).observed_methods[METHODS[k]];for(let f of Object.keys(result)){if(result[f]!==original[f])throw Error("original regression "+world+"/"+f);regression++;}}
   }
   results.push({scenario,world,truth_ATE:truth.toString(),methods:byMethod});
  }
  let sigs=WORLDS.slice(0,2).map(world=>{let map=new Map();for(let r of rows.filter(x=>x.world===world)){let v=q(weights[r.j],16*den);map.set(r.signature,(map.get(r.signature)||zero).add(v));}return [...map].map(([k,v])=>[k,v.toString()]).sort((a,b)=>a[0].localeCompare(b[0]));});
  if(JSON.stringify(sigs[0])!==JSON.stringify(sigs[1]))throw Error("observed joint alias drift");
  alias.push({scenario,observed_joint_equal:true,support_cells:sigs[0].length,true_ATE_pair:["1","0"]});
 }
 return {study:"R225_S21",evidence:"E1_FINITE_ARTIFICIAL_ONLY",source_rows:576,weighted_evaluation_slots:2304,source_blob_sha1:"a1ece971788aabef644cf1bc24522d6b2070ada0",scenario_count:4,world_count:6,method_count:3,original_uniform_numeric_regression_checks:regression,probability_checks:probChecks,alias,results,new_E2:0,new_E3:0,external_independent_replications:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),crypto=require("crypto"),root=path.resolve(__dirname,"..");
 const raw=fs.readFileSync(path.join(root,"R225/R225_ALL_576_ORIGINAL_NATURAL_ASSIGNMENT_SOURCES.csv"));
 const sha=crypto.createHash("sha1").update("blob "+raw.length+"\0").update(raw).digest("hex");
 if(sha!=="a1ece971788aabef644cf1bc24522d6b2070ada0")throw Error("source blob SHA mismatch");
 let baseline=fs.readFileSync(path.join(root,"R225/R225_EXACT_RESULTS.json"),"utf8");
 process.stdout.write(JSON.stringify(compute(raw.toString("utf8"),baseline),null,2)+"\n");
}