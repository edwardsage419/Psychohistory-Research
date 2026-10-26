// R179 synthetic E1: independent BigInt rational moment route for archived receipt.
// Run: node r179_brier_receipt_js_generator_20261026.js
const fs = require('fs');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}const d=gcd(a,b);return [a/d,b/d]}
const add=(x,y)=>f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),neg=x=>[-x[0],x[1]],sub=(x,y)=>add(x,neg(y)),mul=(x,y)=>f(x[0]*y[0],x[1]*y[1]),div=(x,y)=>f(x[0]*y[1],x[1]*y[0]),sq=x=>mul(x,x),fmt=x=>x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1]),N=x=>f(x);
const sources=['IID_BIN','CLUSTERED_BB_C2','CLUSTERED_BB_C8','INACTIVE_ZIB_Z1_8','INACTIVE_ZIB_Z1_4'],priors=[['U',1,1],['S',2,2],['A',1,3]],records=[],counts={positive:0,zero:0,negative:0};
for(const n of [4,8,12])for(const p of [f(1,4),f(1,2)])for(const source of sources)for(const [prior,a,b] of priors){
 let variance=mul(mul(N(n),p),sub(N(1),p));
 if(source.startsWith('CLUSTERED')){const c=source.endsWith('C2')?2:8;variance=mul(variance,f(c+n,c+1))}
 if(source.startsWith('INACTIVE')){const z=source.endsWith('1_8')?f(1,8):f(1,4);variance=add(variance,mul(mul(div(z,sub(N(1),z)),N(n*(n-1))),sq(p)))}
 const risk=div(add(variance,sq(sub(N(a),mul(N(a+b),p)))),sq(N(a+b+n)));
 const priorRisk=sq(sub(f(a,a+b),p)),halfRisk=sq(sub(f(1,2),p)),dprior=sub(priorRisk,risk),dhalf=sub(halfRisk,risk);
 const sign=dprior[0]>0n?'positive':dprior[0]<0n?'negative':'zero';counts[sign]++;
 records.push({n,p:fmt(p),source,prior,a,b,source_variance:fmt(variance),posterior_mse:fmt(risk),prior_only_mse:fmt(priorRisk),neutral_half_mse:fmt(halfRisk),brier_skill_vs_prior:fmt(dprior),brier_skill_vs_half:fmt(dhalf),posterior_expected_brier:fmt(add(mul(p,sub(N(1),p)),risk)),sign_vs_prior:sign})
}
if(records.length!==90||counts.positive!==45||counts.negative!==45)throw Error('unexpected grid counts');
const selected=records.filter(x=>x.n===8&&x.p==='1/4');
if(selected.length!==15||selected[0].posterior_mse!=='7/400'||selected[3].posterior_mse!=='21/400')throw Error('reference mismatch');
const result={research_id:'R179',date:'2026-10-26',evidence:'E1_SYNTHETIC_ONLY',source_grid:'R179 frozen 90 posterior worlds',protocol:'protocols/R179_PRIOR_BASELINE_BRIER_SKILL_THIRD_METHOD_FREEZE_2026-10-26.md',computation:'Independent JS BigInt exact analytic moments; source Python Fraction PMF enumeration checked separately',prior_baseline_sign_counts:counts,by_prior:Object.fromEntries(priors.map(([a])=>[a,{positive:records.filter(x=>x.prior===a&&x.sign_vs_prior==='positive').length,negative:records.filter(x=>x.prior===a&&x.sign_vs_prior==='negative').length,zero:0}])),by_source:Object.fromEntries(sources.map(s=>[s,{positive:records.filter(x=>x.source===s&&x.sign_vs_prior==='positive').length,negative:records.filter(x=>x.source===s&&x.sign_vs_prior==='negative').length,zero:0}])),selected_n8_p_quarter:selected,full_90_worlds:records,comparison_to_R179_archived_full_90_mse:'PENDING_COMPLETE_ARCHIVED_JSON_PARITY',new_E2:0,new_E3:0};
const content=JSON.stringify(result,null,2)+'\n';
fs.writeFileSync(__dirname+'/R179_PRIOR_BRIER_SKILL_EXACT_RECEIPT_2026-10-26.json',content);
console.log('R179 exact worlds',records.length,'signs',counts);
