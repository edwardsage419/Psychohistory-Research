"use strict";
// Exact three-time identification for R154 frozen 100 synthetic worlds.
// Node.js standard library only, no file/network dependencies.
function r154Identifiability(){
 const A0s=[0,2,6,10],vals=[0,1,2,3,4],groups2=new Map(),groups3=new Map(),rows=[];
 let nonstationary=0,stationary=0,exactInversion=0,mutantDetected=0;
 for(const a of A0s)for(const p of vals)for(const q of vals){
   const A1_4=(4-p)*a+q*(10-a);
   const A2_16=(4-p)*A1_4+q*(40-A1_4);
   const key2=`${a}|${A1_4}`,key3=`${a}|${A1_4}|${A2_16}`;
   for(const [map,key] of [[groups2,key2],[groups3,key3]]){if(!map.has(key))map.set(key,[]);map.get(key).push([p,q])}
   const d0=BigInt(A1_4-4*a),d1=BigInt(A2_16-4*A1_4);
   if(d0!==0n){
     nonstationary++;
     const sn=4n*d0-d1,sd=4n*d0;
     const qn=d0*sd+4n*BigInt(a)*sn,qd=40n*sd;
     const pn=sn*qd-qn*sd,pd=sd*qd;
     if(4n*qn!==BigInt(q)*qd||4n*pn!==BigInt(p)*pd)throw Error("exact inversion failed");
     exactInversion++;
   }else stationary++;
   const A2_wrong=(4-p)*A1_4+q*(4*(10-a));
   if(A2_wrong!==A2_16)mutantDetected++;
   rows.push({a0:a,p_num_over4:p,q_num_over4:q,A1_times4:A1_4,A2_times16:A2_16,stationary:d0===0n});
 }
 const stats=map=>{const sizes=[...map.values()].map(v=>v.length);return{classes:sizes.length,unique_classes:sizes.filter(x=>x===1).length,ambiguous_classes:sizes.filter(x=>x>1).length,ambiguous_worlds:sizes.filter(x=>x>1).reduce((a,b)=>a+b,0),max_class_size:Math.max(...sizes)}};
 const s2=stats(groups2),s3=stats(groups3);
 const nonstationary3unique=rows.filter(r=>!r.stationary).every(r=>groups3.get(`${r.a0}|${r.A1_times4}|${r.A2_times16}`).length===1);
 const nonstationary2ambiguous=rows.filter(r=>!r.stationary).some(r=>groups2.get(`${r.a0}|${r.A1_times4}`).length>1);
 if(rows.length!==100||exactInversion!==nonstationary||!nonstationary3unique||!nonstationary2ambiguous||mutantDetected===0||stationary===0)throw Error("frozen gate fail");
 return{research_id:"R154",evidence:"E1_INTERNAL_BOUNDED",worlds:rows.length,nonstationary_worlds:nonstationary,stationary_worlds:stationary,exact_inversion_verified:exactInversion,three_time_nonstationary_unique:nonstationary3unique,two_time_nonstationary_ambiguity_detected:nonstationary2ambiguous,wrong_stale_B_mutant_detected_worlds:mutantDetected,two_time:s2,three_time:s3,stationary_classes:[...groups3.entries()].filter(([k,v])=>v.length>1).map(([k,v])=>({signature:k,pq_pairs_quarters:v})),rows};
}
process.stdout.write(JSON.stringify(r154Identifiability(),null,2)+"\n");
