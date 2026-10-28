"use strict";
// Pure enumeration demonstration; this does NOT execute Google OR-Tools.
const audit=function marketAudit(){
  const rules={
    A:x=>x>=7,
    B:x=>x<=5,
    C:x=>x<=9,
    D:x=>x>=0
  };
  const keys=Object.keys(rules), universe=Array.from({length:11},(_,i)=>i);
  const evaluate=selected=>universe.filter(x=>selected.every(k=>rules[k](x)));
  let checks=0, infeasible=[];
  for(let mask=0;mask<16;mask++){
    let selected=keys.filter((_,i)=>mask&(1<<i));
    let feasible=evaluate(selected);
    let shouldEmpty=selected.includes("A")&&selected.includes("B");
    if((feasible.length===0)!==shouldEmpty)throw Error("subset logic mismatch "+selected);
    checks++;
    if(!feasible.length)infeasible.push(selected);
  }
  const minimal=infeasible.filter(set=>set.every(k=>evaluate(set.filter(z=>z!==k)).length>0));
  if(minimal.length!==1||minimal[0].join(",")!=="A,B")throw Error("MUS incorrect");
  checks+=2;
  const actions={OPTIMAL:"DISPLAY_FEASIBLE_CANDIDATE_REQUIRES_AUTHORIZATION",FEASIBLE:"DISPLAY_NONOPTIMAL_CANDIDATE_REQUIRES_AUTHORIZATION",INFEASIBLE:"REJECT_EXECUTION_AND_EXPLAIN_CONFLICT",MODEL_INVALID:"REJECT_MODEL_AND_FIX_INPUT",UNKNOWN:"ABSTAIN_AND_REQUEST_RECHECK"};
  if(new Set(Object.values(actions)).size!==5)throw Error("status conflation");checks++;
  return {checks,infeasible_subsets:infeasible.length,minimal_core:minimal[0],actions};
};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit};
