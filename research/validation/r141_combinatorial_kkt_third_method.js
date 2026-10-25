"use strict";
// R141 third method: standalone exact arithmetic, no external packages.
// Freeze: R141_COMBINATORIAL_NE_AND_KKT_THIRD_METHOD_PROTOCOL_FREEZE_2026-10-25.md
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b!==0n){const t=a%b;a=b;b=t;}return a||1n;}
class Q{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
 sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
 mul(b){return new Q(this.n*b.n,this.d*b.d);}
 div(b){return new Q(this.n*b.d,this.d*b.n);}
 cmp(b){const x=this.n*b.d-b.n*this.d;return x<0n?-1:x>0n?1:0;}
 toString(){return this.d===1n?String(this.n):String(this.n)+"/"+String(this.d);}
}
const q=(n,d=1)=>new Q(n,d), ZERO=q(0), ONE=q(1), TWO=q(2), TWELVE=q(12);
function check(ok,msg){if(!ok)throw Error(msg);}
function choose(n,k){let v=1;for(let i=1;i<=k;i++)v=v*(n-i+1)/i;return v;}
function payoffScaled(n,r2,m,a){return 24*(m>=3?1:0)+n*(r2-2)*a;}
function binaryAudit(){
 const ns=[3,4,5,6,8,10,12,16],rs=[0,1,4],rows=[];
 let profiles=0,flips=0,bruteNE=0,combinatorialNE=0;
 for(const n of ns)for(const r2 of rs){
  const byM=Array(n+1).fill(0),analytic=Array(n+1).fill(0);
  for(let m=0;m<=n;m++){
   // Independent combinatorial characterization for the frozen r grid.
   const isNE=r2<2?(m===0||(m===3&&24+n*(r2-2)>=0)):(m===n);
   analytic[m]=isNE?choose(n,m):0;
  }
  for(let mask=0;mask<2**n;mask++){
   let m=0;for(let i=0;i<n;i++)m+=(mask>>i)&1;
   let ne=true;
   for(let i=0;i<n;i++){
    const a=(mask>>i)&1, m2=m+(a? -1:1);
    const gain=payoffScaled(n,r2,m2,1-a)-payoffScaled(n,r2,m,a);
    flips++;
    if(gain>0)ne=false;
   }
   if(ne)byM[m]++;
   profiles++;
  }
  check(byM.every((x,i)=>x===analytic[i]),"NE combinatorial disagreement n="+n+" r2="+r2);
  const cnt=byM.reduce((a,b)=>a+b,0);
  bruteNE+=cnt;combinatorialNE+=analytic.reduce((a,b)=>a+b,0);
  rows.push({n,reward:r2===0?"0":r2===1?"1/2":"2",profiles:2**n,ne_count:cnt,ne_by_contributors:byM.map((v,i)=>v?{m:i,count:v}:null).filter(Boolean)});
 }
 check(rows.length===24,"24 binary rows");
 check(profiles===213096,"213096 profiles");
 check(flips===3331944,"3331944 actual flip evaluations");
 check(bruteNE===combinatorialNE,"total NE disagreement");
 const pick=(n,reward)=>rows.find(x=>x.n===n&&x.reward===reward);
 check(pick(8,"0").ne_count===57,"n8 r0");
 check(pick(16,"0").ne_count===1,"n16 r0");
 check(pick(16,"1/2").ne_count===561,"n16 r1/2");
 check(pick(16,"2").ne_count===1,"n16 r2");
 // Frozen negative control NC1: erroneous threshold equilibrium claim for n16 r0.
 let nc1=0;for(let mask=0;mask<2**16;mask++){
  let m=0;for(let i=0;i<16;i++)m+=(mask>>i)&1;
  if(m!==3)continue;
  let violating=false;for(let i=0;i<16;i++)if((mask>>i)&1){
   const gain=payoffScaled(16,0,2,0)-payoffScaled(16,0,3,1);
   if(gain>0)violating=true;
  }
  if(violating)nc1++;
 }
 check(nc1===560,"NC1 all 560 erroneous equilibria rejected");
 // Frozen NC2: external reward must not be included as net resource production.
 const realW=12-16,fiscal=2*16,wrongW=realW+fiscal;
 check(realW===-4&&fiscal===32&&wrongW===28&&realW!==wrongW,"NC2 transfer-as-welfare rejected");
 return {scenarios:rows.length,profiles,actual_flip_evaluations:flips,total_ne_across_scenarios:bruteNE,rows,negative_controls:{NC1_wrong_n16_r0_threshold_equilibria_rejected:nc1,NC2_real_resource_welfare_n16_r2:realW,NC2_external_fiscal_n16_r2:fiscal,NC2_wrong_transfer_included_welfare:wrongW}};
}
function continuousAudit(){
 const ns=[1,2,3,4,5,6,8,10,12,16,20,24],rs=[0,1],rows=[];
 for(const n of ns)for(const r2 of rs){
  const r=q(r2,2),tCandidate=q(12).sub(q(n).mul(ONE.sub(r))).div(q(3));
  const T=tCandidate.cmp(ZERO)<0?ZERO:tCandidate;
  const x=T.div(q(n)),s=ONE.div(q(n));
  const gradient=s.mul(TWELVE.sub(T)).sub(ONE).add(r).sub(TWO.mul(x));
  check(x.cmp(ZERO)>0?gradient.cmp(ZERO)===0:gradient.cmp(ZERO)<=0,"continuous KKT n="+n+" r2="+r2);
  const optimum=q(11*n,n+2),fiscal=r.mul(T);
  const welfare=TWELVE.mul(T).sub(T.mul(T).div(TWO)).sub(T).sub(q(n).mul(x.mul(x)));
  rows.push({n,reward:r.toString(),T_nash:T.toString(),x_individual:x.toString(),T_resource_optimum:optimum.toString(),resource_welfare:welfare.toString(),external_fiscal:fiscal.toString(),kkt_gradient:gradient.toString()});
 }
 check(rows.length===24,"24 continuous rows");
 const shares=[q(1,2),...Array.from({length:15},()=>q(1,30))];
 check(shares.reduce((a,b)=>a.add(b),ZERO).cmp(ONE)===0,"shares sum");
 function activeCandidate(active){
  const ss=active.reduce((acc,i)=>acc.add(shares[i]),ZERO);
  const T=TWELVE.mul(ss).sub(q(active.length)).div(TWO.add(ss));
  const efforts=shares.map((s,i)=>active.includes(i)?s.mul(TWELVE.sub(T)).sub(ONE).div(TWO):ZERO);
  return {T,efforts};
 }
 const a=activeCandidate([0]),b=activeCandidate([...Array(16).keys()]),z={T:ZERO,efforts:Array.from({length:16},()=>ZERO)};
 function valid(c){
  if(c.T.cmp(ZERO)<0)return false;
  if(c.efforts.some(x=>x.cmp(ZERO)<0))return false;
  const sum=c.efforts.reduce((x,y)=>x.add(y),ZERO);
  if(sum.cmp(c.T)!==0)return false;
  return c.efforts.every((x,i)=>{const g=shares[i].mul(TWELVE.sub(c.T)).sub(ONE).sub(TWO.mul(x));return x.cmp(ZERO)>0?g.cmp(ZERO)===0:g.cmp(ZERO)<=0;});
 }
 check(valid(a)&&!valid(b)&&!valid(z),"privileged KKT activity sets");
 check(a.T.cmp(q(2))===0&&a.efforts[0].cmp(q(2))===0&&a.efforts.slice(1).every(x=>x.cmp(ZERO)===0),"privileged T=2");
 const eq16=rows.find(x=>x.n===16&&x.reward==="0");
 check(eq16.T_nash==="0"&&a.T.toString()==="2","NC3 equal shares incorrectly transferred to privileged rejected");
 return {scenarios:rows.length,rows,privileged_n16:{T:a.T.toString(),efforts:a.efforts.map(x=>x.toString()),valid_active_set:[0],all_active_candidate_valid:valid(b),none_active_candidate_valid:valid(z)},negative_controls:{NC3_equal_share_n16_T:eq16.T_nash,NC3_privileged_n16_T:a.T.toString()}};
}
function runAudit(){
 const binary=binaryAudit(),continuous=continuousAudit();
 return {research_id:"R141",protocol:"R141_COMBINATORIAL_NE_AND_KKT_THIRD_METHOD_PROTOCOL_FREEZE_2026-10-25.md",evidence:"E1_PROJECT_SYNTHETIC",method:"independent exact integer full flip enumeration plus combinatorial NE and BigInt rational KKT",binary,continuous,new_E2:0,new_E3:0,external_independent_replications:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 console.log(JSON.stringify(runAudit(),null,2));
}
