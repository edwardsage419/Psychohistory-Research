// B_R201: independent analytic scoring from original 120-row R201 CSV.
// Run: node research/evidence_audit/b_r201_cohort_shift_independent_20261027.js <original120.csv> <new360.json>
"use strict";
const testX={"LOW3_HIGH1":[0,0,0,1],"BALANCED":[0,0,1,1],"LOW1_HIGH3":[0,1,1,1]},oldX=[0,0,1,1];
function gcd(a,b){while(b){let c=a%b;a=b;b=c;}return a;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero");if(b<0n){a=-a;b=-b;}let g=gcd(a<0n?-a:a,b);return [a/g,b/g];}
function P(s){let x=s.split("/");return F(x[0],x[1]||1);}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return add(a,F(-b[0],b[1]));}
function div(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function fmt(a){return a[0]+"/"+a[1];}
const Z=F(0),O=F(1);
function pred(h,x){let r=P(h),w=x.map(t=>t?r:O),d=w.reduce(add,Z);return w.map(v=>div(v,d));}
function risk(p,q){let dot=Z,square=Z;for(let i=0;i<4;i++){dot=add(dot,mul(p[i],q[i]));square=add(square,mul(q[i],q[i]));}return add(sub(O,mul(F(2),dot)),square);}
function csvRows(s){let lines=s.trim().split(/\r?\n/),header=lines.shift().split(",");return lines.map(line=>{let vals=line.split(",");if(vals.length!==header.length)throw Error("CSV shape");return Object.fromEntries(header.map((h,i)=>[h,vals[i]]));});}
function audit(csv,receipt){let source=csvRows(csv);if(source.length!==120||receipt.rows.length!==360||receipt.worlds.length!==27)throw Error("row counts");let rowChecks=0,worldChecks=0,normalized=0;const grouped=new Map();
for(let item of source){let truth=item.true_hr,k=Number(item.observed_failures),prefix=item.prefix_subject_ids,h=item.fitted_hr,mass=P(item.true_source_prefix_probability);
if(!["1/4","1","4"].includes(truth)||![1,2,3].includes(k)||!["1","1/4","4"].includes(h))throw Error("unexpected original CSV");for(let [test,x] of Object.entries(testX)){let p=pred(truth,x),q=pred(h,x),wrong=pred(h,oldX),key=[truth,k,test].join(":");let a=grouped.get(key)||{mass:Z,correct:Z,wrong:Z,selectedTrue:Z,count:0};a.mass=add(a.mass,mass);a.correct=add(a.correct,mul(mass,risk(p,q)));a.wrong=add(a.wrong,mul(mass,risk(p,wrong)));if(h===truth)a.selectedTrue=add(a.selectedTrue,mass);a.count++;grouped.set(key,a);
let row=receipt.rows.find(z=>z.true_hr===truth&&z.k===k&&z.test===test&&z.prefix===prefix);if(!row)throw Error("missing receipt row");
for(let [key,actual] of Object.entries({source_mass:fmt(mass),fitted_hr:h,correct_brier:fmt(risk(p,q)),wrong_feature_brier:fmt(risk(p,wrong))})){rowChecks++;if(row[key]!==actual)throw Error("row mismatch "+key+" "+key);}
}}
for(let w of receipt.worlds){let a=grouped.get([w.true_hr,w.k,w.test].join(":"));if(!a||a.count!==w.training_prefix_count||fmt(a.mass)!=="1/1")throw Error("source mass");normalized++;
let p=pred(w.true_hr,testX[w.test]),oracle=risk(p,p),nullRisk=risk(p,pred("1",testX[w.test]));
let expected={selected_expected_brier:fmt(a.correct),wrong_feature_brier:fmt(a.wrong),oracle_brier:fmt(oracle),fixed_null_brier:fmt(nullRisk),oracle_gap:fmt(sub(a.correct,oracle)),selected_minus_null:fmt(sub(a.correct,nullRisk)),wrong_feature_minus_correct:fmt(sub(a.wrong,a.correct)),selected_true_probability:fmt(a.selectedTrue)};
for(let [key,val] of Object.entries(expected)){worldChecks++;if(w[key]!==val)throw Error("world mismatch "+key);}
}
return {status:"PASS_INTERNAL_ALTERNATE_ANALYTIC_RECOMPUTATION",original_csv_rows:source.length,scored_rows:receipt.rows.length,worlds:receipt.worlds.length,row_field_checks:rowChecks,world_field_checks:worldChecks,normalized_worlds:normalized,external_independent_replication:0};}
if(typeof require!=="undefined"&&require.main===module){let fs=require("node:fs");let a=audit(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));console.log(JSON.stringify(a,null,2));}
if(typeof module!=="undefined")module.exports={audit};
