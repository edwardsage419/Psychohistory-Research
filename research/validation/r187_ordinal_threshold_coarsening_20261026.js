// R187 exact ordinal coarsening. Node.js 18+, run from repository root.
const fs=require('fs');
const calc=function calc(data){
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t}return a};
const f=x=>{let [a,b="1"]=String(x).split("/");a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return[a/g,b/g]};
const plus=(a,b)=>{let n=a[0]*b[1]+b[0]*a[1],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]};
const mul=(a,b)=>{let n=a[0]*b[0],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]};
const minus=(a,b)=>plus(a,[-b[0],b[1]]),str=a=>a[1]===1n?String(a[0]):a.join("/");
function tv(P,Q,m){let total=f(0),pMass=f(0),qMass=f(0),count=0;function visit(i,a,b){if(i===m){let delta=minus(a,b);total=plus(total,[delta[0]<0n?-delta[0]:delta[0],delta[1]]);pMass=plus(pMass,a);qMass=plus(qMass,b);count++;return}for(let k=0;k<P.length;k++)visit(i+1,mul(a,P[k]),mul(b,Q[k]))}visit(0,f(1),f(1));if(str(pMass)!=="1"||str(qMass)!=="1")throw Error("mass");return{tv:str(mul(total,f("1/2"))),support:count}}
let rows=[];let selected=data.source_world_results.filter(x=>x.group_sample_size_m===3);
if(selected.length!==6)throw Error("six source worlds expected");
for(let w of selected){let a=w.truth_categorical_PMF_group0.map(f),b=w.truth_categorical_PMF_group1.map(f);for(let m of [1,2,3])for(let channel of ["FULL","LOW_CDF","UPPER_CDF"]){let P=channel==="FULL"?a:channel==="LOW_CDF"?[a[0],plus(a[1],a[2])]:[plus(a[0],a[1]),a[2]],Q=channel==="FULL"?b:channel==="LOW_CDF"?[b[0],plus(b[1],b[2])]:[plus(b[0],b[1]),b[2]];let t=tv(P,Q,m);let z=f(t.tv);rows.push({source_world:w.source_world,m,channel,group0_PMF:w.truth_categorical_PMF_group0,group1_PMF:w.truth_categorical_PMF_group1,TV:t.tv,Bayes_error:str(mul(minus(f(1),z),f("1/2"))),ordered_support:t.support})}}return rows;
};
const data=JSON.parse(fs.readFileSync('research/R187/R187_EXACT_RESULTS.json','utf8'));
const rows=calc(data);
if(rows.length!==54)throw Error('expected 54 rows');
process.stdout.write(JSON.stringify(rows,null,2)+'\n');
