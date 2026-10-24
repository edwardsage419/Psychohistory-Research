"use strict";
// R138 B-audit: separate JavaScript direct welfare proof and externality audit.
// Synthetic bounded types only. Execute: node r138_b_independent_groves_welfare_audit.js
function profiles(levels,n) {
  let out=[[]];
  for(let i=0;i<n;i++){let next=[];for(const a of out)for(const b of levels)next.push([...a,b]);out=next}
  return out;
}
const allocations=[];
for(let a=-1;a<3;a++)for(let b=-1;b<3;b++)if(a<0||b<0||a!==b)allocations.push([a,b]);
if(allocations.length!==13)throw Error("invalid allocation universe");
function welfare(types,allocation) {
  let total=0;
  for(let item=0;item<2;item++)if(allocation[item]>=0)total+=types[allocation[item]][item];
  return total;
}
function efficient(types) {
  let best=-1, alloc=null;
  for(const a of allocations){const w=welfare(types,a);if(w>best){best=w;alloc=a}}
  return [best,alloc];
}
function pivot(types,agent,allocation) {
  const others=types.map((t,i)=>i===agent?[0,0]:t);
  const outside=efficient(others)[0];
  let realized=0;
  for(let item=0;item<2;item++)if(allocation[item]>=0&&allocation[item]!==agent)realized+=types[allocation[item]][item];
  return outside-realized;
}
function main() {
  const types=profiles([0,1,2],2), worlds=profiles(types,3);
  let deviations=0,grovesViolations=0,welfareViolations=0,negativeTax=0,truthfulIR=0;
  for(const trueTypes of worlds){
    const [optimum,truthAlloc]=efficient(trueTypes);
    for(let i=0;i<3;i++){
      const trueTax=pivot(trueTypes,i,truthAlloc);
      let ownValue=0;
      for(let item=0;item<2;item++)if(truthAlloc[item]===i)ownValue+=trueTypes[i][item];
      const honest=ownValue-trueTax;
      if(honest<0)truthfulIR++;
      if(trueTax<0)negativeTax++;
      for(const reported of types){
        const claims=trueTypes.slice();claims[i]=reported;
        const [,alloc]=efficient(claims);
        const actualWelfare=welfare(trueTypes,alloc);
        if(actualWelfare>optimum)welfareViolations++;
        const tax=pivot(claims,i,alloc);
        let actualValue=0;
        for(let item=0;item<2;item++)if(alloc[item]===i)actualValue+=trueTypes[i][item];
        if(actualValue-tax>honest)grovesViolations++;
        deviations++;
      }
    }
  }
  const result={method:"independent_js_direct_13_allocation_groves_welfare_audit",allocation_count:allocations.length,worlds:worlds.length,deviations,grovesViolations,welfareViolations,negativeTax,truthfulIR,evidence:"internal_E1_only"};
  if(deviations!==19683||grovesViolations||welfareViolations||negativeTax||truthfulIR)throw Error(JSON.stringify(result));
  return result;
}
const result=main();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
