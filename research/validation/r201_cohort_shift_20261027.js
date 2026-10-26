// R201 third method: exact independent new-cohort composition shift.
// Run: node research/validation/r201_cohort_shift_20261027.js
"use strict";
const trainX=[0,0,1,1], tests={"LOW3_HIGH1":[0,0,0,1],"BALANCED":[0,0,1,1],"LOW1_HIGH3":[0,1,1,1]};
const sources=["1/4","1","4"], candidates=["1","1/4","4"];
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(b===0n)throw Error("zero denominator");let g=gcd(a<0n?-a:a,b);return [a/g,b/g];}
function P(s){let x=s.split("/");return F(BigInt(x[0]),BigInt(x[1]||1));}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function sub(a,b){return add(a,F(-b[0],b[1]));}
function gt(a,b){return a[0]*b[1]>b[0]*a[1];}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
function fmt(a){return String(a[0])+"/"+String(a[1]);}
const ONE=F(1),ZERO=F(0);
function distribution(hr,x){const w=x.map(v=>v?P(hr):ONE),den=w.reduce(add,ZERO);return w.map(v=>div(v,den));}
function prefixProbability(prefix,hr){let rem=[0,1,2,3],ans=ONE;for(let id of prefix){let p=distribution(hr,rem.map(i=>trainX[i]));let idx=rem.indexOf(id);if(idx<0)throw Error("duplicate id");ans=mul(ans,p[idx]);rem.splice(idx,1);}return ans;}
function prefixes(k){let out=[];function go(a){if(a.length===k){out.push(a);return;}for(let i=0;i<4;i++)if(!a.includes(i))go([...a,i]);}go([]);return out;}
function fit(prefix){let best=candidates[0],value=prefixProbability(prefix,best);for(let h of candidates.slice(1)){let v=prefixProbability(prefix,h);if(gt(v,value)){best=h;value=v;}}return best;}
function brier(p,q){let s=ZERO;for(let i=0;i<4;i++){let term=add(mul(p[i],mul(sub(ONE,q[i]),sub(ONE,q[i]))),mul(sub(ONE,p[i]),mul(q[i],q[i])));s=add(s,term);}return s;}
function run(){let worlds=[],rows=[],checks=0;for(let truth of sources)for(let k of [1,2,3]){let all=prefixes(k),sum=all.map(pr=>prefixProbability(pr,truth)).reduce(add,ZERO);if(!eq(sum,ONE))throw Error("source normalization");checks++;for(let [name,x] of Object.entries(tests)){let p=distribution(truth,x),oracle=brier(p,p),nullRisk=brier(p,distribution("1",x)),total=ZERO,carry=ZERO,selectedTrue=ZERO;for(let pr of all){let mass=prefixProbability(pr,truth),h=fit(pr),q=distribution(h,x),wrong=distribution(h,trainX),risk=brier(p,q),bad=brier(p,wrong);total=add(total,mul(mass,risk));carry=add(carry,mul(mass,bad));if(h===truth)selectedTrue=add(selectedTrue,mass);rows.push({true_hr:truth,k,test:name,prefix:pr.join("|"),source_mass:fmt(mass),fitted_hr:h,correct_brier:fmt(risk),wrong_feature_brier:fmt(bad)});}
worlds.push({true_hr:truth,k,test:name,training_prefix_count:all.length,source_mass_total:fmt(sum),selected_true_probability:fmt(selectedTrue),selected_expected_brier:fmt(total),fixed_null_brier:fmt(nullRisk),oracle_brier:fmt(oracle),oracle_gap:fmt(sub(total,oracle)),selected_minus_null:fmt(sub(total,nullRisk)),wrong_feature_brier:fmt(carry),wrong_feature_minus_correct:fmt(sub(carry,total))});}}
if(rows.length!==360||worlds.length!==27||checks!==9)throw Error("counts");
const old={"1/4":["183/250","177/250","873/1250"],"1":["21/25","39/50","81/100"],"4":["183/250","177/250","873/1250"]};
for(let w of worlds.filter(w=>w.test==="BALANCED")){if(w.selected_expected_brier!==old[w.true_hr][w.k-1])throw Error("R201 original result mismatch");}
return {research_id:"R201",status:"INTERNAL_BOUNDED_E1_POSTSCORE_ADDENDUM",date:"2026-10-27",prescore_protocol:"protocols/R201_COHORT_COMPOSITION_SHIFT_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",world_count:worlds.length,scored_prefix_cases:rows.length,training_source_normalizations:checks,worlds,rows};}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
if(typeof module!=="undefined")module.exports={run};
