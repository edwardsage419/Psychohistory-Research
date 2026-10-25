/* R152 third-method exact stochastic-order audit. E1 synthetic only.
   Run: node r152_distance_stochastic_order_third_method.js */
"use strict";
const P=[2,3,5,7], L={near:[0,1,3,6],far:[0,1,3,9]},
 A={flat:[1,1,1,1],mid_bonus:[1,1,2,1],last_bonus:[1,1,1,2]},
 B=["pop_10","pop_5","half"], pairs=[[0,1],[1,2],[0,2]];
function gcd(a,b){while(b){[a,b]=[b,a%b]}return a}
function f(n,d){if(d<=0n)throw Error("denominator");let g=gcd(n<0n?-n:n,d);return [String(n/g),String(d/g)]}
function q(coords,att,i,alpha,reverse=false){
 let js=[0,1,2,3].filter(j=>j!==i),dist=js.map(j=>Math.abs(coords[i]-coords[j]));
 let pow=dist.map(d=>BigInt(d)**BigInt(alpha)),common=pow.reduce((a,b)=>a*b,1n);
 let w=js.map((j,k)=>BigInt(P[j]*att[j])*(reverse?pow[k]:common/pow[k]));
 return {dist,w,z:w.reduce((a,b)=>a+b,0n)};
}
function cdf(q,d){return q.w.reduce((a,b,k)=>a+(q.dist[k]<=d?b:0n),0n)}
function budget(i,mode){return mode==="pop_10"?[BigInt(P[i]),10n]:mode==="pop_5"?[BigInt(P[i]),5n]:[1n,2n]}
function main(){
 let rows=[],cdfN=0,strictN=0,oddsN=0,mutants=0,budgetN=0;
 for(let [layout,coords] of Object.entries(L))for(let [attraction,att] of Object.entries(A))
 for(let i=0;i<4;i++){
   for(let [lo,hi] of pairs){
     let a=q(coords,att,i,lo),b=q(coords,att,i,hi),ts=[...new Set(a.dist)].sort((x,y)=>x-y).slice(0,-1);
     let checks=[],strict=0,odds=0;
     for(let d of ts){
       let na=cdf(a,d),nb=cdf(b,d),delta=nb*a.z-na*b.z;
       if(delta<0n)throw Error("CDF dominance violated");
       if(delta>0n){strict++;strictN++}
       cdfN++;checks.push({threshold:d,cdf_low:f(na,a.z),cdf_high:f(nb,b.z),gap:f(delta,a.z*b.z)});
     }
     if(strict===0)throw Error("strict threshold absent");
     for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){
       if(a.dist[j]===a.dist[k]){
         if(b.w[j]*a.w[k]!==b.w[k]*a.w[j])throw Error("tied distance odds changed");
       }else{
         let near=a.dist[j]<a.dist[k]?j:k,far=a.dist[j]<a.dist[k]?k:j;
         if(b.w[near]*a.w[far]<=b.w[far]*a.w[near])throw Error("odds reversed");
         odds++;oddsN++;
       }
     }
     for(let mode of B)rows.push({layout,attraction,budget:mode,origin:i,alpha_low:lo,alpha_high:hi,thresholds:checks,strict_thresholds:strict,odds_checks:odds});
     if(lo===0&&hi===1){
       let wrong=q(coords,att,i,1,true),d=ts[0];
       if(cdf(wrong,d)*a.z-cdf(a,d)*wrong.z>=0n)throw Error("inverse exponent mutant survived");
       mutants+=3;
     }
   }
   for(let alpha of [0,1,2]){
     let route=q(coords,att,i,alpha);
     for(let [b1,b2] of [[B[0],B[1]],[B[0],B[2]],[B[1],B[2]]]){
       let [n1,d1]=budget(i,b1),[n2,d2]=budget(i,b2);
       for(let w of route.w){
         if(f(n1*w*d1,d1*route.z*n1).join("/")!==f(n2*w*d2,d2*route.z*n2).join("/"))throw Error("budget invariant failed");
       }
       budgetN++;
     }
   }
 }
 if(rows.length!==216||cdfN!==135||oddsN!==207||mutants!==72||budgetN!==216)throw Error("coverage mismatch: "+[rows.length,cdfN,oddsN,mutants,budgetN]);
 return {id:"R152_DISTANCE_FOSD_THIRD_METHOD",evidence:"E1_SYNTHETIC_ONLY",rows_count:rows.length,unique_cdf_checks:cdfN,strict_cdf_checks:strictN,unique_odds_checks:oddsN,mutant_cases_rejected:mutants,budget_route_checks:budgetN,all_pass:true,external_replication:false,rows};
}
if(typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(main(),null,2)+"\n");
