/* Research prototype. Node.js >=18. Synthetic cases, not native PR execution. */
function experiment(){
 const graph={G:[],P:["G"],W:["P"],R:["G"],T:["G"],I:["G","T"]};
 // Synthetic planned graph; G is mandatory. Real method edges remain the registry's authority.
 function closurePlan(graph,roots,admitted=new Set(Object.keys(graph))){
  const order=[],blocked={},done=new Set();
  for(const root of ["G",...new Set(roots)]){
   const local=[],visiting=new Set(),visited=new Set();
   function visit(k){
    if(!Object.hasOwn(graph,k))throw Error("MISSING:"+k);
    if(!admitted.has(k))throw Error("NOT_ADMITTED:"+k);
    if(visiting.has(k))throw Error("CYCLE:"+k);
    if(visited.has(k))return;
    visiting.add(k);for(const d of graph[k])visit(d);
    visiting.delete(k);visited.add(k);local.push(k);
   }
   try{visit(root);for(const k of local)if(!done.has(k)){done.add(k);order.push(k)}}catch(e){blocked[root]=e.message}
  }
  // Mandatory gate must be valid for any decision calculation.
  if(blocked.G)return {order:[],blocked};
  return {order,blocked};
 }
 // Independent closure oracle using monotone fixed point and direct precedence check.
 function required(g,roots){
  const s=new Set(["G",...roots]);let changed=true;
  while(changed){changed=false;for(const k of [...s])for(const d of g[k])if(!s.has(d)){s.add(d);changed=true}}
  return [...s].sort().join(",");
 }
 const graphRows=[];
 const nodes=Object.keys(graph).filter(x=>x!=="G");
 for(let mask=0;mask<2**nodes.length;mask++){
  const roots=nodes.filter((_,i)=>mask&(1<<i));
  const a=closurePlan(graph,roots),pos=Object.fromEntries(a.order.map((v,i)=>[v,i]));
  if(Object.keys(a.blocked).length||[...a.order].sort().join(",")!==required(graph,roots)||a.order.some(k=>graph[k].some(d=>!(pos[d]<pos[k]))))throw Error("closure");
  graphRows.push({roots,plan:a.order,all_registry_attempts:Object.keys(graph).length,selected_attempts:a.order.length});
 }
 const bad={...graph,C:["D"],D:["C"],M:["absent"],V:["G"],Z:["C"]};
 const admitted=new Set(Object.keys(bad).filter(x=>x!=="V"));
 const faultSpecs=[
  {roots:["P"],ok:["G","P"],blocked:[]},
  {roots:["P","C"],ok:["G","P"],blocked:["C"]},
  {roots:["I","Z"],ok:["G","T","I"],blocked:["Z"]},
  {roots:["R","M"],ok:["G","R"],blocked:["M"]},
  {roots:["W","V"],ok:["G","P","W"],blocked:["V"]},
  {roots:["M","C","V","I"],ok:["G","T","I"],blocked:["M","C","V"]},
  {roots:["absent","P"],ok:["G","P"],blocked:["absent"]},
  {roots:["P"],ok:[],blocked:["G"],gateMissing:true}
 ];
 const faultRows=faultSpecs.map(s=>{
  const a=closurePlan(bad,s.roots,s.gateMissing?new Set([...admitted].filter(x=>x!=="G")):admitted);
  if(a.order.join(",")!==s.ok.join(",")||s.blocked.some(x=>!Object.hasOwn(a.blocked,x))||(!s.gateMissing&&Object.keys(a.blocked).length!==s.blocked.length))throw Error("fault "+JSON.stringify({s,a}));
  return {...s,actual:a};
 });
 // Typed edges. A result may be an EXECUTED report with a mathematical UNKNOWN.
 // Unknown-aware consumers are allowed to use that result only as UNKNOWN, never as a point.
 const edgeRows=[];
 for(const port of ["resolved_numeric","unknown_aware"])for(let m=0;m<64;m++){
  const [executed,resolved,revision,scope,unit,evidence]=Array.from({length:6},(_,i)=>!!(m&(1<<i)));
  const parent={executed,resolved,revision,scope,unit,evidence};
  const old=executed; // existing dependency loop checks membership of executed
  const reason=!executed?"UPSTREAM_NOT_EXECUTED":!revision?"STALE":!scope?"SCOPE_MISMATCH":!unit?"UNIT_MISMATCH":!evidence?"EVIDENCE_UNQUALIFIED":!resolved&&port==="resolved_numeric"?"UNKNOWN_OUTPUT":null;
  const candidate=reason===null;
  const expected=port==="resolved_numeric"?m===63:(m===61||m===63);
  if(candidate!==expected)throw Error("typed edge");
  edgeRows.push({port,parent,baseline_allows:old,candidate_allows:candidate,reason,expected});
 }
 // Compare criteria without assuming probabilities: exact integer utility grid.
 const eq=(a,b)=>a.join(",")===b.join(",");
 const leaders=(a,b,maximize)=>a===b?["A","B"]:((a>b)===maximize?["A"]:["B"]);
 const ruleRows=[];let example=null;
 for(let a=0;a<=4;a++)for(let b=0;b<=4;b++)for(let c=0;c<=4;c++)for(let d=0;d<=4;d++){
  const u=[[a,b],[c,d]];
  const ceiling=[Math.max(a,c),Math.max(b,d)];
  const worst=u.map(x=>Math.max(ceiling[0]-x[0],ceiling[1]-x[1]));
  const floors=u.map(x=>Math.min(...x));
  const mr=leaders(...worst,false),mm=leaders(...floors,true);
  // Independent direct two-action regret expression.
  const check=leaders(Math.max(0,c-a,d-b),Math.max(0,a-c,b-d),false);
  if(!eq(mr,check))throw Error("regret");
  const relation=eq(mr,mm)?"AGREE":mr.some(x=>mm.includes(x))?"DIFFERENT_CRITERIA_OVERLAP":"DIFFERENT_CRITERIA_DISJOINT";
  const row={u,worst,floors,mr,mm,relation};ruleRows.push(row);
  if(a===0&&b===4&&c===1&&d===1)example=row;
 }
 // Typed comparison distinguishes incompatibility from a same-context disagreement.
 function compare(a,b){
  if(a.revision!==b.revision)return "STALE";
  if(a.scope!==b.scope||a.unit!==b.unit||a.horizon!==b.horizon||a.target!==b.target||a.scenarios!==b.scenarios)return "DIFFERENT_CONTEXT";
  if(a.criterion!==b.criterion)return "DIFFERENT_CRITERIA";
  if(a.assumptions!==b.assumptions)return "DIFFERENT_ASSUMPTIONS";
  if(!a.resolved||!b.resolved)return "UNRESOLVED";
  return eq([...a.leaders].sort(),[...b.leaders].sort())?"AGREE":"SAME_CONTRACT_DISAGREEMENT";
 }
 const template={revision:1,scope:"A,B",unit:"u",horizon:"1yr",target:"choice",scenarios:"s1,s2",criterion:"regret",assumptions:"point",resolved:true,leaders:["A"]};
 const comparisonSpecs=[
  [{}, "AGREE"],[{leaders:["B"]},"SAME_CONTRACT_DISAGREEMENT"],[{leaders:["A","B"]},"SAME_CONTRACT_DISAGREEMENT"],
  [{revision:2,leaders:["B"]},"STALE"],[{scope:"A,C"},"DIFFERENT_CONTEXT"],[{unit:"money"},"DIFFERENT_CONTEXT"],
  [{horizon:"2yr"},"DIFFERENT_CONTEXT"],[{target:"investigate"},"DIFFERENT_CONTEXT"],[{scenarios:"s1,s3"},"DIFFERENT_CONTEXT"],
  [{criterion:"maximin",leaders:["B"]},"DIFFERENT_CRITERIA"],[{assumptions:"interval"},"DIFFERENT_ASSUMPTIONS"],
  [{resolved:false,leaders:[]},"UNRESOLVED"]
 ];
 const comparisonRows=comparisonSpecs.map(([delta,expected])=>{const actual=compare(template,{...template,...delta});if(actual!==expected)throw Error("comparison");return {delta,expected,actual}});
 const aggregate=(rs,k)=>rs.reduce((m,x)=>(m[x[k]]=(m[x[k]]||0)+1,m),{});
 return {graph:{cases:graphRows.length,baseline_attempts:graphRows.reduce((s,x)=>s+x.all_registry_attempts,0),candidate_attempts:graphRows.reduce((s,x)=>s+x.selected_attempts,0),rows:graphRows},faults:{cases:faultRows.length,rows:faultRows},edges:{cases:edgeRows.length,baseline_allows:edgeRows.filter(x=>x.baseline_allows).length,candidate_allows:edgeRows.filter(x=>x.candidate_allows).length,baseline_false_allows:edgeRows.filter(x=>x.baseline_allows&&!x.expected).length,candidate_false_allows:edgeRows.filter(x=>x.candidate_allows&&!x.expected).length,rows:edgeRows},criteria:{cases:ruleRows.length,counts:aggregate(ruleRows,"relation"),example,rows:ruleRows},comparisons:{cases:comparisonRows.length,rows:comparisonRows}};
}
console.log(JSON.stringify(experiment(),null,2));
