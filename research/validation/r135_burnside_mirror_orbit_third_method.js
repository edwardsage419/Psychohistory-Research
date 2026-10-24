(function () {
"use strict";
// R135 third method. Node.js standard library only, exact finite group action.
const assert=(v,msg)=>{if(!v)throw new Error(msg);};
const bits=(n,width)=>Array.from({length:width},(_,i)=>(n>>(width-1-i))&1);
const number=(b)=>b.reduce((a,v)=>2*a+v,0);
function mirrorNorm(n){
 const b=bits(n,8),out=Array(8);
 for(let i=0;i<8;i++){
  const counterpart=2*(3-Math.floor(i/2))+(i%2);
  out[i]=1-b[counterpart];
 }
 return number(out);
}
function mirrorStrategy(s){
 const b=bits(s,4);
 return number([b[3],b[2],b[1],b[0]]);
}
function mirror(id){
 const n=Math.floor(id/16),s=id%16;
 return 16*mirrorNorm(n)+mirrorStrategy(s);
}
const seen=new Set(), fixed=[], sizeCounts={one:0,two:0};
let involutionChecks=0,images=new Set();
for(let id=0;id<4096;id++){
 const target=mirror(id);
 assert(target>=0&&target<4096,"image out of range");
 images.add(target);
 assert(mirror(target)===id,"involution broken");
 involutionChecks++;
 if(target===id)fixed.push(id);
 if(!seen.has(id)){
  seen.add(id);
  if(target===id)sizeCounts.one++;
  else {seen.add(target);sizeCounts.two++;}
 }
}
assert(images.size===4096&&seen.size===4096,"not a bijection");
const fixedNorms=Array.from({length:256},(_,n)=>n).filter(n=>mirrorNorm(n)===n).length;
const fixedStrategies=Array.from({length:16},(_,s)=>s).filter(s=>mirrorStrategy(s)===s).length;
const burnside=(4096+fixedNorms*fixedStrategies)/2;
assert(fixedNorms===16&&fixedStrategies===4,"fixed point formula mismatch");
assert(fixed.length===64&&sizeCounts.one===64&&sizeCounts.two===2016&&burnside===2080,"orbit count mismatch");
assert(sizeCounts.one+sizeCounts.two===burnside,"Burnside mismatch");
// Wrong variants must disagree with the prespecified bit transformation.
const wrongStrategy=number(bits(0,4).reverse().map(v=>1-v));
const wrongNorm=number(bits(0,8).map((_,i)=>bits(0,8)[2*(3-Math.floor(i/2))+(i%2)]));
const negative={strategy_output_inversion_rejected:wrongStrategy!==mirrorStrategy(0),
  norm_output_complement_omission_rejected:wrongNorm!==mirrorNorm(0)};
assert(Object.values(negative).every(Boolean),"negative controls escaped");
const result={research_id:"R135",date:"2026-10-25",
 source:"Ohtsuki and Iwasa 2004 DOI 10.1016/j.jtbi.2004.06.005",
 scope:"binary_reputation_mirror_orbits_internal_E1_only",all_norms:256,all_strategies:16,
 universe:4096,involution_checks:involutionChecks,unique_images:images.size,
 fixed_norms:fixedNorms,fixed_strategies:fixedStrategies,fixed_pairs:fixed.length,
 orbit_size_one:sizeCounts.one,orbit_size_two:sizeCounts.two,burnside_orbits:burnside,
 negative_controls:negative,original_R135_ESS_61440_reexecuted_this_run:false,
 new_E2:0,new_E3:0,CI_run_this_turn:false};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");
 fs.writeFileSync("R135_BURNSIDE_MIRROR_ORBIT_RECEIPT_2026-10-25.json",JSON.stringify(result,null,2)+"\n");
 console.log(JSON.stringify(result,null,2));
}
return result;
})()
