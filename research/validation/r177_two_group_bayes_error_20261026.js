"use strict";
// R177 third-method exact two-independent-group classifier, Node.js 18+.
// Run: node r177_two_group_bayes_error_20261026.js R177_EXACT_RESULTS.json output.json
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(b===0n)throw Error("zero denominator");let g=gcd(a,b);return [a/g,b/g];}
function parse(s){let t=String(s).split("/");return F(t[0],t[1]||1);}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function abs(a){return a[0]<0n?[-a[0],a[1]]:a;}
function str(a){return a[1]===1n?String(a[0]):a[0]+"/"+a[1];}
function cmp(a,b){let v=a[0]*b[1]-b[0]*a[1];return v<0n?-1:v>0n?1:0;}
function tv(a,b,m){let s=F(0);if(m===1){for(let i=0;i<a.length;i++)s=add(s,abs(sub(a[i],b[i])));}
else if(m===2){for(let i=0;i<a.length;i++)for(let j=0;j<a.length;j++)s=add(s,abs(sub(mul(a[i],a[j]),mul(b[i],b[j]))));}
else throw Error("unsupported m");return mul(s,F(1,2));}
function compute(src){
if(src.research_id!=="R177"||src.world_data.length!==108||src.full_PMF_probability_cells!==972)throw Error("source identity mismatch");
const groups=new Map();
for(const w of src.world_data){if(w.family==="BIN"&&w.regime!==0)continue;
const key=w.n+"|"+w.p;if(!groups.has(key))groups.set(key,[]);
groups.get(key).push({id:w.family+"_r"+w.regime,pmf:w.full_PMF.map(parse),n:w.n,p:w.p});}
if(groups.size!==9)throw Error("nine strata required");
const records=[],summaries=[];let inc=0,equal=0,aliases1=0,aliases2=0;
let min1=null,max1=null,min2=null,max2=null;
for(const [key,arr] of [...groups.entries()].sort()){if(arr.length!==10)throw Error("10 mechanisms per stratum");
let localInc=0,localEqual=0,localAliases=0;
for(let i=0;i<arr.length;i++)for(let j=i+1;j<arr.length;j++){
const a=arr[i],b=arr[j],v1=tv(a.pmf,b.pmf,1),v2=tv(a.pmf,b.pmf,2);
if(cmp(v2,v1)<0)throw Error("data processing monotonicity failed");
let e1=mul(sub(F(1),v1),F(1,2)),e2=mul(sub(F(1),v2),F(1,2));
if(cmp(e1,F(0))<0||cmp(e1,F(1,2))>0||cmp(e2,F(0))<0||cmp(e2,F(1,2))>0)throw Error("invalid Bayes error");
let sign=cmp(v2,v1);if(sign>0){inc++;localInc++;}else{equal++;localEqual++;}
if(cmp(v1,F(0))===0)aliases1++;if(cmp(v2,F(0))===0){aliases2++;localAliases++;}
if(min1===null||cmp(v1,min1)<0)min1=v1;if(max1===null||cmp(v1,max1)>0)max1=v1;
if(min2===null||cmp(v2,min2)<0)min2=v2;if(max2===null||cmp(v2,max2)>0)max2=v2;
records.push({n:a.n,p:a.p,a:a.id,b:b.id,tv_m1:str(v1),tv_m2:str(v2),bayes_error_m1:str(e1),bayes_error_m2:str(e2)});
}
summaries.push({stratum:key,pairs:45,strict_increase:localInc,equal:localEqual,aliases_m2:localAliases});}
if(records.length!==405||inc+equal!==405)throw Error("pair count mismatch");
const unif=[F(1,3),F(1,3),F(1,3)];
if(cmp(tv(unif,unif,1),F(0))!==0||cmp(tv(unif,unif,2),F(0))!==0)throw Error("n2 alias negative control");
const selected=groups.get("8|1/4"),a=selected.find(x=>x.id==="BIN_r0"),b=selected.find(x=>x.id==="ZIB_r0");
const normal=tv(a.pmf,b.pmf,1),mutant=tv(a.pmf,[...b.pmf].reverse(),1);
if(cmp(normal,mutant)===0)throw Error("mutant sensitivity failure");
return {research_id:"R177",date:"2026-10-26",evidence:"E1_SYNTHETIC_POSTACCEPTANCE_ADDENDUM",
source_blob_sha:"8a8819e4d85989b518b9152cfc98336457c76a9c",
protocol:"protocols/R177_TWO_INDEPENDENT_GROUP_BAYES_ERROR_THIRD_METHOD_FREEZE_2026-10-26.md",
method:"exact TV of tensor-product PMFs, equal-prior Bayes classification",strata:9,unique_mechanisms:90,
pairs:405,strict_tv_gain_m2:inc,equal_tv_m2:equal,aliases_m1:aliases1,aliases_m2:aliases2,
tv_m1_min:str(min1),tv_m1_max:str(max1),tv_m2_min:str(min2),tv_m2_max:str(max2),
n2_BB_ZIB_alias_tv_m1:"0",n2_BB_ZIB_alias_tv_m2:"0",
mutant_selected_tv_m1:str(normal),mutant_reversed_zib_tv_m1:str(mutant),
stratum_summaries:summaries,pairwise_exact:records,new_E2:0,new_E3:0,external_replication:false};
}
if(typeof module!=="undefined"&&module.exports){
module.exports={compute};
if(require.main===module){const fs=require("fs");let x=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));fs.writeFileSync(process.argv[3],JSON.stringify(compute(x),null,2)+"\n");}}
