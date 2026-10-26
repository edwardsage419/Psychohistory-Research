// Exact R186 observation-channel calculation. Run from repository root with Node.js 18+.
const fs=require('fs');
const compute=function compute(data){
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t}return a};
const f=x=>{let [a,b="1"]=String(x).split("/");a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return [a/g,b/g]};
const add=(a,b)=>{let n=a[0]*b[1]+b[0]*a[1],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]};
const mul=(a,b)=>{let n=a[0]*b[0],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]};
const neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b)),abs=a=>[a[0]<0n?-a[0]:a[0],a[1]],str=a=>a[1]===1n?String(a[0]):a.join("/");
function tv(P,Q,m){let sum=f(0),massA=f(0),massB=f(0),N=0;function visit(i,a,b){if(i===m){sum=add(sum,abs(sub(a,b)));massA=add(massA,a);massB=add(massB,b);N++;return}for(let k=0;k<P.length;k++)visit(i+1,mul(a,P[k]),mul(b,Q[k]))}visit(0,f(1),f(1));return{v:mul(sum,f("1/2")),massA,massB,N}}
let rows=[];
for(let n of [2,4])for(let p of ["1/4","1/2"]){let w=data.all_worlds.filter(x=>x.n===n&&x.m===2&&x.true_marginal_p===p);let a=w.find(x=>x.source==="CLUSTERED_BB_C2"),b=w.find(x=>x.source==="INACTIVE_ZIB_Z1_4");if(!a||!b)throw Error("source missing");let P=a.source_full_count_PMF.map(f),Q=b.source_full_count_PMF.map(f);for(let m of [1,2,3])for(let channel of ["COUNT","ZERO_ONLY"]){let x=channel==="COUNT"?P:[P[0],sub(f(1),P[0])],y=channel==="COUNT"?Q:[Q[0],sub(f(1),Q[0])];let t=tv(x,y,m);if(str(t.massA)!=="1"||str(t.massB)!=="1")throw Error("mass");let mutant=channel==="COUNT"?tv(x.slice(0,-1),y.slice(0,-1),m).v:null;rows.push({n,p,m,channel,source_BB_PMF:a.source_full_count_PMF,source_ZIB_PMF:b.source_full_count_PMF,ordered_support:t.N,TV:str(t.v),Bayes_error:str(mul(sub(f(1),t.v),f("1/2"))),mutant_detected:mutant?str(mutant)!==str(t.v):null})}}
return rows;
};
const data=JSON.parse(fs.readFileSync('research/R186/R186_EXACT_RESULTS.json','utf8'));
const rows=compute(data);
if(rows.length!==24)throw Error('row count');
process.stdout.write(JSON.stringify(rows,null,2)+'\n');
