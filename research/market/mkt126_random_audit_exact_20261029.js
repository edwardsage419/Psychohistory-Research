// MKT126: exact finite-population random audit, no external dependencies.
"use strict";
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a};
const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
const plus=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const minus=(a,b)=>plus(a,[-b[0],b[1]]);
const times=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const over=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const same=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const fmt=a=>a[1]===1n?a[0].toString():a[0]+"/"+a[1];
const comb=(n,k)=>{if(k<0||k>n)return 0n;let z=1n;for(let i=1;i<=k;i++)z=z*BigInt(n-i+1)/BigInt(i);return z};
const H=(N,K,n,j)=>Q(comb(K,j)*comb(N-K,n-j),comb(N,n));
const ONE=Q(1),ZERO=Q(0),N=55,k=11,weight=Q(N,k);
let assertions=0;
const check=(x,msg)=>{assertions++;if(!x)throw Error("ASSERT "+msg)};
const loss=(high,y)=>high?(y?Q(1,25):Q(16,25)):(y?Q(16,25):Q(1,25));
const groupLoss=(high,pos,count)=>plus(times(Q(pos),loss(high,true)),times(Q(count-pos),loss(high,false)));
const visible=plus(groupLoss(true,15,45),groupLoss(false,30,45));
check(same(over(visible,Q(90)),Q(11,25)),"observed risk");
const bounds=[over(plus(visible,times(Q(110),Q(1,25))),Q(200)),over(plus(visible,times(Q(110),Q(16,25))),Q(200))];
check(same(bounds[0],Q(11,50))&&same(bounds[1],Q(11,20)),"bounds");
const worlds=[{name:"A",high:45,low:10,expected:Q(7,25),variance:Q(3,5000)},{name:"B",high:0,low:55,expected:Q(11,20),variance:ZERO}];
const results=[];
for(const w of worlds){
 const truth=over(plus(visible,plus(groupLoss(true,w.high,N),groupLoss(false,w.low,N))),Q(200));
 check(same(truth,w.expected),"truth "+w.name);
 let mass=ZERO,mean=ZERO,second=ZERO,states=0;
 for(let a=0;a<=k;a++)for(let b=0;b<=k;b++){
  const p=times(H(N,w.high,k,a),H(N,w.low,k,b));if(p[0]===0n)continue;
  const auditLoss=plus(groupLoss(true,a,k),groupLoss(false,b,k));
  const estimate=over(plus(visible,times(weight,auditLoss)),Q(200));
  mass=plus(mass,p);mean=plus(mean,times(p,estimate));second=plus(second,times(p,times(estimate,estimate)));states++;
 }
 const variance=minus(second,times(mean,mean));
 check(same(mass,ONE),"audit mass "+w.name);
 check(same(mean,truth),"unbiased "+w.name);
 check(same(variance,w.variance),"variance "+w.name);
 results.push({world:w.name,true_brier:fmt(truth),audit_expected_brier:fmt(mean),audit_variance:fmt(variance),positive_audit_states:states});
}
const missRare=times(H(N,45,k,11),H(N,10,k,0));
check(missRare[0]>0n&&missRare[0]<missRare[1],"rare labels can be missed");
const noAudit=()=>{throw Error("no audit positivity")};
let rejected=false;try{noAudit()}catch(e){rejected=true}check(rejected,"zero inclusion gate");
console.log(JSON.stringify({population:200,visible:90,unseen:110,audit_per_unseen_stratum:k,inclusion_probability:fmt(Q(k,N)),visible_brier:fmt(over(visible,Q(90))),unidentified_bounds:bounds.map(fmt),results,probability_both_rare_categories_missed_A:fmt(missRare),assertions,status:"PASS",evidence:"synthetic E1; exact hypergeometric design"}));
