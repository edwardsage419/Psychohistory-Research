// R186 independent histogram multinomial overlap and negative control. Node.js 18+.
const fs=require('fs');
const audit=function audit(source,rows){
function gcd(a,b){a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t}return a}
function F(x){let [a,b="1"]=String(x).split("/");a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return[a/g,b/g]}
function add(a,b){let n=a[0]*b[1]+b[0]*a[1],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]}
function mul(a,b){let n=a[0]*b[0],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]}
function neg(a){return[-a[0],a[1]]}
function sub(a,b){return add(a,neg(b))}
function cmp(a,b){let z=a[0]*b[1]-b[0]*a[1];return z<0n?-1:z>0n?1:0}
function str(a){return a[1]===1n?String(a[0]):a.join("/")}
function binom(n,k){let z=1n;for(let j=1;j<=k;j++)z=z*BigInt(n-j+1)/BigInt(j);return z}
function hist(P,Q,m){let massP=F(0),massQ=F(0),overlap=F(0),absSum=F(0),h=0;function rec(i,left,c){if(i===P.length){if(left)return;let coef=1n,rem=m;for(let v of c){coef*=binom(rem,v);rem-=v}let a=F(String(coef)),b=F(String(coef));for(let j=0;j<c.length;j++)for(let k=0;k<c[j];k++){a=mul(a,P[j]);b=mul(b,Q[j])}massP=add(massP,a);massQ=add(massQ,b);overlap=add(overlap,cmp(a,b)<=0?a:b);let delta=sub(a,b);absSum=add(absSum,delta[0]<0n?neg(delta):delta);h++;return}for(let v=0;v<=left;v++)rec(i+1,left-v,[...c,v])}rec(0,m,[]);return{massP:str(massP),massQ:str(massQ),overlapTV:str(sub(F(1),overlap)),directTV:str(mul(absSum,F("1/2"))),h}}
let parity=0,mass=0,histTotal=0,mutant=0,alias=0,dominance=0,monotonic=0;
for(let row of rows){let P=row.source_BB_PMF.map(F),Q=row.source_ZIB_PMF.map(F);if(row.channel==="ZERO_ONLY"){P=[P[0],sub(F(1),P[0])];Q=[Q[0],sub(F(1),Q[0])]}let z=hist(P,Q,row.m);if(z.massP!=="1"||z.massQ!=="1")throw Error("mass fail");mass+=2;if(z.overlapTV!==row.TV||z.directTV!==row.TV)throw Error("TV fail");parity++;histTotal+=z.h;if(row.n===2&&row.p==="1/2"){if(row.TV!=="0")throw Error("alias fail");alias++}if(row.channel==="COUNT"){let broken=hist(P.slice(0,-1),Q.slice(0,-1),row.m).directTV;let caught=broken!==row.TV;if(caught!==row.mutant_detected)throw Error("mutant flag mismatch");if(caught)mutant++}}
for(let n of [2,4])for(let p of ["1/4","1/2"]){let subset=rows.filter(x=>x.n===n&&x.p===p);for(let m of [1,2,3]){let c=subset.find(x=>x.m===m&&x.channel==="COUNT"),z=subset.find(x=>x.m===m&&x.channel==="ZERO_ONLY");if(cmp(F(c.TV),F(z.TV))<0)throw Error("data processing");dominance++}for(let channel of ["COUNT","ZERO_ONLY"]){let xs=subset.filter(x=>x.channel===channel);for(let i=1;i<xs.length;i++){if(cmp(F(xs[i].TV),F(xs[i-1].TV))<0)throw Error("monotonic");monotonic++}}}
return{exact_TV_parity:parity,source_joint_mass_checks:mass,histogram_profile_count:histTotal,alias_rows:alias,coarsening_checks:dominance,independent_group_monotonic_checks:monotonic,mutant_detected:mutant,mutant_undetected_due_to_alias:12-mutant,external_replication:false};
};
const source=JSON.parse(fs.readFileSync('research/R186/R186_EXACT_RESULTS.json','utf8'));
const rows=JSON.parse(fs.readFileSync('research/validation/R186_BB_ZIB_COUNT_VS_ZERO_ONLY_EXACT_RECEIPT_2026-10-26.json','utf8')).rows;
const result=audit(source,rows);
if(result.exact_TV_parity!==24||result.mutant_detected!==9)throw Error('B audit failed');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
