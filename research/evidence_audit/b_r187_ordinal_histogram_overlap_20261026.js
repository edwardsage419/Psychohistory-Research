// Independent R187 histogram multinomial-overlap audit. Node.js 18+.
const fs=require('fs');
const audit=function audit(rows){
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t}return a};
const F=x=>{let [a,b="1"]=String(x).split("/");a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return[a/g,b/g]};
const S=(a,b)=>{let n=a[0]*b[1]+b[0]*a[1],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]};
const M=(a,b)=>{let n=a[0]*b[0],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g]};
const C=(a,b)=>a[0]*b[1]-b[0]*a[1];
const T=a=>a[1]===1n?String(a[0]):a.join("/");
function comb(n,k){let r=1n;for(let i=1;i<=k;i++)r=r*BigInt(n-i+1)/BigInt(i);return r}
function hist(P,Q,m){let ov=F(0),pm=F(0),qm=F(0),n=0;function walk(i,left,c){if(i===P.length){if(left)return;let a=F(1),b=F(1),rem=m;for(let j=0;j<c.length;j++){let coef=F(String(comb(rem,c[j])));a=M(a,coef);b=M(b,coef);rem-=c[j];for(let z=0;z<c[j];z++){a=M(a,P[j]);b=M(b,Q[j])}}pm=S(pm,a);qm=S(qm,b);ov=S(ov,C(a,b)<=0n?a:b);n++;return}for(let k=0;k<=left;k++)walk(i+1,left-k,[...c,k])}walk(0,m,[]);return{tv:T(S(F(1),M(F(-1),ov))),pm:T(pm),qm:T(qm),n}}
let parity=0,mass=0,histTotal=0,nullRows=0,coarsening=0,monotonic=0,mutants=0;
for(let row of rows){let a=row.group0_PMF.map(F),b=row.group1_PMF.map(F);if(row.channel==="LOW_CDF"){a=[a[0],S(a[1],a[2])];b=[b[0],S(b[1],b[2])]}if(row.channel==="UPPER_CDF"){a=[S(a[0],a[1]),a[2]];b=[S(b[0],b[1]),b[2]]}let h=hist(a,b,row.m);if(h.tv!==row.TV||h.pm!=="1"||h.qm!=="1")throw Error("audit mismatch");parity++;mass+=2;histTotal+=h.n;if(row.source_world==="NULL"){if(row.TV!=="0")throw Error("NULL alias");nullRows++}}
let sources=[...new Set(rows.map(r=>r.source_world))];
for(let w of sources){let group=rows.filter(r=>r.source_world===w);for(let m of [1,2,3]){let full=group.find(r=>r.m===m&&r.channel==="FULL");for(let channel of ["LOW_CDF","UPPER_CDF"]){let sub=group.find(r=>r.m===m&&r.channel===channel);if(C(F(full.TV),F(sub.TV))<0n)throw Error("coarsening");coarsening++}let low=group.find(r=>r.m===m&&r.channel==="LOW_CDF"),up=group.find(r=>r.m===m&&r.channel==="UPPER_CDF");if(low.TV!==up.TV)mutants++}for(let channel of ["FULL","LOW_CDF","UPPER_CDF"]){let rs=group.filter(r=>r.channel===channel);for(let i=1;i<rs.length;i++){if(C(F(rs[i].TV),F(rs[i-1].TV))<0n)throw Error("monotonic");monotonic++}}}
return{exact_histogram_parity:parity,source_mass_checks:mass,histogram_profiles:histTotal,null_alias_rows:nullRows,coarsening_checks:coarsening,monotonic_checks:monotonic,threshold_swap_mutant_detected:mutants,threshold_swap_total:18,external_replication:false};
};
const rows=JSON.parse(fs.readFileSync('research/validation/R187_ORDINAL_THRESHOLD_COARSENING_54_EXACT_RECEIPT_2026-10-26.json','utf8')).rows;
const result=audit(rows);
if(result.exact_histogram_parity!==54||result.threshold_swap_mutant_detected===0)throw Error('audit failed');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
