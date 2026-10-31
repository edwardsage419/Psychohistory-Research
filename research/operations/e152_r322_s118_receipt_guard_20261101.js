// E152 strict archived R322 S118 60-cell receipt guard, read-only.
function e152Check(j){
 const strata=["all","r0","r1","gate_all"],noise=["0","1/4","1/2"],obs=["behavior_full","behavior_partial","behavior_only","label_only","label_full"];
 const gcd=(a,b)=>b?gcd(b,a%b):a,frac=(n,d)=>{const g=gcd(n,d);return d/g===1?String(n/g):`${n/g}/${d/g}`};
 if(j.schema!=="R322_S118_EXACT_OBSERVATION_LABEL_NOISE_E1_v1"||j.frozen_original_source_blob!=="0cd38ecc22adc5941832c2b00e6928d48be8d896"||j.evidence!=="E1_NONBLIND_INTERNAL_ONLY"||j.source_rows!==256||!Array.isArray(j.cells)||j.cells.length!==60)throw Error("receipt identity/coverage");
 let index=0;
 for(const s of strata)for(const eps of noise)for(const o of obs){
  const c=j.cells[index++];if(c.stratum!==s||c.noise_flip!==eps||c.observation!==o)throw Error("key/order "+index);
  const states=[];
  for(let h=0;h<2;h++)for(let a=0;a<2;a++)for(let y=0;y<2;y++)for(let d=0;d<2;d++)for(let r=0;r<2;r++)for(let w=0;w<2;w++){
   if((s==="r0"&&r!==0)||(s==="r1"&&r!==1)||(s==="gate_all"&&!(d&&r&&w)))continue;
   const gate=Number(h!==a&&d&&r&&w);states.push({h,a,d,r,w,gate,out:gate?a:h});
  }
  const key=(v,l)=>o==="behavior_full"?[v.h,v.a,v.d,v.r,v.w,v.out].join("|"):o==="behavior_partial"?[v.h,v.a,v.out].join("|"):o==="behavior_only"?String(v.out):o==="label_only"?[v.out,l].join("|"):[v.h,v.a,v.d,v.r,v.w,v.out,l].join("|");
  const supports=[0,1].map(p=>{const set=new Set();for(const v of states){const l=p===0?v.gate:0;if(o.startsWith("behavior_"))set.add(key(v,0));else{set.add(key(v,l));if(eps!=="0")set.add(key(v,1-l))}}return set.size});
  const gateCount=states.filter(v=>v.gate).length,k=eps==="0"?0:eps==="1/4"?1:2,n=o.startsWith("behavior_")?0:gateCount*(2-k),den=2*states.length;
  if(c.total_variation!==frac(n,den)||c.bayes_accuracy!==frac(den+n,2*den)||c.support_gated!==supports[0]||c.support_lookup!==supports[1])throw Error("score/support "+index);
 }
 return index;
}
function e152Selftest(j){
 const changes=[["duplicate",x=>x.cells[1]=x.cells[0]],["missing",x=>x.cells.pop()],["reorder",x=>[x.cells[0],x.cells[1]]=[x.cells[1],x.cells[0]]],["tv",x=>x.cells[3].total_variation="0"],["support",x=>x.cells[3].support_gated++],["grade",x=>x.evidence="E3"],["blob",x=>x.frozen_original_source_blob="bad"]];
 const cells=e152Check(j),rejected=[];for(const [n,mut] of changes){const x=JSON.parse(JSON.stringify(j));mut(x);let caught=false;try{e152Check(x)}catch(e){caught=true}if(!caught)throw Error("false accept "+n);rejected.push(n)}
 return {cells,rejected,scope:"nonblind E1 receipt check; no native Node CLI"};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");if(!process.argv[2])throw Error("usage: node e152_r322_s118_receipt_guard_20261101.js receipt.json");console.log(JSON.stringify(e152Selftest(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}
